.. _vector.cloudant:

Cloudant -- Cloudant
====================

.. shortname:: Cloudant

.. build_dependencies:: libcurl

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_CLOUDANT

Cloudant 드라이버와 CouchDB 드라이버의 API는 호환되며 동일한 핵심 기술을 기반으로 합니다. Cloudant의 지리공간 확장 사양은 GeoCouch와 별개입니다. 이 드라이버는 Cloudant 공간 확장 사양을 잠재적으로 활성화한 상태로 Cloudant 서비스에 접속할 수 있습니다.

Cloudant 드라이버를 컴파일하려면 GDAL/OGR를 cURL 지원과 함께 빌드해야만 합니다.

이 드라이버는 읽기 및 쓰기 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

Cloudant 대 OGR 개념
------------------------

Cloudant 데이터베이스는 OGR 레이어로 간주됩니다. Cloudant 문서는 OGR 객체로 간주됩니다.

OGR은 가급적 GeoJSON 사양에 따라 Cloudant 문서를 처리합니다.

데이터셋 이름 문법
-------------------

Cloudant 데이터소스를 열기 위한 다음과 같습니다:

::

   cloudant:http://example.com[/layername]

이때 http://example.com 는 CouchDB 저장소의 루트를 가리키며, 선택 파라미터인 layername은 CouchDB 데이터베이스의 이름입니다.

뷰를 직접 열 수도 있습니다:

::

   cloudant:http://example.com/layername/_design/adesigndoc/_view/aview[?include_docs=true]

map() 함수에서 emit() 함수를 호출해서 반환된 값에 따라 include_docs=true 파라미터가 필요할 수도 있습니다.

인증
--------------

몇몇 작업에 -- 특히 쓰기 작업에는 인증된 접근이 필수입니다. URL에서 ``CLOUDANT_USERPWD`` 환경 변수를 사용자명:비밀번호로 설정하면 인증 정보를 전송할 수 있습니다.

필터링
---------

이 드라이버는 Cloudant 확장 사양을 사용할 수 있을 경우 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다.

이 드라이버는 기본적으로 "_design/SpatialView/_geo/spatial" 공간 필터 함수를 시도할 것입니다. 이 함수는 OGR가 생성한 레이어에 대해 무결한 공간 필터 함수입니다. 이 필터 함수가 존재하지 않지만 다른 함수는 존재하는 경우, CLOUDANT_SPATIAL_FILTER 환경설정 옵션으로 지정할 수 있습니다.

페이지 작업(paging)
------------------

기본적으로 서버로부터 객체들을 200개 덩어리로 가져옵니다.
Cloudant는 북마크를 이용해서 데이터를 훑어봅니다.

쓰기 지원
-------------

테이블을 생성하고 삭제할 수 있습니다.

데이터소스를 업데이트 모드로 연 경우에만 쓰기 지원이 활성화됩니다.

:cpp:func:`OGRFeature::CreateFeature` 함수로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR이 반환된 \_id 및 \_rev를 가져와서 OGR FID로 사용할 것입니다.

쓰기 지원과 OGR 트랜잭션
----------------------------------

CreateFeature()/SetFeature() 작업들은 기본적으로 OGR API 호출과 동시에 서버에 전송됩니다. 하지만 수많은 클라이언트/서버 교환 때문에 수많은 명령어들이 전송되는 경우, 이 때문에 성능이 저하될 수도 있습니다.

:cpp:func:`OGRLayer::StartTransaction()` 과 :cpp:func:`OGRLayer::CommitTransaction()` 사이에 CreateFeature()/SetFeature() 작업을 넣을 수 있습니다. 메모리에 작업을 저장한 다음 :cpp:func:`OGRLayer::CommitTransaction()` 을 호출할 때만 실행할 것입니다.

레이어 생성 옵션
----------------------

다음 레이어 생성 옵션들을 지원합니다:

-  **UPDATE_PERMISSIONS=LOGGED_USER|ALL|ADMIN|function(...)|DEFAULT**:
   새 레이어에 대한 권한을 업데이트합니다.

   -  LOGGED_USER(기본값)로 설정하는 경우, 로그인한 사용자만 레이어에 변경 사항을 적용할 수 있습니다.
   -  ALL로 설정하는 경우, 모든 사용자가 레이어에 변경 사항을 적용할 수 있습니다.
   -  ADMIN으로 설정하는 경우, 관리자만 레이어에 변경 사항을 적용할 수 있습니다.
   -  "function("으로 시작하는 경우, 생성 옵션의 값을 `validate_doc_update 함수 <http://guide.couchdb.org/draft/validation.html>`_ 의 내용으로 사용할 것입니다.
   -  다른 값으로 설정하면, 모든 사용자가 비설계(non-design) 문서에 변경 사항을 적용할 수 있습니다.

-  **GEOJSON=YES|NO**:
   이 옵션을 NO로 설정하면 문서를 GeoJSON 문서로 작성하는 일을 막을 수 있습니다. 기본값은 YES입니다.

-  **COORDINATE_PRECISION=int_number**:
   좌표값의 소수점 뒤에 작성할 최대 자릿수를 설정합니다. 기본값은 15입니다. 후행 0들을 제거하기 위해 "스마트" 절단(truncation)을 수행할 것입니다.
   주의: 데이터셋을 업데이트 모드로 열 때, OGR_CLOUDANT_COORDINATE_PRECISION 환경설정 옵션을 설정해서 비슷한 역할을 하게 할 수 있습니다.

예시
--------

Cloudant 저장소의 테이블들을 목록화하기:

::

   ogrinfo -ro "cloudant:http://some_account.some_cloudant_server.com"

shapefile로부터 테이블을 생성하고 채우기:

::

   ogr2ogr -f cloudant "cloudant:http://some_account.some_cloudant_server.com" shapefile.shp

참고
--------

-  `CouchDB 참조 <http://wiki.apache.org/couchdb/Reference>`_

-  `Cloudant Geospatial <https://cloudant.com/product/cloudant-features/geospatial/>`_

-  `'validate_doc_update' 함수 문서 <http://guide.couchdb.org/draft/validation.html>`_

