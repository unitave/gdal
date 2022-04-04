.. _vector.db2:

DB2 Spatial
===========

.. shortname:: DB2

.. build_dependencies:: ODBC library

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_DB2

이 드라이버는 GDAL에 포함된 기본 ODBC 지원을 이용해서 리눅스, 유닉스 및 윈도우 용 (DB2 LUW) IBM DB2의 공간 테이블에, 그리고 z/OS 용 IBM DB2 관계형 데이터베이스에 접근하기 위한 지원을 구현했습니다.

`z/OS 용 DB2 <http://www-01.ibm.com/support/knowledgecenter/SSEPEK_11.0.0/com.ibm.db2z11.doc.spatl/src/spatl/dasz_spatl.dita?lang=en>`_ 및 `DB2 LUW <http://www-01.ibm.com/support/knowledgecenter/SSEPGG_10.5.0/com.ibm.db2.luw.spatial.topics.doc/doc/db2sb03.html>`_ 에서 DB2 Spatial 객체에 관한 문서를 찾아볼 수 있습니다.

이 드라이버는 현재 윈도우 환경에서만 지원됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터베이스에 연결하기
------------------------

DB2 데이터소스에 접속하려면, 필요한 추가 파라미터들과 함께 데이터베이스 이름을 지정한 연결 문자열을 사용하십시오. 이 연결 문자열 앞에 반드시 '*DB2ODBC:*' 접두어를 붙여야만 합니다.
등록된 DSN을 지정하거나 또는 호스트, 포트 및 프로토콜을 지정하는 파라미터를 이용할 수 있습니다.

   ::

      DB2ODBC:database=dbname;DSN=datasourcename

또는

   ::

      DB2ODBC:database=dbname;DRIVER={IBM DB2 ODBC DRIVER};Hostname=hostipaddr;PROTOCOL=TCPIP;port=db2port;UID=myuserid;PWD=mypw

다음 사용자 지정 파라미터도 다음과 같은 문법으로 사용할 수 있습니다:

-  **Tables=schema1.table1(geometry column1),schema2.table2(geometry column2)**:
   이 파라미터를 이용하면 드라이버가 사용할 레이어의 하위 집합을 지정할 수 있습니다. 이 파라미터를 지정하지 않는 경우, DB2GSE.ST_GEOMETRY_COLUMNS 메타데이터 뷰로부터 레이어를 가져옵니다. 이 문법에서 스키마와 도형 열을 지정하는 부분을 생략할 수 있습니다.

연결 문자열의 파라미터 이름은 대소문자를 구분하지 않습니다.

이 드라이버가 알맞은 데이터베이스를 선택할 수 있게 하려면 **Database** 파라미터를 지정해야 합니다.

레이어
------

DB2 드라이버는 기본적으로 DB2GSE.ST_GEOMETRY_COLUMNS 메타데이터 테이블에 등록된 레이어만 검색할 것입니다.

SQL 선언문
--------------

DB2 드라이버는 OGRDataSource에 ExecuteSQL() 함수를 호출하거나 ogr2ogr에 -sql 명령어 옵션을 사용하는 경우 내부적으로 SQL 선언문을 평가하기 보다는 기본적으로 DB2에 SQL 선언문을 직접 전송합니다. 속성 쿼리 표현식도 DB2에 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 OGR DB2 드라이버가 SQL 선언문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

OGR에서 DB2 드라이버는 일반적인 SQL 맥락에서 OGRLayer::StartTransaction(), OGRLayer::CommitTransaction() 및 OGRLayer::RollbackTransaction() 호출을 지원합니다.

생성 문제점
---------------

이 드라이버는 새 데이터베이스 생성을 지원하지 않습니다. 데이터베이스를 생성하려면 DB2 명령줄 또는 IBM 데이터 스튜디오 같은 도구들을 이용하십시오. 기존 데이터베이스 안에 새 레이어를 생성할 수는 있습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **OVERWRITE**:
   요청한 레이어를 생성하기 전에 요청한 이름을 가진 기존 레이어를 강제로 삭제하고 싶다면 이 옵션을 YES로 설정할 수도 있습니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 DB2와 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

-  **PRECISION**:
   해당 레이어에 생성되는 새 필드가 -- 사용할 수 있는 경우 숫자(길이, 정밀도) 또는 문자(길이) 유형을 사용해서 -- 길이 및 정밀도 정보를 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다. NO로 설정하면 그 대신 float, int 및 varchar 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **DIM={2,3}**:
   레이어의 차원을 제어합니다. 기본값은 2입니다.

-  **GEOM_NAME**:
   새 테이블의 도형 열 이름을 설정합니다. 지정하지 않는 경우 기본값 *ogr_geometry* 를 사용합니다.

-  **SCHEMA**:
   새 테이블에 대한 스키마의 이름을 설정합니다. 기본 스키마는 userid가 데이터베이스에 접속하기 위해 사용한 스키마입니다.

-  **SRID**:
   새 테이블의 공간 참조(Spatial Reference) ID를 명확하게 설정합니다. 해당 항목이 이미 spatial_ref_sys 메타데이터 테이블에 추가되어 있어야 합니다. 이 파라미터를 설정하지 않는 경우 소스 레이어 공간 좌표계의 기관 코드로부터 SRID를 파생시킵니다.

공간 색인 생성
~~~~~~~~~~~~~~~~~~~~~~

DB2 드라이버는 레이어 생성 과정에서 기본적으로 테이블에 공간 색인을 추가하지 않습니다. ``DB2 CREATE INDEX`` 명령어로 공간 색인을 생성해야 합니다.

예시
--------

OGR 데이터소스로부터 레이어를 생성하기:

   ::

      ogr2ogr -overwrite  DB2ODBC:database=sample;DSN=sampDSN zipcodes.shp

레이어에 접속해서 콘텐츠를 덤프하기:

   ::

      ogrinfo -al DB2ODBC:database=sample;DSN=sampDSN;tables=zipcodes

