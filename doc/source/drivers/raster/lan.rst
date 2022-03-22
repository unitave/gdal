.. _raster.lan:

================================================================================
LAN -- ERDAS 7.x .LAN 및 .GIS
================================================================================

.. shortname:: LAN

.. built_in_by_default::

GDAL은 ERDAS 7.x .LAN 및 .GIS 래스터 파일의 읽기와 쓰기를 지원합니다. 현재 4비트, 8비트, 16비트 픽셀 데이터 유형을 읽을 수 있으며, 8비트 및 16비트 픽셀 데이터 유형을 쓸 수 있습니다.

GDAL은 실제로 LAN/GIS 파일로부터 맵 범위(지리변형)를 읽어와서 좌표계 정보를 읽으려 할 것입니다. 하지만 이 파일 포맷은 완전한 좌표계 정보를 포함하지 않기 때문에, SPCS(State Plane Coordinate System)와 UTM 좌표계인 경우 무결한 선형 단위를 가진 LOCAL_CS 정의를 반환하지만 그 이상 의미 있는 정보는 제공하지 않습니다.

현재 .TRL, .PRO 및 월드 파일을 무시합니다.

주의: ``gdal/frmts/raw/landataset.cpp`` 로 구현되었습니다.

이 드라이버는 (`PeopleGIS <http://www.peoplegis.com>`_ 사의) 케빈 플랜더스(Kevin Flanders)의 재정 지원으로 개발되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
