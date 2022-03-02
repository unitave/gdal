.. _gdal_merge:

================================================================================
gdal_merge.py
================================================================================

.. only:: html

    이미지 집합으로 모자이크를 생성합니다.

.. Index:: gdal_merge

개요
--------

.. code-block::

    gdal_merge.py [-o out_filename] [-of out_format] [-co NAME=VALUE]*
                  [-ps pixelsize_x pixelsize_y] [-tap] [-separate] [-q] [-v] [-pct]
                  [-ul_lr ulx uly lrx lry] [-init "value [value...]"]
                  [-n nodata_value] [-a_nodata output_nodata_value]
                  [-ot datatype] [-createonly] input_files

설명
-----------

이 이미지는 이미지 집합으로 자동적으로 모자이크를 생성합니다. 모든 이미지는 동일한 좌표계를 사용해야만 하며 밴드의 개수도 일치해야만 하지만, 서로 중첩할 수도 있고 해상도가 달라도 됩니다. 중첩되는 영역에서는 마지막 이미지가 이전 이미지들 위로 복사될 것입니다. NODATA/투명도 값은 밴드 별 수준에서 고려됩니다. 예를 들어 하나의 소스 밴드 상에 있는 NODATA/투명도 값이 산출되는 래스터의 대상 픽셀의 모든 밴드 상에 있는 NODATA/투명도 값을 설정하지는 않을 것입니다. 또 하나의 소스 밴드 상에 있는 NODATA/투명도 값이 유효한 픽셀 값을 덮어쓰지도 않을 것입니다.

.. program:: gdal_merge

.. option:: -o <out_filename>

    산출물 파일의 이름입니다. 지정한 이름의 파일이 이미 존재하지 않는다면 지정한 이름으로 파일을 생성할 것입니다. (기본값은 "out.tif"입니다.)

.. include:: options/of.rst

.. include:: options/co.rst

.. include:: options/ot.rst

.. option:: -ps <pixelsize_x> <pixelsize_y>

    산출물 파일에 사용할 픽셀 크기입니다. 지정하지 않는 경우 첫 번째 입력 파일의 해상도를 이용할 것입니다.

.. option:: -tap

    (대상 정렬 픽셀(target aligned pixels)) 정렬된 범위가 최소 범위를 포함하도록, 산출물 파일의 범위 좌표를 :option:`-tr` 의 값들에 정렬시킵니다.

.. option:: -ul_lr <ulx> <uly> <lrx> <lry>

    산출물 파일의 범위입니다. 지정하지 않는 경우 모든 입력 파일의 범위를 합친 범위를 이용할 것입니다.

.. option:: -v

    모자이크 작업이 끝나면 작업에 대한 자세한 설명을 생성합니다.

.. option:: -separate

    각 입력 파일을 개별 밴드로 배치합니다.

.. option:: -pct

    첫 번째 입력 이미지로부터 의사색상표를 가져와서 산출물에 사용합니다. 의사색상 이미지들을 이런 방식으로 병합한다는 것은 모든 입력 파일이 동일한 색상표를 사용한다고 가정한다는 뜻입니다.

.. option:: -n <nodata_value>

    병합되는 파일들에서 이 픽셀 값을 가진 픽셀들을 무시합니다.

.. option:: -a_nodata <output_nodata_value>

    산출물 밴드에 지정한 NODATA 값을 할당합니다.

.. option:: -init <"value(s)">

    산출 이미지 밴드를 이 값으로 사전 초기화합니다. 하지만 산출물 파일에서 이 값을 NODATA 값으로 표시하지는 않습니다. 값을 하나만 지정하는 경우, 모든 밴드에 동일한 값을 사용합니다.

.. option:: -createonly

    산출물 파일을 생성하지만 (그리고 사전 초기화할 수도 있지만) 산출물 파일에 어떤 입력 이미지 데이터도 복사하지 않습니다.

.. note::

    gdal_merge.py는 파이썬 스크립트로, GDAL이 파이썬 지원과 함께 빌드된 경우에만 작동할 것입니다.

예시
-------

모든 밴드에 있는 픽셀을 255로 초기화한 이미지를 생성합니다.

::

    gdal_merge.py -init 255 -o out.tif in1.tif in2.tif


데이터가 없는 픽셀을 청색으로 표시한 RGB 이미지를 생성합니다. 처음 두 밴드는 0으로, 그리고 세 번째 밴드는 255로 초기화할 것입니다.

::

    gdal_merge.py -init "0 0 255" -o out.tif in1.tif in2.tif
