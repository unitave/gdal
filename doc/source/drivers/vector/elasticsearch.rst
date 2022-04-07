.. _vector.elasticsearch:

Elasticsearch: Elasticsearch 용 지리 인코딩 객체
===============================================================

.. shortname:: Elasticsearch

.. build_dependencies:: libcurl

GDAL 2.1부터, Elasticsearch 드라이버는 Elasticsearch 1.X 그리고 부분적이지만 2.X 버전의 읽기 및 쓰기를 지원합니다. (5.0버전은 지원하지 않습니다.) GDAL 2.2버전에서 Elasticsearch 2.X 및 5.X 버전 지원이 추가되었습니다.

`Elasticsearch <http://elasticsearch.org/>`_ 사는 다양한 데이터소스를 찾아주는 기업 수준 검색 엔진입니다. 사전 정의된 REST API를 이용해서 빠르고 효율적인 방식으로 이런 데이터의 전체 텍스트 색인 작업(full-text indexing) 및 지리공간 쿼리 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터셋 열기 이름 문법
---------------------------

GDAL 2.1버전부터, 이 드라이버는 Elasticsearch 호스트로부터 기존 색인을 읽어올 수 있습니다. 데이터셋을 열 수 있는 주요 문법이 2개 있습니다:

-  *ES:http://hostname:port* (이때 포트는 일반적으로 9200)
-  *ES:* (HOST와 PORT를 지정하는 열기 옵션을 사용)

다음과 같은 열기 옵션을 사용할 수 있습니다:

-  **HOST=hostname**: 서버 호스트명입니다. 기본값은 localhost입니다.

-  **PORT=port**: 서버 포트입니다. 기본값은 9200입니다.

-  **USERPWD=user:password**: (GDAL 2.4 이상 버전)
   사용자명:비밀번호 형식의 기본 인증 방법입니다.

-  **LAYER=name**: (GDAL 2.4 이상 버전)
   레이어 목록의 제약 조건으로 쓰이는 색인명 또는 index_mapping입니다.

-  **BATCH_SIZE=number**: 배치(batch) 당 가져올 객체의 개수를 설정합니다. 기본값은 100입니다.

-  **FEATURE_COUNT_TO_ESTABLISH_FEATURE_DEFN=number**:
   객체 정의를 확립하기 위해 가져올 객체의 개수를 설정합니다. -1값은 무제한이라는 뜻입니다. 기본값은 100입니다.

-  **SINGLE_QUERY_TIMEOUT=number**: (GDAL 3.2.1 이상 버전)
   GetFeatureCount() 또는 GetExtent() 같은 요청에 대한 (부동소수점형 숫자의) 초 단위 제한 시간을 설정합니다. 기본값은 무제한입니다.

-  **SINGLE_QUERY_TERMINATE_AFTER=number**: (GDAL 3.2.1 이상 버전)
   GetFeatureCount() 또는 GetExtent() 같은 요청에 대해 수집할 문서의 최대 개수입니다. 기본값은 무제한입니다.

-  **FEATURE_ITERATION_TIMEOUT=number**: (GDAL 3.2.1 이상 버전)
   객체 반복 작업에 대한, ResetReading() 시간으로부터 시작하는 (부동소수점형 숫자의) 초 단위 제한 시간을 설정합니다. 기본값은 무제한입니다.

-  **FEATURE_ITERATION_TERMINATE_AFTER=number**: (GDAL 3.2.1 이상 버전)
   객체 반복 작업에 대해 수집할 문서의 최대 개수입니다. 기본값은 무제한입니다.

-  **JSON_FIELD=YES/NO**: 전체 문서를 JSON으로 가지고 있는 "_json"이라는 필드를 포함할지 여부를 선택합니다. 기본값은 NO입니다.

-  **FLATTEN_NESTED_ATTRIBUTE=YES/NO**: 내포된 객체들을 재귀적으로 탐색해서 평탄화된(flatten) OGR 속성을 생산할지 여부를 선택합니다. 기본값은 YES입니다.

-  **FID=string**: FID로 사용할 정수값을 가진 필드의 이름을 설정합니다. 기본값은 'ogc_fid'입니다.

-  **FORWARD_HTTP_HEADERS_FROM_ENV=string**: (GDAL 3.1 이상 버전)
   이 옵션을 사용해서, 보통 인증 목적으로 Elasticsearch로 전송해야만 하는 HTTP 헤더를 지정할 수 있습니다. 문자열의 값은 http_header_name=env_variable_name을 쉼표로 구분한 목록으로, 이때 http_header_name은 HTTP 헤더의 이름이고 env_variable_name은 HTTP 헤더의 값을 가져와야 할 환경 변수/환경설정 옵션의 이름입니다.
   이 옵션의 목적은 들어오는 요청의 HTTP 헤더를 환경 변수로 저장하는 웹 서버가 OGR Elasticsearch 드라이버를 호출하는 경우를 대비하는 것입니다. 이 열기 옵션 대신 ES_FORWARD_HTTP_HEADERS_FROM_ENV 환경설정 옵션도 사용할 수 있습니다.

-  **AGGREGATION=string**: (GDAL 3.5 이상 버전)
   :ref:`집계 <vector.elasticsearch.aggregations>` 의 JSON 직렬화 정의를 설정합니다.

Elasticsearch 대 OGR 개념
-----------------------------

Elasticsearch 색인 내부에서 매핑되는 각 유형을 OGR 레이어로 간주합니다. Elasticsearch 문서는 OGR 객체로 간주합니다.

필드 정의
-----------------

입력 OGR 데이터소스로부터 필드들을 동적으로 매핑합니다. 하지만, 이 드라이버는 `필드 매핑 파일 <http://code.google.com/p/ogr2elasticsearch/wiki/ModifyingtheIndex>`_ 에 정의된 대로 Elasticsearch 내부 고급 옵션을 활용할 것입니다.

이 매핑 파일은 사용자가 `Elasticsearch 필드 특화 유형 <http://www.elasticsearch.org/guide/reference/mapping/core-types.html>`_ 에 따라 매핑을 수정할 수 있게 해줍니다. 선택할 수 있는 옵션들이 많이 있지만, 대부분의 기능은 Elasticsearch 내부 텍스트 필드로 할 수 있는 서로 다른 모든 작업들을 기반으로 합니다.

::

   ogr2ogr -progress --config ES_WRITEMAP /path/to/file/map.txt -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

Elasticsearch 작성기는 다음 환경설정 옵션들을 지원합니다. GDAL 2.1버전부터, 레이어 생성 옵션을 사용할 수 있으며 이를 사용하는 편이 좋습니다:

-  **ES_WRITEMAP=/path/to/mapfile.txt**:
   색인에 삽입하기 전에 사용자가 수정할 수 있는 매핑 파일을 생성합니다. 어떤 객체도 작성하지 않을 것입니다. 이 옵션은 단일 레이어 하나만 생성하는 경우에만 제대로 작동할 것이라는 사실을 기억하십시오. GDAL 2.1버전부터, **WRITE_MAPPING** 레이어 생성 옵션을 사용하는 편이 좋습니다.

-  **ES_META=/path/to/mapfile.txt**:
   드라이버에 사용자 정의 필드 매핑을 사용하라고 지시합니다. GDAL 2.1버전부터, **MAPPING** 레이어 생성 옵션을 사용하는 편이 좋습니다.

-  **ES_BULK=5000000**:
   한 번씩 삽입할 문서들을 저장할 버퍼의 바이트 단위 최대 용량을 설정합니다. 레코드 개수를 적게 설정하면 Elasticsearch 내부 메모리 소비를 줄일 수 있지만 삽입하는 데 더 오래 걸립니다. GDAL 2.1버전부터, **BULK_SIZE** 레이어 생성 옵션을 사용하는 편이 좋습니다.

-  **ES_OVERWRITE=1**:
   기존 색인을 삭제하고 현재 색인을 덮어씁니다. GDAL 2.1버전부터, **OVERWRITE** 레이어 생성 옵션을 사용하는 편이 좋습니다.

도형 유형
--------------

GDAL 2.0 이전 버전에서는 이 드라이버가 처리할 수 있는 도형에 제한이 있었습니다. 폴리곤을 입력받더라도 `지오포인트(geopoint) <http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-geo-point-type.html>`_ 로 저장하고 폴리곤 "중심"을 포인트의 값으로 사용했습니다. GDAL 2.1버전부터, `geo_shape <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-geo-shape-type.html>`_ 을 사용해서 모든 도형 유형을 저장합니다. (Elasticsearch가 처리하지 못 하는 만곡 도형은 예외입니다. 만곡 도형은 가장 근사치에 가까운 선형 도형으로 변환할 것입니다.)

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다.

GDAL 2.2버전부터, :cpp:func:`SetAttributeFilter()` 함수에 설정된 SQL 속성 필터는 `Elasticsearch 필터 문법 <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-filters.html>`_ 으로 변환됩니다. 이 문법을 잠재적으로 정의된 공간 필터와 결합시킬 것입니다.

:cpp:func:`SetAttributeFilter()` 함수에 전송되는 Elasticsearch 필터 문자열을 JSon 직렬화 객체로 설정해서 Elasticsearch 필터를 직접 사용할 수도 있습니다. 다음은 그 예시입니다:

.. code-block:: json

   { "post_filter": { "term": { "properties.EAS_ID": 169 } } }

주의: Elasticsearch JSon 필터를 직접 정의하는 경우, :cpp:func:`OGRLayer::SetSpatialFilter` 함수를 통해 지정한 공간 필터를 무시할 것이기 때문에, 필요한 경우 JSon 필터에 포함시켜야만 합니다.

페이지 작업(paging)
-------------------

서버로부터 객체들을 100개 덩어리로 가져옵니다. BATCH_SIZE 열기 옵션으로 이 개수를 변경할 수 있습니다.

스키마
------

Elasticsearch 색인/유형을 읽어올 때, OGR가 속성 및 도형 필드의 스키마를 확립해야만 합니다. ORG가 고정 스키마 개념을 가지고 있기 때문입니다.

일반적인 경우, OGR는 색인/유형의 매핑 정의 및 처음 100개의 (FEATURE_COUNT_TO_ESTABLISH_FEATURE_DEFN 열기 옵션으로 이 개수를 변경할 수 있습니다) 문서를 읽어와서 가져온 필드와 값에 가장 적합한 스키마를 작성할 것입니다.

JSON_FIELD 열기 옵션을 YES로 설정하면 OGR 스키마에 \_json 특수 필드도 추가할 수 있습니다. Elasticsearch 문서를 OGR 객체로 읽어올 때, \_json 필드에 문서 전체의 JSon 버전을 저장할 것입니다. 복잡 문서 또는 OGR 데이터 유형으로 잘 변환되지 않는 데이터 유형의 경우 유용할 수도 있습니다. 문서 생성/업데이트 작업 시, \_json 필드가 존재하고 설정되어 있는 경우 그 내용을 직접 사용할 것입니다. (다른 필드들은 무시할 것입니다.)

객체 ID (FID)
-------------

Elasticsearch는 문서의 유일 ID를 담고 있는 \_id 특수 필드를 가지고 있습니다. 이 필드는 OGR 필드로 반환되지만, 반드시 정수형이어야만 하는 OGR FeatureID 특수 필드로 사용할 수는 없습니다. OGR는 기본적으로 OGR FeatureID를 설정하기 위해, 존재할 수도 있는 'ogc_fid' 필드를 읽어오려 시도할 것입니다. FID 열기 옵션으로 검색할 필드의 이름을 설정할 수 있습니다. 이 필드를 발견하지 못 하는 경우, OGR가 FID를 1에서 시작하는 일련 번호로 반환하지만 안정적일 것이라고 보장할 수는 없습니다.

ExecuteSQL() 인터페이스
-----------------------

GDAL 2.2버전부터, 단일 레이어에 대한 WHERE 및 ORDER BY 문을 가진 SQL 요청을 Elasticsearch 쿼리로 변환할 것입니다.

이렇게 하지 않고 "ES"를 ExecuteSQL()의 방언으로 지정하면, 직렬화된 `Elasticsearch 필터 <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-filters.html>`_ 를 가진 JSon 문자열을 전송할 수 있습니다. 필터 자체가 검색을 제약하지 않는 이상 모든 색인과 유형에 대해 검색할 것입니다. 반환 레이어는 FEATURE_COUNT_TO_ESTABLISH_FEATURE_DEFN 첫 문서들이 반환하는 유형들을 통합(union)한 것일 것입니다. 이 레이어는 객체들의 출처를 나타내는 \_index 및 \_type 특수 필드도 담고 있을 것입니다.

다음 필터를 사용해서 "poly" 색인과 해당 색인의 "FeatureCollection" 유형 매핑에 대해서만 검색하도록 제약할 수 있습니다(Elasticsearch 1.X 및 2.X 버전):

.. code-block:: json

   { "filter": {
       "indices" : {
           "no_match_filter": "none",
           "index": "poly",
           "filter": {
              "and" : [
                { "type": { "value": "FeatureCollection" } },
                { "term" : { "properties.EAS_ID" : 158.0 } }
              ]
           }
         }
       }
   }

Elasticsearch 5.X 버전의 경우 (2.X 버전에서도 작동함):

.. code-block:: json

   { "post_filter": {
       "indices" : {
           "no_match_query": "none",
           "index": "poly",
           "query": {
             "bool": {
               "must" : [
                 { "type": { "value": "FeatureCollection" } },
                 { "term" : { "properties.EAS_ID" : 158.0 } }
               ]
             }
           }
         }
       }
   }

ExecuteSQL() 인터페이스를 통한 집계(aggregation)는 지원하지 않지만, 다음 메커니즘을 통해 지원할 수 있습니다.

.. _vector.elasticsearch.aggregations:

집계
------------

.. versionadded:: 3.5.0

이 드라이버는 색인에 집계(aggregation) 요청을 전송할 수 있습니다. Elasticsearch 집계는 조금 복잡해질 가능성이 있기 때문에, 현재 예를 들어 히트 맵을 생성하기 위해 사용할 수 있는 통계 지표(최소값, 최대값, 평균 등등)를 가진 추가 필드들을 가지고 있는 지오해시(geohash) 그리드 기반 공간 집계로만 제한하고 있습니다. ``AGGREGATION`` 열기 옵션으로 집계를 지정할 수 있는데, 이 옵션의 값은 다음과 같은 파라미터를 가지고 있는 JSon 직렬화 객체입니다:

-  ``index``: (필수)
   쿼리할 색인 이름입니다.

-  ``geometry_field``: (선택적)
   `지오해시 그리드 집계 <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geohashgrid-aggregation.html>`_ 를 수행할 도형 필드를 가리키는 경로입니다. GeoJSON으로 인코딩된 포인트를 가진 문서의 경우, 예를 들어 `geometry.coordinates` 같은 경로가 될 것입니다. 이 속성을 지정하지 않는 경우, 드라이버가 매핑을 분석해서 (단일 정의가 존재한다는 가정 하에) 발견한 도형 필드 정의를 사용할 것입니다. geo_shape 도형에 대한 집계는 Elasticsearch 7버전부터 지원하기 때문에 유료 사용 허가를 요구할 수도 있다는 사실을 기억하십시오.

-  ``geohash_grid``: (선택적)
   geohash_grid의 몇몇 특성을 서술하는 JSon 객체입니다. geohash_grid는 다음 하위 파라미터들을 가질 수 있습니다:

   *  ``size``: (선택적)
      쿼리 당 반환할 지오해시 버켓의 최대 개수입니다. 기본값은 10,000입니다. ``precision`` 이 지정돼 있는데 결과물 개수가 ``size`` 를 초과하는 경우, 서버가 일치하는 문서들을 내림차순으로 정렬해서 결과물을 다듬을 것입니다.

   *  ``precision``: (선택적)
      결과물의 셀/버켓을 정의하기 위해 사용하는 [1,12] 범위의 지오해시 문자열 길이입니다. 크기가 1인 지오해시는 최대 32개의 버켓을, 크기가 2라면 32x32개의 버켓을, ... 생성할 수 있습니다. 지정하지 않는 경우, 반환되는 버켓의 이론적 개수가 ``size`` 를 초과하지 않도록 드라이버가 ``size`` 파라미터 및 공간 필터를 연산에 넣어 값을 자동으로 계산할 것입니다.

-  ``fields``: (선택적)
   어떤 추가적인 통계 필드를 추가해야 할지 서술하는 JSon 객체입니다. 다음 하위 파라미터들을 가질 수 있습니다:

   *  ``min``: (선택적)
      집계 작업 도중 최소값을 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.

   *  ``max``: (선택적)
      집계 작업 도중 최대값을 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.

   *  ``avg``: (선택적)
      집계 작업 도중 평균을 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.

   *  ``sum``: (선택적)
      집계 작업 도중 합계를 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.

   *  ``count``: (선택적)
      집계 작업 도중 value_count를 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.
        to compute the value_count during aggegation.

   *  ``stats``: (선택적)
      집계 작업 도중 앞의 모든 지표를 계산할 색인 속성을 가리키는 경로를 가지고 있는 배열입니다.

   GeoJSON 매핑을 사용하는 경우, 색인 속성을 가리키는 경로는 보통 ``property.some_name`` 입니다.

AGGREGATION 열기 옵션을 지정하면, ``aggregation`` 이라는 읽기전용 단일 레이어를 반환할 것입니다. 표준 OGR :cpp:func:`OGRLayer::SetSpatialFilter` API를 사용하면 이 레이어에 공간 필터를 설정할 수 있습니다. 이런 공간 필터는 집계 이전에 적용됩니다.

다음은 AGGREGATION 열기 옵션의 예시입니다:

.. code-block:: json

    {
        "index": "my_points",
        "geometry_field": "geometry.coordinates",
        "geohash_grid": {
            "size": 1000,
            "precision": 3
        },
        "fields": {
            "min": [ "field_a", "field_b"],
            "stats": [ "field_c" ]
        }
    }


이 옵션은 Point 도형 필드와 다음 필드들을 가진 레이어를 반환할 것입니다:

- ``key`` -- 문자열 유형: 대응하는 버켓의 지오해시 값
- ``doc_count`` -- Integer64 유형: 버켓에서 일치하는 문서들의 개수
- ``field_a_min`` -- 실수형
- ``field_b_min`` -- 실수형
- ``field_c_min`` -- 실수형
- ``field_c_max`` -- 실수형
- ``field_c_avg`` -- 실수형
- ``field_c_sum`` -- 실수형
- ``field_c_count`` -- Integer64 유형

다중 대상 레이어
-------------------

.. versionadded:: 3.5.0

GetLayerByName() 메소드는 레이어 이름을 입력받습니다. 이 레이어 이름은 쉼표로 구분된, '*' 와일드카드 문자가 포함되었을 수도 있는 색인 목록일 수 있습니다. https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-index.html 을 참조하십시오. 현재 구현된 상태에서는 일치하는 모든 레이어가 아니라 일치하는 레이어 가운데 하나로부터 필드 정의를 확립할 것이기 때문에 일치하는 여러 레이어들이 동일한 스키마를 공유하고 있는 경우에만 이 기능을 제대로 사용할 수 있을 것이라는 사실을 기억하십시오.

메타데이터 수집
----------------

객체 개수를 효율적으로 수집합니다.

범위도 효율적으로 수집하지만, 도형 열이 Elasticsearch 유형 geo_point에 매핑된 경우만입니다. geo_shape 필드 상에서 전체 레이어의 객체를 가져오기 때문에 느릴 수도 있습니다.

쓰기 지원
-------------

색인/유형을 생성하고 삭제할 수 있습니다.

데이터소스를 업데이트 모드로 연 경우에만 쓰기 지원이 활성화됩니다.

비(非) 벌크 모드에서 :cpp:func:`OGRFeature::CreateFeature` 함수로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR이 반환된 \_id를 가져와서 :cpp:func:`OGRFeature::SetFeature` 작업을 위해 사용할 것입니다.

공간 좌표계
------------------------

Elasticsearch에 저장된 도형들은 WGS84 원점(EPSG:4326)의 경도/위도 좌표를 사용할 것입니다. 생성 작업 시, 입력물에 공간 좌표계가 설정되어 있는데 EPSG:4326이 아닌 경우 드라이버가 레이어 (또는 도형 필드) 공간 좌표계로부터 EPSG:4326으로 자동 재투영할 것입니다.

레이어 생성 옵션
----------------------

GDAL 2.1버전부터, 이 드라이버는 다음과 같은 레이어 생성 옵션들을 지원합니다:

-  **INDEX_NAME=name**:
   생성할 (또는 재사용할) 색인의 이름입니다. 기본적으로 색인 이름은 레이어 이름입니다.

-  **INDEX_DEFINITION=filename or JSon**: (GDAL 2.4 이상 버전)
   사용자 정의 색인 정의를 읽어올 파일명을 설정하거나, 또는 그때 그때 즉시 처리하는 색인 정의를 직렬화 JSon으로 처리합니다.

-  **MAPPING_NAME==name**: (Elasticsearch 7 미만 버전)
   색인 내부 매핑 유형의 이름입니다. 매핑 이름은 기본적으로 "FeatureCollection"이며 문서를 GeoJSON Feature 객체로 작성할 것입니다. 다른 매핑 이름을 선택하는 경우, 좀 더 "평탄(flat)"한 구조를 사용할 것입니다. Elasticsearch 7 이상 버전으로 변환하는 경우 이 옵션을 무시합니다. (`매핑 유형 제거 <https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html>`_ 를 참조하십시오.)
   Elasticsearch 7 이상 버전에서는 항상 "평탄"한 구조를 사용합니다.

-  **MAPPING=filename or JSon**:
   사용자 정의 매핑을 읽어올 파일명을 설정하거나, 직렬화 JSon으로 매핑합니다.

-  **WRITE_MAPPING=filename**:
   색인에 삽입하기 전에 사용자가 수정할 수 있는 매핑 파일을 생성합니다. 어떤 객체도 작성하지 않을 것입니다. MAPPING 옵션과 함께 사용할 수 없습니다.

-  **OVERWRITE=YES/NO**:
   기존 유형 매핑을 생성할 레이어 이름으로 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다.

-  **OVERWRITE_INDEX=YES/NO**: (GDAL 2.2 이상 버전)
   레이어가 속해 있는 색인 전체를 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다. 이 옵션은 OVERWRITE 옵션보다 강력합니다. OVERWRITE 옵션은 레이어에 대응하는 유형 매핑이 색인의 단일 유형 매핑인 경우에만 진행됩니다. 유형 매핑이 여러 개 존재하는 경우, 색인 전체를 제거해야 합니다. (매핑과 해당 매핑을 사용하는 문서를 제거하는 것은 위험합니다. 다른 매핑이 사용하는 것일 수도 있기 때문입니다. Elasticsearch 1.X 버전에서는 이런 경우가 있을 수 있지만, 이후 버전에서는 아닙니다.)

-  **GEOMETRY_NAME=name**:
   도형 열의 이름입니다. 기본값은 'geometry'입니다.

-  **GEOM_MAPPING_TYPE=AUTO/GEO_POINT/GEO_SHAPE**:
   도형 열의 매핑 유형입니다. 기본값은 AUTO입니다. GEO_POINT로 설정하면 `geo_point <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-geo-point-type.html>`_ 매핑 유형을 사용합니다. GDAL 2.1 미만 버전에서 이 값을 사용하는 경우, 도형의 "중심점(centroid)"을 사용합니다. GEO_SHAPE으로 설정하면 모든 도형 유형과 호환되는 `geo_shape <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-geo-shape-type.html>`_ 매핑 유형을 사용합니다. 포인트 유형 도형 필드의 경우 AUTO로 설정하면 geo_point를 사용합니다. 다른 유형일 때 AUTO로 설정하면 geo_shape를 사용합니다.

-  **GEO_SHAPE_ENCODING=GeoJSON/WKT**: (GDAL 3.2.1 이상 버전)
   geo_shape 도형 필드 용 인코딩을 설정합니다. 기본값은 GeoJSON입니다. Elasticsearch 6.2버전부터 WKT를 사용할 수 있습니다.

-  **GEOM_PRECISION={value}{unit}**:
   원하는 도형 정밀도를 설정합니다. 숫자값 뒤에 단위를, 예를 들어 1m로 설정합니다. geo_point 도형 필드의 경우 이 옵션을 지정하면 압축 도형 포맷을 사용할 것입니다. MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **STORE_FIELDS=YES/NO**:
   색인에 필드들을 저장해야 할지 여부를 선택합니다. YES로 설정하면 모든 필드에 대해 필드 매핑의 `"store" 속성 <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-core-types.html>`_ 을 "true"로 설정합니다. 기본값은 NO입니다. (주의: GDAL 2.1 미만 버전에서는 필드들을 저장하는 것이 기본 습성입니다.) MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **STORED_FIELDS=string**:
   인덱스에 저장해야 할 필드 이름들을 쉼표로 구분한 목록입니다. 이 필드들은 필드 매핑의 `"store" 속성 <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-core-types.html>`_ 이 "true"로 설정되어 있을 것입니다. 모든 필드를 저장해야만 한다면, STORE_FIELDS=YES를 단축키로 사용할 수 있습니다. MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **NOT_ANALYZED_FIELDS=string**:
   색인 작업 도중 분석하지 말아야 할 필드 이름들을 쉼표로 구분한 목록입니다. 이 필드들은 필드 매핑의 `"index" 속성 <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-core-types.html>`_ 이 "not_analyzed"로 설정되어 있을 것입니다. (Elasticsearch에서 기본값은 "analyzed"입니다.) NOT_ANALYZED_FIELDS 및 NOT_INDEXED_FIELDS 두 옵션 모두에 동일한 필드를 지정해서는 안 됩니다. GDAL 2.2 버전부터, 모든 필드를 지정하려면 {ALL} 값을 사용하면 됩니다. MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **NOT_INDEXED_FIELDS=string**:
   색인되지 말아야 할 필드 이름들을 쉼표로 구분한 목록입니다. 이 필드들은 필드 매핑의 `"index" 속성 <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-core-types.html>`_ 이 "no"로 설정되어 있을 것입니다. (Elasticsearch에서 기본값은 "analyzed"입니다.) NOT_ANALYZED_FIELDS 및 NOT_INDEXED_FIELDS 두 옵션 모두에 동일한 필드를 지정해서는 안 됩니다. MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **FIELDS_WITH_RAW_VALUE=string**: (GDAL 2.2 초과 버전)
   추가적인 raw / not_analyzed 하위 필드와 함께 생성해야 할 (유형 문자열의) 필드 이름들을 쉼표로 구분한 목록입니다. 또는 문자열이 분석된 모든 필드를 지정하고 싶다면 {ALL}으로 설정하십시오. 이 옵션은 필드의 열을 기준으로 필드를 정렬하기 위해 필요합니다. 또 SQL 연산자로 필터링하는 경우 성능을 향상시킬 수 있습니다. MAPPING 옵션을 지정했다면 이 옵션을 무시합니다.

-  **BULK_INSERT=YES/NO**:
   객체 생성을 위해 벌크 삽입을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

-  **BULK_SIZE=value**:
   벌크 업로드를 위한 바이트 단위 버퍼 용량입니다. 기본값은 1,000,000입니다.

-  **FID=string**:
   FID로 사용할 정수값을 가진 필드의 이름입니다. FID 값 작성을 비활성화시키려면 빈 문자열로 설정하면 됩니다. 기본값은 'ogc_fid'입니다.

-  **DOT_AS_NESTED_FIELD=YES/NO**:
   필드 이름에 있는 점('.') 문자를 하위 문서(sub-document)로 간주할지 여부를 선택합니다. 기본값은 YES입니다.

-  **IGNORE_SOURCE_ID=YES/NO**:
   CreateFeature() 함수로 전송되는 객체의 \_id 필드를 무시할지 여부를 선택합니다. 기본값은 NO입니다.

예시
--------

-  로컬 저장소 열기:

::

   ogrinfo ES:

-  원격 저장소 열기:

::

   ogrinfo ES:http://example.com:9200

-  Elasticsearch 필드에 대한 필터링:

::

   ogrinfo -ro ES: my_type -where '{ "post_filter": { "term": { "properties.EAS_ID": 168 } } }'

-  윈도우 시스템 상에서 "match" 쿼리 사용하기:
   윈도우에서는 쿼리를 큰따옴표로 감싸야만 하고, 쿼리 안에 있는 큰따옴표는 이스케이프 처리해야만 합니다.

::

   C:\GDAL_on_Windows>ogrinfo ES: my_type -where "{\"query\": { \"match\": { \"properties.NAME\": \"Helsinki\" } } }"

-  기본 집계:

::

   ogrinfo -ro ES: my_type -oo "AGGREGATION={\"index\":\"my_points\"}"

-  shapefile을 가진 Elasticsearch 색인 불러오기:

::

   ogr2ogr -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

-  매핑 파일 생성하기: 
   매핑 파일은 사용자가 `Elasticsearch 필드 특화 유형 <http://www.elasticsearch.org/guide/reference/mapping/core-types.html>`_ 에 따라 매핑을 수정할 수 있게 해줍니다. 선택할 수 있는 옵션들이 많이 있지만, 대부분의 기능은 Elasticsearch 내부 텍스트 필드로 할 수 있는 서로 다른 모든 작업들을 기반으로 합니다.

::

   ogr2ogr -progress --config ES_WRITEMAP /path/to/file/map.txt -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

   또는 (GDAL 2.1 이상 버전):

::

   ogr2ogr -progress -lco WRITE_MAPPING=/path/to/file/map.txt -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

-  매핑 파일 읽어오기:
   변환 작업 도중 매핑 파일을 읽어옵니다.

::

   ogr2ogr -progress --config ES_META /path/to/file/map.txt -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

   또는 (GDAL 2.1 이상 버전):

::

   ogr2ogr -progress -lco MAPPING=/path/to/file/map.txt -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

-  벌크 업로드하기 (대용량 데이터셋):
   수많은 데이터를 업로드하는 경우 벌크 업로드가 도움이 됩니다. 정수값은 삽입하기 전에 수집하는 바이트 수입니다.
   `벌크 용량 고려 사항 <https://www.elastic.co/guide/en/elasticsearch/guide/current/bulk.html#_how_big_is_too_big>`_ 을 참조하십시오.

::

   ogr2ogr -progress --config ES_BULK 5000000 -f "Elasticsearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

   또는 (GDAL 2.1 이상 버전):

::

   ogr2ogr -progress -lco BULK_SIZE=5000000 -f "Elasticsearch" http://localhost:9200 my_shapefile.shp

-  현재 색인을 덮어쓰기:
   ES_OVERWRITE 옵션을 1로 설정하면 현재 색인을 덮어쓸 것입니다. 설정하지 않는 경우 데이터를 추가할 것입니다.

::

   ogr2ogr -progress --config ES_OVERWRITE 1 -f "Elasticsearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

   또는 (GDAL 2.1 이상 버전):

::

   ogr2ogr -progress -overwrite ES:http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

참고
--------

-  `Elasticsearch 홈페이지 <http://elasticsearch.org/>`_

-  `예제 위키 <http://code.google.com/p/ogr2elasticsearch/w/list>`_

-  `구글 그룹 <http://groups.google.com/group/ogr2elasticsearch>`_

