.. _vector.ngw:

NGW -- NextGIS 웹
==================

.. versionadded:: 2.4

.. shortname:: NGW

.. build_dependencies:: libcurl

NextGIS 웹은 서버 GIS로, 지리 데이터(geodata)를 저장하고 편집할 수 있으며 웹브라우저에 맵을 출력할 수 있습니다. 또한 NextGIS 웹은 다른 NextGIS 소프트웨어와 지리 데이터를 공유할 수 있습니다.

NextGIS 웹은 다음과 같은 기능을 가지고 있습니다:

-  웹브라우저에 (서로 다른 레이어 및 스타일을 가진 서로 다른) 맵을 출력하기
-  유연한 권한 관리
-  PostGIS로부터 지리 데이터 불러오기 또는 GIS 포맷(ESRI Shapefile, GeoJSON 또는 GeoTIFF)로부터 가져오기
-  다음 포맷에 있는 벡터 지리 데이터 불러오기: GeoJSON, CSV, ESRI Shapefile, Mapinfo 탭(tab)
-  QGIS 프로젝트로부터 맵 스타일 가져오기 또는 직접 설정하기
-  TMS, WMS, MVT, WFS 서버 역할
-  WMS 클라이언트 역할
-  사용자가 웹 인터페이스 또는 WFS-T 프로토콜을 통해 레코드에 사진을 추가하고 레코드 속성을 변경할 수 있습니다.

NextGIS 웹은 오픈소스 소프트웨어입니다. (GPL 버전 2 이상의 사용 허가, `GNU 일반 공중 사용 허가서 버전 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>`_ 참조)

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

드라이버
------

NGW 드라이버는 NextGIS 웹 REST API를 구현하는 서비스에 접속할 수 있습니다.
이 드라이버를 사용하려면 GDAL이 cURL을 지원해야 합니다. 이 드라이버는 읽기 및 쓰기 작업을 지원합니다.

데이터셋 이름 문법
-------------------

NGW 데이터소스를 열 수 있는 최소한의 문법은 다음과 같습니다:

::

   NGW:[NextGIS 웹 URL][/resource/][resource identifier]

-  **NextGIS 웹 URL** 은 nextgis.com 클라우드 서비스를 (예를 들어 https://demo.nextgis.com 을) 가리키는 URL일 수도 있습니다. 또는 포트 번호와 추가 경로를 포함하는 (예를 들면 http://192.168.1.1:8000/test 같은) 다른 URL일 수도 있습니다.
-  **resource** 는 리소스 식별자를 URL 나머지 부분과 구분하는 필수 키워드입니다.
-  **resource identifier** 는 0 이상의 양의 숫자입니다. 리소스 그룹, 벡터, PostGIS 또는 래스터 레이어, 스타일일 수도 있습니다.

모든 벡터 레이어, PostGIS, 래스터 레이어, 스타일은 식별자가 리소스 그룹인 경우 하위 리소스로 목록화됩니다. 그렇지 않은 경우 각각 개별 레이어가 될 것입니다.

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`NGW_USERPWD`:
   쌍점(':')으로 구분된 사용자명과 비밀번호입니다. 선택적인 옵션으로 열기 옵션으로도 설정할 수 있습니다.
-  :decl_configoption:`NGW_BATCH_SIZE`:
   서버로 전송하기 전 객체 삽입 및 업데이터 작업 캐시의 용량입니다. 배치(batch) 용량을 -1로 설정하면 배치 모드를 비활성화합니다. 삭제 작업은 즉시 실행될 것입니다.
-  :decl_configoption:`NGW_PAGE_SIZE`:
   서버가 지원하는 경우, 페이지 작업을 통해 원격 서버로부터 객체를 가져올 것입니다. -1로 설정하면 서버가 지원하더라도 페이지 작업을 비활성화합니다.
-  :decl_configoption:`NGW_NATIVE_DATA`:
   객체 네이티브 데이터에 JSon *extensions* 키를 저장할지 여부를 선택합니다.
-  :decl_configoption:`NGW_JSON_DEPTH`:
   파싱할 수 있는 JSon 응답의 심도를 지정합니다. 심도가 이 옵션값을 초과하는 경우, 파싱 오류를 발생시킵니다.
-  :decl_configoption:`NGW_EXTENSIONS`:
   쉼표로 구분한 확장 사양 목록입니다. `description` 및 `attachment` 값을 사용할 수 있습니다. 네이티브 데이터를 채우기 위해 필요합니다.

인증
--------------

어떤 작업이든 (읽기, 쓰기, 메타데이터 가져오기, 속성 변경 등등) 인증된 접근을 요구할 수도 있습니다. 열기, 생성 및 환경설정 옵션으로 사용자명과 비밀번호를 지정하면 인증된 접근을 할 수 있습니다.

객체
-------

NATIVE_DATA 열기 옵션을 YES로 설정한 경우, OGRFeature 객체의 NativeData 속성에 (그리고 NativeMediaType 속성의 "application/json"에) *extensions* JSon 객체를 직렬화 JSon 객체로 저장할 것입니다. 작성하는 OGRFeature의 NativeMediaType 속성이 "application/json"으로 설정되어 있고 NativeData 속성이 직렬화 JSon 객체로 설정되어 있다면, 해당 JSon 객체로부터 새 NGW 객체의 *extensions* JSon 객체를 채울 것입니다.

`NextGIS 웹 API 문서 <http://docs.nextgis.comu/docs_ngweb_dev/doc/developer/resource.html#feature>`_ 에서 확장 사양 JSon 객체 구조를 살펴볼 수 있습니다.

도형
--------

NextGIS 웹은 단 하나의 도형 열만 지원합니다. 기본 공간 좌표계는 웹 메르카토르(EPSG:3857)입니다. 다음 도형 유형들을 사용할 수 있습니다:

-  POINT
-  LINESTRING
-  POLYGON
-  MULTIPOINT
-  MULTILINESTRING
-  MULTIPOLYGON

Z값을 가진 도형도 지원합니다.

필드 데이터 유형
----------------

NextGIS 웹은 다음 필드 유형들만 지원합니다:

-  OFTInteger
-  OFTInteger64
-  OFTReal
-  OFTString
-  OFTDate
-  OFTTime
-  OFTDateTime

페이지 작업(paging)
------------------

서버가 지원하는 경우 NextGIS 웹으로부터 객체들을 덩어리로 가져올 수 있습니다. :decl_configoption:`NGW_PAGE_SIZE` 환경설정 옵션 또는 PAGE_SIZE 열기 옵션으로 이 덩어리 크기를 변경할 수 있습니다.

쓰기 지원
-------------

데이터소스 및 레이어를 생성 및 삭제할 수 있습니다. 데이터소스를 업데이트 모드로 열고 사용자가 적절한 권한을 가지고 있는 경우에만 쓰기 지원이 활성화됩니다. BATCH_SIZE가 0보다 큰 경우에만 벡터 및 PostGIS 레이어 삽입과 업데이트 작업을 캐시에 저장합니다. 삭제 작업은 즉시 실행됩니다.

열기 옵션
------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **USERPWD**: 쌍점으로 구분된 사용자명과 비밀번호입니다.
-  **PAGE_SIZE=-1**: 서버로부터 가져오는 객체의 개수를 제한합니다. -1로 설정하면 무제한입니다.
-  **BATCH_SIZE=-1**: 서버로 전송하기 전 객체 삽입 및 업데이터 작업 캐시의 용량입니다. 배치(batch) 용량을 -1로 설정하면 배치 모드를 비활성화합니다. 기본값은 -1입니다.
-  **NATIVE_DATA=NO**: 객체 네이티브 데이터에 JSon *extensions* 키를 저장할지 여부를 선택합니다. 기본값은 NO입니다.
-  **JSON_DEPTH=32**: 파싱할 수 있는 JSon 응답의 심도를 지정합니다. 심도가 이 옵션값을 초과하는 경우, 파싱 오류를 발생시킵니다.
-  **EXTENSIONS**: 쉼표로 구분한 확장 사양 목록입니다. `description` 및 `attachment` 값을 사용할 수 있습니다. 네이티브 데이터를 채우기 위해 필요합니다.

데이터셋 생성 옵션
------------------------

다음 데이터셋/데이터소스 생성 옵션들을 사용할 수 있습니다:

-  **KEY**: 키 값입니다. 전체 NextGIS 웹 인스턴스에서 유일한 값이어야만 합니다. 선택 옵션입니다.
-  **DESCRIPTION**: 리소스 설명입니다. 선택 옵션입니다.
-  **USERPWD**: 쌍점으로 구분된 사용자명과 비밀번호입니다.
-  **PAGE_SIZE=-1**: 서버로부터 가져오는 객체의 개수를 제한합니다. 기본값인 -1로 설정하면 무제한입니다.
-  **BATCH_SIZE=-1**: 서버로 전송하기 전 객체 삽입 및 업데이터 작업 캐시의 용량입니다. 배치(batch) 용량을 -1로 설정하면 배치 모드를 비활성화합니다. 기본값은 -1입니다.
-  **NATIVE_DATA=NO**: 객체 네이티브 데이터에 JSon *extensions* 키를 저장할지 여부를 선택합니다. 기본값은 NO입니다.
-  **JSON_DEPTH=32**: 파싱할 수 있는 JSon 응답의 심도를 지정합니다. 심도가 이 옵션값을 초과하는 경우, 파싱 오류를 발생시킵니다.
-  **EXTENSIONS**: 쉼표로 구분한 확장 사양 목록입니다. `description` 및 `attachment` 값을 사용할 수 있습니다. 네이티브 데이터를 채우기 위해 필요합니다.

레이어 생성 옵션
----------------------

다음 레이어 생성 옵션들을 사용할 수 있습니다:

-  **OVERWRITE**: 생성할 레이어 이름을 가진 기존 테이블을 덮어쓸지 여부를 선택합니다. 리소스를 삭제하고 새 리소스를 생성할 것입니다. 리소스 식별자가 바뀌게 됩니다. 기본값은 NO입니다. 선택 옵션입니다.
-  **KEY**: 키 값입니다. 전체 NextGIS 웹 인스턴스에서 유일한 값이어야만 합니다. 선택 옵션입니다.
-  **DESCRIPTION**: 리소스 설명입니다. 선택 옵션입니다.

메타데이터
----------

데이터소스, 벡터, PostGIS, 래스터 레이어 및 스타일에서 NextGIS 웹 메타데이터를 지원합니다. 메타데이터는 특화 도메인 "NGW"에 저장됩니다. NextGIS 웹은 문자열 및 숫자형 메타데이터를 지원합니다. 십진수를 가진 메타데이터 키에는 **.d** 접미어가 붙고, 실수를 가진 키에는 **.f** 접미어가 붙습니다. 새로운 메타데이터 항목을 생성하려면, :cpp:func:`SetMetadataItem` 함수와 알맞은 접미어를 사용해서 NGW 도메인에 새로운 키=값 쌍을 추가하십시오. NextGIS 웹으로 전송하는 도중 접미어는 생략될 것입니다. 숫자가 문자열로부터 숫자로 정확하게 변환되는지 확인해야만 합니다.

리소스 설명 및 키는 기본 도메인에 있는 *description* 및 *keyname* 메타데이터 항목에 적절하게 매핑됩니다. 이 메타데이터 항목들을 변경하면 리소스 속성을 업데이트할 것입니다.

리소스 생성 날짜, 유형 및 상위 식별자는 기본 도메인에 있는 읽기 전용 *creation_date*, *resource_type* 및 *parent_id* 메타데이터 항목에 적절하게 매핑됩니다.

벡터 레이어의 필드 속성(별명, 식별자, 라벨 필드, 그리드 가시성)은 다음과 같이 레이어 메타데이터에 매핑됩니다:

-  필드 별명(alias) -> FIELD_{field number}_ALIAS (예: FIELD_0_ALIAS)
-  식별자(identifier) -> FIELD_{field number}_ID (예: FIELD_0_ID)
-  라벨 필드 -> FIELD_{field number}_LABEL_FIELD (예: FIELD_0_LABEL_FIELD)
-  그리드 가시성 -> FIELD_{field number}_GRID_VISIBILITY (예: FIELD_0_GRID_VISIBILITY)

GDAL 3.3버전부터 :cpp:func:`SetAlternativeName` 및 :cpp:func:`GetAlternativeNameRef` 를 통해 필드 별명을 지정할 수/가져올 수 있습니다.

필터
-------

벡터 및 PostGIS 레이어는 :cpp:func:`SetIgnoredFields` 메소드를 지원합니다. 이 메소드를 실행하는 경우 모든 캐시된 객체를 해제할 것입니다.

벡터 및 PostGIS 레이어는 :cpp:func:`OGRLayer::SetAttributeFilter` 및 :cpp:func:`OGRLayer::SetSpatialFilter` 메소드를 지원합니다. 조건이 다음 비교 연산자 가운데 하나인 경우 서버 쪽에서 속성 필터를 평가할 것입니다:

 - 초과 (>)
 - 미만 (<)
 - 이상 (>=)
 - 이하 (<=)
 - 등호 (=)
 - 부등호 (!=)
 - LIKE SQL 문 (문자열 비교 용)
 - ILIKE SQL 문 (문자열 비교 용)

또한 비교 연산자 사이에는 괄호가 없는 AND 연산자만 지원합니다. 다음은 그 예시입니다:

::

   FIELD_1 = 'Value 1'

::

   FIELD_1 = 'Value 1' AND FIELD_2 > Value 2

조건이 이런 비교 연산자 가운데 하나가 아닌 경우 클라이언트 쪽에서 속성 필터를 평가할 것입니다.

NextGIS 웹 네이티브 포맷을 이용해서 속성 필터를 설정할 수 있습니다. 다음은 그 예시입니다:

::

   NGW:fld_FIELD_1=Value 1&fld_FIELD_2__gt=Value 2

WHERE 절 앞에 'NGW:' 접두어를 그리고 필드명 앞에 'fld\_' 접두어를 붙이는 것을 잊지 마십시오.

데이터셋이 :cpp:func:`OGRLayer::ExecuteSQL` 메소드를 지원하지만, 다음 쿼리들만 지원합니다:

-  DELLAYER: layer_name; - layer_name으로 레이어를 삭제합니다.
-  DELETE FROM layer_name; - layer_name 이름인 레이어로부터 모든 객체를 삭제합니다.
-  DROP TABLE layer_name; - layer_name 이름인 레이어를 삭제합니다.
-  ALTER TABLE src_layer RENAME TO dst_layer; - 레이어를 재명명합니다.
-  SELECT field_1,field_2 FROM src_layer WHERE field_1 = 'Value 1' AND field_2 = 'Value 2'; - SELECT 문에 필드 목록 또는 별표('\*')를 지정할 수 있습니다. WHERE 절은 :cpp:func:`OGRLayer::SetAttributeFilter` 메소드의 입력물과 동일한 제한 사항이 적용됩니다.

예시
--------

- 데이터소스 내용 읽어오기('1730'이 리소스 그룹 식별자입니다):

::

       ogrinfo -ro NGW:https://demo.nextgis.com/resource/1730

-  레이어 상세 정보 읽어오기('1730'이 리소스 그룹 식별자, 'Parks'가 벡터 레이어 이름입니다):

::

       ogrinfo -ro -so NGW:https://demo.nextgis.com/resource/1730 Parks

-  식별자가 '1730'인 기존 리소스 그룹에 있는 shapefile로부터 벡터 레이어를 생성하고 채우기. 새 벡터 레이어는 "some new name"으로 명명될 것입니다:

::

       ogr2ogr -f NGW -nln "some new name" -update -doo "BATCH_SIZE=100" -t_srs EPSG:3857 "NGW:https://demo.nextgis.com/resource/1730" myshapefile.shp

.. warning::
   '-update' 키는 필수입니다. 이 키를 지정하지 않는 경우 대상 데이터소스를 그냥 삭제할 것입니다. NextGIS 웹이 지원하는 벡터 레이어의 공간 좌표계는 EPSG:3857뿐이기 때문에 '-t_srs EPSG:3857' 키도 필수입니다.

.. note::
   객체 변환 작업의 속도를 향상시키기 위해 '-doo "BATCH_SIZE=100"' 키를 권장합니다.

-  이름이 "new group"이고 상위 식별자가 '1730'인 새 리소스 그룹에 있는 shapefile로부터 벡터 레이어를 생성하고 채우기. 새 벡터 레이어는 "some new name"으로 명명될 것입니다:

::

       ogr2ogr -f NGW -nln "Название на русском языке" -dsco "BATCH_SIZE=100" -t_srs EPSG:3857 "NGW:https://demo.nextgis.com/resource/1730/new group" myshapefile.shp

참고
--------

-  :ref:`NextGIS 래스터 <raster.ngw>` 드라이버
-  `NextGIS 웹 문서 <http://docs.nextgis.com/docs_ngweb/source/toc.html>`_
-  `개발자를 위한 NextGIS 웹 <http://docs.nextgis.com/docs_ngweb_dev/doc/toc.html>`_
