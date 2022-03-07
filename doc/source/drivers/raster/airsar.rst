.. _raster.airsar:

================================================================================
AIRSAR -- AIRSAR 편광 포맷
================================================================================

.. shortname:: AIRSAR

.. built_in_by_default::

GDAL은 AIP(AIRSAR Integrated Processor)가 만든 AIRSAR 편광(polarimetric) 포맷의 변이형 대부분을 읽어오기 위해 이 포맷을 지원합니다. AIRSAR 상품은 일반적으로 다양한 관련 데이터 파일들을 포함하지만, GDAL은 영상 데이터 자체만 지원합니다. 영상 데이터의 이름은 일반적으로 *mission*\ \_l.dat (L밴드) 또는 *mission*\ \_c.dat (C밴드)입니다.

AIRSAR 포맷은 압축 스토크스(Stokes) 행렬 형태로 된 편광 이미지입니다. GDAL 내부에서 데이터를 스토크스 행렬로 압축 해제한 다음 공분산(covariance) 행렬로 변환합니다. 이때 3x3 에르미트(Hermite) 공분산 행렬을 정의하기 위해 필요한 값 6개인 밴드 6개를 반환합니다. 아래에 산란 행렬 요소인 HH, HV(=VH), 그리고 VV라는 의미에서 공분산 행렬을 표현하기 위해 쓰이는 규범을 정리해놓았습니다. 행렬의 비대각(non-diagonal) 요소는 복잡 값(complex value)인 반면, 대각 요소의 값은 (복잡 밴드로 표현되기는 해도) 실수형이라는 사실을 기억하십시오.

-  밴드 1: Covariance_11 (Float32) = HH*conj(HH)
-  밴드 2: Covariance_12 (CFloat32) = sqrt(2)*HH*conj(HV)
-  밴드 3: Covariance_13 (CFloat32) = HH*conj(VV)
-  밴드 4: Covariance_22 (Float32) = 2*HV*conj(HV)
-  밴드 5: Covariance_23 (CFloat32) = sqrt(2)*HV*conj(VV)
-  밴드 6: Covariance_33 (Float32) = VV*conj(VV)

밴드의 식별 정보는 메타데이터 및 밴드 설명에도 반영되어 있습니다.

AIRSAR 상품 포맷은 (잠재적으로) 정보 헤더를 여러 개 포함하고 있습니다. 이 정보를 수집해서 전체 파일에 메타데이터로 표현합니다. 메인 헤더의 정보 항목에는 접두어 "MH\_"가, 파라미터 헤더의 항목에는 접두어 "PH\_"가, 그리고 캘리브레이션(calibration) 헤더의 정보에는 접두어 "CH\_"가 붙습니다. 메타데이터 항목 이름은 헤더 자체에 있는 필드 이름으로부터 자동으로 파생됩니다.

*mission*\ \_l.mocomp, *mission*\ \_meta.airsar 또는 *mission*\ \_meta.podaac 같은 AIRSAR 상품 관련 파일들은 읽어오지 않습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::

참고
--------

-  `AIRSAR 데이터 포맷 <http://airsar.jpl.nasa.gov/documents/dataformat.htm>`_
