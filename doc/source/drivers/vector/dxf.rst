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

기본적으로, DXF 파일의 전체 내용은 "entities" 라는 이름의 단일 OGR 레이어로 표현됩니다. 모든 객체는 다음과 같은 일반 필드들을 가질 것입니다::

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

DXF files may contain 3DSOLID, REGION, BODY and SURFACE entities, which
contain 3D modelling data in the proprietary Autodesk ShapeManager (ASM) format,
a broadly compatible fork of the ACIS format. GDAL cannot transform these
entities into OGR geometries, so they are skipped by default.

Starting from GDAL 2.3.0, the :decl_configoption:`DXF_3D_EXTENSIBLE_MODE` configuration
option may be set to TRUE to include these entities with the raw ASM
data stored in a field, allowing for interoperability with commercial conversion
tools. This option adds two new fields:

-  ASMData: A binary field that contains the ASM data.
-  ASMTransform: A column-major list of 12 real values indicating the affine
   transformation to be applied to the entity.

This feature only works for DXF files in AutoCAD 2013 (AC1027) format
and later.

문자 인코딩
~~~~~~~~~~~~~~~~~~~

Normally DXF files are in the ANSI_1252 / Win1252 encoding. GDAL/OGR
attempts to translate this to UTF-8 when reading and back into ANSI_1252
when writing. DXF files can also have a header field ($DWGCODEPAGE)
indicating the encoding of the file. An attempt is made to use this to
recode other code pages to UTF-8. Whether this works will depend on the
code page naming and whether GDAL/OGR is built against the iconv library
for character recoding.

In some cases the $DWGCODEPAGE setting in a DXF file will be wrong, or
unrecognised by OGR. It could be edited manually, or the :decl_configoption:`DXF_ENCODING`
configuration variable can be used to override what id will be used by
OGR in transcoding. The value of DXF_ENCODING should be an encoding name
supported by CPLRecode() (i.e. an iconv name), not a DXF $DWGCODEPAGE
name. Using a DXF_ENCODING name of "UTF-8" will avoid any attempt to
recode the text as it is read.

DXF 작성기
----------

DXF files are written in AutoCAD 2004 format. A standard header
(everything up to the ENTITIES keyword) is written from the
$GDAL_DATA/header.dxf file, and the $GDAL_DATA/trailer.dxf file is added
after the entities. Only one OGR layer can be used to create the output
file (but many DXF layers can be created - see below).

-  Point features with LABEL styling are written as MTEXT entities based
   on the styling information.
-  Point features without LABEL styling are written as POINT entities.
-  LineString and MultiLineString features are written as one or more
   LWPOLYLINE entities, closed in the case of polygon rings. If the
   geometry does not have a constant elevation, a POLYLINE entity is
   written. An effort is made to preserve line width and color.
-  Polygon, Triangle and MultiPolygon features are written as HATCH
   entities by default. To write these features as LWPOLYLINE/POLYLINE
   entities instead, set the configuration option :decl_configoption:`DXF_WRITE_HATCH` to
   FALSE. You may need to do this if your geometries do not have a
   constant elevation, as the DXF HATCH entity cannot represent such
   geometries.

Only the first tool (PEN, BRUSH, etc) in the style string is read. The
following style string parameters are understood:

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

The dataset creation supports the following dataset creation options:

-  **HEADER=**\ *filename*: Override the header file used - in place of
   header.dxf located in the GDAL_DATA directory.
-  **TRAILER=**\ *filename*: Override the trailer file used - in place
   of trailer.dxf located in the GDAL_DATA directory.

The header and trailer templates can be
complete DXF files. The driver will scan them and only extract the
needed portions (portion before or after the ENTITIES section).

블록 참조
~~~~~~~~~~~~~~~~

It is possible to export a "blocks" layer to DXF in addition to the
"entities" layer in order to produce actual DXF BLOCKs definitions in
the output file. It is also possible to write INSERT entities if a block
name is provided for an entity. To make this work the following
conditions apply:

-  A "blocks" layer may be created, and it must be created before the
   entities layer.
-  The entities in the blocks layer should have the Block field
   populated. (Note, in GDAL 2.2.x and earlier this attribute was called
   BlockName.)
-  Objects to be written as INSERTs in the entities layer should have a
   POINT geometry, and the BlockName field set. You may also set
   BlockAngle, BlockScale, BlockOCSNormal and BlockOCSCoords (see above
   under DXF_INLINE_BLOCKS for details). If BlockOCSCoords is set to a
   list of 3 real numbers, it is used as the location of the block; in
   this situation the position of the POINT geometry is ignored.
-  If a block (name) is already defined in the template header, that
   will be used regardless of whether a new definition was provided in
   the blocks layer.

The intention is that a simple translation from DXF to DXF with
DXF_INLINE_BLOCKS set to FALSE will approximately reproduce the original
blocks and keep INSERT entities as INSERT entities rather than exploding
them.

레이어 정의
~~~~~~~~~~~~~~~~~

When writing entities, if populated the Layer field is used to set the
written entities layer. If the layer is not already defined in the
template header then a new layer definition will be introduced, copied
from the definition of the default layer ("0").

라인 유형 정의
~~~~~~~~~~~~~~~~~~~~

When writing linestring geometries, the following rules apply with
regard to linetype (dash pattern) definitions.

-  If the Linetype field is set on a written feature, and that linetype
   is already defined in the template header, then it will be referenced
   from the entity. If a style string is present with a "p" pattern
   proportional to the linetype defined in the header, a linetype scale
   value is written.
-  If the Linetype field is set, but the linetype is not defined in the
   header template, then a definition will be added if the feature has
   an OGR style string with a PEN tool and a "p" pattern setting.
-  If the feature has no Linetype field set, but it does have an OGR
   style string with a PEN tool with a "p" pattern set, then an
   automatically named linetype will be created in the output file. Or,
   if an appropriate linetype was previously created, that linetype will
   be referenced, with a linetype scale if required.

The intention is that "dot dash" style patterns will be preserved when
written to DXF and that specific linetypes can be predefined in the
header template, and referenced using the Linetype field if desired.

It is assumed that patterns are using "g" (georeferenced) units for
defining the line pattern. If not, the scaling of the DXF patterns is
likely to be wrong - potentially very wrong.

단위
~~~~~

GDAL writes DXF files with measurement units set to "Imperial - Inches".
If you need to change the units, edit the
`$MEASUREMENT <https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/AutoCAD-Core/files/GUID-1D074C55-0B63-482E-8A37-A52AC0C7C8FE-htm.html>`_
and
`$INSUNITS <https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/AutoCAD-Core/files/GUID-A58A87BB-482B-4042-A00A-EEF55A2B4FD8-htm.html>`_
variables in the header template.


참고
--------

-  `알려진 문제점 목록 <https://github.com/OSGeo/gdal/blob/master/ogr/ogrsf_frmts/dxf/KNOWN_ISSUES.md>`_

-  `오토캐드 2000 DXF 참조 문서 <http://www.autodesk.com/techpubs/autocad/acad2000/dxf/>`_

-  `오토캐드 2014 DXF 참조 문서 <http://images.autodesk.com/adsk/files/autocad_2014_pdf_dxf_reference_enu.pdf>`_

