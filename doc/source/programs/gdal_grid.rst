.. _gdal_grid:

================================================================================
gdal_grid
================================================================================

.. only:: html

    분산 데이터로부터 정규 그리드를 생성합니다.

.. Index:: gdal_grid

개요
--------

.. code-block::

    gdal_grid [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
              CInt16/CInt32/CFloat32/CFloat64}]
              [-of format] [-co "NAME=VALUE"]
              [-zfield field_name] [-z_increase increase_value] [-z_multiply multiply_value]
              [-a_srs srs_def] [-spat xmin ymin xmax ymax]
              [-clipsrc <xmin ymin xmax ymax>|WKT|datasource|spat_extent]
              [-clipsrcsql sql_statement] [-clipsrclayer layer]
              [-clipsrcwhere expression]
              [-l layername]* [-where expression] [-sql select_statement]
              [-txe xmin xmax] [-tye ymin ymax] [-tr xres yres] [-outsize xsize ysize]
              [-a algorithm[:parameter1=value1]*] [-q]
              <src_datasource> <dst_filename>

설명
-----------

이 프로그램은 OGR 데이터소스에서 읽어온 분산 데이터(scattered data)로부터 정규 그리드(래스터)를 생성합니다. 그리드 노드를 값으로 채우기 위해 입력 데이터를 보간하는데, 다양한 보간 메소드 가운데 선택할 수 있습니다.

프로세스를 병렬화하려면 ``GDAL_NUM_THREADS`` 환경설정 옵션을 설정하면 됩니다. 지정한 값이 작업 스레드의 개수가 되고, 또는 ``ALL_CPUS`` 로 설정하면 컴퓨터의 모든 코어/CPU를 사용합니다.

.. program:: gdal_grid

.. include:: options/ot.rst

.. include:: options/of.rst

.. option:: -txe <xmin> <xmax>

    생성할 산출물 파일의 지리참조된 X 범위를 설정합니다.

.. option:: -tye <ymin> <ymax>

    생성할 산출물 파일의 지리참조된 Y 범위를 설정합니다.

.. option:: -tr <xres> <yres>

    산출물 파일의 해상도를 (대상 지리참조 단위로) 설정합니다. :option:`-txe` 및 :option:`-tye` 로부터 나온 무결한 입력물을 사용하면 :option:`-tr` 옵션은 그냥 작동한다는 사실을 기억하십시오.

    .. versionadded:: 3.2

.. option:: -outsize <xsize ysize>

    산출 파일의 크기를 픽셀 및 라인 단위로 설정합니다. :option:`-outsize` 와 :option:`-tr` 를 함께 사용할 수 없다는 사실을 기억하십시오.

.. option:: -a_srs <srs_def>

    산출물 파일의 투영법을 무시합니다. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다. 어떤 재투영도 하지 않습니다.

.. option:: -zfield <field_name>

    Z 값을 가져오기 위해 사용할 객체의 속성 필드를 식별합니다. 이 값이 객체 도형 레코드에서 읽어온 Z 값을 무시합니다. (당연히, 도형이 Z 값을 가지고 있는 경우입니다. 그렇지 않다면 Z 값을 담고 있는 필드 이름을 지정하는 수밖에 없습니다.)

.. option:: -z_increase <increase_value>

    Z 값을 가져오기 위해 사용할 객체의 속성 필드에 더할 값입니다. 이 증가값은 Z 값과 동일한 단위여야 합니다. Z 값과 Z 증가값의 합계를 산출할 것입니다. 기본값은 0입니다.

.. option:: -z_multiply <multiply_value>

    Z 필드의 값에 곱할 배수입니다. 예를 들면 피트 단위를 미터 단위로 바꾸거나 표고를 깊이로 바꾸는 데 사용할 수 있습니다. (Z 값 + Z 증가값) * Z 배수값의 결과를 산출할 것입니다. 기본값은 1입니다.

.. option:: -a <[algorithm[:parameter1=value1][:parameter2=value2]...]>

    보간 알고리즘 또는 데이터 메트릭 이름 및 (선택적으로) 데이터 메트릭의 파라미터를 설정합니다. 사용할 수 있는 옵션에 대해 자세히 알고 싶다면 `Interpolation algorithms`_ 및 `Data metrics`_ 단락을 읽어보십시오.

.. option:: -spat <xmin> <ymin> <xmax> <ymax>

    (xmin, ymin) - (xmax, ymax)가 나타내는 경계상자 내부에 담겨 있는 객체들만 선택하려면 이 공간 필터를 추가하십시오.

.. option:: -clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent

    지정한 (소스 공간 좌표계로 표현된) 경계상자 또는 WKT 도형(폴리곤 또는 멀티폴리곤) 내부에 담겨 있는, 또는 데이터소스로부터 나온, 또는 ``spat_extent`` 키워드를 사용한 경우 :option:`-spat` 옵션의 공간 범위에 있는 객체들만 선택하려면 이 공간 필터를 추가하십시오. 데이터소스를 지정하는 경우, 일반적으로  :option:`-clipsrclayer`, :option:`-clipsrcwhere` 또는 :option:`-clipsrcsql` 옵션과 함께 사용하게 될 것입니다.

.. option:: -clipsrcsql <sql_statement>

    SQL 쿼리를 대신 사용해서 원하는 도형을 선택합니다.

.. option:: -clipsrclayer <layername>

    소스 클립 데이터소스로부터 지정한 레이어를 선택합니다.

.. option:: -clipsrcwhere <expression>

    속성 쿼리를 기반으로 원하는 도형을 제한합니다.

.. option:: -l <layername>

    입력 객체로 사용될, 데이터소스에서 나온 레이어(들)를 설정합니다. 여러 번 지정할 수도 있지만, 최소한 레이어 이름 하나 또는 :option:`-sql` 옵션 하나를 지정해야만 합니다.

.. option:: -where <expression>

    입력 레이어(들)에서 나온, 처리할 객체를 선택하기 위해 적용되는, 선택적인 SQL WHERE 스타일의 쿼리 표현식입니다.

.. option:: -sql <select_statement>

    처리할 객체의 가상 레이어를 생성하기 위한 데이터소스를 대상으로 평가될 SQL 선언문입니다.

.. include:: options/co.rst

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

.. option:: <src_datasource>

    OGR이 지원하는 읽기 가능한 모든 데이터소스를 설정할 수 있습니다.

.. option:: <dst_filename>

    GDAL이 지원하는 산출물 파일입니다.


보간 알고리즘
------------------------

선택할 수 있는 보간 알고리즘이 여러 개 있습니다.

:ref:`gdal_grid_tut` 에서 보간 알고리즘에 대해 더 자세히 알 수 있습니다.

.. _gdal_grid_invdist:

invdist
+++++++

역거리 거듭제곱 가중치 보간법(inverse distance to a power). 기본 알고리즘입니다. 다음 파라미터를 사용합니다:

- ``power``: 가중치 거듭제곱 지수 (기본값은 2.0)
- ``smoothing``: 평활화(smoothing) 파라미터 (기본값은 0.0)
- ``radius1``: 검색 타원의 첫 번째 반경(기울기 각도가 0인 경우 X축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``radius2``: 검색 타원의 두 번째 반경(기울기 각도가 0인 경우 Y축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``angle``: 검색 타원 기울기의 도 단위 각도입니다. (반시계 방향, 기본값은 0.0)
- ``max_points``: 사용할 데이터 포인트의 최대 개수. 이 개수 이하의 포인트만 검색합니다. (두 반경 모두 0이 아닌) 검색 타원을 설정한 경우에만 사용됩니다. 0으로 설정하면 검색된 모든 포인트를 사용합니다. 기본값은 0입니다.
- ``min_points``: 사용할 데이터 포인트의 최소 개수. 이 개수 미만의 포인트가 발견된 그리드 노드는 비어 있다고 간주되어 NODATA 마커로 채워질 것입니다. (두 반경 모두 0이 아닌) 검색 타원을 설정한 경우에만 사용됩니다. 기본값은 0입니다.
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)

invdistnn
+++++++++

.. versionadded:: 2.1

최근접 이웃을 검색하는 역거리 거듭제곱 가중치 보간법. max_points를 사용하는 경우 이상적입니다. 다음 파라미터를 사용합니다:

- ``power``: 가중치 거듭제곱 지수 (기본값은 2.0)
- ``smoothing``: 평활화(smoothing) 파라미터 (기본값은 0.0)
- ``radius``: 검색 원의 반경으로, 0이어서는 안 됩니다. 기본값은 1.0입니다.
- ``max_points``: 사용할 데이터 포인트의 최대 개수. 이 개수 이하의 포인트만 검색합니다. 가중치 작업 시 검색된 포인트를 최근접에서 최원격까지 순위를 매길 것입니다. 기본값은 12입니다.
- ``min_points``: 사용할 데이터 포인트의 최소 개수. 이 개수 미만의 포인트가 발견된 그리드 노드는 비어 있다고 간주되어 NODATA 마커로 채워질 것입니다. 기본값은 0입니다.
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)


.. _gdal_grid_average:

average
+++++++

이동 평균(moving average) 알고리즘입니다. 다음 파라미터를 사용합니다:

- ``radius1``: 검색 타원의 첫 번째 반경(기울기 각도가 0인 경우 X축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``radius2``: 검색 타원의 두 번째 반경(기울기 각도가 0인 경우 Y축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``angle``: 검색 타원 기울기의 도 단위 각도입니다. (반시계 방향, 기본값은 0.0)
- ``min_points``: 사용할 데이터 포인트의 최소 개수. 이 개수 미만의 포인트가 발견된 그리드 노드는 비어 있다고 간주되어 NODATA 마커로 채워질 것입니다. 기본값은 0입니다.
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)

이동 평균 메소드 용 검색 타원을 반드시 설정해야 한다는 점을 기억하십시오. 그리드 노드 값 계산 시 이 창 안에 들어오는 모든 데이터 포인트의 평균을 계산할 것입니다.

.. _gdal_grid_nearest:

nearest
+++++++

최근접 이웃(nearest neighbor) 알고리즘입니다. 다음 파라미터를 사용합니다:

- ``radius1``: 검색 타원의 첫 번째 반경(기울기 각도가 0인 경우 X축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``radius2``: 검색 타원의 두 번째 반경(기울기 각도가 0인 경우 Y축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``angle``: 검색 타원 기울기의 도 단위 각도입니다. (반시계 방향, 기본값은 0.0)
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)

linear
++++++

.. versionadded:: 2.1

선형 보간 알고리즘입니다.

선형 메소드는 점구름(point cloud)의 들로네 삼각분할(Delaunay triangulation)을 계산해서 선형 보간을 수행합니다. 포인트가 삼각분할의 어느 삼각형 안에 있는지 찾은 다음, 해당 삼각형 내부의 무게중심 좌표로부터 선형 보간을 수행합니다. 포인트가 어떤 삼각형에도 들어가지 않는 경우, 이 알고리즘은 검색 반경에 따라 최근접 포인트의 값 또는 NODATA 값을 사용할 것입니다.

다음 파라미터를 사용합니다:

- ``radius``: 보간할 포인트가 들로네 삼각분할의 삼각형 안에 들어가지 않는 경우, 이 최대 거리를 사용해서 최근접 이웃을 찾거나 또는 최대 거리 안에 최근접 이웃이 없다면 NODATA를 사용합니다. 이 파라미터를 -1로 설정하면, 검색 반경이 무한대가 됩니다. 0으로 설정하면 항상 NODATA 값을 사용할 것입니다. 기본값은 -1입니다.
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)

데이터 메트릭
------------

보간 기능 이외에도, :ref:`gdal_grid` 는 지정한 창과 산출 그리드 도형을 사용해서 몇몇 데이터 메트릭(data metrics)을 계산할 수 있습니다. 다음과 같은 메트릭을 계산합니다:

- ``minimum``: 그리드 노드 검색 타원에서 발견된 최소값

- ``maximum``: 그리드 노드 검색 타원에서 발견된 최대값

- ``range``: 그리드 노드 검색 타원에서 발견된 최소값과 최대값의 차

- ``count``:  그리드 노드 검색 타원에서 발견된 데이터 포인트의 개수

- ``average_distance``: 그리드 노드(검색 타원의 중심)와 그리드 노드 검색 타원에서 발견된 모든 데이터 포인트 사이의 평균 거리

- ``average_distance_pts``: 그리드 노드 검색 타원에서 발견된 데이터 포인트들 사이의 평균 거리. 타원 내부에 있는 각 포인트쌍 사이의 거리를 계산하고 그 모든 거리의 평균을 그리드 노드 값으로 설정합니다.

모든 메트릭이 동일한 옵션을 가지고 있습니다:

- ``radius1``: 검색 타원의 첫 번째 반경(기울기 각도가 0인 경우 X축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``radius2``: 검색 타원의 두 번째 반경(기울기 각도가 0인 경우 Y축), 포인트 배열 전체를 사용하려면 이 파라미터를 0으로 설정하십시오. 기본값은 0.0입니다.
- ``angle``: 검색 타원 기울기의 도 단위 각도입니다. (반시계 방향, 기본값은 0.0)
- ``min_points``: 사용할 데이터 포인트의 최소 개수. 이 개수 미만의 포인트가 발견된 그리드 노드는 비어 있다고 간주되어 NODATA 마커로 채워질 것입니다. (두 반경 모두 0이 아닌) 검색 타원을 설정한 경우에만 사용됩니다. 기본값은 0입니다.
- ``nodata``: 비어 있는 포인트를 채울 NODATA 마커 (기본값은 0.0)

쉼표로 분리된 값 읽기
------------------------------

쉼표로 분리된 XYZ 값의 목록을 가진 (CSV 파일이라고 불리는) 텍스트 파일을 작업해야 하는 경우가 자주 있습니다. :ref:`gdal_grid` 에서 이런 유형의 데이터소스를 쉽게 이용할 수 있습니다. 사용자의 CSV 파일을 위한 가상 데이터셋 헤더(VRT)를 생성해서 :ref:`gdal_grid` 의 입력 데이터소스로 쓰면 됩니다. :ref:`vector.vrt` 설명 페이지에서 VRT 포맷에 대한 자세한 내용을 볼 수 있습니다.

간단한 예시를 들어봅시다. 다음과 같은 내용을 담고 있는 <dem.csv>라는 CSV 파일이 있다고 가정합니다:

::

    Easting,Northing,Elevation
    86943.4,891957,139.13
    87124.3,892075,135.01
    86962.4,892321,182.04
    87077.6,891995,135.01
    ...

이 데이터에 대해 다음 내용을 가진 <dem.vrt> 헤더를 생성할 것입니다:

.. code-block:: xml

    <OGRVRTDataSource>
        <OGRVRTLayer name="dem">
            <SrcDataSource>dem.csv</SrcDataSource>
            <GeometryType>wkbPoint</GeometryType>
            <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Elevation"/>
        </OGRVRTLayer>
    </OGRVRTDataSource>

이 서술된 내용은 X, Y 및 Z 3개 좌표를 가지고 있는 소위 2.5D 도형을 지정합니다. 보간 작업에는 Z값을 사용할 것입니다. 이제 모든 OGR 프로그램에서 <dem.vrt>를 사용할 수 있습니다. (모든 것이 잘 작동하는지 확인하려면 :ref:`ogrinfo` 로 시작해보십시오.) 데이터소스가 CSV 파일에 있는 값들로부터 구성된 포인트 객체로 채워진 <"dem">이라는 단일 레이어를 담게 될 것입니다. 이 방법을 사용하면 3개 이상의 열, 스위치 열 등등을 가진 CSV 파일을 처리할 수 있습니다.

사용자의 CSV 파일이 열 헤더를 담고 있지 않다면 다음과 같은 방식으로 처리할 수 있습니다:

.. code-block:: xml

    <GeometryField encoding="PointFromColumns" x="field_1" y="field_2" z="field_3"/>

:ref:`vector.csv` 설명 페이지에서 GDAL/OGR이 지원하는 CSV 포맷에 대한 자세한 내용을 볼 수 있습니다.

C API
-----

C에서 :cpp:func:`GDALGrid` 로도 이 유틸리티를 호출할 수 있습니다.

예시
--------

다음 명령어는 `쉼표로 분리된 값 읽기`_ 단락에서 설명하는 VRT 데이터소스로부터 역거리 거듭제곱 가중치 보간법을 사용해서 래스터 TIFF 파일을 생성할 것입니다. 보간할 값은 도형 레코드의 Z값에서 읽어올 것입니다.

::

    gdal_grid -a invdist:power=2.0:smoothing=1.0 -txe 85000 89000 -tye 894000 890000 -outsize 400 400 -of GTiff -ot Float64 -l dem dem.vrt dem.tiff

다음 명령어는 앞의 예시와 동일한 작업을 하지만, 도형 레코드 대신 **-zfield** 옵션으로 지정한 속성 필드에서 보간할 값을 읽어옵니다. 즉 이 경우 X와 Y 좌표는 도형에서 가져오고 Z 좌표는 <"Elevation"> 필드에서 가져옵니다. 계산 프로세스를 병렬화하기 위해 GDAL_NUM_THREADS도 설정합니다.

::

    gdal_grid -zfield "Elevation" -a invdist:power=2.0:smoothing=1.0 -txe 85000 89000 -tye 894000 890000 -outsize 400 400 -of GTiff -ot Float64 -l dem dem.vrt dem.tiff --config GDAL_NUM_THREADS ALL_CPUS

