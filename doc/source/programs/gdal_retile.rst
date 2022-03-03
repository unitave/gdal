.. _gdal_retile:

================================================================================
gdal_retile.py
================================================================================

.. only:: html

    타일 집합을 다시 타일화하고, 그리고/또는 타일화된 피라미드 수준을 작성합니다.

.. Index:: gdal_retile

개요
--------

.. code-block::

    gdal_retile.py [-v] [-co NAME=VALUE]* [-of out_format] [-ps pixelWidth pixelHeight]
                   [-overlap val_in_pixel]
                   [-ot  {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
                           CInt16/CInt32/CFloat32/CFloat64}]'
                   [ -tileIndex tileIndexName [-tileIndexField tileIndexFieldName]]
                   [ -csv fileName [-csvDelim delimiter]]
                   [-s_srs srs_def]  [-pyramidOnly]
                   [-r {near/bilinear/cubic/cubicspline/lanczos}]
                   -levels numberoflevels
                   [-useDirForEachRow] [-resume]
                   -targetDir TileDirectory input_files

설명
-----------

이 유틸리티는 입력 타일(들)의 집합을 다시 타일화합니다. 모든 입력 타일(들)은 동일한 좌표계에서 지리참조되어야만 하며 밴드 개수가 일치해야만 합니다. 피라미드 수준을 생성하는 옵션이 있습니다. 타일화된 산출물에 대한 shapefile(들)을 생성할 수 있습니다.

입력 타일 개수가 명령줄 버퍼를 넘어서는 경우, 일반적인 :ref:`--optfile <raster_common_options_optfile>` 옵션을 사용하십시오.

.. program:: gdal_retile

.. option:: -targetDir <directory>

    타일화 결과물을 생성하는 디렉터리입니다. 1부터 시작하는 하위 디렉터리에 피라미드를 저장합니다. 생성된 타일 이름은 번호 부여 스키마를 가지고 있으며, 소스 타일(들)의 이름을 담고 있습니다.

.. include:: options/of.rst

.. include:: options/co.rst

.. include:: options/ot.rst

.. option:: -ps <pixelsize_x> <pixelsize_y>

    산출 파일에 사용할 픽셀 크기입니다. 지정하지 않는 경우 기본값은 256x256입니다.

.. option:: -overlap< <val_in_pixel>

    연속되는 타일들을 지정한 픽셀 개수만큼 중첩합니다. 지정하지 않는 경우 기본값은 0입니다.

    .. versionadded:: 2.2

.. option:: -levels <numberOfLevels>

    작성할 피라미드 수준의 개수입니다.

.. option:: -v

    타일화 작업이 끝나면 작업에 대한 자세한 설명을 생성합니다.

.. option:: -pyramidOnly

    다시 타일화하지 않고, 피라미드만 작성합니다.

.. option:: -r <algorithm>

    리샘플링 알고리즘입니다. 기본값은 ``near`` 입니다.

.. option:: -s_srs <srs_def>

    소스 공간 좌표계를 설정합니다. OGRSpatialReference.SetFromUserInput() 호출이 지원하는 모든 좌표계를 전송(pass)할 수 있습니다. 이 모든 좌표계는 EPSG PCS와 GCS들(예: EPSG:4296), (앞에서 보인대로의) PROJ.4 선언문, 또는 WKT를 담고 있는 .prj 파일의 이름을 포함합니다. srs_def를 지정하지 않는 경우, (소스 타일의 srs_def가 있다면) 소스 srs_def를 사용합니다. srs_def는 (가능하다면) 생성된 타일에 그리고 선택적인 shapefile(들)에 들어갈 것입니다.

.. option:: -tileIndex <tileIndexName>

    산출되는 타일(들) 색인을 담고 있는 shapefile의 이름입니다.

.. option:: -tileIndexField <tileIndexFieldName>

    타일 이름을 담고 있는 속성의 이름입니다.

.. option:: -csv <csvFileName>

    타일(들)의 지리참조 정보를 담고 있는 CSV 파일의 이름입니다. 이 파일은 tilename, minx, maxx, miny, maxy 열 5개를 담고 있습니다.

.. option:: -csvDelim <column delimiter>

    CSV 파일에서 쓰이는 열 구분자입니다. 기본값은 쌍반점 ";"입니다.

.. option:: -useDirForEachRow

    일반적으로 기반 이미지의 타일은 :option:`-targetDir` 에 설정한대로 저장됩니다. 대용량 이미지의 경우, 디렉터리 하나 안에 있는 파일 개수가 너무 큰 경우 일부 파일 시스템의 성능이 저하되어 gdal_retile이 적정한 시간 안에 종료되지 않을 수도 있습니다. 이 파라미터를 사용하면 다른 산출물 구조를 생성합니다. 0이라는 하위 디렉터리에 기반 이미지의 타일을 저장하고, 1, 2, ... 번호를 붙인 하위 디렉터리에 피라미드를 저장합니다. 이 디렉터리 각각에 0에서 n까지 번호를 붙인 또다른 수준의 하위 디렉터리를 생성합니다. 이때 n은 각 수준에서 타일 행들이 얼마나 많이 필요하냐에 따라 달라집니다. 결국, 디렉터리 하나가 특정 수준 하나의 행 하나에 해당하는 타일들만 담게 됩니다. 대용량 이미지의 경우 N배의 성능 향상을 이룰 수 있습니다.

.. option:: -resume

    다시 시작(resume) 모드입니다. 누락된 파일만 생성합니다.

.. note::

    gdal_retile.py는 파이썬 스크립트로, GDAL이 파이썬 지원과 함께 빌드된 경우에만 작동할 것입니다.
