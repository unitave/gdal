.. _ogrinfo:

================================================================================
ogrinfo
================================================================================

.. only:: html

    OGR 지원 데이터소스에 대한 정보를 목록화합니다. SQL 선언문을 사용하면 데이터를 편집할 수도 있습니다.

.. Index:: ogrinfo

개요
--------

.. code-block::

    ogrinfo [--help-general] [-ro] [-q] [-where restricted_where|@filename]
            [-spat xmin ymin xmax ymax] [-geomfield field] [-fid fid]
            [-sql statement|@filename] [-dialect dialect] [-al] [-rl] [-so] [-fields={YES/NO}]
            [-geom={YES/NO/SUMMARY/WKT/ISO_WKT}] [--formats] [[-oo NAME=VALUE] ...]
            [-nomd] [-listmdd] [-mdd domain|`all`]*
            [-nocount] [-noextent] [-nogeomtype] [-wkt_format WKT1|WKT2|...]
            [-fielddomain name]
            <datasource_name> [<layer> [<layer> ...]]

설명
-----------

:program:`ogrinfo` 프로그램은 stdout(터미널)에 OGR이 지원하는 데이터소스에 대한 다양한 정보의 목록을 출력합니다. SQL 선언문을 실행하면 데이터를 편집할 수도 있습니다.

.. program:: ogrinfo

.. option:: -ro

    데이터소스를 읽기전용 모드로 엽니다.

.. option:: -al

    모든 레이어의 모든 객체를 목록화합니다. (레이어명을 인자로 넘겨야 할 때 대신 사용합니다)

.. option:: -rl

    임의의 레이어 읽기 모드를 활성화합니다. 예를 들면 레이어별로가 아니라 데이터셋에 있는 객체의 순서대로 읽기를 반복합니다. 몇몇 포맷의 경우 (예: OSM, GMLAS) 읽어오는 속도가 훨씬 빠를 수 있습니다.

    .. versionadded:: 2.2

.. option:: -so

    요약만(Summary Only): 개별 객체 목록을 출력하지 않고 투영볍, 스키마, 객체 개수 및 범위 같은 요약 정보만 출력합니다.

.. option:: -q

    좌표계, 레이어 스키마, 범위 및 객체 개수를 포함하는 다양한 정보를 자세히 리포트하지 않습니다. (침묵 모드)

.. option:: -where <restricted_where>

    SQL `WHERE` 선언문에서 사용되는 쿼리의 제약 양식으로 된 속성 쿼리입니다. 속성 쿼리와 일치하는 객체만 리포트할 것입니다. GDAL 2.1버전부터, 지정한 파일명에 내용이 있다는 사실을 나타내기 위한 ``\filename`` 문법을 사용할 수 있습니다.

.. option:: -sql <statement>

    지정한 SQL 선언문을 실행해서 결과를 반환합니다. GDAL 2.1버전부터, 지정한 파일명에 내용이 있다는 사실을 나타내기 위한 ``@filename`` 문법을 사용할 수 있습니다. SQL INSERT, UPDATE, DELETE, DROP TABLE, ALTER TABLE 등의 명령어로 데이터도 편집할 수 있습니다. 편집 능력은 선택한 ``dialect`` 에 따라 달라집니다.

.. option:: -dialect <dialect>

    SQL 방언(dialect)입니다. 어떤 경우 ``OGRSQL`` 을 전송해서 RDBMS의 네이티브 SQL 대신 (최적화되지 않은) :ref:`ogr_sql_dialect` 을 사용하기 위해 쓰일 수도 있습니다. 모든 데이터소스에서 ``SQLITE`` 및 ``INDIRECT_SQLITE`` 방언 값으로 :ref:`sql_sqlite_dialect` 도 사용할 수 있습니다.

.. option:: -spat <xmin> <ymin> <xmax> <ymax>

    관심 영역(area of interest)입니다. 이 직사각형 내부에 있는 객체만 리포트할 것입니다.

.. option:: -geomfield <field>

    공간 필터가 작동하는 도형 필드의 이름입니다.

.. option:: -fid <fid>

    이 옵션을 지정하는 경우, 이 객체 ID를 가진 객체만 리포트할 것입니다. 공간 또는 속성 쿼리를 제외하고 작동합니다. 주의: 객체 ID를 기반으로 객체 여러 개를 선택하려는 경우, 'fid'가 OGR SQL이 인식하는 특수 필드라는 사실도 이용할 수 있습니다. 즉 `-where "fid in (1,3,5)"` 는 객체 1, 3, 5를 선택할 것입니다.

.. option:: -fields YES|NO:

    ``NO`` 로 설정하면, 객체 덤프가 필드값을 출력하지 않을 것입니다. 기본값은 ``YES`` 입니다.

.. option:: -fielddomain <domain_name>

    .. versionadded:: 3.3

    필드 도메인에 대한 상세 정보를 출력합니다.

.. option:: -geom YES|NO|SUMMARY|WKT|ISO_WKT

    ``NO`` 로 설정하면, 객체 덤프가 도형을 출력하지 않을 것입니다. ``SUMMARY`` 로 설정하면, 도형의 요약 정보만 출력할 것입니다. ``YES`` or ``ISO_WKT`` 로 설정하는 경우, 도형을 완전한 OGC WKT 서식으로 리포트할 것입니다. ``WKT`` 로 설정하면 도형을 예전(legacy) ``WKT`` 로 리포트할 것입니다. 기본값은 ``YES`` 입니다. (GDAL 2.1 버전부터 WKT와 ``ISO_WKT`` 를 사용할 수 있는데, 이 버전부터 기본값이 ISO_WKT로 변경되었습니다.)

.. option:: -oo NAME=VALUE

    데이터 열기 옵션 (특정 포맷 지원)

.. option:: -nomd

    메타데이터를 출력하지 않습니다. 몇몇 데이터셋은 수많은 메타데이터 문자열을 가지고 있을 수도 있습니다.

.. option:: -listmdd

    데이터셋에서 사용할 수 있는 모든 메타데이터 도메인을 목록화합니다.

.. option:: -mdd <domain>

    지정한 도메인에 있는 메타데이터를 리포트합니다. 모든 도메인에 있는 메타데이터를 리포트하길 원한다면 ``all`` 을 사용하면 됩니다.

.. option:: -nocount

    객체 개수를 출력하지 않습니다.

.. option:: -noextent

    공간 범위를 출력하지 않습니다.

.. option:: -nogeomtype

    레이어 도형 유형을 출력하지 않습니다.

    .. versionadded:: 3.1

.. option:: --formats

    활성화된 포맷 드라이버를 목록화합니다.

.. option:: -wkt_format <format>

    공간 좌표계를 출력하기 위해 쓰이는 WKT 서식입니다. 현재 다음과 같은 ``format`` 값을 지원합니다:

    ``WKT1``

    ``WKT2`` (최신 WKT 버전, 현재 *WKT2_2018*)

    ``WKT2_2015``

    ``WKT2_2018``

    .. versionadded:: 3.0.0

.. option:: <datasource_name>

    열어볼 데이터소스입니다. 파일, 디렉터리 또는 기타 가상 이름일 수도 있습니다. 어떤 데이터소스를 지원하는지 알고 싶다면 OGR 벡터 포맷 목록을 참조하십시오.

.. option:: <layer>

    레이어 이름을 하나 이상 리포트할 수도 있습니다. 어떤 레이어 이름도 전송(pass)되지 않는 경우 ogrinfo가 사용할 수 있는 레이어 목록(과 사용할 수 있는 레이어들 전체의 도형 유형)을 리포트할 것입니다. 레이어 이름(들)을 지정하면 레이어의 범위, 좌표계, 객체 개수, 도형 유형, 스키마 및 쿼리 파라미터와 일치하는 모든 객체를 터미널로 리포트할 것입니다. 쿼리 파라미터를 하나도 지정하지 않으면 모든 객체를 리포트합니다.

도형은 OGC WKT 서식으로 리포트됩니다.

예시
--------

NTF 파일에 있는 레이어들의 이름을 리포트하는 예시:

.. code-block::

    ogrinfo wrk/SHETLAND_ISLANDS.NTF

    # INFO: Open of `wrk/SHETLAND_ISLANDS.NTF'
    # using driver `UK .NTF' successful.
    # 1: BL2000_LINK (Line String)
    # 2: BL2000_POLY (None)
    # 3: BL2000_COLLECTIONS (None)
    # 4: FEATURE_CLASSES (None)

모든 객체별로 상세 정보를 출력하지 않고 레이어의 요약 정보를 (``-so``) 가져오는 예시:

.. code-block::

    ogrinfo \
      -so \
      natural_earth_vector.gpkg \
      ne_10m_admin_0_antarctic_claim_limit_lines

      # INFO: Open of `natural_earth_vector.gpkg'
      #      using driver `GPKG' successful.

      # Layer name: ne_10m_admin_0_antarctic_claim_limit_lines
      # Geometry: Line String
      # Feature Count: 23
      # Extent: (-150.000000, -90.000000) - (160.100000, -60.000000)
      # Layer SRS WKT:
      # GEOGCS["WGS 84",
      #     DATUM["WGS_1984",
      #         SPHEROID["WGS 84",6378137,298.257223563,
      #             AUTHORITY["EPSG","7030"]],
      #         AUTHORITY["EPSG","6326"]],
      #     PRIMEM["Greenwich",0,
      #         AUTHORITY["EPSG","8901"]],
      #     UNIT["degree",0.0174532925199433,
      #         AUTHORITY["EPSG","9122"]],
      #     AUTHORITY["EPSG","4326"]]
      # FID Column = fid
      # Geometry Column = geom
      # type: String (15.0)
      # scalerank: Integer (0.0)
      # featurecla: String (50.0)


레이어에 있는 객체를 제한적으로 산출하기 위해 속성 쿼리를 사용하는 예시:

.. code-block::

    ogrinfo -ro \
        -where 'GLOBAL_LINK_ID=185878' \
        wrk/SHETLAND_ISLANDS.NTF BL2000_LINK

    # INFO: Open of `wrk/SHETLAND_ISLANDS.NTF'
    # using driver `UK .NTF' successful.
    #
    # Layer name: BL2000_LINK
    # Geometry: Line String
    # Feature Count: 1
    # Extent: (419794.100000, 1069031.000000) - (419927.900000, 1069153.500000)
    # Layer SRS WKT:
    # PROJCS["OSGB 1936 / British National Grid",
    # GEOGCS["OSGB 1936",
    # DATUM["OSGB_1936",
    # SPHEROID["Airy 1830",6377563.396,299.3249646]],
    # PRIMEM["Greenwich",0],
    # UNIT["degree",0.0174532925199433]],
    # PROJECTION["Transverse_Mercator"],
    # PARAMETER["latitude_of_origin",49],
    # PARAMETER["central_meridian",-2],
    # PARAMETER["scale_factor",0.999601272],
    # PARAMETER["false_easting",400000],
    # PARAMETER["false_northing",-100000],
    # UNIT["metre",1]]
    # LINE_ID: Integer (6.0)
    # GEOM_ID: Integer (6.0)
    # FEAT_CODE: String (4.0)
    # GLOBAL_LINK_ID: Integer (10.0)
    # TILE_REF: String (10.0)
    # OGRFeature(BL2000_LINK):2
    # LINE_ID (Integer) = 2
    # GEOM_ID (Integer) = 2
    # FEAT_CODE (String) = (null)
    # GLOBAL_LINK_ID (Integer) = 185878
    # TILE_REF (String) = SHETLAND I
    # LINESTRING (419832.100 1069046.300,419820.100 1069043.800,419808.300
    # 1069048.800,419805.100 1069046.000,419805.000 1069040.600,419809.400
    # 1069037.400,419827.400 1069035.600,419842 1069031,419859.000
    # 1069032.800,419879.500 1069049.500,419886.700 1069061.400,419890.100
    # 1069070.500,419890.900 1069081.800,419896.500 1069086.800,419898.400
    # 1069092.900,419896.700 1069094.800,419892.500 1069094.300,419878.100
    # 1069085.600,419875.400 1069087.300,419875.100 1069091.100,419872.200
    # 1069094.600,419890.400 1069106.400,419907.600 1069112.800,419924.600
    # 1069133.800,419927.900 1069146.300,419927.600 1069152.400,419922.600
    # 1069153.500,419917.100 1069153.500,419911.500 1069153.000,419908.700
    # 1069152.500,419903.400 1069150.800,419898.800 1069149.400,419894.800
    # 1069149.300,419890.700 1069149.400,419890.600 1069149.400,419880.800
    # 1069149.800,419876.900 1069148.900,419873.100 1069147.500,419870.200
    # 1069146.400,419862.100 1069143.000,419860 1069142,419854.900
    # 1069138.600,419850 1069135,419848.800 1069134.100,419843
    # 1069130,419836.200 1069127.600,419824.600 1069123.800,419820.200
    # 1069126.900,419815.500 1069126.900,419808.200 1069116.500,419798.700
    # 1069117.600,419794.100 1069115.100,419796.300 1069109.100,419801.800
    # 1069106.800,419805.000  1069107.300)

SQLite 방언을 사용해서 shapefile의 속성값을 SQL로 업데이트하는 예시:

.. code-block::

    ogrinfo test.shp -dialect sqlite -sql "update test set attr='bar' where attr='foo'"
