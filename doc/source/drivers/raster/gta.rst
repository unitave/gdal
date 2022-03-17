.. _raster.gta:

================================================================================
GTA - 일반 태그 배열(Generic Tagged Arrays)
================================================================================

.. shortname:: GTA

.. build_dependencies:: libgta

GDAL은 libgta 라이브러리를 통해 GTA 데이터 파일을 읽고 쓸 수 있습니다.

GTA는 모든 유형의 다중 차원 배열 데이터를 저장할 수 있는 파일 포맷으로, 배열 데이터를 범용 조작할 수 있고 다른 파일 포맷들과 쉽게 변환할 수 있도록 해줍니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

생성 옵션
----------------

-  **COMPRESS=method**: GTA 압축 방법을 설정합니다. NONE(기본값) 또는 BZIP2, XZ, ZLIB, ZLIB1, ZLIB2, ZLIB3, ZLIB4, ZLIB5, ZLIB6, ZLIB7, ZLIB8, ZLIB9 가운데 하나를 선택할 수 있습니다.

참고
--------

-  `GTA 홈페이지 <http://gta.nongnu.org>`_
