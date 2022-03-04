.. _gdal_edit:

================================================================================
gdal_edit.py
================================================================================

.. only:: html

    기존 GDAL 데이터셋의 다양한 정보를 제자리 편집합니다.

.. Index:: gdal_edit

개요
--------

.. code-block::

    gdal_edit [--help-general] [-ro] [-a_srs srs_def]
            [-a_ullr ulx uly lrx lry] [-a_ulurll ulx uly urx ury llx lly]
            [-tr xres yres] [-unsetgt] [-unsetrpc] [-a_nodata value] [-unsetnodata]
            [-unsetstats] [-stats] [-approx_stats]
            [-setstats min max mean stddev]
            [-scale value] [-offset value] [-units value]
            [-colorinterp_X red|green|blue|alpha|gray|undefined]*
            [-gcp pixel line easting northing [elevation]]*
            [-unsetmd] [-oo NAME=VALUE]* [-mo "META-TAG=VALUE"]*  datasetname

설명
-----------

:program:`gdal_edit.py` 스크립트를 사용해서 기존 GDAL 데이터셋의 다양한 (투영법, 지리변형, NODATA, 메타데이터) 정보를 제자리(in place) 편집할 수 있습니다.

기존 데이터셋에 업데이트 접근을 지원하는 래스터 포맷과만 작동합니다.

.. caution::

    포맷에 따라, 업데이트된 정보의 예전 값들이, 더 이상 GDAL API를 통해 접근할 수 없을지라도, 파일에 "유령" 상태로 남아 있을 수도 있습니다. 예를 들면 :ref:`raster.gtiff` 포맷이 그런 경우입니다. (완전한 목록은 아닙니다.)

.. option:: --help-general

    일반 GDAL 명령줄 옵션을 위한 간단한 활용 메시지를 출력하고 엑시트합니다.

.. option:: -ro

    데이터셋을 읽기전용(read-only) 모드로 엽니다. 업데이트 모드에서 데이터셋을 사용하기를 거부하는 드라이버의 경우 유용할 수도 있습니다. 이런 경우라면, 업데이트된 정보가 PAM :file:`.aux.xml` 파일로 들어갑니다.

.. option:: -a_srs <srs_def>

    대상 좌표계를 정의합니다. 데이터셋에 이 좌표계를 작성할 것입니다. 비어 있는 문자열 또는 ``None`` 을 지정하면 기존 좌표계를 제거할 것입니다. (TIFF/GeoTIFF의 경우, 이 외에는 잘 지원하지 않을 수도 있습니다.)

.. option:: -a_ullr ulx uly lrx lry:

    데이터셋의 지리참조 경계를 할당/무시합니다.

.. option:: -a_ulurll ulx uly urx ury llx lly:

    데이터셋의 지리참조 경계를 (좌상단, 우상단, 좌하단) 포인트 3개로부터 할당/무시합니다. :option:`-a_ullr` 와는 달리, 이 옵션은 기울어진 (경계가 좌표계 축과 평행하지 않은) 데이터셋도 지원합니다.

    .. versionadded:: 3.1

.. option:: -tr <xres> <yres>

    대상 해상도를 설정합니다. 값을 지리참조 단위로 표현해야만 합니다. 두 값 모두 양의 값이어야만 합니다.

.. option:: -unsetgt

    지리참조 정보를 제거합니다.

.. option:: -unsetrpc

    RPC 정보를 제거합니다.

    .. versionadded:: 2.4

.. option:: -unsetstats

    밴드 통계 정보를 제거합니다.

    .. versionadded:: 2.0

.. option:: -stats

    밴드 통계를 계산해서 저장합니다.

    .. versionadded:: 2.0

.. option:: -setstats min max mean stddev

    밴드 통계에 (최소값, 최대값, 평균값, 표준 편차) 사용자 정의값을 저장합니다. 네 값 중에 하나라도 ``None`` 으로 설정하면, 파일로부터 실제 통계를 계산해서 ``None`` 으로 설정된 값에 실제 통계값을 사용합니다.

    .. versionadded:: 2.4

.. option:: -approx_stats

    밴드 통계 근사치를 계산해서 저장합니다.

    .. versionadded:: 2.0

.. option:: -a_nodata <value>

    산출 밴드에 지정한 NODATA 값을 할당합니다.

.. option:: -unsetnodata

    기존 NODATA 값을 제거합니다.

    .. versionadded:: 2.1

.. option:: -scale <value>

    산출 밴드에 지정한 크기 조정(scale) 값을 할당합니다. 크기 조정 값을 하나만 지정하면 해당 값을 모든 밴드에 대해 설정할 것입니다. 또는 밴드 하나마다 크기 조정 값 하나를 지정할 수도 있습니다. 이 경우 크기 조정 값의 개수와 밴드의 개수가 일치해야만 합니다. 크기를 조정할 필요가 없다면, 값을 1로 설정하도록 권장합니다. 크기 조정과 오프셋은 보통 함께 쓰입니다. 예를 들면, 표고를 -100에서 시작하는 정확도 0.1인 부호 없는 16비트 정수형 파일에 저장하기 위해 크기 조정과 오프셋을 사용할 수도 있습니다. 이때 실제 값은 true_value = (pixel_value * scale) + offset 공식으로 계산될 것입니다.

    .. note::
        
        :program:`gdal_translate` 실행 도중 -unscale을 사용하면 이 값들을 적용할 수 있습니다.

    .. versionadded:: 2.2

.. option:: -offset <value>

    산출 밴드에 지정한 오프셋(offset) 값을 할당합니다. 오프셋 값을 하나만 지정하면 해당 값을 모든 밴드에 대해 설정할 것입니다. 또는 밴드 하나마다 오프셋 값 하나를 지정할 수도 있습니다. 이 경우 오프셋 값의 개수와 밴드의 개수가 일치해야만 합니다. 오프셋을 적용할 필요가 없다면, 값을 0으로 설정하도록 권장합니다. 더 자세한 내용은 scale 옵션을 참조하십시오.

    .. versionadded:: 2.2

.. option:: -units <value>

    산출 밴드(들)에 단위를 할당합니다.

    .. versionadded:: 3.1

.. option:: -colorinterp_X red|green|blue|alpha|gray|undefined

    밴드 X의 색상 해석을 변경합니다. (이때 X는 1부터 시작하는 유효한 밴드 번호입니다.)

    .. versionadded:: 2.3

.. option:: -gcp pixel line easting northing [elevation]

    데이터셋에 지정한 GCP를 추가합니다. GCP 집합을 설정하기 위해 이 옵션을 여러 번 반복할 수도 있습니다.

.. option:: -unsetmd

    (기본 메타데이터 도메인에 있는) 기존 메타데이터를 제거합니다. :option:`-mo` 옵션과 함께 사용할 수 있습니다.

    .. versionadded:: 2.0

.. option:: -mo META-TAG=VALUE

    가능하다면 산출 데이터셋에 설정할 메타데이터 키와 값을 전송(pass)합니다. :option:`-unsetmd` 옵션도 함께 지정된 경우가 아니라면 기존 메타데이터 항목에 이 메타데이터를 추가합니다.

.. option:: -oo NAME=VALUE

    열기 옵션입니다. (특정 포맷 지원)

    .. versionadded:: 2.0

:option:`-a_ullr`, :option:`-a_ulurll`, :option:`-tr` 및 :option:`-unsetgt` 옵션은 서로 함께 사용할 수 없습니다.

:option:`-unsetstats` 와 :option:`-stats` 옵션, 또는 :option:`-unsetstats` 와 :option:`-approx_stats` 옵션은 함께 사용할 수 없습니다.

예시
-------

.. code-block::

    gdal_edit -mo DATUM=WGS84 -mo PROJ=GEODETIC -a_ullr 7 47 8 46 test.ecw

.. code-block::

    gdal_edit -scale 1e3 1e4 -offset 0 10 twoBand.tif
