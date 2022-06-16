.. _vector.parquet:

(지오)파켓
============

.. versionadded:: 3.5

.. shortname:: Parquet

.. build_dependencies:: 아파치 애로우 C++ 라이브러리의 파켓 구성 요소

https://databricks.com/glossary/what-is-parquet 에서 발췌:

   "아파치 파켓(Apache Parquet)은 효율적인 데이터 저장 및 가져오기를 위해 설계된 열 지향(column-oriented) 오픈 소스 데이터 파일 포맷입니다. 복잡한 데이터를 덩어리(bulk)로 처리하기 위해 향상된 성능과 함께 효율적인 데이터 압축 및 인코딩 스키마를 제공합니다.
   아파치 파켓은 배치(batch) 및 대화형 작업 부하(workload) 둘 다를 위한 공통 정보 교환 포맷으로 설계되었습니다."

이 드라이버는 지오파켓(GeoParquet) 사양을 사용하는 도형 열도 지원합니다.

.. note::

   지오파켓 사양이 아직 확정되지 않았기 때문에 이 드라이버를 실험적인 것으로 간주해야 합니다.


드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::


생성 문제점
---------------

이 드라이버는 데이터셋 하나에 단일 레이어 하나만 생성할 수 있습니다.

레이어 생성 옵션
----------------------

-  **COMPRESSION=string**:
   압축 메소드를 지정합니다. ``NONE``, ``SNAPPY``, ``GZIP``, ``BROTLI``, ``ZSTD``, ``LZ4``, ``BZ2`` 또는 ``LZ4_HADOOP`` 가운데 하나로 지정할 수 있습니다. 파켓 라이브러리가 어떻게 컴파일되었는지에 따라 지정할 수 있는 값이 달라집니다.
   SNAPPY를 사용할 수 있는 경우 기본값은 SNAPPY이고, 사용할 수 없다면 기본값은 NONE입니다.

-  **GEOMETRY_ENCODING=WKB/WKT/GEOARROW**:
   도형 인코딩을 지정합니다. 기본값은 WKB입니다.
   지오파켓 사양은 다른 (WKT 및 GEOARROW) 인코딩을 허용하지 않지만, 애로우 드라이버와의 대칭성을 위해 확장 사양으로 처리합니다.

-  **ROW_GROUP_SIZE=integer**:
   그룹 당 행의 최대 개수를 지정합니다. 기본값은 65536입니다.

-  **GEOMETRY_NAME=string**:
   도형 열의 이름을 지정합니다. 기본값은 ``geometry`` 입니다.

-  **FID=string**:
   생성할 FID(Feature ID) 열의 이름을 지정합니다. 아무것도 지정하지 않으면 FID 열을 생성하지 않습니다.
   소스 레이어가 명명된 FID 열을 가지고 있는데 파켓 드라이버를 대상 드라이버로 ogr2ogr 유틸리티를 사용하는 경우, (비어 있는 이름을 설정하기 위해 ``-lco FID=`` ogr2ogr 옵션을 사용하지 않는 이상) 파켓 드라이버의 FID 레이어 생성 옵션을 이 FID 열의 이름으로 자동 설정할 것이라는 사실을 기억하십시오.

-  **POLYGON_ORIENTATION=COUNTERCLOCKWISE/UNMODIFIED**:
   폴리곤의 외곽 고리가 반시계 방향이어야 할지 (그리고 내곽 고리는 시계 방향이어야 할지) 또는 원래 방향으로 유지해야 할지를 지정합니다. 기본값은 COUNTERCLOCKWISE입니다.

-  **EDGES=PLANAR/SPHERICAL**:
   도형의 경계를 해석하는 방법을 지정합니다. 두 포인트를 잇는 라인이 데카르트 직선(PLANAR)인지 또는 구 표면의 최단 라인(SPHERICAL)인 측지선인지를 결정합니다. 기본값은 PLANAR입니다.

-  **CREATOR=string**:
   레이어를 생성하는 응용 프로그램의 이름입니다.

SQL 지원
--------

SQL 선언문은 OGR SQL 엔진을 통해 실행됩니다. 다음과 같이 통계를 사용해서 SQL 요청 평가 시간을 줄일 수 있습니다:

   ``SELECT MIN(colname), MAX(colname), COUNT(colname) FROM layername``

데이터셋/파티션 읽기 지원
-------------------------

GDAL 3.6.0버전부터, 이 드라이버는 파켓 파일 여러 개를 담고 있는 디렉터리를 읽어와서 단일 레이어로 노출시킬 수 있습니다. 드라이버가 ``arrowdataset`` C++ 라이브러리를 대상으로 빌드된 경우에만 이 지원이 활성화됩니다.

현재 필터링에 대한 최적화가 되어 있지 않다는 사실을 기억하십시오.

링크
-----

-  `아파치 파켓 홈페이지 <https://parquet.apache.org/>`_

-  `파켓 파일 포맷 <https://github.com/apache/parquet-format>`_

-  `지오파켓 사양 <https://github.com/opengeospatial/geoparquet>`_

-  관련 드라이버: :ref:`애로우 <vector.arrow>` 드라이버

