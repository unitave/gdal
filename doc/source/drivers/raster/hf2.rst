.. _raster.hf2:

================================================================================
HF2 -- HF2/HFZ 고도장 래스터
================================================================================

.. shortname:: HF2

.. built_in_by_default::

GDAL은 HF2/HFZ/HF2.GZ 고도장(heightfield) 래스터 데이터셋 읽기 및 쓰기를 지원합니다.

HF2는 연속되는 셀 값들 사이의 차를 기록하는 고도장 포맷입니다. HF2 파일을 GZip 알고리즘으로 압축할 수 있는 선택 옵션도 있기 때문에, HF2.GZ (또는 동일한 HFZ) 파일의 용량이 비압축 데이터보다 훨씬 작을 수도 있습니다. 이 파일 포맷은 사용자가 수직 정밀도 파라미터를 통해 원하는 정확도를 제어할 수 있게 해줍니다.

GDAL은 확장 헤더 블록을 통해 지리참조 정보를 읽고 쓸 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

생성 옵션
----------------

-  **COMPRESS=YES/NO**:
   파일을 GZip으로 압축해야만 하는지 여부를 설정합니다. 기본값은 NO입니다.

-  **BLOCKSIZE=block_size**:
   내부 타일 크기를 설정합니다. 8 이상으로 설정해야만 합니다. 기본값은 256입니다.

-  **VERTICAL_PRECISION=vertical_precision**:
   수직 정밀도의 값이 0을 초과하도록 설정해야만 합니다. 기본값은 0.01입니다.

수직 정밀도를 높게 설정할수록 - 특히 COMPRESS를 YES로 설정했다면 - 파일 용량도 작아지지만, 정확도에 손실이 생깁니다.

참고
--------

-  `HF2/HFZ 포맷 사양 <http://www.bundysoft.com/docs/doku.php?id=l3dt:formats:specs:hf2>`_
-  `HF2 확장 헤더 블록 사양 <http://www.bundysoft.com/docs/doku.php?id=l3dt:formats:specs:hf2#extended_header>`_
