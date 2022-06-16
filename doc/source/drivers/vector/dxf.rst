.. _vector.dxf:

오토캐드 DXF
===========

.. shortname:: DXF

.. built_in_by_default::

DXF 포맷은 서로 다른 소프트웨어 패키지 사이에 오토캐드(AutoCAD) 도면 정보를 교환하기 위해 싸용되는 아스키 포맷입니다. OGR는 오토캐드의 최근 모든 버전이 생성한 DXF 파일 읽기 및 AutoCAD 2004 및 이후 버전들과 호환되는 DXF 파일 쓰기를 지원합니다.

DXF 파일은 OGR를 통한 지리참조 정보를 가지고 있지 않다고 간주됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_virtualio::

DXF 판독기
----------

기본적으로, DXF 파일의 전체 내용은 "entities" 라는 이름의 단일 OGR 레이어로 표현됩니다. 모든 객체는 다음과 같은 일반 필드들을 가질 것입니다:

-  Layer: DXF 레이어의 이름입니다. 기본 레이어는 "0"입니다.

-  PaperSpace: 요소가 레이아웃(페이퍼 스페이스) 상에 위치하는 경우 1, 그렇지 않다면 NULL입니다.

-  SubClasses: 사용 가능한 경우, 요소가 속해 있는 클래스들의 목록입니다.

-  ExtendedEntity (GDAL 2.2.x 이하 버전): 사용 가능한 경우, 단일 텍스트 필드를 형성하도록 모든 확장 요소 속성을 추가합니다.

-  RawCodeValues (GDAL 2.3.0 이상 버전): :decl_configoption:`DXF_INCLUDE_RAW_CODE_VALUES` 환경설정 옵션을 TRUE로 설정한 경우에만 사용할 수 있습니다. DXF 판독기가 처리하지 않는 모든 그룹 코드 및 값들을 담고 있는 문자열 목록입니다.

-  Linetype: 사용 가능한 경우, 이 요소에 사용된 라인 유형입니다.

-  EntityHandle: 16진법 요소 핸들(entity handle)입니다. 일종의 FID(Feature ID)입니다.

-  Text: 라벨의 텍스트입니다.

지원 요소
~~~~~~~~~~~~~~~~~~

다음과 같은 요소 유형들을 지원합니다:

-  POINT: 단순 POINT 도형 객체를 생성합니다.

-  MTEXT, TEXT: LABEL 스타일 정보를 가지고 있는 POINT 객체를 생성합니다. 이 스타일 문자열은 f, s, t, a, c, w, p, dx, dy, bo, it 파라미터를 포함할 수도 있습니다. 텍스트 배치가 (특히 MTEXT의 수직 정렬의 경우) CAD 소프트웨어와 정확하게 일치하지 않을 수도 있습니다. 정확한 위치를 계산하려면 GDAL이 글꼴 메트릭스(font metrics)를 인식할 수 있어야 하기 때문입니다. 기본적으로, 적용할 수 있는 경우 %%p 같은 문자 이스케이프를 존중하고, \\Wx.xx; 같은 MTEXT 제어 시퀀스를 제거합니다. 이런 습성을 비활성화시키고 원시(raw) 텍스트 값을 가져오고 싶다면, :decl_configoption:`DXF_TRANSLATE_ESCAPE_SEQUENCES` 환경설정 옵션을 FALSE로 설정하십시오.

-  LINE, POLYLINE, LWPOLYLINE: LINESTRING으로 변환합니다. (꼭짓점의 벗지(budge) 속성이 설정된) 둥글림된(rounded) 폴리라인은 모자이크화(tessellated)합니다. 단일 꼭짓점 폴리라인은 POINT로 변환합니다. 폴리페이스 메시(polyface mesh)는 POLYHEDRALSURFACE 도형으로 변환합니다.

-  MLINE:

   -  (GDAL 2.3.0 이상 버전) MULTILINESTRING으로 변환합니다. 도형만 재구성하고 MLINE 안에 있는 개별 라인 요소에 적용된 스타일은 무시합니다. 채우기 색상 및 라인의 시작/종단 끝(cap)도 생략합니다.
   -  (GDAL 2.2.x 이하 버전) 지원하지 않습니다.

-  CIRCLE, ELLIPSE, ARC, SPLINE, (GDAL 2.3.0 이상 버전) HELIX: LINESTRING으로 변환하고, 곡선을 라인 선분으로 모자이크화합니다.
   (GDAL 2.3.0 이상 버전) 0이 아닌 "두께"를 가진 CIRCLE(원기둥)은 POLYHEDRALSURFACE의 근사치로 변환합니다.

-  INSERT: INSERT가 참조하는 블록 참조는 기본적으로 (예를 들면 블록에서 수많은 라인을 담고 있는 MULTILINESTRING, 또는 블록에서 포인트와 라인을 담고 있는 GEOMETRYCOLLECTION 같은) 복합 도형으로 삽입될 것입니다. 블록이 TEXT 또는 MTEXT 요소를 담고 있는 경우, 복합 도형으로 병합하지 않고 대신 개별 객체로 반환됩니다.

   INSERT 요소의 습성을 제어하기 위해 다음 3개의 환경설정 옵션을 사용할 수 있습니다:

   -  :decl_configoption:`DXF_MERGE_BLOCK_GEOMETRIES`:
      블록들을 복합 도형으로 병합시키지 않으려면 DXF_MERGE_BLOCK_GEOMETRIES 환경설정 옵션을 FALSE로 설정하면 됩니다. 블록 안에 있는 개별 선화(線畵, linework) 요소의 (색상 같은) 스타일을 보전해야 하는 경우 이 옵션을 사용하십시오.
   -  :decl_configoption:`DXF_INLINE_BLOCKS`: 아래 "DXF_INLINE_BLOCKS" 단락을 참조하십시오.
   -  (GDAL 2.3.0 이상 버전) :decl_configoption:`DXF_FEATURE_LIMIT_PER_BLOCK`:
      단일 블록으로부터 삽입되는 객체의 최대 개수를 설정합니다. -1로 설정하면 무제한으로 삽입할 수 있습니다. 기본값은 10,000입니다.

-  ATTDEF, ATTRIB:

   -  (GDAL 2.3.0 이상 버전) 속성(ATTRIB)을 TEXT 요소로 취급하고, 블록 안에 있는 속성 정의(ATTDEF)는 무시합니다. DXF_INLINE_BLOCKS 옵션을 거짓으로 설정한 경우 이 습성이 달라집니다. (아래 단락 참조)
   -  (GDAL 2.2.x 이하 버전) ATTDEF 요소를 TEXT 요소로 취급합니다. ATTRIB 요소는 지원하지 않습니다.

-  HATCH: 라인 및 원호 경계선을 폴리곤 도형으로 수집하지만, 현재 HATCH 요소의 채우기 스타일을 표현하기 위한 어떤 노력도 하지 않고 있습니다.

   -  (GDAL 2.3.0 이상 버전) 해치 경계선에 추가할 다음 구성요소를 검색하는 경우 :decl_configoption:`DXF_HATCH_TOLERANCE` 환경설정 옵션이 허용 오차를 결정합니다.
   -  (GDAL 2.2.x 이하 버전) 라인 및 폴리라인 경계선 경로만 정확하게 변환됩니다.

-  3DFACE, SOLID, (GDAL 2.3.0 이상 버전) TRACE: POLYGON으로 변환합니다. 예외: 분명한 꼭짓점을 하나만 가지고 있는 SOLID 및 TRACE 요소는 POINT로, 또는 분명한 꼭짓점을 두 개만 가지고 있는 SOLID 및 TRACE 요소는 LINESTRING으로 변환합니다.

-  DIMENSION:

   -  (GDAL 2.3.0 이상 버전) DXF 포맷은 각 DIMENSION 요소가 DIMENSION의 도형을 담고 있는 (블록 이름이 \*D로 시작하는) "익명(anonymous)" 블록을 참조할 수 있도록 허용합니다. 익명 블록이 존재하는 경우, 요구 위치에서 이 익명 블록을 그때 그때 즉시 처리할 것입니다. 존재하지 않는다면, 선형 차원을 MULTILINESTRING 객체로 폭발(explode)시키는 단순 DIMENSION 렌더링 작업자(renderer)로 돌아갈 것입니다. 화살표가 존재하는 경우, 하나 또는 그 이상의 추가 객체로 변환합니다. 단순 DIMENSION 렌더링 작업자는 비선형 차원을 선형 차원인 것처럼 렌더링할 것입니다.
   -  (GDAL 2.2.x 이하 버전) 차원을 MULTILINESTRING으로, 텍스트의 경우 POINT로 변환합니다.

-  LEADER, MULTILEADER:

   -  (GDAL 2.3.0 이상 버전) 리더(leader) 라인을 LINESTRING(LEADER) 또는 MULTILINESTRING(MULTILEADER)으로 변환합니다. 화살표가 존재하는 경우, 하나 또는 그 이상의 추가 객체로 변환합니다. MULTILEADER 요소의 텍스트는 라벨을 가진 POINT 객체로 변환합니다. MULTILEADER의 블록 콘텐츠는 INSERT 경우처럼 취급됩니다. 스플라인 리더 라인은 라인 선분으로 모자이크화됩니다.
   -  (GDAL 2.2.x 이하 버전) 지원하지 않습니다.

-  3DSOLID, REGION, BODY, SURFACE: 아래 "3차원 확장성" 단락을 참조하십시오.

요소 변환 시 OGR 객체 스타일 작업 정보를 통해 색상, 라인 굵기(라인 가중치), 라인 유형, 텍스트 크기 및 방향을 보전하려 적정하게 시도합니다. 현재 (텍스트 또는 도형을 포함하는) 복잡 라인 유형 또는 HATCH 채우기 스타일을 보전하려는 어떤 노력도 하지 않습니다.

원호를 한계 각도를 넘지 않는 하위 원호들로 분할해서 원호(arc), 타원, 원 및 둥글림된(rounded) 폴리라인의 라인스트링 근사치를 생성합니다. :decl_configoption:`OGR_ARC_STEPSIZE` 환경설정 옵션으로 한계 각도를 설정합니다. 이 옵션의 기본값은 4도입니다. :decl_configoption:`OGR_ARC_MAX_GAP` 환경설정 옵션을 설정하면 보간된 곡선 상에 있는 인접 포인트들 사이의 최대 거리를 강제할 수도 있습니다. 이 옵션을 (기본값) 0으로 설정하면 최대 거리를 적용하지 않습니다.

스플라인의 경우, 보간된 폴리라인이 각 제어 포인트에 꼭짓점 8개를 담고 있습니다.

DIMENSION, LEADER 그리고 MULTILEADER를 제외한 모든 요소에 대해 DXF 사양 별로 각각 적용되는 "extrusions"라고도 알려진 객체 좌표계(Object Coordinate System; OCS)를 지원합니다. 이 요소 유형 3개는 현재 표고도 지원하지 않습니다. 이 요소들의 도형은 항상 2차원일 것입니다.

DXF_INLINE_BLOCKS
~~~~~~~~~~~~~~~~~

INSERT 요소의 기본 습성은 INSERT 요소를 자신이 참조하는 BLOCK의 도형으로 폭발시키는 것입니다. 하지만, :decl_configoption:`DXF_INLINE_BLOCKS` 환경설정 옵션의 값을 FALSE로 설정하는 경우 습성이 다음과 같이 달라집니다.

-  "blocks"라 불리는 새 레이어를 사용할 수 있습니다. 이 레이어는 파일에 정의된 BLOCK 당 하나 이상의 객체를 담을 것입니다. 이 객체들은 일반적인 필드뿐만 아니라 객체가 속해 있는 블록을 나타내는 Block 속성도 가지게 됩니다. (GDAL 2.2.x 이전 버전에서는 이 필드의 이름이 BlockName이었습니다.)

-  (GDAL 2.3.0 이상 버전) blocks 레이어의 ATTDEF 요소가 ATTDEF 요소의 태그를 지정하는 AttributeTag 필드를 가질 것입니다.

-  entities 레이어가 새 필드 몇 개를 가지게 됩니다:

   -  BlockName: 참조된 블록의 이름입니다.

   -  BlockScale: X, Y 및 Z 척도 인자입니다.

   -  BlockAngle: 블록의 도 단위 각도입니다.

   -  BlockOCSNormal (GDAL 2.3.0 이상 버전): INSERT 요소의 객체 좌표계의 단위 정규 벡터입니다.

   -  BlockOCSCoords (GDAL 2.3.0 이상 버전): 삽입 포인트의 객체 좌표입니다.

   -  BlockAttributes (GDAL 2.3.0 이상 버전): 이 블록과 관련된 속성의 텍스트 내용입니다. 이 문자열 목록에 있는 각 항목은 순서대로 속성 태그, 공백, 해당 속성의 (비어 있을 수도 있는) 텍스트를 담고 있습니다.

-  INSERT 요소가 이 새 필드들을 대응하는 정보로 채울 것입니다. (다른 모든 요소들의 경우 새 필드가 NULL입니다.)

-  INSERT 블록 도형을 그때 그때 즉시 처리하지 않을 것입니다 -- 대신 삽입 포인트를 위한 POINT 도형을 가질 것입니다.

DXF_INLINE_BLOCKS 환경설정 옵션의 목적은, FALSE로 설정하는 경우 블록 참조가 참조로만 남고 "blocks" 레이어를 통해 원본 블록 정보를 사용할 수 있게 된다는 점입니다. 내보내기 작업 시 이 환경설정 옵션을 사용하면 비슷한 블록들을 생성하게 될 것입니다.

3차원 확장성
~~~~~~~~~~~~~~~~

DXF 파일은 광범위하게 호환되는 ACIS 포맷의 포크(fork)인 상용 ASM(Autodesk ShapeManager) 포맷으로 된 3차원 모델링 데이터를 담고 있는 3DSOLID, REGION, BODY 및 SURFACE 요소들을 담을 수도 있습니다. GDAL이 이 요소들을 OGR 도형으로 변환하지 못 하기 때문에, 기본적으로 건너뜁니다.

GDAL 2.3.0버전부터, :decl_configoption:`DXF_3D_EXTENSIBLE_MODE` 환경설정 옵션을 TRUE로 설정해서 필드에 원시 ASM 데이터를 저장한 이 요소들을 포함시켜 상용 변환 도구들과의 상호 호환성을 높일 수 있습니다. 이 옵션은 다음 새 필드 2개를 추가합니다:

-  ASMData: ASM 데이터를 담고 있는 바이너리 필드입니다.
-  ASMTransform: 요소에 적용될 아핀 변환을 나타내는 실수값 12개의 열 중심(column-major) 목록입니다.

이 옵션은 오토캐드 2013(AC1027) 및 그 이후 포맷의 DXF 파일에만 작동합니다.

문자 인코딩
~~~~~~~~~~~~~~~~~~~

일반적으로 DXF 파일은 ANSI_1252/Win1252로 인코딩되어 있습니다. GDAL/OGR은 이 인코딩을 읽어올 때 UTF-8로 변환하고 작성할 때 다시 ANSI_1252로 변환하려 시도합니다. DXF 파일은 자신의 인코딩을 나타내는 헤더 필드($DWGCODEPAGE)도 가질 수 있습니다. 이 헤더 필드를 이용해서 다른 코드 페이지를 UTF-8로 다시 코딩하려 시도합니다. 이 시도의 성공 여부는 코드 페이지 명명법 및 GDAL/OGR가 문자 재(再)코딩을 위한 iconv 라이브러리를 대상으로 빌드되었느냐에 달려 있습니다.

가끔 DXF 파일의 $DWGCODEPAGE 설정이 틀렸거나, OGR가 인식하지 못 하는 경우가 있습니다. 이때 헤더 필드를 직접 편집하거나, :decl_configoption:`DXF_ENCODING` 환경설정 옵션을 사용해서 OGR가 인코딩 변환 시 사용할 ID를 대체할 수 있습니다. DXF_ENCODING의 값은 DXF $DWGCODEPAGE 이름이 아니라 CPLRecode()가 지원하는 인코딩 이름이어야 합니다. DXF_ENCODING 옵션을 "UTF-8"로 설정하면 텍스트를 읽어오면서 다시 코딩하려는 시도를 막을 수 있습니다.

DXF 작성기
----------

DXF 파일은 오토캐드 2004 포맷으로 작성됩니다. $GDAL_DATA/header.dxf 파일로부터 표준 헤더를 (ENTITIES 키워드 바로 앞까지의 모든 내용을) 작성하고, ENTITIES 뒤에 $GDAL_DATA/trailer.dxf 파일을 추가합니다. 산출물 파일을 생성하는 데 ORG 레이어 하나만 사용할 수 있습니다. (그러나 DXF 레이어는 여러 개 생성할 수 있습니다 -- 다음 단락을 참조하십시오.)

-  LABEL 스타일을 가진 포인트 객체를 스타일 정보 기반 MTEXT 요소로 작성합니다.

-  LABEL 스타일이 없는 포인트 객체를 POINT 요소로 작성합니다.

-  라인스트링 및 멀티라인스트링을 하나 또는 그 이상의 LWPOLYLINE 요소로 작성하고, 폴리곤 고리의 경우 고리를 닫습니다. 도형의 표고가 일정하지 않다면 POLYLINE 요소로 작성합니다. 라인 굵기 및 색상을 보전하려 시도합니다.

-  폴리곤, 삼각형 및 멀티폴리곤 객체는 기본적으로 HATCH 요소로 작성합니다. 이 객체들을 HATCH 대신 LWPOLYLINE/POLYLINE 요소로 작성하려면 :decl_configoption:`DXF_WRITE_HATCH` 환경설정 옵션을 FALSE로 설정하십시오. 사용자 도형의 표고가 일정하지 않은 경우 이 옵션을 사용해야 할 수도 있습니다. DXF HATCH 요소가 표고가 일정하지 않은 도형을 표현하지 못 하기 때문입니다.

스타일 문자열에서 첫 번째 (PEN, BRUSH 등등) 도구만 읽어옵니다. 다음 스타일 문자열 파라미터들을 인식합니다:

.. list-table::
   :header-rows: 1

   * - 도구
     - 사용할 수 있는 도형 유형
     - 지원 파라미터
   * - PEN
     - 포인트, (멀티)라인스트링
     - 색상(c); 굵기(w); 대시 패(p)
   * - BRUSH
     - (멀티)폴리곤, 삼각형
     - 전경색(fc)
   * - SYMBOL
     - 포인트
     - 색상(c)
   * - LABEL
     - 포인트
     -  *  GDAL 2.3.0 이상 버전: 텍스트(t); 글꼴 이름(f); 글꼴 크기(s), 대문자 높이로 취급; 굵은 글꼴(bo); 이탤릭 글꼴(it); 텍스트 색상(s); x 및 y 오프셋(dx,dy); 각도(a); 기준점(p); 스트레치(w)
        *  GDAL 2.2.x 이전 버전: 텍스트(t); 글꼴 크기(s), 대문자 높이로 취급; 텍스트 색상(s); 각도(a); 기준점(p)

데이터셋 생성 시 다음 데이터셋 생성 옵셙들을 지원합니다:

-  **HEADER=filename**:
   GDAL_DATA 디렉터리에 위치한 header.dxf 파일을 대체할 헤더 파일을 설정합니다.

-  **TRAILER=filename**:
   GDAL_DATA 디렉터리에 위치한 trailer.dxf 파일을 대체할 트레일러 파일을 설정합니다.

헤더 및 트레일러 템플릿이 완전한 DXF 파일일 수도 있습니다. 이 드라이버는 템플릿을 스캔해서 필요한 부분만 (ENTITIES 부분의 바로 앞 또는 바로 뒤 부분만) 추출할 것입니다.

블록 참조
~~~~~~~~~~~~~~~~

산출 파일에 실제 DXF BLOCK 정의를 생성하기 위해 "entities" 레이어뿐만 아니라 "blocks" 레이어도 DXF로 내보낼 수 있습니다. 어떤 요소에 블록 이름을 지정한 경우 INSERT 요소도 작성할 수 있습니다. 이 작업이 성공하려면 다음과 같은 조건을 만족해야 합니다:

-  "blocks" 레이어를 생성할 수도 있는데, "entities" 레이어보다 먼저 생성해야만 합니다.

-  블록 레이어의 요소들이 Block 필드를 채우고 있어야 합니다. (GDAL 2.2.x 이전 버전에서는 이 속성을 BlockName이라고 부른다는 사실을 기억하십시오.)

-  "entities" 레이어에 INSERT로 작성할 객체가 POINT 도형이어야 하며, BlockName 필드가 설정되어 있어야 합니다. BlockAngle, BlockScale, BlockOCSNormal 및 BlockOCSCoords 필드도 설정할 수도 있습니다. (자세한 내용은 앞의 DXF_INLINE_BLOCKS 단락을 참조하십시오.) BlockOCSCoords 필드를 실수형 숫자 3개로 설정할 경우, 블록 위치로 사용합니다. 이 경우 POINT 도형 위치는 무시합니다.

-  템플릿 헤더에 블록 (이름)이 이미 정의된 경우, "blocks" 레이어에서 새로운 정의를 지정하느냐 마느냐에 상관없이 쳄플릿 헤더의 정의를 사용할 것입니다.

DXF_INLINE_BLOCKS 환경설정 옵션의 목적은, FALSE로 설정하는 경우 DXF로부터 DXF로 단순 변환 시 원본 블록을 재생성하고, INSERT 요소를 폭발시키기 보다 그대로 유지할 수 있게 된다는 점입니다.

레이어 정의
~~~~~~~~~~~~~~~~~

요소 작성 시, Layer 필드가 채워져 있다면 이 필드를 사용해서 "entities" 레이어를 설정합니다. 템플릿 헤더에 레이어가 이미 정의되어 있지 않은 경우, 기본 레이어("0")의 정의로부터 새 레이어 정의를 복사해 올 것입니다.

라인 유형 정의
~~~~~~~~~~~~~~~~~~~~

라인스트링 도형 작성 시, 라인 유형(대시 패턴) 정의에 대해 다음과 같은 규칙을 적용합니다.:

-  작성된 객체에 Linetype 필드가 설정돼 있고 헤더 템플릿에 해당 라인 유형이 이미 정의돼 있는 경우, 요소로부터 그 라인 유형을 참조할 것입니다. 헤더에 정의된 라인 유형에 어울리는 "p" 패턴을 가진 스타일 문자열이 존재하는 경우 라인 유형 척도값을 작성합니다.

-  Linetype 필드가 설정돼 있지만 헤더 템플릿에는 정의돼 있지 않은 경우, 객체가 PEN 도구와 "p" 패턴을 포함하는 OGR 스타일 문자열을 가지고 있다면 그 정의를 추가할 것입니다.

-  객체에 설정된 Linetype 필드는 없지만 객체가 PEN 도구와 "p" 패턴을 포함하는 OGR 스타일 문자열을 가지고 있는 경우 산출 파일에 자동으로 명명된 라인 유형을 생성할 것입니다. 또는 이전에 어울리는 라인 유형을 생성했다면, 필요한 경우 라인 유형 척도를 이용해서 해당 라인 유형을 참조할 것입니다.

이 규칙들의 목적은 DXF에 라인 유형을 작성할 때 "쇄선(dot dash)" 스타일 패턴을 보전하고, 헤더 템플릿에 해당 특정 라인 유형을 사전 정의할 수 있게 하고, 원하는 경우 Linetype 필드를 이용해서 참조할 수 있게 하려는 것입니다.

패턴이 라인 패턴을 정의하는 데 (지리참조된) "g" 단위를 사용한다고 가정합니다. 그렇지 않은 경우, DXF 패턴의 크기 조정 작업이 틀릴 가능성이 아주 높아집니다.

단위
~~~~~

GDAL은 DXF 파일을 "Imperial - Inches"로 설정된 측정 단위로 작성합니다. 이 단위를 변경해야 하는 경우, 헤더 템플릿에 있는 `$MEASUREMENT <https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/AutoCAD-Core/files/GUID-1D074C55-0B63-482E-8A37-A52AC0C7C8FE-htm.html>`_ 및 `$INSUNITS <https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/AutoCAD-Core/files/GUID-A58A87BB-482B-4042-A00A-EEF55A2B4FD8-htm.html>`_ 변수를 편집하십시오.

참고
--------

-  `알려진 문제점 목록 <https://github.com/OSGeo/gdal/blob/master/ogr/ogrsf_frmts/dxf/KNOWN_ISSUES.md>`_

-  `오토캐드 2000 DXF 참조 문서 <http://www.autodesk.com/techpubs/autocad/acad2000/dxf/>`_

-  `오토캐드 2014 DXF 참조 문서 <http://images.autodesk.com/adsk/files/autocad_2014_pdf_dxf_reference_enu.pdf>`_

