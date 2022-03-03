.. _gdal2xyz:

================================================================================
gdal2xyz.py
================================================================================

.. only:: html

    래스터 파일을 `xyz` 포맷으로 변환합니다.

.. Index:: gdal2xyz

개요
--------

.. code-block::

    gdal2xyz [-help]
        [-skip factor]
        [-srcwin xoff yoff xsize ysize]
        [-b band]* [-allbands]
        [-skipnodata]
        [-csv]
        [-srcnodata value] [-dstnodata value]
        src_dataset [dst_dataset]

설명
-----------

:program:`gdal2xyz` 유틸리티를 사용하면 래스터 파일을 xyz 포맷으로 변환할 수 있습니다. `gdal2xyz` 는 `gdal_translate of=xyz` 를 대신할 수 있지만, 다음과 같은 다른 옵션도 지원합니다:

    * 하나 이상의 밴드를 선택할 수 있습니다.
    * NODATA 값을 건너뛰거나 대체할 수 있습니다.
    * 산출물을 넘파이(NumPy) 배열로 반환할 수 있습니다.

.. program:: gdal2xyz

.. option:: -skip

    각 반복 작업마다 얼마나 많은 행/열을 건너뛸지 설정합니다.

.. option:: -srcwin <xoff> <yoff> <xsize> <ysize>

    소스 이미지로부터 픽셀/라인 위치를 기반으로 복사하기 위한 하위 창을 선택합니다.

.. option:: -b, -band <band>

    입력 스펙트럼 밴드로부터 산출물을 위한 *밴드* 를 선택합니다. 밴드 번호는 스펙트럼 밴드가 지정된 순서대로 1부터 시작합니다. **-b** 스위치를 여러 번 사용할 수도 있습니다. -b 스위치를 사용하지 않는 경우, 첫 번째 밴드를 사용할 것입니다. 모든 입력 밴드를 사용하려면 `-allbands` 또는 `-b 0` 으로 설정하십시오.

.. option:: -allbands

    모든 입력 밴드를 선택합니다.

.. option:: -csv

    구분자(delimiter)로 공백 대신 쉼표를 사용합니다.

.. option:: -skipnodata

    (srcnodata로 결정된) NODATA 값을 가진 산출물 라인을 제외합니다.

.. option:: -srcnodata

    (건너뛰거나 대체하기 위한) 데이터셋의 NODATA 값을 지정합니다. 기본값 `None` 은 데이터셋의 NODATA 값을 사용하며, `Sequence`/`Number` 로 설정하면 (밴드 별 또는 데이터셋 별로) 지정한 NODATA 값을 사용합니다.

.. option:: -dstnodata

    소스의 NODATA 값을 지정한 NODATA 값으로 대체합니다. `-skipnodata` 를 설정하지 않은 경우에만 효과가 있습니다. 기본값 `None` 은 값을 대체하지 않고 `srcnodata` 를 그대로 사용하며, `Sequence`/`Number` 로 설정하면 `srcnodata` 를 (밴드 별 또는 데이터셋 별로) 지정한 NODATA 값으로 대체합니다.

.. option:: -h, --help

    도움말 메시지를 표시하고 엑시트합니다.

.. option:: <src_dataset>

    소스 데이터셋의 이름입니다. 파일명, 데이터소스의 URL, 또는 다중 데이터셋 파일의 하위 데이터셋 이름 가운데 하나를 지정할 수 있습니다.

.. option:: <dst_dataset>

    대상 파일의 이름입니다.


예시
--------

::

    gdal2xyz -b 1 -b 2 -dstnodata 0 input.tif output.txt


입력 파일 `input.tif` 로부터 데이터셋의 NODATA 값을 0으로 대체한 첫 번째와 두 번째 밴드를 포함하는 `xyz` 포맷의 텍스트 파일을 생성하기 위한 명령어입니다.
