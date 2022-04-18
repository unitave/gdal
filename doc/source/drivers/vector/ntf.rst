.. _vector.ntf:

영국 .NTF
=========

.. shortname:: UK .NTF

.. built_in_by_default::

영국 육지 측량부(UK Ordnance Survey)에서 주로 사용되는 NTF(National Transfer Format) 파일에 읽기 접근을 지원합니다.

이 드라이버는 디렉터리를 데이터셋으로 취급하고, (일반적으로 각 소스 파일별이 아니라) 각 객체 유형별로 레이어 하나씩을 생성해서 디렉터리 안에 있는 모든 .NTF 파일들을 병합하려 시도합니다. 따라서 Landline 파일을 여러 개 담고 있는 디렉터리의 경우, Landline 파일의 개수와 상관없이 레이어를 3개 (LANDLINE_POINT, LANDLINE_LINE 및 LANDLINE_NAME) 가지게 될 것입니다.

NTF 객체는 언제나 영국 국가 그리드(British National Grid) 좌표계로 반환됩니다. 영국 육지 측량부가 아닌 다른 조직이 NTF 파일을 작성하는 경우 이 좌표계가 어울리지 않을 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `영국 NTF 일반 정보 <https://web.archive.org/web/20130730111701/http://home.gdal.org/projects/ntf/index.html>`_

구현 노트
--------------------

지원 상품(및 레이어)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Landline (및 Landline Plus):

   -  LANDLINE_POINT
   -  LANDLINE_LINE
   -  LANDLINE_NAME

-  Panorama Contours:

   -  PANORAMA_POINT
   -  PANORAMA_CONTOUR

   HEIGHT 속성이 표고를 담고 있습니다.

-  Strategi:

   -  STRATEGI_POINT
   -  STRATEGI_LINE
   -  STRATEGI_TEXT
   -  STRATEGI_NODE

-  Meridian:

   -  MERIDIAN_POINT
   -  MERIDIAN_LINE
   -  MERIDIAN_TEXT
   -  MERIDIAN_NODE

-  Boundaryline:

   -  BOUNDARYLINE_LINK
   -  BOUNDARYLINE_POLY
   -  BOUNDARYLINE_COLLECTIONS

   _POLY 레이어는 진짜 폴리곤을 형성할 수 있게 해주는 "links to links"를 가지고 있습니다. (그렇지 않다면 _POLY 레이어는 도형 용 시드 포인트만 가집니다.)
   집합(collection)은 (읽어오는 동안 도형이 없는) 폴리곤 집합입니다. 이 상품으로부터만 폴리곤을 구성할 수 있습니다.

-  BaseData.GB:

   -  BASEDATA_POINT
   -  BASEDATA_LINE
   -  BASEDATA_TEXT
   -  BASEDATA_NODE

-  OSCAR Asset/Traffic:

   -  OSCAR_POINT
   -  OSCAR_LINE
   -  OSCAR_NODE

-  OSCAR Network:

   -  OSCAR_NETWORK_POINT
   -  OSCAR_NETWORK_LINE
   -  OSCAR_NETWORK_NODE

-  Address Point:

   -  ADDRESS_POINT

-  Code Point:

   -  CODE_POINT

-  Code Point Plus:

   -  CODE_POINT_PLUS

전체 데이터셋도 FEAT_CODE 숫자를 객체 클래스 이름(FC_NAME)과 관계 맺어주는 순수 테이블을 담고 있는 FEATURE_CLASSES 레이어를 가질 것입니다. 이는 데이터셋에 있는 모든 상품에 적용됩니다. 몇몇 (Code Point 및 Address Point 같은) 레이어 유형은 객체 클래스를 포함하지 않습니다. 어떤 상품들은 파일에 정의되어 있지 않은 객체 클래스를 사용하기 때문에, FEATURE_CLASSES 레이어에 그런 객체 클래스들은 나타나지 않을 것입니다.

상품 스키마
~~~~~~~~~~~~~~~

이 판독기는 파일 하나, 또는 파일들을 담은 디렉터리 하나를 단일 데이터셋 하나로 취급하는 접근법을 사용합니다. 데이터셋을 열 때 데이터셋 안에 있는 모든 파일을 스캔합니다. (앞 목록의) 각 특정 상품별로 레이어 집합을 생성하지만, 동일 상품의 파일 여러 개로부터 이런 레이어들을 추출할 수도 있습니다.

이 레이어들은 NTF 파일의 저수준 객체 유형을 기반으로 하지만, 일반적으로 서로 다른 많은 객체 코드(FEAT_CODE 속성)를 담을 것입니다. 해당 레이어 안에 있는 서로 다른 객체들은 파일 안에 다양한 속성들을 가질 수도 있습니다. 하지만 해당 상품군(예: OSCAR Network)의 특정 유형(예: POINT) 객체 내에 있을 수 있는 모든 속성을 통합한 것을 기반으로 스키마를 확립합니다.

알려진 스키마들 가운데 하나와 일치하지 않는 NTF 상품을 읽어오는 경우, GENERIC_POINT 및 GENERIC_LINE 유형의 레이어만 가지고 있는 다른 일반 처리기(handler)를 통해 읽어올 것입니다. 이때 객체는 FEAT_CODE 속성만 가집니다.

ntf_estlayers.cpp 모듈의 마지막에 있는 NTFFileReader::EstablishLayers() 메소드로 어떤 상품의 어떤 레이어가 어떤 속성을 가지고 있는지에 관한 상세 정보를 찾아볼 수 있습니다. 이 파일은 모든 상품의 특화 변환 코드도 담고 있습니다.

특수 속성
~~~~~~~~~~~~~~~~~~

-  FEAT_CODE:
   정수형 일반 객체 코드로, FEATURE_CLASSES 레이어/테이블에서 이름을 검색하는 데 사용할 수 있습니다.

-  TEXT_ID/POINT_ID/LINE_ID/NAME_ID/COLL_ID/POLY_ID/GEOM_ID:
   각각 알맞은 유형의 객체 용 유일 식별자입니다.

-  TILE_REF:
   (FEATURE_CLASSES를 제외한) 모든 레이어가 해당 객체가 나온 파일(타일)을 가리키는 TILE_REF 속성을 담고 있습니다. 대체로 ID 번호는 타일 내부에서만 유일한 값이기 때문에, TILE_REF를 사용해서 동일 파일로부터 나온 객체들  안에서의 ID 링크를 제약할 수 있습니다.

-  FONT/TEXT_HT/DIG_POSTN/ORIENT:
   글꼴, 텍스트 높이, 디지타이즈 작업 위치, 그리고 텍스트 또는 이름 객체의 방향에 관한 상세 정보입니다. 단위 및 이 코드들의 의미를 이해하려면 운영 체제별 상품 지침서를 읽어보십시오.

-  GEOM_ID_OF_POINT:
   _NODE 객체의 경우 이 속성이 해당 노드와 대응하는 포인트 레이어 객체의 POINT_ID를 정의합니다. 대체로 노드는 스스로 도형을 담고 있지 않습니다. 노드의 위치를 확립하려면 노드가 포인트와 관계를 맺고 있어야만 합니다.

-  GEOM_ID_OF_LINK:
   어떤 노드에서 끝나거나 시작하는 _LINK 또는 _LINE 객체의 목록입니다. 네트워크 분석을 위해 라인 객체들의 연결성을 확립하는 경우 일반적으로 노드와 이 속성 필드의 값만 사용합니다. 이 속성이 대상 객체의 LINE_ID가 아니라 GEOM_ID와 관계를 맺고 있어야만 한다는 사실을 기억하십시오.

   BOUNDARYLINE_POLY 레이어에서는 이 속성이 폴리곤의 경계를 형성하는 라인들의 GEOM_ID를 담고 있습니다.

-  POLY_ID:
   BOUNDARYLINE_COLLECTIONS 레이어에서 지정된 집합과 관련된 BOUNDARYLINE_POLY 레이어로부터 나온 POLY_ID의 목록입니다.

일반 상품
~~~~~~~~~~~~~~~~

기존에 알려진 상품의 일부로서 식별되지 않는 파일이 존재하는 경우, 일반 상품(generic product)으로 취급할 것입니다. 이 경우 데이터셋 전체를 스캔해서 어떤 객체가 어떤 속성을 가지고 있는지 확인합니다. 이 때문에 일반 데이터셋을 여는 작업은 식별된 데이터셋을 여는 작업보다 훨씬 느릴 수 있습니다. 이 스캔 작업을 기반으로 다음 객체 목록으로부터 일반 객체(레이어) 목록을 정의합니다:

-  GENERIC_POINT
-  GENERIC_LINE
-  GENERIC_NAME
-  GENERIC_TEXT
-  GENERIC_POLY
-  GENERIC_NODE
-  GENERIC_COLLECTION

ntf_generic.cpp 모듈이 일반 상품을 우선적으로 처리하는 반면 ntf_estlayers.cpp 모듈은 특정 상품을 처리합니다.

육지 측량부의 상품이 아닌 일부 (OSNI 데이터셋) 데이터 상품이 영국 육지 측량부의 일반적인 순서를 따르지 않는 레코드 그룹을 가지고 있기 때문에, 3수준 이상의 일반 상품의 경우 편의적인 레코드 순서에 의존하기보다 일반 상품이 가지고 있는 모든 레코드를 캐시로 불러와서 캐시 안에서 ID 참조로 레코드 그룹을 구성해야 합니다. ntffilereader.cpp 모듈의 마지막 가까이에 있는 NTFFileReader의 "색인 작업" 기능으로 이를 달성할 수 있습니다. 이 때문에 일반 데이터셋에 접근하는 인메모리 색인 작업은 알려진 데이터 상품에 접근하는 것보다 메모리를 훨씬 더 많이 사용할 수 있지만, 1수준 및 2수준 일반 상품의 경우 인메모리 색인 작업이 필요없습니다.

ntfdump.cpp 모듈에서 선보인 대로, OGRNTFDataSource::SetOptionsList() 메소드를 이용해서 FORCE_GENERIC 옵션을 ON으로 설정하면 알려진 상품을 강제로 일반 상품으로 취급하게 할 수 있습니다.
OGR_NTF_OPTIONS 환경 변수를 "FORCE_GENERIC=ON"으로 설정해서 OGR 응용 프로그램 외부에서도 이를 달성할 수 있습니다.

