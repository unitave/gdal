.. _gdalsrsinfo:

================================================================================
gdalsrsinfo
================================================================================

.. only:: html

    입력 공간 좌표계에 대한 정보를 (WKT, PROJ.4 등등) 여러 서식으로 목록화합니다.

.. Index:: gdalsrsinfo

개요
--------

.. code-block::

    Usage: gdalsrsinfo [--single-line] [-V] [-e][-o <out_type>] <srs_def>

설명
-----------

:program:`gdalsrsinfo` 유틸리티는 입력 공간 좌표계에 대한 정보를 다음 가운데 하나로 리포트합니다:

- GDAL/OGR이 지원하는, 공간 좌표계 정보를 담고 있는 데이터셋의 파일명
- 일반적인 GDAL/OGR 양식 가운데 하나 (완전한 WKT, PROJ.4, EPSG:n 또는 공간 좌표계를 담고 있는 파일)


.. program:: gdalsrsinfo

.. option:: --single-line

    WKT를 한 줄로 출력합니다.

.. option:: -V

    공간 좌표계의 무결성을 검증합니다.

.. option:: -e

    공간 좌표계에 대응하는 EPSG 번호(들)를 검색합니다.

.. option:: -o <out_type>

    산출물 유형:

    - ``default``: PROJ.4와 WKT (기본 옵션)
    - ``all``: 사용할 수 있는 모든 옵션
    - ``wkt_all``: 사용할 수 있는 모든 WKT 옵션
    - ``PROJJSON``: PROJJSON 문자열 (GDAL 3.1버전, PROJ 6.2버전 이상)
    - ``proj4``: PROJ.4 문자열
    - ``wkt1``: OGC WKT 서식 (전체)
    - ``wkt_simple``: OGC WKT 1 (단순화)
    - ``wkt_noct``: OGC WKT 1 (OGC CT 파라미터 없음)
    - ``wkt_esri``: ESRI WKT 서식
    - ``wkt``: 최신 WKT 버전 지원, 현재 wkt2_2018
    - ``wkt2``: 최신 WKT2 버전 지원, 현재 wkt2_2018
    - ``wkt2_2015``: OGC WKT2:2015
    - ``wkt2_2018``: OGC WKT2:2018
    - ``mapinfo``: Mapinfo 스타일의 CoordSys 서식
    - ``xml``: XML 서식 (GML 기반)

.. option:: <srs_def>

    GDAL/OGR이 지원하는, 공간 좌표계 정보를 추출할 데이터셋의 파일명 또는 일반적인 GDAL/OGR 양식 (완전한 WKT, PROJ.4, EPSG:n 또는 공간 좌표계를 담고 있는 파일) 가운데 하나일 수 있습니다.

예시
-------

::

    $ gdalsrsinfo EPSG:4326

    PROJ.4 : +proj=longlat +datum=WGS84 +no_defs

    OGC WKT :
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]

::

    $ gdalsrsinfo -o proj4 osr/data/lcc_esri.prj
    '+proj=lcc +lat_1=34.33333333333334 +lat_2=36.16666666666666 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +datum=NAD83 +units=m +no_defs '
    \endverbatim

::

    $ gdalsrsinfo -o proj4 landsat.tif
    PROJ.4 : '+proj=utm +zone=19 +south +datum=WGS84 +units=m +no_defs '

::

    $ gdalsrsinfo  -o wkt "EPSG:32722"

    PROJCRS["WGS 84 / UTM zone 22S",
        BASEGEOGCRS["WGS 84",
            DATUM["World Geodetic System 1984",
                ELLIPSOID["WGS 84",6378137,298.257223563,
                    LENGTHUNIT["metre",1]]],
            PRIMEM["Greenwich",0,
                ANGLEUNIT["degree",0.0174532925199433]]],
        CONVERSION["UTM zone 22S",
            METHOD["Transverse Mercator",
                ID["EPSG",9807]],
            PARAMETER["Latitude of natural origin",0,
                ANGLEUNIT["degree",0.0174532925199433],
                ID["EPSG",8801]],
            PARAMETER["Longitude of natural origin",-51,
                ANGLEUNIT["degree",0.0174532925199433],
                ID["EPSG",8802]],
            PARAMETER["Scale factor at natural origin",0.9996,
                SCALEUNIT["unity",1],
                ID["EPSG",8805]],
            PARAMETER["False easting",500000,
                LENGTHUNIT["metre",1],
                ID["EPSG",8806]],
            PARAMETER["False northing",10000000,
                LENGTHUNIT["metre",1],
                ID["EPSG",8807]]],
        CS[Cartesian,2],
            AXIS["(E)",east,
                ORDER[1],
                LENGTHUNIT["metre",1]],
            AXIS["(N)",north,
                ORDER[2],
                LENGTHUNIT["metre",1]],
        USAGE[
            SCOPE["unknown"],
            AREA["World - S hemisphere - 54°W to 48°W - by country"],
            BBOX[-80,-54,0,-48]],
        ID["EPSG",32722]]

::

    $ gdalsrsinfo -o wkt_all "EPSG:4322"
    OGC WKT 1:
    GEOGCS["WGS 72",
        DATUM["World_Geodetic_System_1972",
            SPHEROID["WGS 72",6378135,298.26,
                AUTHORITY["EPSG","7043"]],
            TOWGS84[0,0,4.5,0,0,0.554,0.2263],
            AUTHORITY["EPSG","6322"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AXIS["Latitude",NORTH],
        AXIS["Longitude",EAST],
        AUTHORITY["EPSG","4322"]]

    OGC WKT2:2015 :
    BOUNDCRS[
        SOURCECRS[
            GEODCRS["WGS 72",
                DATUM["World Geodetic System 1972",
                    ELLIPSOID["WGS 72",6378135,298.26,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                CS[ellipsoidal,2],
                    AXIS["geodetic latitude (Lat)",north,
                        ORDER[1],
                        ANGLEUNIT["degree",0.0174532925199433]],
                    AXIS["geodetic longitude (Lon)",east,
                        ORDER[2],
                        ANGLEUNIT["degree",0.0174532925199433]],
                AREA["World"],
                BBOX[-90,-180,90,180],
                ID["EPSG",4322]]],
        TARGETCRS[
            GEODCRS["WGS 84",
                DATUM["World Geodetic System 1984",
                    ELLIPSOID["WGS 84",6378137,298.257223563,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                CS[ellipsoidal,2],
                    AXIS["latitude",north,
                        ORDER[1],
                        ANGLEUNIT["degree",0.0174532925199433]],
                    AXIS["longitude",east,
                        ORDER[2],
                        ANGLEUNIT["degree",0.0174532925199433]],
                ID["EPSG",4326]]],
        ABRIDGEDTRANSFORMATION["WGS 72 to WGS 84 (1)",
            METHOD["Position Vector transformation (geog2D domain)",
                ID["EPSG",9606]],
            PARAMETER["X-axis translation",0,
                ID["EPSG",8605]],
            PARAMETER["Y-axis translation",0,
                ID["EPSG",8606]],
            PARAMETER["Z-axis translation",4.5,
                ID["EPSG",8607]],
            PARAMETER["X-axis rotation",0,
                ID["EPSG",8608]],
            PARAMETER["Y-axis rotation",0,
                ID["EPSG",8609]],
            PARAMETER["Z-axis rotation",0.554,
                ID["EPSG",8610]],
            PARAMETER["Scale difference",1.0000002263,
                ID["EPSG",8611]],
            AREA["World"],
            BBOX[-90,-180,90,180],
            ID["EPSG",1237]]]

    OGC WKT2:2018 :
    BOUNDCRS[
        SOURCECRS[
            GEOGCRS["WGS 72",
                DATUM["World Geodetic System 1972",
                    ELLIPSOID["WGS 72",6378135,298.26,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                CS[ellipsoidal,2],
                    AXIS["geodetic latitude (Lat)",north,
                        ORDER[1],
                        ANGLEUNIT["degree",0.0174532925199433]],
                    AXIS["geodetic longitude (Lon)",east,
                        ORDER[2],
                        ANGLEUNIT["degree",0.0174532925199433]],
                USAGE[
                    SCOPE["unknown"],
                    AREA["World"],
                    BBOX[-90,-180,90,180]],
                ID["EPSG",4322]]],
        TARGETCRS[
            GEOGCRS["WGS 84",
                DATUM["World Geodetic System 1984",
                    ELLIPSOID["WGS 84",6378137,298.257223563,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                CS[ellipsoidal,2],
                    AXIS["latitude",north,
                        ORDER[1],
                        ANGLEUNIT["degree",0.0174532925199433]],
                    AXIS["longitude",east,
                        ORDER[2],
                        ANGLEUNIT["degree",0.0174532925199433]],
                ID["EPSG",4326]]],
        ABRIDGEDTRANSFORMATION["WGS 72 to WGS 84 (1)",
            METHOD["Position Vector transformation (geog2D domain)",
                ID["EPSG",9606]],
            PARAMETER["X-axis translation",0,
                ID["EPSG",8605]],
            PARAMETER["Y-axis translation",0,
                ID["EPSG",8606]],
            PARAMETER["Z-axis translation",4.5,
                ID["EPSG",8607]],
            PARAMETER["X-axis rotation",0,
                ID["EPSG",8608]],
            PARAMETER["Y-axis rotation",0,
                ID["EPSG",8609]],
            PARAMETER["Z-axis rotation",0.554,
                ID["EPSG",8610]],
            PARAMETER["Scale difference",1.0000002263,
                ID["EPSG",8611]],
            USAGE[
                SCOPE["unknown"],
                AREA["World"],
                BBOX[-90,-180,90,180]],
            ID["EPSG",1237]]]

    OGC WKT 1 (simple) :
    GEOGCS["WGS 72",
        DATUM["World_Geodetic_System_1972",
            SPHEROID["WGS 72",6378135,298.26],
            TOWGS84[0,0,4.5,0,0,0.554,0.2263]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433]]

    OGC WKT 1 (no CT) :
    GEOGCS["WGS 72",
        DATUM["World_Geodetic_System_1972",
            SPHEROID["WGS 72",6378135,298.26]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433]]

    ESRI WKT :
    GEOGCS["GCS_WGS_1972",
        DATUM["D_WGS_1972",
            SPHEROID["WGS_1972",6378135.0,298.26]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.0174532925199433]]
