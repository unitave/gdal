.. _raster.lcp:

================================================================================
LCP -- FARSITE v4 LCP 포맷
================================================================================

.. shortname:: LCP

.. built_in_by_default::

FARSITE v4 LCP(LandScaPe) 파일은 FARSITE, FLAMMAP, 그리고 FBAT (`www.fire.org <http://www.fire.org>`_) 같은 황무지 화재 습성 및 화재 영향 시뮬레이션 모델에 쓰이는 다중 밴드 래스터 포맷입니다. LCP 파일의 밴드에 지형, 수관(樹冠; tree canopy), 그리고 지표 연소 물질을 서술하는 데이터를 저장합니다. `LANDFIRE 데이터 배포 사이트 <https://landfire.cr.usgs.gov/viewer/>`_ 에서 LCP 포맷으로 된 데이터를 배포하며, FARSITE 및 `LFDAT <http://www.landfire.gov/datatool.php>`_ 같은 프로그램이 입력 래스터 집합으로부터 LCP 파일을 생성할 수 있습니다.

LCP 파일(.lcp)은 기본적으로 아래에서 설명하는 7,316바이트 용량의 헤더를 가진 RAW 포맷입니다. 모든 밴드의 데이터 유형은 부호 있는 16비트 정수형입니다. 밴드는 픽셀 교차삽입 유형입니다. 표고, 경사, 경사 방향, 연소 물질 모델, 그리고 수관 차폐율(tree canopy cover) 5개의 밴드는 필수적입니다. 수관 연소 물질 밴드(수관 높이, 수관 기준(base) 높이, 수관 부피 밀도) 그리고 지표 연소 물질 밴드(분탄(duff), 조잡 목질 쇄설물(coarse woody debris))는 선택적입니다.

LCP 드라이버는 선형 단위, 셀 크기 그리고 범위를 읽어오지만, LCP 파일은 투영법을 지정하지 않습니다. 보통 UTM 투영법을 사용하지만, 다른 투영법일 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

메타데이터
---------

GDAL LCP 드라이버는 데이터셋 수준 및 밴드 수준 메타데이터를 리포트합니다:

데이터셋
~~~~~~~

-  LATITUDE: 데이터셋의 위도, 남반구의 경우 음의 값

-  LINEAR_UNIT: 피트 또는 미터

-  DESCRIPTION: LCP 파일 설명

밴드
~~~~

-  <band>_UNIT 또는 <band>_OPTION: 밴드 용 단위 또는 옵션 코드

-  <band>_UNIT_NAME 또는 <band>_OPTION_DESC: 단위/옵션을 설명하는 이름

-  <band>_MIN: 최소값

-  <band>_MAX: 최대값

-  <band>_NUM_CLASSES: 범주(class) 개수, 100을 초과하는 경우 -1

-  <band>_VALUES: 쉼표로 구분된 범주 값들의 목록 (연소 물질 모델 밴드 전용)

-  <band>_FILE: 밴드의 원본 입력 래스터 파일명

**주의**: LCP 드라이버는 gdal/frmts/raw에 선언된 RawDataset 도우미(helper) 클래스로부터 파생되었습니다. 따라서 gdal/frmts/raw/lcpdataset.cpp로 구현되어야 합니다.

생성 옵션
----------------

LCP 드라이버는 CreateCopy() 메소드를 지원하며, 생성 옵션을 통해 메타데이터 값을 설정할 수 있습니다. 다음은 기본값을 첫 항목으로 서술한 옵션 목록입니다:

-  **ELEVATION_UNIT=[METERS/FEET]**:
   표고 밴드 용 수직 단위입니다.

-  **SLOPE_UNIT=[DEGREES/PERCENT]**

-  **ASPECT_UNIT=[AZIMUTH_DEGREES/GRASS_CATEGORIES/GRASS_DEGREES]**

-  **FUEL_MODEL_OPTION=[NO_CUSTOM_AND_NO_FILE/CUSTOM_AND_NO_FILE/NO_CUSTOM_AND_FILE/CUSTOM_AND_FILE]**:
   사용자 지정 연소 물질 모델이 존재하는 경우, 사용자 지정 연소 물질 모델을 사용할지 여부를 지정합니다.

-  **CANOPY_COV_UNIT=[PERCENT/CATEGORIES]**

-  **CANOPY_HT_UNIT=[METERS_X_10/FEET/METERS/FEET_X_10]**

-  **CBH_UNIT=[METERS_X_10/METERS/FEET/FEET_X_10]**

-  **CBD_UNIT=[KG_PER_CUBIC_METER_X_100/POUND_PER_CUBIC_FOOT/KG_PER_CUBIC_METER/POUND_PER_CUBIC_FOOT_X_1000/TONS_PER_ACRE_X_100]**

-  **DUFF_UNIT=[MG_PER_HECTARE_X_10/TONS_PER_ACRE_X_10]**

-  **CALCULATE_STATS=[YES/NO]**:
   헤더에 각 밴드의 최소/최대값을 계산해서 작성하고, 적당한 플래그와 값을 작성합니다. 이 옵션은 대부분의 경우 범례를 생성하기 위해 쓰이는 레거시 기능입니다.

-  **CLASSIFY_DATA=[YES/NO]**:
   헤더에 데이터를 유일값(unique value) 100개 이하로 범주화하고 작성한 다음, 적당한 플래그와 값을 작성합니다. 이 옵션은 대부분의 경우 범례를 생성하기 위해 쓰이는 레거시 기능입니다.

-  **LINEAR_UNIT=[SET_FROM_SRS/METER/FOOT/KILOMETER]**:
   관련 공간 좌표계의 값을 (계산할 수 있는 경우) 대체하는 선형 단위를 설정합니다. 사용할 수 있는 공간 좌표계가 없다면, 기본값은 METER입니다.

-  **LATITUDE=[-90-90]**:
   공간 좌표계의 위도를 대체합니다. 사용할 수 있는 공간 좌표계가 없는 경우 이 옵션을 설정해야 합니다. 그렇지 않으면 생성이 실패할 것입니다.

-  **DESCRIPTION=[...]**:
   데이터셋의 짧은 (512문자 미만) 설명입니다.

선형 측정 단위 관련 생성 옵션은 꽤 유연합니다. 대부분의 경우 METERS와 METER를 동일하게 받아들이고 FOOT과 FEET도 마찬가지입니다.

**주의**: CreateCopy() 메소드는 어떤 데이터도 크기 조정하거나 변경하지 않습니다. 밴드 여러 개에 단위를 설정하면, 모든 밴드의 값이 지정한 단위를 사용한다고 가정합니다.

LCP 헤더 서식
-----------------

============== ================ ========== ================ =================================================================================================================================================================================================
시작 바이트    바이트 개수      유형       이름             설명
============== ================ ========== ================ =================================================================================================================================================================================================
0              4                long       crown fuels      수관 연소 물질이 없다면 20, 수관 연소 물질이 있다면 21 (수관 연소 물질 = 수관 높이, 수관 기준(base) 높이, 수관 부피 밀도)
4              4                long       ground fuels     지표 연소 물질이 없다면 20, 지표 연소 물질이 있다면 21 (지표 연소 물질 = 분탄(duff) 하중, 조잡 목재)
8              4                long       latitude         위도 (남반구의 경우 음의 값)
12             8                double     loeast           좌표 정밀도를 보전하기 위한 오프셋 (16비트 OS 시절의 레거시)
20             8                double     hieast           좌표 정밀도를 보전하기 위한 오프셋 (16비트 OS 시절의 레거시)
28             8                double     lonorth          좌표 정밀도를 보전하기 위한 오프셋 (16비트 OS 시절의 레거시)
36             8                double     hinorth          좌표 정밀도를 보전하기 위한 오프셋 (16비트 OS 시절의 레거시)
44             4                long       loelev           최저 표고
48             4                long       hielev           최대 표고
52             4                long       numelev          표고 범주 개수, 100을 초과하는 경우 -1
56             400              long       elevation values LONG형 표고값 목록
456            4                long       loslope          최저 경사
460            4                long       hislope          최고 경사
464            4                long       numslope         경사 범주 개수, 100을 초과하는 경우 -1
468            400              long       slope values     LONG형 경사값 목록
868            4                long       loaspect         최소 경사 방향
872            4                long       hiaspect         최대 경사 방향
876            4                long       numaspects       경사 방향 범주 개수, 100을 초과하는 경우 -1
880            400              long       aspect values    LONG형 경사 방향 값 목록
1280           4                long       lofuel           최소 연소 물질 모델 값
1284           4                long       hifuel           최대 연소 물질 모델 값
1288           4                long       numfuel          연소 물질 모델 개수, 100을 초과하는 경우 -1
1292           400              long       fuel values      LONG형 연소 물질 모델 값 목록
1692           4                long       locover          최소 수관 차폐율
1696           4                long       hicover          최대 수관 차폐율
1700           4                long       numcover         수관 차폐율 범주 개수, 100을 초과하는 경우 -1
1704           400              long       cover values     LONG형 수관 차폐율 값 목록
2104           4                long       loheight         최소 수관 높이
2108           4                long       hiheight         최대 수관 높이
2112           4                long       numheight        수관 높이 범주 개수, 100을 초과하는 경우 -1
2116           400              long       height values    LONG형 수관 높이 값 목록
2516           4                long       lobase           최소 수관 기준 높이
2520           4                long       hibase           최대 수관 기준 높이
2524           4                long       numbase          수관 기준 높이 범주 개수, 100을 초과하는 경우 -1
2528           400              long       base values      LONG형 수관 기준 높이 값 목록
2928           4                long       lodensity        최소 수관 부피 밀도
2932           4                long       hidensity        최대 수관 부피 밀도
2936           4                long       numdensity       수관 부피 밀도 범주 개수, -1 if >100
2940           400              long       density values   LONG형 수관 부피 밀도 값 목록
3340           4                long       loduff           최소 분탄
3344           4                long       hiduff           최대 분탄
3348           4                long       numduff          분탄 범주 개수, 100을 초과하는 경우 -1
3352           400              long       duff values      LONG형 duff 값 목록
3752           4                long       lowoody          최소 조잡 목재
3756           4                long       hiwoody          최대 조잡 목재
3760           4                long       numwoodies       조잡 목재 범주 개수, 100을 초과하는 경우 -1
3764           400              long       woody values     LONG형 조잡 목재 값 목록
4164           4                long       numeast          래스터 열
4168           4                long       numnorth         래스터 행
4172           8                double     EastUtm          최대 X
4180           8                double     WestUtm          최소 X
4188           8                double     NorthUtm         최대 Y
4196           8                double     SouthUtm         최소 Y
4204           4                long       GridUnits        선형 단위: 0 = 미터, 1 = 피트, 2 = 킬로미터
4208           8                double     XResol           GridUnits 단위 셀 크기의 너비
4216           8                double     YResol           GridUnits 단위 셀 크기의 높이
4224           2                short      EUnits           표고 단위: 0 = 미터, 1 = 피트
4226           2                short      SUnits           경사 단위: 0 = 도, 1 = 백분율
4228           2                short      AUnits           경사 방향 단위: 0 = GRASS 카테고리, 1 = GRASS 도, 2 = 방위각 도
4230           2                short      FOptions         연소 물질 모델 옵션: 0 = 사용자 지정 모델과 변환 파일 둘 다 없음, 1 = 사용자 지정 모델은 있지만 변환 파일은 없음, 2 = 사용자 지정 모델은 없지만 변환 파일은 있음, 3 = 사용자 지정 모델과 변환 파일 둘 다 필요
4232           2                short      CUnits           수관 차폐율 단위: 0 = 카테고리(0-4), 1 = 백분율
4234           2                short      HUnits           수관 높이 단위: 1 = 미터, 2 = 피트, 3 = m x 10, 4 = 피트 x 10
4236           2                short      BUnits           수관 기준 높이 단위: 1 = 미터, 2 = 피트, 3 = m x 10, 4 = 피트 x 10
4238           2                short      PUnits           수관 부피 밀도 단위: 1 = kg/m^3, 2 = 파운드/ft^3, 3 = kg/m^3 x 100, 4 = 파운드/ft^3 x 1000
4240           2                short      DUnits           분탄 단위: 1 = 메가그램/헥타르 x 10, 2 = 톤/에이커 x 10
4242           2                short      WOptions         조잡 목재 옵션 (조잡 목재 밴드가 존재하는 경우 1)
4244           256              char[]     ElevFile         표고 파일명
4500           256              char[]     SlopeFile        경사 파일명
4756           256              char[]     AspectFile       경사 방향 파일명
5012           256              char[]     FuelFile         연소 물질 모델 파일명
5268           256              char[]     CoverFile        수관 차폐율 파일명
5524           256              char[]     HeightFile       수관 높이 파일명
5780           256              char[]     BaseFile         수관 기준 높이 파일명
6036           256              char[]     DensityFile      수관 부피 밀도 파일명
6292           256              char[]     DuffFile         분탄 파일명
6548           256              char[]     WoodyFile        조잡 목재 파일명
6804           512              char[]     Description      LCP 파일 설명
============== ================ ========== ================ =================================================================================================================================================================================================

*크리스 토니(Chris Toney), 2009년 2월 14일*
