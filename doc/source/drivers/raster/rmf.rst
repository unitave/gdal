.. _raster.rmf:

================================================================================
RMF -- 래스터 행렬 포맷
================================================================================

.. shortname:: RMF

.. built_in_by_default::

RMF(Raster Matrix Format)는 "GIS Integration"과 "GIS Panorama"에서 사용되는 단순 타일화 래스터 포맷입니다. 포맷 자체의 케이퍼빌리티는 아주 허술합니다.

RMF에는 MTW과 RSW라는 두 가지 변이형이 있습니다. MTW는 단일 채널에 16비트 정수형 및 32/64비트 부동소수점형 포인트 데이터를 지원하며 DEM 데이터 저장을 목표로 하는 포맷입니다. RSW는 일반적인 목적을 가진 래스터 포맷입니다. RSW는 색상 맵을 가진 단일 채널 또는 RGB 3채널 이미지를 지원합니다. RSW에는 8비트 데이터만 저장할 수 있습니다. 이 두 이미지 유형 모두 단순 지리참조 정보를 제공할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

메타데이터
--------

-  **ELEVATION_MINIMUM**:
   최저 표고값입니다. (MTW 전용)

-  **ELEVATION_MAXIMUM**:
   최고 표고값입니다. (MTW 전용)

-  **ELEVATION_UNITS**:
   래스터 값을 위한 단위의 이름입니다. (MTW 전용)
   "m"(미터), "cm"(센티미터), "dm"(데시미터, 10cm), "mm"(밀리미터) 가운데 하나일 수 있습니다.

-  **ELEVATION_TYPE**:
   0(절대 표고) 또는 1(총 표고) 가운데 하나일 수 있습니다. MTW 전용입니다.

열기 옵션
------------

-  **RMF_SET_VERTCS**:
   이 옵션을 ON으로 설정하면, 수직 좌표계 설명이 존재하는 경우 레이어 공간 좌표계가 수직 좌표계를 포함할 것입니다. 같은 이름의 환경설정 옵션을 통해 이 기능을 활성화시킬 수 있습니다.

생성 옵션
----------------

-  **MTW=ON**:
   MTW 행렬을 강제로 생성합니다. (이 옵션을 설정하지 않는 경우 기본값인 RSW를 생성할 것입니다.)

-  **BLOCKXSIZE=n**:
   타일 너비를 설정합니다. 기본값은 256입니다.

-  **BLOCKYSIZE=n**:
   타일 높이를 설정합니다. 기본값은 256입니다.

-  **RMFHUGE=NO/YES/IF_SAFER**:
   대용량 RMF 파일을 생성할지를 설정합니다. (GIS Panorama 버전 11부터 지원합니다.) 기본값은 NO입니다.

-  **COMPRESS=NONE/LZW/JPEG/RMF_DEM**: (GDAL 2.4버전부터)
   압축 유형을 설정합니다. 기본값은 NONE입니다.
   주의: RGB(3밴드) 바이트형 데이터셋만 JPEG 압축을 지원합니다. Int32 단일 채널 MTW 데이터셋만 RMF_DEM 압축을 지원합니다.

-  **JPEG_QUALITY**: (GDAL 2.4버전부터)
   JPEG 이미지 품질을 1에서 100 사이의 값으로 설정합니다. 기본값은 75입니다.

-  **NUM_THREADS=number_of_threads/ALL_CPUS**: (GDAL 2.4버전부터)
   작업자 스레드 개수를 지정해서 멀티스레딩 압축을 활성화시킵니다. 기본값은 주 스레드에서 압축하는 것입니다.

참고
---------

-  ``gdal/frmts/rmf/rmfdataset.cpp`` 로 구현되었습니다.

-  `GIS Panorama 홈페이지 <https://www.gisinfo.net/>`_
