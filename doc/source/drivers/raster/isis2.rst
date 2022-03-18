.. _raster.isis2:

================================================================================
ISIS2 -- USGS 천체 지질학 ISIS Cube (버전 2)
================================================================================

.. shortname:: ISIS2

.. built_in_by_default::

ISIS2는 USGS 행성 지도 제작(Planetary Cartography) 그룹이 행성 영상 데이터를 저장하고 배포하기 위해 사용하는 포맷입니다. GDAL은 ISIS2 포맷 영상 데이터 읽기 및 쓰기 접근을 지원합니다.

ISIS2 Cube 파일의 확장자는 거의 .cub이며, 관련 .lbl 라벨 파일을 가지고 있는 경우도 있습니다. .lbl 파일이 존재하는 경우 .cub 파일보다는 .lbl 파일을 데이터셋 이름으로 사용해야 합니다.

또한 거의 모든 ISIS2 영상 환경설정을 지원하기 위해, 이 드라이버는 지리참조와 좌표계 정보는 물론 선택한 다른 헤더 메타데이터도 읽어옵니다.

이 드라이버는 미국 지질조사국(United States Geological Survey)의 지원으로 구현되었습니다.

ISIS2는 PDS와 ISIS3를 포함하는 관련 포맷 패밀리의 일원입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

현재 ISIS2 작성기가 헤더를 이미지 구조 정보만 가지도록 정말 최소한으로 작성합니다. 좌표계 정보, 지리참조 정보 또는 다른 메타데이터를 수집하지 않습니다.

생성 옵션
~~~~~~~~~~~~~~~~

-  **LABELING_METHOD=ATTACHED/DETACHED**:
   영상과 동일한 파일에 헤더 라벨 작업을 해야 할지 여부를 결정합니다. 기본값 ATTACHED는 영상과 동일한 파일에 헤더 라벨을 작업하고, DETACHED로 설정하면 개별 파일에 작업합니다.

-  **IMAGE_EXTENSION=\ extension**:
   LABELING_METHOD=DETACHED 옵션으로 생성된 영상 파일에 사용할 확장자를 설정합니다. 기본값은 "cub"입니다. LABELING_METHOD를 DETACHED로 설정한 경우에만 사용할 수 있습니다.

참고
--------

-  ``gdal/frmts/pds/isis2dataset.cpp`` 로 구현되었습니다.
-  :ref:`raster.pds` 드라이버
-  :ref:`raster.isis3` 드라이버
