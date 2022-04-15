.. _vector.mssqlspatial:

MSSQLSpatial - 마이크로소프트 SQL 서버 공간 데이터베이스
====================================================

.. shortname:: MSSQLSpatial

.. build_dependencies:: ODBC 라이브러리

MSSQLSpatial 드라이버는 마이크로소프트 SQL 서버 2008 이상 버전에 있는 도형 열을 표현하기 위한 도형 및 지리 데이터 유형을 담고 있는 공간 테이블에 대한 접근을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터베이스에 접속하기
------------------------

MSSQL 데이터소스에 접근하려면, 데이터베이스 이름을 지정하는 연결 문자열을 필요한 추가 파라미터와 함께 사용하십시오. 연결 문자열 앞에 '*MSSQL:*' 접두어를 반드시 붙여야만 합니다.

   ::

      MSSQL:server=.\MSSQLSERVER2008;database=dbname;trusted_connection=yes

`ODBC 드라이버 연결 문자열 <http://msdn.microsoft.com/en-us/library/ms130822.aspx>`_ 서식으로 된 표준 파라미터 이외에도 다음 사용자 지정 파라미터를 다음과 같은 문법으로 사용할 수도 있습니다:

-  **Tables=schema1.table1(geometry column1),schema2.table2(geometry column2)**:
   이 파라미터를 사용해서 드라이버가 사용할 레이어들의 부분 집합을 지정할 수 있습니다. 이 파라미터를 설정하지 않는 경우, geometry_columns 메타데이터 테이블로부터 레이어를 가져옵니다. 이 문법에서 스키마 및 도형 열을 지정하는 부분을 생략할 수 있습니다.

-  **GeometryFormat=native|wkb|wkt|wkbzm**:
   서버로부터 어떤 포맷으로 도형을 가져와야 할지를 지정합니다. 이 경우 기본값은 'native'로, 이 경우 네이티브 SqlGeometry 및 SqlGeography 직렬화(serialization) 포맷을 사용합니다. 'wkb' 또는 'wkt'로 설정하는 경우 서버에서 도형 표현을 'WKB(Well Known Binary)' 및 'WKT(Well Known Text)'로 변환합니다. 이 변환 작업은 서버에서 상당한 간접 비용(overhead)을 치르도록 요구하기 때문에 네이티브 포맷을 사용할 때보다 객체 접근이 더 느려집니다. 'wkbzm' 포맷은 SQL 서버 2012에 접속하는 경우에만 사용할 수 있습니다.

연결 문자열에 있는 파라미터 이름은 대소문자를 구분하지 않습니다.

이 드라이버가 알맞은 데이터베이스를 선택할 수 있게 하려면 **Database** 파라미터를 지정해야 합니다.

사용자 지정 (FreeTDS 같은) SQL 서버 드라이버를 불러와야 하는 경우 연결 문자열에 선택적인 **Driver** 파라미터가 포함될 수도 있습니다. 이 파라미터의 기본값은 **{SQL Server}** 입니다.

레이어
------

사용자가 MSSQLSPATIAL_LIST_ALL_TABLES 환경 변수를 YES로 정의한 경우 (그리고 연결 문자열에 'Tables='를 지정하지 않은 경우) 모든 정규 사용자 테이블을 레이어로 취급할 것입니다. 공간 데이터가 없는 테이블을 원한다면 이 옵션이 유용합니다.

기본적으로 MSSQLSpatial 드라이버는 *geometry_columns* 메타데이터 테이블에 등록된 레이어만 검색할 것입니다. 사용자가 MSSQLSPATIAL_USE_GEOMETRY_COLUMNS 환경 변수를 NO로 정의하면 드라이버가 시스템 카탈로그에 있는 모든 사용자 공간 테이블을 검색할 것입니다.

SQL 선언문
--------------

MSSQLSpatial 드라이버는 OGRDataSource 상에 ExecuteSQL() 함수를 호출하거나 ogr2ogr 유틸리티에 '-sql' 명령어 옵션을 사용하는 경우, 내부적으로 SQL 문을 평가하기보다는 기본적으로 MS SQL에 SQL 문을 직접 전송합니다. 속성 쿼리 표현식도 MS SQL에 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 MSSQLSpatial 드라이버가 SQL 문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

OGR에서 MSSQLSpatial 드라이버는 일반적인 SQL 맥락에서 OGRLayer::StartTransaction(), OGRLayer::CommitTransaction() 및 OGRLayer::RollbackTransaction() 호출을 지원합니다.

생성 문제점
---------------

이 드라이버는 새 데이터베이스 생성을 지원하지 않습니다. 데이터베이스를 생성하려면 마이크로소프트 SQL 서버 클라이언트 도구(Microsoft SQL Server Client Tools)를 이용하십시오. 기존 데이터베이스 안에 새 레이어를 생성할 수는 있습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **GEOM_TYPE**:
   "geometry" 또는 "geography" 가운데 하나로 설정할 수 있습니다. 이 옵션을 지정하지 않는 경우 기본값은 "geometry"입니다. 즉 "geography" 유형을 가진 도형 열을 생성하려면 이 옵션을 "geography"로 설정해야 한다는 뜻입니다. 이 경우 레이어가 **sys.spatial_reference_systems** SQL 서버 메타데이터 테이블에 정의된 지리 좌표계 가운데 하나인 무결한 공간 좌표계를 사용해야만 합니다.
   이 경우 투영 좌표계는 지원하지 않습니다.

-  **OVERWRITE**:
   요청한 레이어를 생성하기 전에 요청한 이름을 가진 기존 레이어를 강제로 삭제하고 싶다면 이 옵션을 YES로 설정할 수도 있습니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 MS SQL과 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

-  **PRECISION**:
   해당 레이어에 생성되는 새 필드가 -- 사용할 수 있는 경우 숫자(길이, 정밀도) 또는 문자(길이) 유형을 사용해서 -- 길이 및 정밀도 정보를 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다. NO로 설정하면 그 대신 float, int 및 varchar 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **DIM={2,3}**:
   레이어의 차원을 제어합니다. 기본값은 3입니다.

-  **GEOMETRY_NAME**:
   새 테이블의 도형 열 이름을 설정합니다. 지정하지 않는 경우 기본값 *ogr_geometry* 를 사용합니다.

-  **SCHEMA**:
   새 테이블에 대한 스키마의 이름을 설정합니다. 이 파라미터를 지원하지 않는 경우 기본 스키마 "*dbo*"를 사용합니다.

-  **SRID**:
   새 테이블의 공간 좌표계(Spatial Reference) ID를 명확하게 설정합니다. 해당 항목이 이미 spatial_ref_sys 메타데이터 테이블에 추가되어 있어야 합니다. 이 파라미터를 설정하지 않는 경우 소스 레이어 공간 좌표계의 기관 코드로부터 SRID를 파생시킵니다.

-  **SPATIAL_INDEX**:
   새로 생성되는 레이어 상에 공간 색인을 자동 생성할지 여부를 선택하는 불(boolean) 플래그입니다. 기본값은 YES입니다.

-  **UPLOAD_GEOM_FORMAT**:
   객체 생성 또는 수정 시 사용할 도형 포맷(wkb 또는 wkt)을 지정합니다. 기본값은 'wkb'입니다.

-  **FID**:
   생성할 FID 열의 이름을 지정합니다. 기본값은 'ogr_fid'입니다.

-  **FID64**:
   64비트 길이의 ID를 처리하기 위해 BigInt 유형의 FID 열을 생성할지 여부를 선택합니다. 기본값은 NO입니다.

-  **GEOMETRY_NULLABLE**:
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 기본값은 YES입니다.

-  **EXTRACT_SCHEMA_FROM_LAYER_NAME**: (GDAL 2.3.0버전부터)
   점('.') 문자를 스키마와 테이블 이름 사이의 구분자로 간주하지 않으려면 NO로 설정하면 됩니다. 기본값은 YES입니다.

환경설정 옵션
---------------------

이 드라이버의 습성을 제어하는 데 도움이 되는 다양한 `환경설정 옵션 <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 들이 있습니다:

-  **MSSQLSPATIAL_USE_BCP**: (GDAL 2.1.0버전부터)
   객체 추가 시 벌크(bulk) 삽입을 활성화합니다. 이 옵션을 사용하려면 GDAL을 SQL 서버 네이티브 클라이언트 11.0 같은 벌크 복사가 활성화된 ODBC 드라이버를 대상으로 컴파일해야 합니다. 연결 문자열에 BCP(Bulk CoPy) 지원 드라이버를 지정하려면 ``DRIVER={SQL Server Native Client 11.0}`` 같은 드라이버 파라미터를 사용하십시오. GDAL이 SQL 서버 네이티브 클라이언트 10.0 또는 11.0을 대상으로 컴파일된 경우, 이 드라이버를 자동으로 선택하기 때문에 연결 문자열에 지정할 필요가 없습니다. GDAL이 SQL 서버 네이티브 클라이언트 10.0 또는 11.0을 대상으로 컴파일된 경우 이 옵션의 기본 설정값은 TRUE이고, 그렇지 않다면 드라이버가 이 옵션을 무시합니다.

-  **MSSQLSPATIAL_BCP_SIZE**: (GDAL 2.1.0버전부터)
   벌크 삽입 배치(batch) 용량을 지정합니다. 값이 높을수록 삽입 작업이 빨라지지만 더 많은 메모리를 소비합니다. 기본값은 1000입니다.

-  **MSSQLSPATIAL_OGR_FID**:
   FID 열 이름을 대체합니다. 기본값은 'ogr_fid'입니다.

-  **MSSQLSPATIAL_ALWAYS_OUTPUT_FID**:
   항상 (실제 IDENTITY 열이 아니더라도) 최근 생성된 객체의 FID 값을 가져옵니다. 기본값은 NO입니다.

-  **MSSQLSPATIAL_SHOW_FID_COLUMN**:
   FID 열을 객체 속성으로 강제 출력합니다. 기본값은 NO입니다.

-  **MSSQLSPATIAL_USE_GEOMETRY_COLUMNS**:
   데이터베이스에서 geometry_columns 메타데이터 테이블을 사용/생성합니다. 기본값은 YES입니다.

-  **MSSQLSPATIAL_LIST_ALL_TABLES**:
   사용할 수 있는 레이어를 목록화하기 위해 MS SQL 카탈로그를 이용합니다. 기본값은 NO입니다.

-  **MSSQLSPATIAL_USE_GEOMETRY_VALIDATION**: (GDAL 3.0버전부터)
   드라이버가 MS SQL 서버에서 런타임 오류를 촉발시키는 도형을 탐지할 수 있게 해줍니다. 드라이버가 해당 도형을 서버에 제출(submit)하기 전에 수정하려 시도합니다. 기본값은 YES입니다.

트랜잭션 지원
-------------------

이 드라이버는 :ref:`rfc-54` 을 따라 데이터셋 수준에서 트랜잭션을 구현합니다.

예시
--------

-  OGR 데이터소스로부터 레이어를 생성하기:

   ::

      ogr2ogr -overwrite -f MSSQLSpatial "MSSQL:server=.\MSSQLSERVER2008;database=geodb;trusted_connection=yes" "rivers.tab"

      ogr2ogr -overwrite -f MSSQLSpatial "MSSQL:server=127.0.0.1;database=TestDB;UID=SA;PWD=DummyPassw0rd" "rivers.gpkg"
      
-  레이어에 접속해서 콘텐츠를 덤프하기:

   ::

      ogrinfo -al "MSSQL:server=.\MSSQLSERVER2008;database=geodb;tables=rivers;trusted_connection=yes"
      
      ogrinfo -al "MSSQL:server=127.0.0.1;database=TestDB;driver=ODBC Driver 17 for SQL Server;UID=SA;PWD=DummyPassw0rd"

-  사용자명/비밀번호로 접속하기:

   ::
   
      ogrinfo -al   MSSQL:server=.\MSSQLSERVER2008;database=geodb;trusted_connection=no;UID=user;PWD=pwd
