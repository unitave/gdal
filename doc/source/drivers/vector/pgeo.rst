.. _vector.pgeo:

ESRI 개인 지리 데이터베이스
=========================

.. shortname:: PGeo

.. build_dependencies:: ODBC library

OGR는 ODBC를 통해 ESRI 개인 지리 데이터베이스(Personal Geodatabase) .mdb 파일의 읽기를 선택적으로 지원합니다. 개인 지리 데이터베이스란 지리 데이터베이스 메타데이터를 담기 위해 ESRI가 정의한 테이블 집합 및 BLOB 열에 담긴 객체의 맞춤형 포맷으로 된 도형을 (본질적으로 shapefile 도형 조각들을) 가진 마이크로소프트 액세스 데이터베이스입니다. PGeo 드라이버는 ODBC를 통해 하지만 어떤 ESRI 미들웨어에도 의존하지 않고 개인 지리 데이터베이스에 접근합니다.

접근할 .mdb 파일의 파일명을 데이터소스 이름으로 전송해서 개인 지리 데이터베이스에 접근합니다.

서로 다른 환경설정들과의 호환성을 담보하기 위해, 파일명을 인자로 가진 DSN을 프로그램적으로 설정하는 방식을 제공하기 위해 :decl_configoption:`PGEO_DRIVER_TEMPLATE` 환경설정 옵션을 추가했습니다. 드라이버 이름을 알고 있는 경우 이 옵션은 (윈도우 상에서 마이크로소프트 액세스 드라이버에 접근하기 위해 쓰이는) 기본 습성과 비슷한 방식으로 해당 정보를 기반으로 하는 DSN을 구성하게 해줍니다.

OGR는 모든 객체 테이블을 레이어로 취급합니다. 3차원 데이터를 포함, 대부분의 도형 유형을 지원할 것입니다. 측정 정보(m 값)도 지원합니다. 좌표계는 레이어와 제대로 연관되어 있어야 합니다.

OGR 개인 지리 데이터베이스 드라이버는 현재 빠른 공간 쿼리를 위한 공간 색인의 장점을 이용하지 못 하고 있지만, 향후 공간 색인 지원이 추가될 수도 있습니다.

개인 지리 데이터베이스 포맷은 폴리곤 또는 라인 레이어의 경우 멀티 및 단일 도형 유형을 엄격하게 구분하지 않기 때문에, 폴리곤 또는 라인 레이어가 멀티 및 단일 도형 유형을 혼합해서 담고 있을 수 있습니다. 따라서, GDAL 드라이버는 예상 가능한 도형 유형을 지정하기 위해 항상 라인 레이어의 유형을 wkbMultiLineString으로 그리고 폴리곤 레이어의 유형을 wkbMultiPolygon으로 리포트할 것입니다. 읽어오는 도중 데이터베이스에 있는 단일 부분(single part) 라인 또는 폴리곤 객체를 멀티라인스트링 또는 멀티폴리곤으로 승격시킬 것입니다.

기본적으로 MDB 데이터베이스 엔진에 SQL 선언문을 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 드라이버가 SQL 문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

특수 SQL 요청
-------------

"GetLayerDefinition a_layer_name" 및 "GetLayerMetadata a_layer_name"을 특수 SQL 요청으로 이용해서 각각 개인 지리 데이터베이스 테이블의 정의 및 메타데이터를 XML 콘텐츠로 가져올 수 있습니다.

데이터셋 열기 옵션
--------------------

-  **LIST_ALL_TABLES=YES/NO**: (GDAL 3.4 이상 버전)
   (GDB_* 테이블 같은) 시스템 및 내부 테이블을 포함하는 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::


필드 도메인
-------------

.. versionadded:: 3.4

인코딩된 그리고 범위가 지정된 필드 도메인을 지원합니다.

PGeo 드라이버를 (유닉스/리눅스 상에서) unixODBC 및 MDB 도구와 함께 사용하는 방법
--------------------------------------------------------------------------------

이 단락에서는 OGR를 unixODBC 패키지와 함께 사용하는 방법 및 PGeo 드라이버로 개인 지리 데이터베이스에 접근하는 방법을 단계별로 설명합니다. `기타 상세 정보를 위한 GDAL 위키 <http://trac.osgeo.org/gdal/wiki/mdbtools>`_ 도 읽어보십시오.

전제 조건
~~~~~~~~~~~~~
.. role:: bash(code)
   :language: bash

#. `unixODBC <http://www.unixodbc.org>`_ 2.2.11 이상 버전을 설치하십시오.
#. MDB 도구(MDB Tools)를 설치하십시오. MDB 도구의 공식 업스트림은 `https://github.com/mdbtools/mdbtools <https://github.com/mdbtools/mdbtools>`_ 에서 유지관리되고 있습니다.
   PGeo 드라이버와의 최적 호환성을 위해 0.9.4 이상 버전을 권장합니다.
   최신 버전을 설치하는 경우 데비안 리눅스 상에서는 (다음 단락의) 추가 환경설정이 필요없으며, :bash:`ogrinfo sample.mdb` 도 잘 작동합니다.

(우분투에서: :bash:`sudo apt-get install unixodbc libmdbodbc`)

(데비안에서: :bash:`sudo apt-get install unixodbc odbc-mdbtools`)

환경설정
~~~~~~~~~~~~~

unixODBC 용 환경설정 파일이 2개 있습니다:

-  odbcinst.ini -
   이 파일은 모든 사용자가 사용할 수 있는 ODBC 드라이버의 정의를 담고 있습니다. 이 파일의 위치는 /etc 디렉터리 또는 사용자가 직접 unixODBC를 빌드하는 경우 '--sysconfdir' 스위치로 지정한 위치입니다.

-  odbc.ini -
   이 파일은 모든 사용자가 사용할 수 있는 ODBC 데이터소스의 정의(DSN 항목)를 담고 있습니다.

-  ~/.odbc.ini -
   이 파일은 사용자가 자신의 ODBC 데이터소스를 넣을 수 있는 개인 파일(private file)입니다.

DSN(Data Source Name)을 통해 개인 지리 데이터베이스 파일에 직접 접근할 수 있도록 사용자가 ODBC DSN을 설정하려는 경우에만 odbc.ini 파일을 편집해야 합니다. .mdb 파일명을 직접 사용하는 경우 PGeo 드라이버가 필요한 연결 파라미터를 자동으로 처리할 것이기 때문에, odbc.ini 파일 편집은 완전히 선택적인 방식입니다.

환경설정 파일의 서식은 매우 단순합니다:

::

   [section_name]
   entry1 = value
   entry2 = value

더 자세한 내용은 `unixODBC 지침서 <http://www.unixodbc.org/doc/>`_ 를 참조하십시오.

1. ODBC 드라이버 환경설정
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

먼저, ODBC 드라이버가 MDB 도구를 이용해서 마이크로소프트 액세스 데이터베이스에 접근하도록 환경설정해야 합니다. 사용자의 odbcinst.ini 파일에 다음 정의를 추가하십시오.

::

   [Microsoft Access Driver (*.mdb)]
   Description = MDB Tools ODBC drivers
   Driver     = /usr/lib/libmdbodbc.so.0
   Setup      =
   FileUsage  = 1
   CPTimeout  =
   CPReuse    =

-  [Microsoft Access Driver (\*.mdb)] -
   PGeo 드라이버가 "DRIVER=Microsoft Access Driver (\*.mdb);" 문자열을 사용해서 개인 지리 데이터베이스 용 ODBC 연결 문자열을 구성하기 때문에 "Microsoft Access Driver (\*.mdb)"를 단락 이름으로 사용해야 한다는 사실을 기억하십시오.

-  Description -
   이 드라이버 정의의 짧은 설명을 넣으십시오.

-  Driver -
   MDB 도구를 위한 ODBC 드라이버의 전체 경로입니다.

2. ODBC 데이터소스 환경설정 (선택적)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

이 단락에서는 'sample.mdb'를 개인 지리 데이터베이스의 이름으로 사용합니다. 사용자 자신의 데이터베이스로 대체하십시오.

사용자의 홈 디렉터리에 .odbc.ini 파일을 생성하십시오:

::

   $ touch ~/.odbc.ini

사용자의 .odbc.ini 파일에 다음 ODBC 데이터소스 정의를 추가하십시오:

::

   [sample_pgeo]
   Description = Sample PGeo Database
   Driver      = Microsoft Access Driver (*.mdb)
   Database    = /home/mloskot/data/sample.mdb
   Host        = localhost
   Port        = 1360
   User        = mloskot
   Password    =
   Trace       = Yes
   TraceFile   = /home/mloskot/odbc.log

다음은 DSN 항목의 단계별 설명입니다:

-  [sample_pgeo] -
   ODBC 데이터소스의 이름(DSN)입니다. 이 이름을 사용해서 사용자의 개인 지리 데이터베이스를 참조할 것입니다. 여기에 사용자 자신의 데이터소스 이름을 넣으십시오.

-  Description -
   DSN 항목의 짧은 설명입니다.

-  Driver -
   1단계에서 정의한 드라이버의 전체 명칭입니다. 앞 단락을 참조하십시오.

-  Database -
   사용자의 개인 지리 데이터베이스를 가지고 있는 .mdb 파일을 가리키는 전체 경로입니다.

-  MDB 도구 드라이버는 Host, Port, User 및 Password 항목을 사용하지 않습니다.

ogrinfo로 PGeo 드라이버 테스트하기
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

이제 ogrinfo 유틸리티로 PGeo 데이터소스에 접근을 시도해볼 수 있습니다.

먼저 OGR에 PGeo 드라이버가 빌드되어 있는지 확인하십시오:

::

   $ ogrinfo --formats
   Supported Formats:
     ESRI Shapefile
     ...
     PGeo
     ...

이제 사용자의 개인 지리 데이터베이스에 접근할 수 있습니다. 개인 지리 데이터베이스 용 DSN을 (앞 2번 단락에서 설명한 대로) 설정했다면, 데이터소스는 PGeo:<DSN>일 것입니다. 이때 <DSN>이 사용자의 .odbc.ini 파일에 작성한 DSN 항목의 이름입니다.

DSN을 직접 생성하는 대신, OGR에 .mdb 파일명을 직접 전송할 수도 있습니다:

::

   ogrinfo PGeo:sample_pgeo
   INFO: Open of `PGeo:sample_pgeo'
   using driver `PGeo' successful.
   1. ...

앞의 명령어를 실행한 후, 사용자 지리 데이터베이스에 저장된 레이어 목록을 볼 수 있을 것입니다.

이제 특정 레이어의 상세 정보를 쿼리해봅시다:

::

   ogrinfo PGeo:sample_pgeo <layer name>
   INFO: Open of `PGeo:sample_pgeo'
   using driver `PGeo' successful.

   Layer name: ...

리소스
---------

-  `ESRI 지리 데이터베이스에 관하여 <http://www.esri.com/software/arcgis/geodatabase/index.html>`_
-  `MDB 도구 프로젝트 홈 <https://github.com/mdbtools/mdbtools>`_

