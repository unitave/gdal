.. _vector.sqlite:

SQLite / SpatiaLite RDBMS
=========================

.. shortname:: SQLite

.. build_dependencies:: libsqlite3 또는 libspatialite

OGR는 SQLite 3.x 데이터베이스 파일에 저장된 공간 및 비공간 테이블을 선택적으로 지원합니다. SQLite는 꽤 완전한 SQL 의미 체계(semantics) 및 상당한 성능을 갖춘 단일 파일 기반 "경량" RDBMS 엔진입니다.

SQLite 드라이버는 "정규" SQLite 데이터베이스는 물론 SpatiaLite (공간 활성화된 SQLite) 데이터베이스도 처리할 수 있습니다. ``ogrinfo db.sqlite --debug on`` 을 실행해서 얻은 "OGR style SQLite DB found", "OGR style SpatiaLite DB found", 또는 "OGR style SpatiaLite v4 DB found" SQLITE 디버그 정보값으로부터 기존 데이터베이스의 유형을 확인할 수 있습니다.

GDAL 2.2버전부터, SQLite 드라이버는 :ref:`RasterLite2 래스터 커버리지 <raster.rasterlite2>` 를 가진 데이터베이스도 읽을 수 있습니다.

SQLite 데이터베이스는 본질적으로 유형이랄 게 없지만, SQLite 드라이버는 테이블에 있는 첫 번째 레코드의 내용을 기반으로 속성 필드를 텍스트형, 정수형 또는 부동소수점형으로 분류하려 시도할 것입니다. 날짜&시간 필드 유형도 처리합니다.

GDAL 2.2버전부터, "JSonStringList", "JSonIntegerList", "JSonInteger64List" 및 "JSonRealList" SQLite 선언 유형을 이용해서 대응하는 OGR StringList, IntegerList, Integer64List 및 RealList 유형을 매핑합니다. 그 다음 필드값을 적절한 CSV 이스케이프 처리를 한 JSon 배열로 인코딩합니다.

SQLite 데이터베이스는 잠금(locking)을 제대로 지원하지 않기 때문에 NFS 또는 다른 몇몇 네트워크 기반 파일 시스템 프로토콜 상에서 잘 작동하지 않는 경우가 많습니다. SQLite 파일은 로컬 시스템의 실제 디스크 상에서만 작업하는 편이 가장 안전합니다.

SQLite은 드라이버에 선택적으로 컴파일됩니다. 기본적으로 컴파일되지 않습니다.

기본적으로 SQLite 데이터베이스 엔진에 SQL 선언문을 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 드라이버가 SQL 문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

:decl_configoption:`OGR_SQLITE_SYNCHRONOUS` 환경설정 옵션이 추가되었습니다. 이 옵션을 OFF로 설정하면, SQLite 데이터베이스에 'PRAGMA synchronous = OFF' 명령어를 발행합니다. 이렇게 하면 일부 (예: EXT4 파일 시스템 상에) 쓰기 작업의 속도를 향상시킬 수 있지만, 시스템/OS 크래시와 관련된 데이터 보안 문제가 생길 수도 있습니다. 따라서 상품 생산 환경에서 이 옵션을 조심해서 사용해야 합니다. SQLite `관련 문서 <http://www.sqlite.org/pragma.html#pragma_synchronous>`_ 를 읽어보십시오.

:decl_configoption:`OGR_SQLITE_PRAGMA` 환경설정 옵션으로 어떤 SQLite `PRAGMA 선언문 <http://www.sqlite.org/pragma.html>`_ 이든 지정할 수 있습니다. 그 문법은 다음과 같습니다:

::

   OGR_SQLITE_PRAGMA = "pragma_name=pragma_value[,pragma_name2=pragma_value2]*"

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

"정규" SQLite 데이터베이스
--------------------------

이 드라이버는 OGC 단순 피처(Simple Feature) 표준을 느슨하게 따라 정의된, 그 중에서도 `FDO RFC 16 <http://trac.osgeo.org/fdo/wiki/FDORfc16>`_ 에 정의된 대로 설계된 'geometry_columns' 테이블을 검색합니다. 이 테이블이 있는 경우 이를 사용해서 테이블을 레이어와 매핑합니다.

'geometry_columns' 테이블이 없는 경우, 각 테이블을 레이어로 취급합니다. WKT_GEOMETRY 필드를 가진 레이어를 공간 테이블로 취급하고, WKT_GEOMETRY 열을 WKT(Well Known Text) 도형으로 읽어올 것입니다.

'geometry_columns' 테이블이 있는 경우, 이 테이블을 사용해서 'spatial_ref_sys' 테이블에 있는 공간 좌표계를 검색할 것입니다.

SQLite 드라이버가 레코드로부터 공간 데이터 읽기를 지원하긴 하지만, 공간 색인 작업은 지원하지 않기 때문에 공간 쿼리가 느린 편입니다. (공간 쿼리는 SpatiaLite를 이용하십시오.) 속성 쿼리는 -- 특히 "CREATE INDEX ON ( )" SQL 명령어를 사용해서 적절한 속성 열에 대해 색인을 작성한 경우 -- 빠를 수도 있습니다.

이 드라이버는 다음 비선형 도형 유형들도 읽고 쓸 수 있습니다:

   -  CIRCULARSTRING
   -  COMPOUNDCURVE
   -  CURVEPOLYGON
   -  MULTICURVE
   -  MULTISURFACE

주의: 현재 SpatiaLite 버전은 이 도형 유형들을 지원하지 않기 때문에, SpatiaLite 데이터베이스를 사용하는 경우 이 도형 유형들을 읽고 쓸 수 없습니다.

도형 열을 여러 개 가진 테이블
-------------------------------------

:ref:`rfc-41` 에서 설명하는 새 API를 따라 도형 열을 여러 개 가진 레이어를 생성, 수정하고 읽어올 수 있습니다.

REGEXP 연산자
---------------

기본적으로 REGEXP 연산자는 SQLite에 구현되지 않았습니다. OGR를 PCRE 라이브러리를 대상으로 빌드하면, OGR가 실행하는 SQL 선언문에 REGEXP 연산자를 사용할 수 있습니다.

SpatiaLite 라이브러리 (SQLite 용 공간 확장 사양) 사용하기
-----------------------------------------------------------

SQLite 드라이버는 SpatiaLite 데이터베이스를 읽고 쓸 수 있습니다. SpatiaLite 데이터베이스 생성 또는 업데이트는 SpatiaLite 라이브러리(2.3.1 이상 버전)에 대한 명확한 링크 작업을 필요로 합니다. SpatiaLite 라이브러리에 대해 명확한 링크 작업을 하면 이 라이브러리가 제공하는 공간 색인, 공간 함수 등등 같은 기능도 사용할 수 있습니다.

다음은 몇몇 예시입니다:

::

   # SpatiaLite가 제공하는 샘플 데이터베이스를 복제하기
   ogr2ogr -f SQLite testspatialite.sqlite test-2.3.sqlite  -dsco SPATIALITE=YES

   # 공간 필터로 요청하기. 공간 색인이 생성되어 있고 SpatiaLite 라이브러리에
   # 대해 명확한 링크 작업을 한 경우 더 빨리 작동할 것입니다.
   ogrinfo testspatialite.sqlite Towns -spat 754000 4692000 770000 4924000

'VirtualShape:'으로 열기
----------------------------

(SpatiaLite 지원 필수)

SpatiaLite으로 shapefile을 실시간(on-the-fly)으로 VirtualShape으로서 열 수 있습니다. 데이터소스에 대해 사용하는 문법은 다음과 같습니다:

::

   VirtualShape:/path/to/shapefile.shp

이때 shapefile이 "실제" 파일이어야만 합니다.

이렇게 하면 SpatiaLite의 공간 연산을 사용할 수 있는 케이퍼빌리티를 얻을 수 있습니다.
(가상 테이블에 공간 색인을 사용할 수 없다는 사실을 기억하십시오.)

SQLite SQL 방언
----------------------

:ref:`sql_sqlite_dialect` 을 사용하는 경우 SQLite SQL 엔진을 이용해서 어떤 OGR 데이터소스에도 SQL 쿼리를 실행할 수 있습니다.

VirtualOGR SQLite 확장 사양
-------------------------------

GDAL/OGR 라이브러리를 `SQLite 확장 사양 <http://www.sqlite.org/lang_corefunc.html#load_extension>`_ 으로 불러올 수 있습니다. "load_extension(gdal_library_name)" SQL 함수로 이 확장 사양을 불러옵니다. 이때 'gdal_library_name'은 일반적으로 유닉스/리눅스의 경우 libgdal.so, 윈도우의 경우 gdal110.dll, 등등입니다.

이 확장 사양을 불러온 다음, OGR 레이어에 대응하는 가상 테이블을 다음 SQL 선언문 가운데 하나로 생성할 수 있습니다:

::

   CREATE VIRTUAL TABLE table_name USING VirtualOGR(datasource_name);
   CREATE VIRTUAL TABLE table_name USING VirtualOGR(datasource_name, update_mode);
   CREATE VIRTUAL TABLE table_name USING VirtualOGR(datasource_name, update_mode, layer_name);
   CREATE VIRTUAL TABLE table_name USING VirtualOGR(datasource_name, update_mode, layer_name, expose_ogr_style);

이때:

-  'datasource_name':
   어떤 OGR 데이터소스든 가리키는 연결 문자열입니다..

-  'update_mode =':
   (기본값) 0은 읽기 전용 모드, 1은 업데이트 모드입니다.

-  'layer_name =':
   열린 데이터소스의 레이어 이름입니다.

-  'expose_ogr_style =':
   (기본값) 0은 OGR_STYLE 특수 필드를 출력하지 않고, 1은 노출시킵니다.

주의: 데이터소스가 단일 레이어 하나만 가지고 있는 경우 'layer_name'을 지정할 필요는 없습니다.

SQLite3 콘솔에서는, 일반적으로 다음과 같이 사용합니다:

::

   sqlite> SELECT load_extension('libgdal.so');

   sqlite> SELECT load_extension('mod_spatialite.so');

   sqlite> CREATE VIRTUAL TABLE poly USING VirtualOGR('poly.shp');

   sqlite> SELECT *, ST_Area(GEOMETRY) FROM POLY;
   215229.266|168.0|35043411||215229.265625
   247328.172|179.0|35043423||247328.171875
   261752.781|171.0|35043414||261752.78125
   547597.188|173.0|35043416||547597.2109375
   15775.758|172.0|35043415||15775.7578125
   101429.977|169.0|35043412||101429.9765625
   268597.625|166.0|35043409||268597.625
   1634833.375|158.0|35043369||1634833.390625
   596610.313|165.0|35043408||596610.3359375
   5268.813|170.0|35043413||5268.8125

뿐만 아니라, ``ogr_datasource_load_layers(datasource_name[, update_mode[, prefix]])`` 함수를 사용해서 데이터소스의 모든 레이어를 자동으로 불러올 수도 있습니다:

::

   sqlite> SELECT load_extension('libgdal.so');

   sqlite> SELECT load_extension('mod_spatialite.so');

   sqlite> SELECT ogr_datasource_load_layers('poly.shp');
   1
   sqlite> SELECT * FROM sqlite_master;
   table|poly|poly|0|CREATE VIRTUAL TABLE "poly" USING VirtualOGR('poly.shp', 0, 'poly')

VirtualOGR 테이블의 케이퍼빌리티의 개요에 대해서는 :ref:`sql_sqlite_dialect` 을 참조하십시오.

생성 문제점
---------------

SQLite 드라이버는 새 SQLite 데이터베이스 파일 생성하기, 또는 기존 SQLite 데이터베이스 파일에 테이블 추가하기를 지원합니다.

트랜잭션 지원
~~~~~~~~~~~~~~~~~~~

이 드라이버는 :ref:`rfc-54` 별로 데이터베이스 구준에서 트랜잭션을 구현합니다.

데이터셋 열기 옵션
~~~~~~~~~~~~~~~~~~~~

-  **LIST_ALL_TABLES=YES/NO**:
   비공간 테이블을 포함해서 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다.

-  **LIST_VIRTUAL_OGR=YES/NO**:
   VirtualOGR 가상 테이블을 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다. 잠재적인 보안 문제를 피하려면 신뢰할 수 있는 데이터소스에 대해서만 이 옵션을 활성화해야 합니다.

-  **PRELUDE_STATEMENTS=string**: (GDAL 3.2 이상 버전)
   다른 어떤 SQL 선언문보다도 먼저 SQLite3 연결에 전송할 SQL 선언문(들)을 지정합니다. 선언문이 여러 개인 경우, 쌍반점(';') 기호로 구분해야만 합니다. 현재 데이터베이스에 `다른 데이터베이스를 추가 <https://www.sqlite.org/lang_attach.html>`_ 하고 크로스 데이터베이스 요청을 발행하는 데 이 옵션이 유용할 수도 있습니다.

   .. note::

      이때 다른 데이터베이스는 반드시 이 드라이버가 인식하는 유형이어야만 하기 때문에, 그 도형 블랍(blob)을 제대로 인식할 것입니다. (즉 일반적으로 지오패키지 데이터베이스는 아닙니다.)

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~~

-  **METADATA=YES/NO**:
   이 옵션을 이용해서 새 데이터베이스에 'geometry_columns' 및 'spatial_ref_sys' 테이블을 생성하지 않을 수 있습니다. 기본적으로는 새 데이터베이스를 생성할 때 이 메타데이터 테이블들을 생성합니다.

-  **SPATIALITE=YES/NO**:
   이 옵션을 YES로 설정하면 이 OGR SQLite 드라이버가 사용하는 메타데이터와 그리고 OGC 사양과도 조금 다른 SpatiaLite 계열 메타데이터 테이블을 생성합니다. METADATA=YES인 경우에만 사용할 수 있습니다.

   -  기억하십시오: SpatiaLite에 대한 삽입/쓰기 지원을 위해, OGR가 반드시 *libspatialite* 라이브러리에 링크되어 있어야만 합니다. 그렇지 않다면 *읽기 전용* 모드가 강제됩니다. 제대로 된 라이브러리 지원을 건너뛰고 SpatiaLite에 삽입/쓰기 시도를 하는 경우 그냥 망가진 (오류가 발생하는) 데이터베이스 파일을 생성할 것입니다.

   -  주의 사항: 기저 *libspatialite* 라이브러리가 2.3.1 또는 그 이전 버전인 경우 모든 도형을 2차원 [XY]로 생성할 것입니다. 단순히 이 라이브러리의 이전 버전들이 2차원 [XY] 파원을 지원할 수 있기 때문입니다. 2.5차원 [XYZ]를 지원하기 위해서는 2.4.0 이상 버전이 필요합니다.

-  **INIT_WITH_EPSG=YES/NO**:
   이 옵션을 YES로 설정하면 'spatial_ref_sys' 테이블에 EPSG CSV 파일의 내용을 삽입합니다.
   정규 SQLite 데이터베이스의 경우 기본값은 NO입니다.

   -  주의 사항: SPATIALITE=YES이고 기저 *libspatialite* 라이브러리가 2.4 또는 3.X버전인 경우 이 옵션을 무시합니다. 이 라이브러리 버전들은 새 데이터베이스 생성 시 무조건 (*self-initialization*) 'spatial_ref_sys' 테이블에 EPSG 데이터셋을 불러올 것입니다. *libspatialite* 라이브러리 4.0버전부터 이 옵션의 기본값은 YES이지만 NO로 설정할 수 있게 되었습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **FORMAT=WKB/WKT/SPATIALITE**:
   도형 열에 사용되는 포맷을 제어합니다. 기본값은 WKB(Well Known Binary)입니다. WKB가 일반적으로 공간 및 처리 과정에 있어 좀 더 효율적이지만, 단순한 응용 프로그램에서 검사 또는 사용하기에는 WKT(Well Known Text)보다 어렵습니다. SpatiaLite 확장 사양은 자체 바이너리 포맷을 사용해서 도형을 저장하기 때문에 SPATIALITE를 선택해도 됩니다.
   SpatiaLite 데이터베이스를 열었거나 SPATIALITE 데이터셋 생성 옵션을 YES로 설정해서 생성한 경우 자동적으로 SPATIALITE를 선택할 것입니다.

-  **GEOMETRY_NAME**:
   OGR는 기본적으로 새 테이블을 GEOMETRY(또는 FORMAT=WKT인 경우 WKT_GEOMETRY)라는 도형 열과 함께 생성합니다. 다른 이름을 사용하고자 하는 경우, 이 레이어 생성 옵션으로 지정할 수 있습니다.

-  **LAUNDER=YES/NO**:
   새 레이어 및 필드의 이름을 SQLite와 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "'", "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. 기본값은 YES입니다.

-  **SPATIAL_INDEX=YES/NO**:
   데이터베이스가 SpatiaLite 계열이고 OGR가 *libspatialite* 라이브러리에 링크되어 있는 경우, 이 옵션을 사용해서 공간 색인을 생성해야만 하는지 여부를 선택할 수 있습니다. 기본값은 YES입니다.

-  **COMPRESS_GEOM=YES/NO**:
   도형 블랍의 포맷이 SpatiaLite 계열인 경우, 이 옵션을 사용해서 (LINESTRING, POLYGON) 도형에 압축 포맷을 사용해야만 하는지 여부를 선택할 수 있습니다. SpatiaLite 2.4 이상 버전이 압축 포맷을 인식합니다. 기본값은 NO입니다.
   주의: 기존 SpatiaLite 데이터베이스를 업데이트하는 경우, :decl_configoption:`COMPRESS_GEOM` 환경설정 옵션을 사용해서 추가한/덮어쓴 객체에 대해 비슷한 결과를 내도록 설정할 수 있습니다.

-  **SRID=srid**:
   레이어과 관련된 공간 좌표계의 SRID 번호를 강제로 사용하도록 합니다. 이 옵션을 지정하지 않았는데 레이어와 관련된 공간 좌표계가 존재하는 경우, 'spatial_ref_sys' 테이블을 검색해서 해당 공간 좌표계와 일치하는 항목을 찾습니다. 일치하는 항목이 없다면 'spatial_ref_sys' 테이블에 해당 공간 좌표계를 위한 새 항목을 삽입합니다.
   이 옵션을 지정하는 경우, 검색하지 않습니다. (즉 새 항목을 삽입하지도 않습니다.) 지정한 공간 좌표계를 그대로 사용할 것입니다.

-  **COMPRESS_COLUMNS=column_name1[,column_name2, ...]**:
   ZLib DEFLATE 알고리즘으로 압축해야만 하는 (문자열) 열 목록을 지정합니다. 대용량 문자열 블랍을 가진 데이터베이스의 경우 혜택을 볼 수도 있습니다. 하지만, 다른 SQLite 유틸리티들이 (또는 OGR 이전 버전들이) 이런 열의 값을 압축 바이너리 콘텐츠로 읽기 때문에 조심해서 사용하십시오.
   OGR를 사용하는 경우, 압축 열 삽입, 수정 또는 쿼리 작업 시 압축/압축 해제 과정이 투명하게 이루어집니다. 하지만 이런 열을 속성 필터 또는 WHERE 절로 (쉽게) 쿼리할 수는 없습니다.
   주의: 테이블 정의에서 이런 열은 "VARCHAR_deflate" 선언 유형을 가집니다.

-  **FID=fid_name**:
   생성할 FID 열의 이름을 지정합니다. 기본값은 'OGC_FID'입니다.

-  **STRICT=YES/NO**: (SQLite 3.37 이상 그리고 GDAL 3.35 이상 버전)
   기본값은 NO입니다.
   테이블을 `엄격 테이블(strict table) <https://sqlite.org/stricttables.html>`_ 로 생성해야 할지 여부를 선택합니다. 엄격 테이블이란 열 유형 확인 작업을 엄격하게 한다는 의미입니다. OGR만을 통해 작업하는 경우 유형이 지정된 열을 가지기 때문에 일반적으로 큰 영향을 미치지 않지만, 데이터베이스가 외부 도구로 편집될 수도 있는 경우 데이터베이스 무결성을 강화하는 데 도움이 될 수 있습니다.
   STRICT 테이블을 담고 있는 데이터베이스는 SQLite 3.37 이상 버전만이 읽을 수 있다는 사실을 기억하십시오. STRICT 모드에서는 Integer, Integer64, Real, String, DateTime, Date 및 Time 열 데이터 유형을 지원합니다. STRICT 모드에서는 COMPRESS_COLUMNS 옵션을 무시합니다.

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`SQLITE_LIST_ALL_TABLES` =YES/NO:
   ('geometry_columns' 테이블에 목록화된 테이블만이 아니라) 모든 테이블을 목록화하려면 이 옵션을 YES로 설정하십시오. LIST_ALL_TABLES 열기 옵션을 사용해도 모든 테이블을 목록화할 수 있습니다. 기본값은 NO입니다.

-  :decl_configoption:`OGR_SQLITE_LIST_VIRTUAL_OGR` =YES/NO:
   VirtualOGR 레이어를 목록화하려면 이 옵션을 YES로 설정하십시오.
   사용자가 제공받은 파일에 가상 OGR 테이블이 존재한다는 사실을 모를 수도 있다는 보안 문제가 있을 수도 있기 때문에 기본값은 NO입니다.

-  :decl_configoption:`OGR_SQLITE_JOURNAL`:
   이 옵션을 사용해서 SQLite 파일의 저널 모드를 설정할 수 있습니다.
   https://www.sqlite.org/pragma.html#pragma_journal_mode 도 읽어보십시오.

-  :decl_configoption:`OGR_SQLITE_CACHE`:
   :ref:`성능 힌트 <target_drivers_vector_sqlite_performance_hints>` 를 참조하십시오.

-  :decl_configoption:`OGR_SQLITE_SYNCHRONOUS`:
   :ref:`성능 힌트 <target_drivers_vector_sqlite_performance_hints>` 를 참조하십시오.

-  :decl_configoption:`OGR_SQLITE_LOAD_EXTENSIONS` =extension1,...,extensionN,ENABLE_SQL_LOAD_EXTENSION: (GDAL 3.5.0 이상 버전)
   데이터베이스를 열 때 불러올 확장 사양을 담고 있는 공유 라이브러리들의 이름을 쉼표로 구분한 목록을 지정합니다. 파일을 직접 불러올 수 없는 경우, 다양한 운영 체제 특화 확장 사양을 추가로 불러오려 시도합니다. 즉 예를 들어 "samplelib"을 불러오지 못 하는 경우 "samplelib.so" 또는 "samplelib.dylib" 또는 "samplelib.dll" 같은 이름들을 시도할 수도 있습니다.
   특수값 ``ENABLE_SQL_LOAD_EXTENSION`` 을 이용해서 SQL ``load_extension()`` 함수를 이용할 수 있습니다. 이 함수는 SQLite3 표준 빌드에서 일반적으로 비활성화되어 있습니다.
   확장 사양을 신뢰할 수 없는 경우 확장 사양을 불러오는 것이 잠재적인 보안 위협이 될 수 있습니다.

-  :decl_configoption:`OGR_SQLITE_PRAGMA`:
   이 옵션을 이용하면 어떤 SQLite `PRAGMA 선언문 <http://www.sqlite.org/pragma.html>`_ 이든 지정할 수 있습니다. 문법은 다음과 같습니다.
   
::

   OGR_SQLITE_PRAGMA = "pragma_name=pragma_value[,pragma_name2=pragma_value2]*"

-  :decl_configoption:`SQLITE_USE_OGR_VFS`:
   이 옵션을 YES로 설정하면 GDAL/OGR I/O 레이어가 추가적인 버퍼/캐시 작업을 사용할 수 있고, I/O 속도도 향상시킬 수 있습니다. 더 자세한 정보는 :ref:`성능 힌트 <target_user_virtual_file_systems_file_caching>` 를 참조하십시오.
   이 옵션을 활성화한 경우 어떤 파일도 잠그지 않기 때문에 동시 편집 시 데이터베이스에 오류가 발생할 수도 있다는 사실을 주의하십시오.

.. _target_drivers_vector_sqlite_performance_hints:

성능 힌트
-----------------

SQLite는 트랜잭션이 가능한 DBMS입니다. 많은 INSERT 문이 가까운 순서로 실행되는 반면, 최적 성능을 내려면 BEGIN TRANSACTION 및 COMMIT TRANSACTION 문을 (OGR_L_StartTransaction() 및 OGR_L_CommitTransaction() 메소드로) 적절하게 호출해야 합니다.
기본적으로 아무 트랜잭션도 명확하게 시작하지 않는 경우 SQLite는 모든 선언문에 대해 자동 커밋하기 때문에 아주 느릴 것입니다. ogr2ogr 유틸리티를 사용하는 경우 기본 습성은 삽입 행 20,000개마다 트랜잭션을 COMMIT하는 것입니다. '**-gt**' 옵션을 이용해서 각 트랜잭션에 들어갈 행의 개수를 명확하게 설정할 수 있습니다. 이 옵션의 값을 '**-gt 65536**' 또는 그 이상으로 늘리면 수십만 또는 수백만 개의 행을 담고 있는 일부 테이블을 채우는 동안 최적 성능을 낼 수 있습니다.

SQLite는 보통 아주 최소한의 메모리 공간을 차지합니다. 내부 페이지 캐시를 저장하기 위해 약 20MB(겨우 2,000페이지 정도)의 RAM을 예약하고 있습니다. 많은 상황에서 이 값이 충분하지 않을 수 있습니다. 대응하는 공간 색인과 연결된 수많은 테이블을 담고 있는 대용량 데이터베이스 파일에 접근하는 경우 특히 그렇습니다. 내부 페이지 캐시 용량을 훨씬 후하게 설정하면 성능이 눈에 띄게 향상될 수도 있습니다. :decl_configoption:`OGR_SQLITE_CACHE` 환경설정 옵션의 (MB 단위) 값을 이용해서 내부 페이지 캐시 용량을 명확하게 설정할 수 있습니다. 사용자의 하드웨어에서 사용할 수 있는 RAM이 충분한 경우, 캐시 용량을 512MB만큼 (또는 1,024MB까지도) 정의하면 성능을 향상시키는 데 많은 도움이 될 수도 있습니다.

SQLite 데이터베이스 생성 시 :decl_configoption:`OGR_SQLITE_SYNCHRONOUS` 환경설정 옵션을 OFF로 설정하면 (중단/크래시의 경우 데이터베이스 무결성이 망가질 가능성이 있지만) 성능이 향상될 수도 있습니다.

동일 SpatiaLite 테이블에 많은 소스 파일을 수집하는 경우, '-lco SPATIAL_INDEX=NO' 옵션을 사용해서 공간 색인 없이 테이블을 초기화하고 모든 데이터를 추가한 다음 다른 명령어로 공간 색인을 생성하면 속도가 훨씬 빠릅니다. 다음과 같은 ogrinfo 명령어로 공간 색인을 생성할 수 있습니다:

::

   ogr2ogr -f SQLite -dsco SPATIALITE=YES db.sqlite first.shp -nln the_table -lco SPATIAL_INDEX=NO
   ogr2ogr -append db.sqlite second.shp -nln the_table
   ...
   ogr2ogr -append db.sqlite last.shp -nln the_table
   ogrinfo db.sqlite -sql "SELECT CreateSpatialIndex('the_table','GEOMETRY')"

데이터베이스를 편집한 경우, 다음과 같이 `VACUUM <https://sqlite.org/lang_vacuum.html>`_ 쿼리를 실행해서 데이터베이스를 컴팩트하게 최적화하는 것이 유용할 수도 있습니다:

::

   ogrinfo db.sqlite -sql "VACUUM"


예시
-------

- 비공간 SQLite 테이블을 지오패키지로 변환하기:

.. code-block::

  ogr2ogr \
    -f "GPKG" output.gpkg \
    input.sqlite \
    -sql \
    "SELECT
       *,
       MakePoint(longitude, latitude, 4326) AS geometry
     FROM
       my_table" \
    -nln "location" \
    -s_srs "EPSG:4326"

- SQLite와 SpatiaLite 두 데이터베이스를 결합(join)하기:

.. code-block::

    ogrinfo my_spatial.db \
        -sql "SELECT poly.id, other.foo FROM poly JOIN other_schema.other USING (id)" \
        -oo PRELUDE_STATEMENTS="ATTACH DATABASE 'other.db' AS other_schema"

감사의 말
-------

-  OGR SQLite 드라이버는 `DM 솔루션 그룹 <http://www.dmsolutions.ca/>`_ 및 `GoMOOS <http://www.gomoos.org/>`_ 의 지원으로 개발되었습니다.
-  \A. 푸리에리(A. Furieri)가 `이탈리아 토스카나 주 <http://www.regione.toscana.it/>`_ 의 재정 지원을 받아 완전한 SpatiaLite 지원을 구현했습니다.

링크
-----

-  `주 SQLite 페이지 <http://www.sqlite.org/>`_
-  `SQLite의 SpatiaLite 확장 사양 <https://www.gaia-gis.it/fossil/libspatialite/index>`_
-  `FDO RFC 16 <http://trac.osgeo.org/fdo/wiki/FDORfc16>`_: SQLite 용 FDO 제공자
-  :ref:`RasterLite2 <raster.rasterlite2>` 드라이버

