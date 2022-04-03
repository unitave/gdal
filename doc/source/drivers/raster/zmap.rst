.. _raster.zmap:

================================================================================
ZMap -- ZMap 플러스 그리드
================================================================================

.. shortname:: ZMAP

.. built_in_by_default::

GDAL은 ZMap 플러스 그리드(ZMap Plus Grid) 포맷의 읽기 접근 및 생성을 지원합니다. 이 포맷은 아스키 라인 서식으로 된 그리드화 데이터를 전송 및 저장하기 위한 아스키 정보 교환 포맷(ASCII interchange format)입니다. 유전 및 가스전 탐사 현장의 응용 프로그램에서 흔하게 쓰이는 포맷입니다.

기본적으로, PIXEL_IS_AREA 규범에 따라 파일을 해석하고 작성합니다. ZMAP_PIXEL_IS_POINT 환경설정 옵션을 TRUE로 설정하는 경우, PIXEL_IS_POINT 규범을 따라 파일을 해석하고 작성할 것입니다. (이때 파일 헤더의 지리참조 값들을 픽셀 중앙 좌표로 간주할 것입니다.) 이런 경우 GDAL이 기본 PIXEL_IS_AREA 규범에 따라 범위를 리포트할 것이라는 사실을 기억하십시오. (GDAL이 리포트하는 좌상단 모서리의 좌표가 파일에 나타나는 좌표값보다 위쪽으로 좌쪽으로 픽셀 반 개 거리만큼 더 길어질 것입니다.)

`GDAL-dev 메일링 리스트 스레드 <http://lists.osgeo.org/pipermail/gdal-dev/2011-June/029173.html>`_ 에서 비공식 사양을 찾아볼 수 있습니다.

주의: ``gdal/frmts/zmap/zmapdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

