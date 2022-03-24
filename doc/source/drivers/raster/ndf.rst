.. _raster.ndf:

================================================================================
NDF -- NLAPS 데이터 포맷
================================================================================

.. shortname:: NDF

.. built_in_by_default::

GDAL은 NLAPS 데이터 포맷 파일 읽기를 제한적으로 지원합니다. 이 포맷은 USGS EROS(Earth Resources Observation and Science) 데이터 센터가 랜드샛(Landsat) 데이터를 배포하기 위해 주로 사용합니다. NDF 데이터셋은 (확장자가 주로 .H1인) 헤더 파일 및 1개 이상의 (확장자가 주로 .I1, .I2, ...인) 관련 RAW 데이터 파일로 이루어져 있습니다. NDF 데이터셋을 열려면 확장자가 .H1, .H2 또는 .HD일 수도 있는 헤더 파일을 선택하십시오.

NDF 드라이버는 8비트 데이터만 지원합니다. 유일하게 지원하는 투영법은 UTM입니다. NDF 버전 1(NDF_VERSION=0.00) 및 버전 2 둘 다 지원합니다.

주의: ``gdal/frmts/raw/ndfdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
-----

`NLAPS 데이터 포맷 사양 <http://landsat.usgs.gov/documents/NLAPSII.pdf>`_

