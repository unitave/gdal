.. _gdal_viewshed:

================================================================================
gdal_viewshed
================================================================================

.. only:: html

    .. versionadded:: 3.1.0

    입력 DEM 래스터에 있는 사용자 정의 포인트에 대해 [Wang2000]_ 에 정의된 메소드를 이용해서 가시권(viewshed) 래스터를 계산합니다.

.. Index:: gdal_viewshed

개요
--------

.. code-block::

   gdal_viewshed [-b <band>]
                 [-a_nodata <value>] [-f <formatname>]
                 [-oz <observer_height>] [-tz <target_height>] [-md <max_distance>]
                 -ox <observer_x> -oy <observer_y>
                 [-vv <visibility>] [-iv <invisibility>]
                 [-ov <out_of_range>] [-cc <curvature_coef>]
                 [[-co NAME=VALUE] ...]
                 [-q] [-om <output mode>]
                 <src_filename> <dst_filename>

설명
-----------

기본적으로 :program:`gdal_viewshed` 는 입력 DEM 래스터의 밴드 1개로부터 바이너리 가시성 래스터를 생성합니다. 산출 래스터는 바이트 유형이 될 것입니다. -mode 플래그를 사용하면 Float64 유형의 최저 가시 높이(minimum visible height) 래스터도 반환할 수 있습니다.

.. note::
    
    현재 구현된 알고리즘은 투영 좌표계로 지리참조된 경우에만 의미 있는 결과물을 산출할 것입니다.

.. program:: gdal_viewshed

.. include:: options/co.rst

.. option:: -b <band>

    DEM 데이터를 담고 있는 입력 **밴드** 를 선택합니다. 밴드 번호는 1부터 시작합니다. 단일 밴드 1개만 사용합니다. 관찰자(observer) 포인트를 중심으로 지정한 최장 거리 내에 있는 래스터 부분만 처리합니다.

.. option:: -a_nodata <value>

    산출 래스터에 있는 NODATA 셀에 설정할 값입니다.

   .. note::

        현재, 입력물에서 셀이 NODATA인 경우 어떤 특별한 처리도 하지 않습니다. (잘못된 결과물이 나올 수도 있습니다.)

.. option:: -ox <value>

    관찰자의 (공간 좌표계 단위) X 위치입니다.

.. option:: -oy <value>

    관찰자의 (공간 좌표계 단위) Y 위치입니다.

.. option:: -oz <value>

    DEM 표면 위에 있는 DEM의 높이 단위의 관찰자 높이입니다. 기본값은 2입니다.

.. option:: -tz <value>

    DEM 표면 위에 있는 DEM의 높이 단위의 대상 높이입니다. 기본값은 0입니다.

.. option:: -md <value>

    관찰자로부터 가시성을 계산하기 위한 최장 거리입니다. 산출 래스터의 범위를 좁히기 위해서도 사용합니다.

.. option:: -cc <value>

    곡률(curvature)과 굴절(refraction)의 영향을 고려하기 위한 계수(coefficient)입니다. 두 포인트 사이의 가시성을 계산할 때 (예: 가시선(Line Of Sight) 또는 가시권(Viewshed)) 이 영향의 강도는 대기 조건 및 파장에 따라 변화합니다.

    가시성을 계산하기 위한 서로 다른 응용 프로그램들은 이 현상을 설명하기 위해 서로 다른 교환 가능한 표기법을 사용합니다: 굴절 계수, 곡률 계수, 그리고 구체 직경 계수(Sphere Diameter Factor). gdal_viewshed는 곡률 계수 표기법을 사용합니다.

    .. math::

        {CurvCoeff}=1-{RefractionCoeff}

    공기 밀도가 변화하면 빛을 아래쪽으로 구부려 관찰자가 더 멀리 볼 수 있게 하고, 마치 구체(지구)의 직경이 실제보다 더 길어진 것처럼 지구가 덜 휘어 보이게 합니다. 다음 공식이 이런 상상 속의 구체 직경과 실제 구체 직경 간의 비율을 계산합니다:

    .. math::

        {SphereDiameterFactor}=1/{CurvCoeff}=1/(1-{RefractionCoeff})

    가시 광선의 경우, 일반적으로 쓰이는 표준 대기 굴절 계수는 1/7입니다. 따라서 (GDAL 3.4버전부터) gdal_viewshed가 사용하는 CurvCoeff의 기본값은 0.85714(1 - 1/7의 근사치)입니다.

    다음 공식에 따라 DEM의 높이를 수정합니다:

    .. math::

        Height_{Corrected}=Height_{DEM}-{CurvCoeff}\frac{{TargetDistance}^2}{SphereDiameter}

    다음 표는 전형적인 계수 값들을 보여줍니다. (-cc 옵션에는 곡률 계수를 사용하십시오.)

    ================  ==================  ===================  =====================
    이용사례           굴절 계수            **곡률 계수**         구체 직경 계수
    굴절 없음          0                   1                    1
    가시 광선          1/7                 6/7 (=~0.85714)      7/6 (=~1.1666)
    무선 전파          0.25 ~ 0.325        0.75 ~ 0.675         1.33 ~ 1.48
    평평한 지구        1                   0                    inf
    ================  ==================  ===================  =====================

.. option:: -iv <value>

    보이지 않는 영역에 설정할 픽셀 값입니다. 기본값은 0입니다.

.. option:: -ov <value>

    관찰자 위치와 최장 거리로 지정된 범위 바깥에 있는 셀들에 설정할 픽셀 값입니다. 기본값은 0입니다.

.. option:: -vv <value>

    보이는 영역에 설정할 픽셀 값입니다. 기본값은 255입니다.

.. option:: -om <output mode>

    산출물이 어떤 정보를 담을지를 설정합니다.

    사용할 수 있는 값: NORMAL, DEM, GROUND

    NORMAL은 보이는 위치들을 담고 있는 바이트 유형의 래스터를 반환합니다.

    DEM과 GROUND는 DEM 표면 또는 지표면에서 각각 보이는 대상의 최저 대상 높이를 담고 있는 Float64 유형의 래스터를 반환할 것입니다. -tz, -iv 및 -vv 플래그는 무시할 것입니다.

    기본값은 NORMAL입니다.

C API
-----

C에서 :cpp:func:`GDALViewshedGenerate` 를 호출하면 이 유틸리티의 기능을 사용할 수 있습니다.

예시
-------

표고 래스터 데이터소스의 가시성을 기본값으로 계산합니다:


.. figure:: ../../images/gdal_viewshed.png

    DEM 상에서 개별 `-ox` 와 `-oy` 포인트 2개에 대해 계산된 가시성

.. code-block::

    gdal_viewshed -md 500 -ox -10147017 -oy 5108065 source.tif destination.tif


.. [Wang2000]::
    Generating Viewsheds without Using Sightlines. Wang, Jianjun,
    Robinson, Gary J., and White, Kevin. Photogrammetric Engineering and Remote
    Sensing. p81. https://www.asprs.org/wp-content/uploads/pers/2000journal/january/2000_jan_87-90.pdf
