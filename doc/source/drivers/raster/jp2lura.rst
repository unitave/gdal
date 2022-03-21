.. _raster.jp2lura:

================================================================================
JP2Lura -- Lurawave 기반 JPEG2000 드라이버
================================================================================

.. shortname:: JP2LURA

.. versionadded:: 2.2

.. build_dependencies:: Lurawave 라이브러리

이 드라이버는 Lurawave 라이브러리를 기반으로 구현된 JPEG2000 판독기/작성기입니다.

이 드라이버는 VSI 가상 파일 API를 사용하기 때문에, JPEG2000 압축 NITF 파일을 읽을 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

지리참조 작업
--------------

내부(GeoJP2 또는 GMLJP2 경계 상자), 월드 파일 .j2w/.wld 사이드카 파일, 또는 PAM(Persistent Auxiliary metadata) .aux.xml 사이드카 파일 등 서로 다른 소스들로부터 지리참조 정보를 얻을 수 있습니다. 기본적으로 PAM, GeoJP2, GMLJP2, WORLDFILE 순서대로 파일을 수집합니다. (첫 항목을 가장 우선합니다.)

GDAL_GEOREF_SOURCES 환경설정 옵션으로 (또는 GEOREF_SOURCES 열기 옵션으로) 사용할 수 있는 소스와 그 우선 순위를 변경할 수 있습니다. 이 옵션의 값은 PAM, GEOJP2, GMLJP2, (GEOJP2, GMLJP2로 가는 단축 키인) INTERNAL, WORLDFILE, NONE이라는 키워드를 쉼표로 구분한 목록입니다. 목록의 첫 항목이 가장 우선되는 소스입니다. 목록에 없는 소스는 무시할 것입니다.

예를 들어 이 옵션을 "WORLDFILE,PAM,INTERNAL"로 설정하면 PAM이나 내부 JP2 경계 상자보다 잠재적인 월드 파일의 지리변형 행렬을 우선할 것입니다. "PAM,WORLDFILE,GEOJP2"로 설정하면 설정된 소스를 이용하고 GMLJP2 경계 상자는 무시할 것입니다.

사용 허가 번호
--------------

LURA_LICENSE_NUM_1 및 LURA_LICENSE_NUM_2 환경설정 옵션/환경 변수를 합치면 사용 허가 번호가 되는 숫자 2개로 설정해야만 합니다.

열기 옵션
--------------

다음 열기 옵션을 사용할 수 있습니다:

-  **GEOREF_SOURCES=string**:
   사용할 수 있는 지리참조 소스와 그 우선 순위를 정의합니다. `지리참조 작업 <#georeferencing>`_ 단락을 참조하십시오.

생성 옵션
----------------

-  **CODEC=JP2/Codestream**:
   JP2 코덱은 코드스트림 데이터에 맞춰 JP2 경계 상자를 추가할 것입니다.
   파일 확장자로부터 이 옵션의 값을 자동으로 결정합니다.
   이 옵션의 값이 JP2도 Codestream도 아닌 경우 JP2 코덱을 사용합니다.

-  **GMLJP2=YES/NO**:
   JPEG2000 사양의 OGC GML을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. GMLJP2V2_DEF를 사용하지 않는 이상, GMLJP2 경계 상자의 버전은 1일 것입니다. 기본값은 YES입니다.

-  **GMLJP2V2_DEF=filename**:
   `OGC GML-in-JPEG2000 버전 2.0.1 <http://docs.opengeospatial.org/is/08-085r5/08-085r5.html>`_ 사양을 준수하는 GML 경계 상자가 파일에 포함되어야 하는지를 선택합니다. *filename* 이 GMLJP2 v2 경계 상자를 어떻게 작성해야 할지 정의하는 JSON 콘텐츠를 가진 파일을 가리켜야만 합니다. JSON 환경설정 파일의 문법에 대해서는 JP2OpenJPEG 드라이버 문서에 있는 :ref:`GMLJP2v2 정의 파일 단락 <gmjp2v2def>` 을 참조하십시오. JSON 콘텐츠를 그때 그때 처리해서(inline) 문자열로 직접 전송할 수도 있습니다. filename을 그냥 YES로 설정하면, 최소한의 인스턴스만 빌드할 것입니다.

-  **GeoJP2=YES/NO**:
   GeoJP2 (GeoTIFF-in-JPEG2000) 사양을 준수하는 UUID/GeoTIFF 경계 상자가 파일에 포함되어야 하는지를 선택합니다. 기본값은 NO입니다.

-  **SPLIT_IEEE754=YES/NO**:
   Float32 유형 밴드를 IEEE-754 구조에 따라 분해한 값들을 가진 밴드 3개로 인코딩할지 여부를 선택합니다. 첫 번째 밴드는 부호 비트를 가진 부호 있는 1비트, 두 번째 밴드는 지수(exponent) 값을 가진 부호 없는 8비트, 세 번째 밴드는 가수(假數; mantissa) 값을 가진 부호 없는 23비트입니다. 기본값은 NO입니다.
   이 옵션은 부동소수점형 값을 인코딩하기 위한 비표준 확장 사양입니다. 기본적으로 부호 비트와 지수를 (REVERSIBLE=NO를 설정했더라도) 가역 웨이블릿으로 인코딩하고, 가수는 비가역 웨이블릿으로 인코딩합니다. REVERSIBLE=YES를 설정한 경우, 세 구성요소 모두 가역 웨이블릿으로 인코딩할 것입니다.

-  **NBITS=int_value** :
   sub-byte형 파일(1-7), sub-uint16형 파일(9-15), sub-uint32형 파일(17-28)의 비트(정밀도)입니다.

-  **QUALITY_STYLE=PSNR/XXSmall/XSmall/Small/Medium/Large/XLarge/XXLarge**:
   이 속성 태그는 손실 압축 시 품질 모드를 설정하는 데 쓰입니다. 일반적인 이미지 및 상황에는 (1:1 픽셀 표출, 50cm 이하의 시거리) Small 또는 PSNR를 권장합니다. 품질 측정의 경우 PSNR만 사용해야 합니다. 기본값은 PSNR입니다.

-  **SPEED_MODE=Fast/Accurate**:
   이 속성 태그는 손실 압축 시 속도 모드를 설정하는 데 쓰입니다. 다음 모드들을 정의합니다. 기본값은 Fast입니다.

-  **RATE=int_value.**:
   이 옵션의 값을 지정하면, 대상 압축 파일 용량이 비압축 파일 용량을 RATE 값으로 나눈 용량이 될 것입니다. 일반적으로 압축률은 딱 지정한 용량대로 또는 몇 바이트 작게 나올 것입니다. 비가역 웨이블릿을 강제로 사용합니다. 기본값은 0(최고 품질)입니다.

-  **QUALITY=1 to 100**
   표준 강술(講述) 양자화를 사용하고 관심 지역이 없는 9-7 필터를 이용하는 경우에만 특정 품질로 압축할 수 있습니다. 압축 품질을 1(저품질)에서 100(고품질) 사이로 지정할 수 있습니다. 산출되는 JPEG 파일의 용량은 이미지 콘텐츠에 따라 달라질 것입니다. 이 옵션은 비가역 압축의 경우에만 사용됩니다. 압축 품질 옵션은 RATE 옵션과 함께 사용할 수 없습니다. 기본값은 0(최고 품질)입니다. 이 옵션을 SPLIT_IEEE754=YES 설정과 함께 사용하는 경우, 부호 비트와 지수 밴드를 비가역 인코딩으로 변환해야 할 것입니다. 이때 재구축된 부동소수점형 값에 큰 손실이 일어날 수도 있습니다.

-  **PRECISION=int_value**:
   효율성을 향상시키기 위해, 라이브러리가 웨이블릿 계수에 16비트 또는 32비트 표현을 이미지 심도에 따라 자동으로 사용합니다. 이 정밀도 옵션을 사용하면 라이브러리가 항상 32비트 표현을 사용하게 강제할 수 있습니다. 32비트 값을 사용하는 경우 이미지 품질과 속도 및 요구 메모리를 조금이나마 향상시킬 수도 있습니다. 기본값은 0(알맞은 정밀도를 자동 선택)입니다.

-  **REVERSIBLE=YES/NO**:
   YES로 설정하면 가역 5x3 정수 전용 필터를 사용하고, NO로 설정하면 비가역 DWT 9-7 필터를 사용합니다. 기본값은 NO입니다.

-  **LEVELS=int_value** (0-16):
   이 옵션을 설정해서 웨이블릿 변환 수준 개수를 지정할 수 있습니다. 0(웨이블릿 분석을 하지 않음)에서 16(초정밀 분석) 사이의 값을 지정할 수 있습니다. 이 변환 수준 개수가 증가할수록 요구 메모리 및 압축 시간도 늘어납니다. 변환 수준의 적당한 개수는 4에서 6 사이의 범위입니다. 기본값은 5입니다.

-  **QUANTIZATION_STYLE=DERIVED/EXPOUNDED**:
   이 옵션은 비가역 필터(9-7)를 사용하는 경우에만 설정할 수 있습니다. 기반 양자화 단계인 DERIVED로부터 양자화 단계를 파생시키거나, 또는 각 이미지의 하위 밴드인 EXPOUNDED에 대해 양자화 단계를 계산할 수 있습니다. 비가역 필터를 사용하는 경우 EXPOUNDED 스타일을 권장합니다. 기본값은 EXPOUNDED입니다.

-  **TILEXSIZE=int_value**:
   타일 너비를 설정합니다. 이미지를 더 작은 타일들로 분할할 수 있는데, 이때 각 타일을 개별적으로 압축할 수 있습니다. 이 옵션을 설정하면 가상 압축 참조 그리드 상에 있는 첫 번째 타일에 기본 타일 크기 및 오프셋을 설정할 수 있습니다. 첫 번째 타일은 첫 번째 이미지 픽셀을 담고 있어야만 합니다. 대용량 이미지에 대해서만 이미지 타일 작업을 권장합니다. 기본값은 0(전체 이미지를 담고 있는 타일 1개)입니다. 이미지 크기가 15000x15000을 초과하는 경우, 1024x1024 크기의 타일로 타일화될 것입니다.

-  **TILEYSIZE=int_value**:
   타일 높이를 설정합니다. 이미지를 더 작은 타일들로 분할할 수 있는데, 이때 각 타일을 개별적으로 압축할 수 있습니다. 이 옵션을 설정하면 가상 압축 참조 그리드 상에 있는 첫 번째 타일에 기본 타일 크기 및 오프셋을 설정할 수 있습니다. 첫 번째 타일은 첫 번째 이미지 픽셀을 담고 있어야만 합니다. 대용량 이미지에 대해서만 이미지 타일 작업을 권장합니다. 기본값은 0(전체 이미지를 담고 있는 타일 1개)입니다. 이미지 크기가 15000x15000을 초과하는 경우, 1024x1024 크기의 타일로 타일화될 것입니다.

-  **TLM=YES/NO**:
   타일 마커(TiLe Marker) 사용을 선택합니다. 타일 길이 마커를 사용하면 타일화 이미지에 있는 영역의 디코딩 효율성을 향상시킬 수도 있습니다. 타일 길이 마커는 JPEG2000 코드스트림의 각 타일의 위치를 담고 있기 때문에, 타일화 데이터에 더 빨리 접근할 수 있습니다. 기본값은 NO입니다.

-  **PROGRESSION=LRCP/RLCP/RPCL/PCRL/CPRL**:
   이 속성 태그를 설정해서 파일에 코딩되는 데이터의 구조를 설정할 수 있습니다. 다음 진행 순서를 정의합니다:
   
   * LRCP = 품질 진행(Quality progressive)
   * RLCP = 해상도 후 품질 진행(Resolution then quality progressive)
   * RPCL = 해상도 후 위치 진행(Resolution then position progressive)
   * PCRL = 위치 진행(Position progressive)
   * CPRL = 색상/채널 진행(Color/channel progressive)
   
   레이어 여러 개를 사용하는 경우 LRCP(품질) 설정이 가장 유용합니다. 구역(precinct)을 사용하는 경우 PCRL(위치) 설정을 사용해야 합니다. 기본값은 LRCP입니다.

-  **JPX=YES/NO**:
   GMLJP2 경계 상자 작성 시 JPX 객체를 노출시키고 판독기 필수 경계 상자를 추가할지 여부를 선택합니다. (GMLJP2 v2의 경우 파일명에도 "jpx "를 추가할 것입니다.) 기본값은 YES입니다. 판독기와 호환성 문제가 발생하지 않는 한 이 옵션을 사용해서는 안 됩니다.

-  **CODEBLOCK_WIDTH=int_value**:
   코드 블록 너비를 설정합니다. 4에서 1024 사이의 2의 거듭제곱 값을 지정할 수 있습니다. 기본값은 64입니다. CODEBLOCK_WIDTH와 CODEBLOCK_HEIGHT를 곱한 값이 절대로 4096을 초과해서는 안 된다는 사실을 기억하십시오. PROFILE_1 호환성을 설정한 경우, CODEBLOCK_WIDTH가 절대로 64를 초과해서는 안 됩니다.

-  **CODEBLOCK_HEIGHT=int_value**:
   코드 블록 높이를 설정합니다. 4에서 1024 사이의 2의 거듭제곱 값을 지정할 수 있습니다. 기본값은 64입니다. CODEBLOCK_WIDTH와 CODEBLOCK_HEIGHT를 곱한 값이 절대로 4096을 초과해서는 안 된다는 사실을 기억하십시오. PROFILE_1 호환성을 설정한 경우, CODEBLOCK_HEIGHT가 절대로 64를 초과해서는 안 됩니다.

-  **ERROR_RESILIENCE=YES/NO**:
   이 옵션은 압축/압축 해제 속도를 높이기 위해 JPEG2000 스트림 또는 특별 코덱(예: 하드웨어 코더 등)의 오류 허용성을 향상시킵니다. 이 옵션은 이미지 품질이 동일한 코드 스트림 생성 시 파일 용량을 약간 늘릴 것입니다. 기본값은 NO입니다.

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

-  **MAIN_MD_DOMAIN_ONLY=YES/NO**:
   (WRITE_METADATA 옵션을 YES로 설정한 경우에만) 주 도메인으로부터 나온 메타데이터만 작성해야 할지 여부를 선택합니다. 기본값은 NO입니다.

-  **USE_SRC_CODESTREAM=YES/NO**:
   (실험적인 옵션입니다!) 소스 데이터셋이 JPEG2000인 경우, 소스 데이터셋의 코드스트림을 수정하지 않은 채 재사용할지 여부를 선택합니다. 기본값은 NO입니다. 이 기능을 활성화하면 JP2 경계 상자의 내용과 소스 코드스트림의 내용이 일관성을 잃을 수도 있습니다. 이 모드에서는 다른 대부분의 생성 옵션을 무시할 것입니다. 지리참조, 메타데이터 등등을 추가하거나 수정하는 몇몇 활용례의 경우 유용할 수도 있습니다.

비손실 압축
~~~~~~~~~~~~~~~~~~~~

REVERSIBLE을 YES로 설정한 (그리고 RATE를 설정하지 않은) 경우 비손실 압축을 사용할 수 있습니다.

벡터 정보
------------------

OGR API를 통해 GML 객체 집합 그리고/또는 KML 주석을 내장한 GMLJP2 v2 경계 상자를 담고 있는 JPEG2000 파일을 벡터 파일로서 열 수 있습니다. 다음은 그 예시입니다:

::

   ogrinfo -ro my.jp2

   INFO: Open of my.jp2'
         using driver `JP2Lura' successful.
   1: FC_GridCoverage_1_rivers (LineString)
   2: FC_GridCoverage_1_borders (LineString)
   3: Annotation_1_poly

객체 집합을 GMLJP2 v2 경계 상자로부터 원격 위치로 링크시킬 수 있습니다. 기본적으로, 링크를 따르지 않습니다. OPEN_REMOTE_GML 열기 옵션을 YES로 설정하면 링크를 따를 것입니다.

버그
----

64비트 리눅스 플랫폼에서 Int32/UInt32/Float32-IEEE754-split 유형 JPEG2000을 지원하려면 SDK 2.1.00.17 이상 버전이 필수입니다.

참고
--------

-  `LuraTech JPEG-2000 SDK <https://www.luratech.com/en/solutions/applications/data-compression-imaging-with-jpeg-2000/>`_

다른 JPEG2000 GDAL 드라이버:

-  :ref:`JP2OpenJPEG: OpenJPEG 라이브러리 기반 (오픈소스) <raster.jp2openjpeg>`

-  :ref:`JPEG2000: 재스퍼 라이브러리 (오픈소스) <raster.jpeg2000>`

-  :ref:`JP2ECW: ERDAS ECW 라이브러리 기반 (상용) <raster.jp2ecw>`

-  :ref:`JP2MRSID: 리저드테크 MrSID 라이브러리 (상용) <raster.jp2mrsid>`

-  :ref:`JP2KAK: 카카두 라이브러리 기반 (상용) <raster.jp2kak>`
