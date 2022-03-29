.. _raster.srp:

================================================================================
SRP -- 표준 상품 포맷 (ASRP/USRP) (.gen)
================================================================================

.. shortname:: SRP

.. built_in_by_default::

(DGIWG가 정의하는) ASRP와 USRP 래스터 상품은 공통 표준 상품 포맷(Common Standard Product Format)의 변이형으로, GDAL이 읽기를 지원합니다. ASRP와 USRP 데이터셋은 일반적으로 공통 기본명을 가진 .GEN, .IMG, .SOU 및 .QAL 파일들로 이루어져 있습니다. 데이터셋에 접근하려면 .IMG 파일을 선택해야 합니다.

(지리 좌표계를 사용하는) ASRP와 (UTM/UPS 좌표계를 사용하는) USRP 상품은 색상표와 지리참조 정보를 가진 단일 밴드 이미지입니다.

.THF 전송 헤더 파일(Transmission Header File)도 GDAL에 입력할 수 있습니다. .THF 파일이 하나 이상의 이미지를 참조하는 경우, GDAL은 이미지가 하위 데이터셋으로 구성돼 있다고 리포트할 것입니다. .THF 파일이 이미지 하나만 참조한다면, GDAL은 이미지를 직접 열 것입니다.

주의: ``gdal/frmts/adrg/srpdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
