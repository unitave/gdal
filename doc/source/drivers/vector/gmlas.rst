.. _vector.gmlas:

GMLAS - 응용 프로그램 스키마 주도 GML
=====================================================================

.. versionadded:: 2.2

.. shortname:: GMLAS

.. build_dependencies:: Xerces

GMLAS(GML driven by Application Schemas) 드라이버는 이른바 복잡 피처(Complex Feature)를 담고 있는 파일을 포함하는 임의 구조의 XML 파일을 읽고 쓸 수 있습니다. 이때 XML 파일 콘텐츠의 구조를 설명하는 XML 스키마 하나 또는 여러 개가 해당 파일 위치에 함께 있어야 합니다.
이 드라이버가 모든 XML 스키마에 포괄적이긴 하지만, 주 목표는 GML(Geography Markup Language) 이름공간을 직접 또는 간접적으로 참조하는 문서를 읽고 쓸 수 있도록 하는 것입니다.

이 드라이버는 아파치 Xerces-C 3.1 이상 버전을 필요로 합니다.

이 드라이버는 스트리밍 모드로 작동하기 때문에 그다지 많지 않은 RAM 사용량으로 임의 용량의 파일을 처리할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

열기 문법
--------------

연결 문자열은 다음과 같습니다:

::

   GMLAS:/path/to/the.gml

"GMLAS:" 접두어를 기억하십시오. 이 접두어를 생략하면, 아마도 GML 드라이버를 사용할 것입니다.

"GMLAS:"만 연결 문자열로 사용할 수도 있지만, 그 경우 반드시 XSD 열기 옵션으로 스키마를 명확하게 지정해줘야만 합니다.

XML 구조를 OGR 레이어 및 필드로 매핑하기
-------------------------------------------------

이 드라이버는 OGR 레이어 및 필드를 작성하기 위해 XML/GML이 참조하는 XML 스키마를 스캔합니다. 직접 또는 간접적으로 사용되는 스키마가 완전하게 무결할 것을 엄격하게 요구합니다. XML/GML 파일 자체의 내용은 미미하게, 주로 도형 열의 공간 좌표계를 판단하기 위해 사용됩니다.

일반적으로 스키마의 최상위 수준에서 선언되는 XML 요소를 OGR 레이어로 노출시킬 것입니다. 단순 XML 유형의 (문자열, 정수형, 실수형 등등의) 최상위 수준 XML 요소의 속성 및 하위 요소를 OGR 필드로 노출시킬 것입니다. 하위 요소가 복잡 유형인 경우 다른 습성을 보일 수 있습니다. 하위 요소의 집합원 개수(cardinality)가 최대 1개이고 다른 요소들이 참조하지 않는 경우, 해당 상위 요소로 "평탄화(flatten)" 됩니다. 그렇지 않다면 OGR 레이어로 노출시킬 것입니다. 이때 하위 요소가 그 상위 요소에 특화된 경우라면 해당 하위 요소의 "상위" 레이어를 가리키는 링크를 가진 OGR 레이어로, 또는 여러 상위 요소들이 해당 하위 요소를 공유하는 경우라면 연결 테이블(junction table)을 통해 OGR 레이어로 노출시킬 것입니다.

이 드라이버는 기본적으로 스키마를 엄격하게 준수하지 않는 문서에 강합니다. 문서에 있는 예상 외의 콘텐츠는 물론, 문서에 스키마가 필수로 요구하는 콘텐츠가 없는 경우에도 조용히 무시할 것입니다.

더 자세한 내용은 :ref:`GMLAS 매핑 예시 <gmlas_mapping_examples>` 페이지를 읽어보십시오.

기본적으로 환경설정에서, SWE(Sensor Web Enablement) 공통 데이터 모델 이름공간으로부터 나온 swe:DataRecord 및 swe:DataArray 요소를 OGR 개념에 더 자연스럽게 매핑되도록 특수 처리할 것입니다. swe:DataArray의 "swe:field" 요소를 OGR 필드로 매핑하고, "swe:values" 요소는 각 swe:DataArray 전용 레이어에 OGR 객체로 파싱할 것입니다.
이런 편의적인 노출은 읽기전용 목적을 위해서라는 사실을 기억하십시오. 이 드라이버의 작성기를 사용하는 경우 일반적인 매핑 메커니즘의 콘텐츠만 사용할 것입니다.

메타데이터 레이어
---------------

"_ogr_fields_metadata", "_ogr_layers_metadata", "_ogr_layer_relationships" 특수 레이어 3개와 "_ogr_other_metadata" 레이어가 OGR 레이어 및 필드 상의 OGR 데이터 모델로부터 가져올 수 있는 기본 정보에 추가 정보를 추가합니다.

EXPOSE_METADATA_LAYERS 열기 옵션을 YES로 설정한 경우 (또는 환경설정에서 활성화한 경우) 이 레이어들을 노출시킵니다. GetLayerByName() 호출에 또는 또는 ogrinfo 및 ogr2ogr 유틸리티에 레이어 이름을 지정하면 개별적으로 가져올 수도 있습니다.

더 자세한 내용은 :ref:`GMLAS 메타데이터 레이어 <gmlas_metadata_layers>` 페이지를 읽어보십시오.

환경설정 파일
------------------

GDAL 설치본의 데이터 디렉터리에 `gmlasconf.xml <http://github.com/OSGeo/gdal/blob/master/data/gmlasconf.xml>`_ 기본 환경설정 파일이 존재합니다. 이 파일의 구조 및 내용은 `gmlasconf.xsd <http://github.com/OSGeo/gdal/blob/master/data/gmlasconf.xsd>`_ 스키마에 문서화되어 있습니다.

사용자가 이 환경설정 파일을 통해 다음 설정들을 수정할 수 있습니다:

-  원격 스키마를 다운로드해야 하는지 여부. 기본적으로 활성화됩니다.

-  스키마의 로컬 캐시를 활성화할지 여부. 기본적으로 활성화됩니다.

-  로컬 캐시의 경로. 기본값은 "$HOME/.gdal/gmlas_xsd_cache" 입니다.

-  스키마를 기준으로 문서를 검증해야 할지 여부. 기본적으로 비활성화됩니다.

-  검증 오류 발생 시 데이터셋 열기를 중단해야 할지 여부. 기본적으로 비활성화됩니다.

-  기본적으로 메타데이터 레이어를 노출시켜야 할지 여부. 기본적으로 비활성화됩니다.

-  'ogr_pkid' 필드를 항상 생성해야 할지 여부. 기본적으로 비활성화됩니다. 이 설정을 활성화시키면 여러 문서 사이에서 ID의 유일성이 보장되지 않는 ID 속성을 가지고 있는 레이어에 유용할 수 있습니다. 즉 문서 여러 개를 대상 데이터베이스 테이블에 추가하는 경우 문제가 발생할 수도 있습니다.

-  XML 문서에서 사용되지 않는 레이어 및 필드를 제거해야 할지 여부. 기본적으로 비활성화됩니다.

-  OGR 배열 데이터 유형을 사용할 수 있는지 여부. 기본적으로 활성화됩니다.

-  GML 도형의 XML 정의를 OGR 문자열 필드로 리포트해야 할지 여부. 기본적으로 비활성화됩니다.

-  스키마에 있는 요소 가운데 최소한 1개가 gml:_Feature 또는 gml:AbstractFeature로부터 파생된 경우, 스키마 작성 작업의 초기 패스(initial pass)에서 gml:_Feature 또는 gml:AbstractFeature로부터 파생된 XML 요소만 고려해야 할지 여부. 기본적으로 활성화됩니다.

-  xlink:href를 분해할지 여부 및 어떻게 분해해야 할지에 관한 몇 가지 규칙들.

-  OGR 레이어 및 필드 개수를 줄일 수 있도록 무시해야만 하는 요소 및 속성의 XPaths 정의.

이 환경설정 파일을 수정할 수 있고, CONFIG_FILE 열기 옵션으로 수정 버전을 드라이버에 지정할 수 있습니다. 환경설정 파일의 모든 요소들은 필수가 아닙니다. 요소가 없을 경우, 스키마 문서에 나타난 기본값을 사용합니다.

다른 열기 옵션들을 통해서도 환경설정을 지정할 수 있습니다. 몇몇 열기 옵션은 환경설정 파일에 있는 설정과 동일한 이름을 가지고 있다는 사실을 기억하십시오. 이런 열기 옵션을 지정하는 경우, 해당 옵션의 값이 (기본 환경설정 파일이든, CONFIG_FILE 열기 옵션으로 지정한 파일이든) 환경설정 파일의 값을 대체할 것입니다.

도형 지원
----------------

XML 스키마는 도형 유형만 나타낼 뿐 공간 좌표계를 제약하지는 않습니다. 따라서 이론적으로는 동일한 도형 필드에 서로 다른 공간 좌표계를 가진 동일 클래스의 객체 인스턴스들이 존재할 수도 있습니다. 이런 데이터를 처리할 수는 없기 때문에, 도형 필드를 탐지했을 때 srsName이 명확하게 설정된 각 도형 필드의 첫 번째 도형을 찾기 위해 문서를 초기 스캔합니다. 이 첫 번째 도형이 각 도형 필드 전체를 대표할 것입니다. 같은 필드에 다른 공간 좌표계를 가진 도형이 있는 경우, 재투영할 것입니다.

기본적으로 OGR 객체에 GML 도형으로부터 작성된 OGR 도형만 노출시킵니다. 환경설정 파일의 IncludeGeometryXML 설정을 참으로 변경하면 GML 도형의 XML 정의를 가진 OGR 문자열 필드를 노출시킬 수 있습니다.

대용량 다중 레이어 GML 파일의 성능 문제점
----------------------------------------------------

일반적으로 OGR 데이터소스를 읽으려면, GDALDataset::GetLayer() 메소드로 레이어 요청을 반복하고 각 레이어에 OGRLayer::GetNextFeature() 메소드로 객체 요청을 반복합니다. GMLAS 드라이버도 이런 접근법을 사용할 수 있기는 하지만, 대용량 문서 또는 수많은 OGR 레이어로 변환되는 복잡 스키마를 사용하는 문서의 경우 성능이 크게 저하될 수도 있습니다.

따라서 .gml/.xml 파일에 객체가 나타날 때마다 즉시 GDALDataset::GetNextFeature() 메소드로 객체 요청을 반복할 것을 권장합니다. 이 경우 객체가 내포 요소들을 포함하고 있다면 비순차적(non-sequential) 레이어로부터 객체를 반환할 수도 있습니다.

열기 옵션
------------

-  **XSD=filename(s)**:
   사용할 XSD 응용 프로그램 스키마를 (또는 쉼표로 구분된 파일명 목록을) 지정합니다. "http://" 또는 "https://" URL을 사용할 수 있습니다. XML/GML 문서가 문서 루트 요소에 무결한 링크를 가진 schemaLocation 속성을 가지고 있는 경우 이 옵션은 필수가 아닙니다.

-  **CONFIG_FILE=filename or inline XML definition**:
   XML 환경설정 파일의 파일명 또는 그때 그때 즉시 처리되는 XML 정의를 지정합니다. 파일명은 `gmlasconf.xsd <https://github.com/OSGeo/gdal/blob/master/data/gmlasconf.xsd>`_ 스키마를 준수합니다. XML 콘텐츠가 "<Configuration>"으로 시작하는 경우 XML 콘텐츠를 직접 그때 그때 즉시 처리해서 지정할 수도 있습니다.

-  **EXPOSE_METADATA_LAYERS=YES/NO**:
   "_ogr_fields_metadata", "_ogr_layers_metadata", "_ogr_layer_relationships" 및 "ogr_other_metadata" 메타데이터 레이어를 기본적으로 리포트해야 할지 여부를 선택합니다. 기본값은 NO입니다.

-  **VALIDATE=YES/NO**:
   스키마를 기준으로 문서를 검증해야 할지 여부를 선택합니다. 검증은 데이터셋을 열 때 이루어집니다. 기본값은 NO입니다.

-  **FAIL_IF_VALIDATION_ERROR=YES/NO**:
   검증 오류 발생 시 데이터셋 열기를 중단해야 할지 여부를 선택합니다. (VALIDATE=YES인 경우에만 사용할 수 있습니다.) 기본값은 NO입니다.

-  **REFRESH_CACHE=YES/NO**:
   xlink:href 링크가 가리키는 원격 스키마 및 문서가 이미 로컬 캐시에 존재하더라도 서버로부터 다운로드해야 할지 여부를 선택합니다. 캐시가 활성화된 경우, 새로 다운로드한 리소스로 새로고침될 것입니다. 기본값은 NO입니다.

-  **SWAP_COORDINATES=AUTO/YES/NO**:
   x/y 또는 경도/위도 좌표 순서를 뒤바꿔야 할지 여부를 선택합니다.
   AUTO 모드에서는, 드라이버가 순서를 바꿔야만 하는지를 srsName으로부터 판단할 것입니다. srsName이 urn:ogc:def:crs:EPSG::XXXX 형식이고 EPSG 데이터베이스에 있는 해당 공간 좌표계의 좌표 순서가 위도,경도 또는 편북,편동인 경우 드라이버가 GIS 친화적인 순서로 (경도,위도 또는 편동,편북으로) 바꿀 것입니다. 공간 좌표계의 형식이 (EPSG:XXXX와 같이) 다를 경우, GIS 친화적인 순서를 가정하기 때문에 순서를 뒤바꾸지 않습니다.
   이 옵션을 YES로 설정하면 GML에 나타나는 좌표 순서와 상관없이 항상 순서를 뒤바꿀 것입니다.
   NO로 설정하면 동일한 순서를 유지할 것입니다.
   기본값은 AUTO입니다.

-  **REMOVE_UNUSED_LAYERS=YES/NO**:
   리포트된 레이어들에서 사용되지 않는 레이어를 제거할지 여부를 선택합니다. 기본값은 NO입니다.

-  **REMOVE_UNUSED_FIELDS=YES/NO**:
   리포트된 레이어들에서 사용되지 않는 필드를 제거할지 여부를 선택합니다. 기본값은 NO입니다.

-  **HANDLE_MULTIPLE_IMPORTS=YES/NO**:
   이름공간은 동일하지만 스키마가 다른 데이터셋들의 다중 가져오기를 허용할지 여부를 선택합니다. 기본값은 NO입니다.

-  **SCHEMA_FULL_CHECKING=YES/NO**:
   XSD 확인을 -- 예를 들면 주 문서에서 스키마의 무결하지 않은 부분을 참조하지는 않았는지 -- 엄격하게 할지 또는 여유를 둘지 여부를 선택합니다. 기본값은 NO입니다.

생성 지원
----------------

GMLAS 드라이버는 (CreateLayer() 및 CreateFeature() 인터페이스를 구현해서 읽기를 지원하는 대부분의 다른 드라이버와는 반대로) 소스 데이터셋을 변환해서 스키마 주도 방식으로 XML 문서를 작성할 수 있습니다.
전형적인 워크플로(workflow)는 GMLAS 드라이버의 판독기를 이용해서 SQLite/Spatialite/PostGIS 데이터베이스를 생성하는 것입니다. 이때 가져온 객체를 수정한 다음 이 데이터베이스를 새 XML 문서로 다시 내보낼 수도 있습니다.

이 드라이버는 소스 데이터셋의 "최상위" 레이어를 식별하고, 해당 레이어에서 다른 최상위 레이어들이 참조하지 않는 객체를 구분할 것입니다. 산출 XML의 생성이 스키마 주도이기 때문에, 스키마를 사용할 수 있어야 합니다. 다음 두 가지 방법으로 스키마를 사용할 수 있습니다:

-  소스 .xml 파일을 변환할 때 EXPOSE_METADATA_LAYERS 열기 옵션을 YES로 설정해서 소스 데이터셋에 스키마를 처리한 결과물을 \_ogr_\* 메타데이터 테이블 4개로 저장하거나 또는,

-  생성 작업 시 INPUT_XSD 생성 옵션으로 스키마를 지정할 수 있습니다.

이 드라이버는 기본적으로 WFS 2.0 wfs:FeatureCollection / wfs:member 요소 안에 객체들을 "묶을(wrap)" 것입니다. 드라이버에 그 대신 ogr_gmlas:FeatureCollection / ogr_gmlas:featureMember XML 요소를 선언하는 사용자 지정 "묶음" .xsd 파일을 생성하도록 요청할 수도 있습니다.

내보내기로부터 산출되는 파일이 무결한 XML이어야 하는 반면, 해당 파일이 XML 스키마(들)에 표현된 추가적인 제약 사항들을 기준으로 검증될 것이라는 보증은 없다는 사실을 기억하십시오. 검증 성공 여부는 객체 콘텐츠에 따라 달라질 것입니다. (예를 들어 스키마를 준수하지 않는 GML 파일을 변환하는 경우 드라이버의 산출물은 일반적으로 검증되지 않을 것입니다.)

입력 레이어가 "_xml" 접미어가 이름 뒤에 붙은 필드에 GML 콘텐츠로 저장된 도형을 가지고 있다면, 이 드라이버는 해당 XML 콘텐츠로부터 작성된 OGR 도형과 객체의 전용 도형 필드에 저장된 OGR 도형을 비교할 것입니다. 두 도형이 일치하는 경우, 초기 GML 콘텐츠의 특성들을 보전하기 위해 "_xml" 접미어가 붙은 필드에 저장된 GML 콘텐츠를 사용할 것입니다.

대용량 데이터베이스 상에서 내보내기 성능을 향상시키려면, "_ogr_layers_metadata" 메타데이터 레이어의 "layer_pkid_name" 속성이 가리키는 필드들에 속성 색인을 생성하는 것이 도움이 될 것입니다.

ogr2ogr 습성
~~~~~~~~~~~~~~~~~

소스 데이터베이스에서 XML/GML으로 변환시키기 위해 ogr2ogr / GDALVectorTranslate()를 이용하는 경우, 사용할 수 있는 옵션에 제약이 있습니다.
ogr2ogr의 다음 옵션들만 지원합니다:

-  데이터셋 생성 옵션 (아래 참조)
-  레이어 이름
-  "-spat" 옵션을 통한 공간 필터
-  "-where" 옵션을 통한 속성 필터

공간 및 속성 필터링은 최상위 레이어에만 영향을 미칩니다. "join"을 통해 선택된 하위 객체는 이 필터들의 영향을 받지 않습니다.

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

다음과 같은 데이터셋 생성 옵션들을 지원합니다:

-  **INPUT_XSD=filename(s)**:
   사용할 XSD 응용 프로그램 스키마를 (또는 쉼표로 구분된 파일명 목록을) 지정합니다. "http://" 또는 "https://" URL을 사용할 수 있습니다. 소스 데이터셋이 스키마 및 위치로 채워진 \_ogr_other_metadata를 가지고 있는 경우 이 옵션은 필수가 아닙니다.

-  **CONFIG_FILE=filename or inline XML definition**:
   XML 환경설정 파일의 파일명 또는 그때 그때 즉시 처리되는 XML 정의를 지정합니다. 파일명은 `gmlasconf.xsd <https://github.com/OSGeo/gdal/blob/master/data/gmlasconf.xsd>`_ 스키마를 준수합니다. XML 콘텐츠가 "<Configuration>"으로 시작하는 경우 XML 콘텐츠를 직접 그때 그때 즉시 처리해서 지정할 수도 있습니다.

-  **LAYERS=layers**:
   최상위 객체로 내보낼, 쉼표로 구분한 레이어 목록입니다. 특수값 "{SPATIAL_LAYERS}"를 사용하면 도형을 가진 모든 레이어들을 지정할 수도 있습니다. 이 옵션을 지정하지 않는 경우 드라이버가 소스 데이터셋의 "최상위" 레이어를 식별하고, 해당 레이어에서 다른 최상위 레이어들이 참조하지 않는 객체를 구분할 것입니다.

-  **SRSNAME_FORMAT=SHORT/OGC_URN/OGC_URL**: (GML 버전 3 산출물 전용)
   기본값은 OGC_URL입니다.
   SHORT로 설정하면, srsName이 AUTHORITY_NAME:AUTHORITY_CODE 형식일 것입니다.
   OGC_URN으로 설정하면, srsName이 urn:ogc:def:crs:AUTHORITY_NAME::AUTHORITY_CODE 형식일 것입니다.
   OGC_URL으로 설정하면, srsName이 http://www.opengis.net/def/crs/AUTHORITY_NAME/0/AUTHORITY_CODE 형식일 것입니다.
   OGC_URN 및 OGC_URL의 경우, 공간 좌표계가 명확한 AXIS 순서를 가지고 있지 않지만 ImportFromEPSGA() 메소드로 가져온 동일한 공간 좌표계 기관 코드를 위도/경도 또는 편북/편동으로 취급해야 한다면, 드라이버가 좌표 순서를 뒤바꿀 것입니다.

-  **INDENT_SIZE=[0-8]**:
   각 들여쓰기 수준의 공백 개수입니다. 기본값은 2입니다.

-  **COMMENT=string**:
   생성된 XML 파일 최상단에 XML 주석으로 추가할 주석 문자열입니다.

-  **LINEFORMAT=CRLF/LF**:
   사용할 새줄 문자 시퀀스를 지정합니다. 기본값은 윈도우의 경우 CRLF 그리고 다른 플랫폼들의 경우 LF입니다.

-  **WRAPPING=WFS2_FEATURECOLLECTION/GMLAS_FEATURECOLLECTION**:
   객체들을 wfs:FeatureCollection으로 묶을지 또는 ogr_gmlas:FeatureCollection으로 묶을지 지정합니다.
   기본값은 WFS2_FEATURECOLLECTION입니다.

-  **TIMESTAMP=XML date time**:
   wfs:FeatureCollection 속성에 사용할 타임 스탬프를 위한 사용자 지정 XML 날짜&시간 유형의 값입니다. 지정하지 않는 경우, 현재 날짜와 시간을 사용합니다. WRAPPING=WFS2_FEATURECOLLECTION인 경우에만 영향을 미칩니다.

-  **WFS20_SCHEMALOCATION=Path or URL to wfs.xsd**:
   WRAPPING=WFS2_FEATURECOLLECTION인 경우에만 영향을 미칩니다.
   기본값은 "http://schemas.opengis.net/wfs/2.0/wfs.xsd" 입니다.

-  **GENERATE_XSD=YES/NO**:
   묶음(wrapping) ogr_gmlas:FeatureCollection / ogr_gmlas:featureMember 요소의 구조를 가지고 있는 .xsd 파일을 생성할지 여부를 선택합니다. WRAPPING=GMLAS_FEATURECOLLECTION인 경우에만 영향을 미칩니다. 기본값은 YES입니다.

-  **OUTPUT_XSD_FILENAME=string**:
   묶음(wrapping) .xsd 파일의 파일명을 지정합니다. 지정하지 않는 경우 산출 파일과 동일한 기본명에 .xsd 확장자를 붙입니다. GENERATE_XSD=NO인 경우에도 이 옵션을 사용할 수 있다는 사실을 기억하십시오. .xml 파일의 schemaLocation 속성에 묶음 .xsd가 나타납니다. WRAPPING=GMLAS_FEATURECOLLECTION인 경우에만 영향을 미칩니다.

예시
--------

-  데이터 파일의 내용을 목록화하기:

::

   ogrinfo -ro GMLAS:my.gml

-  PostGIS로 변환하기:

::

   ogr2ogr -f PostgreSQL PG:'host=myserver dbname=warmerda' GMLAS:my.gml -nlt CONVERT_TO_LINEAR

-  Spatialite로 변환한 다음 다시 GML로 변환하기:

::

   ogr2ogr -f SQLite tmp.sqlite GMLAS:in.gml -dsco SPATILIATE=YES -nlt CONVERT_TO_LINEAR -oo EXPOSE_METADATA_LAYERS=YES
   ogr2ogr -f GMLAS out.gml tmp.sqlite

참고
--------

-  :ref:`GML <vector.gml>`: 스키마는 필수가 아니지만 복잡 객체 지원은 제한되는 범용 드라이버

-  :ref:`NAS/ALKIS <vector.nas>`: 독일 지적도에 특화된 GML 드라이버

감사의 말
-------

이 드라이버는 EU의 코페르니쿠스 지구 관측 프로그램이 유럽환경청에 위임한 사업의 일환으로 재정 지원을 받아 초기 구현되었습니다.

SWE(Sensor Web Enablement) 공통 데이터 모델의 swe:DataRecord 및 swe:DataArray 구조의 특수 처리 과정은 프랑스 지질광물연구소의 재정 지원으로 개발되었습니다.

.. toctree::
   :maxdepth: 1
   :hidden:

   gmlas_mapping_examples
   gmlas_metadata_layers

