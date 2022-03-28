.. _raster.sar_ceos:

================================================================================
SAR_CEOS -- CEOS SAR 이미지
================================================================================

.. shortname:: SAR_CEOS

.. built_in_by_default::

이 드라이버는 CEOS SAR 이미지 파일을 위한 읽기전용 판독기입니다. 이 드라이버를 사용하려면 주 영상 파일을 선택하십시오.

이 드라이버는 SLC(Single Look Complex) 상품을 포함하는 레이더샛, JERS-1 및 ERS 데이터 상품 대부분을 처리합니다. 하지만 레이더샛 계열이 아닌 CEOS 상품은 처리하지 못 할 것입니다. 이런 상품에는 더 단순한 `CEOS <#CEOS>`_ 드라이버가 어울립니다.

이 드라이버는 스캔 라인 별 CEOS 수퍼스트럭처 정보를 샘플링해서 위도/경도 GCP 15개를 읽어오려 시도할 것입니다. 알래스카 위성 운영 시설에서 나온 상품이라면, ScanSAR 상품의 경우 맵 투영 레코드로부터 또는 ScanSAR 상품이 아닌 경우 시설 데이터 레코드로부터 모서리 좌표를 수집할 것입니다. 또한 다양한 헤더 파일들로부터 다음을 포함하는 다양한 메타데이터를 수집합니다:

::

     CEOS_LOGICAL_VOLUME_ID=EERS-1-SAR-MLD
     CEOS_FACILITY=CDPF-RSAT
     CEOS_PROCESSING_FACILITY=APP
     CEOS_PROCESSING_AGENCY=CCRS
     CEOS_PROCESSING_COUNTRY=CANADA
     CEOS_SOFTWARE_ID=APP 1.62
     CEOS_ACQUISITION_TIME=19911029162818919
     CEOS_SENSOR_CLOCK_ANGLE=  90.000
     CEOS_ELLIPSOID=IUGG_75
     CEOS_SEMI_MAJOR=    6378.1400000
     CEOS_SEMI_MINOR=    6356.7550000

SAR_CEOS 드라이버는 SIR-C 및 PALSAR 편광 데이터도 일부 지원합니다. SIR-C 포맷은 `여기 <http://southport.jpl.nasa.gov/software/dcomp/dcomp.html>`_ 에 설명된 대로 압축 분산 행렬 형식의 이미지를 담고 있습니다. GDAL은 이 데이터를 읽어오면서 압축 해제합니다. PALSAR 포맷은 3x3 에르미트 공분산 행렬의 요소들에 거의 정확하게 대응하는 밴드들을 담고 있습니다. 이에 대한 완전한 설명을 원한다면 `ERSDAC-VX-CEOS-004A.pdf <http://www.ersdac.or.jp/palsar/palsar_E.html>`_ 문서를 읽어보십시오. (픽셀 저장소는 193페이지에 설명되어 있습니다.) GDAL은 이 밴드들을 읽어오면서 복소수 부정소수점형 공분산 행렬 밴드로 변환합니다. 분산 행렬 요소 HH, HV(=VH), 그리고 VV 면에서 공분산 행렬을 표현하기 위해 쓰이는 규범은 아래 목록과 같습니다. 행렬의 비대각(non-diagonal) 요소는 복소수값인 반면, 대각 요소의 값은 (복소수 밴드로 표현되긴 하지만) 실수라는 사실을 기억하십시오.

-  밴드 1: Covariance_11 (Float32) = HH*conj(HH)
-  밴드 2: Covariance_12 (CFloat32) = sqrt(2)*HH*conj(HV)
-  밴드 3: Covariance_13 (CFloat32) = HH*conj(VV)
-  밴드 4: Covariance_22 (Float32) = 2*HV*conj(HV)
-  밴드 5: Covariance_23 (CFloat32) = sqrt(2)*HV*conj(VV)
-  밴드 6: Covariance_33 (Float32) = VV*conj(VV)

이때 sqrt는 제곱근, conj는 켤레 복소수(complex conjugate)라는 뜻입니다.

밴드 식별 정보는 메타데이터에도 반영되어 있습니다.

주의: ``gdal/frmts/ceos2/sar_ceosdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

