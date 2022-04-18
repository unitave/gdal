.. _vector.odbc:

ODBC RDBMS
==========

.. shortname:: ODBC

.. build_dependencies:: ODBC 라이브러리

OGR는 ODBC를 통한 공간 및 비공간 테이블에의 접근을 선택적으로 지원합니다. ODBC는 수많은 데이터베이스 시스템 및 데이터베이스(테이블 집합)로 표현될 수 있는 데이터에 접근하기 위한 일반 접근 레이어입니다. 유닉스 및 윈도우 플랫폼 상에서 ODBC 지원을 사용할 수 있는 가능성이 있지만, 특수 환경설정 옵션을 사용해야만 ODBC 지원이 유닉스 빌드에 포함됩니다.

다음과 같은 형식의 데이터소스 이름을 사용해서 ODBC 데이터소스에 접근할 수 있습니다:

::

   ODBC:\ userid/password\ @\ dsn,\ schema.tablename(geometrycolname),...:srs_tablename(sridcolumn,srtextcolumn)

다음과 같이 선택적인 항목을 삭제한 형식도 사용할 수 있습니다:

-  ``ODBC:\ userid/password\ @\ dsn``
-  ``ODBC:\ userid\ @\ dsn,\ table_list``
-  ``ODBC:\ dsn,\ table_list``
-  ``ODBC:\ dsn``
-  ``ODBC:\ dsn,\ table_list:srs_tablename``

**dsn** 이란 ODBC 데이터소스 이름(Data Source Name)입니다. ODBC 데이터소스는 일반적으로 ODBC 관리자 도구를 이용해서 설정되고 DSN을 할당받습니다. 데이터소스에 접근하기 위해 이 DSN을 사용하는 것입니다.

ODBC는 기본적으로 GEOMETRY_COLUMNS 테이블을 검색합니다. 이 테이블을 찾았다면 OGR가 레이어로 취급해야 할 공간 테이블 집합을 식별하기 위해 사용합니다. 찾지 못 한 경우, 데이터소스에 있는 모든 테이블을 비공간 레이어로 반환합니다. 하지만 (테이블 이름을 쉼표로 구분한) 테이블 목록을 지정한다면 그 테이블들만 (비공간) 레이어로 표현할 것입니다. 복잡한 데이터베이스에 있는 모든 테이블의 완전한 정의를 가져오는 것은 꽤 시간이 걸릴 수 있기 때문에, 접근할 테이블들의 집합을 제한할 수 있는 기능은 성능을 좌우할 수 있습니다.

GEOMETRY_COLUMNS 테이블을 찾았다면, 도형 소스가 될 열을 선택하기 위해 사용합니다. 데이터소스 이름에 테이블을 포하시켜 전송하는 경우, 테이블명 뒤에 테이블 관련 도형 열을 둥근 괄호로 묶어서 포함시킬 수 있습니다. 현재, 필드가 바이너리 유형이면 도형이 WKB(Well Known Binary) 포맷이고 다른 유형이면 WKT(Well Known Text) 포맷이라는 가정이 하드코딩되어 있습니다. GEOMETRY_COLUMNS 테이블은 최소한 F_TABLE_NAME, F_GEOMETRY_COLUMN 및 GEOMETRY_TYPE 열을 가지고 있어야 합니다.

테이블이 도형 열을 가지고 있고 도형 열이 XMIN, YMIN, XMAX 및 YMAX라는 필드를 가지고 있는 경우, 공간 필터로 테이블을 직접 쿼리해서 공간 쿼리의 속도를 향상시킬 수 있습니다. XMIN, YMIN, XMAX 및 YMAX 필드는 행에 테이블 좌표계 단위의 도형 범위를 나타내야 합니다.

기본적으로 기저 데이터베이스 엔진에 SQL 선언문을 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 드라이버가 SQL 문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

데이터셋 열기 옵션
--------------------

-  **LIST_ALL_TABLES=YES/NO**: (GDAL 3.4 이상 버전)
   (MSys* 테이블 같은) 시스템 및 내부 테이블을 포함하는 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다. 마이크로소프트 액세스(Access) 데이터베이스 전용 옵션입니다. 마이크로소프트 액세스 ODBC 드라이버가 언제나 MSys* 테이블을 완전히 제거하기 때문에, 윈도우 플랫폼 상에서는 이 옵션을 YES로 설정했더라도 MSys* 테이블을 반환하지 않을 것이라는 사실을 기억하십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

액세스 데이터베이스 (.MDB) 지원
-------------------------------

윈도우 상에서 "마이크로소프트 액세스 드라이버 (\*.mdb)" ODBC 드라이버가 설치되어 있다고 할 때, (개인 지리 데이터베이스(Personal Geodatabase) 또는 Geomedia 데이터베이스가 아닌) 비공간 마이크로소프트 액세스 데이터베이스를 파일명으로 직접 열 수 있습니다.

리눅스 상에서는 unixODBC 및 mdbtools를 설치하면 ODBC 드라이버를 이용해서 비공간 마이크로소프트 액세스 데이터베이스를 열 수 있습니다. 어떻게 이를 활성화할 수 있는지 알고 싶다면 :ref:`MDB <vector.pgeo>` 드라이버 문서를 읽어보십시오.

이 드라이버는 마이크로소프트 액세스 데이터베이스 용 .mdb 또는 .accdb 확장자를 둘 다 지원합니다. 뿐만 아니라 ESRI .style 데이터베이스 확장자를 가진 파일도 열 수 있습니다. (ESRI .style 확장자는 .mdb 파일 확장자의 별명일 뿐입니다.)

생성 문제점
---------------

현재 ODBC OGR 드라이버는 읽기 전용이기 때문에, OGR 응용 프로그램이 새 객체, 테이블 및 데이터소스를 정상적으로 생성하지 못 합니다. 이 제한 사항은 향후 제거될 수도 있습니다.

참고
----

-  `MSDN ODBC API 참조 자료 <http://msdn.microsoft.com/en-us/library/ms714562(VS.85).aspx>`__
-  :ref:`PGeo <vector.pgeo>` 드라이버

