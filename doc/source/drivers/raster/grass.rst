.. _raster.grass:

================================================================================
GRASS 래스터 포맷
================================================================================

.. shortname:: GRASS

.. build_dependencies:: libgrass

GDAL은 기존 GRASS GIS 래스터 맵 또는 영상 그룹 읽기를 지원할 수 있는 선택 옵션을 가지고 있지만, 쓰기 또는 내보내기는 지원하지 않습니다. GRASS 라이브러리를 환경설정해야 GRASS 래스터 포맷에 대한 지원을 활성화하는데, 사전에 libgrass를 반드시 설치해야 합니다. (아래 메모 참조)

다음 몇 가지 방법으로 GRASS 래스터 맵 또는 영상 그룹을 선택할 수 있습니다.

#. ``cellhd`` 파일을 가리키는 전체 경로를 지정하면 됩니다. 상대 경로가 아니며, 최소한 GRASS 데이터베이스 루트 자체를 포함하는 GRASS 데이터베이스 내부의 모든 경로 구성요소를 담고 있어야만 합니다. 다음 예시는 ``/data/grassdb`` 에 위치한 GRASS 데이터베이스에 있는 "myloc" GRASS 위치(location)의 "PERMANENT" GRASS 맵셋(mapset) 내에 있는 "elevation" 래스터 맵을 엽니다.

   예시:

   ::

      gdalinfo /data/grassdb/myloc/PERMANENT/cellhd/elevation

#. 전체 영상 그룹을 단일 데이터셋으로 참조하려면 영상 그룹에 관한 정보를 담고 있는 디렉터리를 (또는 그 안에 있는 REF 파일을) 가리키는 전체 경로를 지정하면 됩니다. 다음 예시가 그런 내용입니다.

   예시:

   ::

      gdalinfo /data/grassdb/imagery/raw/group/testmff/REF
      gdalinfo /data/grassdb/imagery/raw/group/testmff

#. 사용자의 홈 디렉터리에 정확한 ``.grassrc7/rc`` (GRASS 7) 셋업 파일이 있는 경우 셀 또는 그룹명만으로 래스터 맵 또는 영상 그룹을 열 수도 있습니다. 래스터 맵 또는 영상 그룹이 GRASS 셋업 파일에 정의된 현재 GRASS 위치 및 맵셋에 있는 경우에만 이 방법이 작동합니다.

GDAL/GRASS 링크는 다음 기능을 지원합니다.

-  래스터 색상표로부터 나온 항목들을 256개(0-255)까지 읽어옵니다.
-  압축 및 비압축 정수형(CELL), 부동소수점형(FCELL) 그리고 배정밀도 부동소수점형(DCELL) 래스터 맵을 모두 지원합니다. 정수형 래스터 맵은 픽셀 당 1바이트 포맷을 사용하는 경우 "바이트" 밴드 유형으로 분류되고, 픽셀 당 2바이트 포맷을 사용하는 경우 "UInt16" 밴드 유형으로 분류됩니다. 두 경우 다 아니라면 래스터 맵을 "UInt32" 밴드 유형으로 취급합니다.
-  GRASS 포맷으로부터 지리참조 정보를 제대로 읽어옵니다.
-  좌표계 변환 시도를 하지만, 몇몇 변환의 경우 - 특히 원점(datum) 및 단위를 처리하는 경우 오류가 발생할 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

드라이버 변이형에 대한 메모
--------------------------

이 드라이버는 libgrass를 사용하는 대신 GRASS GIS 공유 라이브러리를 직접 사용할 수 있습니다. (순환 종속성(circular dependency)이 발생할 가능성이 있기 때문에 권장하지 않습니다.) 현재 이 드라이버의 두 가지 버전을 사용할 수 있으며, libgrass 변이형의 경우 ``--with-libgrass`` 를 이용해서, 또는 GRASS GIS 라이브러리 기반 버전의 경우 ``--with-grass=<dir>`` 를 이용해서 환경설정할 수 있습니다. GRASS 드라이버 버전은 현재 좌표계를 지원하지 않지만, 언젠가 수정될 것으로 전망합니다.

참고
--------

-  `GRASS GIS 홈페이지 <https://grass.osgeo.org>`_
-  `libgrass 페이지 <https://web.archive.org/web/20130730111701/http://home.gdal.org/projects/grass/>`_
