.. _raster.pdf:

================================================================================
PDF -- 지리공간 PDF
================================================================================

.. shortname:: PDF

.. build_dependencies:: 쓰기 지원 의존성은 없음, 읽기 지원의 경우 Poppler/PoDoFo/PDFium 의존성

GDAL은 지리공간 PDF(Geospatial PDF) 문서로부터 지리참조 정보를 추출하고 데이터를 래스터화해서 지리공간 PDF 문서 읽어오기를 지원합니다. 이 드라이버는 지리공간 PDF 문서가 아닌 PDF 문서도 인식할 것입니다.

다른 GDAL 래스터 데이터셋으로부터 PDF 문서를 생성할 수 있으며, OGR 데이터소스가 래스터 레이어 위에 렌더링되도록 선택할 수도 있습니다. (아래 생성 옵션 단락에서 OGR\_\* 옵션들을 참조하십시오.)

이 드라이버는 현재 OGC 인코딩 모범 사례(OGC encoding best practice) 또는 ISO 32000에 대한 어도비 부록(Adobe Supplement to ISO 32000) 두 가지 기존 방식 가운데 하나로 인코딩된 지리참조 정보 읽어오기를 지원합니다.

다중 페이지 문서는 하위 데이터셋으로 -- 문서 1페이지 당 하위 데이터셋 1개로 노출됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

벡터 지원
--------------

:ref:`PDF 벡터 <vector.pdf>` 문서 페이지를 참조하십시오.

메타데이터
---------

(OGC 모범 사례의 경우) 도곽선(neatline)을 또는 (어도비 스타일의) 경계 상자를 NEATLINE 메타데이터 항목으로 리포트할 것이기 때문에, 나중에 왜곡 작업(warping) 알고리즘 용 절단선(cutline)으로 사용할 수 있습니다.

파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.

예를 들어 USGS Topo PDF 같은 파일로부터 추가 메타데이터를 추출할 수 있고, EMBEDDED_METADATA 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.

환경설정 옵션
---------------------

-  :decl_configoption:`GDAL_PDF_DPI`:
   래스터화 DPI를 기본값 150으로 지정해서 래스터 크기를 제어합니다. 이 드라이버는 일부 PDF 파일에 담겨 있는 특정 메타데이터 항목으로부터 DPI 값을 추정하거나, 또는 (단순 작성의 경우) PDF 내부 래스터 이미지로부터 DPI 값을 추정하려고 시도할 것입니다.

-  :decl_configoption:`GDAL_PDF_NEATLINE`:
   선택할 도곽선의 이름입니다. (OGC 인코딩 모범 사례에 따라 인코딩된 지리정보 PDF인 경우에만 사용할 수 있습니다.) USGS Topo PDF의 경우 기본값은 "Map Layers"입니다. 찾을 수 없는 경우 가장 넓은 영역을 커버하는 도곽선을 사용합니다.

-  :decl_configoption:`GDAL_USER_PWD`:
   보안이 걸린 PDF 용 사용자 비밀번호입니다.

-  :decl_configoption:`GDAL_PDF_RENDERING_OPTIONS`:
   벡터, 래스터 또는 텍스트 객체를 렌더링해야 할지 여부를 선택하기 위한, 쉼표로 구분된 VECTOR, RASTER 및 TEXT의 조합입니다. 이 옵션을 지정하지 않는 경우, (Poppler 및 PDFium은) 모든 객체를 렌더링합니다.

-  :decl_configoption:`GDAL_PDF_BANDS`=3 또는 4:
   PDF를 RGB(3) 또는 RGBA(4) 이미지로 렌더링해야 할지를 지정합니다. 기본값은 사용하는 PDF 렌더링과 (Poppler인지 PDFium인지) PDF 파일의 콘텐츠에 따라 달라집니다. (투명도를 가진 이미지를 인식한 경우, 4를 사용할 것입니다.) 3밴드를 선택한 경우, 하얀색을 배경색으로 사용합니다.

-  :decl_configoption:`GDAL_PDF_LAYERS`=레이어 목록 (쉼표 구분):
   쉼표로 구분된 가시화시킬 레이어들의 목록입니다. (또는 "ALL"로 지정하면 모든 레이어가 가시화됩니다.) LAYERS 메타데이터 도메인을 쿼리하면 레이어 이름을 수집할 수 있습니다. 이 옵션을 지정한 경우, (Poppler 및 PDFium은) 명확하게 목록에 있지 않은 레이어들을 숨길 것입니다.

-  :decl_configoption:`GDAL_PDF_LAYERS_OFF`=레이어 목록 (쉼표 구분):
   쉼표로 구분된 숨길 레이어들의 목록입니다. (Poppler 및 PDFium의 경우) LAYERS 메타데이터 도메인을 쿼리하면 레이어 이름을 수집할 수 있습니다.

-  :decl_configoption:`GDAL_PDF_LAUNDER_LAYER_NAMES`=YES/NO: (GDAL 3.1 이상 버전)
   LAYERS 메타데이터 도메인에 리포트된 레이어 이름이 또는 OGR 벡터 레이어 이름이 "세탁"되는 일을 막으려면 NO로 설정하면 됩니다.

열기 옵션
~~~~~~~~~~~~

앞의 환경설정 옵션을 열기 옵션으로도 사용할 수 있습니다.

-  **RENDERING_OPTIONS=[RASTER,VECTOR,TEXT / RASTER,VECTOR / RASTER,TEXT / RASTER / VECTOR,TEXT / VECTOR / TEXT]**:
   GDAL_PDF_RENDERING_OPTIONS 환경설정 옵션과 동일합니다.

-  **DPI=value**:
   GDAL_PDF_DPI 환경설정 옵션과 동일합니다.

-  **USER_PWD=password**:
   GDAL_USER_PWD 환경설정 옵션과 동일합니다.

-  **PDF_LIB=[POPPLER/PODOFO/PDFIUM]**:
   다중 백엔드로 빌드된 경우에만 사용할 수 있습니다.

-  **LAYERS=string**:
   쉼표로 구분된 가시화시킬 레이어들의 목록입니다.
   GDAL_PDF_LAYERS 환경설정 옵션과 동일합니다.

-  **GDAL_PDF_LAYERS_OFF=string**:
   쉼표로 구분된 숨길 레이어들의 목록입니다.
   GDAL_PDF_LAYERS_OFF 환경설정 옵션과 동일합니다.

-  **BANDS=3 또는 4**:
   GDAL_PDF_BANDS 환경설정 옵션과 동일합니다.

-  **NEATLINE=string**:
   도곽선 이름입니다. GDAL_PDF_NEATLINE 환경설정 옵션과 동일합니다.

LAYERS 메타데이터 도메인
----------------------

GDAL을 Poppler 또는 PDFium을 대상으로 컴파일한 경우, 가시성 상태를 끄거나 켤 수 있는 레이어 이름을 수집하기 위해 LAYERS 메타데이터 도메인을 쿼리할 수 있습니다. *GDAL_PDF_LAYERS* 또는 *GDAL_PDF_LAYERS_OFF* 환경설정 옵션에 지정할 값을 알아내는 데 유용합니다.

다음은 그 예시입니다:

::

   $ gdalinfo ../autotest/gdrivers/data/adobe_style_geospatial.pdf -mdd LAYERS

   Driver: PDF/Geospatial PDF
   Files: ../autotest/gdrivers/data/adobe_style_geospatial.pdf
   [...]
   Metadata (LAYERS):
     LAYER_00_NAME=New_Data_Frame
     LAYER_01_NAME=New_Data_Frame.Graticule
     LAYER_02_NAME=Layers
     LAYER_03_NAME=Layers.Measured_Grid
     LAYER_04_NAME=Layers.Graticule
   [...]

   $ gdal_translate ../autotest/gdrivers/data/adobe_style_geospatial.pdf out.tif --config GDAL_PDF_LAYERS_OFF "New_Data_Frame"

제약 조건
------------

(지리참조 정보를 얻기 위해) PDF 문서를 열 때의 속도는 빠르지만, (Poppler의 경우) 래스터 블록에 처음 접근할 때 전체 페이지를 래스터화할 것이기 때문에 속도가 느려질 수 있습니다.

주의: (일부 USGS GeoPDF 파일들처럼) 래스터만 가지고 있는 일부 PDF 파일의 경우, GDAL PDF 드라이버가 정규 타일화된 래스터를 타일화 데이터셋으로 노출시키기 때문에, 어떤 백엔드로도 렌더링할 수 있습니다.

이 드라이버에 현재 매핑된 OGC 모범 사례 사양에서 사용할 수 있는 원점(datum)이 많지 않습니다. 인식할 수 없는 원점은 WGS84 타원제 기반 원점으로 간주할 것입니다.

한 페이지에 도곽선을 여러 개 담고 있는 (삽화가 여러 개인) 문서의 경우, (스크린 관점에서) 가장 넓은 영역을 가지고 있는 삽화로부터 지리참조 정보를 추출할 것입니다.

생성 문제점
---------------

1밴드(회색조 또는 색상표), 3밴드(RGB) 또는 4밴드(RGBA)를 가지고 있는 GDAL 래스터 데이터셋으로부터 PDF 문서를 생성할 수 있습니다.

기본적으로 ISO 32000 사양에 따라 지리참조 정보를 작성할 것입니다. (몇 안 되는 원점과 투영 유형으로 제한되겠지만) OGC 모범 사례 규범에 따라 작성할 수도 있습니다.

주의: PDF 쓰기 지원은 어떤 백엔드와의 링크 작업도 요구하지 않습니다.

생성 옵션
~~~~~~~~~~~~~~~~

-  **COMPRESS=[NONE/DEFLATE/JPEG/JPEG2000]**:
   래스터 데이터에 사용할 압축 방식을 설정합니다. 기본값은 DEFLATE입니다.

-  **STREAM_COMPRESS=[NONE/DEFLATE]**:
   스트림 객체(벡터 도형, 자바스크립트 콘텐츠)에 사용할 압축 방식을 설정합니다. 기본값은 DEFLATE입니다.

-  **DPI=value**:
   사용할 DPI를 설정합니다. 기본값은 72입니다.
   페이지 크기가 애크러뱃이 허용하는 (사용자 단위) 최대 14400값을 초과하지 않도록 더 높은 해상도값으로 자동 조정될 수도 있습니다.

-  **WRITE_USERUNIT=YES/NO**: (GDAL 2.2이상 버전)
   파일에 DPI로부터 계산한 UserUnit 설정을 (UserUnit = DPI / 72.0) 기록해야 할지 여부를 선택합니다.
   UserUnit을 기록하는 경우, 읽기 작업 시 GDAL이 인식하는 픽셀 단위 래스터 크기가 소스 래스터 크기와 동일할 것입니다. UserUnit을 기록하지 않으면 인쇄되는 크기가 DPI 값에 따라 달라질 것입니다. DPI는 지정했는데 이 파라미터를 설정하지 않는 경우, 기본값 NO를 사용할 것입니다. (즉 인쇄되는 크기가 DPI 값에 따라 달라집니다.) 이 파라미터는 설정했는데 DPI를 지정하지 않으면, UserUnit을 기록할 것입니다. (즉 읽기 작업 시 GDAL이 인식하는 픽셀 단위 래스터 크기가 소스 래스터 크기와 동일합니다.)

-  **PREDICTOR=[1/2]**:
   DEFLATE 압축을 사용하는 경우에만 설정할 수 있습니다. 파일 용량을 더 작게 생성할 수 있는 (그러나 항상 그렇지는 않습니다!) 수평 예측 변수를 사용하려면 2로 설정하면 됩니다. 기본값은 1입니다.

-  **JPEG_QUALITY=[1-100]**:
   JPEG 압축을 사용하는 경우 JPEG 품질을 설정합니다.
   100이 최고 품질(최저 압축), 1이 최저 품질(최고 압축)입니다. 기본값은 75입니다.

-  **JPEG2000_DRIVER=[JP2KAK/JP2ECW/JP2OpenJPEG/JPEG2000]**:
   사용할 JPEG2000 드라이버를 설정합니다. 설정하지 않는 경우 목록에서 검색할 것입니다.

-  **TILED=YES**:
   기본적으로 블록 1개로 이루어진 파일을 생성합니다.
   이 옵션을 설정하면 타일화 PDF 파일을 강제로 생성할 수 있습니다.

-  **BLOCKXSIZE=n**:
   타일 너비를 설정합니다. 기본값은 256입니다.

-  **BLOCKYSIZE=n**:
   타일 높이를 설정합니다. 기본값은 256입니다.

-  **CLIPPING_EXTENT=xmin,ymin,xmax,ymax**:
   주 소스 데이터셋 및 선택적인 추가 래스터에 자르기 범위를 설정합니다. 좌표 단위는 데이터셋의 공간 좌표계 단위입니다. 지정하지 않는 경우, 주 소스 데이터셋의 범위를 자르기 범위로 설정합니다.

-  **LAYER_NAME=name**:
   래스터가 배치되는 레이어의 이름입니다. 이 옵션을 지정하는 경우, PDF 판독기의 "레이어 트리"에서 가시성을 켜고 끌 수 있는 레이어에 래스터를 배치할 것입니다.

-  **EXTRA_RASTERS=dataset_ids**:
   페이지에 삽일할, 쉼표로 구분된 지리참조 래스터 목록입니다. 이 래스터들을 주 소스 래스터 위에 출력합니다. 동일한 투영법으로 지리참조되어 있어야만 하며, CLIPPING_EXTENT 옵션을 설정한 경우 자르기 범위에 맞춰 잘려질 것입니다. (CLIPPING_EXTENT 옵션을 설정하지 않았다면 주 소스 래스터의 범위에 맞춰 잘려질 것입니다.)

-  **EXTRA_RASTERS_LAYER_NAME=dataset_names**:
   EXTRA_RASTERS에 지정한 각 래스터의 이름을 쉼표로 구분한 목록입니다. 이 옵션을 지정하는 경우, 지정한 이름으로 명명된 레이어 하나에 해당 이름을 가진 래스터 하나를 각각 배치할 것입니다. 이 레이어들은 PDF 판독기의 "레이어 트리"에서 가시성을 켜고 끌 수 있습니다. 지정하지 않는다면, 기본 레이어에 모든 추가 래스터를 배치할 것입니다.

-  **EXTRA_STREAM=content**:
   영상을 렌더링한 다음 -- 보통 텍스트를 추가하기 위해 -- 렌더링할 PDF 콘텐츠 스트림입니다.
   표준 PDF 1번 유형 글꼴 14개 가운데 어떤 글꼴이든 (하이픈을 생략하고) /FTimesRoman, /FTimesBold, /FHelvetica, /FCourierOblique, ... 형태로 참조할 수도 있습니다. 이때 요청된 리소스 디렉터리를 삽입할 것입니다.

-  **EXTRA_IMAGES=image_file_name,x,y,scale[,link=some_url] (반복 가능)**:
   페이지에 추가 콘텐츠로 삽입할 (지리참조 되지 않은) 이미지 목록입니다. 로고, 범례 등등을 삽입하는 데 유용한 옵션입니다. x 및 y는 페이지의 좌하단 모서리에서 시작하는 사용자 단위 좌표로, 기준점(anchor point)이 이미지의 좌하단 픽셀입니다. 척도(scale)는 확대 비율입니다. (확실하지 않은 경우 1로 설정하십시오.) link=some_url을 지정하는 경우, 이미지를 클릭할 수 있게 됩니다. 이런 이미지를 클릭하면 웹브라우저가 지정한 URL로 열릴 것입니다.

-  **EXTRA_LAYER_NAME=name**:
   EXTRA_STREAM 또는 EXTRA_IMAGES 옵션으로 지정한 추가 콘텐츠를 배치할 레이어의 이름입니다.
   이 옵션을 지정한 경우, PDF 판독기의 "레이어 트리"에서 가시성을 켜고 끌 수 있는 레이어에 추가 콘텐츠를 배치할 것입니다.

-  **MARGIN/LEFT_MARGIN/RIGHT_MARGIN/TOP_MARGIN/BOTTOM_MARGIN=value**:
   이미지 주위에 사용자 단위 여백을 설정합니다.

-  **GEO_ENCODING=[NONE/ISO32000/OGC_BP/BOTH]**:
   사용할 지리 인코딩 메소드를 설정합니다. 기본값은 ISO 32000입니다.

-  **NEATLINE=polygon_definition_in_wkt**:
   사용할 NEATLINE을 설정합니다.

-  **XMP=[NONE/xml_xmp_content]**:
   소스 데이터셋이 'xml:XMP' 메타데이터 도메인에 데이터를 가지고 있는 경우, 이 옵션을 NONE으로 설정하지 않는 이상 기본적으로 산출 PDF에 이 데이터를 복사할 것입니다. 이 옵션에 XMP XML 문자열을 직접 설정할 수도 있습니다.

-  **WRITE_INFO=[YES/NO]**:
   기본적으로, PDF Info 블록에 소스 데이터셋의 해당 메타데이터 항목으로부터 나온 AUTHOR, CREATOR, CREATION_DATE, KEYWORDS, PRODUCER, SUBJECT 및 TITLE 정보를 작성할 것입니다.
   이 옵션을 설정하지 않은 경우 대응하는 생성 옵션으로부터 PDF Info 블록에 앞의 정보를 작성할 것입니다.
   이 옵션을 NO로 설정하면, 어떤 정보도 작성하지 않을 것입니다.

-  **AUTHOR**, **CREATOR**, **CREATION_DATE**, **KEYWORDS**, **PRODUCER**, **SUBJECT**, **TITLE**:
   PDF Info 블록에 작성할 수 있는 메타데이터입니다.
   주의: CREATION_DATE에 설정할 값의 서식이 반드시 D:YYYYMMDDHHmmSSOHH'mm'이어야만 합니다. (예: 2012년 11월 22일 13:24:47 GMT+02는 D:20121122132447+02'00'으로 표현됩니다.)
   (`PDF 참조 문서 1.7버전 <http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf>`_ 의 160페이지를 참조하십시오.)

-  **OGR_DATASOURCE=name**:
   래스터 레이어 위에 출력할 OGR 데이터소스의 이름입니다.

-  **OGR_DISPLAY_FIELD=name**:
   잘 알려진 PDF 뷰어의 "모델 트리" UI 구성요소에 노출될 객체의 라벨을 작성하기 위해 사용할 (OGR 레이어 정의의 필드명과 일치하는) 필드명입니다. 예를 들어, OGR 레이어가 "ID"라는 필드를 가지고 있다면 이 필드를 이 옵션의 값으로 사용할 수 있습니다. "모델 트리"에 있는 객체의 라벨을 "ID" 필드의 값으로 작성할 것입니다.
   이 옵션을 지정하지 않는 경우, 순차적인 일반 라벨을 ("feature1", "feature2", ...) 사용할 것입니다.

-  **OGR_DISPLAY_LAYER_NAMES=names**:
   "모델 트리"에 OGR 레이어를 출력하기 위한, 쉼표로 구분된 레이어 이름 목록입니다. 이 옵션을 지정하지 않는 경우 쓰이는 OGR 레이어 이름 대신 사용자 지정 이름을 지정하는 데 유용한 옵션입니다. 이 옵션을 지정하면, 이름의 개수와 데이터소스에 있는 OGR 레이어들의 개수가 (또한 예를 들어 ogrinfo로 OGR 레이어 목록이 리포트될 때의 순서도) 일치해야 합니다.

-  **OGR_WRITE_ATTRIBUTES=YES/NO**:
   OGR 객체의 속성을 작성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **OGR_LINK_FIELD=name**:
   OGR 객체를 클릭하면 해당 필드값이 지정하는 URL로 웹브라우저를 열기 위해 사용할 (OGR 레이어 정의의 필드명과 일치하는) 필드명을 설정합니다.

-  **OFF_LAYERS=names**:
   처음에는 숨겨야 할, 쉼표로 구분된 레이어 이름 목록입니다. 기본적으로 모든 레이어의 가시성이 켜져 있습니다.
   LAYER_NAME(주 래스터 레이어 이름), EXTRA_RASTERS_LAYER_NAME, EXTRA_LAYER_NAME 및 OGR_DISPLAY_LAYER_NAMES 옵션에 지정한 이름을 설정할 수 있습니다.

-  **EXCLUSIVE_LAYERS=names**:
   한번에 하나만 가시화될 수 있는, 쉼표로 구분된 레이어 이름 목록입니다.
   GUI에서 라디오 버튼의 습성과 동일합니다. LAYER_NAME(주 래스터 레이어 이름), EXTRA_RASTERS_LAYER_NAME, EXTRA_LAYER_NAME 및 OGR_DISPLAY_LAYER_NAMES 옵션에 지정한 이름을 설정할 수 있습니다.

-  **JAVASCRIPT=script**:
   문서를 열 때 실행될 자바스크립트의 내용입니다.
   `애크러뱃(R) 자바스크립트 스크립트 작업 참조 문서 <http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_ 를 참조하십시오.

-  **JAVASCRIPT_FILE=script_filename**:
   문서에 내장되어 문서를 열 때 실행될 자바스크립트 파일의 이름입니다.
   `애크러뱃(R) 자바스크립트 스크립트 작업 참조 문서 <http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_ 를 참조하십시오.

-  **COMPOSITION_FILE=xml_filename**: (GDAL 3.0 이상 버전)
   아래에 있는 "XML 구성 파일로부터 PDF 파일 생성" 단락을 참조하십시오.

기존 파일 업데이트
------------------------

다음 요소들을 설정하거나 업데이트하기 위해 (GDAL이 생성했거나 또는 생성하지 않은) 기존 PDF 파일을 업데이트 모드로 열 수 있습니다:

-  지리변형 및 관련 투영법 (SetGeoTransform() 및 SetProjection() 이용)
-  GCP (SetGCPs() 이용)
-  도곽선 (SetMetadataItem("NEATLINE",polygon_definition_in_wkt) 이용)
-  Info 객체의 내용 (SetMetadataItem(key, value) 이용, 이때 키는 AUTHOR, CREATOR, CREATION_DATE, KEYWORDS, PRODUCER, SUBJECT 및 TITLE 가운데 하나)
-  xml:XMP 메타데이터 (SetMetadata(md, "xml:XMP") 이용)

지리변형 또는 GCP의 경우, 기본적으로 사용하는 지리 인코딩은 ISO 32000입니다. GDAL_PDF_GEO_ENCODING 환경설정 옵션을 OGC_BP로 설정하면 OGC_BP를 선택할 수 있습니다.

업데이트된 요소들은 PDF 사양에서 서술하는 증분 업데이트 메소드에 따라 파일 마지막에 작성됩니다.

XML 구성 파일로부터 PDF 파일 생성 (GDAL 3.0 이상 버전)
--------------------------------------------------------------

다음과 같은 PDF의 구성(composition)을 서술하는 XML 파일로부터 PDF 파일을 생성할 수 있습니다:

-  페이지 수
-  가시성 상태 및 제외 그룹을 가진 레이어 트리
-  페이지 당 0개, 1개 또는 여러 개인 지리참조 영역의 정의
-  래스터, 벡터 또는 라벨로 이루어진 페이지 내용

GDALCreate() API를 width = height = bands = 0 및 datatype = GDT_Unknown으로 사용해야만 하며, 반드시 COMPOSITION_FILE만 단일 생성 옵션으로 사용해야 합니다.

`pdfcomposition.xsd <https://raw.githubusercontent.com/OSGeo/gdal/master/data/pdfcomposition.xsd>`_ XML 스키마를 기준으로 구성 파일을 무결성 검증해야만 합니다.

다음은 API 사용법에 대한 예시입니다:

.. code-block:: c++

   char** papszOptions = CSLSetNameValue(nullptr, "COMPOSITION_FILE", "the.xml");
   GDALDataset* ds = GDALCreate("the.pdf", 0, 0, 0, GDT_Unknown, papszOptions);
   // return a non-null (fake) dataset in case of success, nullptr otherwise.
   GDALClose(ds);
   CSLDestroy(papszOptions);

파이썬 스크립트 샘플 `gdal_create_pdf.py <https://raw.githubusercontent.com/OSGeo/gdal/master/swig/python/gdal-utils/osgeo_utils/samples/gdal_create_pdf.py>`_ 도 이용할 수 있습니다. GDAL 3.2버전부터, :ref:`gdal_create` 유틸리티도 사용할 수 있습니다.

다음은 XML 구성 파일의 예시입니다:

.. code-block:: xml

   <PDFComposition>
       <Metadata>
           <Author>Even</Author>
       </Metadata>

       <LayerTree displayOnlyOnVisiblePages="true">
           <Layer id="l1" name="Satellite imagery"/>
           <Layer id="l2" name="OSM data">
               <Layer id="l2.1" name="Roads" initiallyVisible="false"/>
               <Layer id="l2.2" name="Buildings" mutuallyExclusiveGroupId="group1">
                   <Layer id="l2.2.text" name="Buildings name"/>
               </Layer>
               <Layer id="l2.3" name="Cadastral parcels" mutuallyExclusiveGroupId="group1"/>
           </Layer>
       </LayerTree>

       <Page id="page_1">
           <DPI>72</DPI>
           <Width>10</Width>
           <Height>15</Height>
           <Georeferencing id="georeferenced">
               <SRS dataAxisToSRSAxisMapping="2,1">EPSG:4326</SRS>
               <BoundingBox x1="1" y1="1" x2="9" y2="14"/>
               <BoundingPolygon>POLYGON((1 1,9 1,9 14,1 14,1 1))</BoundingPolygon>
               <ControlPoint x="1"  y="1"  GeoY="48"  GeoX="2"/>
               <ControlPoint x="1"  y="14" GeoY="49"  GeoX="2"/>
               <ControlPoint x="9"  y="1"  GeoY="49"  GeoX="3"/>
               <ControlPoint x="9"  y="14" GeoY="48"  GeoX="3"/>
           </Georeferencing>

           <Content>
               <IfLayerOn layerId="l1">
                   <!-- image drawn, and stretched to (x1,y1)->(x2,y2), without reading its georeferencing -->
                   <Raster dataset="satellite.png" x1="1" y1="1" x2="9" y2="14"/>
               </IfLayerOn>
               <IfLayerOn layerId="l2">
                   <IfLayerOn layerId="l2.1">
                       <Raster dataset="roads.jpg" x1="1" y1="1" x2="9" y2="14"/>
                       <!-- vector drawn with coordinates in PDF coordinate space -->
                       <Vector dataset="roads_pdf_units.shp" layer="roads_pdf_units" visible="false">
                           <LogicalStructure displayLayerName="Roads" fieldToDisplay="road_name"/>>
                       </Vector>
                   </IfLayerOn>
                   <IfLayerOn layerId="l2.2">
                       <!-- image drawn by taking into account its georeferencing -->
                       <Raster dataset="buildings.tif" georeferencingId="georeferenced"/>
                       <IfLayerOn layerId="l2.2.text">
                           <!-- vector drawn by taking into account its georeferenced coordinates -->
                           <VectorLabel dataset="labels.shp" layer="labels" georeferencingId="georeferenced">
                           </VectorLabel>
                       </IfLayerOn>
                   </IfLayerOn>
                   <IfLayerOn layerId="l2.3">
                       <PDF dataset="parcels.pdf">
                           <Blending function="Normal" opacity="0.7"/>
                       </PDF>
                   </IfLayerOn>
               </IfLayerOn>
           </Content>
       </Page>

       <Page id="page_2">
           <DPI>72</DPI>
           <Width>10</Width>
           <Height>15</Height>
           <Content>
           </Content>
       </Page>

       <Outline>
           <OutlineItem name="turn only layer 'Satellite imagery' on, and switch to fullscreen" italic="true" bold="true">
               <Actions>
                   <SetAllLayersStateAction visible="false"/>
                   <SetLayerStateAction visible="true" layerId="l1"/>
                   <JavascriptAction>app.fs.isFullScreen = true;</JavascriptAction>
               </Actions>
           </OutlineItem>
           <OutlineItem name="Page 1" pageId="page_1">
               <OutlineItem name="Important feature !">
                   <Actions>
                       <GotoPageAction pageId="page_1" x1="1" y1="2" x2="3" y2="4"/>
                   </Actions>
               </OutlineItem>
           </OutlineItem>
           <OutlineItem name="Page 2" pageId="page_2"/>
       </Outline>

   </PDFComposition>

빌드 의존성
------------------

GDAL이 읽기 지원을 하려면 GDAL을 다음 라이브러리들 가운데 하나를 대상으로 빌드해야하만 합니다:

-  `Poppler <http://poppler.freedesktop.org/>`_ (GPL 사용 허가)
-  `PoDoFo <http://podofo.sourceforge.net/>`_ (LGPL 사용 허가)
-  `PDFium <https://code.google.com/p/pdfium/>`_ (새로운 BSD 사용 허가, GDAL 2.1.0버전부터 지원)

주의: 이 라이브러리들 가운데 몇 개의 조합을 대상으로 빌드할 수도 있습니다. PDFium을 Poppler보다 우선 사용하고, Poppler를 PoDoFo보다 우선 사용할 것입니다.

유닉스 빌드
~~~~~~~~~~

관련 환경설정 옵션은 다음과 같습니다:

   -  \--with-poppler
   -  \--with-podofo
   -  \--with-podofo-lib
   -  \--with-podofo-extra-lib-for-test

GDAL 2.1.0버전부터 다음 옵션도 사용할 수 있습니다:

   -  \--with-pdfium
   -  \--with-pdfium-lib
   -  \--with-pdfium-extra-lib-for-test
   -  \--enable-pdf-plugin

Poppler
~~~~~~~

libpoppler 자체를 -DENABLE_UNSTABLE_API_ABI_HEADERS=ON 옵션으로 환경설정 해야만 xpdf C++ 헤더를 사용할 수 있습니다.
주의: Poppler C++ API가 불안정하기 때문에, 드라이버를 너무 예전이거나 너무 최신인 Poppler 버전으로 컴파일하는 경우 실패할 수도 있습니다.

PoDoFo
~~~~~~

libpoppler 의존성을 피하려면, PDF 드라이버를 불완전한 대체제인 libpodofo를 대상으로 컴파일할 수 있습니다. PoDoFo 라이브러리는 지리참조 정보 및 벡터 정보를 읽어오기에 충분합니다. 하지만 영상을 읽어오려면 시스템 PATH 환경 변수에 Poppler 배포판에 포함된 pdftoppm 유틸리티를 반드시 지정해야만 합니다.
다음 환경설정 옵션에 따라 결정되는 디렉터리에 임시 파일을 생성할 것입니다(우선 순위 순서입니다):

   -  CPL_TMPDIR
   -  TMPDIR
   -  TEMP

어떤 디렉터리도 정의하지 않는 경우, 현재 디렉터리를 사용할 것입니다.

libpodofo 0.8.4, 0.9.1 및 0.9.3버전이 성공적으로 테스트되었습니다.

중요: PoDoFo 0.9.0버전을 사용하지 말 것을 강력히 권장합니다. 해당 버전의 버그로 인해 GDAL이 멈출 수 있기 때문입니다.

PDFium
~~~~~~

PDFium을 백엔드로 사용하면 래스터, 벡터, 지리참조 정보 및 기타 메타데이터에 접근할 수 있습니다. PDFium 백엔드는 빠른 속도의 축소(zoom out)를 위한 임의의 오버뷰도 지원합니다.

PDFium 안정 빌드를 대상으로 빌드된 GDAL만 테스트되었습니다. PDFium을 빌드하는 작업은 어렵기도 하고, GDAL과 제대로 작동하려면 특정 빌드를 사용해야만 합니다.

GDAL 3.5 이상 버전
+++++++++++++++++

PDFium 패치 버전을 빌드하려면 반드시 `<https://github.com/rouault/pdfium_build_gdal_3_5>`_ 저장소에 있는 스크립트를 이용해야만 합니다.

GDAL 3.4버전
+++++++++++++++++++

PDFium 패치 버전을 빌드하려면 반드시 `<https://github.com/rouault/pdfium_build_gdal_3_4>`_ 저장소에 있는 스크립트를 이용해야만 합니다.

GDAL 3.2 및 3.3버전
+++++++++++++++++++++

PDFium 패치 버전을 빌드하려면 반드시 `<https://github.com/rouault/pdfium_build_gdal_3_2>`_ 저장소에 있는 스크립트를 이용해야만 합니다.

GDAL 3.1.x
+++++++++++++++

PDFium 패치 버전을 빌드하려면 반드시 `<https://github.com/rouault/pdfium_build_gdal_3_1>`_ 저장소에 있는 스크립트를 이용해야만 합니다.

GDAL 2.2.0 이상 3.1 미만 버전
++++++++++++++++++++++++++++

`단순 빌드를 위한 PDFium 포크 버전 <https://github.com/rouault/pdfium>`_ 을 사용할 수 있습니다. (윈도우의 경우, 전용 `win_gdal_build <https://github.com/rouault/pdfium/tree/win_gdal_build>`_ 브랜치를 권장합니다.)

`빌드 저장소 <https://github.com/rouault/pdfium/tree/build>`_ 에서 리눅스/macOS/윈도우 용 PDFium을 빌드하기 위한 템플릿으로 사용할 수 있는 스크립트 몇 개를 사용할 수 있습니다.

이 포크 버전들은 V8 자바스크립트 엔진 의존성을 제거하고, 리눅스 상에서 libjpeg 및 libopenjpeg과의 심볼 충돌을 막기 위해 몇 가지 변경 사항을 적용한 버전입니다.

PDF 드라이버를 GDAL 플러그인으로 빌드하는 것도 이런 문제점들을 피하기 위한 방법 가운데 하나입니다.

PDFium을 빌드하는 것은 물론 GDAL 자체를 PDFium 대상으로 빌드하기 위해서도 C++11 호환 컴파일러가 필요합니다.

성공적으로 테스트된 컴파일러의 버전은 GCC 4.7.0 (이전 버전들은 호환되지 않습니다) 그리고 비주얼 스튜디오 12 및 2013입니다.

예시
--------

-  래스터 2개(main_raster 및 another_raster)로부터 처음에는 main_raster를 출력하고, 한번에 하나만 가시화할 수 있는 PDF를 생성합니다:

   ::

      gdal_translate -of PDF main_raster.tif my.pdf -co LAYER_NAME=main_raster
                     -co EXTRA_RASTERS=another_raster.tif -co EXTRA_RASTERS_LAYER_NAME=another_raster
                     -co OFF_LAYERS=another_raster -co EXCLUSIVE_LAYERS=main_raster,another_raster

-  자바스크립트로 PDF를 생성합니다:

   ::

      gdal_translate -of PDF my.tif my.pdf -co JAVASCRIPT_FILE=script.js

   이때 script.js의 내용은 다음과 같습니다:

   ::

      button = app.alert({cMsg: 'This file was generated by GDAL. Do you want to visit its website ?', cTitle: 'Question', nIcon:2, nType:2});
      if (button == 4) app.launchURL('http://gdal.org/');

참고
--------

-  :ref:`PDF 벡터 <vector.pdf>` 문서 페이지

-  사양:

   -  `OGC GeoPDF 인코딩 모범 사례 2.2버전 (08-139r3) <http://portal.opengeospatial.org/files/?artifact_id=40537>`_
   -  `ISO 32000에 대한 어도비 부록 <http://www.adobe.com/devnet/acrobat/pdfs/adobe_supplement_iso32000.pdf>`_
   -  `PDF 참조 문서 1.7버전 <http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf>`_
   -  `애크러뱃(R) 자바스크립트 스크립트 작업 참조 문서 <http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_

-  라이브러리:

   -  `Poppler 홈페이지 <http://poppler.freedesktop.org/>`_
   -  `PoDoFo 홈페이지 <http://podofo.sourceforge.net/>`_
   -  `PDFium 홈페이지 <https://code.google.com/p/pdfium/>`_
   -  `단순 빌드를 위한 PDFium 포크 버전 <https://github.com/rouault/pdfium>`_

-  샘플:

   -  `몇몇 지리공간 PDF 샘플들 <https://www.terragotech.com/learn-more/sample-geopdfs>`_
   -  `OSM 데이터로부터 지리공간 PDF 맵을 생성하는 예제 <http://latuviitta.org/documents/Geospatial_PDF_maps_from_OSM_with_GDAL.pdf>`_
