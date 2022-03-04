.. _gdallocationinfo:

================================================================================
gdallocationinfo
================================================================================

.. only:: html

    래스터 쿼리 도구

.. Index:: gdallocationinfo

개요
--------

.. code-block::

    Usage: gdallocationinfo [--help-general] [-xml] [-lifonly] [-valonly]
                            [-b band]* [-overview overview_level]
                            [-l_srs srs_def] [-geoloc] [-wgs84]
                            [-oo NAME=VALUE]* srcfile [x y]

설명
-----------

:program:`gdallocationinfo` 유틸리티는 다양한 좌표계 가운데 한 좌표계로 위치를 지정한 픽셀 하나에 대한 정보를 쿼리하는 메커니즘을 제공합니다. 리포트 작업을 위한 몇 가지 옵션이 있습니다.

.. program:: gdallocationinfo

.. option:: -xml

    편리한 포스팅을 위해 산출 리포트를 XML 서식으로 작성합니다.

.. option:: -lifonly

    데이터베이스를 대상으로 하는 LocationInfo 요청으로부터 (예를 들면 VRT로부터 영향을 받은 파일을 식별하기 위해) 파일명만 생성합니다.

.. option:: -valonly

    선택한 각 밴드에서 선택한 픽셀 값만 산출합니다.

.. option:: -b <band>

    쿼리할 밴드를 선택합니다. 밴드를 여러개 목록화할 수 있습니다. 기본적으로 모든 밴드를 쿼리합니다.

.. option:: -overview <overview_level>

    기반(base) 밴드 대신, <overview_level> 번째 오버뷰를 쿼리합니다. (overview_level을 1로 설정하면 첫 번째 오버뷰라는 의미입니다.) 이 경우에도 (좌표계가 픽셀/라인 단위인 경우) 기반 밴드에 따라 x, y 위치를 입력해야만 한다는 사실을 기억하십시오.

.. option:: -l_srs <srs_def>

    입력 x, y 위치의 좌표계입니다.

.. option:: -geoloc

    입력 x, y 포인트의 좌표계가 이미지의 지리참조 좌표계입니다.

.. option:: -wgs84

    입력 x, y 포인트의 좌표계가 WGS84 경도/위도입니다.

.. option:: -oo NAME=VALUE

    데이터셋 열기 옵션 (특정 포맷 지원)

.. option:: <srcfile>

    소스 GDAL 래스터 데이터셋의 이름입니다.

.. option:: <x>

    대상 픽셀의 X 위치입니다. -l_srs, -wgs84 또는 -geoloc을 설정하지 않았다면 기본 좌표계는 픽셀/라인 단위입니다.

.. option:: <y>

    대상 픽셀의 Y 위치입니다. -l_srs, -wgs84 또는 -geoloc을 설정하지 않았다면 기본 좌표계는 픽셀/라인 단위입니다. 


이 유틸리티의 목적은 픽셀에 대한 다양한 정보를 제공하는 것입니다. 현재 다음과 같은 정보를 리포트합니다:

- 픽셀/라인 공간에서 픽셀의 위치
- 데이터소스를 대상으로 하는 LocationInfo 메타데이터 쿼리의 결과. 해당 픽셀에 대한 요청을 만족시키기 위한, 그리고 :ref:`raster.mbtiles` 드라이버가 사용하는, 파일(들)을 리포트할 VRT 파일을 위해 구현되었습니다.
- 밴드 전체 또는 하위 집합에서 해당 픽셀의 래스터 픽셀 값
- 크기 조정 그리고/또는 오프셋이 밴드에 적용된 경우 크기 조정하기 전의 픽셀 값

명령줄에서 x/y 좌표를 입력해서, 또는 stdin으로부터 좌표를 읽어와서 선택한 픽셀을 요청합니다. stdin으로부터 좌표를 읽어오는 경우 좌표쌍을 하나 이상 지정할 수 있습니다. 기본적으로 픽셀/라인 좌표를 가정합니다. 하지만 :option:`-geoloc`, :option:`-wgs84`, 또는 :option:`-l_srs` 스위치를 사용하면 다른 좌표계로 위치를 지정할 수 있습니다.

기본 리포트는 사람이 읽을 수 있는 텍스트 서식입니다. -xml 스위치를 쓰면 XML 산출물을 대신 요청할 수 있습니다.

스크립트 작업 목적을 위해, 산출물을 실제 픽셀 값 또는 픽셀을 식별한 LocationInfo 파일로 제한하기 위한 -valonly 및 -lifonly 스위치를 사용할 수 있습니다.

향후 gdallocationinfo에 추가적인 리포트 작업 기능들이 추가될 것으로 기대하고 있습니다.

예시
--------

utm.tif 파일에 있는 (256,256) 픽셀에 대해 리포트 하는 간단한 예시입니다.

::

    $ gdallocationinfo utm.tif 256 256
    Report:
    Location: (256P,256L)
    Band 1:
        Value: 115

위치를 WGS84로 지정하는 VRT 파일을 쿼리하고, 그 결과를 XML 서식으로 받습니다.

::

    $ gdallocationinfo -xml -wgs84 utm.vrt -117.5 33.75
    <Report pixel="217" line="282">
        <BandReport band="1">
            <LocationInfo>
            <File>utm.tif</File>
            </LocationInfo>
            <Value>16</Value>
        </BandReport>
    </Report>

stdin으로부터 위치를 읽어옵니다.

::

    $ cat coordinates.txt
    443020 3748359
    441197 3749005
    443852 3747743
    
    $ cat coordinates.txt | gdallocationinfo -geoloc utmsmall.tif
    Report:
      Location: (38P,49L)
      Band 1:
        Value: 214
    Report:
      Location: (7P,38L)
      Band 1:
        Value: 107
    Report:
      Location: (52P,59L)
      Band 1:
        Value: 148
