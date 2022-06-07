.. _rfc-60:

=======================================================================================
RFC 60 : ORG의 미봉책 개선
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.1버전에 구현

요약
----

이 RFC는 벡터 포맷, 특히 GeoJSON 확장 사양을 변환하는 과정에서 미봉책(round-tripping)을 어떻게 개선할 것인지를 정의합니다.

근거
----

일부 포맷들이 OGR 추상화로는 제대로 모델링할 수 없는 개념을 가지고 있기는 하지만, 대상 포맷이 소스 포맷인 경우 재투영, 공간/속성 필터링, 자르기 등등을 수반하는 변환 시나리오에서 이런 개념을 보전하는 것이 바람직합니다.

핵심 GeoJSON 사양의 FeatureCollection, Feature 또는 Geometry 수준에서 다양한 확장 사양들이 존재합니다.

`carmen geojson <https://github.com/mapbox/carmen/blob/master/carmen-geojson.md>`_ 과:

::

   {
       "type": "FeatureCollection",
       "query": ["austin"],
       "features": [
           {
               "type": "Feature",
               "id": "place.4201",
               "text": "Austin",
               "place_name": "Austin, Texas, United States",
               "bbox": [-97.9383829999999, 30.098659, -97.5614889999999, 30.516863],
               "center": [-97.7559964, 30.3071816],
               "geometry": {
                   "type": "Point",
                   "coordinates": [-97.7559964, 30.3071816]
               },
               "properties": {
                   "title": "Austin",
                   "type": "city",
                   "score": 600000790107194.8
               },
               "context": [
                   {
                       "id": "province.293",
                       "text": "Texas"
                   },
                   {
                       "id": "country.51",
                       "text": "United States"
                   }
               ]
           },
           ...
       ]
   }

`https://github.com/geocoders/geocodejson-spec/blob/master/draft/README.md <https://github.com/geocoders/geocodejson-spec/blob/master/draft/README.md>`_ 및:

::

   {

     // 필수. GeocodeJSON 결과물이 FeatureCollection입니다.
     "type": "FeatureCollection",

     // 필수. 이름공간입니다.
     "geocoding": {

       // 필수. semver.org을 준수하는 버전 번호입니다. 이 인스턴스가 구현하는
       // GeocodeJSON 사양의 버전을 서술합니다.
       "version": "0.1.0",

       // 선택적. 기본값: NULL. 데이터의 사용 허가(licence)입니다. 소스가 여러 개이고
       // 사용 허가도 여러 개인 경우, 소스의 키 하나를 가진 객체일 수 있습니다.
       "licence": "ODbL",

       // 선택적. 기본값: NULL. 데이터의 속성입니다. 소스가 여러 개이고
       // 속성도 여러 개인 경우, 소스의 키 하나를 가진 객체일 수 있습니다.
       "attribution": "OpenStreetMap Contributors",

       // 선택적. 기본값: NULL. 검색을 촉발하기 위해 발행된 쿼리입니다.
       "query": "24 allée de Bercy 75012 Paris",

     },

     // 필수. GeoJSON 사양을 따릅니다.
     "features": [
       // 선택적. 피처 객체 배열입니다. 다음을 참조하십시오.
     ]
   }

또는 `https://github.com/geojson/draft-geojson/issues/80#issuecomment-138037554 <https://github.com/geojson/draft-geojson/issues/80#issuecomment-138037554>`_ 를 참조하십시오:

::

   { "type" : "GeometryCollection",
     "geometries" : [
       { "type" : "LineString",
         "extensions" : [ "time", "atemp", "hr", "cad" ],
         "coordinates" : [
           [
             -122.45671039447188,
             37.786870915442705,
             0.4000000059604645, 
             "2014-11-06T19:16:06.000Z", 
             31.0, 
             99, 
             0
           ], 

변경 사항
---------

OGRFeature
~~~~~~~~~~

:cpp:class:`OGRFeature` 클래스에 m_pszNativeData(문자열) 및 m_pszNativeMediaType(문자열) 2개의 멤버를 추가할 것입니다.  m_pszNativeData는 원본 피처의 표현(또는 표현의 일부분)을 담고, m_pszNativeMediaType은 `미디어 유형 <https://ko.wikipedia.org/wiki/%EB%AF%B8%EB%94%94%EC%96%B4_%ED%83%80%EC%9E%85>`_ 을 담을 것입니다.

:cpp:class:`OGRFeature` 클래스에 다음 메소드들을 추가할 것입니다:

::

   public:
       const char *GetNativeData() const;
       const char *GetNativeMediaType() const;
       void        SetNativeData( const char* pszNativeData );
       void        SetNativeMediaType( const char* pszNativeMediaType );

따라서 GeoJSON의 경우 nativeData가 GeoJSON Feature의 완전한 직렬화를 담을 것입니다. m_pszNativeMediaType은 "application/vnd.geo+json"으로 설정될 것입니다. GeoJSON 드라이버의 작성기 쪽은 nativeData가 존재하는 경우 (그리고 nativeMediaType이 "application/vnd.geo+json"인 경우) nativeData로부터 시작하고, 그 속성 멤버를 OGR 필드의 내용으로 대체하며, 그 도형이 추가적인 JSON 객체를 포함하도록 패치할 것입니다.

:cpp:func:`OGRFeature::Clone` 및 :cpp:func:`OGRFeature::SetFrom` 메소드가 nativeData 및 nativeMediaType을 전파할 것입니다.

OGRLayer
~~~~~~~~

그 안에 "NATIVE_DATA"가 있을 "NATIVE_DATA"와 "NATIVE_MEDIA_TYPE" 전용 메타데이터 도메인을 사용할 것입니다. GeoJSON의 경우 이 전용 도메인이 FeatureCollection 수준에서 (당연히 피처 배열을 제외한) JSON 멤버들을 담을 것입니다.

Driver 열기 옵션 및 레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

읽기 시 nativeData를 지원하는 드라이버는 NATIVE_DATA 불(boolean) 열기 옵션을 노출시키고, 성능에 영향을 미치지 않기 위해 기본적으로 비활성화시켜야 합니다. ogr2ogr는 기본적으로 이 옵션을 활성화시킬 것입니다.

쓰기 시 레이어 수준에서 nativeData를 지원하는 드라이버는 NATIVE_DATA 문자열 및 NATIVE_MEDIA_TYPE 문자열 레이어 생성 옵션을 노출시켜 ogr2ogr가 소스 레이어(들)의 NATIVE_DATA 메타데이터 도메인의 내용으로 두 생성 옵션을 채울 수 있게 해야 합니다.

C API
-----

다음 함수들을 추가할 것입니다:

::

   const char CPL_DLL *OGR_F_GetNativeData(OGRFeatureH);
   void OGR_F_SetNativeData(OGRFeatureH, const char*);
   const char CPL_DLL *OGR_F_GetNativeMediaType(OGRFeatureH);
   void OGR_F_SetNativeMediaType(OGRFeatureH, const char*);

SQL 산출 레이어
---------------

OGR SQL 및 SQLite SQL 방언 구현이 소스 레이어의 (FROM 테이블의) NATIVE_DATA 메타데이터 도메인의 내용을 대상 레이어로 전파하고, 소스 피처의 NativeData 및 NativeMediaType을 대상 피처로 복사하도록 수정했습니다.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

SWIG에 새 함수들을 GetNativeData(), SetNativeData(), GetNativeMediaType() and SetNativeMediaType()으로 매핑할 것입니다.

드라이버
--------

GeoJSON 드라이버가 읽기 및 쓰기 시 이 RFC를 구현하도록 수정할 것이기 때문에:

-  레이어 및 피처의 네이티브 데이터를 저장할 수 있는 NATIVE_DATA 열기 옵션을 선언할 것입니다.
-  FeatureCollection 수준에서 네이티브 데이터를 작성할 수 있도록 NATIVE_DATA 및 NATIVE_MEDIA_TYPE 레이어 생성 옵션도 선언할 것입니다.
-  쓰기 시 :cpp:class:`OGRFeature` nativeData를 사용할 것입니다.

이 변경 사항이 미치는 영향은 ogr2ogr가 다음 코드 조각에서 ``***`` 사이에 표시된 멤버들을 보전할 수 있게 된다는 점입니다:

::

   {
     "type": "FeatureCollection",
     ***"extra_fc_member": "foo",***
     "features":
     [
       {
         "type": "Feature",
         ***"extra_feat_member": "bar",***
         "geometry": {
           "type": "Point",
           ***extra_geom_member": "baz",***
           "coordinates": [ 2, 49, 3, ***100, 101*** ]
         },
         "properties": {
           "a_property": "foo",
         }
       }
     ]
   }


``_json`` OGR 필드를 미봉책(round-tripping)으로 사용하는 ElasticSearch 및 MongoDB 같은 다른 드라이버들도 이 RFC의 메커니즘으로부터 혜택을 받을 수 있도록 업그레이드할 수도 있습니다.

유틸리티
--------

ogr2ogr가 레이어 및 피처 수준에서 자동으로 nativeData를 복사하도록 수정할 것입니다. 이렇게 하는 것이 바람직하지 않을 경우, 자동 복사를 막을 수 있는 "-noNativeData" 플래그를 추가할 것입니다.

기본적으로 ogr2ogr는 데이터소스를 NATIVE_DATA=YES 열기 옵션으로 열 것이기 때문에 nativeData를 저장할 수 있는 드라이버는 nativeData를 저장할 것입니다. 그리고 산출 데이터소스가 NATIVE_DATA 및 NATIVE_MEDIA_TYPE 레이어 생성 옵션을 지원하는 경우, 두 옵션을 소스 레이어의 NATIVE_DATA 메타데이터 도메인의 내용으로 채울 것입니다.

문서화
------

새 메소드 및 함수를 모두 문서화합니다.

테스트 스위트
-------------

GeoJSON 및 ogr2ogr 관련 테스트를 확장할 것입니다.

호환성 문제점
-------------

심각한 문제점은 예상되지 않습니다. 기존 스크립트에 예전 습성으로 돌아가기 위한 "-noNativeData"를 추가해야 할 수도 있습니다.

관련 티켓
---------

`#5310 티켓 <https://trac.osgeo.org/gdal/ticket/5310>`_

구현
----

이벤 루올(`Spatialys <http://www.spatialys.com>`_)이 `Mapbox <https://www.mapbox.com/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc60_native_data" 브랜치 <https://github.com/rouault/gdal2/tree/rfc60_native_data>`_ 와 `#75 풀 요청 <https://github.com/OSGeo/gdal/pull/75>`_ 에 있습니다.

투표 이력
---------

-  하워드 버틀러 +1
-  커트 슈베어(Kurt Schwehr) +1
-  세케레시 터마시 +1
-  유카 라흐코넨 +1
-  이벤 루올 +1

