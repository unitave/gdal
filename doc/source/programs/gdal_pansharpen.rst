.. _gdal_pansharpen:

================================================================================
gdal_pansharpen.py
================================================================================

.. only:: html

    영상융합(pan-sharpening) 작업을 수행합니다.

    (GDAL 2.1버전부터)

.. Index:: gdal_pansharpen

개요
--------

.. code-block::

    gdal_pansharpen [--help-general] pan_dataset {spectral_dataset[,band=num]}+ out_dataset
                    [-of format] [-b band]* [-w weight_val]*
                    [-r {nearest,bilinear,cubic,cubicspline,lanczos,average}]
                    [-threads {ALL_CPUS|number}] [-bitdepth val] [-nodata val]
                    [-spat_adjust {union,intersection,none,nonewithoutwarning}]
                    [-co NAME=VALUE]* [-q]

설명
-----------

:program:`gdal_pansharpen.py` 스크립트는 영상융합(pan-sharpening) 작업을 수행합니다. 이 스크립트는 (GeoTIFF 같은) "대표적인" 산출 데이터셋 또는 영상융합 작업을 설명하는 VRT 데이터셋을 생성할 수 있습니다.

:ref:`gdal_vrttut_pansharpen` 단락에서 더 자세한 내용을 찾아볼 수 있습니다.

.. option:: -of <format>:

    산출물 포맷을 선택합니다. GDAL 2.3버전부터, 이 옵션을 지정하지 않을 경우 확장자로부터 포맷을 추정합니다. (이전에는 GTiff가 기본값이었습니다.) 단축 포맷 이름을 사용하십시오. ``VRT`` 도 사용할 수 있습니다.

.. option:: -b <band>

    입력 스펙트럼 밴드로부터 산출물을 위한 *밴드* 를 선택합니다. 밴드 번호는 스펙트럼 밴드가 지정된 순서대로 1부터 시작합니다. **-b** 스위치를 여러 번 사용할 수도 있습니다. -b 스위치를 사용하지 않는 경우, 산출물에 모든 스펙트럼 밴드를 설정합니다.

.. option:: -w <weight_val>

    의사 전정색(panchromatic) 값을 계산하기 위한 가중치를 지정합니다. 입력 스펙트럼 밴드의 개수와 동일한 개수의 -w 스위치를 사용해야만 합니다.

.. option:: -r {nearest,bilinear,cubic (default),cubicspline,lanczos,average}

    리샘플링 알고리즘을 선택합니다.

.. option:: -threads {ALL_CPUS,number}

    리샘플링과 영상융합 자체를 수행하기 위해 사용할 스레드 개수를 지정합니다. 정수 또는 ALL_CPUS로 설정할 수 있습니다.

.. option:: -bitdepth <val>

    전정색 및 스펙트럼 밴드의 비트 깊이(bit depth)를 (예를 들면 12로) 지정합니다. 지정하지 않는 경우, 전정색 밴드로부터 나온 NBITS 메타데이터 항목이 존재한다면 이를 사용할 것입니다.

.. option:: -nodata <val>

    밴드에 NODATA 값을 지정합니다. 리샘플링과 영상융합 자체를 수행하기 위해 사용됩니다. 지정하지 않는 경우, 모든 입력 밴드의 설정이 일관된다는 가정 하에 입력 밴드로부터 추정합니다.

.. option:: -spat_adjust {union(default),intersection,none,nonewithoutwarning}

    밴드들이 동일한 범위가 아닌 경우의 습성을 선택합니다. :ref:`gdal_vrttut_pansharpen` 에 있는 *SpatialExtentAdjustment* 문서를 읽어보십시오.

.. include:: options/co.rst

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

.. option:: <pan_dataset>

    전정색 밴드를 가진 데이터셋입니다. (첫 번째 밴드를 사용할 것입니다.)

.. option:: <spectral_dataset>[,band=num]

    스펙트럼 밴드를 하나 또는 몇 개 가진 데이터셋입니다. -b 옵션을 설정하지 않은 경우, 연산에 데이터셋의 모든 밴드를 사용합니다. 밴드 옵션을 설정했다면 지정한 <band>번째 밴드만 사용합니다. 동일한 데이터셋을 몇 번 반복해서 지정할 수 있습니다.

.. option:: <out_dataset>

    산출 데이터셋입니다.

밴드들이 동일한 투영법을 사용해야 합니다.

예시
-------

단일 데이터셋에 있는 스펙트럼 밴드들을 작업합니다:

.. code-block::

    gdal_pansharpen.py panchro.tif multispectral.tif pansharpened_out.tif

단일 데이터셋에서 나온 스펙트럼 밴드 몇 개의 순서를 재정렬해서 작업합니다:

.. code-block::

    gdal_pansharpen.py panchro.tif multispectral.tif,band=3 multispectral.tif,band=2 multispectral.tif,band=1 pansharpened_out.tif

데이터셋 몇 개에 있는 스펙트럼 밴드들을 작업합니다:

.. code-block::

    gdal_pansharpen.py panchro.tif band1.tif band2.tif band3.tif pansharpened_out.tif

가중치를 지원합니다:

.. code-block::

    gdal_pansharpen.py -w 0.7 -w 0.2 -w 0.1 panchro.tif multispectral.tif pansharpened_out.tif

RGBNir 밴드 4개에서 의사 전정색 강도를 계산하는 동안 RGBNir 다중 스펙트럼 데이터셋으로부터 나온 RGB 밴드를 지정합니다:

.. code-block::

    gdal_pansharpen.py -b 1 -b 2 -b 3 panchro.tif rgbnir.tif pansharpened_out.tif
