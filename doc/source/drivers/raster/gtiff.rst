.. _raster.gtiff:

================================================================================
GTiff -- GeoTIFF 파일 포맷
================================================================================

.. shortname:: GTiff

.. built_in_by_default::

GDAL은 TIFF 및 GeoTIFF 파일의 거의 모든 형식을 읽기 지원하며, 좀 더 적은 변이형들을 쓰기 지원합니다.

GDAL은 BigTIFF 파일 읽기와 쓰기도 지원합니다. (BigTIFF는 TIFF 포맷이 4GB보다 큰 용량의 파일을 지원할 수 있도록 개발된 TIFF 포맷의 진화형입니다.)

현재 읽기와 쓰기를 지원하는 밴드 유형은 Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, CInt16, CInt32, CFloat32 및 CFloat64입니다. 색상표 이미지는 밴드와 관련된 색상표 정보를 반환할 것입니다. 아래 목록에 있는 압축 포맷들도 읽기 지원할 것입니다.

또한 1비트 파일이나 YCbCr 색상 모델 파일 같은 몇몇 특이한 GeoTIFF 변이형 파일들은 자동적으로 RGBA(적색, 녹색, 청색, 알파) 형식으로 변환되어 8비트 밴드 4개로 취급됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

지리참조 작업
--------------

GeoTIFF 투영법을 거의 모두 지원할 것입니다. 다만 흔히 사용되지 않는 투영법으로 변환하거나 지리 좌표계를 OGC WKT로 변환하기 위해서는 PROJ proj.db 데이터베이스를 사용할 수 있어야 합니다. 이 데이터베이스는 PROJ_LIB 환경 변수가 가리키는 위치 또는 OSRSetPROJSearchPaths()를 통해 프로그램 상에서 설정된 위치에 있어야만 합니다.

원격 지점(tiepoint) 1개와 픽셀 크기, 변형 행렬, 또는 지상기준점(GCP) 목록이라는 형태로 GeoTIFF에서의 지리참조 작업을 지원합니다.

TIFF 파일 자체에 사용할 수 있는 지리참조 정보가 없는 경우, GDAL은 .tfw, .tifw/.tiffw 또는 .wld 확장자를 가진 ESRI :ref:`월드 파일 <raster.wld>` 은 물론 MapInfo .tab 파일의 존재를 확인하고 사용할 것입니다.

기본적으로 정보를 다음 순서대로 불러옵니다(첫 항목을 가장 우선하는 순서입니다): PAM(Persistent Auxiliary Metadata) .aux.xml 사이드카 파일(소스 포맷이 지원하지 않는 데이터를 메타데이터로 저장하는 파일), INTERNAL(GeoTIFF 키 및 태그), TABFILE(.tab), WORLDFILE(.tfw, .tifw/.tiffw or .wld).

GDAL 2.2버전부터, GDAL_GEOREF_SOURCES 환경설정 옵션으로 (또는 GEOREF_SOURCES 열기 옵션으로) 사용할 수 있는 소스와 그 우선 순위를 변경할 수 있습니다. 이 옵션의 값은 PAM, INTERNAL, TABFILE, WORLDFILE, NONE이라는 키워드를 쉼표로 구분한 목록입니다. 목록의 첫 항목이 가장 우선되는 소스입니다. 목록에 없는 소스는 무시할 것입니다.

예를 들어 이 옵션을 "WORLDFILE,PAM,INTERNAL"로 설정하면 PAM이나 GeoTIFF보다 잠재적인 월드 파일의 지리변형 행렬을 우선할 것입니다.

GDAL은 `GeoTIFF에서의 RPC <http://geotiff.maptools.org/rpc_prop.html>`_ 확장 사양 제안에서 설명하는 대로 *RPCCoefficientTag* 를 읽고 쓸 수 있습니다. GDALGeoTIFF 기본 프로파일로 생성된 파일에만 이 태그를 작성합니다. 다른 프로파일을 사용하는 경우 .RPB 파일을 생성합니다. GDAL 데이터 모델에서 RPC 계수는 RPC 메타데이터 도메인에 저장됩니다. 더 자세한 내용을 알고 싶다면 :ref:`rfc-22` 을 읽어보십시오. .RPB 또는 \_RPC.TXT 파일이 존재하는 경우, *RPCCoefficientTag* 태그가 설정돼 있더라도 해당 파일로부터 RPC를 읽어올 것입니다.

내부 NODATA 마스크
---------------------

TIFF 파일은 내부 투명도 마스크를 담을 수 있습니다. GeoTIFF 드라이버는 TIFFTAG_SUBFILETYPE 태그에 FILETYPE_MASK 비트 값이 설정된 경우 내부 디렉터리를 투명도 마스크로 인식합니다. TIFF 사양에 따르면 이런 내부 투명도 마스크는 1비트 데이터의 샘플 1개를 담고 있습니다. TIFF 사양이 내부 투명도 마스크에 대해 더 높은 해상도를 허용하긴 하지만, GeoTIFF 드라이버는 주 이미지와 동일한 차원의 내부 투명도 마스크만 지원합니다. 내부 오버뷰의 투명도 마스크도 지원합니다.

GDAL_TIFF_INTERNAL_MASK 환경설정 옵션을 YES로 설정하면 GeoTIFF 파일을 업데이트 모드로 열고, TIFF 데이터셋 또는 래스터 밴드에 CreateMaskBand() 메소드를 이용해서 내부 투명도 마스크를 생성할 것입니다. NO로 설정하는 경우, NODATA 마스크 생성 작업의 기본 습성을 이용할 것입니다. :ref:`rfc-15` 별로 .msk 파일을 생성한다는 뜻입니다.

1비트 내부 마스크 밴드는 DEFLATE 압축됩니다. 내부 마스크 밴드를 다시 읽어올 때 마스크 밴드와 알파 밴드 사이의 변환을 더 쉽게 하기 위해, GDAL_TIFF_INTERNAL_MASK_TO_8BIT 환경설정 옵션을 NO로 설정하지 않는 한, 사용자에게 마스크 밴드를 완전한 8비트로 (예를 들면 마스크되지 않은 픽셀값은 255) 승격시켜 노출합니다. 이 습성은 마스크 밴드 작성 방식에 영향을 미치지 않습니다. (내부 마스크 밴드는 항상 1비트입니다.)

오버뷰
---------

GeoTIFF 드라이버는 내부 오버뷰 읽기, 생성 및 업데이트를 지원합니다. GeoTIFF 파일을 업데이트 모드로 열면 GeoTIFF 파일에 내부 오버뷰를 (이를테면 gdaladdo를 이용해서) 생성할 수 있습니다. GeoTIFF 파일을 읽기전용 모드로 여는 경우, 오버뷰를 외부 .ovr 파일로 생성할 것입니다. BuildOverviews() 메소드로 요청하는 경우에만 오버뷰를 업데이트합니다.

GDAL_TIFF_OVR_BLOCKSIZE 환경설정 변수를 64에서 4096 사이의 2의 거듭제곱 값으로 지정해서 (내부 또는 외부) 오버뷰에 사용되는 블록 크기(타일 너비와 높이)를 지정할 수 있습니다. 기본값은 128인데, GDAL 3.1버전부터는 가능한 경우 (예를 들면 블록 너비와 높이가 같고 64에서 4096 사이의 2의 거듭제곱 숫자인 경우) 동일한 블록 크기를 전체 해상도 데이터셋의 블록 크기로 사용할 수 있습니다.

오버뷰와 NODATA 마스크
--------------------------

오버뷰 및 NODATA 마스크가 내부적인지 아닌지에 따라 다음 환경설정을 보게 될 수 있습니다.

다음 두 경우, 환경설정은 잘 지원됩니다:

-  내부 오버뷰, 내부 NODATA 마스크: GeoTIFF 파일이 내부 투명도 마스크를 가진 경우 (그리고 GDAL_TIFF_INTERNAL_MASK 환경 변수를 NO로 설정하지 않은 경우) GeoTIFF 파일을 업데이트 모드로 열고 BuildOverviews()가 내부 투명도 마스크의 오버뷰를 자동 생성할 것입니다.
-  외부 오버뷰, 외부 NODATA 마스크: GeoTIFF 파일을 읽기전용 모드로 여는 경우 BuildOverviews()가 외부 투명도 마스크의 오버뷰를 (.msk.ovr 파일로) 자동 생성할 것입니다.

다른 두 경우의 습성은 조금 덜 확실합니다:

-  내부 오버뷰, 외부 NODATA 마스크: 업데이트 모드에서 .tif 파일에 BuildOverviews()를 실행하는 경우, 주요 밴드들의 오버뷰만 생성할 것입니다. 외부 .msk 파일의 오버뷰는 BuildOverviews()를 명확하게 .msk 파일에 대해 실행해서 생성해야만 합니다.
-  외부 오버뷰, 내부 NODATA 마스크: 읽기전용 모드에서 .tif 파일에 BuildOverviews()를 실행하는 경우, 주요 밴드들의 오버뷰만 생성할 것입니다. 이 드라이버는 아직 내부 NODATA 마스크의 외부 오버뷰 생성을 지원하지 않습니다.

실용적인 메모: 명령줄 관점에서 보면, BuildOverview()를 업데이트 모드에서 실행한다는 것은 (-ro 옵션을 설정하지 않은) "gdaladdo the.tiff"라는 뜻입니다. 반면에 BuildOverview()를 읽기전용 모드에서 실행한다는 것은 "gdaladdo -ro the.tiff"를 의미합니다.

메타데이터
---------

GDAL은 다음 기초(baseline) TIFF 태그들을 데이터셋 수준 메타데이터로 처리할 수 있습니다:

-  TIFFTAG_DOCUMENTNAME
-  TIFFTAG_IMAGEDESCRIPTION
-  TIFFTAG_SOFTWARE
-  TIFFTAG_DATETIME
-  TIFFTAG_ARTIST
-  TIFFTAG_HOSTCOMPUTER
-  TIFFTAG_COPYRIGHT
-  TIFFTAG_XRESOLUTION
-  TIFFTAG_YRESOLUTION
-  TIFFTAG_RESOLUTIONUNIT
-  TIFFTAG_MINSAMPLEVALUE (read only)
-  TIFFTAG_MAXSAMPLEVALUE (read only)
-  `GEO_METADATA <https://www.awaresystems.be/imaging/tiff/tifftags/geo_metadata.html>`_:
   코드 19139 기반 스키마를 이용해서 준비된 XML 인코딩 인스턴스 문서를 내장시키기 위해 이 태그를 사용할 수도 있습니다. (GeoTIFF DGIWG) (GDAL 2.3 이상 버전)
-  `TIFF_RSID <https://www.awaresystems.be/imaging/tiff/tifftags/tiff_rsid.html>`_:
   이 태그는 DMF 정의에 따라 파일 범용 고유 식별자(File Universal Unique Identifier), 또는 RSID를 지정합니다. (GeoTIFF DGIWG) (GDAL 2.3 이상 버전)

사용할 메타데이터 항목의 이름은 앞의 이름들 ("TIFFTAG_DOCUMENTNAME" 등등) 가운데 하나입니다. 생성 시, 이 태그들을 예를 들면 다음과 같은 명령어로 설정할 수 있습니다:

::

   gdal_translate in.tif out.tif -mo {TAGNAME}=VALUE

GDALGeoTIFF 프로파일(기본값, 아래에 있는 생성 문제점 단락 참조)로 생성된 TIFF에는 다른 비표준 메타데이터 항목들도 저장할 수 있습니다. 이런 메타데이터 항목은 비표준 TIFFTAG_GDAL_METADATA 아스키 태그(코드 42112)에 저장되는 XML 문자열로 그룹화됩니다. BASELINE 또는 GeoTIFF 프로파일을 사용하는 경우, 이런 비표준 메타데이터 항목은 PAM .aux.xml 파일로 저장됩니다.

GDALGeoTIFF 또는 GeoTIFF 프로파일을 사용하는 경우, GDALMD_AREA_OR_POINT("AREA_OR_POINT") 메타데이터 항목은 RasterPixelIsPoint라는 GeoTIFF 키에 저장됩니다.

파일로부터 XMP 메타데이터를 추출할 수 있는데, 추출한 메타데이터를 xml:XMP 메타데이터 도메인의 XML RAW 콘텐츠로 리포트할 것입니다.

파일로부터 EXIF 메타데이터를 추출할 수 있는데, EXIF 메타데이터 도메인에 추출한 메타데이터를 리포트할 것입니다.

색상 프로파일 메타데이터
----------------------

GDAL은 COLOR_PROFILE 도메인에 있는 다음 색상 프로파일 메타데이터를 처리할 수 있습니다:

-  SOURCE_ICC_PROFILE (파일에 내장된 Base64 인코딩 ICC 프로파일. 이 태그가 존재하는 경우 다른 태그들을 무시합니다.)
-  SOURCE_PRIMARIES_RED (적색 우선인 경우 "x,y,1" 서식의 xyY)
-  SOURCE_PRIMARIES_GREEN (녹색 우선인 경우 "x,y,1" 서식의 xyY)
-  SOURCE_PRIMARIES_BLUE (청색 우선인 경우 "x,y,1" 서식의 xyY)
-  SOURCE_WHITEPOINT (화이트 포인트의 경우 "x,y,1" 서식의 xyY)
-  TIFFTAG_TRANSFERFUNCTION_RED (TIFFTAG_TRANSFERFUNCTION의 적색 테이블)
-  TIFFTAG_TRANSFERFUNCTION_GREEN (TIFFTAG_TRANSFERFUNCTION의 녹색 테이블)
-  TIFFTAG_TRANSFERFUNCTION_BLUE (TIFFTAG_TRANSFERFUNCTION의 청색 테이블)
-  TIFFTAG_TRANSFERRANGE_BLACK (TIFFTAG_TRANSFERRANGE의 최소 범위)
-  TIFFTAG_TRANSFERRANGE_WHITE (TIFFTAG_TRANSFERRANGE의 최대 범위)

원본 RAW 픽셀 데이터에서만 이 메타데이터 속성들을 사용할 수 있다는 사실을 기억하십시오. RGB로의 자동 변환이 이루어진 경우, 색상 프로파일 정보를 사용할 수 없습니다.

이 모든 메타데이터 태그들을 무시할 수 있고, 그리고/또는 생성 옵션으로 사용할 수 있습니다.

NODATA 값
------------

기본 GDALGeoTIFF 프로파일로 생성된 파일인 경우, GDAL은 비표준 TIFFTAG_GDAL_NODATA 아스키 태그(코드 42113)에 밴드 NODATA 값을 저장합니다. 모든 밴드가 동일한 NODATA 값을 사용해야만 한다는 사실을 기억하십시오. BASELINE 또는 GeoTIFF 프로파일을 사용하는 경우, NODATA 값은 PAM .aux.xml 파일로 저장됩니다.

희소(sparse) 파일
----------------

GDAL은 오프셋과 바이트 개수가 0으로 설정된 TIFF 타일 또는 스트립, 즉 대응하는 할당된 물리적 저장소가 없는 타일 또는 스트립을 특별하게 해석합니다. 이런 파일을 읽어오는 경우, 이런 타일 또는 스트립이 정의되었을 때 명확하게 0 또는 NODATA 값으로 설정되었다고 간주합니다. 이런 파일을 작성할 때 Create() 인터페이스를 통해 SPARSE_OK 생성 옵션을 YES로 설정하면 이런 타일 또는 스트립 생성을 활성화할 수 있습니다. 그 다음, IWriteBlock()/IRasterIO() 인터페이스를 통해 작성되지 않은 블록들의 오프셋과 바이트 개수를 0으로 설정할 것입니다. 파일의 값을 채우기 위한 이후 처리 과정으로 넘기기 전에 파일을 초기화해야만 하는 경우 이 옵션이 디스크 용량 및 시간을 절약하는 데 특히 유용합니다. 다음 문단에서 논의할 또다른 희소 메커니즘과 혼동하지 않기 위해, 이런 내포 타일/스트립을 가진 파일을 "TIFF 희소 파일"이라고 부를 것입니다. GDAL 기반이 아닌 TIFF 판독기는 이런 파일을 상호 작업할 수 **없을** 것이며, 이런 내포 타일/스트립을 가진 파일을 결함이 있다고 간주할 것입니다.

GDAL 2.2버전부터, 이 메커니즘이 (업데이트 모드를 위해) CreateCopy()는 물론 Open() 인터페이스까지 확장되었습니다. SPARSE_OK 생성 옵션을 (또는 Open()의 경우 SPARSE_OK 열기 옵션을) YES로 설정하면, 모든 0 또는 NODATA 블록을 작성하려는 시도조차 탐지해서 이런 타일 또는 스트립이 물리적 저장소에 할당되지 않도록 할 것입니다. (이미 저장소에 할당되어 있는 경우, 그 내용을 0 또는 NODATA 내용으로 대체할 것입니다.)

GDAL 2.2버전부터, SPARSE_OK를 정의하지 않으면 (또는 기본값 FALSE로 설정하면) NODATA 값이 설정되지 않았거나 0으로 설정된 비압축 파일의 경우, Create() 및 CreateCopy() 모드에서 이 드라이버는 파일의 가장 마지막 부분에 작성하기 위해 그리고 어떤 의미에서는 파일 시스템의 희소 파일 메커니즘과 호환될 수 있도록 (앞에서 논의했던 TIFF 희소 파일 확장 사양과 구별할 수 있도록) 파일이 닫힐 때까지 0값 블록의 할당을 지연시킬 것입니다. 즉 TIFF 관점에서는 모든 비어 있는 블록이 제대로 할당된 것처럼 보이지만 (대응하는 타일/스트립이 무결한 오프셋과 바이트 개수를 가질 것이지만) 대응하는 물리적 저장소는 없을 것입니다. 물론 파일 시스템이 이런 희소 파일을 지원하는 경우에 말입니다. 리눅스의 유명한 파일 시스템 대부분(ext2/3/4, xfs, btfs 등등) 또는 윈도우의 NTFS가 희소 파일을 지원합니다. 파일 시스템이 희소 파일을 지원하지 않는다면 물리적 저장소를 할당하고 0으로 채울 것입니다.

RAW 모드
--------

"이상한" 측광 색 공간(photometric color space)을 가지고 있는 몇몇 TIFF 변이형의 경우, RGBA로 실시간(on-the-fly) 디코딩합니다. 어떤 경우 이런 습성이 바람직하지 않을 수도 있습니다. 파일명 앞에 GTIFF_RAW: 접두어를 붙이면 이 습성을 비활성화시킬 수 있습니다.

예를 들어 CMYK 파일을 다른 파일로 변환한다면:

::

   gdal_translate GTIFF_RAW:in.tif out.tif -co PHOTOMETRIC=CMYK

열기 옵션
------------

-  **NUM_THREADS=number_of_threads/ALL_CPUS**: (GDAL 2.1버전부터) 작업자 스레드의 개수를 지정해서 멀티스레딩 압축을 활성화합니다. DEFLATE 또는 LZMA 같은 느린 압축 알고리즘에 사용해볼 만합니다. 기본값은 주 스레드에서 압축하는 것입니다.

-  **GEOREF_SOURCES=string**: (GDAL 2.2 이상 버전) 사용할 수 있는 지리참조 소스와 그 우선 순위를 정의합니다. `지리참조 작업 <#georeferencing>`_ 단락을 참조하십시오.

-  **SPARSE_OK=TRUE/FALSE**: (GDAL 2.2 이상 버전) 디스크에서 비어 있는 블록을 생략해야 할지 여부를 선택합니다. 이 옵션을 설정한 경우, (파일 안에 대응하는 블록이 이미 할당되어 있는 경우가 아니라면) 모든 픽셀이 0 또는 NODATA 값인 어떤 블록도 작성되지 못 할 것입니다. 희소 파일은 타일/스트립 오프셋이 0인 블록을 작성하지 않기 때문에 디스크 공간을 절약합니다. 하지만, GDAL이 아닌 대부분의 패키지는 이런 파일을 읽어오지 못 합니다. 기본값은 FALSE입니다.

생성 문제점
---------------

복소수 유형을 포함하는 GDAL이 정의하는 모든 밴드 유형으로 GeoTIFF 파일을 생성할 수 있습니다. 생성 파일의 밴드 개수에 제한은 없습니다. 정확히 밴드 3개를 가진 바이트 데이터 유형 파일은 RGB 측광으로 해석될 것이고, 정확히 밴드 4개를 가진 바이트 데이터 유형 파일은 RGBA 측광으로 해석될 것입니다. 반면 다른 모든 조합들은 MIN_IS_BLACK이라는 측광으로 해석될 것입니다. GDAL 2.2버전부터, 생성 및 읽기 시 GDAL 내부 메타데이터 TIFF 태그에 (내재적인 TIFF 케이퍼빌리티를 기준으로) BGR 순서 같은 비표준 밴드 색상 해석을 저장해서 처리할 것입니다.

TIFF 포맷은 색상표(palette 또는 color table)에 R, G, B 구성요소만 지원합니다. 따라서 알파 정보 쓰기는 암묵적으로 폐기될 것입니다.


`클라우드 최적화 GeoTIFF 파일 생성 및 읽기 <https://trac.osgeo.org/gdal/wiki/CloudOptimizedGeoTIFF>`_ 를 위한 힌트를 읽어보십시오.

생성 옵션
~~~~~~~~~~~~~~~~

-  **TFW=YES**: 관련 ESRI 월드 파일(.tfw)을 강제로 생성합니다. 자세한 내용은 :ref:`월드 파일 <raster.wld>` 페이지를 참조하십시오.

-  **RPB=YES**: RPC(Rational Polynomial Coefficients) 정보를 사용할 수 있는 경우 RPC를 설명하는 관련 .RPB 파일을 강제로 생성합니다. 지정하지 않는다면, RPC 정보가 존재하고 PROFILE이 기본값 GDALGeoTIFF가 아닐 때 이 파일을 자동 생성합니다.

-  **RPCTXT=YES**: RPC(Rational Polynomial Coefficients) 정보를 사용할 수 있는 경우 RPC를 설명하는 관련 \_RPC.TXT 파일을 강제로 생성합니다.

-  **INTERLEAVE=[BAND,PIXEL]**: 기본적으로 픽셀이 교차삽입되는 (TIFF 용어로는 PLANARCONFIG_CONTIG) TIFF 파일을 생성합니다. PIXEL 교차삽입은 몇몇 목적을 위해 BAND 교차삽입보다 약간 덜 효율적이지만, 픽셀이 교차삽입된 TIFF 파일만 지원하는 응용 프로그램도 일부 존재합니다.
   GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 가진 다중 밴드 소스 데이터셋으로부터 복사할 때 INTERLEAVE 생성 옵션을 지정하지 않으면, COMPRESS 생성 옵션을 지정하지 않는 이상 소스 데이터셋의 INTERLEAVE를 자동으로 연산에 넣을 것입니다.

-  **TILED=YES**: 기본적으로 스트립화 TIFF 파일을 생성합니다. 타일화 TIFF 파일을 강제로 생성하기 위해 이 옵션을 사용할 수 있습니다.

-  **BLOCKXSIZE=n**: 타일 너비를 설정합니다. 기본값은 256입니다.

-  **BLOCKYSIZE=n**: 타일 또는 스트립 높이를 설정합니다. 타일 높이 기본값은 256이고, 스트립 높이 기본값은 스트립 하나가 8K 미만이 되는 값입니다.

-  **NBITS=n**: 1에서 7 사이의 값을 전송해서 샘플 당 8비트 미만인 파일을 생성합니다. 이때 픽셀 유형은 당연히 바이트형이어야 합니다. n=9...15(UInt16형), n=17...31(UInt32형) 값도 설정할 수 있습니다. GDAL 2.2버전부터, 반정밀도 부동소수점형 값을 생성하기 위한 Float32형에 n=16을 설정할 수 있습니다.

-  **COMPRESS=[JPEG/LZW/PACKBITS/DEFLATE/CCITTRLE/CCITTFAX3/CCITTFAX4/LZMA/ZSTD/LERC/LERC_DEFLATE/LERC_ZSTD/WEBP/JXL/NONE]**: 사용할 압축 방식을 선택합니다.

   * ``JPEG`` 은 일반적으로 (채널 당 8비트인) 바이트 데이터 유형에만 사용해야 합니다. Y, Cb, Cr 구성 요소를 4:2:2로 서브샘플링한 PHOTOMETRIC=YCBCR 색 공간(color space)을 사용하면 RGB 이미지를 더 잘 압축할 수 있습니다.

     GDAL 3.4버전부터, GDAL이 내부 libtiff로 빌드된 경우 (그리고 JPEG 지원도 활성화된 경우) 12비트 샘플을 가진 JPEG 압축 TIFF(JPEG-in-TIFF) 읽기 및 쓰기 지원이 기본적으로 활성화됩니다. 이때 12비트 샘플 지원을 위해 추가적으로 변경된 IJG libjpeg-6b를 기반으로 한 GDAL 내부 libjpeg을 사용합니다. 12비트 샘플을 가진 JPEG 지원은 8비트 JPEG 지원이 내부 IJG libjpeg-6b 또는 (libjpeg-turbo 같은) 외부 libjpeg을 통해 활성화되었는지 여부와는 상관없습니다.

   * ``CCITTFAX3``, ``CCITTFAX4`` 또는 ``CCITRLE`` 압축은 1비트 (NBITS=1) 데이터에만 사용해야 합니다.

   * ``LZW``, ``DEFLATE`` 및 ``ZSTD`` 압축은 PREDICTOR 생성 옵션과 함께 사용할 수 있습니다.

   * ``ZSTD`` 압축은 GDAL 2.3버전부터 내부 libtiff를 사용하고 GDAL이 libzstd 1.0 이상 버전을 대상으로 빌드된 경우 또는 zstd를 지원하는 외부 libtiff를 대상으로 빌드된 경우 사용할 수 있습니다.

   * ``LERC`` 및 ``LERC_DEFLATE`` 압축은 GDAL 3.3.0 미만 버전 용 내부 libtiff를 사용하는 경우에만 사용할 수 있습니다. GDAL 3.3.0버전부터, GDAL이 https://github.com/esri/lerc 대상으로 자체 빌드된 4.3.0버전 이상의 외부 libtiff를 대상으로 빌드된 경우 LERC 압축을 사용할 수 있습니다.

   * ``LERC_ZSTD`` 압축은 ``LERC`` 과 ``ZSTD`` 를 사용할 수 있는 경우 사용할 수 있습니다.

   * ``JXL`` 압축은 JPEG-XL 전용으로, 내부 libtiff를 사용하고 GDAL이 https://github.com/libjxl/libjxl 대상으로 빌드된 경우에만 사용할 수 있습니다.
     JXL 압축은 밴드 4개 이하를 가진 데이터셋에 (기본값인) ``INTERLEAVE=PIXEL`` 과 함께 사용하는 경우가 아니라면 사용할 수 없을 수도 있습니다.

   * ``NONE`` 이 기본값입니다.

-  **NUM_THREADS=number_of_threads/ALL_CPUS**: (GDAL 2.1버전부터) 작업자 스레드의 개수를 지정해서 멀티스레딩 압축을 활성화합니다. DEFLATE 또는 LZMA 같은 느린 압축 알고리즘에 사용해볼 만합니다. 기본값은 주 스레드에서 압축하는 것입니다.

-  **PREDICTOR=[1/2/3]**: LZW, DEFLATE 및 ZSTD 압축을 위한 예측 변수(predictor)를 설정합니다.
   기본값은 1(예측 변수 없음), 2는 수평 차별화(horizontal differencing)이고 3은 부동소수점형 예측 변수입니다.
   PREDICTOR=2는 8, 16, 32 및 64비트 샘플에서만 지원됩니다(libtiff 4.3.0 다음 버전부터 64비트 지원이 추가되었습니다.)
   PREDICTOR=3은 16, 32 및 64비트 부동소수점형 데이터에서만 지원됩니다.

-  **DISCARD_LSB=nbits or nbits_band1,nbits_band2,...nbits_bandN**:
   제거할 최하위 비트(least significant bit)의 개수를 설정합니다. 밴드 별로 다르게 설정할 수도 있습니다. PREDICTOR=2 및 LZW/DEFLATE/ZSTD 압축과 가장 잘 사용할 수 있는 손실 압축 스키마입니다.

-  **SPARSE_OK=TRUE/FALSE**: 
   Create() 인터페이스를 통해 새로 생성되는 파일이 희소 파일이어도 될지 여부를 선택합니다. 희소 파일은 타일/스트립 오프셋이 0인 블록을 작성하지 않기 때문에 디스크 공간을 절약합니다. 하지만, GDAL이 아닌 대부분의 패키지는 이런 파일을 읽어오지 못 합니다. GDAL 2.2버전부터, CreateCopy() 인터페이스를 통해서도 SPARSE_OK=TRUE를 지원합니다. GDAL 2.2버전부터 이 옵션을 설정한 경우, (파일 안에 대응하는 블록이 이미 할당되어 있는 경우가 아니라면) 모든 픽셀이 0 또는 NODATA 값인 어떤 블록도 작성되지 못 할 것입니다. 기본값은 FALSE입니다.

-  **JPEG_QUALITY=[1-100]**: JPEG 압축 사용 시 JPEG 품질을 설정합니다. 값이 100이면 최고 품질(최저 압축), 1이면 최저 품질(최고 압축)입니다. 기본값은 75입니다.

-  **JPEGTABLESMODE=0/1/2/3**: TIFF JpegTables 태그와 타일/스트립에 JPEG 양자화(quantization) 테이블 및 허프먼 코드 테이블을 어떻게 그리고 어디에 작성할지 환경설정합니다. 기본값은 1입니다.

   -  0: JpegTables를 작성하지 않습니다. 각 타일/스트립이 고유 양자화 테이블을 담게 되며 최적화된 허프먼 코딩을 이용합니다.
   -  1: JpegTables를 양자화 테이블만으로 작성합니다. 각 타일/스트립이 이 양자화 테이블들을 참조하며 최적화된 허프먼 코딩을 이용합니다. 일반적으로 이 옵션이 가장 작은 파일 크기에 최적화된 선택이기 때문에 기본값으로 쓰입니다.
   -  2: JpegTables를 기본 허프먼 코드 테이블만으로 작성합니다. 각 타일/스트립이 이 허프먼 테이블들을 참조하며 (따라서 최적화된 허프먼 코딩이 없습니다) 고유의 (동일한) 양자화 테이블을 담게 됩니다. 이 옵션에는 기대되는 실용적인 가치가 없습니다.
   -  3: JpegTables를 양자화 테이블과 기본 허프먼 코드 테이블로 작성합니다. 각 타일/스트립이 이 테이블들을 참조합니다. (따라서 최적화된 허프먼 코딩이 없습니다.) 일부 데이터에서는 이 옵션이 아마도 1보다 더 효율적일 수도 있지만, 그런 경우는 극히 드물 것입니다.

-  **ZLEVEL=[1-9] or [1-12]**: DEFLATE (또는 LERC_DEFLATE) 압축 사용 시 압축 수준을 설정합니다. zlib (또는 LERC_DEFLATE의 경우 libdeflate) 사용 시 9로 (또는 LERC_DEFLATE의 경우 12로) 설정하면 속도는 가장 느리지만 압축률은 가장 높습니다. 1로 설정하면 속도는 가장 빠르지만 압축률은 가장 떨어집니다. 기본값은 6입니다.

-  **ZSTD_LEVEL=[1-22]**: ZSTD (또는 LERC_ZSTD) 압축 사용 시 압축 수준을 설정합니다. 22로 설정하면 속도는 가장 느리지만 압축률은 가장 높습니다. 1로 설정하면 속도는 가장 빠르지만 압축률은 가장 떨어집니다. 기본값은 9입니다.

-  **MAX_Z_ERROR=threshold**: LERC/LERC_DEFLATE/LERC_ZSTD 압축에 대한 최대 오류 한계값을 설정합니다. 기본값은 0(비손실)입니다.

-  **WEBP_LEVEL=[1-100]**: WEBP 압축 사용 시 WEBP 품질을 설정합니다. 값이 100이면 최고 품질(최저 압축), 1이면 최저 품질(최고 압축)입니다. 기본값은 75입니다.

-  **WEBP_LOSSLESS=True/False**: (GDAL 2.4.0 및 libwebp 0.1.4 이상)
   기본적으로 손실 압축 방식을 사용합니다. True로 설정하면 비손실 압축 방식을 사용할 것입니다. 각 타일/스트립에 비손실 WEBP 압축 사용 시 작업 시간이 심각하게 늘어나기 때문에, 스트립 레이아웃의 경우 BLOCKYSIZE를 늘려야 할 수도 있습니다.

-  **JXL_LOSSLESS=YES/NO**: JPEG-XL 압축이 비손실(YES, 기본값)이어야 할지 또는 손실(NO)이어야 할지 여부를 선택합니다. 기저 데이터가 회색조, 회색조+알파, RGB, RBGA 가운데 하나일 때만 손실 압축을 사용해야 합니다.

-  **JXL_EFFORT=[1-9]**: JPEG-XL 압축에 대한 LOE(Level of Effort)를 설정합니다. 값을 높게 설정할수록 파일 용량은 작아지고 압축 시간은 늘어납니다. 기본값은 5입니다.

-  **JXL_DISTANCE=[0.1-15]**: 손실 JPEG-XL 압축에 대한 거리 수준을 설정합니다. 0은 수학적으로 비손실, 1.0은 시각적으로 비손실입니다. 보통 [0.5,3] 범위의 값을 설정할 수 있습니다. 기본값은 1.0입니다.

-  **PHOTOMETRIC=[MINISBLACK/MINISWHITE/RGB/CMYK/YCBCR/CIELAB/ICCLAB/ITULAB]**:
   측광 해석 태그를 설정합니다. 기본값은 MINISBLACK이지만, 입력 이미지가 바이트 유형의 밴드 3개 또는 4개를 가지고 있는 경우 RGB가 선택될 것입니다. 이 옵션으로 기본 측광을 무시할 수 있습니다.

-  **ALPHA=[YES/NON-PREMULTIPLIED/PREMULTIPLIED/UNSPECIFIED]**: 엑스트라 샘플(extra sample)이 하나라도 있을 경우 첫 번째 "ExtraSample"을 알파로 표시합니다. (예를 들어) 알파 밴드를 가진 회색조 TIFF 파일을 생성하려는 경우 이 옵션이 필수입니다. YES는 NON-PREMULTIPLIED 알파를 뜻합니다.

-  **PROFILE=[GDALGeoTIFF/GeoTIFF/BASELINE]**: GDAL이 어떤 비기초(non-baseline) 태그를 내보낼지를 제어합니다.

   -  ``GDALGeoTIFF`` (기본값)로 설정하면 다양한 GDAL 사용자 지정 태그를 작성할 수도 있습니다.
   -  ``GeoTIFF`` 로 설정하면 기초 태그에 GeoTIFF 태그만 추가할 것입니다.
   -  ``BASELINE`` 으로 설정하면 GDAL 또는 GeoTIFF 태그를 작성하지 않을 것입니다. 식별하지 못 하는 태그를 오류로 인식하는 응용 프로그램이 읽게 될 파일을 작성하는 경우 BASELINE이 유용합니다.

-  **BIGTIFF=YES/NO/IF_NEEDED/IF_SAFER**: 파일을 BigTIFF로 생성할지 또는 전형적인 TIFF로 생성할지 제어합니다.

   -  ``YES`` 는 강제로 BigTIFF를 생성합니다.
   -  ``NO`` 는 강제로 전형적인 TIFF를 생성합니다.
   -  ``IF_NEEDED`` 는 분명히 필요한 경우에만 BigTIFF를 생성할 것입니다. (압축하지 않고, 이미지 용량이 4GB를 초과하는 경우. 따라서 이런 경우에는 압축 방법을 지정해도 영향을 미치지 않습니다.)
   -  ``IF_SAFER`` 는 생성되는 파일이 4GB를 *초과할 수도 있는* 경우 BigTIFF를 생성할 것입니다. 주의: 압축률에 따라 동작하지 않을 수도 있는 휴리스틱(heuristic) 옵션입니다.

   BigTIFF란 4GB를 초과하는 데이터를 담을 수 있는 TIFF의 변이형입니다. (전형적인 TIFF의 용량은 4GB를 넘을 수 없도록 제한되어 있습니다.) GDAL이 libtiff 라이브러리 4.0 이상 버전과 함께 빌드된 경우 이 옵션을 사용할 수 있습니다. 기본값은 IF_NEEDED입니다.

   새 GeoTIFF를 압축하지 않고 생성하는 경우, GDAL은 생성될 파일의 용량을 사전에 계산합니다. 이렇게 계산한 파일 용량이 4GB를 초과하면 GDAL은 BigTIFF 파일을 생성하도록 자동으로 결정할 것입니다. 하지만 압축을 사용하는 경우, 파일의 최종 용량을 사전에 알 수는 없기 때문에 전형적인 TIFF를 선택할 것입니다. 이런 경우에 최종 파일이 전형적인 TIFF 파일이 감당하기에는 너무 커질 거라고 예측된다면, 사용자가 BIGTIFF=YES 옵션으로 BigTIFF 생성을 명확하게 요구해야만 합니다. BigTIFF 생성을 명확하게 요구하지 않거나 추정하지 못 했는데 생성된 파일이 전형적인 TIFF 파일이 감당하기에는 너무 큰 경우, libtiff가 "TIFFAppendToStrip:Maximum TIFF file size exceeded" 같은 오류 메시지와 함께 정지할 것입니다.

-  **PIXELTYPE=[DEFAULT/SIGNEDBYTE]**: 이 옵션을 SIGNEDBYTE로 설정하면, 새 바이트 유형 파일을 강제로 부호 있는 바이트 유형으로 작성할 수 있습니다.

-  **COPY_SRC_OVERVIEWS=[YES/NO]**: (CreateCopy() 전용)
   이 옵션을 YES로 설정하면 (기본값은 NO) 소스 데이터셋에 있을 수도 있는 기존 오버뷰를 재계산하지 않은 채 대상 데이터셋에 복사할 것입니다. 주로 클라우드 최적화 Geotiff를 생성하기 위해 이 옵션을 사용합니다. (GDAL 3.1버전부터, :ref:`raster.cog` 드라이버를 사용하면 더 쉽게 클라우드 최적화 Geotiff를 생성할 수 있습니다.) GDAL_TIFF_INTERNAL_MASK 환경설정 옵션을 YES로 설정했는데 마스크 밴드의 오버뷰도 존재하는 경우, 마스크 밴드의 오버뷰도 복사할 것입니다. gdal_translate의 일반 옵션(예: 생성 옵션이 아닌 옵션)을 사용하는 경우 이 생성 옵션은 `어떤 영향도 미치지 못 할 것 <http://trac.osgeo.org/gdal/ticket/3917>`_ 이란 사실을 기억하십시오. 산출 오버뷰에는 압축과 관련된 생성 옵션들도 적용됩니다.

-  **GEOTIFF_KEYS_FLAVOR=[STANDARD/ESRI_PE]**: (GDAL 2.1.0 이상 버전)
   공간 좌표계 정보를 작성하기 위해 어떤 "종류(flavor)"의 GeoTIFF 키를 사용해야만 할지를 결정합니다. 기본값인 STANDARD 방식은 GeoTIFF 키 가운데 일반적으로 받아들여지는 공식 형태(formulation)를 사용할 것입니다. 이 공식 형태는 새로운 EPSG 코드에 ProjectedCSTypeGeoKey로 받아들여지는 값들의 확장 사양을 포함합니다. ESRI_PE 방식은 ArcGIS와 (조금 더) 호환되는 공식 형태를 작성할 것입니다. 산출물 작성 시, ESRI_PE 설정이 가장 효과를 보이는 때는 EPSG:3857 (웹 메르카토르) 공간 좌표계를 작성하는 경우입니다. 다른 공간 좌표계의 경우, STANDARD 방식을 ESRI_PE WKT 문자열을 PCSCitationGeoKey의 값으로 추가해서 사용할 것입니다.

-  **GEOTIFF_VERSION=[AUTO/1.0/1.1]**: (GDAL 3.1.0 이상 버전)
   지리참조 정보를 인코딩하기 위해 쓰이는 GeoTIFF 표준의 버전을 선택합니다.
   ``1.0`` 은 원조 `1995, GeoTIFF Revision 1.0, by Ritter & Ruth <http://geotiff.maptools.org/spec/geotiffhome.html>`_ 입니다.
   ``1.1`` 은 OGC 표준 19-008로, 1.0의 애매했던 표현을 고치고 대부분 좌표계의 수직 부분의 처리 과정에 있던 모순들을 수정한 진화형입니다.
   ``AUTO`` 모드(기본값)는 인코딩할 좌표계가 수직 구성요소를 가지고 있거나 3차원 좌표계가 아니라면 일반적으로 1.0을 선택할 것입니다. 수직 구성요소를 가지고 있거나 3차원 좌표계인 경우 1.1을 선택합니다.

   .. note:: GeoTIFF 1.1의 경우 쓰기를 지원하려면 libgeotiff 1.6.0 이상 버전이 필요합니다.

하위 데이터셋
~~~~~~~~~~~~

다중 페이지 TIFF 파일들을 하위 데이터셋으로 노출시킵니다. 파일을 열 때, 하위 데이터셋의 이름은 GTIFF_DIR:{index}:filename.tif이며 이때 {index}는 1부터 시작합니다.

GDAL 3.0버전부터, APPEND_SUBDATASET=YES 생성 옵션을 이용하면 하위 데이터셋을 생성할 수 있습니다. Create() 또는 CreateCopy()에 전송되는 파일명은 (GTIFF_DIR: 문법을 사용하지 않은) 정규 파일명이어야 합니다. 다중 페이지 TIFF에서의 오버뷰 생성은 지원하지 않습니다.

GDAL 3.2버전부터, 상위 데이터셋 IFD가 `TIFFTAG_SUBIFD <https://www.awaresystems.be/imaging/tiff/tifftags/subifds.html>`_ 태그를 통해 하위 데이터셋의 오버뷰와 마스크를 참조하고 있는 경우 하위 데이터셋의 오버뷰와 마스크에 읽기전용 접근을 할 수 있습니다.

RGB 이미지의 JPEG 압축에 대해
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RGB 이미지를 JPEG 압축 TIFF(JPEG-In-TIFF)로 변환하는 경우, PHOTOMETRIC=YCBCR을 설정하면 기본 측광값(RGB)보다 보통 2배에서 3배 작은 용량의 이미지를 생성할 수 있습니다. PHOTOMETRIC=YCBCR 사용 시, INTERLEAVE 옵션을 기본값(PIXEL)으로 설정해야만 합니다. 그렇지 않으면 libtiff가 데이터를 압축하는 데 실패할 것입니다.

타일 또는 스트립의 크기도 PHOTOMETRIC=RGB의 경우 8의 배수 또는 PHOTOMETRIC=YCBCR의 경우 16의 배수여야만 한다는 사실을 기억하십시오.

JPEG을 JPEG-in-TIFF로 비손실 변환
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

다음 모든 조건을 만족시키는 경우, gdal_translate를 (또는 CreateCopy() API를) 사용하면 압축 해제와 압축 사이클 없이, 즉 추가적인 품질 손실 없이 (JPEG-in-TIFF 파일이 *아닌*) JPEG 파일을 JPEG-in-TIFF 파일로 변환할 수 있습니다:

- 소스 데이터셋이 JPEG 파일입니다. (또는 JPEG을 단일 SimpleSource로서 가지고 있는 VRT입니다.)
- 대상 데이터셋이 JPEG-in-TIFF 파일입니다.
- 대상 JPEG 품질을 명확하게 지정하지 않았습니다.
- 색 공간에 어떤 변경도 지정하지 않았습니다.
- 어떤 하위 창 작업(sub-windowing)도 요청하지 않았습니다.
- 좀 더 일반적으로, 픽셀값을 변경하지 않습니다.

원본 JPEG 이미지로부터 타일화된 JPEG-in-TIFF를 생성할 수 있습니다. 대상 공간 좌표계 및 경계 범위도 명확하게 할당할 수 있습니다.

따라서, 다음 명령어들은 비손실 복사 메소드를 사용할 것입니다:

::

    gdal_translate in.jpg out.tif -co COMPRESS=JPEG

    gdal_translate in.jpg out.tif -co COMPRESS=JPEG -co TILED=YES

    gdal_translate in.jpg out.tif -co COMPRESS=JPEG -a_srs EPSG:4326 -a_ullr -180 90 180 -90


반면 다음 명령어들은 비손실 복사 메소드를 사용하지 *않을* 것입니다. (즉 JPEG 압축해제와 압축 사이클이 발생합니다.):

::

    gdal_translate in.jpg out.tif -co COMPRESS=JPEG -co JPEG_QUALITY=60

    gdal_translate in.jpg out.tif -srcwin 0 0 500 500 -co COMPRESS=JPEG


스트리밍 작업
~~~~~~~~~~~~~~~~~~~~

GeoTIFF 드라이버는 TIFF 파일의 읽기 또는 쓰기를 스트리밍 호환 가능한 방식으로 (아래에서 자세히 설명하는 몇몇 제약들과 함께) 지원할 수 있습니다.

(유닉스의) 지정된 파이프인 /vsistdin/ 으로부터 파일을 읽어올 때, 또는 TIFF_READ_STREAMING 환경설정 옵션을 YES로 설정해서 스트리밍 읽기를 강제하는 경우, GeoTIFF 드라이버는 TIFF IFD(Image File Directory)가 파일의 시작 부분 - 예를 들면 전형적인 TIFF 파일의 경우 오프셋 8 위치 또는 BigTIFF 파일의 경우 오프셋 16 위치에 있다고 가정합니다.
파일의 시작 부분에 - IFD의 마지막 그리고 첫 번째 이미지 타일/스트립 사이에 - 배열 유형의 태그 값들을 담고 있어야만 합니다.
판독기는 타일/스트립이 파일에 작성된 순서대로 타일/스트립을 읽어와야만 합니다.
픽셀 교차삽입 파일의 경우 (PlanarConfiguration=Contig) 작성기를 위한 권장 순서는 - 따라서 판독기를 위한 권장 순서는 - 스트립으로 구성된 파일의 경우 상단에서 하단 순서이고, 또는 타일로 구성된 파일의 경우 상단에서 하단 - 블록 높이의 조각(chunk) - 그리고 좌측에서 우측 순서입니다.
밴드로 구성된 파일의 경우 (PlanarConfiguration=Separate) 첫 번째 밴드의 내용, 두 번째 밴드의 내용, ... 별로 위의 순서를 권장합니다.
엄밀히 말하자면 이 순서는 TileOffsets/StripOffsets 태그의 증가하는 오프셋 순서에 대응합니다.
GDAL 래스터 복사 루틴이 이 순서를 가정할 것입니다.

앞에서 설명한 순서대로인 경우가 아니라면, UNORDERED_BLOCKS=YES 데이터셋 메타데이터 항목이 TIFF 메타데이터 도메인에 설정될 것입니다.
TIFF 메타데이터 도메인에 "BLOCK_OFFSET_[xblock]_[yblock]" 밴드 메타데이터 항목을 쿼리하면 각 블록의 오프셋을 결정할 수 있습니다. (이때 xblock, yblock은 블록의 좌표입니다.) 판독기는 이 정보를 이용해서 이미지 블록에 대한 알맞은 읽기 순서를 결정할 수 있습니다.

GeoTIFF 드라이버가 스트리밍 가능한 산출 모드로 압축 파일을 생성할 수 없다고는 해도, GeoTIFF 드라이버로 스트리밍되는 파일이 압축 파일일 수는 있습니다. (TIFF 파일을 정규 생성하면 이렇게 스트리밍 읽기와 호환 가능한 파일을 생성할 것입니다.)

(유닉스의) 지정된 파이프인 /vsistdin/ 으로부터 파일을 작성할 때, 또는 STREAMABLE_OUTPUT 생성 옵션을 YES로 설정하는 경우, GeoTIFF 드라이버의 CreateCopy() 메소드가 앞에서 정의한 (IFD 위치 및 블록 순서 관련) 제약에 따라 파일을 생성할 것입니다. 이 습성은 비압축 파일을 생성하는 경우에만 지원됩니다.

Create() 메소드도 스트리밍 가능한 호환 파일 생성을 지원하지만, 작성기가 이미지 블록을 작성하기 전에 투영법, 지리변형 또는 메타데이터를 설정하도록 (즉 작성기가 파일의 시작 부분에 IFD를 작성하도록) 주의해야만 합니다.
그리고 이미지 블록을 작성할 때, 블록 순서가 앞에서 설명한 순서 가운데 하나여야만 합니다. 그렇지 않으면 오류를 리포트할 것입니다.


예시:

::

   gdal_translate in.tif /vsistdout/ -co TILED=YES | gzip | gunzip | gdal_translate /vsistdin/ out.tif -co TILED=YES -co COMPRESS=DEFLATE

또는

::

   mkfifo my_fifo
   gdalwarp in.tif my_fifo -t_srs EPSG:3857
   gdal_translate my_fifo out.png -of PNG

주의: 모든 유틸리티가 이런 입력 또는 산출 스트리밍 작업과 호환되지는 않으며, 이런 파일을 처리할 수도 있는 유틸리티라 하더라도 모든 상황에서 처리할 수는 없을 수도 있습니다. 예를 들면 산출 파일을 따르는 읽기 드라이버가 스트리밍되는 입력물의 블록 순서와 호환되지 않을 수도 있습니다.

환경설정 옵션
~~~~~~~~~~~~~~~~~~~~~

이 단락은 GeoTIFF 드라이버의 기본 습성을 변경하기 위해 설정할 수 있는 환경설정 옵션들의 목록입니다.

-  **:decl_configoption:`GTIFF_IGNORE_READ_ERRORS`**:
   이 옵션을 TRUE로 설정하면 libtiff 오류가 GDAL 오류로 바뀌는 일을 막을 수 있습니다. 부분적으로 손상된 TIFF 파일을 읽어오는 데 도움이 될 수도 있습니다.

-  **:decl_configoption:`ESRI_XML_PAM`**:
   이 옵션을 TRUE로 설정하면 xml:ESRI 도메인에 있는 메타데이터를 강제로 PAM에 작성할 수 있습니다.

-  **:decl_configoption:`COMPRESS_OVERVIEW`**:
   `생성 옵션의 COMPRESS <#creation-options>`_ 항목을 참조하십시오. 오버뷰에 사용할 압축 유형을 설정합니다.

-  **:decl_configoption:`PHOTOMETRIC_OVERVIEW`**:
   YCBCR입니다. 오버뷰 생성 시 사용할 측광 색 공간을 설정합니다.

-  **:decl_configoption:`PREDICTOR_OVERVIEW`**:
   정수 1, 2 또는 3입니다. LZW, DEFLATE 및 ZSTD로 압축된 오버뷰에 사용할 예측 변수를 설정합니다.

-  **:decl_configoption:`JPEG_QUALITY_OVERVIEW`**:
   0에서 100 사이의 정수입니다. 기본값은 75입니다. JPEG으로 압축된 내부 또는 외부 오버뷰의 품질 수준을 설정합니다.

-  **:decl_configoption:`WEBP_LEVEL_OVERVIEW`**:
   0에서 100 사이의 정수입니다. 기본값은 75입니다. WEBP로 압축된 내부 또는 외부 오버뷰의 품질 수준을 설정합니다.

-  **:decl_configoption:`ZLEVEL_OVERVIEW`**:
   1에서 9 (또는 libdeflate 사용 시 12) 사이의 정수입니다. 기본값은 6입니다. COMPRESS_OVERVIEW=DEFLATE 또는 LERC_DEFLATE 사용 시 내부 또는 외부 오버뷰의 DEFLATE 압축 수준을 설정합니다. GDAL 3.4.1부터 추가되었습니다.

-  **:decl_configoption:`ZSTD_LEVEL_OVERVIEW`**:
   1에서 22 사이의 정수입니다. 기본값은 9입니다. COMPRESS_OVERVIEW=ZSTD 또는 LERC_ZSTD 사용 시 내부 또는 외부 오버뷰의 ZSTD 압축 수준을 설정합니다. GDAL 3.4.1부터 추가되었습니다.

-  **:decl_configoption:`MAX_Z_ERROR_OVERVIEW`**:
   부동소수점형 값입니다. 기본값은 0(비손실)입니다. 내부 또는 외부 오버뷰의 LERC/LERC_DEFLATE/LERC_ZSTD 압축에 대한 최대 오류 한계값입니다. GDAL 3.4.1부터 추가되었습니다.

-  **:decl_configoption:`SPARSE_OK_OVERVIEW`**:
   불(Boolean) 값입니다. 기본값은 OFF입니다. ON으로 설정하면, 픽셀이 모두 NODATA (또는 NODATA가 정의되지 않은 경우 0) 값인 블록을 작성하지 않을 것입니다. GDAL 3.4.1부터 추가되었습니다.

-  **:decl_configoption:`GDAL_TIFF_INTERNAL_MASK`**:
   `내부 NODATA 마스크 <#internal-nodata-masks>`_ 단락을 참조하십시오. 기본값은 FALSE입니다.

-  **:decl_configoption:`GDAL_TIFF_INTERNAL_MASK_TO_8BIT`**:
   `내부 NODATA 마스크 <#internal-nodata-masks>`_ 단락을 참조하십시오. 기본값은 TRUE입니다.

-  **:decl_configoption:`USE_RRD`**:
   이 옵션을 TRUE로 설정하면 RRD 포맷으로 된 외부 오버뷰를 강제로 생성할 수 있습니다. 기본값은 FALSE입니다.

-  **:decl_configoption:`TIFF_USE_OVR`**:
   이 옵션을 TRUE로 설정하면 GeoTIFF(.ovr) 포맷으로 된 외부 오버뷰를 강제로 생성할 수 있습니다. 기본값은 FALSE입니다.

-  **:decl_configoption:`GTIFF_POINT_GEO_IGNORE`**:
   이 옵션을 TRUE로 설정하면 예전 GDAL 버전들이 지리변형에 따라 PixelIsPoint를 해석하는 방법에 관한 습성으로 돌아갈 수 있습니다. 자세한 내용은 :ref:`rfc-33` 을 참조하십시오. 기본값은 FALSE입니다.

-  **:decl_configoption:`GTIFF_REPORT_COMPD_CS`**:
   이 옵션을 TRUE로 설정하면 파일의 공간 좌표계를 읽어올 때 복합 좌표계의 수직 좌표계가 제거되는 일을 막을 수 있습니다. 쓰기 향에는 영향을 미치지 않습니다. GeoTIFF 1.0 파일의 경우 기본값은 FALSE이고, (GDAL 3.1버전부터) GeoTIFF 1.1 파일의 경우 기본값은 TRUE입니다.

-  **:decl_configoption:`GDAL_ENABLE_TIFF_SPLIT`**:
   이 옵션을 FALSE로 설정하면 단일 스트립에 모든 데이터를 담고 있는(all-in-one-strip) 파일이 ?????로 나타나는 일을 막을 수 있습니다. 기본값은 TRUE입니다.

-  **:decl_configoption:`GDAL_TIFF_OVR_BLOCKSIZE`**:
   `Overviews <#overviews>`_ 단락을 참조하십시오.

-  **:decl_configoption:`GTIFF_LINEAR_UNITS`**:
   이 옵션을 BROKEN으로 설정하면 좌표계 선형 단위여야 할 거짓 편동/편북이 엉뚱하게 미터 단위로 되어 있는 GeoTIFF 파일을 읽어올 수 있습니다. (`Ticket #3901 <http://trac.osgeo.org/gdal/ticket/3901>`_)

-  **:decl_configoption:`TAB_APPROX_GEOTRANSFORM` =YES/NO**:
   .tab 파일을 읽어올 때 근사치 지리변형을 허용할 것인지 여부를 결정합니다. 기본값은 NO입니다.

-  **:decl_configoption:`GTIFF_DIRECT_IO` =YES/NO**:
   이 옵션을 YES로 설정하면 비압축 TIFF 파일을 읽어올 때 (GDAL 2.0까지는 타일화되지 않은 파일만, GDAL 2.1부터는 타일화되지 않은 파일과 타일화 파일 모두) 블록 캐시 사용을 피하기 위해 특화된 RasterIO() 구현을 사용할 수 있습니다.
   최적화된 작업이 적용되지 않는 경우에도 YES 설정은 안전할 것입니다. (일반 RasterIO() 구현을 사용할 것입니다.) 기본값은 NO입니다.

-  **:decl_configoption:`GTIFF_VIRTUAL_MEM_IO` =YES/NO/IF_ENOUGH_RAM**:
   이 옵션을 YES로 설정하면 비압축 TIFF 파일을 읽어올 때 블록 캐시 사용을 피하기 위해 특화된 RasterIO() 구현을 사용할 수 있습니다.
   이 구현은 메모리 매핑 파일 I/O에 의존하며, 현재 리눅스에서만 지원됩니다. (64비트 빌드를 강력히 권장합니다.) 또는 GDAL 2.1버전부터 다른 POSIX 계열 시스템에서도 지원됩니다.
   최적화된 작업이 적용되지 않는 경우에도 YES 설정은 안전할 것입니다. (일반 RasterIO() 구현을 사용할 것입니다.) 그러나 파일 용량이 RAM 용량을 초과할 때 전체 파일을 읽어오는 경우 디스크 스왑이 발생할 수도 있습니다.
   이 옵션을 IF_ENOUGH_RAM으로 설정하면 가장 먼저 비압축 파일 용량이 물리적 메모리 용량을 초과하지 않는지 확인할 것입니다.
   기본값은 NO입니다.
   GTIFF_VIRTUAL_MEM_IO과 GTIFF_DIRECT_IO 둘 다 활성화하는 경우, 전자를 우선 사용합니다. 전자를 사용할 수 없다면 후자를 시도합니다.

-  **:decl_configoption:`GDAL_GEOREF_SOURCES` =comma-separated list**:
   PAM, INTERNAL, TABFILE 또는 WORLDFILE 가운데 하나 또는 여러 개를 쉼표로 구분한 목록입니다. GDAL 2.2부터 추가되었습니다. `지리참조 작업 <#georeferencing>`_ 단락을 참조하십시오.

-  **:decl_configoption:`GDAL_NUM_THREADS` =number_of_threads/ALL_CPUS**:
   (GDAL 2.1버전부터) 작업자 스레드의 개수를 지정해서 멀티스레딩 압축을 활성화합니다. DEFLATE 또는 LZMA 같은 느린 압축 알고리즘에 사용해볼 만합니다. JPEG 압축을 사용하는 경우 이 옵션을 무시할 것입니다. 기본값은 주 스레드에서 압축하는 것입니다.
   주의: 이 환경설정 옵션은 GDAL의 다른 부분(왜곡 작업, 그리드 작업 등등)에도 적용됩니다.

-  **:decl_configoption:`GTIFF_WRITE_TOWGS84` =AUTO/YES/NO**:
   (GDAL 3.0.3부터) 이 옵션을 AUTO로 설정하면, 좌표계에 첨부된 EPSG 코드가 없는 경우 또는 좌표계에 첨부된 TOWGS84 변환이 EPSG 코드로부터 가져온 TOWGS84 변환과 일치하지 않는 경우, GeogTOWGS84GeoKey 지리 키(geokey)를 TOWGS84 3 또는 파라미터 7개를 사용하는 헬메르트 변환과 함께 작성할 것입니다.
   YES로 설정하면, 항상 좌표계에 첨부된 TOWGS84 변환을 작성할 것입니다.
   NO로 설정하면, 어떤 상황에도 변환 정보를 작성하지 않을 것입니다.

참고
--------

-  `GeoTIFF 정보 페이지 <https://trac.osgeo.org/geotiff>`_
-  `libtiff 페이지 <http://www.simplesystems.org/libtiff/>`_
-  `BigTIFF 파일 포맷에 대한 상세 정보 <http://www.awaresystems.be/imaging/tiff/bigtiff.html>`_
-  :ref:`raster.cog` 드라이버

.. toctree::
   :maxdepth: 1
   :hidden:

   wld
