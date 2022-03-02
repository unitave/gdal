.. _gdaldem:

================================================================================
gdaldem
================================================================================

.. only:: html

    DEM을 분석하고 가시화하는 도구입니다.

.. Index:: gdaldem

개요
--------

.. code-block::

    gdaldem <mode> <input> <output> <options>

GDAL이 지원하는 모든 표고 래스터로부터 음영기복도(shaded relief map)를 생성합니다:

.. code-block::

    gdaldem hillshade input_dem output_hillshade
                [-z ZFactor (default=1)] [-s scale* (default=1)]
                [-az Azimuth (default=315)] [-alt Altitude (default=45)]
                [-alg Horn|ZevenbergenThorne] [-combined | -multidirectional | -igor]
                [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

GDAL이 지원하는 모든 표고 래스터로부터 경사도(slope map)를 생성합니다:

.. code-block::

    gdaldem slope input_dem output_slope_map
                [-p use percent slope (default=degrees)] [-s scale* (default=1)]
                [-alg Horn|ZevenbergenThorne]
                [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

GDAL이 지원하는 모든 표고 래스터로부터 경사방향도(aspect map)를 생성해서 방위각을 의미하는 0에서 360까지의 픽셀 값을 가진 32비트 부동소수점 데이터 유형 래스터를 산출합니다:

.. code-block::

    gdaldem aspect input_dem output_aspect_map
                [-trigonometric] [-zero_for_flat]
                [-alg Horn|ZevenbergenThorne]
                [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

GDAL이 지원하는 모든 표고 래스터로부터 색상기복도(color relief map)를 생성합니다:

.. code-block::

    gdaldem color-relief input_dem color_text_file output_color_relief_map
                [-alpha] [-exact_color_entry | -nearest_color_entry]
                [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
    where color_text_file contains lines of the format "elevation_value red green blue"

GDAL이 지원하는 모든 표고 래스터로부터 지형 험상 지수(Terrain Ruggedness Index; TRI) 맵을 생성합니다:

.. code-block::

    gdaldem TRI input_dem output_TRI_map
                [-alg Wilson|Riley]
                [-compute_edges] [-b Band (default=1)] [-of format] [-q]

GDAL이 지원하는 모든 표고 래스터로부터 지형 위치 지수(Topographic Position Index; TPI) 맵을 생성합니다:

.. code-block::

    gdaldem TPI input_dem output_TPI_map
                [-compute_edges] [-b Band (default=1)] [-of format] [-q]

GDAL이 지원하는 모든 표고 래스터로부터 거칠기(roughness) 맵을 생성합니다:

.. code-block::

    gdaldem roughness input_dem output_roughness_map
                [-compute_edges] [-b Band (default=1)] [-of format] [-q]

설명
-----------

:program:`gdaldem` 은 일반적으로 x, y 및 z 단위가 동일하다고 가정합니다. x(동-서)와 y(남-북) 단위는 동일하지만 z(표고) 단위가 다른 경우, 척도(-s) 옵션을 사용해서 수직 단위와 수평 단위의 비율을 설정할 수 있습니다. 적도에 가까운 위도/경도 투영법의 경우 (표고가 피트 단위일 때) scale=370400, 또는 (표고가 미터 단위일 때) scale=111120을 사용하면 표고(z) 단위가 호환되도록 변환할 수 있습니다. 적도에 가까운 위치가 아니라면, gdaldem을 사용하기 전에 gdalwarp를 사용해서 사용자의 그리드를 재투영하는 방법이 최선일 것입니다.

.. option:: <mode>

    <mode> 위치에 다음 7개 모드 가운데 하나를 사용할 수 있습니다:

    * ``hillshade``

        GDAL이 지원하는 모든 표고 래스터로부터 음영기복도(shaded relief map)를 생성합니다.

    * ``slope``

        GDAL이 지원하는 모든 표고 래스터로부터 경사도(slope map)를 생성합니다.

    * ``aspect``

        GDAL이 지원하는 모든 표고 래스터로부터 경사방향도(aspect map)를 생성합니다.

    * ``color-relief``

        GDAL이 지원하는 모든 표고 래스터로부터 색상기복도(color relief map)를 생성합니다.

    * ``TRI``

        GDAL이 지원하는 모든 표고 래스터로부터 지형 험상 지수(Terrain Ruggedness Index; TRI) 맵을 생성합니다.

    * ``TPI``

        GDAL이 지원하는 모든 표고 래스터로부터 지형 위치 지수(Topographic Position Index; TPI) 맵을 생성합니다.

    * ``roughness``

        GDAL이 지원하는 모든 표고 래스터로부터 거칠기(roughness) 맵을 생성합니다.

다음 일반 옵션들을 사용할 수 있습니다:

.. option:: input_dem

    처리할 입력 DEM 래스터입니다.

.. option:: output_xxx_map

    생산한 산출 래스터입니다.

.. option:: -of <format>

    산출물 포맷을 선택합니다.

    .. versionadded:: 2.3.0

        지정하지 않는 경우, 확장자로부터 포맷을 추정합니다. (이전 버전까지는 :ref:`raster.gtiff` 를 사용했습니다.) 단축 포맷명을 사용하십시오.

.. option:: -compute_edges

    래스터 경계와 NODATA 값에 근접한 위치에서 계산을 수행합니다.

.. option:: -b <band>

    처리할 입력 밴드를 선택합니다. 밴드 번호는 1부터 시작합니다.

.. include:: options/co.rst

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

색상기복을 제외한 모든 알고리즘에서, 각 소스 픽셀을 중심으로 하는 3x3 창 안에서 NODATA 값으로 설정된 픽셀이 하나라도 탐지되는 경우, 대상 데이터셋에서 NODATA 값을 누락시킬 것입니다. 그 결과 NODATA 값이 설정된 각 이미지를 둘러싼 픽셀 1개 두께의 경계선이 생길 것입니다.

    :option:`-compute_edges` 를 지정한 경우, gdaldem이 이미지 경계에서 값을 계산할 것입니다. 또는 3x3 창 안에서 NODATA 값을 하나라도 탐지한 경우, 누락된 값을 보간해서 계산할 것입니다.

모드
-----

hillshade
^^^^^^^^^

이 명령어는 보기 좋은 음영기복 효과를 준 8비트 래스터를 산출합니다. 지형을 가시화하는 데 매우 유용한 모드입니다. 광원의 방위각과 고도를 선택적으로 지정할 수 있고, 수직 과장 인자 및 수직과 수평 단위의 차이를 조정하기 위한 척도 인자도 지정할 수 있습니다.

0을 산출 NODATA 값으로 사용합니다.

다음 특화 옵션을 사용할 수 있습니다:

.. option:: -alg Horn|ZevenbergenThorne

    문헌에 따르면 체벤베르겐 & 손(Zevenbergen & Thorne) 공식은 매끄러운 풍경에 더 적합한 반면, 혼(Horn) 공식은 거친 지형에서 더 나은 결과를 보인다고 합니다.

.. option:: -z <factor>

    표고를 사전에 증가시키기 위해 쓰이는 수직 강조 인자입니다.

.. option:: -s <scale>

    수직 단위와 수평 단위의 비율입니다. 소스 DEM의 수평 단위가 도(예: 위도/경도 WGS84 투영법)인 경우, 수평 단위가 미터라면 scale=111120 을 (또는 피트라면 scale=370400을) 사용하면 됩니다.

.. option:: -az <azimuth>

    광원의 (도 단위) 방위각입니다. 래스터 위 수직 방향에서 빛이 온다면 0, 동쪽 방향에서 온다면 90, ... 기본값인 315는 음영기복도를 생산할 때 일반적으로 쓰이는 값이기 때문에 변경해야 할 일은 거의 없습니다.

.. option:: -alt <altitude>

    광원의 (도 단위) 고도입니다. DEM 위 수직 방향에서 빛이 온다면 90이고, 지평선에 평행하게 온다면 0입니다.

.. option:: -combined

    경사와 사선 음영을 결합한 결합 음영을 산출합니다.

.. option:: -multidirectional

    225도, 270도, 315도, 그리고 360도 방위각으로부터 빛을 비춘 음영기복을 결합한 다중방향 음영을 산출합니다.

    .. versionadded:: 2.2

.. option:: -igor

    음영이 아래 있는 다른 맵 객체에 미치는 영향을 최소화시킵니다. -alt 옵션과 함께 사용해서는 안 됩니다.

    .. versionadded:: 3.0

다중방향 음영은 http://pubs.usgs.gov/of/1992/of92-422/of92-422.pdf 의 공식을 적용합니다.

이고르(Igor) 음영은 Maperitive의 http://maperitive.net/docs/Commands/GenerateReliefImageIgor.html 에서 나온 공식을 사용합니다.

slope
^^^^^

이 명령어는 DEM 래스터를 입력받아 경사 값을 가진 32비트 부동소수점 데이터 유형 래스터를 산출합니다. 사용자가 원하는 경사 값 유형을 지정할 수 있는 옵션이 있습니다: 도 또는 백분율 경사입니다. 수평 단위와 수직 단위가 다른 경우, 척도 인자도 지정할 수 있습니다.

`-9999` 값을 산출 NODATA 값으로 사용합니다.

다음 특화 옵션을 사용할 수 있습니다:

.. option:: -alg Horn|ZevenbergenThorne

    문헌에 따르면 체벤베르겐 & 손(Zevenbergen & Thorne) 공식은 매끄러운 풍경에 더 적합한 반면, 혼(Horn) 공식은 거친 지형에서 더 나은 결과를 보인다고 합니다.

.. option:: -p

    이 옵션을 지정하면, 경사가 백분율로 표현될 것입니다. 지정하지 않으면 도 단위로 표현됩니다.

.. option:: -s

    수직 단위와 수평 단위의 비율입니다. 소스 DEM의 수평 단위가 도(예: 위도/경도 WGS84 투영법)인 경우, 수평 단위가 미터라면 s=111120 을 (또는 피트라면 s=370400을) 사용하면 됩니다.

aspect
^^^^^^

이 명령어는 경사면이 향하고 있는 방위각을 표현하는 0°에서 360°까지의 값을 가진 32비트 부동소수점 데이터 유형 래스터를 산출합니다. 방위각의 정의는 다음과 같습니다: (사용자의 입력 래스터의 위쪽이 북쪽 방향이라는 가정 하에) 0°는 경사면이 정북을 향하고 있다는 의미이고, 90°는 정동, 180°는 정남 그리고 270°는 정서를 향하고 있다는 뜻입니다. 경사방향 값 -9999를 경사가 0인 평지에서 정의되지 않는 경사방향을 의미하는 NODATA 값으로 사용합니다.

다음 특화 옵션을 사용할 수 있습니다:

.. option:: -alg Horn|ZevenbergenThorne

    문헌에 따르면 체벤베르겐 & 손(Zevenbergen & Thorne) 공식은 매끄러운 풍경에 더 적합한 반면, 혼(Horn) 공식은 거친 지형에서 더 나은 결과를 보인다고 합니다.

.. option:: -trigonometric

    방위각 대신 삼각함수 각도를 반환합니다. 즉 0°가 정동, 90°가 정북, 180°가 정서, 270°가 정남을 의미합니다.

.. option:: -zero_for_flat

    경사가 0인 평지의 경우 -9999 대신 0을 반환합니다.

이 옵션 2개를 사용하면, gdaldem이 반환하는 경사방향은 GRASS r.slope.aspect가 반환하는 경사방향과 동일할 것입니다. 사용하지 않는 경우, 매슈 페리(Matthew Perry)의 :file:`aspect.cpp` 유틸리티가 반환하는 경사방향과 동일합니다.

color-relief
^^^^^^^^^^^^

이 명령어는 다양한 표고 값과 그에 대응하는 원하는 색상 간의 조합을 담고 있는 텍스트 기반 색상 환경설정 파일과 표고로부터 계산된 값을 가진 밴드 3개(RGB) 또는 밴드 4개(RGBA) 래스터를 산출합니다. 기본적으로 입력된 표고 값들 사이의 색상들은 부드럽게 혼합되어 그 결과 보기 좋게 색을 입힌 DEM을 생성합니다. -exact_color_entry 또는 -nearest_color_entry 옵션을 사용해서 색상 환경설정 파일의 색인과 일치하지 않는 값에 대한 선형 보간을 방지할 수 있습니다.

다음 특화 옵션을 사용할 수 있습니다:

.. option:: color_text_file

    텍스트 기반 색상 환경설정 파일

.. option:: -alpha

    산출 래스터에 알파 채널을 추가합니다.

.. option:: -exact_color_entry

    색상 환경설정 파일을 검색할 때 엄격한 일치 기준을 사용합니다. 일치하는 색상 항목을 찾지 못 하는 경우, "0,0,0,0"이라는 RGBA 4개 값을 사용할 것입니다.

.. option:: -nearest_color_entry

    색상 환경설정 파일에서 가장 근접한 항목에 해당하는 RGBA 4개 값을 사용합니다.

색상기복 모드는 산출물 포맷으로 VRT를 지원하는 유일한 모드입니다. 이런 경우, 색상 환경설정 파일을 적절한 LUT 요소로 변환할 것입니다. 백분율로 지정된 표고를 절대값으로 변환할 것이라는 점을 기억하십시오. 이때 소스 래스터의 통계가 VRT를 작성할 때 쓰였던 래스터의 통계와 다를 경우 이 절대값을 고려해야만 합니다.

텍스트 기반 색상 환경설정 파일은 일반적으로 행마다 열 4개를 담고 있습니다: 표고 값과 그에 대응하는 (0에서 255 사이의) 적색(Red), 녹색(Green), 청색(Blue) 구성요소입니다. 표고 값은 모든 부동소수점 값을 지원하며, NODATA 값의 경우 nv 키워드를 쓸 수 있습니다. 표고를 백분율로도 표현할 수 있습니다: 래스터에서 검색된 최저값을 0%, 최고값을 100%로 표현합니다.

알파 구성요소를 위해 추가적인 열을 선택적으로 추가할 수 있습니다. 이 열을 지정하지 않는 경우, 완전히 불투명(255)하다고 가정합니다.

다양한 필드 구분자(field separator)를 지원합니다: 쉼표, 표, 공백, 쌍점(':').

GRASS가 사용하는 공통 색상도, RGB 3개 값 대신 색상 이름을 사용해서 지정할 수 있습니다. 지원하는 색상 목록은: white, black, red, green, blue, yellow, magenta, cyan, aqua, grey/gray, orange, brown, purple/violet 및 indigo 입니다.

    GMT :file:`.cpt` 색상표(palette) 파일도 지원합니다(COLOR_MODEL = RGB 전용).

주의: 색상 환경설정 파일의 문법은 GRASS r.colors 유틸리티가 지원하는 문법으로부터 파생된 것입니다. ESRI HDR 색상표 파일(.clr)도 해당 문법과 일치합니다. 구분자로 탭과 쉼표를 지원하는 것과 알파 구성요소는 GDAL에 특화된 확장 기능입니다.

예를 들면:

::

    3500   white
    2500   235:220:175
    50%   190 185 135
    700    240 250 150
    0      50  180  50
    nv     0   0   0   0


"하한값으로 반올림(round to the floor value)" 모드를 구현하려면, 표고 값을 한계값보다 살짝 위에 있는 새로운 값으로 복제할 수 있어야 합니다. 예를 들어 적색을 [0,10], 녹색을 [10,20], 청색을 [20,30] 표고 값으로 조합시키려면:

::

    0       red
    10      red
    10.001  green
    20      green
    20.001  blue
    30      blue

TRI
^^^

이 명령어는 표고로부터 계산된 값을 가진 단일 밴드 래스터를 산출합니다. `TRI` 는 지형 험상 지수(Terrain Ruggedness Index)의 약어로, 중심 픽셀과 중심 픽셀을 감싸고 있는 셀들 사이의 차이를 측정합니다.

-9999값을 산출 NODATA 값으로 사용합니다.

다음 옵션을 사용할 수 있습니다:

.. option:: -alg Wilson|Riley

    GDAL 3.3버전부터, 라일리(Riley) 알고리즘과 새로운 기본값을 사용할 수 있습니다. (Riley, S.J., De Gloria, S.D., Elliot, R. (1999): A Terrain Ruggedness that Quantifies Topographic Heterogeneity. Intermountain Journal of Science, Vol.5, No.1-4, pp.23-27 참조) 이 알고리즘은 중심 픽셀과 중심 픽셀을 감싸고 있는 셀들 사이의 차이를 제곱한 값들을 모두 더한 값의 제곱근을 이용합니다. 지상 사용(terrestrial use) 사례에 사용하면 좋습니다.

    윌슨(Wilson) 알고리즘은 중심 픽셀과 중심 픽셀을 감싸고 있는 셀들 사이의 차이의 평균을 이용합니다. (Wilson et al 2007, Marine Geodesy 30:3-35 참조) 심해 사용(bathymetric use) 사례에 사용하면 좋습니다.

TPI
^^^

이 명령어는 표고로부터 계산된 값을 가진 단일 밴드 래스터를 산출합니다. `TPI` 는 지형 위치 지수(Topographic Position Index)의 약어로, 중심 픽셀과 중심 픽셀을 감싸고 있는 셀들의 평균 사이의 차이로 정의됩니다. (Wilson et al 2007, Marine Geodesy 30:3-35 참조)

-9999값을 산출 NODATA 값으로 사용합니다.

특화 옵션이 없습니다.

roughness
^^^^^^^^^

이 명령어는 표고로부터 계산된 값을 가진 단일 밴드 래스터를 산출합니다. 거칠기란 Wilson et al 2007, Marine Geodesy 30:3-35에 정의된대로 중심 픽셀과 중심 픽셀을 감싸고 있는 셀들 사이의 차이 가운데 가장 큰 값입니다.

-9999값을 산출 NODATA 값으로 사용합니다.

특화 옵션이 없습니다.

C API
-----

C에서 :cpp:func:`GDALDEMProcessing` 을 호출하면 이 유틸리티의 기능을 수행할 수 있습니다.

.. versionadded:: 2.1

작성자
-------

매슈 페리(Matthew Perry) perrygeo@gmail.com, 이반 루오(Even Rouault) even.rouault@spatialys.com,
하워드 버틀러(Howard Butler) hobu.inc@gmail.com, 크리스 예슨(Chris Yesson) chris.yesson@ioz.ac.uk

마이클 샤피로(Michael Shapiro), 올가 바우포티치(Olga Waupotitsch), 마조리 라슨(Marjorie Larson), 짐 웨스터벨트(Jim Westervelt)가 작성한 코드에서 파생: 미육군 건축공학연구소, 1993. GRASS 4.1 참조 지침서. 미육군 공병대, 건축공학연구소, 일리노이 주 샴페인 시, 1-425.

참고
--------

관련 GRASS 유틸리티 문서:

https://grass.osgeo.org/grass79/manuals/r.slope.aspect.html

https://grass.osgeo.org/grass79/manuals/r.relief.html

https://grass.osgeo.org/grass79/manuals/r.colors.html
