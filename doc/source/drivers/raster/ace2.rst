.. _raster.ace2:

================================================================================
ACE2 -- ACE2
================================================================================

.. shortname:: ACE2

.. built_in_by_default::

이 드라이버는 ACE2 DEM을 읽기 위한 편의적인 드라이버입니다. ACE2 DEM 파일은 원본(raw) 바이너리 데이터를 담고 있습니다. 파일 이름이 전적으로 지리참조를 결정합니다. 품질, 소스 그리고 신뢰(confidence) 레이어는 Int16 유형인 반면, 표고 데이터는 Float32 유형으로 반환됩니다.

`ACE2 상품 개요 <http://tethys.eaprs.cse.dmu.ac.uk/ACE2/shared/overview>`_

주의: ``gdal/frmts/raw/ace2dataset.cpp`` 로 구현되었습니다.


드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
