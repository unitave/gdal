.. _vector.hana:

SAP HANA
====================

.. shortname:: HANA

.. build_dependencies:: odbc-cpp-wrapper

이 드라이버는 `SAP HANA <https://www.sap.com/products/hana.html>`_ 데이터베이스에 저장된 공간 데이터에 대한 읽기 및 쓰기 접근 지원을 구현했습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터베이스 접속하기
------------------------

SAP HANA 데이터베이스에 접속하려면, 데이터베이스 이름을 필요한 파라미터들과 함께 지정한 연결 문자열을 사용하십시오. "HANA:" 접두어를 사용해서 이름을 HANA 연결 문자열로 표시할 수 있습니다.

::

   HANA:"DRIVER={HDBODBC};DATABASE=HAN;HOST=localhost;PORT=30015;USER=mylogin;PASSWORD=mypassword;SCHEMA=MYSCHEMA"

이 문법에서 각 파라미터 설정은 키워드=값 형식으로 되어 있습니다. 등호 기호 양쪽에 공백을 넣을 수도 있습니다. 비어 있는 값 또는 공백을 담고 있는 값을 작성하려면, keyword='a value'처럼 값을 작은따옴표로 감싸십시오. 값에 있는 작은따옴표 및 백슬래시는 \\' 및 \\\ 처럼 백슬래시로 이스케이프 처리해야만 합니다.


SQL 선언문
--------------

OGRDataSource에 ExecuteSQL() 호출을 사용하거나 또는 ogr2ogr에 -sql 명령어 옵션을 사용하는 경우 HANA 드라이버는 기본적으로 SQL 문을 내부에서 평가하기보다 HANA에 직접 SQL 문을 전송합니다. 속성 쿼리 표현식도 HANA로 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언의 이름으로 전송하면 OGR HANA 드라이버가 :ref:`OGR SQL <ogr_sql_dialect>` 엔진을 이용해서 SQL 문을 처리하도록 요청할 수도 있습니다.

OGR HANA 드라이버는 일반적인 SQL 맥락에서 OGRDataSource::StartTransaction(), OGRDataSource::CommitTransaction() 및 OGRDataSource::RollbackTransaction() 호출을 지원합니다.

생성 문제점
---------------

HANA 드라이버는 새 스키마의 생성을 지원하지 않지만, 기존 스키마 안에 새 레이어(테이블)의 생성은 지원합니다.

데이터셋 열기 옵션
~~~~~~~~~~~~~~~~~~~~

-  **DSN=string**:
   데이터소스의 이름을 설정합니다.

-  **DRIVER=string**:
   드라이버를 가리키는 이름 또는 경로를 설정합니다. 예를 들어 (윈도우의 경우) DRIVER={HDBODBC} 또는 (리눅스/맥OS의 경우) DRIVER=/usr/sap/hdbclient/libodbcHDB.so 처럼 설정할 수 있습니다.

-  **HOST=string**:
   서버 호스트명을 설정합니다.

-  **PORT=integer**:
   포트 번호를 설정합니다.

-  **USER=string**:
   사용자명을 설정합니다.

-  **PASSWORD=string**:
   사용자 비밀번호를 설정합니다.

-  **DATABASE=string**:
   데이터베이스의 이름을 설정합니다.

-  **SCHEMA=string**:
   TABLES 옵션에 목록화된 테이블에 사용되는 스키마를 설정합니다.

-  **TABLES=string**:
   목록화할 테이블들의 제한된 집합을 (쉼표로 구분해서) 설정합니다.

-  **ENCRYPT=boolean**:
   TLS/SSL 암호화를 활성화하거나 비활성화합니다. 기본값은 NO입니다.

-  **SSL_CRYPTO_PROVIDER=string**:
   SSL 통신을 위해 사용되는 암호 라이브러리 제공자를 설정합니다. (commoncrypto | sapcrypto | openssl)

-  **SSL_KEY_STORE=string**:
   서버의 비밀 키(private key)를 담고 있는 키 저장 파일(key store file)을 가리키는 경로를 설정합니다.

-  **SSL_TRUST_STORE=string**:
   서버의 공개 인증 정보(들)을 담고 있는 신뢰 저장 파일(trust store file)을 가리키는 경로를 설정합니다. (OpenSSL 전용)

-  **SSL_VALIDATE_CERTIFICATE=string**:
   이 옵션을 참으로 설정하면, 서버의 인증 정보를 검증합니다. 기본값은 YES입니다.

-  **SSL_HOST_NAME_IN_CERTIFICATE=string**:
   서버의 식별 정보 검증에 사용되는 호스트명을 설정합니다.

-  **CONNECTION_TIMEOUT=integer**:
   밀리초 단위 연결 시간 제한을 설정합니다. 기본값은 0(비활성화)입니다.

-  **PACKET_SIZE=integer**:
   클라이언트로부터 서버로 전송되는 요청 패킷의 바이트 단위 최대 용량을 설정합니다. 최소값은 1MB입니다. 기본값은 1MB입니다.

-  **SPLIT_BATCH_COMMANDS=boolean**:
   파티션을 나눈 테이블에 대한 배치(batch) 명령어들의 분할 및 병렬 실행을 허용할지 여부를 선택합니다. 기본값은 YES입니다.

-  **DETECT_GEOMETRY_TYPE=boolean**:
   도형 열의 유형을 탐지할지 여부를 선택합니다. 대용량 테이블의 경우 상당한 시간이 걸릴 수도 있다는 사실을 기억하십시오. 기본값은 YES입니다.

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

없습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **OVERWRITE**:
   요청한 레이어를 생성하기 전에 요청한 이름과 같은 이름을 가진 기존 레이어를 강제로 삭제하려면 이 옵션을 YES로 설정할 수도 있습니다. 기본값은 NO입니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 HANA와 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. NO로 설정하면 이름을 그대로 보전합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

-  **PRECISION**:
   해당 레이어에 생성되는 새 필드가 DECIMAL(width,precision) 또는 CHAR(width) 유형을 사용할 수 있는 경우 이를 사용해서 필드 길이 및 정밀도를 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다.
   NO로 설정하면 그 대신 REAL, INTEGER 및 VARCHAR 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **DEFAULT_STRING_SIZE**:
   문자열 열의 기본 크기를 설정합니다. 기본값은 256입니다.

-  **GEOMETRY_NAME**:
   새 테이블에 있는 도형 열의 이름을 설정합니다. 이 옵션을 생략하는 경우 기본값은 *GEOMETRY* 입니다.

-  **GEOMETRY_NULLABLE**:
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 기본값은 YES입니다.

-  **SRID**:
   레이어의 SRID를 설정합니다.

-  **FID**:
   생성할 FID 열의 이름을 설정합니다. 기본값은 'OGR_FID'입니다.

-  **FID64**:
   64비트 길이의 ID를 처리하기 위해 BIGINT 유형의 FID 열을 생성할지 여부를 선택합니다. 기본값은 NO입니다.

-  **COLUMN_TYPES**:
   열 유형을 정의하는 field_name=hana_field_type 서식으로 된 문자열들을 쉼표로 구분한 목록을 설정합니다.

-  **BATCH_SIZE**:
   배치(batch) 작업 당 작성할 바이트 개수를 설정합니다. 기본값은 4194304(4MB)입니다.

다중 테넌트 데이터베이스 컨테이너
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

테넌트(tenant) 데이터베이스에 접속하려면, 정확히 원하는 인스턴스에 할당된 포트 번호를 지정해야 합니다. 테넌트 데이터베이스로부터 다음 쿼리를 실행하면 이 포트 번호를 판단할 수 있습니다.

   ::

      SELECT SQL_PORT FROM SYS.M_SERVICES WHERE ((SERVICE_NAME='indexserver' and COORDINATOR_TYPE= 'MASTER') or (SERVICE_NAME='xsengine'))

더 자세한 정보는 `SAP HANA 다중 테넌트(Multitenant) 데이터베이스 컨테이너 <https://help.sap.com/doc/0987e3b51fb74e5a8631385fe4599c97/2.0.00/en-us/sap_hana_multitenant_database_containers_en.pdf>`_ 문서의 **2.9 다중 테넌트 데이터베이스 컨테이너에 접속** 단락을 읽어보십시오.


예시
--------

-  다음 예시는 :ref:`ogrinfo` 명령어를 이용해서 지정한 호스트 상에 있는 HANA 레이어들을 목록화하는 방법을 보여줍니다:

   ::

      ogrinfo -ro HANA:"DRIVER={HDBODBC};DATABASE=HAN;HOST=localhost;PORT=30015;USER=mylogin;PASSWORD=mypassword;SCHEMA=MYSCHEMA"

   또는

   ::

      ogrinfo -ro HANA:"DSN=MYHANADB;USER=mylogin;PASSWORD=mypassword;SCHEMA=MYSCHEMA"

-  다음 예시는 :ref:`ogrinfo` 명령어를 이용해서 지정한 레이어, 예를 들어 'planet_osm_line' 레이어에 관한 요약 정보를 출력하는 방법을 보여줍니다:

   ::

      ogrinfo -ro HANA:"DRIVER={HDBODBC};DATABASE=HAN;HOST=localhost;PORT=30015;USER=mylogin;PASSWORD=mypassword;SCHEMA=MYSCHEMA" -so "planet_osm_line"

      Layer name: planet_osm_line
      Geometry: Line String
      Feature Count: 81013
      Extent: (732496.086304, 6950959.464783) - (1018694.144531, 7204272.976379)
      Layer SRS WKT:
      PROJCS["WGS 84 / Pseudo-Mercator",
          GEOGCS["WGS 84",
              DATUM["WGS_1984",
                  SPHEROID["WGS 84",6378137,298.257223563, AHORITY["EPSG","7030"]],
                  AUTHORITY["EPSG","6326"]],
                  PRIMEM["Greenwich",0, AUTHORITY["EPSG","8901"]],
                  UNIT["degree",0.0174532925199433, AUTHORITY["EPSG","9122"]],
                  AUTHORITY["EPSG","4326"]],
              PROJECTION["Mercator_1SP"],
              PARAMETER["central_meridian",0],
              PARAMETER["scale_factor",1],
              PARAMETER["false_easting",0],
              PARAMETER["false_northing",0],
              UNIT["metre",1,AUTHORITY["EPSG","9001"]],
              AXIS["X",EAST],
              AXIS["Y",NORTH],
              AUTHORITY["EPSG","3857"]]
      Geometry Column = way
      osm_id: Integer64 (0.0)
      access: String (4000.0)
      addr:housename: String (4000.0)
      addr:housenumber: String (4000.0)
      addr:interpolation: String (4000.0)
      admin_level: String (4000.0)
      aerialway: String (4000.0)
      aeroway: String (4000.0)

-  다음 예시는 'points' 테이블로부터 'points_output.shp'라는 shapefile로 데이터를 내보내는 방법을 보여줍니다:

   ::

      ogr2ogr -f "ESRI Shapefile" "D:\\points_output.shp" HANA:"DRIVER={HDBODBC};DATABASE=HAN;HOST=localhost;PORT=30015;USER=mylogin;PASSWORD=mypassword;SCHEMA=GIS;TABLES=points"

-  다음 예시는 shapefile로부터 가져온 데이터로 테이블을 생성하고 채우는 방법을 보여줍니다:

   ::

      ogr2ogr -f HANA HANA:"DRIVER={HDBODBC};DATABASE=HAN;HOST=localhost;PORT=30015;USER=mylogin;PASSWORD=mypassword;SCHEMA=MYSCHEMA" myshapefile.shp


개발자에게
--------------

SAP HANA 드라이버를 컴파일하려면, `odbc-cpp-wrapper <https://github.com/SAP/odbc-cpp-wrapper/>`_ 라이브러리를 링크하거나 설치해야 합니다.
더 자세한 내용을 원한다면, 각각 윈도우 또는 리눅스/맥OS 용 드라이버를 빌드하기 위한 nmake.opt 또는 configure.ac 파일에 있는 주석을 참조하십시오.

참고
--------

-  `SAP HANA 홈페이지 <https://www.sap.com/products/hana.html>`_
-  `SAP HANA 공간 참조 <https://help.sap.com/viewer/cbbbfc20871e4559abfd45a78ad58c02/2.0.03/en-US/e1c934157bd14021a3b43b5822b2cbe9.html>`_
-  `SAP HANA ODBC 연결 속성 <https://help.sap.com/viewer/0eec0d68141541d1b07893a39944924e/2.0.02/en-US/7cab593774474f2f8db335710b2f5c50.html>`_

