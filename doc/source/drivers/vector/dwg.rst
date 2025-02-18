.. _vector.dwg:

오토캐드 DWG
===========

.. shortname:: DWG

.. build_dependencies:: 오픈 디자인 얼라이언스 Teigha 라이브러리

OGR는 오픈 디자인 얼라이언스 Teigha 라이브러리와 함께 빌드된 경우 오토캐드(AutoCAD) DWG 포맷의 거의 모든 버전의 읽기를 지원합니다. DWG는 오토캐드 도면 용으로 사용되는 바이터리 작업 포맷입니다. ORG DWG 드라이버가 공통 데이터 모델을 공유하는 OGR DXF 드라이버와 비슷하게 작동하도록 하기 위해 적정한 시간과 노력을 들였습니다. .dwg 파일의 전체 내용은 "entities" 라는 이름의 단일 레이어로 표현됩니다.

DWG 파일은 OGR를 통한 지리참조 정보를 가지고 있지 않다고 간주됩니다. 모든 객체는 다음과 같은 일반 속성들을 가질 것입니다:

-  Layer: DXF 레이어의 이름입니다. 기본 레이어는 "0"입니다.

-  SubClasses: 사용 가능한 경우, 요소가 속해 있는 클래스들의 목록입니다.

-  ExtendedEntity: 사용 가능한 경우, 단일 텍스트 속성을 형성하도록 모든 확장 요소 속성을 추가합니다.

-  Linetype: 사용 가능한 경우, 이 요소에 사용된 라인 유형입니다.

-  EntityHandle: 16진법 요소 핸들(entity handle)입니다. 일종의 FID(Feature ID)입니다.

-  Text: 라벨의 텍스트입니다.

요소 변환 시 OGR 객체 스타일 작업 정보를 통해 라인 색상, 라인 굵기, 텍스트 크기 및 방향을 보전하려 적정하게 시도합니다. 현재 채우기 스타일 또는 복잡 라인 스타일 속성을 보전하려는 어떤 노력도 하지 않습니다.

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`OGR_ARC_STEPSIZE`:
   원호를 한계 각도를 넘지 않는 하위 원호들로 분할해서 원호(arc), 타원, 원 및 둥글림된(rounded) 폴리라인의 라인스트링 근사치를 생성합니다. OGR_ARC_STEPSIZE 환경설정 옵션으로 한계 각도를 설정합니다. 기본값은 4도이지만, 이 옵션을 설정해서 대체할 수 있습니다.

-  :decl_configoption:`DWG_INLINE_BLOCKS`:
   블록 참조의 기본 습성은 블록 참조가 참조하는 블록의 도형으로 확장되는 것입니다. 하지만, DWG_INLINE_BLOCKS 환경설정 옵션의 값을 FALSE로 설정하는 경우 습성이 다음과 같이 달라집니다.

   -  "blocks"라 불리는 새 레이어를 사용할 수 있습니다. 이 레이어는 파일에 정의된 블록 당 하나 이상의 객체를 담을 것입니다. 이 객체들은 일반적인 속성뿐만 아니라 객체가 속해 있는 블록을 나타내는 BlockName 속성도 가지게 됩니다.

   -  "entities" 레이어가 새로운 BlockName, BlockScale, BlockAngle 및 BlockAttributes 속성을 가지게 됩니다.

   -  BlockAttributes 속성은 모든 가시(visible) 속성의 (JSON 인코딩된) 태그x값 목록이 될 것입니다.

   -  참조된 블록이 이 새 필드들을 대응하는 정보로 채울 것입니다. (다른 모든 요소들의 경우 새 필드가 NULL입니다.)

   -  블록 참조는 블록 도형을 그때 그때 즉시 처리하지 않을 것입니다 -- 대신 삽입 포인트를 위한 포인트 도형을 가질 것입니다.

   DWG_INLINE_BLOCKS 환경설정 옵션의 목적은, FALSE로 설정하는 경우 블록 참조가 참조로만 남고 "blocks" 레이어를 통해 원본 블록 정보를 사용할 수 있게 된다는 점입니다.

-  :decl_configoption:`DWG_ATTRIBUTES`:
   이 옵션을 TRUE로 설정하는 경우, 블록 속성을 태그 하나 당 객체 속성 하나인 객체 속성으로 취급합니다. 이 옵션을 사용하면 블록 속성을 데이터베이스 테이블 같은 행 및 열 데이터로 변환할 수 있습니다.

-  :decl_configoption:`DWG_ALL_ATTRIBUTES`:
   이 옵션을 FALSE로 설정하면, 태그 속성의 가시 속성이 거짓인 경우 블록 속성을 무시합니다. 모든 속성들을 가시화하려면 DWG_ALL_ATTRIBUTES를 (기본값) TRUE로 설정하십시오.

빌드 작업
--------

GDAL을 ODA 지원과 함께 빌드하려면 :ref:`ODA 플랫폼 지원 <vector.oda>` 을 참조하십시오.

