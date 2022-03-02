.. _gdal_translate:

================================================================================
gdal_translate
================================================================================

.. only:: html

    래스터 데이터를 서로 다른 포맷으로 변환합니다.

.. Index:: gdal_translate

개요
--------

.. code-block::


    gdal_translate [--help-general]
        [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
                CInt16/CInt32/CFloat32/CFloat64}] [-strict]
        [-if format]* [-of format]
        [-b band]* [-mask band] [-expand {gray|rgb|rgba}]
        [-outsize xsize[%]|0 ysize[%]|0] [-tr xres yres]
        [-r {nearest,bilinear,cubic,cubicspline,lanczos,average,rms,mode}]
        [-unscale] [-scale[_bn] [src_min src_max [dst_min dst_max]]]* [-exponent[_bn] exp_val]*
        [-srcwin xoff yoff xsize ysize] [-epo] [-eco]
        [-projwin ulx uly lrx lry] [-projwin_srs srs_def]
        [-a_srs srs_def] [-a_coord_epoch <epoch>]
        [-a_ullr ulx uly lrx lry] [-a_nodata value]
        [-a_scale value] [-a_offset value]
        [-nogcp] [-gcp pixel line easting northing [elevation]]*
        |-colorinterp{_bn} {red|green|blue|alpha|gray|undefined}]
        |-colorinterp {red|green|blue|alpha|gray|undefined},...]
        [-mo "META-TAG=VALUE"]* [-q] [-sds]
        [-co "NAME=VALUE"]* [-stats] [-norat] [-noxmp]
        [-oo NAME=VALUE]*
        src_dataset dst_dataset

설명
-----------

:program:`gdal_translate` 유틸리티는 래스터 데이터를 서로 다른 포맷으로 변환하기 위해 쓰일 수 있습니다. 이 과정에서 하위 집합 생성, 리샘플링, 그리고 픽셀 크기 조정 같은 몇몇 작업을 수행할 수도 있습니다.

.. program:: gdal_translate

.. include:: options/ot.rst

.. option:: -strict

    산출물 포맷으로 변환하는 과정에서 부정합(mismatch) 및 손상 데이터를 용납하지 않습니다.

.. include:: options/if.rst

.. include:: options/of.rst

.. option:: -b <band>

    입력 밴드에서 산출물 용 **밴드** 를 선택합니다. 밴드 번호는 1부터 시작합니다. 산출 파일에 작성할 입력 밴드를 여러 개 선택하기 위해, 또는 밴드 순서를 재정렬하기 위해 :option:`-b` 스위치를 여러 개 사용할 수도 있습니다. 입력 데이터셋의 첫 번째 밴드의 마스크 밴드를 의도하려면 **밴드** 를 "mask,1"(또는 그냥 "mask")로 설정할 수도 있습니다.

.. option:: -mask <band>

    입력 밴드에서 산출 데이터셋 마스크 밴드를 생성하기 위한 **밴드** 를 선택합니다. 밴드 번호는 1부터 시작합니다. 입력 데이터셋에 전체 수준(global) 마스크가 존재하는 경우 이를 복사하는 일을 피하려면 **밴드** 를 "none"으로 설정하면 됩니다. 이렇게 하지 않으면, 마스크가 알파 채널이 아니거나 명백히 산출 데이터셋의 정규 밴드로 쓰이는 경우("-b mask")를 제외하고, 기본적으로 ("auto") 복사될 것입니다. 입력 데이터셋의 첫 번째 밴드의 마스크 밴드를 의도하려면 **밴드** 를 "mask,1"(또는 그냥 "mask")로 설정할 수도 있습니다.

.. option:: -expand gray|rgb|rgba

    색상표를 가지고 있는 밴드 1개의 데이터셋을 밴드 3개(RGB) 또는 4개(RGBA)의 데이터셋으로 노출시킵니다. 색상 색인(color indexed) 데이터셋을 지원하지 않는 JPEG, JPEG2000, MrSID, ECW 같은 산출물 드라이버에 유용합니다. 'gray' 값은 회색도(gray level)만 담고 있는 색상표를 가진 데이터셋을 회색 색인 데이터셋으로 확장시켜 줍니다.

.. option:: -outsize <xsize>[%]|0 <ysize>[%]|0

    산출 파일의 크기를 설정합니다. outsize는 '%'가 붙지 않는 이상 픽셀과 행 단위입니다. '%'가 붙는 경우 입력 이미지 크기 대비 비율을 의미합니다. 2개의 값 가운데 하나를 0으로 설정하면, 소스 데이터셋의 가로세로비(aspect ratio)를 유지한다는 기준으로 다른 값으로부터 해당 값을 결정할 것입니다.

.. option:: -tr <xres> <yres>

    대상(target) 해상도를 설정합니다. 값은 지리참조된 단위로 표현되어야만 합니다. 두 값 모두 양의 값이어야만 합니다. 이 옵션을 :option:`-outsize` 및 :option:`-a_ullr` 옵션과 함께 사용해서는 안 됩니다.

.. option:: -r {nearest (default),bilinear,cubic,cubicspline,lanczos,average,rms,mode}

    리샘플링 알고리즘을 선택합니다.

    ``nearest`` 최근접 이웃 (단순 샘플링) 리샘플링 도구(resampler)를 적용합니다.

    ``average`` NODATA가 아닌 모든 기여 픽셀(contributing pixel)의 평균을 계산합니다. GDAL 3.1버전부터, 이 평균은 대상 픽셀에 완전히 기여하지 않는 소스 픽셀의 가중치를 제대로 고려하는 가중 평균이 되었습니다.

    ``rms`` NODATA가 아닌 모든 기여 픽셀의 제곱평균제곱근(root mean squared)/이차평균(quadratic mean)을 계산합니다. (GDAL 3.3버전 이상)

    ``bilinear`` 이중선형 회선 커널(bilinear convolution kernel)을 적용합니다.

    ``cubic`` 3차 회선 커널(cubic convolution kernel)을 적용합니.

    ``cubicspline`` B 스플라인 회선 커널(B-Spline convolution kernel)을 적용합니다.

    ``lanczos`` 란초시 창함수 싱크 회선 커널(Lánczos windowed sinc convolution kernel)을 적용합니다.

    ``mode`` 샘플링된 모든 포인트들에서 가장 출현 빈도가 높은 값을 선택합니다.

.. option:: -scale [src_min src_max [dst_min dst_max]]

    입력 픽셀 값을 **src_min** 에서 **src_max** 까지의 범위로부터 **dst_min** 에서 **dst_max** 까지의 범위로 값의 크기를 재조정(rescale)합니다. 이 옵션을 지정하지 않는 경우 산출 범위는 0에서 255까지이며, 입력 범위는 소스 데이터로부터 자동적으로 계산됩니다. 이 값들은 크기 조정 계산 및 입력 래스터 값에 적용하기 위한 상쇄(offset)에만 사용된다는 사실을 기억하십시오. 특히, src_min과 src_max는 입력값을 자르기(clip) 위해 사용되지 않습니다. 밴드 파라미터마다 지정하려면 -scale을 여러 번 반복하면 됩니다. (한번만 지정해도 산출 데이터의 모든 밴드에 적용됩니다.) 한 개 또는 여러 개의 특정 밴드의 파라미터를 지정하기 위해 "-scale_bn"이라는 문법도 사용할 수 있습니다. 이때 bn은 밴드 번호입니다. (예: "-scale_2"는 산출 데이터셋의 두 번째 밴드를 뜻합니다.)

.. option:: -exponent <exp_val>

    거듭제곱 함수로 비선형적으로 값의 크기를 조정합니다. exp_val은 거듭제곱 함수의 지수(exponent)입니다(양의 값이어야만 합니다). 이 옵션은 -scale 옵션과 함께 사용해야만 합니다. 한번만 지정하는 경우, 산출 이미지의 모든 밴드에 -exponent를 적용합니다. 밴드 파라미터마다 지정하려면 -exponent를 여러 번 반복하면 됩니다. 한 개 또는 여러 개의 특정 밴드의 파라미터를 지정하기 위해 "-exponent_bn"이라는 문법도 사용할 수 있습니다. 이때 bn은 밴드 번호입니다. (예: "-exponent_2"는 산출 데이터셋의 두 번째 밴드를 뜻합니다.)

.. option:: -unscale

    밴드에 scale/offset 메타데이터를 적용해서 크기 조정된 값을 조정되지 않은 값으로 변환합니다. 또 :option:`-ot` 스위치로 산출물 데이터 유형을 리셋시켜햐 하는 경우도 많습니다.

.. option:: -srcwin <xoff> <yoff> <xsize> <ysize>

   픽셀/행 위치를 기반으로 복사하기 위해 소스 이미지에서 하위 창(subwindow)을 선택합니다.

.. option:: -projwin <ulx> <uly> <lrx> <lry>

    복사하기 위해 (:option:`-srcwin` 처럼) 소스 이미지에서 하위 창을 선택하지만 모서리를 지리참조된 좌표로 입력합니다. (기본적으로 데이터셋의 공간 좌표계로 표현합니다. :option:`-projwin_srs` 옵션으로 좌표계를 변경할 수 있습니다.)

    .. note::

        GDAL 2.1.0 및 2.1.1에서, 픽셀과 정렬되지 않는 좌표계로 -projwin을 사용하면 하위 픽셀(sub-pixel)이 이동할 것입니다. 이후 버전에서는 수정되었습니다. GDAL 2.1.0버전부터, 최근접 이웃 리샘플링 이외의 메소드를 선택하는 경우, 보다 나은 결과물을 얻기 위해 하위 픽셀 정확도를 어찌됐든 이용합니다.

.. option:: -projwin_srs <srs_def>

    :option:`-projwin` 으로 입력된 좌표를 해석하기 위한 공간 좌표계를 지정합니다. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다.

    .. warning::
        이 옵션은 데이터셋을 지정한 공간 좌표계로 재투영하지 않습니다.

.. option:: -epo

    (부분적으로 외부에 있을 경우 오류(Error when Partially Outside)) 이 옵션을 설정한 경우, 소스 래스터 범위를 부분적으로 벗어나는 :option:`-srcwin` 또는 :option:`-projwin` 값을 오류로 간주할 것입니다. 이런 요청이 이전에 오류로 간주되었더라도, 기본적으로 이런 요청을 받아들입니다.

.. option:: -eco

    (완전히 외부에 있을 경우 오류(Error when Completely Outside)) 오류로 판단하는 기준이 요청이 소스 래스터 범위를 완전히 벗어나는 경우인 점을 제외하면, :option:`-epo` 와 동일합니다.

.. option:: -a_srs <srs_def>

    산출 파일의 투영법을 무시합니다.

    .. include:: options/srs_def.rst

    .. note:: 어떤 재투영도 하지 않습니다.

.. option:: -a_coord_epoch <epoch>

    .. versionadded:: 3.4

    산출물의 공간 좌표계와 링크된 시대 좌표(coordinate epoch)를 할당합니다. 산출물의 공간 좌표계가 동적 좌표계(dynamic CRS)인 경우 유용합니다.

.. option:: -a_scale <value>

    밴드 크기 조정 값을 설정합니다. (어떤 픽셀 값도 수정하지 않습니다.)

    .. versionadded:: 2.3

.. option:: -a_offset<value>

    밴드 오프셋 값을 설정합니다. (어떤 픽셀 값도 수정하지 않습니다.)

    .. versionadded:: 2.3

.. option:: -a_ullr <ulx> <uly> <lrx> <lry>

    산출 파일의 지리참조된 경계를 할당/무시합니다. 이 옵션은 소스 파일로부터 파생되었을 경계를 무시하고, 산출 파일에 지리참조된 경계를 할당합니다. 즉 이 옵션은 지정한 공간 좌표계로 재투영하지 않습니다.

.. option:: -a_nodata <value>

    산출 밴드에 지정한 NODATA 값을 할당합니다. 산출 파일에 소스 파일에 있을 수도 있는 값을 설정하는 경우를 피하려면 ``none`` 으로 설정하면 됩니다. 입력 데이터셋에 NODATA 값이 존재하는 경우, 이 옵션이 해당 NODATA 값과 동일한 픽셀 값을 지정한 값으로 변경하지 않는다는 사실을 기억하십시오.

.. option:: -colorinterp_X <red|green|blue|alpha|gray|undefined>

    밴드 X의 색상 해석을 무시합니다. (이때 X는 1부터 시작하는 유효한 밴드 번호입니다.)

    .. versionadded:: 2.3

.. option:: -colorinterp <red|green|blue|alpha|gray|undefined[,red|green|blue|alpha|gray|undefined]*>

    지정한 모든 밴드의 색상 해석을 무시합니다. 예를 들면 밴드 4개를 가진 산출 데이터셋의 경우 -colorinterp red,green,blue,alpha 처럼 사용할 수 있습니다.

    .. versionadded:: 2.3

.. option:: -mo META-TAG=VALUE

    가능하다면 산출 데이터셋에 설정할 메타데이터 키와 값을 전송(pass)합니다.

.. include:: options/co.rst

.. option:: -nogcp

    산출 데이터셋에 소스 데이터셋에 있는 GCP들을 복사하지 않습니다.

.. option:: -gcp <pixel> <line> <easting> <northing> <elevation>

    산출 데이터셋에 지정한 GCP를 추가합니다. GCP 집합을 추가하려면 이 옵션을 여러 번 사용할 수도 있습니다.

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

.. option:: -sds

    개별 산출 파일에 이 파일의 모든 하위 데이터셋을 복사합니다. 하위 데이터셋을 지원하는 HDF 같은 포맷과 함께 사용하십시오.

.. option:: -stats

    통계를 강제로 (다시) 계산합니다.

.. option:: -norat

    대상(destination) 데이터셋에 소스의 RAT을 복사하지 않습니다.

.. option:: -noxmp

    드라이버가 복사할 수 있더라도, 산출 데이터셋에 소스 데이터셋에 있는 XMP 메타데이터를 복사하지 않습니다.

    .. versionadded:: 3.2

.. option:: -oo NAME=VALUE

    데이터셋 열기 옵션 (특정 포맷 지원)

.. option:: <src_dataset>

    소스 데이터셋의 이름입니다. 파일명일 수도, 데이터소스의 URL 일 수도 있고 다중 데이터셋 파일들의 하위 데이터셋 이름일 수도 있습니다.

.. option:: <dst_dataset>

    대상(destination) 파일의 이름입니다.

C API
-----

이 유틸리티는 C에서 :cpp:func:`GDALTranslate` 로 호출할 수도 있습니다.

.. versionadded:: 2.1

예시
--------

::

    gdal_translate -of GTiff -co "TILED=YES" utm.tif utm_tiled.tif


RGBA 데이터셋으로부터 나온 내부 마스크를 가진 JPEG 압축 TIFF를 생성하려면

::

    gdal_translate rgba.tif withmask.tif -b 1 -b 2 -b 3 -mask 4 -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR --config GDAL_TIFF_INTERNAL_MASK YES


마스크를 가진 RGB 데이터셋으로부터 RGBA 데이터셋을 생성하려면

::

    gdal_translate withmask.tif rgba.tif -b 1 -b 2 -b 3 -b mask

