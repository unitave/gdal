.. _rgb2pct:

================================================================================
rgb2pct.py
================================================================================

.. only:: html

    24비트 RGB 이미지를 8비트 색상표 이미지로 변환합니다.

.. Index:: rgb2pct

개요
--------

.. code-block::

    rgb2pct.py [-n colors | -pct palette_file] [-of format] <source_file> <dest_file>

설명
-----------

이 유틸리티는 입력된 RGB 이미지의 다운샘플링된 RGB 히스토그램 상에 중간값 잘라내기(median cut) 알고리즘을 사용해서 입력된 RGB 이미지에 대한 최적 의사색상표(pseudo-color table)를 계산할 것입니다. 그 다음 색상표를 이용해서 입력 이미지를 의사색상 이미지로 변환합니다. 이 변환 과정에서 산출 이미지의 시각 품질을 극대화하기 위해 플로이드-스타인버그 디더링(Floyd-Steinberg dithering; 오차확산법(error diffusion))을 활용합니다.

.. program:: rgb2pct

.. option:: -n <color>

    생성된 색상표에 들어갈 색상 개수를 선택합니다. 기본값은 256개입니다. 이 값은 2에서 256사이의 정수여야만 합니다.

.. option:: -pct <palette_file>

    색상표를 계산하는 대신 <palette_file>로부터 색상표를 추출합니다. 여러 파일에 일관된 색상표를 적용하려는 경우 사용할 수 있습니다. <palette_file>은 GDAL이 지원하는 포맷의 색상표를 가진 래스터 파일 또는 이 프로그램이 지원하는 포맷(txt, qml, qlr)으로 된 색상 파일 가운데 하나여야만 합니다.

.. option:: -of <format>

    산출물 포맷을 선택합니다. GDAL 2.3버전부터 이 옵션을 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지는 GTiff를 사용했습니다.) 단축 포맷명을 사용하십시오. 의사색상표를 지원하는 산출물 포맷만 사용해야 합니다.

.. option:: <source_file>

    입력 RGB 파일입니다.

.. option:: <dest_file>

    생성할 산출 의사색상 파일입니다.

주의: rgb2pct.py는 파이썬 스크립트로, GDAL이 파이썬 지원과 함께 빌드된 경우에만 작동할 것입니다.

예시
-------

직접 색상표를 생성하기 원한다면, 가장 단순한 텍스트 포맷은 GDAL VRT 포맷일 것입니다. 다음 예시에서는 텍스트 편집기에서 238/238/238/255, 237/237/237/255, 236/236/236/255 그리고 229/229/229/255라는 RGBA 색상 4개를 가진 작은 색상표를 담은 VRT를 생성합니다.

::

    rgb2pct.py -pct palette.vrt rgb.tif pseudo-colored.tif
    more < palette.vrt
    <VRTDataset rasterXSize="226" rasterYSize="271">
        <VRTRasterBand dataType="Byte" band="1">
            <ColorInterp>Palette</ColorInterp>
            <ColorTable>
            <Entry c1="238" c2="238" c3="238" c4="255"/>
            <Entry c1="237" c2="237" c3="237" c4="255"/>
            <Entry c1="236" c2="236" c3="236" c4="255"/>
            <Entry c1="229" c2="229" c3="229" c4="255"/>
            </ColorTable>
        </VRTRasterBand>
    </VRTDataset>
