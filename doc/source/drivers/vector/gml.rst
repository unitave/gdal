.. _vector.gml:

GML - 지리 마크업 언어
===============================

.. shortname:: GML

.. build_dependencies:: (읽기 지원에 Xerces 또는 libexpat 필요)

OGR는 GML(Geography Markup Language) 읽기 및 쓰기를 제한적으로 지원합니다. 기존 파일의 업데이트는 지원하지 않습니다.

지원하는 GML 계열:

.. list-table:: Supported GML flavors
   :header-rows: 1

   * - 읽기
     - 쓰기
   * - 단순 피처 모델로 변환할 수 있는 GML2 및 GML3
     - GML 2.1.2 또는 GML 3 SF-0(GML 3.1.1 준수 SF-0 수준)

GDAL 2.2버전부터, 응용 프로그램 스키마 주도 GML 용 또다른 드라이버 :ref:`GMLAS <vector.gmlas>` 도 사용할 수 있습니다. GML 및 GMLAS 드라이버는 각각 자신만의 사용례를 가지고 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

파서(parser)
------------

이 드라이버의 판독기 부분은 OGR가 Xerces 링크를 포함해서 빌드된 경우에만 작동합니다. Xerces를 사용할 수 없는 경우, OGR가 Expat 링크를 포함해서 빌드된 경우에도 판독기가 작동합니다. XML 검증은 기본적으로 비활성화됩니다. GML 쓰기 부분은 Xerces 또는 Expat이 없더라도 항상 지원됩니다.

주의: 빌드 시 Xerces 및 Expat 둘 다 사용할 수 있다면, GML 드라이버는 가능한 경우 (호환되는 인코딩으로 된 GML 파일의 경우) 런타임에서 Expat 파서를 우선적으로 선택하고, 그 외의 경우 Xerces 파서를 기본값으로 선택할 것입니다. 하지만 **GML_PARSER** 환경설정 옵션을 **EXPAT** 또는 **XERCES** 로 설정하면 드라이버의 파서 선택을 강제할 수 있습니다.

좌표계 지원
-----------

GML 드라이버는 좌표계를 지원합니다. 레이어의 모든 도형이 동일한 srsName 속성값을 가지고 있는 경우에만 좌표계를 리포트합니다. (예를 들어 WFS 1.1.0버전이 반환하는) 지리 좌표계가 "urn:ogc:def:crs:EPSG:" (또는 GDAL 2.1.2버전부터 "http://www.opengis.net/def/crs/EPSG/0/") 같은 srsName인 경우 축 순서가 표준이 요구하는 [위도,경도]일 것이지만, 이는 일반적이지 않은 순서로 축 순서를 인식하지 못 하는 응용 프로그램에서 문제가 발생할 수도 있습니다. 따라서 이 드라이버는 기본적으로 좌표 순서를 뒤바꿔서 [경도,위도] 순서로 만들고, 축 순서를 지정하지 않은 공간 좌표계를 리포트할 것입니다. **GML_INVERT_AXIS_ORDER_IF_LAT_LONG** 환경설정 옵션을 **NO** 로 설정하면 원본 [위도,경도] 순서와 축 순서를 지정한 공간 좌표계를 가져올 수 있습니다.

srsName이 (목적 상 "urn:ogc:def:crs:EPSG::XXXX" 형식이 더 명확하겠지만) "EPSG:XXXX" 형식이고 파일의 좌표가 [위도,경도] 순서인 경우도 있습니다. OGR는 기본적으로 EPSG 축 순서를 고려하지 않고 좌표를 [위도,경도] 순서로 리포트할 것입니다. 하지만 **GML_CONSIDER_EPSG_AS_URN** 환경설정 옵션을 **YES** 로 설정하면 앞 문단에서 설명한 규칙이 적용될 것입니다.

이런 규칙은 EPSG 선호 축 순서가 [편북,편동]인 투영 좌표계에도 적용됩니다.

GDAL 2.1.2버전부터, SWAP_COORDINATES 열기 옵션(또는 GML_SWAP_COORDINATES 환경설정 옵션)을 AUTO/YES/NO로 설정할 수 있습니다. 이 옵션은 x/y 또는 경도/위도 좌표 순서를 뒤바꿔야 할지 여부를 제어합니다. AUTO 모드에서는, 드라이버가 순서를 바꿔야만 하는지를 srsName과 CONSIDER_EPSG_AS_URN 및 INVERT_AXIS_ORDER_IF_LAT_LONG 같은 다른 옵션들의 값으로부터 판단할 것입니다. SWAP_COORDINATES 옵션을 YES로 설정하면 GML에 나타나는 좌표 순서와 상관없이 항상 순서를 뒤바꿀 것입니다. NO로 설정하면 동일한 순서를 유지할 것입니다. 기본값은 AUTO입니다.

스키마
------

대부분의 GML 판독기와는 반대로, OGR GML 판독기는 GML 파일을 읽을 수 있기 위해 (.xsd 확장자를 가진) 객체 클래스의 XML 스키마 정의를 필요로 하지 않습니다. .xsd 파일이 없거나 또는 OGR가 .xsd 파일을 파싱하지 못 하는 경우, 이 드라이버가 구조를 판단하기 위해 파일을 스캔하고 GML 이름공간에 있는 "알려진" GML 객체를 찾아서 객체 클래스와 연관 속성을 자동적으로 발견하려 시도합니다. 이 접근법이 오류를 일으키기 쉽긴 하지만, 관련 스키마 (.xsd) 파일이 없더라도 GML 파일을 작업할 수 있다는 장점이 있습니다.

"a_filename.gml,xsd=another_filename.xsd"를 연결 문자열로 이용하면 사용할 XSD 스키마를 명확하게 파일명으로 지정할 수 있습니다. XSD 열기 옵션으로도 XSD를 지정할 수 있습니다.

GML 파일을 처음으로 열 때 관련 .xsd 파일이 없거나 정확하게 파싱되지 않은 경우, 객체 유형 집합, 각 객체 유형 관련 속성, 그리고 다른 데이터셋 수준 정보를 판단하기 위해 GML 파일 전체를 완전히 스캔합니다. 대상 GML 파일과 동일한 기본명에 .gfs 확장자를 붙인 파일에 이 정보를 저장합니다. 이후 동일한 GML 파일에 접근할 때, 접근 속도를 높이기 위해 데이터셋 수준 정보를 사전 정의하고 있는 .gfs 파일을 이용할 것입니다. GML 파일을 어떻게 파싱할 것인지 그 방법을 변경하기 위해 제한적인 범위에서 .gfs 파일을 직접 편집할 수도 있습니다. 관련 .gml 파일이 더 최근의 타임스탬프를 가지고 있을 경우 .gfs 파일을 무시할 것이라는 사실을 주의하십시오.

객체 유형 및 필드 목록을 결정하기 위해 GML 파일을 사전 스캔할 때, 필드 유형을 시도하고 결정하기 위해 필드의 내용도 스캔합니다. 일부 응용 프로그램에서는 모든 필드를 그냥 문자열 필드로 취급하면 더 쉽게 스캔할 수 있습니다. **GML_FIELDTYPES** 환경설정 옵션을 **ALWAYS_STRING** 으로 설정하면 됩니다.

**GML_ATTRIBUTES_TO_OGR_FIELDS** 환경설정 옵션을 **YES** 로 설정하면 OGR 필드를 생성하기 위해 GML 요소의 속성도 연산에 넣을 것입니다.

CPLSetConfigOption() 함수를 통해 또는 환경 변수로 환경설정 옵션을 설정할 수 있습니다.

**GML_GFS_TEMPLATE** 환경설정 옵션(또는 **GFS_TEMPLATE** 열기 옵션)을 **path_to_template.gfs** 로 설정하면 사전 정의된 GFS 파일을 무조건적으로 사용할 수 있습니다. 수많은 개별 GML 파일을 연속으로 가져오는 데 (**-append**) 전체 GML 집합의 완전하게 일관된 데이터 레이아웃을 보전하고자 하는 경우 이 옵션이 매우 유용합니다.
**GML_GFS_TEMPLATE** 환경설정 옵션을 사용하는 경우 **-lco LAUNDER=yes** 를 설정하지 않도록 주의해주십시오. 연속적인 GML 가져오기 실행들 사이에 속성 이름을 정확하게 인식할 수 없게 만들기 때문입니다.

특정 GML 응용 프로그램 스키마
----------------------------------

영국 육지측량부(UK Ordnance Survey) MasterMap 같은 몇몇 GML 프로파일에서 찾을 수 있는 (평탄화되지 않는 속성 계층) 내포 GML 요소의 객체 속성을 탐지합니다. GML 요소의 발생 빈도가 몇 번 이상일 경우 IntegerList, RealList 및 StringList 필드 유형도 지원합니다.

독일 GML 정보 교환 포맷(NAS/ALKIS)을 읽어오는 데 특화된 GML 드라이버 -- :ref:`NAS <vector.nas>` 드라이버 -- 를 사용할 수 있습니다.

GML 드라이버는 AIXM 또는 CityGML 파일의 읽기를 부분적으로 지원합니다.

GML 드라이버는 다음 파일의 읽기를 지원합니다:

-  `핀란드 국토조사원 지형 데이터 GML 파일(MTK GML) <http://xml.nls.fi/XML/Schema/Maastotietojarjestelma/MTK/201202/Maastotiedot.xsd>`_

-  `핀란드 국토조사원 지적 데이터 GML 파일 <http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/>`_

-  `Inspire GML 스키마 지적 데이터 <http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd>`_

-  `체코 RUIAN 정보 교환 포맷(VFR) <http://www.cuzk.cz/Uvod/Produkty-a-sluzby/RUIAN/2-Poskytovani-udaju-RUIAN-ISUI-VDP/Vymenny-format-RUIAN/Vymenny-format-RUIAN-%28VFR%29.aspx>`_

GML 드라이버는 CSW GetRecords 쿼리에 대한 응답의 읽기를 지원합니다.

OGR 2.2버전부터, GML 드라이버는 일본 FGD GML v4 파일의 읽기를 지원합니다.

도형 읽어오기
----------------

객체를 읽어올 때 (다중 도형인 경우) 이 드라이버는 기본적으로 객체를 서술하는 XML 하위 트리에서 마지막으로 인식한 GML 도형만 연산에 넣을 것입니다.

그러나 XSD 파서가 .xsd 스키마를 이해하고 도형 필드 여러 개를 선언하는 경우 또는 .gfs 파일이 도형 필드 여러 개를 선언하는 경우, GML 드라이버가 :ref:`rfc-41` 에 따라 다중 도형 필드를 리포트할 것입니다.

다중 도형이 나타나는 경우, 도형이 <geometry> 요소 안에 있다면 해당 도형을 선택할 것입니다. Inspire GML 객체에도 일관적으로 이 기본 습성이 적용될 것입니다.

사용자가 .gfs 파일을 변경해서 <GeometryElementPath> 요소로 그 경로를 지정, 적절한 도형을 선택하게 할 수 있습니다. 아래 .gfs 문법 설명을 참조하십시오.

TopoCurve, TopoSurface, MultiCurve를 포함하는 GML 도형을 지원합니다. TopoCurve 유형 GML 도형을 두 가지 도형 유형 가운데 하나로 해석할 수 있습니다. TopoCurve 유형 GML 도형에 있는 <Edge> 요소가 곡선 및 곡선에 대응하는 노드들을 담고 있습니다. 기본적으로 주 도형인 곡선만 OGRMultiLineString으로 리포트합니다. 노드를 OGRMultiPoint로 가져오려면, 환경설정 옵션 **GML_GET_SECONDARY_GEOM** 을 **YES** 로 설정해야 합니다. 이 옵션을 설정하면 부 도형만 리포트합니다.

Arc, ArcString, ArcByBulge, ArcByCenterPoint, Circle 및 CircleByCenterPoints를 원형 스트링(circular string) OGR 도형으로 반환할 것입니다. CurveComposite, MultiCurve, Surface 같은 다른 GML 도형이 이런 GML 도형들을 담고 있는 경우, 대응하는 비선형 OGR 도형도 반환할 것입니다.
GML3 응용 프로그램 스키마를 읽어올 때 CurvePropertyType, SurfacePropertyType, MultiCurvePropertyType 또는 MultiSurfacePropertyType 같은 도형 필드의 선언도 잠재적인 비선형 도형이라고 해석하고, 대응하는 OGR 도형을 레이어 도형 유형으로 사용할 것입니다.

gml:xlink 분해하기
-------------------

gml:xlink 분해(resolve)를 지원합니다. 분해기(resolver)가 xlink:href 태그를 담고 있는 요소를 발견하면, 동일한 GML 파일, 파일 시스템에 있는 다른 GML 파일, 또는 cURL을 사용하는 웹 상에서 대응하는 gml:id를 가진 요소를 찾으려 시도합니다. 분해를 활성화하려면 **GML_SKIP_RESOLVE_ELEMS** 환경설정 옵션을 **NONE** 으로 설정하십시오.

분해된 파일이 이미 존재하지 않는 경우, 기본적으로 원본 파일과 같은 디렉터리에 분해된 파일을 ".resolved.gml" 확장자로 저장할 것입니다. **GML_SAVE_RESOLVED_TO** 환경설정 옵션을 이용해서 이 습성을 변경할 수 있습니다. 이 옵션을 **SAME** 으로 설정하면 원본 파일을 덮어씁니다. **filename ending with .gml** 로 설정하면 해당 위치에 저장합니다. 다른 설정값은 모두 무시합니다. 분해기가 어떤 이유로든 파일을 작성하지 못 하는 경우, CPLGenerateTempFilename("ResolvedGML") 함수를 이용해서 생성되는 임시 파일로 저장하려 시도할 것입니다. 그렇게 하지 못 한다면, 분해 작업이 실패합니다.

분해 작업 알고리즘이 대용량 파일에 최적화되지 않았다는 사실을 기억하십시오. xlink:href 태그를 수천 개 이상 가진 파일의 경우 처리 시간이 몇 분을 넘길 수도 있습니다. 매 256개 링크마다 CPLDebug() 함수를 통해 대략적인 진행 상황을 출력합니다. CPL_DEBUG 환경 변수를 설정해야 이를 볼 수 있습니다.
사용자가 필요없는 요소를 하나라도 알고 있다면 분해 작업 시간을 줄일 수 있습니다. **GML_SKIP_RESOLVE_ELEMS** 환경설정 옵션에 필요없는 요소의 이름을 쉼표로 구분한 목록을 설정하십시오. (기본값) **ALL** 로 설정하면 모든 분해 작업을 건너뜁니다. **NONE** 으로 설정하면 모든 xlink를 분해합니다.

대체 분해 메소드를 사용할 수 있습니다. **GML_SKIP_RESOLVE_ELEMS HUGE** 환경설정 옵션을 이용하면 이 대체 메소드를 활성화시킬 것입니다. 이 경우 대응하는 모든 gml:id 관계를 식별하기 위한 임시 SQLite 데이터베이스를 이용해서 모든 gml:xlink를 분해할 것입니다. 이 SQL 기반 처리 과정 마지막에, **NONE** 으로 설정한 경우와 정확히 동일하지만 그 제한 사항은 없는 분해된 파일을 생성할 것입니다. gml:xlink와 gml:id 관계성을 분해하기 위해 외부 (임시) DBMS를 사용할 때의 주요 장점은 다음과 같습니다:

-  메모리 용량 제약이 없습니다. **NONE** 메소드는 전체 GML 노드 트리를 인메모리(in-memory) 저장합니다. 즉 32비트 플랫폼 상에서는 메모리 할당 제한 때문에 실질적으로 1GB를 초과하는 어떤 GML 파일도 처리하지 못 한다는 의미입니다. 파일 시스템 기반 DBMS를 사용하면 이 문제점을 간단히 피할 수 있습니다.

-  효율이 훨씬 높습니다. 특히 xlink:href / gml:id 관계쌍을 수천 개 (또는 수백만 개까지) 담고 있는 대용량 GML 파일을 작업하는 경우 그렇습니다.

-  **GML_SKIP_RESOLVE_ELEMS HUGE** 메소드를 사용하면, xlink:href / gml:id 관계쌍을 수백만 개 이상 담고 있는 (3GB 이상의) 초대용량 GML 파일을 적당한 시간 안에 (약 1시간 정도) 성공적으로 분해할 수 있습니다.

-  **GML_SKIP_RESOLVE_ELEMS HUGE** 메소드는 다음과 같은 심화 환경설정 옵션을 지원합니다:

TopoSurface 해석 규칙 (폴리곤과 내부 구멍)
--------------------------------------------------------------

GML 드라이버는 폴리곤이 내부 구멍을 하나라도 담고 있는 경우 TopoSurface의 서로 다른 두 가지 해석 규칙을 인식할 수 있습니다:

-  이전까지 지원하던 해석 규칙은 다음을 가정합니다:

   -  각 TopoSurface가 수많은 Face들의 집합으로 표현될 수도 있습니다.
   -  *양(positive)의* (예를 들면 **orientation="+"** 를 선언하는) Face가 일부 폴리곤의 외부 고리(Exterior Ring)를 표현한다고 가정합니다.
   -  *음(negative)의* (예를 들면 **orientation="-"** 를 선언하는) Face가 가장 최근 선언된 외부 고리에 속한 내부 고리(Interior Ring)를 표현한다고 가정합니다.
   -  각 고리를 표현하기 위해 사용된 Edge를 정렬하는 일은 중요합니다: 각 Edge가 다음 Edge에 정확하게 인접한다고 예상하기 때문입니다.

-  새로운 해석 규칙은 다음을 가정합니다:

   -  각 TopoSurface가 수많은 Face들의 집합으로 표현될 수도 있습니다.
   -  모든 Face에 선언된 **orientation** 은 외부/내부 고리와 아무 상관도 없습니다.
   -  각 Face는 이제 최종적으로는 가능한 모든 내부 고리(*구멍*)을 포함하는 완전한 폴리곤을 표현하려 합니다.
   -  같은 Face를 구성하는 모든 Edge의 상대적인 정렬 순서는 전혀 상관없습니다.

최신 해석은 GML 3 표준 권장 사항과 완전하게 일치하는 것처럼 보입니다. 따라서 현재 이 최신 해석 규칙을 OGR가 지원하는 기본 해석으로 가정합니다.

**주의** : 최신 해석을 사용하기 위해서는 GDAL/OGR를 GEOS 라이브러리를 대상으로 빌드해야 합니다.

하지만 어쨌든 **GML_FACE_HOLE_NEGATIVE** 환경설정 옵션을 이용하면, GML 3 위상(Topology)을 파싱할 때 실제로 적용할 해석을 선택할 수 있습니다:

-  **GML_FACE_HOLE_NEGATIVE NO** (*기본* 옵션)을 선택하면 최신 해석 규칙을 활성화합니다.

-  그러나 **GML_FACE_HOLE_NEGATIVE YES** 를 명확하게 설정하면 예전 해석 규칙을 활성화합니다.

인코딩 문제점
---------------

Expat 라이브러리는 다음 내장 인코딩 읽기를 지원합니다:

-  US-ASCII
-  UTF-8
-  UTF-16
-  ISO-8859-1
-  Windows-1252

OGR가 반환하는 콘텐츠는 파일 헤더에 언급된 인코딩으로 변환한 다음 UTF-8로 인코딩될 것입니다.

GML 파일이 앞의 인코딩 가운데 하나로 인코딩되지 않았는데 사용할 수 있는 파서가 Expat뿐인 경우, GML 드라이버는 해당 파일을 파싱하지 않을 것입니다. 해당 파일을 지원되는 인코딩 가운데 하나로 -- 예를 들면 *iconv* 유틸리티를 이용해서 -- 변환한 다음 XML 헤더에 있는 *encoding* 파라미터를 그에 맞춰 변경할 수도 있습니다.

GML 파일 작성 시, 이 드라이버는 UTF-8 콘텐츠가 전송되어 올 것으로 예상합니다.

주의: 현재 XML 헤더에 지정된 XML 인코딩을 이해하지 못 하는 통합 XML 파서가 .xsd 스키마 파일을 파싱합니다. 이 파서는 인코딩이 항상 UTF-8일 것으로 예상합니다. 스키마 파일에 있는 속성 이름이 아스키가 아닌 문자를 담고 있다면, 먼저 *iconv* 유틸리티를 이용해서 .xsd 파일을 UTF-8 인코딩으로 변환하는 편이 좋습니다.

객체ID (fid / gml:id)
-------------------------

이 드라이버는 GML WFS 문서를 읽어올 때 gml:id 속성의 내용을 *gml_id* 라는 문자열 필드로 노출시킵니다. GML 3 문서를 작성할 때 필드 이름이 *gml_id* 라면 해당 필드의 내용도 생성되는 객체의 gml:id 속성의 내용을 작성하는 데 사용할 것입니다.

이 드라이버는 파일 시작 위치에 있는 fid(GML 2 문서, GML 3에서는 gml:id) 속성의 존재를 자동 탐지합니다. 이 속성이 탐지되면, 기본적으로 *fid* (GML 3에서는 *gml_id*) 필드로 노출시킵니다. **GML_EXPOSE_FID** 또는 **GML_EXPOSE_GML_ID** 환경설정 옵션들을 각각 **YES** 또는 **NO** 로 설정하면 자동 탐지를 무시할 수 있습니다.

GML 2 문서를 작성할 때 필드 이름이 *fid* 라면 해당 필드의 내용도 생성되는 객체의 fid 속성의 내용을 작성하는 데 사용할 것입니다.

대용량 다중 레이어 GML 파일 작업 시 성능 문제
----------------------------------------------------

여러 레이어들 사이에 공유되는 GML 파서는 GML 데이터소스 하나 당 하나뿐입니다. GML 드라이버는 기본적으로 레이어에 처음 접근할 때마다 파일 처음부터 다시 읽기 시작하기 때문에, 대용량 GML 파일의 경우 성능이 저하될 수 있습니다.

동일한 레이어에 속해 있는 모든 객체가 파일에 순차적으로 작성된 경우 **GML_READ_MODE** 환경설정 옵션을 **SEQUENTIAL_LAYERS** 로 설정할 수 있습니다. 그러면 레이어를 하나씩 완전히 읽어올 때 판독기가 필요없는 리셋을 하지 않을 것입니다. 최상의 성능을 보이려면, 레이어를 파일에 나타나는 순서대로 읽어와야만 합니다.

.xsd 및 .gfs 파일이 둘 다 없는 경우, .gfs 파일 작성 시 파서가 레이어들의 레이아웃을 탐지할 것입니다. 레이어들이 순차적이라면, .gfs 파일에 *<SequentialLayers>true</SequentialLayers>* 요소를 작성해서 사용자가 명확하게 설정하지 않더라도 GML_READ_MODE 환경설정 옵션을 자동적으로 SEQUENTIAL_LAYERS로 초기화할 것입니다.

GML_READ_MODE 환경설정 옵션을 INTERLEAVED_LAYERS로 설정하면 서로 다른 레이어들의 객체들이 교차삽입된 GML 파일을 읽어올 수 있습니다. 이 경우, GetNextFeature() 매소드의 의미가 다음과 같이 살짝 변경될 것입니다: NULL이 반환되더라도 반드시 현재 레이어의 모든 객체를 읽었다는 뜻이 아니라 아직 읽어올 객체가 있지만 또다른 레이어에 속해 있다는 뜻이 될 수도 있습니다. 이런 경우 다음과 비슷한 코드를 이용해서 파일을 읽어야 합니다:

::

       int nLayerCount = poDS->GetLayerCount();
       int bFoundFeature;
       do
       {
           bFoundFeature = FALSE;
           for( int iLayer = 0; iLayer < nLayerCount; iLayer++ )
           {
               OGRLayer   *poLayer = poDS->GetLayer(iLayer);
               OGRFeature *poFeature;
               while((poFeature = poLayer->GetNextFeature()) != NULL)
               {
                   bFoundFeature = TRUE;
                   poFeature->DumpReadable(stdout, NULL);
                   OGRFeature::DestroyFeature(poFeature);
               }
           }
       } while (bInterleaved && bFoundFeature);

열기 옵션
------------

-  **XSD=filename**:
   사용할 XSD 응용 프로그램 스키마의 파일명을 명확하게 지정합니다.

-  **WRITE_GFS=AUTO/YES/NO**: (GDAL 3.2 이상 버전)
   .gfs 파일을 작성할지 여부를 선택합니다.
   AUTO 모드에서는 인식되는 .xsd 파일이 없고, .gfs 파일이 존재하지 않으며, 파일 시스템이 네트워크를 지원하지 않는 경우에만 .gfs 파일을 작성합니다. 이 옵션을 YES로 설정하면 AUTO 모드에서는 시도하지 않을 상황에서도 강제로 .gfs 파일을 작성합니다. 또는 NO로 설정해서 .gfs 파일 작성을 비활성화시킬 수도 있습니다.

-  **GFS_TEMPLATE=filename**:
   사전 정의된 .gfs 파일을 무조건 사용합니다.
   수많은 개별 GML 파일을 연속으로 가져오는 데 (**-append**) 전체 GML 집합의 완전하게 일관된 데이터 레이아웃을 보전하고자 하는 경우 이 옵션이 매우 유용합니다.
   이 옵션을 사용하는 경우 **-lco LAUNDER=yes** 를 설정하지 않도록 주의해주십시오. 연속적인 GML 가져오기 실행들 사이에 속성 이름을 정확하게 인식할 수 없게 만들기 때문입니다.

-  **FORCE_SRS_DETECTION=YES/NO**:
   레이어의 공간 좌표계를 탐지하기 위해 강제로 파일 전체를 스캔합니다. .gml 파일 옆에 .xsd 파일이 존재하는 경우 이 옵션이 필요할 수도 있습니다. 일반적으로 이런 경우 OGR가 공간 좌표계를 탐지하지 못 할 것입니다. 왜냐하면 공간 좌표계를 탐지하려면 파일 전체를 스캔해야 하기 때문입니다. 기본값은 NO입니다.

-  **EMPTY_AS_NULL=YES/NO**:
   기본적으로 (EMPTY_AS_NULL=YES) 비어 있는 내용을 가진 필드를 비어 있는 문자열 대신 NULL이라고 리포트합니다. 이 습성은 아주 오래 전의 습성이지만, 응용 프로그램 스키마가 이런 필드를 필수라고 선언하는 경우 해당 필드를 NULL이 될 수 없다(not-nullable)고 선언하는 일을 막을 수 있습니다. 즉 비어 있는 문자열을 그대로 리포트할 뿐만 아니라 필수 필드를 NULL이 될 수 없다(not-nullable)고 리포트하게 하려면 이 옵션을 NO로 설정하면 됩니다.

-  **GML_ATTRIBUTES_TO_OGR_FIELDS=YES/NO**:
   GML 속성을 OGR 필드로 리포트해야 할지 여부를 선택합니다. GML 파일을 처음으로 열었을 때 GML 파일이 무결한 관련 .xsd 파일을 가지고 있지 않은 경우에만 이 옵션이 영향을 미친다는 사실을 기억하십시오. 기본값은 NO입니다.

-  **INVERT_AXIS_ORDER_IF_LAT_LONG=YES/NO**:
   공간 좌표계 및 좌표 순서를 일반적인 GIS 순서로 표현할지 여부를 선택합니다. 기본값은 YES입니다.

-  **CONSIDER_EPSG_AS_URN=YES/NO/AUTO**:
   EPSG:XXXX 같은 srsName이 EPSG 축 순서를 준수한다고 간주할지 여부를 선택합니다. 기본값은 AUTO입니다.

-  **SWAP_COORDINATES=AUTO/YES/NO**: (GDAL 2.1.2 이상 버전)
   x/y 또는 경도/위도 좌표 순서를 뒤바꿔야 할지 여부를 선택합니다.
   AUTO 모드에서는, 드라이버가 순서를 바꿔야만 하는지를 srsName과 CONSIDER_EPSG_AS_URN 및 INVERT_AXIS_ORDER_IF_LAT_LONG 같은 다른 옵션들의 값으로부터 판단할 것입니다.
   이 옵션을 YES로 설정하면 GML에 나타나는 좌표 순서와 상관없이 항상 순서를 뒤바꿀 것입니다.
   NO로 설정하면 동일한 순서를 유지할 것입니다.
   기본값은 AUTO입니다.

-  **READ_MODE=AUTO/STANDARD/SEQUENTIAL_LAYERS/INTERLEAVED_LAYERS**:
   읽기 모드를 설정합니다. 기본값은 AUTO입니다.

-  **EXPOSE_GML_ID=YES/NO/AUTO**:
   객체의 gml:id를 gml_id 속성으로 노출시킬지 여부를 선택합니다. 기본값은 AUTO입니다.

-  **EXPOSE_FID=YES/NO/AUTO**:
   객체ID를 fid 속성으로 노출시킬지 여부를 선택합니다. 기본값은 AUTO입니다.

-  **DOWNLOAD_SCHEMA=YES/NO**:
   필요한 경우 원격 응용 프로그램 스키마를 다운로드할지 여부를 선택합니다. (현재 원격 서버가 WFS인 경우에만 영향을 미칩니다.) 기본값은 YES입니다.

-  **REGISTRY=filename**:
   응용 프로그램 스키마를 가지고 있는 레지스트리의 파일명입니다. 기본값은 ``{GDAL_DATA}/gml_registry.xml`` 입니다.

생성 문제점
---------------

내보내기 작업 시, 단일 GML 파일에 모든 레이어를 단일 객체 집합으로 작성합니다. 각 레이어의 이름을 해당 레이어에 있는 객체의 요소 이름으로 사용합니다. 언제나 도형을 객체의 ogr:geometryProperty 요소로 작성합니다.

GML 작성기는 다음과 같은 데이터셋 생성 옵션들을 지원합니다:

-  **XSISCHEMAURI**:
   이 옵션을 설정하는 경우, 이 URI를 스키마 위치로서 삽입할 것입니다. OGR가 스키마 파일에 실제로 접근하지 않기 때문에, 사용자가 이 URI가 반드시 OGR가 생산한 GML 데이터 파일의 스키마와 일치하도록 해야 한다는 사실을 기억하십시오.

-  **XSISCHEMA**:
   이 옵션을 EXTERNAL, INTERNAL 또는 OFF 가운데 하나로 설정할 수 있습니다. 기본값은 EXTERNAL입니다.
   EXTERNAL로 설정하면 GML 응용 프로그램 스키마 파일을 (동일한 기본명을 가진) 대응하는 .xsd 파일로 작성합니다.
   INTERNAL로 설정하면 GML 파일 내부에 스키마를 작성하지만, 이는 실험적인 기능으로 거의 확실하게 무결하지 않은 XML을 생성할 것입니다.
   OFF로 설정하는 경우 스키마 생성을 비활성화합니다. (그리고 XSISCHEMAURI 옵션을 사용한다는 것을 암시합니다.)

-  **PREFIX**:
   기본값은 'ogr'입니다. 응용 프로그램 대상 이름공간 용 접두어입니다.

-  **STRIP_PREFIX**:
   기본값은 FALSE입니다. TRUE로 설정하면 GML 파일에 응용 프로그램 대상 이름공간의 접두어를 작성하지 않습니다.

-  **TARGET_NAMESPACE**:
   기본값은 "http://ogr.maptools.org/" 입니다. 응용 프로그램 대상 이름공간입니다.

-  **FORMAT**: 다음 가운데 하나로 설정할 수 있습니다:

   -  *GML2* -- GML 2.1.2를 준수하는 GML 파일을 작성 (GDAL 3.4버전 이전의 기본값)
   -  *GML3* -- GML 3.1.1 SF-0 프로파일을 준수하는 GML 파일을 작성
   -  *GML3Deegree* -- GML3 SF-0 프로파일이 권장하는 구조를 따르기 위한 몇몇 변이형을 가지고 있지만 (Deegree 버전 3 같은) 몇몇 소프트웨어가 더 잘 받아들일 수 있는 GML 3.1.1 .XSD 스키마를 작성
   -  *GML3.2* -- GML 3.2.1 SF-0 프로파일을 준수하는 GML 파일을 작성 (GDAL 3.4 이상 버전의 기본값)

   비선형 도형을 작성할 수 있지만, 앞의 GML 3 변이형 가운데 하나를 선택한 경우에만 호환됩니다. 그렇지 않다면 비선형 도형과 가장 가깝게 일치하는 선형 도형 근사치로 변환할 것입니다.
   주의: StringList, RealList 또는 IntegerList 유형을 필드를 작성할 수 있습니다. 이런 필드를 작성하면 .XSD 스키마에 SF-1 프로파일을 전파하게 될 것입니다. (SF-0 스키마는 이런 유형들을 지원하지 않기 때문입니다.)

-  **GML_FEATURE_COLLECTION=YES/NO**: (OGR 2.3 이상 버전)
   대상 이름공간에 전용 컨테이너 요소를 생성하는 대신 gml:FeatureCollection을 사용할지 여부를 선택합니다. FORMAT=GML3/GML3.2인 경우에만 영향을 미칩니다. gml:FeatureCollection은 GML 3.2버전에서 퇴출되었고, (GML 3.1.1의 경우) OGC 06-049r1 "GML 단순 피처 프로파일"이 그리고 (GML 3.2의 경우) OGC 10-100r3 "GML 단순 피처 프로파일 (정오표 포함)" 사양이 gml:FeatureCollection을 허용하지 않는다는 사실을 기억하십시오.

-  **GML3_LONGSRS=YES/NO**: (FORMAT=GML3/GML3Degree/GML3.2인 경우에만 영향을 미칩니다.)
   GDAL 2.2버전에서 퇴출되었고, SRSNAME_FORMAT으로 바뀌었습니다. 기본값은 YES입니다.
   YES로 설정한 경우, ESPG 기관을 가진 공간 좌표계를 "urn:ogc:def:crs:EPSG::" 접두어를 붙여 작성할 것입니다. 공간 좌표계에 명확한 AXIS 순서가 지정되지 않았지만 ImportFromEPSGA() 함수로 가져온 동일한 공간 좌표계 기관 코드를 위도/경도 또는 편북/편동으로 취급해야 하는 경우, 이 함수가 좌표 순서 뒤바꾸기를 처리할 것입니다.
   NO로 설정하면, ESPG 기관을 가진 공간 좌표계가 위도/경도 순서이더라도 "EPSG:" 접두어를 붙여 작성할 것입니다.

-  **SRSNAME_FORMAT=SHORT/OGC_URN/OGC_URL**: (FORMAT=GML3/GML3Degree/GML3.2이고 GDAL 버전이 2.2 이상인 경우에만 영향을 미칩니다.) 기본값은 OGC_URN입니다.
   SHORT으로 설정하면, srsName이 AUTHORITY_NAME:AUTHORITY_CODE 형식이 될 것입니다.
   OGC_URN으로 설정하면, srsName이 urn:ogc:def:crs:AUTHORITY_NAME::AUTHORITY_CODE 형식이 될 것입니다.
   OGC_URL으로 설정하면, srsName이 http://www.opengis.net/def/crs/AUTHORITY_NAME/0/AUTHORITY_CODE 형식이 될 것입니다.
   OGC_URN 및 OGC_URL의 경우, 공간 좌표계에 명확한 AXIS 순서가 지정되지 않았지만 ImportFromEPSGA() 함수로 가져온 동일한 공간 좌표계 기관 코드를 위도/경도 또는 편북/편동으로 취급해야 한다면 이 함수가 좌표 순서 뒤바꾸기를 처리할 것입니다.

-  **SRSDIMENSION_LOC=POSLIST/GEOMETRY/GEOMETRY,POSLIST**: (FORMAT=GML3/GML3Degree/GML3.2인 경우에만 영향을 미칩니다.) 기본값은 POSLIST입니다.
   2.5차원 도형의 경우, srsDimension 속성을 추가할 위치를 정의하십시오. 다양한 구현 방식이 있습니다. 일부는 <gml:posList> 요소에 삽입하고, 일부는 도형 요소 위에 삽입하기도 합니다.

-  **WRITE_FEATURE_BOUNDED_BY=YES/NO**: (FORMAT=GML3/GML3Degree/GML3.2인 경우에만 영향을 미칩니다.)
   기본값은 YES입니다.
   NO로 설정하면, 각 객체에 <gml:boundedBy> 요소를 작성하지 않을 것입니다.

-  **SPACE_INDENTATION=YES/NO**:
   기본값은 YES입니다.
   YES로 설정하면, 산출물의 가독성을 높이기 위해 더 많은 공백을 사용할 것이지만 파일 용량이 더 커질 것입니다.

-  **GML_ID=string**: (GML 3.2인 경우에만 영향을 미칩니다.)
   객체 집합 gml:id의 값입니다. 기본값은 "aFeatureCollection"입니다.

-  **NAME=string**:
   GML name 요소의 내용입니다. 데이터셋의 NAME 메타데이터 항목으로도 설정할 수 있습니다.

-  **DESCRIPTION=string**:
   GML description 요소의 내용입니다. 데이터셋의 DESCRIPTION 메타데이터 항목으로도 설정할 수 있습니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API이 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다. 이 경우 (.xsd 파일이 아니라) 표준 출력(standard output)에 GML 파일의 콘텐츠만 작성할 것이라는 사실을 기억하십시오. <boundedBy> 요소는 작성하지 않을 것입니다. /vsigzip/ 에 작성할 때도 마찬가지입니다.

.gfs 파일의 문법 예시
------------------------------

다음과 같은 test.gml 파일과

.. code-block:: XML

   <?xml version="1.0" encoding="UTF-8"?>
   <gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml">
     <gml:featureMember>
       <LAYER>
         <attrib1>attrib1_value</attrib1>
         <attrib2container>
           <attrib2>attrib2_value</attrib2>
         </attrib2container>
         <location1container>
           <location1>
               <gml:Point><gml:coordinates>3,50</gml:coordinates></gml:Point>
           </location1>
         </location1container>
         <location2>
           <gml:Point><gml:coordinates>2,49</gml:coordinates></gml:Point>
         </location2>
       </LAYER>
     </gml:featureMember>
   </gml:FeatureCollection>

관련 .gfs 파일이 있다고 할 때:

.. code-block:: XML

   <GMLFeatureClassList>
     <GMLFeatureClass>
       <Name>LAYER</Name>
       <ElementPath>LAYER</ElementPath>
       <GeometryElementPath>location1container|location1</GeometryElementPath>
       <PropertyDefn>
         <Name>attrib1</Name>
         <ElementPath>attrib1</ElementPath>
         <Type>String</Type>
         <Width>13</Width>
       </PropertyDefn>
       <PropertyDefn>
         <Name>attrib2</Name>
         <ElementPath>attrib2container|attrib2</ElementPath>
         <Type>String</Type>
         <Width>13</Width>
       </PropertyDefn>
     </GMLFeatureClass>
   </GMLFeatureClassList>

Note the presence of the '|' character in the <ElementPath> and
<GeometryElementPath> elements to specify the wished field/geometry
element that is a nested XML element. Nested field elements are supported,
as well as specifying <GeometryElementPath> If
GeometryElementPath is not specified, the GML driver will use the last
recognized geometry element.

The <GeometryType> element can be specified to force the geometry type.
Accepted values are : 0 (any geometry type), 1 (point), 2 (linestring),
3 (polygon), 4 (multipoint), 5 (multilinestring), 6 (multipolygon), 7
(geometrycollection).

The <GeometryElementPath> and <GeometryType> can
be specified as many times as there are geometry fields in the GML file.
Another possibility is to define a <GeomPropertyDefn>element as many
times as necessary:

.. code-block:: XML

   <GMLFeatureClassList>
     <GMLFeatureClass>
       <Name>LAYER</Name>
       <ElementPath>LAYER</ElementPath>
       <GeomPropertyDefn>
           <Name>geometry</Name> <!-- OGR geometry name -->
           <ElementPath>geometry</ElementPath> <!-- XML element name possibly with '|' to specify the path -->
           <Type>MultiPolygon</Type>
       </GeomPropertyDefn>
       <GeomPropertyDefn>
           <Name>referencePoint</Name>
           <ElementPath>referencePoint</ElementPath>
           <Type>Point</Type>
       </GeomPropertyDefn>
     </GMLFeatureClass>
   </GMLFeatureClassList>

The output of *ogrinfo test.gml -ro -al* is:

::

   Layer name: LAYER
   Geometry: Unknown (any)
   Feature Count: 1
   Extent: (3.000000, 50.000000) - (3.000000, 50.000000)
   Layer SRS WKT:
   (unknown)
   Geometry Column = location1container|location1
   attrib1: String (13.0)
   attrib2: String (13.0)
   OGRFeature(LAYER):0
     attrib1 (String) = attrib1_value
     attrib2 (String) = attrib2_value
     POINT (3 50)

고급 .gfs 문법
--------------------

Specifying ElementPath to find objects embedded into top level objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider the following test.gml file :

.. code-block:: XML

   <?xml version="1.0" encoding="utf-8"?>
   <gml:FeatureCollection xmlns:xlink="http://www.w3.org/1999/xlink"
                          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                          gml:id="foo" xmlns:gml="http://www.opengis.net/gml/3.2">
     <gml:featureMember>
       <TopLevelObject gml:id="TopLevelObject.1">
         <content>
           <Object gml:id="Object.1">
             <geometry>
               <gml:Polygon gml:id="Object.1.Geometry" srsName="urn:ogc:def:crs:EPSG::4326">
                 <gml:exterior>
                   <gml:LinearRing>
                     <gml:posList srsDimension="2">48 2 49 2 49 3 48 3 48 2</gml:posList>
                   </gml:LinearRing>
                 </gml:exterior>
               </gml:Polygon>
             </geometry>
             <foo>bar</foo>
           </Object>
         </content>
         <content>
           <Object gml:id="Object.2">
             <geometry>
               <gml:Polygon gml:id="Object.2.Geometry" srsName="urn:ogc:def:crs:EPSG::4326">
                 <gml:exterior>
                   <gml:LinearRing>
                     <gml:posList srsDimension="2">-48 2 -49 2 -49 3 -48 3 -48 2</gml:posList>
                   </gml:LinearRing>
                 </gml:exterior>
               </gml:Polygon>
             </geometry>
             <foo>baz</foo>
           </Object>
         </content>
       </TopLevelObject>
     </gml:featureMember>
   </gml:FeatureCollection>

By default, only the TopLevelObject object would be reported and it
would only use the second geometry. This is not the desired behavior in
that instance. You can edit the generated .gfs and modify it like the
following in order to specify a full path to the element (top level XML
element being omitted) :

.. code-block:: XML

   <GMLFeatureClassList>
     <GMLFeatureClass>
       <Name>Object</Name>
       <ElementPath>featureMember|TopLevelObject|content|Object</ElementPath>
       <GeometryType>3</GeometryType>
       <PropertyDefn>
         <Name>foo</Name>
         <ElementPath>foo</ElementPath>
         <Type>String</Type>
       </PropertyDefn>
     </GMLFeatureClass>
   </GMLFeatureClassList>

Getting XML attributes as OGR fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The element@attribute syntax can be used in the <ElementPath> to specify
that the value of attribute 'attribute' of element 'element' must be
fetched.

Let's consider the following test.gml file :

.. code-block:: XML

   <?xml version="1.0" encoding="UTF-8"?>
   <gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml">
     <gml:featureMember>
       <LAYER>
         <length unit="m">5</length>
       </LAYER>
     </gml:featureMember>
   </gml:FeatureCollection>

and the following associated .gfs file.

.. code-block:: XML

   <GMLFeatureClassList>
     <GMLFeatureClass>
       <Name>LAYER</Name>
       <ElementPath>LAYER</ElementPath>
       <GeometryType>100</GeometryType> <!-- no geometry -->
       <PropertyDefn>
         <Name>length</Name>
         <ElementPath>length</ElementPath>
         <Type>Real</Type>
       </PropertyDefn>
       <PropertyDefn>
         <Name>length_unit</Name>
         <ElementPath>length@unit</ElementPath>
         <Type>String</Type>
       </PropertyDefn>
     </GMLFeatureClass>
   </GMLFeatureClassList>

The output of *ogrinfo test.gml -ro -al* is:

::

   Layer name: LAYER
   Geometry: None
   Feature Count: 1
   Layer SRS WKT:
   (unknown)
   gml_id: String (0.0)
   length: Real (0.0)
   length_unit: String (0.0)
   OGRFeature(LAYER):0
     gml_id (String) = (null)
     length (Real) = 5
     length_unit (String) = m

Using conditions on XML attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A <Condition> element can be specified as a child element of a
<PropertyDefn>. The content of the Condition follows a minimalistic
XPath syntax. It must be of the form @attrname[=|!=]'attrvalue' [and|or
other_cond]*. Note that 'and' and 'or' operators cannot be mixed (their
precedence is not taken into account).

Several <PropertyDefn> can be defined with the same <ElementPath>, but
with <Condition> that must be mutually exclusive.

Let's consider the following testcondition.gml file :

.. code-block:: XML

   <?xml version="1.0" encoding="utf-8" ?>
   <ogr:FeatureCollection
        xmlns:ogr="http://ogr.maptools.org/"
        xmlns:gml="http://www.opengis.net/gml">
     <gml:featureMember>
       <ogr:testcondition fid="testcondition.0">
         <ogr:name lang="en">English name</ogr:name>
         <ogr:name lang="fr">Nom francais</ogr:name>
         <ogr:name lang="de">Deutsche name</ogr:name>
       </ogr:testcondition>
     </gml:featureMember>
   </ogr:FeatureCollection>

and the following associated .gfs file.

.. code-block:: XML

   <GMLFeatureClassList>
     <GMLFeatureClass>
       <Name>testcondition</Name>
       <ElementPath>testcondition</ElementPath>
       <GeometryType>100</GeometryType>
       <PropertyDefn>
         <Name>name_en</Name>
         <ElementPath>name</ElementPath>
         <Condition>@lang='en'</Condition>
         <Type>String</Type>
       </PropertyDefn>
       <PropertyDefn>
         <Name>name_fr</Name>
         <ElementPath>name</ElementPath>
         <Condition>@lang='fr'</Condition>
         <Type>String</Type>
       </PropertyDefn>
       <PropertyDefn>
         <Name>name_others_lang</Name>
         <ElementPath>name@lang</ElementPath>
         <Condition>@lang!='en' and @lang!='fr'</Condition>
         <Type>StringList</Type>
       </PropertyDefn>
       <PropertyDefn>
         <Name>name_others</Name>
         <ElementPath>name</ElementPath>
         <Condition>@lang!='en' and @lang!='fr'</Condition>
         <Type>StringList</Type>
       </PropertyDefn>
     </GMLFeatureClass>
   </GMLFeatureClassList>

The output of *ogrinfo testcondition.gml -ro -al* is:

::

   Layer name: testcondition
   Geometry: None
   Feature Count: 1
   Layer SRS WKT:
   (unknown)
   fid: String (0.0)
   name_en: String (0.0)
   name_fr: String (0.0)
   name_others_lang: StringList (0.0)
   name_others: StringList (0.0)
   OGRFeature(testcondition):0
     fid (String) = testcondition.0
     name_en (String) = English name
     name_fr (String) = Nom francais
     name_others_lang (StringList) = (1:de)
     name_others (StringList) = (1:Deutsche name)

Registry for GML application schemas
------------------------------------

The "data" directory of the GDAL installation contains a
"gml_registry.xml" file that links feature types of GML application
schemas to .xsd or .gfs files that contain their definition. This is
used in case no valid .gfs or .xsd file is found next to the GML file.

An alternate location for the registry file can be defined by setting
its full pathname to the GML_REGISTRY 환경설정 옵션.

An example of such a file is :

.. code-block:: XML

   <gml_registry>
       <!-- Finnish National Land Survey cadastral data -->
       <namespace prefix="ktjkiiwfs" uri="http://xml.nls.fi/ktjkiiwfs/2010/02" useGlobalSRSName="true">
           <featureType elementName="KiinteistorajanSijaintitiedot"
                    schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/KiinteistorajanSijaintitiedot.xsd"/>
           <featureType elementName="PalstanTunnuspisteenSijaintitiedot"
                    schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/palstanTunnuspisteenSijaintitiedot.xsd"/>
           <featureType elementName="RekisteriyksikonTietoja"
                    schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/RekisteriyksikonTietoja.xsd"/>
           <featureType elementName="PalstanTietoja"
                    schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/PalstanTietoja.xsd"/>
       </namespace>

       <!-- Inspire CadastralParcels schema -->
       <namespace prefix="cp" uri="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" useGlobalSRSName="true">
           <featureType elementName="BasicPropertyUnit"
                        gfsSchemaLocation="inspire_cp_BasicPropertyUnit.gfs"/>
           <featureType elementName="CadastralBoundary"
                        gfsSchemaLocation="inspire_cp_CadastralBoundary.gfs"/>
           <featureType elementName="CadastralParcel"
                        gfsSchemaLocation="inspire_cp_CadastralParcel.gfs"/>
           <featureType elementName="CadastralZoning"
                        gfsSchemaLocation="inspire_cp_CadastralZoning.gfs"/>
       </namespace>

       <!-- Czech RUIAN (VFR) schema (v1) -->
       <namespace prefix="vf"
                  uri="urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1 ../ruian/xsd/vymenny_format/VymennyFormatTypy.xsd"
                  useGlobalSRSName="true">
           <featureType elementName="TypSouboru"
                        elementValue="OB"
                        gfsSchemaLocation="ruian_vf_ob_v1.gfs"/>
           <featureType elementName="TypSouboru"
                        elementValue="ST"
                        gfsSchemaLocation="ruian_vf_st_v1.gfs"/>
       </namespace>
   </gml_registry>

XML schema definition (.xsd) files are pointed by the schemaLocation
attribute, whereas OGR .gfs files are pointed by the gfsSchemaLocation
attribute. In both cases, the filename can be a URL (http://, https://),
an absolute filename, or a relative filename (relative to the location
of gml_registry.xml).

The schema is used if and only if the namespace prefix and URI are found
in the first bytes of the GML file (e.g.
*xmlns:ktjkiiwfs="http://xml.nls.fi/ktjkiiwfs/2010/02"*), and that the
feature type is also detected in the first bytes of the GML file (e.g.
*ktjkiiwfs:KiinteistorajanSijaintitiedot*). If the element value is
defined than the schema is used only if the feature type together with
the value is found in the first bytes of the GML file (e.g.
*vf:TypSouboru>OB_UKSH*).

Building junction tables
------------------------

The
`ogr_build_junction_table.py <https://github.com/OSGeo/gdal/blob/master/swig/python/gdal-utils/osgeo_utils/samples/ogr_build_junction_table.py>`_
script can be used to build a `junction
table <http://en.wikipedia.org/wiki/Junction_table>`_ from OGR layers
that contain "XXXX_href" fields. Let's considering the following output
of a GML file with links to other features :

::

   OGRFeature(myFeature):1
     gml_id (String) = myFeature.1
     [...]
     otherFeature_href (StringList) = (2:#otherFeature.10,#otherFeature.20)

   OGRFeature(myFeature):2
     gml_id (String) = myFeature.2
     [...]
     otherFeature_href (StringList) = (2:#otherFeature.30,#otherFeature.10)

After running

::

   ogr2ogr -f PG PG:dbname=mydb my.gml

to import it into PostGIS and

::

   python ogr_build_junction_table.py PG:dbname=mydb

, a *myfeature_otherfeature* table will be created and will contain the
following content :

.. list-table:: myfeature_otherfeature Table
   :header-rows: 1

   * - myfeature_gml_id
     - otherfeature_gml_id
   * - myFeature.1
     - otherFeature.10
   * - myFeature.1
     - otherFeature.20
   * - myFeature.2
     - otherFeature.30
   * - myFeature.2
     - otherFeature.10

Reading datasets resulting from a WFS 2.0 join queries
------------------------------------------------------

The GML driver can read datasets resulting from a WFS 2.0 join queries.

Such datasets typically look like:

.. code-block:: XML


   <wfs:FeatureCollection xmlns:xs="http://www.w3.org/2001/XMLSchema"
       xmlns:app="http://app.com"
       xmlns:wfs="http://www.opengis.net/wfs/2.0"
       xmlns:gml="http://www.opengis.net/gml/3.2"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       numberMatched="unknown" numberReturned="2" timeStamp="2015-01-01T00:00:00.000Z"
       xsi:schemaLocation="http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd
                           http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd">
     <wfs:member>
       <wfs:Tuple>
         <wfs:member>
           <app:table1 gml:id="table1-1">
             <app:foo>1</app:foo>
           </app:table1>
         </wfs:member>
         <wfs:member>
           <app:table2 gml:id="table2-1">
             <app:bar>2</app:bar>
             <app:baz>foo</app:baz>
             <app:geometry><gml:Point gml:id="table2-2.geom.0"><gml:pos>2 49</gml:pos></gml:Point></app:geometry>
           </app:table2>
         </wfs:member>
       </wfs:Tuple>
     </wfs:member>
     <wfs:member>
       <wfs:Tuple>
         <wfs:member>
           <app:table1 gml:id="table1-2">
             <app:bar>2</app:bar>
             <app:geometry><gml:Point gml:id="table1-1.geom.0"><gml:pos>3 50</gml:pos></gml:Point></app:geometry>
           </app:table1>
         </wfs:member>
         <wfs:member>
           <app:table2 gml:id="table2-2">
             <app:bar>2</app:bar>
             <app:baz>bar</app:baz>
             <app:geometry><gml:Point gml:id="table2-2.geom.0"><gml:pos>2 50</gml:pos></gml:Point></app:geometry>
           </app:table2>
         </wfs:member>
       </wfs:Tuple>
     </wfs:member>
   </wfs:FeatureCollection>

OGR will group together the attributes from the layers participating to
the join and will prefix them with the layer name. So the above example
will be read as the following:

::

   OGRFeature(join_table1_table2):0
     table1.gml_id (String) = table1-1
     table1.foo (Integer) = 1
     table1.bar (Integer) = (null)
     table2.gml_id (String) = table2-1
     table2.bar (Integer) = 2
     table2.baz (String) = foo
     table2.geometry = POINT (2 49)

   OGRFeature(join_table1_table2):1
     table1.gml_id (String) = table1-2
     table1.foo (Integer) = (null)
     table1.bar (Integer) = 2
     table2.gml_id (String) = table2-2
     table2.bar (Integer) = 2
     table2.baz (String) = bar
     table1.geometry = POINT (3 50)
     table2.geometry = POINT (2 50)

예시
--------

ogr2ogr 유틸리티를 이용해서 GML에 대한 오라클 쿼리의 결과물을 덤프하기:

::

   ogr2ogr -f GML output.gml OCI:usr/pwd@db my_feature -where "id = 0"

ogr2ogr 유틸리티를 이용해서 GML에 대한 PostGIS 쿼리의 결과물을 덤프하기:

::

   ogr2ogr -f GML output.gml PG:'host=myserver dbname=warmerda' -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

참고
--------

-  `GML 사양 <http://www.opengeospatial.org/standards/gml>`_

-  `GML 3.1.1 단순 피처 프로파일 - OGC(R) 06-049r1 <http://portal.opengeospatial.org/files/?artifact_id=15201>`_

-  `GML 3.2.1 단순 피처 프로파일 (정오표 포함) - OGC(R) 10-100r3 <https://portal.opengeospatial.org/files/?artifact_id=42729>`_

-  `Xerces <http://xml.apache.org/xerces2-j/index.html>`_

-  :ref:`GMLAS - 응용 프로그램 스키마 주도 GML <vector.gmlas>` 드라이버

-  :ref:`NAS/ALKIS : 독일 지적도에 특화된 GML <vector.nas>` 드라이버

감사의 말
---------

-  A. 푸리에리(A. Furieri)가 이탈리아 토스카나 주의 재정 지원을 받아 **GML_SKIP_RESOLVE_ELEMS HUGE** 를 구현했습니다.

-  핀란드 농림부의 티케(Tike) 정보 센터의 재정 지원을 받아 핀란드 국토조사원 GML 및 Inspire GML 포맷 지적 데이터를 지원하게 되었습니다.

