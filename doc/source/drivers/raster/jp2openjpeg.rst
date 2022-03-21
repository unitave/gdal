.. _raster.jp2openjpeg:

================================================================================
JP2OpenJPEG -- OpenJPEG 라이브러리 기반 JPEG2000 드라이버
================================================================================

.. shortname:: JP2OpenJPEG

.. build_dependencies:: openjpeg 2.1 이상 버전

이 드라이버는 OpenJPEG **버전 2** 를 기반으로 구현된 JPEG2000 판독기/작성기입니다.

이 드라이버는 VSI 가상 파일 API를 사용하기 때문에, JPEG2000 압축 NITF 파일을 읽을 수 있습니다.

JPEG2000 파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.

이 드라이버는 지리참조 정보를 GeoJP2 및 GMLJP2 경계 상자로 작성하는 기능을 지원합니다.

이 드라이버는 투명도와 임의의 밴드 개수를 가진 파일 생성 및 메타데이터 추가/읽기를 지원합니다. 기존 파일의 지리참조 정보 또는 메타데이터도 업데이트할 수 있습니다. xml:IPR 경계 상자에 있는 선택적인 지적재산 메타데이터를 읽고 쓸 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

지리참조 작업
--------------

내부(GeoJP2 또는 GMLJP2 경계 상자), 월드 파일 .j2w/.wld 사이드카 파일, 또는 PAM(Persistent Auxiliary metadata) .aux.xml 사이드카 파일 등 서로 다른 소스들로부터 지리참조 정보를 얻을 수 있습니다. 기본적으로 PAM, GeoJP2, GMLJP2, WORLDFILE 순서대로 정보를 수집합니다. (첫 항목을 가장 우선합니다.)

GDAL 2.2버전부터, GDAL_GEOREF_SOURCES 환경설정 옵션으로 (또는 GEOREF_SOURCES 열기 옵션으로) 사용할 수 있는 소스와 그 우선 순위를 변경할 수 있습니다. 이 옵션의 값은 PAM, GEOJP2, GMLJP2, (GEOJP2, GMLJP2로 가는 단축 키인) INTERNAL, WORLDFILE, NONE이라는 키워드를 쉼표로 구분한 목록입니다. 목록의 첫 항목이 가장 우선되는 소스입니다. 목록에 없는 소스는 무시할 것입니다.

예를 들어 이 옵션을 "WORLDFILE,PAM,INTERNAL"로 설정하면 PAM이나 내부 JP2 경계 상자보다 잠재적인 월드 파일의 지리변형 행렬을 우선할 것입니다. "PAM,WORLDFILE,GEOJP2"로 설정하면 설정된 소스를 이용하고 GMLJP2 경계 상자는 무시할 것입니다.

스레드 지원
--------------

JPEG2000 파일이 내부 타일을 가지고 있다면, GDAL은 기본적으로 RasterIO()가 교차하는 타일 여러 개를 요청해서 받는 경우 타일 여러 개를 멀티스레드로 디코딩하려 시도할 것입니다. 이 맥락에서 기본값이 ALL_CPUS인 ``GDAL_NUM_THREADS`` 환경설정 옵션을 이용하면 이런 습성을 제어할 수 있습니다. RAM 옵션으로 메모리 용량이 제한된 경우, 멀티스레딩을 비활성화시키기 위해 GDAL_NUM_THREADS 환경설정 옵션을 1로 설정해야 할 수도 있습니다.

OpenJPEG 2.2.0버전부터, 코드 블록 수준에서 멀티스레드 디코딩을 활성화할 수도 있습니다. 반드시 ``OPJ_NUM_THREADS`` 환경설정 변수로 활성화시켜야만 합니다. (주의: 이 변수는 GDAL 환경설정 변수가 아니라 시스템 환경설정 변수입니다.) 숫자값 또는 NUM_CPUS를 이 변수의 값으로 설정할 수 있습니다. 기본값은 1입니다. GDAL 2.3버전부터, GDAL은 코드 블록 수준에서 이 멀티스레드 디코딩을 자동으로 활성화합니다.
GDAL 3.0.1 및 OpenJPEG 2.3.2버전부터 멀티스레드 디코딩을 자동으로 활성화하고, 이를 ``OPJ_NUM_THREADS`` 환경설정 변수 또는 ``GDAL_NUM_THREADS`` 환경설정 옵션으로 제어할 수 있습니다.

이 두 개의 멀티스레딩 메커니즘을 함께 사용할 수 있습니다.

열기 옵션
--------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **STRICT=YES/NO**:
   (GDAL 3.5 및 OpenJPEG 2.5 이상 버전) 엄격한, 또는 지나치게 규칙을 준수하는 디코딩 모드를 활성화해야 할지 여부를 선택합니다. 일부 결손 파일의 - 보통 단일 타일로 잘린(truncated) 파일의 - 디코딩을 허용하려면 NO로 설정하면 됩니다. 기본값은 YES(엄격 모드)입니다.

-  **1BIT_ALPHA_PROMOTION=YES/NO**:
   1비트 알파 채널을 8비트로 승격시켜야 할지 여부를 선택합니다. 기본값은 YES입니다.

-  **GEOREF_SOURCES=string**:
   (GDAL 2.2 이상 버전) 사용할 수 있는 지리참조 소스와 그 우선 순위를 정의합니다. `지리참조 작업 <#georeferencing>`_ 단락을 참조하십시오.

-  **USE_TILE_AS_BLOCK=YES/NO**:
   (GDAL 2.2 이상 버전) GDAL 블록 크기를 언제나 JPEG2000 블록 크기로 사용할지 여부를 선택합니다. 기본값은 NO입니다. 이미지가 단일 타일인 경우 전체 이미지를 압축 해제할 때 이 옵션을 설정하면 유용할 수 있습니다. 하지만 타일 용량이 절대로 2GB를 초과해서는 안 된다는 사실을 기억하십시오. GDAL이 2GB를 초과하는 타일을 지원하지 않기 때문입니다.

생성 옵션
----------------

-  **CODEC=JP2/J2K**:
   JP2 코덱은 코드스트림 데이터에 맞춰 JP2 경계 상자를 추가할 것입니다.
   파일 확장자로부터 이 옵션의 값을 자동으로 결정합니다.
   이 옵션의 값이 JP2도 J2K도 아닌 경우 J2K 코덱을 사용합니다.

-  **GMLJP2=YES/NO**:
   JPEG2000 사양의 OGC GML을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. GMLJP2V2_DEF를 사용하지 않는 이상, GMLJP2 경계 상자의 버전은 1일 것입니다. 기본값은 YES입니다.

-  **GMLJP2V2_DEF=filename**:
   `OGC GML-in-JPEG2000 버전 2.0.1 <http://docs.opengeospatial.org/is/08-085r5/08-085r5.html>`_ 사양을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. *filename* 이 GMLJP2 v2 경계 상자를 어떻게 작성해야 할지 정의하는 JSON 콘텐츠를 가진 파일을 가리켜야만 합니다. JSON 환경설정 파일의 문법에 대해서는 다음 :ref:`GMLJP2v2 정의 파일 단락 <gmjp2v2def>` 을 참조하십시오. JSON 콘텐츠를 그때 그때 처리해서(inline) 문자열로 직접 전송할 수도 있습니다. filename을 그냥 YES로 설정하면, 최소한의 인스턴스만 빌드할 것입니다.
   주의: GDAL 2.0과 2.1버전은 예전 `OGC GML-in-JPEG2000 버전 2.0 <http://docs.opengeospatial.org/is/08-085r4/08-085r4.html>`_ 사양을 사용합니다. 이 사양은 gmljp2:GMLJP2CoverageCollection의 gml:domainSet, gml:rangeSet 및 gmlcov:rangeType 요소의 내용이 본질적으로 다릅니다.

-  **GeoJP2=YES/NO**:
   GeoJP2 (GeoTIFF-in-JPEG2000) 사양을 준수하는 UUID/GeoTIFF 경계 상자가 파일에 포함되어야 하는지를 선택합니다. 기본값은 NO입니다. 기본값은 YES입니다.

-  **QUALITY=float_value,float_value,...**:
   압축 용량 비율을 0에서 100 사이의 비압축 이미지 용량의 백분율로 설정합니다. 50으로 설정하면 비압축 데이터의 1/2 용량의 파일을 생성할 것입니다. 33으로 설정하면 1/3 용량의 파일을 생성할 것입니다. 데이터셋이 색상표를 가진 단일 밴드로 이루어지지 않은 한 기본값은 25입니다. 데이터셋이 색상표를 가진 단일 밴드로 이루어져 있는 경우 기본값은 100입니다. 품질 레이어 여러 개를 요청하기 위해 품질값을 (쉼표로 구분된) 여러 값으로 지정할 수 있습니다. 이때 작은 값에서 큰 값 순서로 지정해야 합니다.

-  **REVERSIBLE=YES/NO**:
   YES로 설정하면 가역 5x3 정수 전용 필터를 사용하고, NO로 설정하면 비가역 DWT 9-7 필터를 사용합니다. 데이터셋이 색상표를 가진 단일 밴드로 이루어지지 않은 한 기본값은 NO입니다. 데이터셋이 색상표를 가진 단일 밴드로 이루어져 있는 경우 가역 필터를 사용합니다.

-  **RESOLUTIONS=int_value**:
   해상도 수준의 개수를 설정합니다. 타일의 가장 작은 오버뷰의 크기가 128x128을 넘지 않는 기본값을 선택합니다.

-  **BLOCKXSIZE=int_value**:
   타일 너비를 설정합니다. 기본값은 1024입니다.

-  **BLOCKYSIZE=int_value**:
   타일 높이를 설정합니다. 기본값은 1024입니다.

-  **PROGRESSION=LRCP/RLCP/RPCL/PCRL/CPRL**:
   진행 순서를 설정합니다. 기본값은 LRCP입니다.

-  **SOP=YES/NO**:
   패킷의 시작(Start of Packet) 마커를 산출할지 여부를 선택합니다. 기본값은 NO입니다.

-  **EPH=YES/NO**:
   패킷 헤더의 마지막(End of Packet Header) 마커를 산출할지 여부를 선택합니다. 기본값은 NO입니다.

-  **YCBCR420=YES/NO**:
   RGB를 YCbCr 4:2:0으로 리샘플링해야만 하는지 여부를 선택합니다. 기본값은 NO입니다.

-  **YCC=YES/NO**:
   RGB를 YCC 색공간으로 변환해야만 하는지 ("MCT 변환", 예: 시각적으로 악화되지 않는 내부 변환을 해야만 하는지) 여부를 선택합니다. 기본값은 YES입니다.

-  **NBITS=int_value**:
   sub-byte형 파일(1-7), sub-uint16형 파일(9-15), sub-uint32형 파일(17-31)의 비트(정밀도)입니다.

-  **1BIT_ALPHA=YES/NO**:
   (알파 채널이 존재하는 경우) 알파 채널을 1비트 채널로 인코딩할지 여부를 선택합니다. INSPIRE_TG를 YES로 설정하지 않는 한, 기본값은 NO입니다. 이 옵션을 활성화하면 몇몇 판독기와 호환성 문제가 발생할 수도 있습니다. 이 문서를 작성한 때를 기준으로, MrSID JPEG2000 SDK 기반 판독기는 1비트 채널로 인코딩한 알파 채널을 가진 파일을 열지 못 합니다. ECW JPEG2000 SDK 기반 판독기의 경우, 손실/비가역 압축된 1비트 알파 채널을 디코딩하면 시각적으로 악화됩니다. (비손실 인코딩된 경우는 괜찮습니다.)

-  **ALPHA=YES/NO**:
   마지막 채널을 알파 채널로 강제 인코딩할지 여부를 선택합니다. 해당 채널의 색상을 이미 알파로 해석하지 않은 경우에만 유용합니다. 기본값은 NO입니다.

-  **PROFILE=AUTO/UNRESTRICTED/PROFILE_1**:
   사용할 코드스트림 프로파일을 결정합니다.
   
   * UNRESTRICTED: "Unrestricted JPEG 2000 Part 1 codestream" (RSIZ=0)
   * PROFILE_1: "JPEG 2000 Part 1 Profile 1 codestream" (RSIZ=2), 타일 크기 및 해상도 개수에 제약 조건을 추가합니다.
   * AUTO: 이 모드에서는 드라이버가 BLOCKXSIZE, BLOCKYSIZE, RESOLUTIONS, CODEBLOCK_WIDTH 및 CODEBLOCK_HEIGHT 옵션 값들이 PROFILE_1과 호환되는지 결정하고 호환되는 경우 노출시킬 것입니다. 이 옵션들의 기본값은 PROFILE_1과 호환된다는 사실을 기억하십시오. 기본값으로 설정하지 않아 호환되지 않는 경우 UNRESTRICTED를 사용할 것입니다.
   
   기본값은 AUTO입니다.

-  **INSPIRE_TG=YES/NO**:
   `정사영상에 관한 인스파이어(Inspire) 데이터 사양 - 기술 지침 <http://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_DataSpecification_OI_v3.0.pdf>`_ 을 준수하는 JPEG2000 객체를 사용할지 여부를 선택합니다. 기본값은 NO입니다.
   이 옵션을 YES로 설정하면, PROFILE=PROFILE_1, 1BIT_ALPHA=YES, GEOBOXES_AFTER_JP2C=YES를 정의한다는 의미입니다. 기술 지침의 요구사항 및 권장사항에 대해 CODEC, BLOCKXSIZE, BLOCKYSIZE, RESOLUTIONS, NBITS, PROFILE, CODEBLOCK_WIDTH 및 CODEBLOCK_HEIGHT 옵션을 검증할 것입니다.

-  **JPX=YES/NO**:
   GMLJP2 경계 상자 작성 시 JPX 객체를 노출시키고 판독기 필수 경계 상자를 추가할지 여부를 선택합니다. 기본값은 YES입니다. 판독기와 호환성 문제가 발생하지 않는 한 이 옵션을 사용해서는 안 됩니다.

-  **GEOBOXES_AFTER_JP2C=YES/NO**:
   코드스트림 뒤에 GeoJP2/GMLJP2 경계 상자를 배치할지 여부를 선택합니다. INSPIRE_TG를 YES로 설정하지 않는 한, 기본값은 NO입니다. 판독기와 호환성 문제가 발생하지 않는 한 이 옵션을 사용해서는 안 됩니다.

-  **PRECINCTS={prec_w,prec_h},{prec_w,prec_h},...**:
   구역(precinct) 크기를 지정하기 위한 {구역 너비,구역 높이} 투플(tuple) 목록입니다. 각 값이 2의 배수여야 합니다. 목록에 있는 투플의 최대 개수가 해상도 개수가 될 것입니다. 첫 번째 투플이 최고 해상도 수준에 대응하고, 그 다음은 한 단계 낮은 해상도 수준에 대응합니다. 지정한 투플 개수가 적을수록 마지막 투플의 값을 2로 나누어 각 추가 저해상도 수준에 사용합니다. 기본값은 {512,512},{256,512},{128,512},{64,512},{32,512},{16,512},{8,512},{4,512},{2,512}입니다.
   구역을 비활성화하려면 빈 문자열을 설정하면 됩니다. (예: 이런 경우 기본값 {32767,32767},{32767,32767}, ...을 사용할 것입니다.)

-  **TILEPARTS=DISABLED/RESOLUTIONS/LAYERS/COMPONENTS**:
   타일 부분(tile-part)을 생성할지, 생성한다면 어떤 기준에 따라 생성할지 설정합니다. 기본값은 DISABLED입니다.

-  **CODEBLOCK_WIDTH=int_value**:
   코드 블록 너비를 설정합니다. 4에서 1024 사이의 2의 거듭제곱 값을 지정할 수 있습니다. 기본값은 64입니다. CODEBLOCK_WIDTH와 CODEBLOCK_HEIGHT를 곱한 값이 절대로 4096을 초과해서는 안 된다는 사실을 기억하십시오. PROFILE_1 호환성을 설정한 경우, CODEBLOCK_WIDTH가 절대로 64를 초과해서는 안 됩니다.

-  **CODEBLOCK_HEIGHT=int_value**:
   코드 블록 높이를 설정합니다. 4에서 1024 사이의 2의 거듭제곱 값을 지정할 수 있습니다. 기본값은 64입니다. CODEBLOCK_WIDTH와 CODEBLOCK_HEIGHT를 곱한 값이 절대로 4096을 초과해서는 안 된다는 사실을 기억하십시오. PROFILE_1 호환성을 설정한 경우, CODEBLOCK_HEIGHT가 절대로 64를 초과해서는 안 됩니다.

-  **CODEBLOCK_STYLE=string**:
   (GDAL 2.4 및 OpenJPEG 2.3.0 이상 버전) 코드 블록의 코딩 패스 스타일을 설정합니다. 다음 6개의 독립적인 설정을 함께 결합할 수 있습니다(값을 쉼표로 구분해야 합니다):

   *  *BYPASS* (1): 선택적인 산술 코딩 바이패스를 활성화합니다. (파일 용량은 늘어나지만 코딩/디코딩 속도를 훨씬 향상시킬 수 있습니다.)
   *  *RESET* (2): 코딩 패스 경계 상에 있는 문맥 확률(context probability)을 리셋합니다.
   *  *TERMALL* (4): 각 코딩 패스에 대한 종료(termination)를 활성화합니다.
   *  *VSC* (8): 수직 인과 관계(vertically causal context)를 활성화합니다.
   *  *PREDICTABLE* (16): 예상 가능한 종료를 활성화합니다. (오류를 탐지한 경우 도움이 됩니다.)
   *  *SEGSYM* (32): 분할(segmentation) 심볼을 활성화합니다. (오류를 탐지한 경우 도움이 됩니다.)

   스타일을 텍스트로 설정하는 대신, 선택한 전체 수준 코드 블록 스타일의 해당 숫자값을 더해서 설정할 수도 있습니다. (예를 들면 "BYPASS,TERMALL"을 "5"(1+4)로 설정할 수 있습니다.)

   기본적으로 어떤 스타일도 활성화하지 않습니다. 이 스타일들을 활성화하면 일반적으로 코드스트림 용량이 늘어나지만, 코딩/디코딩 속도 또는 오류 허용도(resilience) 또는 오류 탐지를 향상시킬 것입니다.

-  **PLT=YES/NO**:
   (GDAL 3.1.1 및 OpenJPEG 2.4.0 이상 버전) 타일 부분(tile-part) 헤더에 PLT(Packet Length) 마커 부분을 작성할지 여부를 선택합니다. 기본값은 NO입니다.

-  **TLM=YES/NO**:
   (GDAL 3.4.0 및 OpenJPEG 2.5.0 이상 버전) 주 헤더에 TLM(Tile-part Length) 마커 부분을 작성할지 여부를 선택합니다. 기본값은 NO입니다.

-  **WRITE_METADATA=YES/NO**:
   전용 JP2 'xml ' 경계 상자에 메타데이터를 작성해야 할지 여부를 선택합니다. 기본값은 NO입니다. 'xml ' 상자의 내용은 다음과 비슷할 것입니다:

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

   "xml:BOX\_"로 시작하는 메타데이터 도메인 이름이 존재하는 경우, 해당 메타데이터 도메인을 각각 개별 JP2 'xml ' 경계 상자로 작성할 것입니다.

   이름이 "xml:XMP"인 메타데이터 도메인이 존재하는 경우, 그 내용을 JP2 'uuid' XMP 상자로 작성할 것입니다.

   이름이 "xml:IPR"인 메타데이터 도메인이 존재하는 경우, 그 내용을 JP2 'jp2i' 상자로 작성할 것입니다.

-  **MAIN_MD_DOMAIN_ONLY=YES/NO**:
   (WRITE_METADATA 옵션을 YES로 설정한 경우에만) 주 도메인으로부터 나온 메타데이터만 작성해야 할지 여부를 선택합니다. 기본값은 NO입니다.

-  **USE_SRC_CODESTREAM=YES/NO**:
   (실험적인 옵션입니다!) 소스 데이터셋이 JPEG2000인 경우, 소스 데이터셋의 코드스트림을 수정하지 않은 채 재사용할지 여부를 선택합니다. 기본값은 NO입니다. 이 기능을 활성화하면 JP2 경계 상자의 내용과 소스 코드스트림의 내용이 일관성을 잃을 수도 있습니다. 이 모드에서는 다른 대부분의 생성 옵션을 무시할 것입니다. 지리참조, 메타데이터 등등을 추가하거나 수정하는 몇몇 활용례의 경우 유용할 수도 있습니다.
   INSPIRE_TG 및 PROFILE 옵션을 무시하고, 코드스트림의 프로파일을 (코드스트림의 특성과 일치하지 않을 수도 있는) 이 옵션이 지정하는/암시하는 프로파일로 대체할 것입니다.

비손실 압축
~~~~~~~~~~~~~~~~~~~~

다음 생성 옵션들을 모두 다음과 같이 정의한 경우 비손실 압축을 사용할 수 있습니다.:

-  QUALITY=100
-  REVERSIBLE=YES
-  YCBCR420=NO (기본값)

.. _gmjp2v2def:

GMLJP2v2 정의 파일
~~~~~~~~~~~~~~~~~~~~~~~~

GMLJP2 v2 경계 상자는 일반적으로 공간 좌표계 정보와 지리변형 행렬을 가진 GMLJP2RectifiedGridCoverage를 단고 있습니다. 메타데이터, 벡터 객체(GML 객체 집합), 주석(KML), 스타일(일반적으로 SLD, 또는 기타 XML 서식) 또는 다른 어떤 XML 콘텐츠도 확장 사양으로 추가할 수 있습니다. GMLJP2V2_DEF 생성 옵션의 값은 다음 문법을 준수하는 파일이어야 합니다("#"으로 시작하는 요소는 문서이며, 생략할 수 있습니다):

.. code-block:: json

   {
       "#doc" : "Unless otherwise specified, all elements are optional",

       "#root_instance_doc": "Describe content of the GMLJP2CoverageCollection",
       "root_instance": {
           "#gml_id_doc": "Specify GMLJP2CoverageCollection gml:id. Default is ID_GMLJP2_0",
           "gml_id": "some_gml_id",

           "#grid_coverage_file_doc": [
               "External XML file, whose root might be a GMLJP2GridCoverage, ",
               "GMLJP2RectifiedGridCoverage or a GMLJP2ReferenceableGridCoverage.",
               "If not specified, GDAL will auto-generate a GMLJP2RectifiedGridCoverage" ],
           "grid_coverage_file": "gmljp2gridcoverage.xml",

           "#grid_coverage_range_type_field_predefined_name_doc": [
               "New in GDAL 2.2",
               "One of Color, Elevation_meter or Panchromatic ",
               "to fill gmlcov:rangeType/swe:DataRecord/swe:field",
               "Only used if grid_coverage_file is not defined.",
               "Exclusive with grid_coverage_range_type_file" ],
           "grid_coverage_range_type_field_predefined_name": "Color",

           "#grid_coverage_range_type_file_doc": [
               "New in GDAL 2.2",
               "File that is XML content to put under gml:RectifiedGrid/gmlcov:rangeType",
               "Only used if grid_coverage_file is not defined.",
               "Exclusive with grid_coverage_range_type_field_predefined_name" ],
           "grid_coverage_range_type_file": "grid_coverage_range_type.xml",

           "#crs_url_doc": [
               "true for http://www.opengis.net/def/crs/EPSG/0/XXXX CRS URL.",
               "If false, use CRS URN. Default value is true",
               "Only taken into account for a auto-generated GMLJP2RectifiedGridCoverage"],
           "crs_url": true,

           "#metadata_doc": [ "An array of metadata items. Can be either strings, with ",
                              "a filename or directly inline XML content, or either ",
                              "a more complete description." ],
           "metadata": [

               "dcmetadata.xml",

               {
                   "#file_doc": "Can use relative or absolute paths. Exclusive of content, gdal_metadata and generated_metadata.",
                   "file": "dcmetadata.xml",

                   "#gdal_metadata_doc": "Whether to serialize GDAL metadata as GDALMultiDomainMetadata",
                   "gdal_metadata": false,

                   "#dynamic_metadata_doc":
                       [ "The metadata file will be generated from a template and a source file.",
                         "The template is a valid GMLJP2 metadata XML tree with placeholders like",
                         "{{{XPATH(some_xpath_expression)}}}",
                         "that are evaluated from the source XML file. Typical use case",
                         "is to generate a gmljp2:eopMetadata from the XML metadata",
                         "provided by the image provider in their own particular format." ],
                   "dynamic_metadata" :
                   {
                       "template": "my_template.xml",
                       "source": "my_source.xml"
                   },

                   "#content": "Exclusive of file. Inline XML metadata content",
                   "content": "<gmljp2:metadata>Some simple textual metadata</gmljp2:metadata>",

                   "#parent_node": ["Where to put the metadata.",
                                    "Under CoverageCollection (default) or GridCoverage" ],
                   "parent_node": "CoverageCollection"
               }
           ],

           "#annotations_doc": [ "An array of filenames, either directly KML files",
                                 "or other vector files recognized by GDAL that ",
                                 "will be translated on-the-fly as KML" ],
           "annotations": [
               "my.kml"
           ],

           "#gml_filelist_doc" :[
               "An array of GML files or vector files that will be on-the-fly converted",
               "to GML 3.2. Can be either GML filenames (or other OGR datasource names), ",
               "or a more complete description" ],
           "gml_filelist": [

               "my.gml",

               "my.shp",

               {
                   "#file_doc": "OGR datasource. Can use relative or absolute paths. Exclusive of remote_resource",
                   "file": "converted/test_0.gml",

                   "#remote_resource_doc": "URL of a feature collection that must be referenced through a xlink:href",
                   "remote_resource": "https://github.com/OSGeo/gdal/blob/master/autotest/ogr/data/expected_gml_gml32.gml",

                   "#namespace_doc": ["The namespace in schemaLocation for which to substitute",
                                     "its original schemaLocation with the one provided below.",
                                     "Ignored for a remote_resource"],
                   "namespace": "http://example.com",

                   "#schema_location_doc": ["Value of the substituted schemaLocation. ",
                                            "Typically a schema box label (link)",
                                            "Ignored for a remote_resource"],
                   "schema_location": "gmljp2://xml/schema_0.xsd",

                   "#inline_doc": [
                       "Whether to inline the content, or put it in a separate xml box. Default is true",
                       "Ignored for a remote_resource." ],
                   "inline": true,

                   "#parent_node": ["Where to put the FeatureCollection.",
                                    "Under CoverageCollection (default) or GridCoverage" ],
                   "parent_node": "CoverageCollection"
               }
           ],


           "#styles_doc": [ "An array of styles. For example SLD files" ],
           "styles" : [
               {
                   "#file_doc": "Can use relative or absolute paths.",
                   "file": "my.sld",

                   "#parent_node": ["Where to put the FeatureCollection.",
                                    "Under CoverageCollection (default) or GridCoverage" ],
                   "parent_node": "CoverageCollection"
               }
           ],

           "#extensions_doc": [ "An array of extensions." ],
           "extensions" : [
               {
                   "#file_doc": "Can use relative or absolute paths.",
                   "file": "my.xml",

                   "#parent_node": ["Where to put the FeatureCollection.",
                                    "Under CoverageCollection (default) or GridCoverage" ],
                   "parent_node": "CoverageCollection"
               }
           ]
       },

       "#boxes_doc": "An array to describe the content of XML asoc boxes",
       "boxes": [
           {
               "#file_doc": "can use relative or absolute paths. Required",
               "file": "converted/test_0.xsd",

               "#label_doc": ["the label of the XML box. If not specified, will be the ",
                             "filename without the directory part." ],
               "label": "schema_0.xsd"
           }
       ]
   }

(이런 맥락에서 XML 구조를 가진) 템플릿 파일 및 XML 소스 파일로부터 메타데이터를 동적으로 생성할 수 있습니다. {{{XPATH(xpath_expr)}}} 같은 패턴을 검색하고 이를 소스 파일의 내용에 대한 평가로 대체해서 템플릿 파일을 처리합니다. xpath_expr는 다음 함수들을 추가한 XPath 1.0 호환 표현식이어야만 합니다:

-  **if(cond_expr,expr_if_true,expr_if_false)**:
   cond_expr가 참으로 평가된 경우, expr_if_true를 반환합니다. 그렇지 않으면 expr_if_false를 반환합니다.

-  **uuid()**:
   임의의 UUID를 평가합니다.

`여기 <https://git.earthdata.nasa.gov/projects/GEE/repos/gdal-enhancements-for-esdis/browse/gdal-current/frmts/openjpeg/eoptemplate_pleiades.xml>`_ 에서 플레이아데스(Pleiades) 성단 영상의 XML 메타데이터를 처리하기 위한 템플릿 파일을, 그리고 `여기 <https://git.earthdata.nasa.gov/projects/GEE/repos/gdal-enhancements-for-esdis/browse/gdal-current/frmts/openjpeg/eoptemplate_worldviewgeoeye.xml>`_ 에서 GeoEye/WorldView 영상의 XML 메타데이터를 처리하기 위한 템플릿 파일을 찾아볼 수 있습니다.

벡터 정보
------------------

OGR API를 통해 GML 객체 집합 그리고/또는 KML 주석을 내장한 GMLJP2 v2 경계 상자를 담고 있는 JPEG2000 파일을 벡터 파일로서 열 수 있습니다. 다음은 그 예시입니다:

::

   ogrinfo -ro my.jp2

   INFO: Open of my.jp2'
         using driver `JP2OpenJPEG' successful.
   1: FC_GridCoverage_1_rivers (LineString)
   2: FC_GridCoverage_1_borders (LineString)
   3: Annotation_1_poly

객체 집합을 GMLJP2 v2 경계 상자로부터 원격 위치로 링크시킬 수 있습니다. 기본적으로, 링크를 따르지 않습니다. OPEN_REMOTE_GML 열기 옵션을 YES로 설정하면 링크를 따를 것입니다.

참고
---------

-  ``gdal/frmts/openjpeg/openjpegdataset.cpp`` 로 구현되었습니다.

-  `공식 JPEG2000 페이지 <http://www.jpeg.org/jpeg2000/index.html>`_

-  `OpenJPEG 라이브러리 홈페이지 <https://github.com/uclouvain/openjpeg>`_

-  `OGC GML-in-JPEG2000 버전 2.0 <http://docs.opengeospatial.org/is/08-085r4/08-085r4.html>`_
   (GDAL 2.0 및 2.1)

-  `OGC GML-in-JPEG2000 버전 2.0.1 <http://docs.opengeospatial.org/is/08-085r5/08-085r5.html>`_
   (GDAL 2.2 이상)

-  `정사영상에 관한 인스파이어(Inspire) 데이터 사양 - 기술 지침 <http://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_DataSpecification_OI_v3.0.pdf>`_

다른 JPEG2000 GDAL 드라이버:

-  :ref:`JPEG2000: 재스퍼 라이브러리 (오픈소스) <raster.jpeg2000>`

-  :ref:`JP2ECW: ERDAS ECW 라이브러리 기반 (상용) <raster.jp2ecw>`

-  :ref:`JP2MRSID: 리저드테크 MrSID 라이브러리 (상용) <raster.jp2mrsid>`

-  :ref:`JP2KAK: 카카두 라이브러리 기반 (상용) <raster.jp2kak>`
