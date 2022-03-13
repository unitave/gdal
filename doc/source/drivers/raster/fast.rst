.. _raster.fast:

================================================================================
FAST -- EOSAT FAST 포맷
================================================================================

.. shortname:: FAST

.. built_in_by_default::

이 드라이버는 FAST-L7A 포맷(랜드샛 TM 데이터)과 EOSAT FAST 포맷 C개정판(IRS-1C/1D 데이터) 읽기를 지원합니다. 이 포맷으로 된 다른 데이터셋(SPOT)을 읽으려고 한다면, 저자에게 연락하십시오. (안드레이 키셀료프(Andrey Kiselev), dron@ak4719.spb.edu) 데이터 샘플을 공유해줘야 합니다.

FAST 포맷 데이터셋은 하나 이상의 관리(administrative) 헤더와 RAW 포맷으로 된 실제 이미지 데이터를 가진 하나 이상의 파일 여러 개로 이루어져 있습니다. 관리 파일은 이미지 파일명을 포함하는 신(scene) 파라미터들에 대한 서로 다른 정보를 담고 있습니다. 관리 헤더를 가진 파일은 평문 아스키 텍스트이기 때문에, 어떤 텍스트 뷰어/편집기로도 읽을 수 있습니다.

이 드라이버는 관리 파일을 입력받아 이미지 파일명을 추출하고 데이터를 가져올 것입니다. 모든 파일을 밴드로 해석할 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

데이터
------

FAST-L7A
~~~~~~~~

FAST-L7A는 이미지 데이터를 가진 큰 파일들과 관리 정보를 가진 작은 파일 3개로 이루어져 있습니다. 이 드라이버에 관리 파일 가운데 하나를 입력해야 합니다:

-  L7fppprrr_rrrYYYYMMDD_HPN.FST: 밴드 1개를 가진 전정색(panchromatic) 밴드 헤더 파일
-  L7fppprrr_rrrYYYYMMDD_HRF.FST: 밴드 6개를 가진 VNIR/SWIR 밴드 헤더 파일
-  L7fppprrr_rrrYYYYMMDD_HTM.FST: 밴드 2개를 가진 열(thermal) 밴드 헤더 파일

해당 관리 파일에 대응하는 모든 RAW 이미지를 GDAL 밴드로 가져올 것입니다.

`1수준 상품 산출 파일 데이터 포맷 제어 지침서 <http://ltpwww.gsfc.nasa.gov/IAS/pdfs/DFCB_V5_B2_R4.pdf>`_ 의 내용 가운데:

"FAST-L7A 상품 파일을 위한 파일 명명 규범은 L7fppprrr_rrrYYYYMMDD_AAA.FST입니다. 이때 L7은 랜드샛 7호 미션, f는 ETM+ (1 또는 2) 포맷(특정 포맷에 속하는 데이터가 아닌 경우 기본값은 1), ppp는 상품의 시작 경로, rrr_rrr는 상품의 시작 및 종단 행, YYYYMMDD는 이미지 촬영 날짜, AAA는 파일 유형입니다. 파일 유형으로는 HPN(전정색 밴드 헤더 파일), HRF(VNIR/SWIR 밴드 헤더 파일), HTM(열 밴드 헤더 파일), B10(밴드1), B20(밴드2), B30(밴드3), B40(밴드4), B50(밴드5), B61(밴드6L), B62(밴드6H), B70(밴드7), B80(밴드8)을 지원합니다. FST는 FAST 파일 확장자입니다."

따라서 사용자는 드라이버에 다음 ``L7fppprrr_rrrYYYYMMDD_HPN.FST``, ``L7fppprrr_rrrYYYYMMDD_HRF.FST`` 또는
``L7fppprrr_rrrYYYYMMDD_HTM.FST`` 파일 가운데 하나를 입력해야 합니다.

IRS-1C/1D
~~~~~~~~~

FAST 포맷 C개정판은 관리 헤더에 밴드 파일명을 담고 있지 않습니다. 서로 다른 데이터 배포자들이 자신의 파일을 서로 다르게 명명하기 때문에, 밴드 파일명을 추정해야 합니다. GDAL의 FAST 드라이버에는 다음과 같은 여러 명명 스키마들이 소문자 또는 대문자로 하드코딩되어 있습니다:

``<header>.<ext> <header>.1.<ext> <header>.2.<ext> ...``

또는

``<header>.<ext> band1.<ext> band2.<ext> ...``

또는

``<header>.<ext> band1.dat band2.dat ...``

또는

``<header>.<ext> imagery1.<ext> imagery2.<ext> ...``

또는

``<header>.<ext> imagery1.dat imagery2.dat ...``

헤더 파일의 이름은 임의로 명명할 수 있습니다. 이런 스키마들은 배포자들이 사용하는 파일 명명 규범 대부분을 커버할 것입니다. 그러나 운이 나쁘게도 사용자의 데이터셋이 이런 스키마들과는 다르게 명명되었다면, GDAL로 데이터를 가져오기 전에 스키마에 맞춰 이름을 직접 수정해야 합니다.

GDAL은 Euromap GmbH가 IRS-1C/IRS-1D PAN, LISS3 및 WIFS 센서 용으로 개발한 데이터셋의 밴드 파일을 명명하기 위한 규범도 지원합니다. 이 파일명 규범은 `Euromap 명명 작업 규범 <http://www.euromap.de/download/em_names.pdf>`_ 에 설명되어 있습니다.

지리참조
------------

모든 USGS 투영법을 (이를테면 UTM, LCC, PS, PC, TM, OM, SOM을) 지원할 것입니다. 투영법을 제대로 추출할 수 없다면 저자에게 연락하십시오.

메타데이터
---------

각 밴드에 대한 교정 계수(calibration coefficient)를 메타데이터 항목으로 리포트합니다.

-  **ACQUISITION_DATE**: yyyyddmm 서식으로 된 첫 번째 신(scene) 촬영 날짜
-  **SATELLITE**: 첫 번째 신(scene)의 위성 이름
-  **SENSOR**: 첫 번째 신(scene)의 센서 이름
-  **BIASn**: **n** 채널에 대한 편향값(bias value)
-  **GAINn**: **n** 채널에 대한 이익값(gain value)

참고
--------

``gdal/frmts/raw/fastdataset.cpp`` 로 구현되었습니다.

http://ltpwww.gsfc.nasa.gov/IAS/htmls/l7_review.html 에서 Landsat FAST L7A 포맷 설명을 읽어볼 수 있습니다. (`ESDIS 1수준 상품 생성 시스템(LPGS) 산출 파일 DFCB, 5권 2호 <http://ltpwww.gsfc.nasa.gov/IAS/pdfs/DFCB_V5_B2_R4.pdf>`_ 참조)

http://www.euromap.de/docs/doc_001.html 에서 EOSAT FAST 포맷 설명서 C개정판을 읽어볼 수 있습니다.
