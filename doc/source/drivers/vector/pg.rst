.. _vector.pg:

PostgreSQL / PostGIS
====================

.. shortname:: PostgreSQL

.. build_dependencies:: PostgreSQL 클라이언트 라이브러리 (libpq)

이 드라이버는 `PostGIS <http://postgis.net/>`_ 공간 데이터 지원으로 확장된 PostgreSQL에 있는 공간 테이블로의 접근 지원을 구현합니다. 이 드라이버는 PostGIS 없이 PostgreSQL만 사용하는 기능도 일부 지원하지만 활용성은 떨어집니다.

이 드라이버는 PostgreSQL 데이터베이스에 연결되어야 합니다. 나중에 PostgreSQL 데이터베이스로 인젝션할 SQL 덤프를 준비하려는 경우 :ref:`PostgreSQL SQL 덤프 드라이버 <vector.pgdump>` 를 대신 사용하면 됩니다.


:ref:`고급 OGR PostgreSQL 드라이버 정보 <vector.pg_advanced>` 페이지에서 이 드라이버에 관한 추가 정보를 찾아볼 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터베이스에 접속하기
------------------------

PostgreSQL 데이터소스에 연결하려면, 데이터베이스 이름을 지정하는 연결 문자열을 필요한 추가 파라미터와 함께 사용하십시오. 연결 문자열 앞에 PostgreSQL 연결 문자열임을 표시하는 'PG:' 접두어를 붙여야 합니다.

   ::

      PG:dbname=databasename

   *또는*

   ::

      PG:"dbname='databasename' host='addr' port='5432' user='x' password='y'"

   이 문법에서 각 파라미터 설정은 키워드=값 형식으로 되어 있습니다. 등호 기호 양쪽에 공백을 넣을 수도 있습니다. 비어 있는 값 또는 공백을 담고 있는 값을 작성하려면, keyword='a value'처럼 값을 작은따옴표로 감싸십시오. 값에 있는 작은따옴표 및 백슬래시는 \\' 및 \\\ 처럼 백슬래시로 이스케이프 처리해야만 합니다.


   GDAL 3.1버전부터 다음 문법도 지원합니다:

   ::

      PG:service=servicename


   GDAL 3.4부터, URI 문법도 지원합니다:

   ::

      postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]

데이터베이스 이름을 생략하고 사용자명이 이름인 *기본* 데이터베이스에 접속할 수도 있습니다.

**주의**: 연결을 생성하기 위해 PQconnectdb() 메소드를 사용합니다. `PostgreSQL libpq 문서 <https://www.postgresql.org/docs/12/libpq-connect.html>`_ 에서 자세한 내용을 읽어보십시오.

도형 열
----------------

*geometry_columns* 테이블이 존재하는 경우 (예를 들어 접근한 데이터베이스에 PostGIS가 활성화된 경우) *geometry_columns* 테이블에 목록화된 테이블 및 명명된 뷰를 모두 OGR 레이어로 취급할 것입니다. 그렇지 않으면 (접근한 데이터베이스에 PostGIS가 활성화되지 않은 경우) 모든 정규 사용자 테이블 및 명명된 뷰를 레이어로 취급할 것입니다.

이 드라이버는 PostGIS 1.5버전에서 도입된 `geography <http://postgis.net/docs/manual-1.5/ch04.html#PostGIS_Geography>`_ 열 유형도 지원합니다.

이 드라이버는 다음 비선형 도형 유형들도 읽고 쓸 수 있습니다:

   -  CIRCULARSTRING
   -  COMPOUNDCURVE
   -  CURVEPOLYGON
   -  MULTICURVE
   -  MULTISURFACE

SQL 선언문
--------------

PostgreSQL 드라이버는 OGRDataSource 상에 ExecuteSQL() 함수를 호출하거나 ogr2ogr 유틸리티에 '-sql' 명령어 옵션을 사용하는 경우, 내부적으로 SQL 문을 평가하기보다는 기본적으로 PostgreSQL에 SQL 문을 직접 전송합니다. 속성 쿼리 표현식도 PostgreSQL에 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 OGR PostgreSQL 드라이버가 SQL 문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

PostgreSQL 드라이버가 ExecuteSQL() 요청 집합의 결과물을 탐색할 때 PostgreSQL 커서를 사용하고, 작성 작업 시 결과물 집합이 결과물 페이지 1장에 충분히 들어갈 만큼 작은 경우 PostgreSQL 기본 설정을 최적화하지 않는다는 사실을 기억하십시오. 성능 저하를 경험했다면, ``PRELUDE_STATEMENTS=SET cursor_tuple_fraction = 1.0;`` 열기 옵션을 이렇게 지정하면 도움이 될 수도 있습니다.

OGR에서 PostgreSQL 드라이버는 일반적인 SQL 맥락에서 OGRDataSource::StartTransaction(), OGRDataSource::CommitTransaction() 및 OGRDataSource::RollbackTransaction() 호출을 지원합니다.

생성 문제점
---------------

이 드라이버는 새 데이터셋(PostgreSQL 안에 있는 데이터베이스) 생성을 지원하지 않지만, 기존 데이터베이스 안에 새 레이어를 생성할 수는 있습니다.

앞에서 언급한 대로 유형 시스템이 부족하기 때문에, 많은 OGR 유형이 제대로 PostgreSQL로 매핑되지 않을 것입니다.

데이터베이스가 PostGIS 유형들을 (예를 들어 도형 유형을) 불러온 경우, 새로 생성되는 레이어를 PostGIS 도형 유형으로 생성할 것입니다. 그렇지 않다면 OID를 사용할 것입니다.

기본적으로 PostgreSQL로 전송되는 텍스트가 UTF-8로 인코딩되어 있다고 가정합니다. 평문 아스키인 경우 괜찮지만, 확장 문자 집합(ASCII 155+, LATIN1 등등)인 경우 오류가 발생할 수 있습니다. OGR는 이 문제를 직접 제어하지 못 하지만, 사용자가 PGCLIENTENCODING 환경 변수를 설정해서 전송되는 텍스트의 인코딩 포맷을 알려줄 수 있습니다. 예를 들면 사용자의 텍스트가 LATIN1 인코딩인 경우 OGR를 사용하기 전에 환경 변수를 LATIN1으로 설정해주면 입력물의 인코딩을 UTF-8이 아니라 LATIN1이라고 가정할 것입니다. 클라이언트 인코딩을 설정하는 또다른 방법은 ExecuteSQL() 메소드에 ``SET client_encoding TO encoding_name`` SQL 명령어를 설정하는 것입니다. 이때 encoding_name이 ASCII 155+, LATIN1 등등입니다. 이 명령어를 CPLPushErrorHandler() / CPLPopErrorHandler() 쌍 사이에 넣으면 오류를 잡아낼 수 있습니다.

데이터셋 열기 옵션
~~~~~~~~~~~~~~~~~~~~

-  **DBNAME=string**:
   데이터베이스 이름을 지정합니다.

-  **PORT=integer**:
   포트 번호를 지정합니다.

-  **USER=string**:
   사용자명을 지정합니다.

-  **PASSWORD=string**:
   비밀번호를 지정합니다.

-  **HOST=string**:
   서버 호스트명을 지정합니다.

-  **SERVICE=string**: (GDAL 3.1 이상 버전)
   서비스명을 지정합니다.

-  **ACTIVE_SCHEMA=string**:
   작동 중인 스키마를 지정합니다.

-  **SCHEMAS=string**:
   탐색할 스키마의 (쉼표로 구분된) 제한된 집합을 지정합니다.

-  **TABLES=string**:
   목록화할 테이블의 (쉼표로 구분된) 제한된 집합을 지정합니다.

-  **LIST_ALL_TABLES=YES/NO**:
   비공간 테이블을 포함하는 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다.

-  **PRELUDE_STATEMENTS=string**: (GDAL 2.1 이상 버전)
   다른 어떤 SQL 선언문보다도 먼저 PostgreSQL 클라이언트 연결에 전송할 SQL 선언문(들)을 지정합니다. 선언문이 여러 개인 경우, 쌍반점(';') 기호로 구분해야만 합니다. BEGIN/COMMIT 자체를 생략하는 일을 피하기 위해, 이 드라이버는 특히 BEGIN을 첫 번째 선언문으로 인식할 것입니다.
   트랜잭션 풀 작업에서 이 드라이버를 pg_bouncer와 함께, 예를 들어 ``BEGIN; SET LOCAL statement_timeout TO "1h";`` 와 같이 사용하는 경우 이 옵션이 유용할 수도 있습니다.

-  **CLOSING_STATEMENTS=string**: (GDAL 2.1 이상 버전)
   다른 모든 SQL 선언문 다음에 PostgreSQL 클라이언트 연결에 전송할 SQL 선언문(들)을 지정합니다. 선언문이 여러 개인 경우, 쌍반점(';') 기호로 구분해야만 합니다. 앞 PRELUDE_STATEMENTS 옵션의 예와 같이, CLOSING_STATEMENTS 옵션의 적절한 값은 "COMMIT"일 것입니다.

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

없음

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **GEOM_TYPE**:
   "geometry", (PostGIS 1.5버전부터) "geography", "BYTEA" 또는 "OID" 가운데 하나로 설정해서 테이블의 도형 유형을 강제할 수 있습니다. PostGIS 데이터베이스의 경우 기본값은 "geometry"입니다. PostGIS "geography" 도형 유형은 지리 좌표계를 가정하지만 (PostGIS 2.2 이전 버전들의 경우 심지어 EPSG:4326이어야 했습니다) 이 드라이버는 내장 재투영 로직을 가지고 있지 않기 때문에 'GEOM_TYPE=geography'와 함께 항상 '-t_srs EPSG:4326'를 (또는 원점(datum) 변형을 피하려면 투영 좌표계에 대응하는 표준 지리 좌표계를) 사용하는 것이 안전합니다.

-  **OVERWRITE**:
   요청한 레이어를 생성하기 전에 요청한 이름과 같은 이름을 가진 기존 레이어를 강제로 삭제하려면 이 옵션을 YES로 설정할 수도 있습니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 PostgreSQL과 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. NO로 설정하면 이름을 그대로 보전합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

-  **PRECISION**:
   해당 레이어에 생성되는 새 필드가 -- 사용할 수 있는 경우 NUMERIC(길이, 정밀도) 또는 CHAR(길이) 유형을 사용해서 -- 길이 및 정밀도 정보를 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다. NO로 설정하면 그 대신 FLOAT8, INTEGER 및 VARCHAR 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **DIM={2,3,XYM,XYZM}**:
   레이어의 차원을 제어합니다. PostGIS 1.0 이상 버전에서 데이터를 불러오는 도중 도형 차원에 제약 조건이 적용되기 때문에, 2차원 레이어의 경우 이 옵션을 2로 설정하는 것이 중요합니다.

-  **GEOMETRY_NAME**:
   새 테이블의 도형 열 이름을 설정합니다. 지정하지 않으면 GEOM_TYPE=geometry인 경우 *wkb_geometry* 를, GEOM_TYPE=geography인 경우 *the_geog* 를 기본값으로 사용합니다.

-  **SCHEMA**:
   새 테이블에 대한 스키마의 이름을 설정합니다. 서로 다른 스키마에 동일한 레이어 이름을 사용할 수 있지만, 공개(public) 스키마 및 기타 스키마에서는 사용할 수 없습니다. ogr2ogr 유틸리티의 '-overwrite' 옵션과 '-lco SCHEMA=' 옵션을 동시에 사용하면 작동하지 않을 것이라는 사실을 기억하십시오. ogr2ogr 유틸리티는 지정한 스키마에 있는 기존 레이어를 삭제해야만 한다는 사실을 이해하지 못 할 것이기 때문입니다. ogr2ogr 유틸리티의 '-nln' 옵션을 사용하거나, 차라리 active_schema 연결 문자열을 사용하는 편이 더 낫습니다. 아래 예시를 참조하십시오.

-  **SPATIAL_INDEX**\ = (GDAL 2.4버전부터) NONE/GIST/SPGIST/BRIN 또는 (이전 버전들 및 하위 호환성을 위해) YES/NO:
   기본값은 GIST(GDAL 2.4 이상 버전, 이전 버전들의 경우 YES)입니다.
   GIST로 설정하면 쿼리 속도를 높이기 위해 도형 열에 공간 색인(GiST)을 생성합니다. (PostGIS를 사용할 수 있는 경우에만 영향을 미칩니다.)
   NONE(GDAL 2.4 이상 버전, 이전 버전들의 경우 FALSE)로 설정하면 공간 색인 생성을 비활성화시킵니다.
   BRIN은 PostgreSQL 9.4버전 이상 그리고 PostGIS 2.3버전 이상인 경우에만 사용할 수 있습니다.
   SPGIST는 PostgreSQL 11버전 이상 그리고 PostGIS 2.5버전 이상인 경우에만 사용할 수 있습니다.

-  **TEMPORARY**:
   기본값은 OFF입니다. 영구적인 테이블 대신 임시 테이블을 생성합니다.

-  **UNLOGGED**:
   기본값은 OFF입니다. 테이블을 로그 작성 방지 속성을 가진 테이블로 생성할지 여부를 선택합니다. PostgreSQL 9.1버전부터 로그 작성 방지 속성을 가진 테이블을 지원하고, GiST 색인은 PostgreSQL 9.3버전부터 공간 색인 작업에 사용됩니다.

-  **NONE_AS_UNKNOWN**:
   TRUE로 설정하면 비공간 레이어(wkbNone)를 GEOMETRY 유형의 공간 테이블(wkbUnknown)로 강제 생성할 수 있습니다.
   기본값은 NO로, 이 경우 정규 테이블을 생성하는데 PostGIS geometry_columns 테이블에 기록하지 않습니다.

-  **FID**:
   생성할 FID 열의 이름을 지정합니다. 기본값은 'ogr_fid'입니다.

-  **FID64**:
   64비트 길이의 ID를 지원할 수 있는 FID 열을 생성하려면 TRUE로 설정할 수도 있습니다. 기본값은 FALSE입니다.

-  **EXTRACT_SCHEMA_FROM_LAYER_NAME**:
   스키마와 테이블 이름 사이의 점('.') 문자를 구분자로 간주하지 않으려면 NO로 설정하면 됩니다. 기본값은 YES입니다.

-  **COLUMN_TYPES**:
   ``CreateField()`` 메소드가 호출되었을 때 사용해야 할 'field_name=pg_field_type' 서식을 쉼표로 구분한 문자열 목록입니다. 이 옵션은 OGR가 선택했을 기본 유형을 대체합니다. 예를 들면 `HSTORE <http://www.postgresql.org/docs/9.0/static/hstore.html>`_ 유형의 열을 생성하는 데 이 옵션을 사용할 수 있습니다.

-  **DESCRIPTION**: (GDAL 2.1버전부터)
   pg_description 시스템 테이블에 들어갈 설명 문자열입니다. 읽기 작업 시, 이런 설명을 찾은 경우 DESCRIPTION 메타데이터 항목에 노출됩니다.
   ``SetMetadataItem("DESCRIPTION", description_string)`` 메소드로도 설명을 작성할 수 있습니다. ogr2ogr 유틸리티는 '-nomd' 옵션을 사용하지 않는 이상 기본적으로 설명을 보전합니다.

환경설정 옵션
~~~~~~~~~~~~~~~~~~~~~

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`PG_USE_COPY`:
   PostgreSQL에 데이터를 삽입할 때 COPY를 사용하려면 이 옵션을 YES로 설정할 수도 있습니다. COPY가 INSERT보다 훨씬 더 빠릅니다. 방금 생성된 테이블로부터 데이터를 삽입하는 경우 기본적으로 COPY를 사용합니다.

-  :decl_configoption:`PGSQL_OGR_FID`:
   'ogc_fid' 대신 기본 키의 이름을 설정합니다. 기본 키를 자동 탐지할 수 없는 레이어를 여는 경우에만 사용합니다. FID 생성 옵션을 사용하는 CreateLayer() 메소드를 사용하는 경우 이 환경설정 옵션의 값을 무시합니다.

-  :decl_configoption:`PG_USE_BASE64`:
   이 옵션을 YES로 설정하면, 도형을 표준 HEX 인코딩 EWKB 형식 대신 BASE64로 인코딩된 EWKB 형식으로 가져올 것입니다. 이렇게 하면 전송 데이터의 용량을 2N에서 1.333N으로 줄일 수 있습니다. 이때 N은 EWKB 데이터의 용량입니다. 하지만 클라이언트와 서버가 동일한 머신에 있는 경우 표준 형식으로 가져오는 것보다 조금 느릴 수도 있기 때문에, 기본값은 NO입니다.

-  :decl_configoption:`OGR_TRUNCATE`:
   이 옵션을 YES로 설정하면, 첫 번째 객체를 삽입하기 전에 SQL TRUNCATE 명령어로 테이블의 내용을 먼저 지울 것입니다. 이 옵션은 테이블 기반 뷰를 삭제하지 않는 ogr2ogr 유틸리티의 '-overwrite' 옵션 대신 사용할 수 있습니다.
   일반적인 사용례는 다음과 같습니다: ``ogr2ogr -append PG:dbname=foo abc.shp --config OGR_TRUNCATE YES``

예시
----

-  shapefile을 PostgreSQL로 단순 변환합니다. abc.shp 파일의 객체와 abc.dbf 파일의 속성으로 'abc' 테이블을 생성할 것입니다. 데이터베이스 인스턴스(warmerda)가 반드시 기존에 존재해야 하며, 'abc' 테이블은 기존에 존재해서는 안 됩니다.

   ::

      ogr2ogr -f PostgreSQL PG:dbname=warmerda abc.shp

-  두 번째 예시는 (:ref:`OGDI <vector.ogdi>` 드라이버를 통해) VPF로부터 행정 구역을 불러와서 암호 같은 OGDI 레이어 이름을 좀 더 알기 쉬운 이름으로 재명명합니다. 원하는 이름을 가진 기존 테이블이 존재하는 경우 덮어씁니다:

   ::

      ogr2ogr -f PostgreSQL PG:dbname=warmerda \
              gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia \
              -lco OVERWRITE=yes -nln polbndl_bnd 'polbndl@bnd(*)_line'

- 단일 PostgreSQL 테이블을 지오패키지로 내보내기:

   ::

     ogr2ogr \
       -f GPKG output.gpkg \
       PG:"dbname='my_database'" "my_table"

- PostgreSQL 테이블 여러 개를 지오패키지로 내보내기:

   ::

     ogr2ogr \
       -f GPKG output.gpkg \
       PG:"dbname='my_database' tables='table_1,table_3'"

- 전체 PostgreSQL 데이터베이스를 지오패키지로 내보내기:

   ::

     ogr2ogr \
       -f GPKG output.gpkg \
       PG:dbname=my_database


- 단일 지오패키지 레이어를 PostgreSQL로 불러오기:

   ::

     ogr2ogr \
       -f "PostgreSQL" PG:"dbname='my_database'" \
       input.gpkg \
       -nln "name_of_new_table"


-  이 예시에서는 서로 다른 두 디렉터리에 있는 TIGER 파일들로부터 TIGER/Line 데이터를 테이블 하나로 병합합니다. 두 번째 명령어가 'OVERWRITE=yes' 대신 '-append'를 사용한다는 점을 기억하십시오:

   ::

      ogr2ogr -f PostgreSQL PG:dbname=warmerda tiger_michigan \
           -lco OVERWRITE=yes CompleteChain
      ogr2ogr -update -append -f PostgreSQL PG:dbname=warmerda tiger_ohio \
           CompleteChain

-  이 예시는 ogrinfo 유틸리티를 이용해서 PostgreSQL 내에서 SQL 쿼리 선언문을 평가하는 방법을 보여줍니다. ogrinfo 유틸리티에 '-sql' 명령줄 스위치를 지정해서 좀 더 복잡한 PostGIS 특화 쿼리도 사용할 수 있습니다:

   ::

      ogrinfo -ro PG:dbname=warmerda -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

-  이 예시는 ogrinfo 유틸리티를 이용해서 다른 호스트 상에 있는 PostgreSQL/PostGIS 레이어를 목록화하는 방법을 보여줍니다:

   ::

      ogrinfo -ro PG:"host='myserver.velocet.ca' user='postgres' dbname='warmerda'"

-  이 예시는 PRELUDE_STATEMENTS 및 CLOSING_STATEMENTS 데이터셋 열기 옵션을 ogr2ogr 유틸리티의 대상 열기 옵션으로 사용하는 방법을 보여줍니다:

   ::

      ogrinfo PG:"dbname='mydb'" poly -doo "PRELUDE_STATEMENTS=BEGIN; SET LOCAL statement_timeout TO '1h';" -doo CLOSING_STATEMENTS=COMMIT

FAQs
----

-  **어째서 테이블이 안 보이나요? PostGIS를 설치했고 데이터도 있습니다**:
   사용자가 읽어오려 하는 모든 테이블 *그리고* geometry_columns 및 spatial_ref_sys 테이블에 대한 권한을 가지고 있어야만 합니다.
   이 테이블들에 대한 권한이 없는 경우 오류 메시지 없이 이해할 수 없는 습성을 보일 수도 있습니다. :decl_configoption:`PG_LIST_ALL_TABLES` 환경설정 옵션을 YES로 설정해서 (예: ``ogrinfo --config PG_LIST_ALL_TABLES YES PG:xxxxx``) 이 테이블들을 볼 수 있는지 확인해보십시오. 일반적으로 geometry_columns 그리고/또는 spatial_ref_sys 테이블에 대한 권한 문제를 확인할 수 있습니다.

참고
--------

-  :ref:`고급 OGR PostgreSQL 드라이버 정보 <vector.pg_advanced>`
-  :ref:`OGR PostgreSQL SQL 덤프 <vector.pgdump>` 드라이버
-  `PostgreSQL 홈페이지 <http://www.postgresql.org/>`_
-  `PostGIS <http://postgis.net/>`_
-  `PostGIS / OGR 위키 예제 페이지 <http://trac.osgeo.org/postgis/wiki/UsersWikiOGR>`_

.. toctree::
   :maxdepth: 1
   :hidden:

   pg_advanced

