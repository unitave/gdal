.. _raster.jp2ecw:

================================================================================
JP2ECW -- ERDAS JPEG2000 (.jp2)
================================================================================

.. shortname:: JP2ECW

.. build_dependencies:: ECW SDK

GDAL은 헥사곤 지오스페이셜(Hexagon Geospatial; 예전의 Intergraph, ERDAS, ERMapper) 사가 개발한 ERDAS ECW/JP2 SDK를 이용해서 JPEG2000 파일 읽기와 쓰기를 지원합니다. 이 지원은 선택 옵션으로 ECW/JP2 SDK 다운로드 페이지에서 사용할 수 있는 라이브러리들과 링크해야 합니다.

좌표계 및 지리참조 변환을 읽어오고, GeoJP2™ (GeoTIFF-in-JPEG2000), ERDAS GML-in-JPEG2000, 그리고 OGC가 개발한 새 GML-in-JPEG2000 사양을 어느 정도 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

사용 허가
---------

여러 사용 허가(license) 유형 아래 ERDAS ECW/JP2 SDK v5.x버전을 사용할 수 있습니다. 데스크톱 사용의 경우, 모든 크기의 ECW/JP2 이미지 디코딩을 무료로 사용할 수 있습니다. 서버 플랫폼에서 배포하기 위해 압축하거나, 또는 모바일 플랫폼 상에서 무제한 크기의 파일을 디코딩하려면 헥사곤 지오스페이셜 사로부터 사용 권한을 구매해야만 합니다.

이력
-------

-  v3.x - 2006년 배포 중지
-  v4.x - 2012년 배포 중지
-  v5.x - 2013년~현재 개발 중

지리참조 작업
--------------

내부(GeoJP2 또는 GMLJP2 경계 상자), 월드 파일 .j2w/.wld 사이드카 파일, 또는 PAM(Persistent Auxiliary metadata) .aux.xml 사이드카 파일 등 서로 다른 소스들로부터 지리참조 정보를 얻을 수 있습니다. 기본적으로 PAM, GeoJP2, GMLJP2, WORLDFILE 순서대로 정보를 수집합니다. (첫 항목을 가장 우선합니다.)

GDAL 2.2버전부터, GDAL_GEOREF_SOURCES 환경설정 옵션으로 (또는 GEOREF_SOURCES 열기 옵션으로) 사용할 수 있는 소스와 그 우선 순위를 변경할 수 있습니다. 이 옵션의 값은 PAM, GEOJP2, GMLJP2, (GEOJP2, GMLJP2로 가는 단축 키인) INTERNAL, WORLDFILE, NONE이라는 키워드를 쉼표로 구분한 목록입니다. 목록의 첫 항목이 가장 우선되는 소스입니다. 목록에 없는 소스는 무시할 것입니다.

예를 들어 이 옵션을 "WORLDFILE,PAM,INTERNAL"로 설정하면 PAM이나 내부 JP2 경계 상자보다 잠재적인 월드 파일의 지리변형 행렬을 우선할 것입니다. "PAM,WORLDFILE,GEOJP2"로 설정하면 설정된 소스를 이용하고 GMLJP2 경계 상자는 무시할 것입니다.

열기 옵션
--------------

다음과 같은 열기 옵션을 사용할 수 있습니다:

-  **1BIT_ALPHA_PROMOTION=YES/NO**:
   1비트 알파 채널을 8비트로 승격시켜야 할지 여부를 선택합니다. 기본값은 YES입니다.

-  **GEOREF_SOURCES=string**:
   (GDAL 2.2 이상 버전) 사용할 수 있는 지리참조 소스와 그 우선 순위를 정의합니다. `지리참조 작업 <#georeferencing>`_ 단락을 참조하십시오.

생성 옵션
-----------------

주의: 사용 권한이 있고 압축된 파일만 대상으로 지정해야 합니다. ECW/JP2 SDK는 입력물의 특성에 따라 모든 다른 옵션들을 권장 설정으로 초기화할 것입니다. 다른 옵션을 변경하면 디코딩 속도 및 다른 JPEG2000 도구들과의 호환성에 *상당한* 영향을 미칠 것입니다.

-  **LARGE_OK=YES**:
   *(v3.x SDK 전용)* EULA 조건에 부합되는 경우 500MB를 초과하는 파일을 압축할 수 있습니다. v4.x부터 퇴출되었고, ECW_ENCODE_KEY와 ECW_ENCODE_COMPANY로 대체되었습니다.

-  **ECW_ENCODE_KEY=key**:
   (v4.x SDK 이상)* 사용 허가된 기가픽셀 제한까지 인코딩 케이퍼빌리티를 활성화하기 위한 OEM 인코딩 키를 입력합니다. 이 키의 길이는 약 129개의 16진법 자릿수입니다. 사용 권한을 구매한 회사와 키가 일치해야만 하며, SDK 버전이 오를 때마다 키를 재생성해야만 합니다. 전체 수준에서 환경설정 옵션으로 입력할 수도 있습니다.

-  **ECW_ENCODE_COMPANY=name**:
   *(v4.x SDK 이상)* 발행된 OEM 키(ECW_ENCODE_KEY 참조)에 있는 회사명을 입력합니다. 사용 권한을 구매한 회사와 키가 일치해야만 하며, SDK 버전이 오를 때마다 키를 재생성해야만 합니다. 전체 수준에서 환경설정 옵션으로 입력할 수도 있습니다.

-  **TARGET=percent**: 대상 용량 감소를 원본의 백분율로 설정합니다. 지정하지 않는 경우 기본값은 75% 감소를 의미하는 75입니다. 0으로 설정하면 비손실 압축을 의미합니다.

-  **PROJ=name**:
   사용할 ECW 투영법 문자열의 이름입니다. 흔히 쓰이는 값으로는 NUTM11 또는 GEODETIC 등이 있습니다.

-  **DATUM=name**:
   사용할 ECW 원점(datum) 문자열의 이름입니다. 흔히 쓰이는 값으로는 WGS84 또는 NAD83 등이 있습니다.

-  **GMLJP2=YES/NO**:
   JPEG2000 사양의 OGC GML을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. GMLJP2V2_DEF를 사용하지 않는 이상, GMLJP2 경계 상자의 버전은 1일 것입니다. 기본값은 YES입니다.

-  **GMLJP2V2_DEF=filename**:
   `OGC GML-in-JPEG2000 버전 2.0 <http://docs.opengeospatial.org/is/08-085r4/08-085r4.html>`_ 사양을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. *filename* 이 GMLJP2 v2 경계 상자를 어떻게 작성해야 할지 정의하는 JSON 콘텐츠를 가진 파일을 가리켜야만 합니다. JSON 환경설정 파일의 문법에 대해서는 JP2OpenJPEG 드라이버 문서에 있는 :ref:`GMLJP2v2 정의 파일 단락 <gmjp2v2def>` 을 참조하십시오. JSON 콘텐츠를 그때 그때 처리해서(inline) 문자열로 직접 전송할 수도 있습니다. filename을 그냥 YES로 설정하면, 최소한의 인스턴스만 빌드할 것입니다.

-  **GeoJP2=YES/NO**:
   GeoJP2 (GeoTIFF-in-JPEG2000) 사양을 준수하는 UUID/GeoTIFF 경계 상자가 파일에 포함되어야 하는지를 선택합니다. 기본값은 YES입니다.

-  **PROFILE=profile**:
   BASELINE_0, BASELINE_1, BASELINE_2, NPJE 또는 EPJE 가운데 하나를 설정합니다. 각 프로파일의 상세 정보를 알고 싶다면 ECW SDK 문서를 읽어보십시오.

-  **PROGRESSION=LRCP/RLCP/RPCL**:
   JPEG2000 코드스트림을 작성하는 진행 순서(progression order)를 설정합니다. 기본값은 RPCL입니다.

-  **CODESTREAM_ONLY=YES/NO**:
   이 옵션을 YES로 설정하는 경우, 압축된 영상 코드만 작성할 것입니다. NO로 설정하면 다양한 메타 정보를 포함하는 코드스트림에 맞춰 JP2 패키지를 작성할 것입니다. 기본값은 NO입니다.

-  **LEVELS=n**:
   피라미드의 해상도 수준 개수를 설정합니다. (기본값은 가장 작은 섬네일 이미지의 크기가 최대 64x64 픽셀이 되는 개수입니다.)

-  **LAYERS=n**:
   품질 레이어의 개수를 설정합니다. 기본값은 1입니다.

-  **PRECINCT_WIDTH=n**:
   구역(precinct)의 너비를 설정합니다. 기본값은 64입니다.

-  **PRECINCT_HEIGHT=n**:
   구역(precinct)의 높이를 설정합니다. 기본값은 64입니다.

-  **TILE_WIDTH=n**:
   타일의 너비를 설정합니다. 기본값은 이미지 너비로, 예를 들면 타일 1개입니다.
   GeoTIFF와는 달리, JPEG2000 타일화 작업에서는 구역(precinct)을 사용해도 속도에 큰 영향을 미치지 않습니다. 표준이 허용하는 최소 타일 크기는 1024x1024 픽셀입니다.

-  **TILE_HEIGHT=n**:
   타일의 높이를 설정합니다. 기본값은 이미지 높이로, 예를 들면 타일 1개입니다.

-  **INCLUDE_SOP=YES/NO**:
   패킷의 시작(Start of Packet) 마커를 산출할지 여부를 선택합니다. 기본값은 NO입니다.

-  **INCLUDE_EPH=YES/NO**:
   패킷 헤더의 마지막(End of Packet Header) 마커를 산출할지 여부를 선택합니다. 기본값은 YES입니다.

-  **DECOMPRESS_LAYERS=n**:
   디코딩할 품질 레이어의 개수를 설정합니다.

-  **DECOMPRESS_RECONSTRUCTION_PARAMETER=n**:
   IRREVERSIBLE_9x7 또는 REVERSIBLE_5x3 가운데 하나로 설정할 수 있습니다.

-  **WRITE_METADATA=YES/NO**:
   전용 JP2 XML 경계 상자에 메타데이터를 작성해야 할지 여부를 선택합니다. 기본값은 NO입니다.
   이 XML 상자의 내용은 다음과 비슷할 것입니다:

   ::

      <GDALMultiDomainMetadata>
        <Metadata>
          <MDI key="foo">bar</MDI>
        </Metadata>
        <Metadata domain='aux_domain'>
          <MDI key="foo">bar</MDI>
        </Metadata>
        <Metadata domain='a_xml_domain' format='xml'>
          <arbitrary_xml_content>
          </arbitrary_xml_content>
        </Metadata>
      </GDALMultiDomainMetadata>

   이름이 "xml:BOX\_"로 시작하는 메타데이터 도메인이 존재하는 경우, 각각 개별 JP2 XML 상자로 작성할 것입니다.

   이름이 "xml:XMP"인 메타데이터 도메인이 존재하는 경우, 그 내용을 JP2 UUID XMP 상자로 작성할 것입니다.

-  **MAIN_MD_DOMAIN_ONLY=YES/NO**:
   (WRITE_METADATA=YES를 설정한 경우에만) 주 도메인으로부터 나온 메타데이터만 작성해야 할지 여부를 선택합니다. 기본값은 NO입니다.

"JPEG2000 포맷은 GDAL 오버뷰 생성을 지원하지 않습니다. 이 포맷이 이미 "임의의 오버뷰"에 최적화된 것으로 간주하기 때문입니다. JP2ECW 드라이버는 JP2 코드스트림도 2의 거듭제곱 오버뷰에 최적 접근할 수 있도록 처리합니다. 이 습성은 LEVELS 생성 옵션으로 제어됩니다."

환경설정 옵션
---------------------

ERDAS ECW/JP2 SDK는 여러 객체들을 제어하기 위해 다양한 `런타임 환경설정 옵션 <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 을 지원합니다. 이런 옵션들 대부분은 GDAL 환경설정 옵션으로 노출됩니다. 이 옵션들의 의미를 완전하게 알고 싶다면 ECW/JP2 SDK 문서를 읽어보십시오.

-  **ECW_CACHE_MAXMEM=bytes**:
   인메모리(in-memory) 캐시 작업에 쓰이는 RAM의 최대 바이트를 설정합니다. 설정하지 않는 경우, SDK가 인메모리 캐시 작업을 위해 물리적 RAM의 1/4까지 사용할 것입니다.

-  **ECW_TEXTURE_DITHER=TRUE/FALSE**:
   ECW 파일 압축 해제 시 디더링을 비활성화하려면 이 옵션을 FALSE로 설정할 수도 있습니다. 기본값은 TRUE입니다.

-  **ECW_FORCE_FILE_REOPEN=TRUE/FALSE**:
   각 연결이 생성될 때마다 각 파일에 대해 파일 핸들(file handle)을 강제로 열려면 이 옵션을 TRUE로 설정할 수도 있습니다. 기본값은 FALSE입니다.

-  **ECW_CACHE_MAXOPEN=number**:
   ECW 파일 핸들 캐시 작업을 위해 열고 있어야 하는 파일의 최대 개수를 설정합니다. 기본값은 무제한입니다.

-  **ECW_AUTOGEN_J2I=TRUE/FALSE**:
   JPEG2000 파일을 열 때 .j2i 색인 파일을 생성해야 할지 여부를 제어합니다. 기본값은 TRUE입니다.

-  **ECW_RESILIENT_DECODING=TRUE/FALSE**:
   판독기가 파일에 있는 오류를 무시해야 하는지, 사용할 수 있는만큼 많은 데이터를 반환하려 해야 하는지 여부를 제어합니다. 기본값은 TRUE입니다. FALSE로 설정하면 무결하지 않은 파일이 오류를 발생시킬 것입니다.

메타데이터
---------

JPEG2000 파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.

ECW/JP2 SDK 5.1 이상 버전도 JPEG2000 구조 정보를 "JPEG2000" 메타데이터 도메인 (-mdd) 아래 리포트된 일반 파일 메타데이터로 노출시킵니다:

-  **ALL_COMMENTS**:
   일반 주석 텍스트 필드

-  **PROFILE**:
   프로파일 유형(0, 1, 2)입니다. 자세한 정보는 ECW/JP2 SDK 문서를 참조하십시오.

-  **TILES_X**:
   X(수평)축 상의 타일 개수

-  **TILES_Y**:
   Y(수직)축 상의 타일 개수

-  **TILE_WIDTH**:
   X축에 있는 타일 하나의 크기

-  **TILE_HEIGHT**:
   Y축에 있는 타일 하나의 크기

-  **PRECINCT_SIZE_X**:
   X축에서 각 해상도 (최저에서 최고) 수준 별 구역(precinct)의 크기

-  **PRECINCT_SIZE_Y**:
   Y축에서 각 해상도 (최저에서 최고) 수준 별 구역(precinct)의 크기

-  **CODE_BLOCK_SIZE_X**:
   X축에 있는 코드 블록의 크기

-  **CODE_BLOCK_SIZE_Y**:
   Y축에 있는 코드 블록의 크기

-  **PRECISION**:
   각 구성요소의 정밀도/비트 심도(bit depth).
   예: 8비트 밴드 3개를 가진 영상의 경우 8,8,8

-  **RESOLUTION_LEVELS**:
   해상도 수준의 개수

-  **QUALITY_LAYERS**:
   품질 레이어의 개수

-  **PROGRESSION_ORDER**:
   진행 순서 (RPCL, LRCP, CPRL, RLCP)

-  **TRANSFORMATION_TYPE**:
   변형 필터링 사용 (9x7, 5x3)

-  **USE_SOP**:
   패킷의 시작(Start of Packet) 마커 탐지 여부 (TRUE/FALSE)

-  **USE_EPH**:
   패킷 헤더의 마지막(End of Packet Header) 마커 탐지 여부 (TRUE/FALSE)

-  **GML_JP2_DATA**:
   OGC GML 지리참조 경계 상자 탐지 여부 (TRUE/FALSE)

-  **COMPRESSION_RATE_TARGET**:
   인코딩에 사용된 대상 압축률

참고
--------

-  ``gdal/frmts/ecw/ecwdataset.cpp`` 로 구현되었습니다.
-  `www.hexagongeospatial.com <http://hexagongeospatial.com/products/data-management-compression/ecw/erdas-ecw-jp2-sdk>`_ 에서 ECW/JP2 SDK를 다운로드할 수 있습니다.
-  `사용자 지침서 <http://hexagongeospatial.com/products/data-management-compression/ecw/erdas-ecw-jp2-sdk/literature>`_ 에서 상품 정보를 더 자세히 볼 수 있습니다.
-  GDAL 특화가 아닌 문제에 대한 지원을 받으려면 `헥사곤 지오스페이셜 공공 포럼 <https://sgisupport.intergraph.com/infocenter/index?page=forums&forum=507301383c17ef4e013d8dfa30c2007ef1>`_ 에 문의해보십시오.
-  `GDAL ECW 빌드 힌트 <http://trac.osgeo.org/gdal/wiki/ECW>`_
