.. _gdalinfo:

================================================================================
gdalinfo
================================================================================

.. only:: html

    래스터 데이터셋에 대한 정보를 목록화합니다.

.. Index:: gdalinfo

개요
--------

.. code-block::

    gdalinfo [--help-general] [-json] [-mm] [-stats | -approx_stats] [-hist] [-nogcp] [-nomd]
             [-norat] [-noct] [-nofl] [-checksum] [-proj4]
             [-listmdd] [-mdd domain|`all`]* [-wkt_format WKT1|WKT2|...]
             [-sd subdataset] [-oo NAME=VALUE]* [-if format]* datasetname

설명
-----------

:program:`gdalinfo` 프로그램은 GDAL이 지원하는 래스터 데이터셋에 대한 다양한 정보를 목록화합니다.

다음 명령줄 파라미터들은 순서에 상관없이 사용할 수 있습니다.

.. program:: gdalinfo

.. option:: -json

    산출물을 JSON 서식으로 표시합니다.

.. option:: -mm

    데이터셋에 있는 각 밴드에 대해 실제 최소/최대값을 강제로 계산합니다.

.. option:: -stats

    이미지 통계를 읽고 표시합니다. 이미지에 어떤 통계도 저장돼 있지 않다면 강제로 계산합니다.

.. option:: -approx_stats

    이미지 통계를 읽고 표시합니다. 이미지에 어떤 통계도 저장돼 있지 않다면 강제로 계산합니다. 하지만 이런 통계는 오버뷰를 또는 전체 타일의 하위 집합을 기반으로 계산된 것일 수도 있습니다. 급한 경우 쓸 만하지만 정확한 통계를 바라지는 마십시오.

.. option:: -hist

    모든 밴드에 대해 히스토그램 정보를 리포트합니다.

.. option:: -nogcp

    지상기준점(Ground Control Point) 목록을 표시하지 않습니다. 지상기준점 수 천 개를 담고 있는 L1B AVHRR 또는 HDF4 MODIS처럼 수많은 지상기준점을 가진 데이터셋을 입력하는 경우 이 옵션이 유용할 수도 있습니다.

.. option:: -nomd

    메타데이터를 표시하지 않습니다. 일부 데이터셋의 경우 수많은 메타데이터 문자열을 담고 있을 수도 있습니다.

.. option:: -norat

    래스터 속성 테이블을 표시하지 않습니다.

.. option:: -noct

    색상표(color table)를 표시하지 않습니다.

.. option:: -checksum

    데이터셋의 각 밴드에 대한 체크섬(checksum)을 강제로 계산합니다.

.. option:: -listmdd

    데이터셋에 대해 사용할 수 있는 모든 메타데이터 도메인을 목록화합니다.

.. option:: -mdd <domain>|all

    다음을 사용해서 메타데이터를 추가합니다:

    ``domain`` 지정한 도메인에 대한 메타데이터를 리포트합니다.

    ``all`` 모든 도메인에 대한 메타데이터를 리포트합니다.

.. option:: -nofl

    첫 번째 목록의 첫 번째 파일만 표시합니다.

.. option:: -wkt_format WKT1|WKT2|WKT2_2015|WKT2_2018

    공간 좌표계를 표시하기 위해 쓰이는 WKT 서식입니다.
    현재 다음과 같은 값들을 지원합니다:

    ``WKT1``

    ``WKT2`` (최신 WKT 버전, 현재 *WKT2_2018*)

    ``WKT2_2015``

    ``WKT2_2018``

    .. versionadded:: 3.0.0

.. option:: -sd <n>

    입력 데이터셋이 하위 데이터셋 몇 개를 담고 있는 경우 지정한 (1부터 시작하는) ``n`` 번만큼 하위 데이터셋을 읽고 표시합니다. 하위 데이터셋 이름 전체를 입력하는 대신 사용할 수 있는 방법입니다.

.. option:: -proj4

    파일의 좌표계에 해당하는 PROJ.4 문자열을 리포트합니다.

.. option:: -oo <NAME=VALUE>

    데이터셋 열기 옵션입니다(특정 포맷에 대응합니다).

.. include:: options/if.rst


gdalinfo는 다음 내용을 (알려져 있는 경우) 모두 리포트할 것입니다:

-  파일에 접근하기 위해 쓰인 포맷 드라이버.
-  래스터 크기(픽셀 및 행 단위).
-  파일의 좌표계(OGC WKT).
-  파일과 관련된 지리변환(geotransform). (현재 회전 계수(rotational coefficient)는 리포트되지 않습니다.)
-  지리참조된 모서리 좌표들, 가능한 경우 전체 지리변환을 기반으로 한 위도/경도(지상기준점은 제외).
-  지상기준점.
-  전체 파일의 (하위 데이터셋을 포함한) 메타데이터.
-  밴드 데이터 유형.
-  밴드 색상 해석(interpretation).
-  밴드 블록 크기.
-  밴드 설명.
-  밴드 최소/최대값(내부적으로 알려져 있고 가능하면 계산된 값).
-  밴드 체크섬(계산 과정에서 요청할 경우).
-  밴드 NODATA 값.
-  사용할 수 있는 밴드 오버뷰 해상도.
-  밴드 단위 유형(예: 표고 밴드 용 "meters" 또는 "feet").
-  밴드 의사색상표(pseudo-color table).

C API
-----

C에서도 이 유틸리티를 :cpp:func:`GDALInfo` 로 호출할 수 있습니다.

.. versionadded:: 2.1

예시
-------

.. code-block::

    gdalinfo ~/openev/utm.tif
    Driver: GTiff/GeoTIFF
    Size is 512, 512
    Coordinate System is:
    PROJCS["NAD27 / UTM zone 11N",
        GEOGCS["NAD27",
            DATUM["North_American_Datum_1927",
                SPHEROID["Clarke 1866",6378206.4,294.978698213901]],
            PRIMEM["Greenwich",0],
            UNIT["degree",0.0174532925199433]],
        PROJECTION["Transverse_Mercator"],
        PARAMETER["latitude_of_origin",0],
        PARAMETER["central_meridian",-117],
        PARAMETER["scale_factor",0.9996],
        PARAMETER["false_easting",500000],
        PARAMETER["false_northing",0],
        UNIT["metre",1]]
    Origin = (440720.000000,3751320.000000)
    Pixel Size = (60.000000,-60.000000)
    Corner Coordinates:
    Upper Left  (  440720.000, 3751320.000) (117d38'28.21"W, 33d54'8.47"N)
    Lower Left  (  440720.000, 3720600.000) (117d38'20.79"W, 33d37'31.04"N)
    Upper Right (  471440.000, 3751320.000) (117d18'32.07"W, 33d54'13.08"N)
    Lower Right (  471440.000, 3720600.000) (117d18'28.50"W, 33d37'35.61"N)
    Center      (  456080.000, 3735960.000) (117d28'27.39"W, 33d45'52.46"N)
    Band 1 Block=512x16 Type=Byte, ColorInterp=Gray
