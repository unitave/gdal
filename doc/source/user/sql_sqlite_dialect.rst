.. _sql_sqlite_dialect:

================================================================================
SQL SQLite 방언
================================================================================

.. highlight:: sql

SQLite "방언"을 :ref:`ogr_sql_dialect` 에 대한 대체 SQL 방언으로 사용할 수 있습니다.
SQLite 방언을 사용한다는 것은 GDAL/OGR가 SQLite 지원과 함께, 그리고 이왕이면 공간 함수를 이용할 수 있도록 `SpatiaLite <https://www.gaia-gis.it/fossil/libspatialite/index>`_ 지원도 함께 빌드되었다는 뜻입니다.

SQLite 방언은 OGR SQL 방언과 마찬가지로 모든 OGR 데이터소스에 사용할 수 있습니다. ``pszDialect`` 인자를 "SQLITE"로 지정하면 :cpp:func:`GDALDataset::ExecuteSQL` 메소드를 통해 SQLite 방언을 사용할 수 있습니다. :ref:`ogrinfo` 또는 :ref:`ogr2ogr` 유틸리티의 경우, "-dialect SQLITE" 옵션을 지정해야만 합니다.

SQLite 방언의 주요 목적은 SELECT 문을 실행하는 것이지만, 업데이트를 지원하는 데이터소스의 경우 INSERT/UPDATE/DELETE 문도 실행할 수 있습니다. GDAL은 내부적으로 `SQLite의 가상 테이블 메커니즘 <https://sqlite.org/vtab.html>`_ 을 이용하기 때문에, ALTER TABLE 같은 작업은 지원하지 않습니다. ALTER TABLE 또는 DROP TABLE을 실행하려면 :ref:`ogr_sql_dialect` 을 사용하십시오.

데이터소스가 SQLite 데이터베이스(지오패키지, SpatiaLite)인 경우 SQLite 방언이 네이티브 SQL 방언으로 동작하기 때문에 가상 테이블 메커니즘을 이용하지 않습니다. 이런 경우에도 "-dialect INDIRECT_SQLITE" 옵션을 지정하면 GDAL이 가상 테이블 메커니즘을 이용하도록 강제할 수 있습니다. 이 옵션은 꼭 필요한 경우에만 사용해야 합니다. 가상 테이블 메커니즘을 이용하면 성능이 저하될 수도 있기 때문입니다.

SQL 선언문의 문법은 SQLite SQL 엔진의 완전한 문법과 동일합니다. 다음 웹페이지들을 참조하십시오:

- `SELECT <http://www.sqlite.org/lang_select.html>`_
- `INSERT <http://www.sqlite.org/lang_insert.html>`_
- `UPDATE <http://www.sqlite.org/lang_update.html>`_
- `DELETE <http://www.sqlite.org/lang_delete.html>`_

SELECT 문
----------------

SELECT 선언문을 사용해서 임시 객체 레이어로 표현되는 쿼리 결과물을 가진 (RDBMS의 테이블 행과 유사한) 레이어 객체를 가져옵니다. 데이터소스의 레이어는 RDBMS에 있는 테이블과 유사하며 객체 속성은 열의 값과 유사합니다. OGR SQLITE SELECT 문의 가장 단순한 형식은 다음과 같습니다:

.. code-block::

    SELECT * FROM polylayer

WHERE, JOIN, USING, GROUP BY, ORDER BY, sub SELECT 등을 포함하는 좀 더 복잡한 선언문도 당연히 사용할 수 있습니다.

ExecuteSQL() 메소드가 호출되는 데이터소스에서 사용할 수 있는 레이어 이름을 테이블 이름으로 사용할 수 있습니다.

OGR SQL과 마찬가지로, 다른 데이터소스의 레이어도 ``"other_datasource_name"."layer_name"`` 와 같은 문법으로 참조할 수 있습니다:

.. code-block::

    SELECT p.*, NAME FROM poly p JOIN "idlink.dbf"."idlink" il USING (eas_id)

마스터 데이터소스가 SQLite 데이터베이스(지오패키지, SpatiaLite)인 경우 간접 SQLite 방언을 사용해야 합니다. 그렇지 않으면 추가 데이터소스를 열지 않고 마스터 데이터베이스로부터 JOIN에서 사용할 테이블을 찾습니다.

.. code-block:: shell

    ogrinfo jointest.gpkg -dialect INDIRECT_SQLITE -sql "SELECT a.ID,b.ID FROM jointest a JOIN \"jointest2.shp\".\"jointest2\" b ON a.ID=b.ID"

결과물의 열 목록, WHERE 절, JOIN 등에 레이어의 필드 이름을 열 이름으로 사용할 수 있습니다. 표현식, SQLite 함수, 공간 함수 등도 사용할 수 있습니다.

WHERE 절 또는 JOIN에 나타나는 필드에 대한 조건을 가능한 한 기저 OGR 레이어에 적용되는 속성 필터로 변환합니다. 부 테이블이 사용 중인 키 필드에 대해 색인되어 있지 않은 경우 JOIN 작업의 부하량이 매우 커질 수 있습니다.

구분 식별자
+++++++++++++++++++++

레이어 또는 속성의 이름이 'FROM'처럼 SQL에 예약된 키워드거나 숫자 또는 언더바로 시작하는 경우, 반드시 "구분 식별자(delimited identifier)"로 처리해야만 하고 쿼리에서 큰따옴표 기호로 감싸야만 합니다. 꼭 필요하지 않은 경우에도 큰따옴표를 사용할 수 있습니다:

.. code-block::

    SELECT "p"."geometry", "p"."FROM", "p"."3D" FROM "poly" p

명령줄 셸에서 SQL 선언문을 사용하는데 선언문 자체가 큰따옴표로 감싸인 경우, 선언문 안에 있는 큰따옴표를 "\\"로 이스케이프 처리해야만 합니다:

.. code-block:: shell

    ogrinfo p.shp -sql "SELECT geometry \"FROM\", \"3D\" FROM p"

도형 필드
++++++++++++++

``GEOMETRY`` 특수 필드는 :cpp:func:`OGRFeature::GetGeometryRef` 메소드가 반환하는 객체의 도형을 표현합니다. SELECT 문의 결과물 열 목록에 도형 필드를 명확하게 지정할 수 있으며, "\*" 와일드카드 문자를 사용하는 경우 자동으로 선택할 것입니다.

:cpp:func:`OGRLayer::GetGeometryColumn` 메소드가 반환하는 도형 열 이름이 빈 문자열이 아닌 OGR 레이어의 경우 (일반적으로 RDBMS 데이터소스인 경우) SQL 선언문에서 기저 OGR 레이어의 도형 열 이름을 도형 특수 필드의 이름으로 사용합니다. shapefile 등의 경우처럼 소스 레이어에 있는 도형 열 이름이 빈 문자열이라면, SQL 선언문에 항상 "geometry"라는 이름을 사용합니다:

.. code-block::

    SELECT EAS_ID, GEOMETRY FROM poly

이 SELECT 문은 다음을 반환합니다:

::

    OGRFeature(SELECT):0
    EAS_ID (Real) = 168
    POLYGON ((479819.84375 4765180.5,479690.1875 4765259.5,[...],479819.84375 4765180.5))

.. code-block::

    SELECT * FROM poly

그리고 이 SELECT 문은 다음을 반환합니다:

::

    OGRFeature(SELECT):0
    AREA (Real) = 215229.266
    EAS_ID (Real) = 168
    PRFEDEA (String) = 35043411
    POLYGON ((479819.84375 4765180.5,479690.1875 4765259.5,[...],479819.84375 4765180.5))

객체ID
++++++++++

객체ID는 일반적으로 객체의 특수 속성(property)으로, 객체 속성(attribute)으로 취급되지 않습니다. 쿼리에 객체ID를 활용해서 결과물을 정규 필드로 산출할 수 있다면 편리한 경우가 있습니다. 이렇게 하려면 ``rowid`` 라는 이름을 사용하십시오. 필드 와일드카드 확장 사양은 객체ID를 포함하지 않지만, 다음과 같은 문법을 사용해서 명확하게 포함시킬 수도 있습니다:

.. code-block::

    SELECT rowid, * FROM nation

당연히 재명명할 수도 있습니다:

.. code-block::

    SELECT rowid AS fid, * FROM nation

OGR_STYLE 특수 필드
+++++++++++++++++++++++

``OGR_STYLE`` 특수 필드는 :cpp:func:`OGRFeature::GetStyleString` 메소드가 반환하는 객체의 스타일 문자열을 표현합니다. 이 필드와 ``LIKE`` 연산자를 사용하면 쿼리 결과물을 스타일로 필터링할 수 있습니다. 다음은 주석 객체를 선택하는 예시입니다:

.. code-block::

    SELECT * FROM nation WHERE OGR_STYLE LIKE 'LABEL%'

SpatiaLite SQL 함수
++++++++++++++++++++++++

GDAL/OGR를 `SpatiaLite <https://www.gaia-gis.it/fossil/libspatialite/index>`_ 라이브러리 지원과 함께 빌드하면, 결과물 열 필드, WHERE 절 등등에 수많은 `추가 SQL 함수 <http://www.gaia-gis.it/gaia-sins/spatialite-sql-latest.html>`_ 를, 그 중에서도 특히 공간 함수를 사용할 수 있습니다:

.. code-block::

    SELECT EAS_ID, ST_Area(GEOMETRY) AS area FROM poly WHERE
        ST_Intersects(GEOMETRY, BuildCircleMbr(479750.6875,4764702.0,100))

이 SELECT 문은 다음을 반환합니다:

::

    OGRFeature(SELECT):0
    EAS_ID (Real) = 169
    area (Real) = 101429.9765625

    OGRFeature(SELECT):1
    EAS_ID (Real) = 165
    area (Real) = 596610.3359375

    OGRFeature(SELECT):2
    EAS_ID (Real) = 170
    area (Real) = 5268.8125

OGR 데이터소스 SQL 함수
++++++++++++++++++++++++++++

``ogr_datasource_load_layers(datasource_name[, update_mode[, prefix]])`` 함수를 사용해서 데이터소스의 모든 레이어를 자동으로 :ref:`가상 OGR 테이블 <vector.sqlite>` 로 불러올 수 있습니다:

::

    sqlite> SELECT load_extension('libgdal.so');

    sqlite> SELECT load_extension('libspatialite.so');

    sqlite> SELECT ogr_datasource_load_layers('poly.shp');
    1
    sqlite> SELECT * FROM sqlite_master;
    table|poly|poly|0|CREATE VIRTUAL TABLE "poly" USING VirtualOGR('poly.shp', 0, 'poly')

OGR 레이어 SQL 함수
+++++++++++++++++++++++

``ogr_layer_Extent()``, ``ogr_layer_SRID()``, ``ogr_layer_GeometryType()`` 및 ``ogr_layer_FeatureCount()`` SQL 함수들에 레이어 이름을 지정해서 사용할 수 있습니다:

.. code-block::

    SELECT ogr_layer_Extent('poly'), ogr_layer_SRID('poly') AS srid,
        ogr_layer_GeometryType('poly') AS geomtype, ogr_layer_FeatureCount('poly') AS count

이 SELECT 문은 다음을 반환합니다:

::

    OGRFeature(SELECT):0
    srid (Integer) = 40004
    geomtype (String) = POLYGON
    count (Integer) = 10
    POLYGON ((478315.53125 4762880.5,481645.3125 4762880.5,481645.3125 4765610.5,478315.53125 4765610.5,478315.53125 4762880.5))

OGR 압축 함수
+++++++++++++++++++++++++

``ogr_deflate(text_or_blob[, compression_level])`` 함수는 ZLib DEFLATE 알고리즘으로 압축한 바이너리 블랍(blob)을 반환합니다. :cpp:func:`CPLZLibDeflate` 함수를 참조하십시오.

``ogr_inflate(compressed_blob)`` 은 ZLib DEFLATE 알고리즘으로 압축한 블랍으로부터 압축 해제한 바이너리 블랍을 반환합니다. 압축된 바이너리가 문자열인 경우, ``CAST(ogr_inflate(compressed_blob) AS VARCHAR)`` 를 사용하십시오. :cpp:func:`CPLZLibInflate` 함수를 참조하십시오.

기타 함수
+++++++++++++++

``hstore_get_value()`` 함수를 사용하면 HSTORE 문자열로부터 키와 관련된 값을 ``key=>value,other_key=>other_value,...`` 같은 서식으로 추출할 수 있습니다:

.. code-block::

    SELECT hstore_get_value('a => b, "key with space"=> "value with space"', 'key with space') --> 'value with space'

OGR 지오코딩 함수
+++++++++++++++++++++++

``ogr_geocode(...)`` 및 ``ogr_geocode_reverse(...)`` SQL 함수를 사용할 수 있습니다.

- ``ogr_geocode(name_to_geocode [, field_to_return [, option1 [, option2, ...]]])``:
  "name_to_geocode"는 글자 그대로 지오코딩할 이름 또는 지오코딩해야만 할 열 이름입니다. 선택적인 "field_to_return"을 지정한다면, 반환할 필드가 도형 필드인 경우 (기본값) "geometry"일 수 있고, 또는 :cpp:func:`OGRGeocode` 함수가 반환하는 레이어의 필드 이름일 수 있습니다. 특수 필드 "raw"를 지정하면 지오코딩 서비스의 원시(raw) 응답을 (XML 문자열을) 반환할 수 있습니다.
  "option1", "option2", ...는 키=값 서식이어야만 하며, :cpp:func:`OGRGeocodeCreateSession` 또는 :cpp:func:`OGRGeocode` 함수가 이해하는 옵션이어야 합니다.

  이 함수는 내부적으로 :cpp:func:`OGRGeocode` API를 사용합니다. 더 자세한 내용은 OGRGeocode() API를 참조하십시오.

  .. code-block::

      SELECT ST_Centroid(ogr_geocode('Paris'))

  이 SELECT 문은 다음을 반환합니다:

  ::

      OGRFeature(SELECT):0
      POINT (2.342878767069653 48.85661793020374)

  .. code-block:: shell

      ogrinfo cities.csv -dialect sqlite -sql "SELECT *, ogr_geocode(city, 'country') AS country, ST_Centroid(ogr_geocode(city)) FROM cities"

  그리고 이 SELECT 문은 다음을 반환합니다:


  .. highlight:: none

  ::

      OGRFeature(SELECT):0
      id (Real) = 1
      city (String) = Paris
      country (String) = France métropolitaine
      POINT (2.342878767069653 48.85661793020374)

      OGRFeature(SELECT):1
      id (Real) = 2
      city (String) = London
      country (String) = United Kingdom
      POINT (-0.109369427546499 51.500506667319407)

      OGRFeature(SELECT):2
      id (Real) = 3
      city (String) = Rennes
      country (String) = France métropolitaine
      POINT (-1.68185153381778 48.111663929761093)

      OGRFeature(SELECT):3
      id (Real) = 4
      city (String) = Strasbourg
      country (String) = France métropolitaine
      POINT (7.767762859150757 48.571233274141846)

      OGRFeature(SELECT):4
      id (Real) = 5
      city (String) = New York
      country (String) = United States of America
      POINT (-73.938140243499049 40.663799577449979)

      OGRFeature(SELECT):5
      id (Real) = 6
      city (String) = Berlin
      country (String) = Deutschland
      POINT (13.402306623451983 52.501470321410636)

      OGRFeature(SELECT):6
      id (Real) = 7
      city (String) = Beijing
      POINT (116.391195 39.9064702)

      OGRFeature(SELECT):7
      id (Real) = 8
      city (String) = Brasilia
      country (String) = Brasil
      POINT (-52.830435216371839 -10.828214867369699)

      OGRFeature(SELECT):8
      id (Real) = 9
      city (String) = Moscow
      country (String) = Российская Федерация
      POINT (37.367988106866868 55.556208255649558)

.. highlight:: sql

- ``ogr_geocode_reverse(longitude, latitude, field_to_return [, option1 [, option2, ...]])``:
  이때 "longitude, latitude"가 쿼리할 좌표입니다. "field_to_return"은 :cpp:func:`OGRGeocodeReverse` 가 반환하는 레이어의 (예를 들어 'display_name' 같은) 필드 이름이어야만 합니다. 특수 필드 "raw"를 지정하면 지오코딩 서비스의 원시(raw) 응답을 (XML 문자열을) 반환할 수 있습니다.
  "option1", "option2", ...는 키=값 서식이어야만 하며, :cpp:func:`OGRGeocodeCreateSession` 또는 :cpp:func:`OGRGeocodeReverse` 함수가 이해하는 옵션이어야 합니다.

- ``ogr_geocode_reverse(geometry, field_to_return [, option1 [, option2, ...]])``:
  "geometry"가 (SpatiaLite) 포인트 도형인 대체 문법도 허용됩니다.

  이 함수는 내부적으로 :cpp:func:`OGRGeocodeReverse` API를 사용합니다. 더 자세한 내용은 OGRGeocodeReverse() API를 참조하십시오.

SpatiaLite 공간 색인
++++++++++++++++++++++++

SQL에 공간 색인 가상 테이블을 ("idx_layername_geometrycolumn" 형식으로) 확실하게 언급하거나 또는 VirtualSpatialIndex 확장 사양으로부터 좀 더 최신인 SpatialIndex를 사용하면 SpatiaLite 공간 색인 메커니즘을 촉발시킬 수 있습니다. 이 경우, 인메모리 R-트리를 작성해서 공간 쿼리의 속도를 향상시키는 데 사용할 것입니다.

예를 들어 두 레이어가 공간 교차한다고 할 때 레이어 중 하나에 공간 색인을 사용하면 실제 도형 교차 계산의 개수를 제한할 수 있습니다:

.. code-block::

    SELECT city_name, region_name FROM cities, regions WHERE
        ST_Area(ST_Intersection(cities.geometry, regions.geometry)) > 0 AND
        regions.rowid IN (
            SELECT pkid FROM idx_regions_geometry WHERE
                xmax >= MbrMinX(cities.geometry) AND xmin <= MbrMaxX(cities.geometry) AND
                ymax >= MbrMinY(cities.geometry) AND ymin <= MbrMaxY(cities.geometry))

또는 좀 더 명쾌하게 작성할 수 있습니다:

.. code-block::

    SELECT city_name, region_name FROM cities, regions WHERE
        ST_Area(ST_Intersection(cities.geometry, regions.geometry)) > 0 AND
        regions.rowid IN (
            SELECT rowid FROM SpatialIndex WHERE
                f_table_name = 'regions' AND search_frame = cities.geometry)

