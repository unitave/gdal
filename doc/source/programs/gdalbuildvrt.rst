.. _gdalbuildvrt:

================================================================================
gdalbuildvrt
================================================================================

.. only:: html

    데이터셋 목록으로부터 VRT를 작성합니다.

.. Index:: gdalbuildvrt

개요
--------

.. code-block::

    gdalbuildvrt [-tileindex field_name]
                [-resolution {highest|lowest|average|user}]
                [-te xmin ymin xmax ymax] [-tr xres yres] [-tap]
                [-separate] [-b band]* [-sd subdataset]
                [-allow_projection_difference] [-q]
                [-addalpha] [-hidenodata]
                [-srcnodata "value [value...]"] [-vrtnodata "value [value...]"]
                [-ignore_srcmaskband]
                [-a_srs srs_def]
                [-r {nearest,bilinear,cubic,cubicspline,lanczos,average,mode}]
                [-oo NAME=VALUE]*
                [-input_file_list my_list.txt] [-overwrite]
                [-strict | -non_strict]
                output.vrt [gdalfile]*

설명
-----------

이 프로그램은 입력 GDAL 데이터셋들의 목록의 모자이크인 VRT(Virtual Dataset)를 작성합니다. 명령줄 마지막 부분에 입력 GDAL 데이터셋들을 지정하거나, 매우 긴 목록의 경우 (1행마다 파일명 하나인) 텍스트 파일 또는 MapServer 타일 색인을 삽입할 수 있습니다. (:ref:`gdaltindex` 유틸리티 참조) 후자의 경우, 타일 색인에 있는 모든 항목이 VRT에 추가될 것입니다.

-separate 옵션을 사용하면, VRT 데이터셋의 개별 밴드에 각 파일을 넣습니다. 그렇지 않다면 파일들을 더 큰 모자이크의 타일들로 간주해서 VRT 파일이 입력 파일들 가운데 가장 많은 밴드를 가지고 있는 파일의 밴드 개수만큼의 밴드를 가집니다.

GDAL 데이터셋 하나가 하위 데이터셋 몇 개로 이루어져 있고 래스터 밴드 0개를 가지고 있는 경우, VRT에 데이터셋 자체가 아니라 모든 하위 데이터셋을 추가할 것입니다.

gdalbuildvrt는 산출되는 VRT에 들어갈 모든 파일들이 비슷한 특성을 가지고 있는지 검증합니다: 밴드 개수, 투영법, 색상 해석... 비슷하지 않다면, 공통 특성과 일치하지 않는 파일을 건너뛸 것입니다. (기본 모드에서만 이렇고, -separate 옵션을 사용하는 경우엔 아닙니다.)

파일들 사이에 어느 정도의 공간 중첩이 있는 경우, 소스 목록에 나타나는 파일들의 순서가 중요해집니다: 목록 마지막 부분에 있는 파일들로부터 내용을 불러올 것입니다. 우선 순위가 낮은 데이터셋으로부터 데이터를 불러올 가능성이 있도록 NODATA를 고려할 것이지만, 현재로서는 알파 채널 합성 작업을 위해 알파 채널을 고려하지 않습니다. (따라서 또다른 소스 위에 나타나는 알파 채널이 0인 소스가 또다른 소스의 내용을 무시할 것입니다.) 이 습성은 다음 버전에서 달라질 수도 있습니다.

.. program:: gdalbuildvrt

.. option:: -tileindex

    기본값인 'location' 대신 지정한 값을 타일 색인 필드로 사용합니다.

.. option:: -resolution {highest|lowest|average|user}

    모든 입력 파일의 해상도가 동일하지 않은 경우, -resolution 플래그를 사용하면 사용자가 산출물 해상도가 계산되는 방식을 제어할 수 있습니다.

    `highest`는 소스 래스터 집합 내에서 픽셀 차원의 가장 작은 값을 고를 것입니다.

    `lowest`는 소스 래스터 집합 내에서 픽셀 차원의 가장 큰 값을 고를 것입니다.

    `average`는 기본값으로 소스 래스터 집합 내에서 픽셀 차원의 평균을 계산할 것입니다.

    `user`는 대상 해상도를 지정하기 위해 :option:`-tr` 옵션과 함께 쓰여야만 합니다.

.. option:: -tr <xres> <yres>

    대상 해상도를 설정합니다. 이 값은 지리참조 단위로 표현되어야만 합니다. 두 값 모두 양의 값이어야만 합니다. 이 값들을 지정하면 당연히 :option:`-resolution` 옵션의 highest|lowest|average 값을 사용할 수 없게 됩니다.

.. option:: -tap

    (대상에 정렬된 픽셀(target aligned pixels)) 산출물 파일의 범위의 좌표를 :option:`-tr` 옵션의 값에 정렬시켜 정렬된 범위가 최소 범위를 포함하도록 합니다.

.. option:: -te xmin ymin xmax ymax

    VRT 파일의 지리참조 범위를 설정합니다. 이 값은 지리참조 단위로 표현되어야만 합니다. 이 옵션을 지정하지 않는 경우, VRT의 범위는 소스 래스터 집합의 최소 경계 상자가 됩니다.

.. option:: -addalpha

    소스 래스터에 알파 밴드가 없는 경우 VRT에 알파 마스크 밴드를 추가합니다. 주로 RGB (또는 회색조) 소스에 유용합니다. 이 알파 밴드는 어떤 소스 래스터도 없는 영역을 실시간으로(on-the-fly) 0값으로 채우고, 소스 래스터가 있는 영역을 255값으로 채웁니다. 이렇게 하면 RGBA 뷰어가 소스 래스터가 없는 영역을 투명하게 렌더링하고 소스 래스터가 있는 영역을 불투명하게 렌더링하게 됩니다. 이 옵션을 :option:`-separate` 옵션과 함께 사용할 수 없습니다.

.. option:: -hidenodata

    NODATA 값을 담고 있는 밴드가 있더라도, 이 옵션을 사용하면 VRT 밴드가 NODATA를 리포트하지 않습니다. 데이터셋의 배경색을 제어하려 할 때 유용합니다. -addalpha 옵션과 함께 사용하면, NODATA를 리포트하지 않지만 데이터가 없는 영역이 투명한 데이터셋을 준비할 수 있습니다.

.. option:: -srcnodata <value> [<value>...]

    입력 밴드에 대한 NODATA 값을 설정합니다. (각 밴드 별로 서로 다른 값을 지정할 수 있습니다.) 값을 하나 이상 지정하는 경우 모든 값들을 단일 운영체제 인수로써 따옴표로 묶어주어야 합니다. 이 옵션을 지정하지 않으면 소스 데이터셋 상의 고유한 NODATA 설정을 (존재하는 경우) 사용할 것입니다. 이 옵션으로 설정한 값은 각 ComplexSource 요소의 NODATA 요소에 작성됩니다. 소스 데이터셋 상의 고유한 NODATA 설정을 무시하려면 ``None`` 이라는 값을 사용하십시오.

.. option:: -ignore_srcmaskband

    .. versionadded:: 3.3

    GDAL 3.3버전부터, 소스가 마스크 밴드를 (내부/외부 마스크 밴드, 또는 알파 밴드를) 가지고 있는 경우 VRT 드라이버에 소스의 마스크 밴드를 사용해서 합성 중인 픽셀을 마스킹하도록 지시하기 위해 기본적으로 <UseMaskBand>true</UseMaskBand> 상속(child) 요소로 <ComplexSource> 요소를 생성합니다. 이것은 NODATA 요소를 일반화(generalization)하는 것입니다. -ignore_srcmaskband 옵션을 지정할 때 소스의 마스크 밴드를 고려하지 않으며, 소스들 사이에 중첩이 발생하는 경우 중첩되는 영역에서 마지막 소스가 이전 소스를 무시할 것입니다.

.. option:: -b <band>

    처리한 입력 <band>를 선택합니다. 밴드 번호는 1부터 시작합니다. 입력 밴드를 설정하지 않는 경우 VRT에 모든 밴드를 추가할 것입니다. 입력 밴드 집합을 선택하기 위해 :option:`-b` 스위치를 여러 개 사용할 수도 있습니다.

.. option:: -sd< <subdataset>

    입력 데이터셋이 하위 데이터셋 몇 개를 담고 있는 경우 지정한 (1부터 시작하는) 번호로 하위 데이터셋을 사용할 수 있습니다. 하위 데이터셋 이름 전체를 입력하는 대신 쓸 수 있는 옵션입니다.

.. option:: -vrtnodata <value> [<value>...]

    VRT 밴드 수준에서 NODATA 값을 설정합니다. (각 밴드 별로 서로 다른 값을 지정할 수 있습니다.) 값을 하나 이상 지정하는 경우 모든 값들을 단일 운영체제 인수로써 따옴표로 묶어주어야 합니다. 이 옵션을 지정하지 않으면 첫 번째 데이터셋 상의 고유한 NODATA 설정을 (존재하는 경우) 사용할 것입니다. 이 옵션으로 설정한 값은 각 각 VRTRasterBand 요소의 NoDataValue 요소에 작성됩니다. 소스 데이터셋 상의 고유한 NODATA 설정을 무시하려면 ``None`` 이라는 값을 사용하십시오.

.. option:: -separate

    각 입력 파일을 개별 밴드로 배치합니다. 이런 경우, 각 데이터셋의 첫 번째 밴드만 새 밴드로 배치될 것입니다. 기본 모드와는 반대로, 모든 밴드가 동일한 데이터 유형이어야 할 필요는 없습니다.

.. option:: -allow_projection_difference

    이 옵션을 지정하면 유틸리티가 입력 데이터셋들이 동일한 투영법이 아니더라도 받아들여 VRT를 생성할 것입니다. 주의: 입력 데이터셋이 재투영될 것이라는 의미가 아닙니다. 그냥 입력 데이터셋의 투영법을 무시할 뿐입니다.

.. option:: -a_srs <srs_def>

    산출물 파일의 투영법을 무시합니다. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다. 어떤 재투영도 하지 않습니다.

.. option:: -r {nearest (default),bilinear,cubic,cubicspline,lanczos,average,mode}

    리샘플링 알고리즘을 선택합니다.

.. option:: -oo NAME=VALUE

    데이터셋 열기 옵션 (특정 포맷 지원)

    .. versionadded:: 2.2

.. option:: -input_file_list <mylist.txt>

    각 행에 입력 파일명을 가진 텍스트 파일을 지정합니다.

.. option:: -q

    콘솔의 진행 상태 막대(progress bar)를 비활성화합니다.

.. option:: -overwrite

    VRT가 이미 존재하는 경우 VRT를 덮어씁니다.

.. option:: -strict

    경고를 실패로 바꿉니다. 기본값인 -non_strict와 함께 사용할 수 없습니다.

    .. versionadded:: 3.4.2

.. option:: -non_strict

    경고를 받는 문제를 가진 소스 데이터셋을 건너뛰고 계속 진행합니다. 기본값입니다.

    .. versionadded:: 3.4.2

예시
--------

- 디렉터리에 있는 모든 TIFF 파일로부터 가상 모자이크를 생성합니다:

::

    gdalbuildvrt doq_index.vrt doq/*.tif

- 텍스트 파일에 파일명이 지정돼 있는 파일들로부터 가상 모자이크를 생성합니다:

::

    gdalbuildvrt -input_file_list my_list.txt doq_index.vrt


- 단일 밴드 입력 파일 3개로부터 RGB 가상 모자이크를 생성합니다:

::

    gdalbuildvrt -separate rgb.vrt red.tif green.tif blue.tif

- 배경색이 파란색(RGB: 0 0 255)인 가상 모자이크를 생성합니다:

::

    gdalbuildvrt -hidenodata -vrtnodata "0 0 255" doq_index.vrt doq/*.tif
