.. _rfc-86:

=============================================================
RFC 86: 벡터 레이어 용 열 지향 읽기 API
=============================================================

======= ==========================
저자:   이벤 루올
연락처: even.rouault@spatialys.com
제안일: 2022년 5월 24일
수정일: 2022년 6월 14일
상태:   승인
대상:   GDAL 3.6버전
======= ==========================

요약
----

이 RFC는 :cpp:class:`OGRLayer` 클래스에 열 지향(column-oriented) 메모리 레이아웃을 가진 피처를 배치(batch)로 가져올 수 있는 새 메소드들을 추가할 것을 제안합니다. 이런 메소드는 특히 `아파치 애로우(Apache Arrow) <https://arrow.apache.org/docs/>`_, `Pandas <https://pandas.pydata.org/>`_ / `GeoPandas <https://geopandas.org/>`_ 생태계, `R Spatial <https://rspatial.org/>`_ 패키지, 그리고 열 지향적인 많은 최신 (데이터 분석 중심, 예를 들면 `Snowflake <https://www.snowflake.com/?lang=ko>`_, `Google BigQuery <https://cloud.google.com/bigquery/docs/introduction?hl=ko>`_ 등등) 데이터베이스/엔진과 같은 열 지향 방식으로 데이터를 표현할 것을 예상하는 기관 또는 다운스트림 소비자를 가진 포맷에 적합합니다.

동기
----

현재로서는 피처 정보를 가져오려면 사용자가 C++ 객체를 반환하는 GetNextFeature()로 레이어의 각 피처를 반복해야만 합니다. 이 C++ 객체에 대한 쿼리가 다양한 "get" 메소드를 사용해서 속성 및 도형을 가져옵니다. 바인딩 언어로부터 호출될 때 일반적으로 다른 언어가 네이티브 코드를 호출할 때마다 오버헤드(overhead)가 발생합니다. 즉 피처 N개와 필드 N개로 이루어진 레이어에 대한 모든 정보를 가져오려면 피처 N개 * 필드 N개 횟수의 호출이 필요합니다.
이 오버헤드가 중요합니다. :ref:`rfc-86-benchmarks` 단락을 참조하십시오.

C API의 또다른 불편한 점은 동일 필드의 많은 행들을 수반하는 (예를 들면 필드에 대한 통계를 계산하는) 처리 과정이 가장 효율적인 (벡터화된 CPU 명령을 사용하는) 처리를 위해 RAM에 데이터를 계속 담아둬야 할 수도 있다는 것입니다. 현재의 OGR API는 이를 직접적으로 허용하지 않기 때문에, 사용자가 직접 데이터를 적절한 데이터 구조로 섞어야 합니다.
마찬가지로 앞에서 언급한 프레임워크(애로우, Pandas/GeoPandas)도 이런 메모리 레이아웃을 요구하기 때문에, 현재 OGR로부터 읽어올 때 데이터를 재구성해야 합니다. 예를 들어 `pyogrio <https://github.com/geopandas/pyogrio>`_ 프로젝트가 이런 요구 사항을 해결하려는 시도 가운데 하나입니다.

뿐만 아니라, GDAL 3.5.0버전에 파일 구조가 열 및 배치(batch) 지향적인 :ref:`vector.arrow` 및 :ref:`vector.parquet` 드라이버가 추가되었습니다. 결과적으로 열 지향 API가 이런 포맷들에 대해 최고의 성능을 가능하게 할 것입니다.

상세 사항
---------

새로 제안하는 API는 `아파치 애로우 C 스트림 인터페이스 <https://arrow.apache.org/docs/format/CStreamInterface.html>`_ 를 구현합니다. 이 RFC의 나머지 부분을 더 잘 이해하려면 `아파치 애로우 C 데이터 인터페이스 <https://arrow.apache.org/docs/format/CDataInterface.html>`_ 의 처음 문장들은 물론 문서 전체를 읽어볼 것을 강력하게 권장합니다. (다양한 데이터 유형들에 대한 내용은 건너뛰어도 됩니다.)

애로우 C 스트림 인터페이스는 현재 실험적이라고 표시되어 있지만, 2020년 11월 도입된 이후 버전에 변화가 없으며 이미 애로우 R 바인딩과 DuckDB 간의 인터페이스처럼 ABI에 민감한 위치에서 사용되고 있습니다.

이 인터페이스는 다음을 가져올 수 있는 주요 콜백(callback) 2개를 제공하는 C 구조 및 ArrowArrayStream 집합으로 이루어져 있습니다:

- get_schema() 콜백으로 ArrowSchema를 가져옵니다. ArrowSchema는 필드 설명 집합(이름, 유형, 메타데이터)을 서술합니다. 모든 OGR 데이터 유형에는 각각 대응하는 애로우 데이터 유형이 존재합니다.

- the get_next() 콜백으로 ArrowArray 순열(sequence)을 가져옵니다. ArrowArray는 피처 부분 집합에 있는 특정 열/필드 값의 집합을 수집합니다. 이 순열은 Pandas DataFrame에 있는 `Series <https://arrow.apache.org/docs/python/pandas.html#series>`_ 와 동등합니다.
  이 순열은 하위 배열들을 모두 합할 수 있는 잠재적인 계층 구조로, OGR 사용례에서는 주 배열이 OGR 속성 및 도형 필드의 선택 집합인 StructArray일 것입니다. `애로우 Columnar 포맷 <https://arrow.apache.org/docs/format/Columnar.html>`_ 에서 데이터 유형별 버퍼 및 하위 배열의 레이아웃을 자세하게 설명하고 있습니다.

레이어가 (정수형 하나와 부동소수점형 하나인) 필드 2개를 가지고 있고 피처 4개로 이루어져 있는 경우, 이 레이어를 ArrowArray로 표현하면 '개념적으로' 다음과 같을 것입니다:

.. code-block:: c

    array.children[0].buffers[1] = { 1, 2, 3, 4 };
    array.children[1].buffers[1] = { 1.2, 2.3, 3.4, 4.5 };

전체 레이어의 콘텐츠를 각 레코드 배치가 피처들의 부분 집합의 ArrowArray인 레코드 배치(batch)의 순열로 볼 수 있습니다. 개별 피처들을 반복하는 대신, 한 번에 피처 여러 개로 이루어진 배치를 반복합니다.

아파치 애로우 C++와 API/ABI의 호환성을 확보하기 위해 `애로우 C ABI <https://github.com/apache/arrow/blob/master/cpp/src/arrow/c/abi.h>`_ 로부터 직접 파생된 :file:`ogr_recordbatch.h` 공개 헤더 파일에서 ArrowArrayStream, ArrowSchema, ArrowArray 구조를 정의하고 있습니다. 관련 배열 배치 API를 사용하는 경우 이 헤더 파일을 명확하게 포함시켜야만 합니다.

:cpp:class:`OGRLayer` 클래스에 다음 가상 메소드를 추가합니다:

  .. code-block:: cpp

        virtual bool OGRLayer::GetArrowStream(struct ArrowArrayStream* out_stream,
                                              CSLConstList papszOptions = nullptr);

C API에서도 이 메소드를 OGR_L_GetArrowStream()으로 사용할 수 있습니다.

'out_stream'은 초기화되지 않은 상태일 수 있는 ArrowArrayStream을 가리키는 포인터입니다. (이 메소드는 모든 초기 콘텐츠를 무시할 것입니다.)

반환에 성공해서 스트림 인터페이스가 더 이상 필요없는 경우 ``out_stream->release(out_stream)`` 으로 인터페이스를 해제해야만 합니다.

OGR 맥락에서 고려해야 할 추가적인 예방 조치가 있습니다. 특정 드라이버 구현이 다르게 지정하지 않는 이상, ArrowArrayStream 구조가 초기화되었던 :cpp:class:`OGRLayer` 가 삭제된 후에 (일반적으로 데이터셋 종료 시) ArrowArrayStream 구조 및 ArrowArrayStream의 콜백이 반환한 ArrowSchema 또는 ArrowArray 객체를 (잠재적으로 해제하는 경우를 제외하면) 더 이상 사용해서는 안 됩니다.
뿐만 아니라, 특정 드라이버 구현이 다르게 지정하지 않는 이상 어떤 레이어 상에 한 번에 ArrowArrayStream 하나만 활성화될 수 있습니다. (다시 말해 다음 ArrowArrayStream을 요청하기 전에 마지막으로 활성화되었던 ArrowArrayStream을 명확하게 해제해야만 합니다.)
ArrowArrayStream을 사용하는 동안 필터 상태 및 무시되는 열을 변경하거나, 스키마를 수정하거나, 또는 ResetReading()/GetNextFeature()를 사용하는 것을 강력하게 권장하지 않으며, 이렇게 하면 예상하지 못 한 결과로 이어질 수도 있습니다. 경험에 따르면 어떤 레이어 상에 있는 ArrowArrayStream이 활성화되어 있는 동안 해당 레이어에 레이어의 상태에 영향을 미치는 어떤 :cpp:class:`OGRLayer` 메소드도 호출해서는 안 됩니다.

다음과 같이 사용할 수 있을 것입니다:

.. code-block:: cpp

    struct ArrowArrayStream stream;
    if( !poLayer->GetArrowStream(&stream, nullptr))
    {
        fprintf(stderr, "GetArrowStream() failed\n");
        exit(1);
    }
    struct ArrowSchema schema;
    if( stream.get_schema(&stream, &schema) == 0 )
    {
        // 유용한 일을 하십시오.
        schema.release(schema);
    }
    while( true )
    {
        struct ArrowArray array;
        // 오류(get_next()가 0이 아닌 코드를 반환) 또는
        // 반복의 끝(array.release == nullptr)을 찾습니다.
        //
        if( stream.get_next(&stream, &array) != 0 ||
            array.release == nullptr )
        {
            break;
        }
        // 유용한 일을 하십시오.
        array.release(&array);
    }
    stream.release(&stream);

제공될 수도 있는 'papszOptions'는 NULL로 종료되는 키=값 문자열 목록으로, 드라이버 특화 목록일 수도 있습니다.

:cpp:class:`OGRLayer` 는 GetArrowStream()을 다음과 같이 기반 구현합니다:

- get_schema() 콜백은 반환되는 최상위 객체가 Struct 유형이며 그 하위 유형이 FID 열 및 모든 OGR 속성 필드와 도형 필드가 애로우 필드로 변환된 유형인 스키마를 반환합니다. INCLUDE_FID 옵션을 NO로 설정하면 FID 열을 누락시킬 수도 있습니다.

  get_schema()가 0을 반환하고 스키마가 더 이상 필요없는 경우 다음 과정을 통해 스키마를 반드시 해제해야만 합니다. 이때 애로우 C 데이터 인터페이스에 문서화되어 있는 대로 다른 코드가 해제했을 수도 있다는 것을 고려해야 합니다:

  .. code-block:: c

          if( out_schema->release )
              out_schema->release(out_schema)


- get_next() 콜백은 레이어의 다음 레코드 배치를 가져옵니다.

  'out_array'는 초기화되지 않은 상태일 수 있는 ArrowArray 구조를 가리키는 포인터입니다. (이 메소드는 모든 초기 콘텐츠를 무시할 것입니다.)

  기본 구현은 GetNextFeature()를 내부적으로 사용해서 피처 65,536개까지의 배치(batch)를 가져옵니다. (``MAX_FEATURES_IN_BATCH=num`` 옵션으로 이 개수를 환경설정할 수 있습니다.) 기본 구현이 할당한 버퍼의 시작 주소는 64바이트 경계에 정렬됩니다.

  기본 구현은 바이너리 필드에 도형을 WKB로 산출합니다. ``ARROW:extension:name`` 메타데이터 항목을 ``ogc.wkb`` 로 설정해서 스키마에서 그에 대응하는 항목을 표시합니다. 특수 구현은 (특히 지오애로우(GeoArrow) 사양에 따라 좌표 목록을 이용해서 인코딩된 도형을 반환할 수 있는 애로우 드라이버가) 기본적으로 다른 포맷들을 산출할 수도 있습니다. ``GEOMETRY_ENCODING=WKB`` 옵션을 전송하면 (기본 구현을 통해) WKB를 강제로 사용하게 할 수 있습니다.

  이 메소드는 SetIgnoredFields()를 이용해서 무시하도록 설정된 필드를 고려할 수도 있고 (기본 구현이 그렇게 합니다) SetSpatialFilter() 및 SetAttributeFilter()로 설정된 필터를 고려해야 합니다. 하지만 필터를 설정할 경우 특수 구현이 (느린) 기본 구현으로 되돌아갈 수도 있다는 사실을 기억하십시오.

  GetNextFeature() 및 get_next()를 함께 호출하는 일은 권장하지 않습니다. 어떤 습성을 보일지 알 수 없기 때문입니다. (그러나 충돌하지는 않을 것입니다.)

  get_next()가 0을 반환하고 배열이 더 이상 필요없는 경우 다음 과정을 통해 배열을 반드시 해제해야만 합니다. 이때 애로우 C 데이터 인터페이스에 문서화되어 있는 대로 다른 코드가 해제했을 수도 있다는 것을 고려해야 합니다:

  .. code-block:: c

          if( out_array->release )
              out_array->release(out_array)

특수 구현을 가진 드라이버는 새로운 OLCFastGetArrowStream 레이어 케이퍼빌리티를 노출시켜야 합니다.

기타
----

ArrowArray를 (생상자 또는 소비자로서) 직접 사용하는 것은 쉬운 일이 아니며, 애로우 C 데이터 인터페이스와 열 배열 사양을 잘 알고 있어야 배열의 어느 버퍼에서 데이터를 읽어올지, 어떤 데이터 유형에 ``void*`` 버퍼를 캐스트할지, NULL임 또는 NULL이 아님이라는 정보를 담고 있는 버퍼를 어떻게 사용할지, List 데이터 유형에 대해 오프셋 버퍼를 어떻게 사용할지 등등을 알 수 있습니다.

소비하는 쪽의 경우, 레코드 배치에 쉽고 안전한 접근을 제공하는 (Py)Arrow, Pandas, GeoPandas, Numpy와 함께 사용하면 새 API를 가장 잘 사용할 것입니다.
SWIG 파이썬 바인딩에 추가된 gdal_array._RecordBatchAsNumpy() 메소드를 연구하면 ArrowArray를 연결된 ArrowSchema와 함께 어떻게 사용할지에 대해 감을 잡을 수 있습니다. DuckDB도 ArrowArray 인터페이스를 사용하는 `또다른 예시 <https://github.com/duckdb/duckdb/blob/master/src/common/types/data_chunk.cpp>`_ 입니다.

대부분의 드라이버가 GetArrowStream() 또는 그 콜백들을 전용으로 구현할 것이라 기대하지 않습니다. 이를 구현하는 작업은 쉽지 않으며 입출력이 매우 빠르기 때문에 인메모리(in-memory) 데이터 섞기가 총 시간(입출력 및 섞기)에 상대적으로 시간이 걸리는 드라이버만 상당한 이익을 볼 것이라고 예상되기 때문입니다.

이 RFC의 범위에는 들어가지 않지만, 향후 새 피처를 작성할 수 있는 WriteRecordBatch() 열 지향 메소드를 추가할 수 있습니다.

드라이버에 미치는 영향
----------------------

- 애로우 및 파켓 드라이버:
  이 드라이버들은 get_schema() 및 get_next()가 리소스를 거의 사용하지 않고 (어떤 데이터도 복사하지 않고) 내부 C++ 구현을 C 데이터 인터페이스와 이어주는 arrow-cpp 라이브러리의 메소드들에 직접 매핑되도록 특수 구현합니다.

- FlatGeoBuf 및 지오패키지 드라이버:
  get_next()가 :cpp:class:`OGRFeature` 추상화를 통하지 않도록 특수 구현했습니다. 그 효율성 측정값을 알고 싶다면 :ref:`rfc-86-benchmarks` 단락을 참조하십시오.

바인딩
------

이 RFC에 따라, 파이썬 바인딩만 새 기능을 매핑하도록 확장합니다.

``ogr.Layer`` 클래스에 다음과 같은 새 메소드들을 추가합니다:

- GetArrowStreamAsPyArrow():
  C ArrowSchema를 이용해서 ``schema`` 속성을 대응하는 PyArrow Schema 객체로 변환하고, get_next() 콜백이 반환한 C ArrowArray를 대응하는 PyArrow Array 객체로 노출시키는 파이썬 반복자(iterator)를 구현한 :cpp:func:`OGRLayer::GetArrowStream` 메소드를 감싸는 래퍼(wrapper)입니다. 리소스를 거의 사용하지 않는 호출입니다.

- GetArrowStreamAsNumPy():
  get_next() 콜백이 반환한 C ArrowArray를 키가 ArrowArray의 값들을 표현하는 NumPy 배열의 필드 이름과 값인 파이썬 딕셔너리로 노출시키는 파이썬 반복자를 구현한 :cpp:func:`OGRLayer::GetArrowStream` 을 감싸는 래퍼입니다. :cpp:func:`OGRLayer::GetArrowStream` 의 기반 구현이 반환하는 모든 데이터 유형에 대해 유형 매핑이 되어 있지만, 애로우/파켓 드라이버에 구현된 것과 같은 특수 구현이 반환할 수 있는 "실험적인" 데이터 유형은 매핑이 되어 있지 않을 수도 있습니다. 숫자형 데이터 유형의 경우 NumPy 배열이 C 버퍼의 무복사(zero-copy) 개조물입니다. 다른 데이터 유형들의 경우 파이썬 객체 배열을 복사할 수도 있습니다.


.. _rfc-86-benchmarks:

벤치마크
--------

:ref:`rfc-86-annexes` 에 참조된 테스트 프로그램들은 각각 13개의 (정수 유형의 필드 2개, 문자열 유형의 필드 8개, 날짜&시간 유형의 필드 3개) 필드와 폴리곤 도형 피처 330만 개를 가진 데이터셋을 대상으로 실행되었습니다.

:ref:`rfc-86-bench-ogr-py`, :ref:`rfc-86-bench-fiona` 및 :ref:`rfc-86-bench-ogr-cpp` 는 GetNextFeature()를 이용해서 피처를 반복하는 유사한 기능을 가지고 있습니다.

:ref:`rfc-86-bench-pyogrio-raw` 는 그 뿐만 아니라 애로우 배열을 작성합니다.

:ref:`rfc-86-bench-pyogrio`, :ref:`rfc-86-bench-geopandas` 및 :ref:`rfc-86-bench-ogr-to-geopandas` 는 모두 GeoPandas GeoDataFrame을 작성하는 유사한 기능을 가지고 있습니다.

:ref:`rfc-86-bench-ogr-batch-cpp` 를 사용하면 제안하는 GetArrowStream() API의 원시(raw) 성능을 측정할 수 있습니다.

1. nz-building-outlines.fgb (FlatGeoBuf, 1.8 GB)

=========================================  =============
            벤치 프로그램                  걸린 시간(초)
=========================================  =============
bench_ogr.cpp                              6.3
bench_ogr.py                               71
bench_fiona.py                             68
bench_pyogrio_raw.py                       40
bench_pyogrio.py                           108
bench_geopandas.py                         232
bench_ogr_batch.cpp (드라이버 구현)        4.5
bench_ogr_batch.cpp (기반 구현)            14
bench_ogr_to_geopandas.py (드라이버 구현)  10
bench_ogr_to_geopandas.py (기반 구현)      20
=========================================  =============

"드라이버 구현"은 GetArrowStream()의 특수 구현을 사용한다는 의미입니다.
"기반 구현"은 기저에서 GetNextFeature()를 사용하는 GetArrowStream()의 일반 구현을 사용한다는 의미입니다.

2. nz-building-outlines.parquet (GeoParquet, 436 MB)

=========================================  =============
            벤치 프로그램                  걸린 시간(초)
=========================================  =============
bench_ogr.cpp                              6.4
bench_ogr.py                               72
bench_fiona.py                             70
bench_pyogrio_raw.py                       46
bench_pyogrio.py                           115
bench_geopandas.py                         228
bench_ogr_batch.cpp (드라이버 구현)        1.6
bench_ogr_batch.cpp (기반 구현)            13.8
bench_ogr_to_geopandas.py (드라이버 구현)  6.8
bench_ogr_to_geopandas.py (기반 구현)      20
=========================================  =============

주의: Fiona가 파켓 드라이버를 인식하는 드라이버로 받아들이도록 살짝 수정했습니다.

3. nz-building-outlines.gpkg (GeoPackage, 1.7 GB)

=========================================  =============
            벤치 프로그램                  걸린 시간(초)
=========================================  =============
bench_ogr.cpp                              7.6
bench_ogr.py                               71
bench_fiona.py                             63
bench_pyogrio_raw.py                       41
bench_pyogrio.py                           103
bench_geopandas.py                         227
bench_ogr_batch.cpp (드라이버 구현)        1.0
bench_ogr_batch.cpp (기반 구현)            15.5
bench_ogr_to_geopandas.py (드라이버 구현)  10
bench_ogr_to_geopandas.py (기반 구현)      21
=========================================  =============

:file:`bench_ogr_batch.cpp` 가 FlatGeoBuf 상에서보다 GeoPackage 상에서 더 빠릅니다.
FlatGeoBuf 도형이 다른 인코딩을 사용하는 반면 GeoPackage 도형은 이미 (추가 헤더를 가진) WKB로 인코딩되어 있기 때문입니다.

주의: :file:`bench_ogr_to_geopandas.py` 에서는 GeoPackage가 GeoParquet보다 느린 반면 어째서 :file:`bench_ogr_batch.cpp` 에서는 GeoPackage가 GeoParquet보다 더 빠른지 완벽하게 이해할 수 없습니다. 파켓 배치(batch)가 더 큰 배열의 슬라이스(slice)이고 pa.RecordBatch.from_arrays()가 파켓 배치를 더 빨리 병합할 수 있기 때문일 수도 있습니다.

이 벤치마크는 다음과 같은 사실을 보여줍니다:

- 새 API를 사용하면 GetArrowStream()의 특수 구현 없이도 그리고 네이티브한 행 구조를 가진 포맷(FlatGeoBuf, GeoPackage)에 대해서도 OGR 레이어를 pyogrio와 비교해서 속도가 4배~10배 향상된 순서를 가진 GeoPandas GeoDataFrame으로 불러오는 상당한 성능 향상을 얻을 수 있습니다.

- 파켓 드라이버는 파일 구조가 열 지향적이고 네이티브한 레이어 접근 방식이 ArrowArray와 호환되기 때문에 새 API의 혜택을 가장 많이 받습니다.

- GetArrowStream()의 특수 구현이 없고 레이아웃이 행 구조인 드라이버의 경우, GetNextFeature() 접근법이 GetArrowStream() 접근법보다 (약간) 더 빠릅니다.

하위 호환성
-----------

API만 추가하기 때문에, 완벽하게 하위 호환됩니다.

가상 메소드 추가 때문에 C++ ABI를 변경합니다.

새 의존성
---------

- libgdal의 경우: 없음

  아파치 애로우 C 데이터 인터페이스는 C 구조 2개를 정의할 뿐입니다. GDAL 자체를 아파치 애로우 C++ 라이브러리를 대상으로 링크할 필요가 없습니다. (애로우 그리고/또는 파켓(Parquet) 드라이버가 활성화된 경우 링크할 수도 있지만, 이 RFC에서 논의하는 주제와는 상관없습니다.)

- 파이썬 바인딩의 경우:
  컴파일 시에는 없습니다. 런타임 시, GetArrowStreamAsPyArrow()가 `PyArrow <https://arrow.apache.org/docs/python/index.html>`_ 를 가져옵니다. gdal_array 모듈이 GetArrowStreamAsNumPy() 메소드를 내부적으로 구현하기 때문에, 컴파일 및 런타임 시 NumPy를 사용할 수 있는 경우에만 이 메소드를 사용할 수 있습니다.

문서화
------

새로운 메소드들을 문서화하고, GDAL 문서에 새 문서 페이지를 추가할 것입니다.

테스트
------

새 메소드들을 테스트합니다.

관련 풀 요청:
-------------

https://github.com/OSGeo/gdal/compare/master...rouault:arrow_batch_new?expand=1

.. _rfc-86-annexes:

부록
----

.. _rfc-86-bench-ogr-cpp:

bench_ogr.cpp
+++++++++++++

일반적인 GetNextFeature() 및 C로부터 나온 관련 API를 사용합니다:

.. code-block:: cpp

    #include "gdal_priv.h"
    #include "ogr_api.h"
    #include "ogrsf_frmts.h"

    int main(int argc, char* argv[])
    {
        GDALAllRegister();
        GDALDataset* poDS = GDALDataset::Open(argv[1]);
        OGRLayer* poLayer = poDS->GetLayer(0);
        OGRLayerH hLayer = OGRLayer::ToHandle(poLayer);
        OGRFeatureDefnH hFDefn = OGR_L_GetLayerDefn(hLayer);
        int nFields = OGR_FD_GetFieldCount(hFDefn);
        std::vector<OGRFieldType> aeTypes;
        for( int i = 0; i < nFields; i++ )
            aeTypes.push_back(OGR_Fld_GetType(OGR_FD_GetFieldDefn(hFDefn, i)));
        int nYear, nMonth, nDay, nHour, nMin, nSecond, nTZ;
        while( true )
        {
            OGRFeatureH hFeat = OGR_L_GetNextFeature(hLayer);
            if( hFeat == nullptr )
                break;
            OGR_F_GetFID(hFeat);
            for( int i = 0; i < nFields; i++ )
            {
                if( aeTypes[i] == OFTInteger )
                    OGR_F_GetFieldAsInteger(hFeat, i);
                else if( aeTypes[i] == OFTInteger64 )
                    OGR_F_GetFieldAsInteger64(hFeat, i);
                else if( aeTypes[i] == OFTReal )
                    OGR_F_GetFieldAsDouble(hFeat, i);
                else if( aeTypes[i] == OFTString )
                    OGR_F_GetFieldAsString(hFeat, i);
                else if( aeTypes[i] == OFTDateTime )
                    OGR_F_GetFieldAsDateTime(hFeat, i, &nYear, &nMonth, &nDay, &nHour, &nMin, &nSecond, &nTZ);
            }
            OGRGeometryH hGeom = OGR_F_GetGeometryRef(hFeat);
            if( hGeom )
            {
                int size = OGR_G_WkbSize(hGeom);
                GByte* pabyWKB = static_cast<GByte*>(malloc(size));
                OGR_G_ExportToIsoWkb( hGeom, wkbNDR, pabyWKB);
                CPLFree(pabyWKB);
            }
            OGR_F_Destroy(hFeat);
        }
        delete poDS;
        return 0;
    }

.. _rfc-86-bench-ogr-py:

bench_ogr.py
++++++++++++

일반적인 GetNextFeature() 및 파이썬(:file:`bench_ogr.cpp` 의 포팅)으로부터 나온 관련 API를 사용합니다:

.. code-block:: python

    from osgeo import ogr
    import sys

    ds = ogr.Open(sys.argv[1])
    lyr = ds.GetLayer(0)
    lyr_defn = lyr.GetLayerDefn()
    fld_count = lyr_defn.GetFieldCount()
    types = [lyr_defn.GetFieldDefn(i).GetType() for i in range(fld_count)]
    for f in lyr:
        f.GetFID()
        for i in range(fld_count):
            fld_type = types[i]
            if fld_type == ogr.OFTInteger:
                f.GetFieldAsInteger(i)
            elif fld_type == ogr.OFTReal:
                f.GetFieldAsDouble(i)
            elif fld_type == ogr.OFTString:
                f.GetFieldAsString(i)
            else:
                f.GetField(i)
        geom = f.GetGeometryRef()
        if geom:
            geom.ExportToWkb()

.. _rfc-86-bench-fiona:

bench_fiona.py
++++++++++++++

파이썬 딕셔너리가 담고 있는 GeoJSON 피처로 노출시키기 위해 기저에서 GetNextFeature() OGR C 함수를 사용하는 `Fiona 파이썬 라이브러리 <https://pypi.org/project/Fiona/>`_ 를 사용합니다:

.. code-block:: python

    import sys
    import fiona

    with fiona.open(sys.argv[1], 'r') as features:
        for f in features:
            pass

.. note:: 피처를 누적하기 위해 앞의 루프를 ``list(features)`` 로 변경하는 것은 대용량 데이터셋만의 경우가 아니라 모든 경우에 메모리 사용에 상당히 나쁜 영향을 미칩니다.

.. _rfc-86-bench-pyogrio-raw:

bench_pyogrio_raw.py
++++++++++++++++++++

레이어를 애로우 배열 집합으로 노출시키기 위해 기저에서 GetNextFeature() OGR C 함수를 사용하는 `pyogrio 파이썬 라이브러리 <https://pypi.org/project/pyogrio/>`_ 를 사용합니다:

.. code-block:: python

    import sys
    from pyogrio.raw import read

    read(sys.argv[1])


.. _rfc-86-bench-pyogrio:

bench_pyogrio.py
++++++++++++++++

레이어를 (WKB를 GEOS 객체로 파싱하는 작업을 수반하는) `GeoPandas <https://geopandas.org/en/stable/>`_ GeoDataFrame으로 노출시키기 위해 기저에서 GetNextFeature() OGR C 함수를 사용하는 `pyogrio 파이썬 라이브러리 <https://pypi.org/project/pyogrio/>`_ 를 사용합니다:

.. code-block:: python

    import sys
    from pyogrio import read_dataframe

    read_dataframe(sys.argv[1])

.. _rfc-86-bench-geopandas:

bench_gepandas.py
+++++++++++++++++

레이어를 GeoPandas GeoDataFrame으로 노출시키기 위해 기저에서 Fiona를 사용하는 `GeoPandas 파이썬 라이브러리 <https://pypi.org/project/geopandas/>`_ 를 사용합니다:

.. code-block:: python

    import sys
    import geopandas

    gdf = geopandas.read_file(sys.argv[1])

.. _rfc-86-bench-ogr-batch-cpp:

bench_ogr_batch.cpp
+++++++++++++++++++

C++로부터 나온, 제안하는 GetNextRecordBatch() API를 사용합니다:

.. code-block:: cpp

    #include "gdal_priv.h"
    #include "ogr_api.h"
    #include "ogrsf_frmts.h"
    #include "ogr_recordbatch.h"

    int main(int argc, char* argv[])
    {
        GDALAllRegister();
        GDALDataset* poDS = GDALDataset::Open(argv[1]);
        OGRLayer* poLayer = poDS->GetLayer(0);
        OGRLayerH hLayer = OGRLayer::ToHandle(poLayer);
        struct ArrowArrayStream stream;
        if( !OGR_L_GetArrowStream(hLayer, &stream, nullptr))
        {
            CPLError(CE_Failure, CPLE_AppDefined, "OGR_L_GetArrowStream() failed\n");
            exit(1);
        }
        while( true )
        {
            struct ArrowArray array;
            if( stream.get_next(&stream, &array) != 0 ||
                array.release == nullptr )
            {
                break;
            }
            array.release(&array);
        }
        stream.release(&stream);
        delete poDS;
        return 0;
    }

.. _rfc-86-bench-ogr-to-geopandas:

bench_ogr_to_geopandas.py
+++++++++++++++++++++++++

반환된 배열들을 연결(concatenation)로부터 GeoPandas GeoDataFrame을 작성하기 위해 파이썬으로부터 나온, 제안하는 GetNextRecordBatchAsPyArrow API를 사용합니다:

.. code-block:: python

    import sys
    from osgeo import ogr
    import pyarrow as pa

    def layer_as_geopandas(lyr):
        stream = lyr.GetArrowStreamAsPyArrow()
        schema = stream.schema

        geom_field_name = None
        for field in schema:
            field_md = field.metadata
            if (field_md and field_md.get(b'ARROW:extension:name', None) == b'WKB') or field.name == lyr.GetGeometryColumn():
                geom_field_name = field.name
                break

        fields = [field for field in schema]
        schema_without_geom = pa.schema(list(filter(lambda f: f.name != geom_field_name, fields)))
        batches_without_geom = []
        non_geom_field_names = [f.name for f in filter(lambda f: f.name != geom_field_name, fields)]
        if geom_field_name:
            schema_geom = pa.schema(list(filter(lambda f: f.name == geom_field_name, fields)))
            batches_with_geom = []
        for record_batch in stream:
            arrays_without_geom = [record_batch.field(field_name) for field_name in non_geom_field_names]
            batch_without_geom = pa.RecordBatch.from_arrays(arrays_without_geom, schema=schema_without_geom)
            batches_without_geom.append(batch_without_geom)
            if geom_field_name:
                batch_with_geom = pa.RecordBatch.from_arrays([record_batch.field(geom_field_name)], schema=schema_geom)
                batches_with_geom.append(batch_with_geom)

        table = pa.Table.from_batches(batches_without_geom)
        df = table.to_pandas()
        if geom_field_name:
            from geopandas.array import from_wkb
            import geopandas as gp
            geometry = from_wkb(pa.Table.from_batches(batches_with_geom)[0])
            gdf = gp.GeoDataFrame(df, geometry=geometry)
            return gdf
        else:
            return df


    if __name__ == '__main__':
        ds = ogr.Open(sys.argv[1])
        lyr = ds.GetLayer(0)
        print(layer_as_geopandas(lyr))

투표 이력
---------

-  마테우시 워스코트 +1
-  유카 라흐코넨 +1
-  하워드 버틀러 +1
-  이벤 루올 +1

