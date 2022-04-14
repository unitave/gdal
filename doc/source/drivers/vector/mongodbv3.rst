.. _vector.mongodbv3:

MongoDBv3
=========

.. versionadded:: 3.0

.. shortname:: MongoDBv3

.. build_dependencies:: MongoDB C++ 3.4.0 이상 버전 클라이언트 라이브러리

MongoDBv3 드라이버는 MongoDB 서비스에 접속할 수 있습니다.

이 드라이버는 문서/객체 및 집합/레이어의 읽기, 생성, 업데이트 및 삭제 작업을 지원합니다. OGR 작업 전에 MongoDB 데이터베이스가 이미 존재해야만 합니다.

이 드라이버는 Mongo C++ 3.4.0 이상 버전 클라이언트 라이브러리를 필요로 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

MongoDB 대 OGR 개념
-----------------------

데이터베이스 안에 있는 MongoDB 집합(collection)을 OGR 레이어로 간주합니다. MongoDB 문서는 OGR 객체로 간주합니다.

데이터셋 이름 문법
-------------------

데이터셋을 열 수 있는 주요 문법이 2개 있습니다:

-  *MONGODBV3:* 접두어가 붙은 `MongoDB URI <https://docs.mongodb.com/manual/reference/connection-string/index.html>`_ 를 사용하는 방법입니다.

   ::

      MONGODBV3:mongodb://[usr:pwd@]host1[:port1]...[,hostN[:portN]]][/[db][?options]]

-  *MongoDBv3:* 만 이름으로 사용하고 호스트명, 포트 번호, 사용자명, 비밀번호, 데이터베이스 등등은 열기 옵션으로 지정하는 방법입니다.

주의: 레거시 :ref:`MongoDB <vector.mongodb>` 드라이버 대신 이 드라이버가 데이터셋을 인식하기 위해서는 *mongodb://* 로 시작하는 URI 앞에 *MONGODBV3:* 접두어를 붙여야 합니다. URI가 *mongodb+srv://* 로 시작하는 경우 접두어가 필요없습니다.

다음 열기 옵션들을 사용할 수 있습니다:

-  **URI=uri**:
   `연결 URI <https://docs.mongodb.com/manual/reference/connection-string/index.html>`_

-  **HOST=hostname**:
   서버 호스트명을 지정합니다. 기본값은 'localhost'입니다.

-  **PORT=port**:
   서버 포트 번호를 지정합니다. 기본값은 27017입니다.

-  **DBNAME=dbname**:
   데이터베이스 이름을 지정합니다. 호스트 접속 시 사용자 인증 정보와 함께 지정해야 합니다.

-  **USER=name**:
   사용자명을 지정합니다.

-  **PASSWORD=password**:
   사용자 비밀번호를 지정합니다.

-  **SSL_PEM_KEY_FILE=filename**:
   SSL PEM 인증서/키 파일명을 지정합니다.

-  **SSL_PEM_KEY_PASSWORD=password**:
   SSL PEM 키 비밀번호를 지정합니다.

-  **SSL_CA_FILE=filename**:
   SSL 인증서 기관(Certification Authority) 파일명을 지정합니다.

-  **SSL_CRL_FILE=filename**:
   SSL 인증서 폐기 목록(Certification Revocation List) 파일명을 지정합니다.

-  **SSL_ALLOW_INVALID_CERTIFICATES=YES/NO**:
   무결하지 않은 인증서로 서버 접속을 허용할지 여부를 선택합니다. 기본값은 NO입니다.

-  **BATCH_SIZE=number**:
   배치(batch) 당 가져올 객체 개수를 지정합니다.
   대부분의 쿼리에서, 첫 번째 배치가 문서 101개 또는 1MB를 초과하기에 딱 적당한 개수의 문서를 반환합니다. 이어지는 배치 용량은 4MB입니다.

-  **FEATURE_COUNT_TO_ESTABLISH_FEATURE_DEFN=number**:
   객체 정의를 확립하기 위해 가져와야 할 객체의 개수를 지정합니다. -1로 설정하면 무제한이라는 의미입니다. 기본값은 100입니다.

-  **JSON_FIELD=YES/NO**:
   전체 문서를 JSON으로 가지고 있는 "_json" 필드를 포함할지 여부를 선택합니다. 기본값은 NO입니다.

-  **FLATTEN_NESTED_ATTRIBUTE=YES/NO**:
   내포 객체들을 재귀적으로 탐색해서 평탄화된 OGR 속성을 생성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **FID=name**:
   FID로 사용할 정수형 값들을 가진 필드의 이름을 지정합니다. 기본값은 'ogc_fid'입니다.

-  **USE_OGR_METADATA=YES/NO**:
   레이어 메타데이터를 읽어오기 위해 \_ogr_metadata 집합을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

-  **BULK_INSERT=YES/NO**:
   객체 생성을 위해 벌크(bulk) 삽입을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

필터링
---------

이 드라이버는 도형 필드에서 서버에 "2d" 또는 "2dsphere" 공간 색인을 사용할 수 있을 경우 SetSpatialFilter()로 설정된 모든 공간 필터를 포워딩할 것입니다.

하지만 현재로서는 SetAttributeFilter()로 설정된 SQL 속성 필터를 클라이언트 쪽에서만 평가합니다. 서버 쪽 필터링을 활성화하려면 SetAttributeFilter()에 전송되는 문자열이 `MongoDB 필터 문법 <https://docs.mongodb.com/manual/reference/method/db.collection.find/index.html>`_ 으로 된 JSon 객체여야만 합니다.

페이지 작업
------

서버로부터 객체를 문서 101개 또는 1MB를 초과하기에 딱 적당한 개수의 문서 덩어리로 가져옵니다. 이어지는 배치 용량은 4MB입니다. BATCH_SIZE 열기 옵션을 이용해서 이 습성을 변경할 수 있습니다.

스키마
------

MongoDB 집합을 읽어올 때, OGR가 속성 및 도형 필드의 스키마를 확립해야만 합니다. OGR는 스키마를 사용하지 않는 MongoDB 집합과는 반대로 고정 스키마 개념을 가지기 때문입니다.

일반적인 경우, OGR는 집합의 처음 문서 100개를 (FEATURE_COUNT_TO_ESTABLISH_FEATURE_DEFN 열기 옵션으로 이 개수를 변경할 수 있습니다.) 읽어와서 가져온 필드와 값에 가장 적합한 스키마를 작성할 것입니다.

이전에 OGR로 생성한 집합/레이어의 경우, \_ogr_metadata 특수 집합이 OGR 스키마를 담고 있습니다. 이 경우 해당 OGR 스키마를 직접 사용할 것입니다. USE_OGR_METADATA 열기 옵션을 NO로 설정해서 \_ogr_metadata에 작성된 스키마를 무시할 수도 있습니다.

JSON_FIELD 열기 옵션을 YES로 설정하면 OGR 스키마에 \_json 특수 필드도 추가할 수 있습니다. MongoDB 문서를 OGR 객체로 읽어올 때, \_json 필드에 문서 전체의 JSon 버전을 저장할 것입니다. 복잡 문서 또는 OGR 데이터 유형으로 잘 변환되지 않는 데이터 유형의 경우 유용할 수도 있습니다. 문서 생성/업데이트 작업 시, \_json 필드가 존재하고 설정되어 있는 경우 그 내용을 직접 사용할 것입니다. (다른 필드들은 무시할 것입니다.)

객체 ID (FID)
----------

MongoDB는 문서의 유일 ID를 담고 있는 \_id 특수 필드를 가지고 있습니다. 이 필드는 OGR 필드로 반환되지만, 반드시 정수형이어야만 하는 OGR FeatureID 특수 필드로 사용할 수는 없습니다. OGR는 기본적으로 OGR FeatureID를 설정하기 위해, 존재할 수도 있는 'ogc_fid' 필드를 읽어오려 시도할 것입니다. FID 열기 옵션으로 검색할 필드의 이름을 설정할 수 있습니다. 이 필드를 발견하지 못 하는 경우, OGR가 FID를 1에서 시작하는 일련 번호로 반환하지만 안정적일 것이라고 보장할 수는 없습니다.

ExecuteSQL() 인터페이스
----------------------

"MongoDB"를 ExecuteSQL()의 방언으로 지정하면, 직렬화된 `MongoDB 명령어 <https://docs.mongodb.com/manual/reference/command/index.html>`_ 를 가진 JSon 문자열을 전송할 수 있습니다. 결과물은 단일 OGR 객체에 있는 JSon 문자열로 반환될 것입니다.

표준 SQL 요청은 클라이언트 쪽에서 실행될 것입니다.

쓰기 지원
-------------

레이어/집합을 생성하고 삭제할 수 있습니다.

데이터소스를 업데이트 모드로 연 경우에만 쓰기 지원이 활성화됩니다.

:cpp:func:`OGRFeature::CreateFeature` 함수로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR이 반환된 \_id를 가져와서 :cpp:func:`OGRFeature::SetFeature` 작업을 위해 사용할 것입니다.

레이어 생성 옵션
----------------------

다음과 같은 레이어 생성 옵션들을 지원합니다:

-  **OVERWRITE=YES/NO**:
   기존 집합을 생성할 레이어 이름으로 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다.

-  **GEOMETRY_NAME=name**:
   도형 열의 이름입니다. 기본값은 'geometry'입니다.

-  **SPATIAL_INDEX=YES/NO**:
   공간 색인(2dsphere)을 생성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **FID=string**:
   FID로 사용할 정수값을 가진 필드의 이름입니다. 기본값은 'ogc_fid'입니다.

-  **WRITE_OGR_METADATA=YES/NO**:
   \_ogr_metadata 집합에 레이어 필드의 설명을 생성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **DOT_AS_NESTED_FIELD=YES/NO**:
   필드 이름에 있는 점('.') 문자를 하위 문서(sub-document)로 간주할지 여부를 선택합니다. 기본값은 YES입니다.

-  **IGNORE_SOURCE_ID=YES/NO**:
   CreateFeature() 함수로 전송되는 객체의 \_id 필드를 무시할지 여부를 선택합니다. 기본값은 NO입니다.

예시
--------

-  MongoDB 데이터베이스의 테이블을 목록화하기:

::

   ogrinfo -ro mongodb+srv://user:password@cluster0-ox9uy.mongodb.net/test

-  MongoDB 필드에 대한 필터링:

::

   ogrinfo -ro mongodb+srv://user:password@cluster0-ox9uy.mongodb.net/test -where '{ "field": 5 }'

shapefile로부터 집합을 생성하고 채우기:

::

   ogr2ogr -update mongodb+srv://user:password@cluster0-ox9uy.mongodb.net/test shapefile.shp

빌드 지침
------------------

MongoDBv3 드라이버를 컴파일 하려면 GDAL/OGR를 `MongoDB 3.4.0 이상 버전 C++ 드라이버 클라이언트 라이브러리 <https://github.com/mongodb/mongo-cxx-driver>`_ 를 대상으로 빌드해야만 합니다.

먼저 `MongoDB C++ 드라이버 클라이언트 빌드 지침 <http://mongocxx.org/mongocxx-v3/installation/>`_ 을 따르십시오.

그 다음:

-  리눅스/유닉스의 경우, ``./configure --with-mongocxxv3`` 를 실행하십시오.
   (PKG_CONFIG_PATH가 ``{INSTALLATION_PREFIX_OF_MONGOCXX}/lib/pkgconfig`` 을 가리키도록 대체해야 할 수도 있습니다.)

-  윈도우의 경우, nmake.opt 파일에서 다음 내용의 주석 처리를 해제하고 수정하십시오. (또는 nmake.local 파일에 추가하십시오.):

   ::

      # Uncomment for MongoDBv3 support
      # Uncomment following line if plugin is preferred
      #MONGODBV3_PLUGIN = YES
      BOOST_INC=E:/boost_1_69_0
      MONGOCXXV3_CFLAGS = -IE:/dev/install-mongocxx-3.4.0/include/mongocxx/v_noabi -IE:/dev/install-mongocxx-3.4.0/include/bsoncxx/v_noabi
      MONGOCXXV3_LIBS = E:/dev/install-mongocxx-3.4.0/lib/mongocxx.lib E:/dev/install-mongocxx-3.4.0/lib/bsoncxx.lib

참고
--------

-  `MongoDB C++ 드라이버 <https://github.com/mongodb/mongo-cxx-driver>`_

-  `MongoDB 지침서 <https://docs.mongodb.com/manual/>`_

