.. _vector.pgdump:

PostgreSQL SQL 덤프
===================

.. shortname:: PGDump

.. built_in_by_default::

이 쓰기 전용 드라이버는 나중에 활성화된 PostgreSQL 인스턴스로 인젝션할 수 있는 SQL 덤프 파일의 생성 지원을 구현합니다. 이 드라이버는 `PostGIS <http://postgis.net/>`_ 도형으로 확장된 PostgreSQL을 지원합니다.

이 드라이버는 PostGIS shp2pgsql 유틸리티와 매우 유사합니다.

PGDump 드라이버는 정규 PostgreSQL 드라이버와 생성 옵션 대부분을 공유합니다.

PGDump 드라이버는 PostGIS 도형 열을 여러 개 가진 테이블을 (:ref:`rfc-41` 에 따라) 생성할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 옵션
----------------

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

-  **LINEFORMAT**:
   기본적으로 파일을 생성할 때 로컬 플랫폼의 새줄 문자 규범으로 (win32에서는 CR/LF로 또는 다른 모든 시스템에서는 LF로) 생성합니다. **CRLF** (도스 서식) 또는 **LF** (유닉스 서식) 값을 가질 수 있는 LINEFORMAT 레이어 생성 옵션을 이용하면 이 기본 습성을 대체할 수 있습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **GEOM_TYPE**:
   "geometry" 또는 (PostGIS 1.5버전부터) "geography" 가운데 하나로 설정해서 테이블의 도형 유형을 강제할 수 있습니다. 기본값은 "geometry"입니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 PostgreSQL과 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. NO로 설정하면 이름을 그대로 보전합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

-  **PRECISION**:
   해당 레이어에 생성되는 새 필드가 -- 사용할 수 있는 경우 NUMERIC(길이, 정밀도) 또는 CHAR(길이) 유형을 사용해서 -- 길이 및 정밀도 정보를 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다. NO로 설정하면 그 대신 FLOAT8, INTEGER 및 VARCHAR 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **DIM={2,3,XYM,XYZM}**:
   레이어의 차원을 제어합니다. PostGIS 1.0 이상 버전에서 데이터를 불러오는 도중 도형 차원에 제약 조건이 적용되기 때문에, 2차원 레이어의 경우 이 옵션을 2로 설정하는 것이 중요합니다.

-  **GEOMETRY_NAME**:
   새 테이블의 도형 열 이름을 설정합니다. 지정하지 않으면 GEOM_TYPE=geometry인 경우 *wkb_geometry* 를, GEOM_TYPE=geography인 경우 *the_geog* 를 기본값으로 사용합니다.

-  **SCHEMA**:
   새 테이블에 대한 스키마의 이름을 설정합니다. 서로 다른 스키마에 동일한 레이어 이름을 사용할 수 있지만, 공개(public) 스키마 및 기타 스키마에서는 사용할 수 없습니다.

-  **CREATE_SCHEMA**:
   SCHEMA 옵션과 함께 사용해야 합니다. CREATE SCHEMA 지침을 전송하도록 기본값은 ON입니다. OFF로 설정하면 CREATE SCHEMA 지침을 전송하지 않습니다.

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

-  **WRITE_EWKT_GEOM**:
   기본값은 OFF입니다. ON으로 설정하면 HEX 도형 대신 EWKT 도형을 작성합니다. PG_USE_COPY 환경 변수가 YES로 설정된 경우 이 옵션은 아무 영향도 미치지 않을 것입니다.

-  **CREATE_TABLE**:
   필요한 경우 테이블을 재생성하도록 기본값은 ON입니다. OFF로 설정하면 테이블 재생성을 비활성화시키고 기존 테이블 구조를 사용합니다.

-  **DROP_TABLE**\ =ON/OFF/IF_EXISTS:
   기본값은 IF_EXISTS입니다.
   ON으로 설정하면 테이블을 재생성하기 전에 삭제합니다.
   OFF로 설정하면 DROP TABLE을 전송하지 않습니다.
   IF_EXISTS로 설정하면 DROP TABLE IF EXISTS를 전송합니다. (PostgreSQL 8.2 이상 버전 필요)

-  **SRID**:
   도형의 SRID를 설정합니다. 공간 좌표계가 레이어와 연관되어 있지 않는 이상 기본값은 -1입니다. 공간 좌표계가 레이어와 연관되어 있는 경우, EPSG 코드가 언급되었다면 해당 EPSG 코드를 SRID로 사용할 것입니다. (주의: spatial_ref_sys 테이블을 지정한 SRID로 정확하게 채워야만 합니다.)

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

-  **POSTGIS_VERSION**:
   GDAL 3.2버전부터 기본값은 2.2입니다. (이전 버전들에서는 1.5였습니다.) 1.5, 2.0 또는 2.2 가운데 하나로 설정할 수 있습니다. PostGIS 2.0버전은 비선형 도형 유형을 다르게 인코딩합니다. 그리고 2.2버전은 POINT EMPTY 도형에 대한 특수 처리 방식을 도입했습니다.

-  **DESCRIPTION**: (GDAL 2.1버전부터)
   pg_description 시스템 테이블에 들어갈 설명 문자열입니다. ``SetMetadataItem("DESCRIPTION", description_string)`` 메소드로도 설명을 작성할 수 있습니다. ogr2ogr 유틸리티는 '-nomd' 옵션을 사용하지 않는 이상 기본적으로 설명을 보전합니다.

환경 변수
~~~~~~~~~~~~~~~~~~~~~

-  **PG_USE_COPY**:
   PostgreSQL에 데이터를 삽입할 때 COPY를 사용하려면 이 옵션을 YES로 설정할 수도 있습니다. COPY가 INSERT보다 훨씬 더 빠릅니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ , /vsigzip/ 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

예시
----

-  shapefile을 PostgreSQL로 인젝션할 수 있는 abc.sql 덤프 파일로 단순 변환합니다. abc.shp 파일의 객체와 abc.dbf 파일의 속성으로 'abc' 테이블을 생성할 것입니다. SRID를 지정합니다. 성능을 향상시키기 위해 PG_USE_COPY 환경 변수를 YES로 설정합니다:

   ::

      ogr2ogr --config PG_USE_COPY YES -f PGDump abc.sql abc.shp -lco SRID=32631

-  PGDump 드라이버의 산출물을 psql 유틸리티로 넘깁니다:

   ::

      ogr2ogr --config PG_USE_COPY YES -f PGDump /vsistdout/ abc.shp | psql -d my_dbname -f -

참고
----

-  :ref:`OGR PostgreSQL <vector.pg>` 드라이버
-  `PostgreSQL 홈페이지 <http://www.postgresql.org/>`_
-  `PostGIS <http://postgis.net/>`_
-  `PostGIS / OGR 위키 예제 페이지 <http://trac.osgeo.org/postgis/wiki/UsersWikiOGR>`_

