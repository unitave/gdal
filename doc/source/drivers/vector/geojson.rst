.. _vector.geojson:

GeoJSON
=======

.. shortname:: GeoJSON

.. built_in_by_default::

GeoJSON 드라이버는 `GeoJSON <http://geojson.org/>`_ 서식으로 인코딩된 객체에 접근하기 위한 읽기 및 쓰기 지원을 구현합니다. GeoJSON은 `JSON(JavaScript Object Notation) <http://json.org/>`_ 을 기반으로 하는 방언입니다. JSON은 데이터 정보 교환 용 가벼운 평문 텍스트 서식으로 GeoJSON은 지리 콘텐츠 특화 버전일 뿐입니다.

`GeoServer <http://docs.geoserver.org/2.6.x/en/user/services/wfs/outputformats.html>`_, `CartoWeb <http://exportgge.sourceforge.net/kml/>`_ 등등 수많은 서비스가 산출물 포맷으로서 GeoJSON을 지원하고 있습니다.

OGR GeoJSON 드라이버는 GeoJSON으로 인코딩된 데이터를 `OGR 단순 피처 모델 <ogr_arch.html>`_ 의 Datasource, Layer, Feature, Geometry 객체로 변환합니다. `GeoJSON 사양 1.0버전 <http://geojson.org/geojson-spec.html>`_ 을 기반으로 구현되었습니다.

GDAL 2.1.0버전부터, GeoJSON 드라이버는 기존 GeoJSON 파일의 업데이트를 지원합니다. 이런 경우, NATIVE_DATA 열기 옵션의 기본값이 YES일 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

Datasource
----------

OGR GeoJSON 드라이버는 세 가지 유형의 데이터소스를 입력받습니다:

-  URL(`Uniform Resource Locator <http://en.wikipedia.org/wiki/URL>`_)

   *  `HTTP <http://en.wikipedia.org/wiki/HTTP>`_ 요청을 수행하기 위한 웹 주소입니다.

-  .geojson 또는 .json 파일 확장자로 식별되는, GeoJSON 데이터를 가진 평문 텍스트 파일

-  직접 전송되는, GeoJSON으로 인코딩된 텍스트


GDAL 2.3버전부터, 다른 드라이버들과의 혼동을 피하기 위해 'URL', 'filename', 'text' 앞에 'GeoJSON:' 접두어를 붙여야 할 수도 있습니다.

Layer
-----

GeoJSON 데이터소스는 사전 정의된 *OGRGeoJSON* 이라는 이름을 가진 단일 OGRLayer 객체로 변환됩니다:

::

   ogrinfo -ro http://featureserver/data/.geojson OGRGeoJSON

GeoJSON 데이터소스에 대해 OGRDataSource::GetLayerCount()를 호출하면 언제나 1을 반환한다고 가정해도 무방합니다.

GDAL 2.2버전부터, 레이어 이름을 다음 논리에 따라 작성합니다:

#. FeatureCollection 수준에 "name" 멤버가 존재하는 경우, 해당 이름을 사용합니다.
#. 존재하지 않고 파일명이 정규인 경우 (예를 들어 쿼리 파라미터를 가진 URL이 아닌 경우) 확장자 및 경로가 없는 파일명을 레이어 이름으로 사용합니다.
#. 둘 다 아니라면 OGRGeoJSON을 사용합니다.

웹 서비스를 데이터소스로 (예: FeatureServer로) 접근하면, 각각의 요청이 새 레이어를 생성할 것입니다. 이 습성은 HTTP 트랜잭션의 무상태적인(stateless) 본질을 준수하며 단일 요청 == 단일 페이지라는 웹브라우저 작동 방식과 유사합니다.

GeoJSON 데이터의 최상위 멤버가 *FeatureCollection* 이 아닌 다른 유형일 경우, 이 드라이버는 객체 하나만 가지고 있는 레이어 하나를 생성할 것입니다. 최상위 멤버가 *FeatureCollection* 인 경우, 객체 집합으로 이루어진 레이어를 생성할 것입니다.

NATIVE_DATA 열기 옵션을 YES로 설정하면, FeatureCollection 수준에 있는 멤버를 레이어 객체의 NATIVE_DATA 메타데이터 도메인의 NATIVE_DATA 항목에 직렬화된 JSon 객체로 저장할 것입니다. (그리고 NATIVE_DATA 메타데이터 도메인의 NATIVE_MEDIA_TYPE 항목에 "application/vnd.geo+json"을 저장할 것입니다.)

Feature
-------

OGR GeoJSON 드라이버는 Point, LineString, Polygon, GeometryCollection, Feature 유형의 객체를 각각 새로운 *OGRFeature* 객체와 매핑시킵니다.

*GeoJSON 사양* 에 따라, *Feature* 유형의 객체만 *properties* 라는 이름의 멤버를 가져야만 합니다. *properties* 의 멤버 각각 그리고 모두는 OGRField 유형의 OGR 객체로 변환되어 대응하는 OGRFeature 객체에 추가됩니다.

*GeoJSON 사양* 은 집합에 있는 모든 *Feature* 유형의 객체가 동일한 속성 스키마를 가질 것을 요구하지 않습니다. *FeatureCollection* 객체가 정의하는 집합에 있는 *Feature* 유형의 객체들이 서로 다른 속성 스키마를 가지고 있는 경우, OGRFeatureDefn에 산출되는 필드 스키마를 모든 *Feature* 속성의 `합집합 <https://ko.wikipedia.org/wiki/%ED%95%A9%EC%A7%91%ED%95%A9>`_ 으로 생성합니다.

스키마 탐지는 String, Integer, Real, StringList, IntegerList 및 RealList, Integer(Boolean), Date, Time 및 DateTime 유형의 필드를 인식할 것입니다.

:decl_configoption:`ATTRIBUTES_SKIP` 환경설정 옵션을 YES로 설정하면 드라이버가 속성을 처리하는 것을 막을 수 있습니다. 기본 습성은 모든 속성을 (앞에서 설명한 것처럼 합집합으로) 보전하는 것입니다. 이는 :decl_configoption:`ATTRIBUTES_SKIP` 옵션을 NO로 설정한 것과 동일한 효과입니다.

NATIVE_DATA 열기 옵션을 YES로 설정하면, Feature JSon 객체를 OGRFeature 객체의 NativeData 속성에 직렬화된 JSon 객체로 저장할 것입니다. (그리고 NativeMediaType 속성에 "application/vnd.geo+json"을 저장할 것입니다.)
쓰기 작업 시, 작성할 OGRFeature의 NativeMediaType 속성이 직렬화된 JSon 객체인 문자열로 설정되었다면 이 객체의 (예를 들면 "property" 딕셔너리도 아니고 도형 좌표의 처음 3개의 차원도 아닌) 추가 멤버들을 사용해서 OGRFeature로부터 생성된 JSon 객체를 향상시킬 것입니다. 더 자세한 정보는 :ref:`rfc-60` 을 참조하십시오.

Geometry
--------

혼합 속성 객체의 문제점과 마찬가지로, *GeoJSON 사양* 초안은 집합에 있는 모든 *Feature* 유형의 객체가 동일한 유형의 도형일 것을 요구하지 않습니다. 다행히 OGR 객체 모델이 단일 레이어에 서로 다른 유형의 도형들이 존재하는 것을 -- 혼성(heterogeneous) 레이어를 허용하고 있습니다. GeoJSON 드라이버는 기본적으로 도형 유형을 보전합니다.

하지만, 혼성 객체들의 집합으로부터 동종(homogeneous) 레이어를 생성해야 하는 경우도 있습니다. 이를 위해 드라이버에 OGRGeometryCollection 유형을 공통분모로 사용해서 모든 도형들을 묶으라고 지시할 수 있습니다. :decl_configoption:`GEOMETRY_AS_COLLECTION` 환경설정 옵션을 YES로 설정하면 이 습성을 제어할 수도 있습니다. (기본값은 NO입니다.)

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`GEOMETRY_AS_COLLECTION`:
   도형의 변환을 제어하기 위해 사용합니다. YES로 설정하면 OGRGeometryCollection 유형으로 도형들을 묶습니다.

-  :decl_configoption:`ATTRIBUTES_SKIP`:
   속성의 변환을 제어하기 위해 사용합니다. YES로 설정하면 모든 속성을 건너뜁니다.

-  :decl_configoption:`OGR_GEOJSON_MAX_OBJ_SIZE`: (GDAL 3.0.2 이상 버전)
   입력받을 수 있는 단일 피처의 최대 용량을 MB 단위로 설정합니다. 기본값은 200MB입니다.

열기 옵션
------------

-  **FLATTEN_NESTED_ATTRIBUTES=YES/NO**:
   내포된 객체들을 재귀적으로 탐색해서 평탄화된(flatten) OGR 속성을 생산할지 여부를 선택합니다. 기본값은 NO입니다.

-  **NESTED_ATTRIBUTE_SEPARATOR=character**:
   내포된 속성들의 구성요소들 사이의 구분자입니다. 기본값은 '_'입니다.

-  **FEATURE_SERVER_PAGING=YES/NO**:
   ArcGIS 피처 서비스 종단점을 가진 결과물을 자동 스크롤할지 여부를 선택합니다.

-  **NATIVE_DATA=YES/NO**: (GDAL 2.1 이상 버전)
   FeatureCollection 및 Feature 수준에 있는 네이티브 JSon 표현을 저장할지 여부를 선택합니다. 기본값은 NO입니다. 이 옵션을 사용하면, OGR 추상이 다른 경우에는 무시했을 추가 JSon 객체를 보전해서 GeoJSON에서 GeoJSON으로의 (데이터를 내보냈다가 손실 없이 무결하게 다시 가져오는) 라운드트립 작업을 향상시킬 수 있습니다. 사용자가 -noNativeData 스위치를 지정하지 않는 이상 ogr2ogr 유틸리티는 기본적으로 이 옵션을 활성화시킨다는 사실을 기억하십시오.

-  **ARRAY_AS_STRING=YES/NO**: (GDAL 2.1 이상 버전)
   문자열, 정수 또는 실수형의 JSon 배열을 OGR String 유형으로 노출시킬지 여부를 선택합니다. 기본값은 NO입니다. :decl_configoption:`OGR_GEOJSON_ARRAY_AS_STRING` 환경설정 옵션으로도 설정할 수 있습니다.

-  **DATE_AS_STRING=YES/NO**: (GDAL 3.0.3 이상 버전)
   날짜/시간/날짜&시간 유형 콘텐츠를 전용 OGR 날짜/시간/날짜&시간 유형으로 노출시킬지 또는 OGR String 유형으로 노출시킬지를 선택합니다. 기본값은 NO입니다. (즉 날짜/시간/날짜&시간 유형을 그대로 탐지한다는 뜻입니다.)
   :decl_configoption:`OGR_GEOJSON_DATE_AS_STRING` 환경설정 옵션으로도 설정할 수 있습니다.

FLATTEN_NESTED_ATTRIBUTES 옵션을 설명하자면, 다음과 같은 GeoJSON 조각이 있다고 할 때:

::

   {
     "type": "FeatureCollection",
     "features":
     [
       {
         "type": "Feature",
         "geometry": {
           "type": "Point",
           "coordinates": [ 2, 49 ]
         },
         "properties": {
           "a_property": "foo",
           "some_object": {
             "a_property": 1,
             "another_property": 2
           }
         }
       }
     ]
   }

"ogrinfo test.json -al -oo FLATTEN_NESTED_ATTRIBUTES=yes" 명령어는 다음을 리포트합니다:

::

   OGRFeature(OGRGeoJSON):0
     a_property (String) = foo
     some_object_a_property (Integer) = 1
     some_object_another_property (Integer) = 2
     POINT (2 49)

레이어 생성 옵션
----------------------

-  **WRITE_BBOX=YES/NO**:
   이 옵션을 YES로 설정하면 bbox 속성을 객체 및 객체 집합 수준에 있는 도형들의 경계 상자로 작성합니다. 기본값은 NO입니다.

-  **COORDINATE_PRECISION=int_number**:
   좌표값의 소수점 뒤에 작성할 최대 자릿수를 설정합니다. 기본값은 GeoJSON 2008의 경우 15, RFC 7946의 경우 7입니다. 후행 0들을 제거하기 위해 "스마트" 절단(truncation)을 수행할 것입니다.

-  **SIGNIFICANT_FIGURES=int_number**: (OGR 2.1 이상 버전)
   부동소수점형 숫자를 작성할 때 산출할 유효 숫자(significant digit) 자릿수를 지정합니다. 기본값은 17입니다. 이 옵션을 명확하게 지정하고 COORDINATE_PRECISION 옵션은 지정하지 않은 경우, 좌표에도 이 옵션을 적용할 것입니다.

-  **NATIVE_DATA=string**: (OGR 2.1 이상 버전)
   FeatureCollection 수준에 저장할 추가 속성들을 담고 있는 직렬화된 JSon 객체입니다.

-  **NATIVE_MEDIA_TYPE=string**: (OGR 2.1 이상 버전)
   NATIVE_DATA의 서식입니다. "application/vnd.geo+json"이어야만 합니다. 그렇지 않은 경우 NATIVE_DATA를 무시할 것입니다.

-  **RFC7946=YES/NO**: (OGR 2.2 이상 버전)
   `RFC 7946 <https://tools.ietf.org/html/rfc7946>`_ 표준을 사용할지 여부를 선택합니다. 사용하지 않을 경우 `GeoJSON 2008 <http://geojson.org/geojson-spec.html>`_ 초기 버전을 사용할 것입니다. 기본값은 NO(즉 GeoJSON 2008)입니다.

-  **WRITE_NAME=YES/NO**: (OGR 2.2 이상 버전)
   객체 집합 수준에 있는 "name" 속성을 레이어 이름으로 작성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **DESCRIPTION=string**: (OGR 2.2 이상 버전) (Long)
   객체 집합 수준에 있는 "description" 속성에 작성할 설명입니다. 읽기 작업 시, 레이어의 DESCRIPTION 메타데이터 항목에 이 문자열을 리포트할 것입니다.

-  **ID_FIELD=string**: (OGR 2.3 이상 버전)
   Feature 객체의 'id' 멤버로 작성해야만 하는 소스 필드의 이름을 설정합니다.

-  **ID_TYPE=AUTO/String/Integer**: (OGR 2.3 이상 버전)
   Feature 객체의 'id' 멤버의 유형을 설정합니다.

-  **ID_GENERATE=YES/NO**: (OGR 3.1 이상 버전)
   FID(Feature ID)를 자동 생성할지 여부를 선택합니다.

-  **WRITE_NON_FINITE_VALUES=YES/NO**: (OGR 2.4 이상 버전)
   NaN / Infinity 값을 작성할지 여부를 선택합니다. 엄격한 JSon 모드에서는 이런 값을 허용하지 않지만, 일부 JSon 파서(parser)는 (예를 들어 libjson-c 0.12 이상 버전은) ECMAScript가 이런 값을 허용하기 때문에 이를 인식할 수 있습니다. 기본값은 NO입니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

추가 JSon 멤버의 라운드트립 작업
------------------------------------

자세한 내용은 :ref:`rfc-60` 을 참조하십시오.

GDAL 2.1버전부터 소스 및 대상 모두에 GeoJSON을 가진 ogr2ogr 유틸리티를 실행하는 경우, 아래 코드 조각에 있는 "extra_XXXXX_member" 라는 추가 JSon 멤버 같은, 일반적으로 OGR 추상에 반영되지 않는 FeatureCollection, Feature 또는 Geometry 수준에 있는 추가 JSon 멤버를 기본적으로 보전합니다.
이런 습성은 변환 작업이 도형 구조를 보전하는 경우 (예를 들면 재투영할 수는 있지만 좌표 몇 개가 변경되지 않는 경우) 세 번째 차원을 넘어서는 (아래 예시에서는 100, 101) 도형들의 위치 투플(tuple)에 있는 추가값들에도 적용됩니다.

::

   {
     "type": "FeatureCollection",
     "extra_fc_member": "foo",
     "features":
     [
       {
         "type": "Feature",
         "extra_feat_member": "bar",
         "geometry": {
           "type": "Point",
           "extra_geom_member": "baz",
           "coordinates": [ 2, 49, 3, 100, 101 ]
         },
         "properties": {
           "a_property": "foo",
         }
       }
     ]
   }

ogr2ogr 유틸리티의 **-noNativeData** 스위치를 지정하면 이 습성을 비활성화시킬 수 있습니다.

RFC 7946 쓰기 지원
----------------------

이 드라이버는 기본적으로 GeoJSON 2008 사양에 따라 GeoJSON 파일을 작성할 것입니다. RFC7946 생성 옵션을 YES로 설정하면 RFC 7946 표준을 대신 사용할 것입니다.

이 두 버전 사이의 차이점은 `RFC 7946 부록 B <https://tools.ietf.org/html/rfc7946#appendix-B>`_ 에서 언급하고 있으며, 여기에서는 이 드라이버에 중요한 차이점만 발췌합니다:

-  좌표는 WGS84 타원체를 사용하는 지리 좌표계여야만 하기 때문에, 레이어 생성 시 지정한 공간 좌표계가 EPSG:4326가 아닌 경우 드라이버가 실시간으로(on-the-fly) 재투영할 것입니다.

-  폴리곤은 방향이 오른손 법칙을 따르도록 (외부 고리는 반시계 방향으로, 내부 고리는 시계 방향으로) 작성할 것입니다.

-  "bbox" 배열의 값은 "[minx, miny, maxx, maxy]"가 아니라 "[west, south, east, north]"입니다.

-  몇몇 확장 사양 멤버 이름들은 (라운드트립 단락 참조) FeatureCollection, Feature 및 Geometry 객체에서 금지됩니다.

-  기본 좌표계 정밀도는 소수점 이하 7자리입니다.

예시
--------

-  .geojson 파일의 내용을 덤프하기:

::

   ogrinfo -ro point.geojson

-  속성 필터를 사용해서 원격 서비스로부터 객체 쿼리하기:

::

   ogrinfo -ro http://featureserver/cities/.geojson OGRGeoJSON -where "name=Warsaw"

-  FeatureServer로부터 쿼리해온 객체 몇 개를 ESRI Shapefile로 변환하기:

::

   ogr2ogr -f "ESRI Shapefile" cities.shp http://featureserver/cities/.geojson OGRGeoJSON

-  ESRI Shapefile을 RFC 7946 GeoJSON 파일로 변환하기:

::

   ogr2ogr -f GeoJSON cities.json cities.shp -lco RFC7946=YES

참고
--------

-  `GeoJSON <http://geojson.org/>`_ -- 지리 콘텐츠를 JSON으로 인코딩

-  `RFC 7946 <https://tools.ietf.org/html/rfc7946>`_ 표준

-  `GeoJSON 2008 <http://geojson.org/geojson-spec.html>`_ 사양 (RFC 7946으로 폐기)

-  `JSON <http://json.org/>`_ - JavaScript Object Notation

-  :ref:`GeoJSON 시퀀스 <vector.geojsonseq>` 드라이버

-  :ref:`ESRIJSON / FeatureService <vector.esrijson>` 드라이버

-  :ref:`TopoJSON <vector.topojson>` 드라이버

