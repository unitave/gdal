.. _vector.gpkg:

GPKG -- 지오패키지 벡터
=========================

.. shortname:: GPKG

.. build_dependencies:: libsqlite3

이 드라이버는 `OGC 지오패키지(GeoPackage) 포맷 표준 <http://www.opengeospatial.org/standards/geopackage>`_ 공간 테이블에 접근 지원을 구현합니다. 지오패키지 표준은 SQLite 데이터베이스 파일을 일반 컨테이너로 사용하며, 다음을 정의하고 있습니다:

-  예상 메타데이터 테이블 (``gpkg_contents``, ``gpkg_spatial_ref_sys``, ``gpkg_geometry_columns``)
-  공간 테이블에 있는 도형을 위한 바이너리 포맷 인코딩 (기본적으로 ISO 표준 WKB(Well-Known Binary)를 준수하는 GPKG 표준 헤더 객체)
-  확장자 명명 및 규범(확장 객체 유형) 및 색인(상호운용적인 방식으로 SQLite R-트리를 사용하는 방법)

이 드라이버는 파일 시스템에서 SQLite 파일을 읽고 쓰기 때문에, 작업 파일에 읽기/쓰기 접근 권한을 가진 사용자가 이 드라이버를 실행해야만 합니다.

이 드라이버는 다음 비선형 도형 유형들도 읽고 쓸 수 있습니다:

   -  CIRCULARSTRING
   -  COMPOUNDCURVE
   -  CURVEPOLYGON
   -  MULTICURVE
   -  MULTISURFACE

지오패키지 래스터/타일도 지원합니다. :ref:`지오패키지 래스터 <raster.gpkg>` 문서도 읽어보십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

사양 버전
---------------------

GDAL 2.2버전부터, 이 드라이버는 1.0/1.0.1, 1.1 또는 1.2버전을 준수하는 지오패키지 데이터베이스를 생성할 수 있습니다. GDAL 2.2버전의 경우, 이 드라이버는 지오패키지가 사용하는 객체가 요구하는 최저 버전으로 자동 조정할 것입니다. GDAL 2.3 이상 버전의 경우, 기본값 1.2버전을 사용할 것입니다. VERSION 데이터셋 생성 옵션을 지정하면 버전을 명확하게 선택할 수 있습니다.

제한 사항
-----------

-  지오패키지는 테이블 하나 당 도형 열 하나만 지원합니다.

SQL
---

이 드라이버는 OGR 속성 필터를 지원하며, 사용자가 SQLite 방언으로 필터를 지정할 것을 기대합니다. 필터가 데이터베이스를 대상으로 직접 실행될 것이기 때문입니다.

ExecuteSQL()로 전송되는 SQL SELECT 문도 데이터베이스를 대상으로 직접 실행됩니다. Spatialite를 사용하는 경우, 지오패키지 도형을 Spatialite 도형으로 변환하려면 Spatialite 최신 버전(4.2.0)과 명확한 캐스트 연산자 AsGPB()를 사용해야 합니다. (GPKG 드라이버는 Spatialite 도형을 자동으로 역변환할 것입니다.) "INDIRECT_SQLITE" 방언을 지정하면 -- 비록 느리긴 하지만 -- 다른 Spatialite 버전도 사용할 수 있습니다. 이 경우 지오패키지 도형은 OGR가 변환한 이후 자동적으로 Spatialite 도형으로 나타납니다.

GDAL 2.2버전부터, "DROP TABLE layer_name" 및 "ALTER TABLE layer_name RENAME TO new_layer" 선언문을 사용할 수 있습니다. 이 선언문들은 지오패키지 시스템 테이블을 업데이트할 것입니다.

GDAL 2.2버전부터, 테이블이 명명된 도형 열에 대한 공간 색인을 가지고 있는지 확인하기 위해 "HasSpatialIndex('table_name','geom_col_name')" 선언문을 사용할 수 있습니다.

테이블을 삭제(drop)하거나 테이블로부터 레코드를 제거하는 경우, 테이블 또는 레코드가 차지하고 있던 공간을 즉시 해제하지 않고 SQLite가 나중에 다시 사용할 수도 있는 파일 페이지 풀에 유지합니다. 파일을 최소 용량으로 줄여야 한다면 "VACUUM" SQL 요청을 명확하게 전송해야 합니다. 이 요청은 전체 파일을 다시 작성할 것이라는 사실을 기억하십시오.

SQL 함수
~~~~~~~~~~~~~

지오패키지 사양에 있는 다음 SQL 함수들을 사용할 수 있습니다:

-  ST_MinX(geom *Geometry*): 도형의 최소 X 좌표를 반환합니다.
-  ST_MinY(geom *Geometry*): 도형의 최소 Y 좌표를 반환합니다.
-  ST_MaxX(geom *Geometry*): 도형의 최대 X 좌표를 반환합니다.
-  ST_MaxY(geom *Geometry*): 도형의 최대 Y 좌표를 반환합니다.
-  ST_IsEmpty(geom *Geometry*): 비어 있는 (그러나 NULL은 아닌) 도형인 경우 1을 반환합니다. 예: POINT EMPTY 도형
-  ST_GeometryType(geom *Geometry*): 'POINT', 'LINESTRING', 'POLYGON', 'MULTIPOLYGON', 'MULTILINESTRING', 'MULTIPOINT', 'GEOMETRYCOLLECTION' 도형 유형을 반환합니다.
-  ST_SRID(geom *Geometry*): 도형의 SRID를 반환합니다.
-  GPKG_IsAssignable(expected_geom_type *String*, actual_geom_type *String*): 주로 '도형 유형 트리거 확장 사양(Geometry Type Triggers Extension)'에 필요합니다.

Spatialite에서와 동일한 문법과 의미를 가진 다음 함수들도 사용할 수 있습니다:

-  CreateSpatialIndex(table_name *String*, geom_column_name *String*):
   지정한 테이블/도형 열에 공간 색인(R-트리)을 생성합니다.
-  DisableSpatialIndex(table_name *String*, geom_column_name *String*):
   지정한 테이블/도형 열에 있는 공간 색인(R-트리)을 삭제(drop)합니다.
-  ST_Transform(geom *Geometry*, target_srs_id *Integer*):
   도형을 지정한 srs_id 공간 좌표계로 재투영합니다. gpkg_spatial_ref_sys에서 지정한 srs_id를 가진 공간 좌표계를 찾지 못 하는 경우, GDAL 3.2버전부터 srs_id를 EPSG 코드로 해석할 것입니다.

Spatialite과의 링크
~~~~~~~~~~~~~~~~~~~~

GPKG 드라이버를 Spatialite 4.2 이상 버전을 대상으로 컴파일하는 경우, Spatialite SQL 함수도 사용할 수 있습니다. 반드시 GPKG 도형 바이너리 인코딩을 Spatialite 도형 바이너리 인코딩으로 명확하게 변환해야만 합니다.

::

   ogrinfo poly.gpkg -sql "SELECT ST_Buffer(CastAutomagic(geom),5) FROM poly"

Spatialite 4.3버전부터, CastAutomagic이 더 이상 필요하지 않습니다.

트랜잭션 지원
-------------------

이 드라이버는 :ref:`rfc-54` 에 따라 데이터베이스 수준에서 트랜잭션을 구현합니다.

데이터셋 열기 옵션
------------------

다음 데이터셋 열기 옵션들을 사용할 수 있습니다:

-  **LIST_ALL_TABLES=AUTO/YES/NO**: (GDAL 2.2 이상 버전)
   모든 테이블을, gpkg_contents에 목록화되어 있지 않은 테이블도 포함해서 목록화해야 할지 여부를 선택합니다. 기본값은 AUTO입니다.
   AUTO로 설정하면, 비공간(aspatial) 확장 사양이 발견된 경우 또는 테이블이 gpkg_contents에 'attributes'로 등록되어 있는 경우를 제외하고 gpkg_contents에 목록화되어 있지 않은 테이블을 포함하는 모든 테이블을 목록화할 것입니다.
   YES로 설정하면, 어떤 경우에도 gpkg_contents에 목록화되어 있지 않은 테이블을 포함하는 모든 테이블을 목록화할 것입니다.
   NO로 설정하면, 'features', 'attributes' 또는 'aspatial'로 등록된 테이블만 목록화할 것입니다.

-  **PRELUDE_STATEMENTS=string**: (GDAL 3.2 이상 버전)
   SQL 문(들)을 다른 어떤 연결보다 먼저 SQLite3 연결로 전송합니다. SQL 문이 여러 개인 경우, 반드시 쌍반점(';') 기호로 구분해야만 합니다. 현재 데이터베이스에 `또다른 데이터베이스를 붙이고 <https://www.sqlite.org/lang_attach.html>`_ 크로스 데이터베이스 요청을 전송하려면 이 옵션이 유용할 수도 있습니다.

   .. note::

      추가된 데이터베이스의 도형 블랍(blob)을 제대로 인식하기 위해서는 추가된 데이터베이스도 지오패키지 데이터베이스여야만 합니다. (즉 일반적으로 Spatialite 데이터베이스는 아닙니다.)

-  **NOLOCK=YES/NO**: (GDAL 3.4.2 이상 버전)
   기본값은 NO입니다. 데이터베이스를 어떤 파일도 잠그지(lock) 않고 사용해야 할지 여부를 선택합니다.
   YES로 설정하면, 데이터베이스를 읽기전용 모드로 열었는데 저널(journal) 모드가 WAL이 아닌 경우에만 영향을 미칠 것입니다. https://www.sqlite.org/uri.html 에서 설명하고 있는 "nolock=1" 쿼리 파라미터와 동등합니다.

주의: 열기 옵션은 대부분의 OGR 유틸리티에서 일반적으로 "-oo name=value" 문법으로 또는 ``GDALOpenEx()`` API 호출로 지정됩니다.

주의: :decl_configoption:`OGR_SQLITE_JOURNAL` 환경설정 옵션을 사용해서 지오패키지의 (따라서 SQLite의) 저널 모드를 설정할 수도 있습니다. https://www.sqlite.org/pragma.html#pragma_journal_mode 도 참조하십시오.

생성 문제점
---------------

새 지오패키지 파일을 생성할 때, 이 드라이버는 데이터베이스의 텍스트 처리를 OGR 엄격 UTF-8 케이퍼빌리티를 만족시키는 UTF-8 모드로 강제하려 시도할 것입니다. 기존 파일의 경우 이 드라이버는 어떤 지정 인코딩이든 작업할 것입니다.

이 드라이버는 파일 생성 또는 수정 시 지오패키지의 ``last_change`` 타임스탬프를 업데이트합니다. 재현 가능성(reproducibility)을 위해 일관된 바이너리 산출물이 필요한 경우, :decl_configoption:`OGR_CURRENT_DATE` 전체 수준 환경설정 옵션을 설정하면 타임스탬프를 특정값으로 강제할 수 있습니다. 이 옵션을 설정할 때 지오패키지 표준이 -- 예를 들면 `1.2버전 <https://www.geopackage.org/spec120/#r15>`_ 이 -- 요구하는 특정한 시간 서식을 따르도록 주의하십시오.

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

다음과 같은 (벡터 특화 또는 래스터 공통) 생성 옵션들을 사용할 수 있습니다:

-  **VERSION=AUTO/1.0/1.1/1.2/1.3**: (GDAL 2.2 이상 버전)
   (application_id 및 user_version 필드를 위한) 지오패키지 버전을 설정합니다. AUTO 모드에서는, GDAL 2.3버전부터 기본값이 1.2입니다. GDAL 3.3버전부터는 1.3을 사용할 수 있습니다.

-  **ADD_GPKG_OGR_CONTENTS=YES/NO**: (GDAL 2.2 이상 버전)
   벡터 레이어의 객체 개수와 관련 트리거를 보전하기 위한 gpkg_ogr_contents 테이블을 추가할지 여부를 선택합니다. 기본값은 YES입니다.

-  **DATETIME_FORMAT=WITH_TZ/UTC**: (GDAL 3.2 이상 버전)
   데이터소스에 사용된 표준시간대(time zone)의 날짜&시간 값을 유지할지(WITH_TZ), 또는 날짜&시간 표현을 UTC(Coordinated Universal Time; 협정 세계시)로 변환할지 여부를 정의합니다. 기본값은 WITH_TZ입니다.
   지오패키지 1.3버전은 현재 지나치게 세세한 사항에 얽매여 UTC가 아닌 표준시간대를 지원하지 않습니다. (https://github.com/opengeospatial/geopackage/issues/530 를 참조하십시오.)
   표준시간대가 지정되지 않은 UTC 서식을 사용하는 경우, UTC로 가정할 것입니다.

래스터 용 다른 옵션들도 사용할 수 있습니다. :ref:`지오패키지 래스터 <raster.gpkg>` 드라이버 문서를 읽어보십시오.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

다음 레이어 생성 옵션들을 사용할 수 있습니다:

-  **GEOMETRY_NAME**:
   도형 열에 사용할 이름을 설정합니다. 기본값은 "geom"입니다.
   주의: GDAL 버전 2 이전 배포판에서 이 옵션은 GEOMETRY_COLUMN이었습니다.

-  **GEOMETRY_NULLABLE**:
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 해당 도형이 필수인 경우 NO로 설정하면 됩니다. 기본값은 YES입니다.

-  **FID**:
   OGR FID로 (SQLite 데이터베이스에서 기본 키(primary key)로) 사용할 열의 이름을 설정합니다. 기본값은 "fid"입니다.

-  **OVERWRITE**:
   생성할 레이어와 같은 이름인 기존 레이어를 생성할 레이어로 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다.

-  **SPATIAL_INDEX**:
   YES로 설정하면 해당 레이어 용 공간 색인을 생성할 것입니다. 기본값은 YES입니다.

-  **PRECISION**:
   TEXT(width) 유형을 사용할 수 있는 경우, 해당 레이어에 생성되는 새 필드가 텍스트 필드의 길이를 (바이트 길이가 아니라 UTF-8 문자 길이를) 강제로 시도하고 표현하게 하려면 이 옵션을 YES로 설정할 수도 있습니다.
   NO로 설정하면 그 대신 TEXT 유형을 사용할 것입니다. 기본값은 YES입니다.

-  **TRUNCATE_FIELDS**:
   텍스트 필드의 최대 길이를 넘어서는 필드값을 강제로 절단(truncate)하고, 전송된 문자열을 무결한 UTF-8 문자열로 변환해야 하는 경우 전송된 문자열을 강제로 "고치도록" 하려면 이 옵션을 YES로 설정할 수도 있습니다.
   NO로 설정하면 값을 절단하거나 수정하지 않습니다. 기본값은 NO입니다.

-  **IDENTIFIER=string**:
   contents 테이블에 삽입할 레이어 식별자입니다.

-  **DESCRIPTION=string**:
   contents 테이블에 삽입할 레이어 설명입니다.

-  **ASPATIAL_VARIANT=GPKG_ATTRIBUTES/NOT_REGISTERED**: (GDAL 2.2 이상 버전)
   비공간 테이블을 등록할 방법을 설정합니다. GDAL 2.2 이상 버전에서 기본값은 GPKG_ATTRIBUTES입니다. (이전 버전에서의 습성은 OGR_ASPATIAL과 동등했습니다.) 지오패키지 1.2버전부터, 사양에 비공간 테이블을 포함합니다. gpkg_contents 테이블에 비공간 테이블을 data_type="attributes" 속성을 가진 레코드로 작성합니다. 이런 비공간 테이블은 GDAL 2.2 이상 버전에서만 호환됩니다.
   NOT_REGISTERED로 설정하면, 지오패키지 시스템 테이블에 어떤 비공간 테이블도 등록하지 않습니다.
   이전 OGR 2.0 및 2.1버전에서 비슷한 목적으로 "aspatial" 확장 사양을 개발했기 때문에, OGR_ASPATIAL로 설정하면 비공간 테이블을 data_type="aspatial" 속성을 가진 레코드로 작성하고 gpkg_extensions 테이블에 "aspatial" 확장 사양을 선언할 것입니다. GDAL 3.3버전부터, 생성 작업 시 더 이상 OGR_ASPATIAL을 사용할 수 없습니다.

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`OGR_SQLITE_JOURNAL`:
   이 옵션을 이용해서 지오패키지 (및 당연히 SQLite) 파일의 저널 모드를 설정할 수 있습니다.
   https://www.sqlite.org/pragma.html#pragma_journal_mode 도 읽어보십시오.

-  :decl_configoption:`OGR_SQLITE_CACHE`:
   :ref:`성능 힌트 <target_drivers_vector_gpkg_performance_hints>` 를 참조하십시오.

-  :decl_configoption:`OGR_SQLITE_SYNCHRONOUS`:
   :ref:`성능 힌트 <target_drivers_vector_gpkg_performance_hints>` 를 참조하십시오.

-  :decl_configoption:`OGR_SQLITE_LOAD_EXTENSIONS` =extension1,...,extensionN,ENABLE_SQL_LOAD_EXTENSION: (GDAL 3.5.0 이상 버전)
   데이터베이스를 열 때 불러올 확장 사양을 담고 있는 공유 라이브러리들의 이름을 쉼표로 구분한 목록을 지정합니다. 파일을 직접 불러올 수 없는 경우, 다양한 운영 체제 특화 확장 사양을 추가로 불러오려 시도할 것입니다. 즉 예를 들어 "samplelib"을 불러오지 못 하는 경우 "samplelib.so" 또는 "samplelib.dylib" 또는 "samplelib.dll" 같은 이름들을 시도할 수도 있습니다.
   특수값 ``ENABLE_SQL_LOAD_EXTENSION`` 을 이용해서 SQL ``load_extension()`` 함수를 이용할 수 있습니다. 이 함수는 SQLite3 표준 빌드에서 일반적으로 비활성화되어 있습니다.
   확장 사양을 신뢰할 수 없는 경우 확장 사양을 불러오는 것이 잠재적인 보안 위협이 될 수 있습니다.

-  :decl_configoption:`OGR_SQLITE_PRAGMA`:
   이 옵션을 이용하면 어떤 SQLite `PRAGMA 선언문 <http://www.sqlite.org/pragma.html>`_ 이든 지정할 수 있습니다. 문법은 다음과 같습니다.

   ::

      OGR_SQLITE_PRAGMA = "pragma_name=pragma_value[,pragma_name2=pragma_value2]"

-  :decl_configoption:`OGR_CURRENT_DATE`:
   이 드라이버는 파일 생성 또는 수정 시 지오패키지의 ``last_change`` 타임스탬프를 업데이트합니다. 재현 가능성(reproducibility)을 위해 일관된 바이너리 산출물이 필요한 경우, 이 전체 수준 환경설정 옵션을 설정하면 타임스탬프를 특정값으로 강제할 수 있습니다. 이 옵션을 설정할 때 지오패키지 표준이 -- 예를 들면 `1.2버전 <https://www.geopackage.org/spec120/#r15>`_ 이 -- 요구하는 특정한 시간 서식을 따르도록 주의하십시오.

-  :decl_configoption:`SQLITE_USE_OGR_VFS`:
   이 옵션을 YES로 설정하면 GDAL/OGR I/O 레이어가 추가적인 버퍼/캐시 작업을 사용할 수 있고, I/O 속도도 향상시킬 수 있습니다. 더 자세한 정보는 :ref:`성능 힌트 <target_user_virtual_file_systems_file_caching>` 를 참조하십시오.
   이 옵션을 활성화한 경우 어떤 파일도 잠그지 않기 때문에 동시 편집 시 데이터베이스에 오류가 발생할 수도 있다는 사실을 주의하십시오.

메타데이터
--------

GDAL은 데이터셋과 레이어 객체에 메타데이터를 읽고 쓰기 위해 표준화된 `gpkg_metadata <http://www.geopackage.org/spec/#_metadata_table>`_ 및 `gpkg_metadata_reference <http://www.geopackage.org/spec/#_metadata_reference_table>`_ 테이블을 사용합니다.

기본 메타데이터 도메인 및 잠재적인 다른 메타데이터 도메인으로부터 나온 GDAL 메타데이터는 GDAL PAM(Persistent Auxiliary Metadata) .aux.xml 파일에서 사용되는 서식을 준수하는 단일 XML 문서에 직렬화(serialize)되고, gpkg_metadata에 "md_scope=dataset" 및 "md_standard_uri=http://gdal.org" 로 등록됩니다. 데이터셋의 경우, gpkg_metadata_reference에서 이 항목을 "reference_scope=geopackage"로 참조합니다. 레이어의 경우, gpkg_metadata_reference에서 이 항목을 "reference_scope=table" 및 "table_name={name of the table}"로 참조합니다.

이 드라이버는 GDAL로부터 나오지 않은 메타데이터를 읽을 수 있으며, GPKG_METADATA_ITEM_XXX 형식의 키와 gpkg_metadata 테이블의 *metadata* 열의 내용을 값으로 가지는 메타데이터 항목으로 노출시킬 것입니다. 현재 GDAL 인터페이스를 통해 이런 메타데이터를 업데이트하는 것을 지원하지 않습니다. (다만 직접적인 SQL 명령어로 업데이트할 수는 있습니다.)

읽기/쓰기 시 기본 메타데이터 도메인의 특정 DESCRIPTION 및 IDENTIFIER 메타데이터 항목을 사용하면 gpkg_contents 테이블의 대응하는 열들을 읽고 업데이트할 수 있습니다.

비공간 테이블
------------------

지오패키지 1.0 및 1.1의 핵심 지오패키지 사양은 비공간(non-spatial) 테이블을 지원하지 않습니다. 비공간 테이블은 지오패키지 1.2버전에서 "attributes" 데이터 유형으로 추가되었습니다.

이 드라이버는 :ref:`vector.geopackage_aspatial` 을 이용해서 비공간 테이블을 읽고 쓸 수 있습니다.

GDAL 2.2버전부터, 이 드라이버는 기본적으로 지오패키지 1.2버전의 "attributes" 데이터 유형을 지원하는 것은 물론 gdal_aspatial 확장 사양을 통해 등록되지 않은 비공간 테이블도 목록화할 것입니다.
GDAL 2.2버전부터, 기본적으로 지오패키지 1.2버전의 "attributes" 데이터 유형을 따라 비공간 테이블을 생성합니다. (이 습성은 ASPATIAL_VARIANT 레이어 생성 옵션으로 제어할 수 있습니다.)

공간 뷰
-------------

gpkg_contents 및 gpkg_geometry_columns 테이블에 대응하는 레코드를 삽입한 경우 뷰를 무결한 공간 레이어로 생성하고 인식할 수 있습니다.

GDAL 2.2버전부터, 뷰의 SELECT 문에 있는 열이 정수형 기본 키 역할을 하는 경우 해당 열을 OGC_FID로 재명명하면 OGR가 이 열을 뷰의 FID 열로 인식할 수 있습니다. 이렇게 재명명하지 않고 소스 테이블로부터 객체ID를 선택하는 것은 충분하지 않을 것입니다. 결합(join) 때문에 이 객체ID가 여러 번 나타날 수 있기 때문입니다. 따라서 사용자가 해당 열이 정말로 기본 키인지 확실하게 알고 있어야만 합니다.

예를 들면:

.. code-block:: sql

   CREATE VIEW my_view AS SELECT foo.fid AS OGC_FID, foo.geom, ... FROM foo JOIN another_table ON foo.some_id = another_table.other_id
   INSERT INTO gpkg_contents (table_name, identifier, data_type, srs_id) VALUES ( 'my_view', 'my_view', 'features', 4326)
   INSERT INTO gpkg_geometry_columns (table_name, column_name, geometry_type_name, srs_id, z, m) values ('my_view', 'my_geom', 'GEOMETRY', 4326, 0, 0)

이 SQL 문이 성공하려면 GDAL을 SQLITE_ENABLE_COLUMN_METADATA 옵션을 가진 SQLite3 및 SQLITE_HAS_COLUMN_METADATA 옵션과 함께 컴파일해야 합니다.
GDAL 2.3버전부터, (예를 들어 ``ogrinfo --format GPKG`` 명령어로) SQLITE_HAS_COLUMN_METADATA=YES 드라이버 메타데이터 항목이 선언되었는지를 확인하면 이렇게 컴파일되었는지 쉽게 검증할 수 있습니다.

좌표계
----------------------------

지오패키지는 GDAL이 일반적으로 지원하는 무결한 지리, 투영 및 복합 좌표계를 지원하고, ``gpkg_spatial_ref_sys`` 테이블에 저장합니다.

지오패키지 사양 별로 하드 코딩된 특수 좌표계 2개를 준비하고 있습니다:

-  정의되지 않은 지리 좌표계를 위한 SRID 0:
   어떤 좌표계도 명확하게 지정하지 않고 공간 레이어를 생성하는 경우 기본적으로 이 좌표계를 선택합니다.

-  정의되지 않은 투영 좌표계를 위한 SRID -1: (GDAL 3.3 이상 버전)
   ``LOCAL_CS["Undefined cartesian SRS"]`` WKT 문자열로부터 인스턴스화된 좌표계를 가진 레이어를 생성하면 이 좌표계를 선택할 수도 있습니다.

지오패키지 확장 지원 수준
-----------------------------------------

(벡터 스코프(scope)를 가지고 있는 지오패키지에 한합니다.)

.. list-table:: GeoPackage Extensions
   :header-rows: 1

   * - 확장 이름
     - OGC 도입 확장인가?
     - GDAL이 지원하는가?
   * - `비선형 도형 유형 <http://www.geopackage.org/guidance/extensions/nonlinear_geometry_types.html>`_
     - Ｏ
     - GDAL 2.1버전부터 Ｏ
   * - `R-트리 공간 색인 <http://www.geopackage.org/guidance/extensions/rtree_spatial_indexes.html>`_
     - Ｏ
     - Ｏ
   * - `메타데이터 <http://www.geopackage.org/guidance/extensions/metadata.html>`_
     - Ｏ
     - Ｏ
   * - `스키마 <http://www.geopackage.org/guidance/extensions/schema.html>`_
     - Ｏ
     - GDAL 3.3버전부터 Ｏ (필드 도메인으로 노출되는 지오패키지 제약 조건)
   * - `좌표계 용 WKT <http://www.geopackage.org/guidance/extensions/wkt_for_crs.md>`_ (WKT v2)
     - Ｏ
     -  GDAL 2.2버전 부터 부분 지원. GDAL이 이 확장 사양으로 데이터베이스를 읽어올 수 있지만, WKT v2 항목만 가지고 있는 공간 좌표계 항목을 해석하지는 못 합니다.
   * - :ref:`vector.geopackage_aspatial`
     - Ｘ
     - Ｏ (GDAL 2.2버전에서 *attributes* 공식 data_type 퇴출)

.. _target_drivers_vector_gpkg_performance_hints:

성능 힌트
---------

:ref:`SQLite 드라이버 <target_drivers_vector_sqlite_performance_hints>` 에 언급된 것과 동일한 성틍 힌트들이 적용됩니다.

예시
--------

-  단일 shapefile을 지오패키지로 단순 변환하기. abc.shp의 객체들과 abc.dbf의 속성들로 'abc' 테이블을 생성할 것입니다. ``filename.gpkg`` 파일을 생성할 것이기 때문에, 이 파일이 기존에 존재해서는 절대로 **안 됩니다**. 기존 지오패키지에 새 레이어를 추가하려면  ogr2ogr 유틸리티를 **-update** 스위치와 함께 실행하십시오.

   ::

      ogr2ogr -f GPKG filename.gpkg abc.shp

-  기존 지오패키지 파일 -- 예를 들면 지오패키지 템플릿 -- 에 동일한 또는 하위 호환되는 데이터베이스 스키마에 따라 피처를 담고 있는 또다른 지오패키지로부터 피처를 추가해서 업데이트하기.

   ::

      ogr2ogr -append output.gpkg input.gpkg

-  shapefile들이 있는 디렉터리를 지오패키지로 변환하기. 각 파일은 GPKG 파일 안에 새 테이블로 각각 작성될 것입니다. ``filename.gpkg`` 파일을 생성할 것이기 때문에, 이 파일이 기존에 존재해서는 절대로 **안 됩니다**.

   ::

      ogr2ogr -f GPKG filename.gpkg ./path/to/dir

-  PostGIS 데이터베이스를 GeoPackage로 변환하기. 데이터베이스의 각 테이블은 GPKG 파일 안에 테이블로 각각 작성될 것입니다. ``filename.gpkg`` 파일을 생성할 것이기 때문에, 이 파일이 기존에 존재해서는 절대로 **안 됩니다**.

   ::

      ogr2ogr -f GPKG filename.gpkg PG:'dbname=mydatabase host=localhost'

-  지오패키지 데이터베이스 2개를 결합(join)시키기:

   ::

      ogrinfo my_spatial.gpkg \
        -sql "SELECT poly.id, other.foo FROM poly JOIN other_schema.other USING (id)" \
        -oo PRELUDE_STATEMENTS="ATTACH DATABASE 'other.gpkg' AS other_schema"

참고
--------

-  :ref:`지오패키지 래스터 <raster.gpkg>` 드라이버 문서
-  `지오패키지 알아보기 <http://www.geopackage.org/guidance/getting-started.html>`_
-  `OGC 지오패키지 포맷 표준 <http://www.geopackage.org/spec/>`_ 사양, HTML 포맷 (표준의 현재/개발 버전)
-  `OGC 지오패키지 인코딩 표준 <http://www.opengeospatial.org/standards/geopackage>`_ 페이지
-  `SQLite <http://sqlite.org/>`_

.. toctree::
   :hidden:

   geopackage_aspatial
