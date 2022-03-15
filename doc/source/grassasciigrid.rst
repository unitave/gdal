.. _raster.grassasciigrid:

================================================================================
GRASSASCIIGrid -- GRASS 아스키 그리드
================================================================================

.. shortname:: GRASSASCIIGrid

.. built_in_by_default::

이 드라이버는 (Arc/Info 아스키 그리드와 유사한) GRASS 아스키 그리드 포맷 읽기를 지원합니다.

기본적으로 GDAL이 GRASS 아스키 그리드 데이터셋에 반환하는 데이터 유형을 자동 탐지해서, 부동소수점형 값을 가진 그리드의 경우 Float32로 설정하고 그렇지 않은 경우 Int32로 설정합니다. 이 과정은 NULL 값의 서식과 그리드 데이터의 처음 100KB를 분석해서 이루어집니다. GRASSASCIIGRID_DATATYPE 환경설정 옵션을 설정하면 데이터 유형을 명확하게 지정할 수도 있습니다. (현재 Int32, Float32 및 Float64로 지정할 수 있습니다.)

주의: ``gdal/frmts/aaigrid/aaigriddataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
