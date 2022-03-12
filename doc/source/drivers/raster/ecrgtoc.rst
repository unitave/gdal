.. _raster.ecrgtoc:

================================================================================
ECRGTOC -- ECRG 목차 (TOC.xml)
================================================================================

.. shortname:: ECRGTOC

.. built_in_by_default::

이 드라이버는 ECRG(Enhanced Compressed Raster Graphic) 상품을 위한 읽기전용 판독기입니다. TOC.xml 목차(table of contents) 파일을 이용해서 목차에 담겨 있는 ECRG 프레임의 집합이 커버리지인 가상 데이터셋을 노출시킵니다.

이 드라이버는 TOC.xml 파일에서 찾은 각 하위 데이터셋에 대해 서로 다른 하위 데이터셋을 리포트할 것입니다. 각 하위 데이터셋은 동일한 상품 ID, 디스크 ID, 그리고 동일한 축척의 프레임들로 이루어져 있습니다.

다음은 TOC.xml 파일에 대한 gdalinfo 산출물의 예시입니다:

::

   Subdatasets:
     SUBDATASET_1_NAME=ECRG_TOC_ENTRY:ECRG:FalconView:1_500_K:ECRG_Sample/EPF/TOC.xml
     SUBDATASET_1_DESC=Product ECRG, Disk FalconView, Scale 1:500 K

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::


참고
--------

-  :ref:`raster.nitf`: ECRG 프레임의 포맷
-  `MIL-PRF-32283 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28030000+-+79999%29/MIL-PRF-32283_26022/>`_: ECRG 상품의 사양

주의: ``gdal/frmts/nitf/ecrgtocdataset.cpp`` 로 구현되었습니다.
