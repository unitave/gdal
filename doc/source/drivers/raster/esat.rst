.. _raster.esat:

================================================================================
ESAT -- Envisat 이미지 상품
================================================================================

.. shortname:: ESAT

.. built_in_by_default::

GDAL은 Envisat 상품 읽기 접근을 지원합니다. 모든 샘플 유형을 지원합니다. 일치하는 측정 데이터셋(MDS; measurement dataset) 2개를 가진 파일은 밴드 2개를 가진 것으로 표현됩니다. 현재 ASAR 1수준 이상의 모든 상품과 일부 MERIS 및 AATSR 상품을 지원합니다.

사용 가능한 경우, 일반적으로 데이터셋의 괜찮은 커버리지를 제공하는 GEOLOCATION GRID ADS 데이터셋의 제어 포인트들을 읽어옵니다. GCP는 WGS84 좌표계를 사용합니다.

MPH 및 SPH(제1 및 제2 헤더)로부터 나온 사실상 모든 키/값 쌍들을 데이터셋 수준 메타데이터를 통해 복사합니다.

"RECORDS" 메타데이터 도메인을 사용하면 (지리위치 레코드를 제외한) ADS 및 GADS 레코드에 담겨 있는 ASAR 및 MERIS 파라미터들을 키/값 쌍으로 가져올 수 있습니다.

주의: ``gdal/frmts/envisat/envisatdataset.cpp`` 로 구현되었습니다.

참고: ESA의 `Envisat 데이터 상품 <http://envisat.esa.int/dataproducts/>`_

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::
