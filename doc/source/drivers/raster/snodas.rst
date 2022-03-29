.. _raster.snodas:

================================================================================
SNODAS -- 강설 데이터 동화 시스템
================================================================================

.. shortname:: SNODAS

.. built_in_by_default::

이 드라이버는 강설 데이터 동화 시스템(Snow Data Assimilation System) 데이터를 읽는 데 편리합니다. SNODAS 데이터 파일은 Int16형 RAW 바이너리 데이터를 담고 있습니다. GDAL에는 .Hdr 파일을 입력해야 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
----

-  ``gdal/frmts/raw/snodasdataset.cpp`` 로 구현되었습니다.

-  `NSIDC 강설 데이터 동화 시스템(SNODAS) 데이터 상품 <http://nsidc.org/data/docs/noaa/g02158_snodas_snow_cover_model/index.html>`_

