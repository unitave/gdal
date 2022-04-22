.. _vector.tiger:

미국 인구 조사국 TIGER/Line
===========================

.. shortname:: TIGER

.. built_in_by_default::

TIGER 드라이버는 TIGER/Line 파일 세트에 읽기 접근을 지원합니다.

TIGER/Line 파일은 미국 전역을 커버하는 도로, 철도, 하천, 호수, 행정 구역, 인구 조사 통계 구역 등등 같은 지리 객체의 디지털 데이터베이스입니다. 이 데이터베이스는 이런 객체들의 위도/경도 위치, 이름, 유형, 도로 대부분에 대한 주소 범위, 다른 객체와의 지리적 관계성, 그리고 기타 관련 정보를 담고 있습니다. TIGER/Line 파일은 미국 인구 조사국의 TIGER(Topologically Integrated Geographic Encoding and Referencing) 지리 정보 데이터베이스로부터 생성된 공공 제품입니다. 미국 인구 조사국이 10년 단위 인구 조사 및 표본 설문조사 프로그램에 필요한 매핑 및 관련 지리 활동을 지원하기 위해 TIGER를 개발했습니다.

TIGER/Line 제품이 인구 조사 통계를 포함하지 않는다는 사실을 기억하십시오. 인구 통계는 미국 인구 조사국이 (FME(Feature Manipulation Engine)가 직접 지원하지 않는) 개별 포맷으로 판매하고 있는데, 해당 통계는 TIGER/Line 파일에 있는 인구 조사 블록과 다시 연결됩니다.

TIGER/Line 데이터셋을 열려면, 데이터 파일 세트를 하나 이상 담고 있는 디렉터리를 선택하십시오. 지역(region)은 군(county) 또는 그에 상응하는 단위입니다. 각 군은 공통 기본명을 가졌지만 확장자가 다른 일련의 파일로 이루어져 있습니다. 예를 들어 26번 주(state; 미시건)에 있는 1번 군은 Tiger98에서 다음과 같은 파일 세트로 이루어져 있습니다:

::

   TGR26001.RT1
   TGR26001.RT2
   TGR26001.RT3
   TGR26001.RT4
   TGR26001.RT5
   TGR26001.RT6
   TGR26001.RT7
   TGR26001.RT8
   TGR26001.RT9
   TGR26001.RTA
   TGR26001.RTC
   TGR26001.RTH
   TGR26001.RTI
   TGR26001.RTP
   TGR26001.RTR
   TGR26001.RTS
   TGR26001.RTZ

TIGER/Line 좌표계는 NAD83 위도/경도 도(degree)로 하드코딩되어 있습니다. 최근 몇 년 동안의 모든 TIGER/Line 제품에 이 좌표계가 적절할 것입니다.

TIGER 드라이버는 업데이트 또는 생성을 지원하지 않습니다.

TIGER/Line 판독기는 TIGER/Line 1998 파일에 대해 구현되었지만, 1992, 1995, 1997, 1999, 2000, 2002, 2003 및 2004년 TIGER/Line 제품도 호환되도록 약간의 노력을 기울였습니다. 2005년 제품도 잘 작동한다고 보고되었습니다. 이 판독기가 1990년대부터의 모든 TIGER/Line 제품을 읽을 수 있다고 믿어지지만, 일부 버전 특화 정보를 잃을 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

객체 표현
----------------------

몇몇 예외를 제외하면, TIGER/Line 데이터 파일의 각 레코드 당 객체 하나를 생성합니다. 각 (예: .RT1, .RTA) 파일은 TIGER/Line 제품 지침서에 있는 속성명과 일치하는 속성명을 가진 알맞은 OGR 객체 유형으로 변환됩니다.

TIGER/Line RT(Record Type) 및 VERSION 속성은 일반적으로 폐기하지만, MODULE 속성은 각 객체에 추가합니다. MODULE 속성은 객체가 생성된 군(county) 모듈의 기반명을 (예: TGR26001) 담고 있습니다. 데이터셋(디렉터리)이 하나 이상의 데이터 군(county)으로 이루어진 경우 이 MODULE 속성이 (LAND, POLYID, 그리고 CENID 같은) 몇몇 키를 유일 키로 만들어야 합니다.

다음 단락부터 객체 유형 및 해당 객체 유형의 TIGER/Line 제품과의 관계를 설명합니다.

CompleteChain
^^^^^^^^^^^^^

CompleteChain은 관련 TLID(TIGER/Line ID)를 가진 폴리라인입니다. CompleteChain 객체는 1번 유형 레코드(Complete Chain Basic Data Record)로부터 확립되는데, 사용할 수 있는 경우 3번 유형 레코드(Complete Chain Geographic Entity Codes)와 연결됩니다. 또, 사용할 수 있는 모든 2번 유형 레코드(Complete Chain Shape Coordinates)를 사용해서 원호 상에 중간 도형(intermediate shape) 포인트를 채웁니다. TLID는 기본 키이며, 전국 TIGER/Line 커버리지 안에서 유일합니다.

이 객체는 항상 라인 도형을 가집니다.

AltName
^^^^^^^
이 객체는 4번 유형 레코드(Index to Alternate Feature Identifiers)로부터 파생되며, FeatureIds 객체로 개별적으로 보관되는 1개에서 4개까지의 대체 객체 이름 번호(FEAT 속성)와 연결됩니다. 표준 판독기 파이프라인은 FeatureIds 객체에서 나온 이름을 ALT_FEDIRS{}, ALT_FEDIRP{}, ALT_FENAME{} 및 ALT_FETYPE{} 배열 속성에 추가합니다. ALT_FENAME{}은 AltName 객체 상에서 TLID와 관련된 객체 이름들의 목록입니다.

어떤 TLID의 경우 AltName 레코드가 0개, 1개 또는 그 이상 존재할 수도 있으며 각 AltName 레코드는 1개에서 4개까지의 대체 이름을 담을 수 있다는 사실을 기억하십시오. AltName 객체를 활용해서 대체 이름을 CompleteChains와 연결하는 것은 여전히 매우 어렵기 때문에, 향후 TIGER/Line 파일용 표준 판독기 파이프라인이 업그레이드되어 대체 이름을 단순화시킬 것이라고 예상하고 있습니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

FeatureIds
^^^^^^^^^^

이 객체는 5번 유형 레코드(Complete Chain Feature Identifiers)로부터 파생됩니다. 각 객체는 객체 이름(FENAME)을 담고 있으며 객체 ID 코드(FEAT)와 연결됩니다. FEAT 속성은 기본 키이며, 군 모듈 안에서 유일합니다. FeatureIds는 AltName 및 KeyFeatures 객체들과 일대다 관계입니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

ZipCodes
^^^^^^^^

이 객체는 6번 유형 레코드(Additional Address Range and ZIP Code Data)로부터 파생됩니다. 이 객체의 목적은 CompleteChain 객체 상에 직접 보관된 우편번호 정보를 보완하는 것으로, ZipCodes 객체와 CompleteChain 객체는 다대일 관계입니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

Landmarks
^^^^^^^^^

이 객체는 7번 유형 레코드(Landmark Features)로부터 파생됩니다. 이 객체는 포인트 또는 영역 랜드마크와 연결됩니다. 영역 랜드마크의 경우 AreaLandmark 레코드와 일대일 관계입니다. LAND 속성은 기본 키이며, 군 모듈 안에서 유일합니다.

이 객체와 연결된 포인트 도형이 있을 수도 있습니다. 폴리곤과 연결된 랜드마크에는 폴리곤 도형을 추가하지 않을 것입니다. 폴리곤 도형을 추가하려면 (AreaLandmark 객체를 통해) Polygon 객체로부터 수집해야 할 것입니다.

AreaLandmarks
^^^^^^^^^^^^^

이 객체는 8번 유형 레코드(Polygons Linked to Area Landmarks)로부터 파생됩니다. 각 객체가 Polygon 객체(POLYID 속성)을 가진 Landmarks 객체(LAND 속성)와 연결됩니다. 이 객체는 Polygon 객체와 다대다 관계입니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

KeyFeatures
^^^^^^^^^^^

이 객체는 9번 유형 레코드(Key Geographic Location Features)로부터 파생됩니다. 이 객체는 (FEAT 속성을 통해) FeatureIds 객체와 그리고 (POLYID 속성을 통해) Polygon 객체와 연결될 수도 있습니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

Polygon
^^^^^^^

이 객체는 A 유형 레코드(Polygon Geographic Entity Codes) 및 사용할 수 있는 경우 S 유형 레코드(Polygon Additional
Geographic Entity Codes)로부터 파생됩니다. POLYID 속성은 기본 키이며, 군 모듈 안에서 폴리곤을 유일하게 식별합니다.

OGR TIGER 드라이버가 읽어오는 대로 이 객체는 관련 도형을 가지고 있지 않습니다. PolyChainLink를 이용해서 외부적으로 연결해야 합니다. gdal.py, pymod.py, samples.py, tigerpoly.py 스크립트를 이용해서 TIGER 데이터셋을 읽어와 **도형을 가진** 폴리곤 레이어를 shapefile로 추출할 수도 있습니다.

EntityNames
^^^^^^^^^^^
이 객체는 C 유형 레코드(Geographic Entity Names)로부터 파생됩니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

IDHistory
^^^^^^^^^

이 객체는 H 유형 레코드(TIGER/Line ID History)로부터 파생됩니다. 이 객체를 이용해서 CompleteChain 객체의 분할, 병합, 생성 및 삭제 작업 이력을 추적할 수 있습니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

PolyChainLink
^^^^^^^^^^^^^

이 객체는 I 유형 레코드(Link Between Complete Chains and Polygons)로부터 파생됩니다. CompleteChain의 폴리곤 도형을 확립하기 위해 Polygon 객체에 CompleteChain 도형을 추가하는 동안 표준 판독기 파이프라인이 이 객체를 사용합니다. PolyChainLink 객체와 Polygon 객체는 다대일 관계이며, PolyChainLink 객체와 CompleteChain 객체는 일대일 관계입니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

PIP
^^^

이 객체는 P 유형 레코드(Polygon Internal Point)로부터 파생됩니다. 이 객체는 POLYID 속성을 통해 Polygon 객체와 연결되며, Polygon 객체에 대한 내부 포인트를 확립하는 데 사용할 수 있습니다.

이 객체는 포인트 도형을 가집니다.

ZipPlus4
^^^^^^^^

이 객체는 Z 유형 레코드(ZIP+4 Codes)로부터 파생됩니다. ZipPlus4 객체는 CompleteChain 객체와 다대일 관계입니다.

이 객체는 관련 도형을 가지고 있지 않습니다.

참고
--------

-  `TIGER 데이터 상품 가이드 <https://www.census.gov/programs-surveys/geography/guidance/tiger-data-products-guide.html>`_:
   이 미국 인구 조사국 웹페이지에서 TIGER/Line 파일 포맷과 데이터 상품에 관한 자세한 정보를 찾아볼 수 있습니다.

- `2000년 TIGER/Line 파일 기술 문서 <https://www2.census.gov/geo/tiger/tigerua/ua2ktgr.pdf>`_

