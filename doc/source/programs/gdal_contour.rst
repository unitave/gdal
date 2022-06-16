.. _gdal_contour:

================================================================================
gdal_contour
================================================================================

.. only:: html

    래스터 표고 모델로부터 벡터 등고선 라인을 작성합니다.

.. Index:: gdal_contour

개요
----

.. code-block::

    gdal_contour [-b <band>] [-a <attribute_name>] [-amin <attribute_name>] [-amax <attribute_name>]
                 [-3d] [-inodata]
                 [-snodata n] [-i <interval>]
                 [-f <formatname>] [[-dsco NAME=VALUE] ...] [[-lco NAME=VALUE] ...]
                 [-off <offset>] [-fl <level> <level>...] [-e <exp_base>]
                 [-nln <outlayername>] [-q] [-p]
                 <src_filename> <dst_filename>

설명
----

:program:`gdal_contour` 는 입력 래스터 DEM으로부터 벡터 등고선 파일을 생성합니다.

등고선 라인스트링의 방향은 일정하며 더 높은 쪽이 오른쪽일 것입니다. 예를 들면 라인스트링이 산봉우리 주변을 시계 방향으로 돕니다.

.. program:: gdal_contour

.. option:: -b <band>

    DEM을 가져올 특정 밴드를 선택합니다. 기본값은 1번 밴드입니다.

.. option:: -a <name>

    표고를 넣을 속성의 이름을 지정합니다. 지정하지 않는 경우 어떤 표고 속성도 추가하지 않습니다. 폴리곤 등고선 (:option:`-p`) 모드에서는 무시됩니다.

.. option:: -amin <name>

    등고선 폴리곤의 최저 표고를 넣을 속성의 이름을 지정합니다. 지정하지 않는 경우 어떤 최저 표고 속성도 추가하지 않습니다. 기본 라인 등고선 모드에서는 무시됩니다.

    .. versionadded:: 2.4.0

.. option:: -amax <name>

    등고선 폴리곤의 최고 표고를 넣을 속성의 이름을 지정합니다. 지정하지 않는 경우 어떤 최고 표고 속성도 추가하지 않습니다. 기본 라인 등고선 모드에서는 무시됩니다.

    .. versionadded:: 2.4.0

.. option:: -3d

    2차원 벡터 대신 3차원 벡터를 강제 생성합니다. 모든 꼭짓점에 표고가 포함됩니다.

.. option:: -inodata

    데이터셋에 나타나는 모든 NODATA 값을 무시합니다 -- 모든 값을 무결한 것으로 취급합니다.

.. option:: -snodata <value>

    "NODATA"로 취급할 입력 픽셀 값을 지정합니다.

.. option:: -f <format>

    산출물을 특정 포맷으로 생성합니다.

    .. versionadded:: 2.3.0

        지정하지 않는 경우, 확장자로부터 포맷을 추정합니다. (예전에는 기본값 ESRI Shapefile로 생성했습니다.)

.. option:: -dsco <NAME=VALUE>

    데이터셋 생성 옵션(DataSet Creation Option) (포맷 특화)

.. option:: -lco <NAME=VALUE>

    레이어 생성 옵션(Layer Creation Option) (포맷 특화)

.. option:: -i <interval>

    등고선 사이의 표고 간격을 지정합니다.

.. option:: -off <offset>

    간격을 해석할 기준에 비례하는 0으로부터의 오프셋입니다.

.. option:: -fl <level>

    하나 이상의 추출할 "고정 수준(Fixed Level)"의 이름을 지정합니다.

.. option:: -e <base>

    지수(exponential) 척도로 수준을 생성합니다. ``base ^ k`` 에서 ``k`` 는 정수입니다.

    .. versionadded:: 2.4.0

.. option:: -nln <name>

    산출 벡터 레이어의 이름을 지정합니다. 기본값은 "contour"입니다.

.. option:: -p

    등고선 라인 대신 등고선 폴리곤을 생성합니다.

    .. versionadded:: 2.4.0

.. option:: -q

    아무것도 출력하지 않습니다.

C API
-----

이 유틸리티의 기능은 :cpp:func:`GDALContourGenerate` C 함수로도 수행할 수 있습니다.

예시
----

다음 명령어는 :file:`dem.tif` 의 DEM 데이터로부터 10미터 간격 등고선을 생성해서, ``elev`` 속성에 등고선 표고를 가진 :file:`contour.shp|shx|dbf` shapefile을 생성할 것입니다:

.. code-block::

    gdal_contour -a elev dem.tif contour.shp -i 10.0

