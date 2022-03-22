.. _raster.jpeg:

================================================================================
JPEG -- JPEG JFIF 파일 포맷
================================================================================

.. shortname:: JPEG

.. build_dependencies:: (내부 libjpeg 제공)

JPEG JFIF 포맷은 읽기와 배치(batch) 쓰기를 지원하지만, 제자리(in place) 업데이트는 지원하지 않습니다. JPEG 파일은 바이트형 값을 가진 1밴드(회색조) 또는 3밴드(RGB) 데이터셋으로 표현됩니다.

이 드라이버는 GDAL_JPEG_TO_RGB 옵션을 (기본값 YES가 아닌) NO로 설정하지 않는 이상 YCbCr, CMYK 또는 YCbCrK 색 공간을 가진 이미지를 RGB로 자동 변환할 것입니다. RGB로의 색 공간 변환이 끝나면, IMAGE_STRUCTURE 도메인의 SOURCE_COLOR_SPACE 메타데이터에 소스 색 공간을 기록합니다.

JPEG 파일로부터 EXIF 메타데이터를 읽어올 수 있습니다. (그러나 EXIF_GPSLatitude 및 EXIF_GPSLongitude 태그를 설정했더라도 지리참조된 이미지를 생성하지는 않을 것입니다.) 그러나 .jgw, .jpgw/.jpegw 또는 .wld 확장자를 가진 ESRI 월드 파일이 존재하는 경우, 월드 파일을 읽어와서 이를 이용해 이미지에 지리변형을 적용할 것입니다. 사용할 수 있는 경우, MapInfo .tab 파일도 지리참조 작업에 이용할 것입니다. JPEG 파일의 오버뷰는 외부 .ovr 파일로 작성할 수 있습니다.

이 드라이버는 몇몇 데이터 제공자가 픽셀이 무결하지 않은 데이터인지 식별하기 위한 비트 마스크(bit mask)를 추가하기 위해 사용하는 "파일에 첨부된 ZLib 압축 마스크" 접근법도 지원합니다. 더 자세한 내용은 :ref:`rfc-15` 를 참조하십시오.

이 드라이버는 비트들이 최상위 비트(most significant bit)가 맨 앞에 오는 순서대로 정렬된 비트 마스크도 처리할 수 있습니다. (반면 일반적인 규범은 최하위 비트(least significant bit)가 맨 앞에 오는 순서입니다.) 이 드라이버는 이런 상황을 자동 탐지하려 할 것이지만, 이런 휴리스틱 방식이 실패할 수도 있습니다. 그런 경우, JPEG_MASK_BIT_ORDER 환경설정 옵션을 MSB로 설정하면 됩니다. JPEG_READ_MASK 옵션을 NO로 설정하면 비트 마스크를 완전히 무시할 수도 있습니다.

GDAL JPEG 드라이버는 독립 JPEG 그룹의 JPEG 라이브러리를 이용해서 빌드됩니다. GeoTIFF 드라이버가 JPEG 압축 타일을 가진 타일화 TIFF를 지원한다는 사실도 기억하십시오. 이 사실을 이용하면 단일 JPEG 이미지의 경우 최대 65,535x65,535 픽셀 크기를 초과하는 데이터셋에 JPEG 압축을 적용할 수 있습니다.

JPEG 드라이버를 libjpeg-turbo, libjpeg의 어떤 버전, 그리고 기준(baseline) JPEG 압축/압축 해제 속도를 높이기 위해 MMX, SSE 및 SSE2 SIMD 지침을 사용하는 IJG libjpeg-6b와 호환되는 API 및 ABI와 함께 사용할 수도 있습니다.

GDAL 3.4버전부터, (JPEG 지원도 활성화된 경우) 12비트 샘플링된 JPEG 이미지 읽기 및 쓰기 지원도 (12비트 샘플링 지원을 위해 추가적으로 수정된 IJG libjpeg-6b 기반) GDAL 내부 libjpeg을 이용해서 기본적으로 활성화됩니다. 내부 IJG libjpeg-6b 또는 (libjpeg-turbo 같은) 외부 libjpeg을 통해 8비트 JPEG 지원이 활성화되었는지에 관계 없이, 12비트 샘플링된 JPEG을 지원합니다.

파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.

GDAL이 (JPEG 압축된) 내장 EXIF 섬네일을 생성할 수 있는데, 이 섬네일을 오버뷰로 사용할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

색상 프로파일 메타데이터
----------------------

GDAL은 COLOR_PROFILE 도메인에 있는 다음 색상 프로파일 메타데이터를 처리할 수 있습니다:

-  SOURCE_ICC_PROFILE (파일에 내장된 Base64 인코딩 ICC 프로파일입니다.)

원본 RAW 픽셀 데이터에서만 이 메타데이터 속성을 사용할 수 있다는 사실을 기억하십시오.
RGB로 자동 변환이 끝난 경우, 색상 프로파일 정보를 사용할 수 없습니다.

이 메타데이터 태그를 생성 옵션으로 사용할 수 있습니다.

오류 관리
----------------

libjpeg은 디코딩 도중 JPEG 데이터스트림의 일부 오류를 허용할 수 있으며 가능한 한 오류로부터 회복하려 시도할 것입니다. 이런 오류는 GDAL 경고로서 리포트되지만, GDAL_ERROR_ON_LIBJPEG_WARNING 환경설정 옵션을 TRUE로 설정하면 이런 오류를 진짜 오류로 간주하도록 선택할 수 있습니다.

생성 옵션
----------------

JPEG 파일은 "JPEG" 드라이버 코드를 이용해서 생성됩니다. 바이트형 밴드 유형만 지원합니다. 다음과 같은 환경설정을 지원합니다:

   - 1밴드: 회색조
   - 3밴드: 입력물이 RGB 색 공간을 사용해야 합니다. 드라이버가 저장을 위해 YCbCr 색공간으로 자동 변환하고, 읽기 시 다시 RGB로 노출시킬 것입니다.
   - 4밴드: 입력물이 이미 CMYK 색 공간을 사용해야 합니다. :decl_configoption:`GDAL_JPEG_TO_RGB` 환경설정 옵션을 NO로 설정하지 않는 이상 읽기 시 RGB로 노출시킬 것입니다.

JPEG 파일 생성은 배치 (CreateCopy) 메소드로 구현되었습니다. 생성 시 YCbCrK 색 공간은 지원하지 않습니다. 소스 데이터셋이 NODATA 마스크를 가지고 있는 경우, JPEG 파일에 ZLib 압축 마스크로 첨부할 것입니다.

-  **WORLDFILE=YES**:
   관련 ESRI 월드 파일(.wld)을 강제로 생성합니다.

-  **QUALITY=n**:
   기본적으로 품질 플래그는 75로 설정되어 있지만, 이 옵션을 사용하면 다른 값을 선택할 수 있습니다. 10에서 100 사이의 값이어야만 합니다. 낮은 값으로 설정하면 높은 압축률을 보이지만 이미지 품질은 떨어집니다. 값이 95를 넘게 되면 의미 있는 품질 향상이 이루어지지는 않지만 용량이 훨씬 커질 수 있습니다.

-  **PROGRESSIVE=ON**:
   진행형(progressive) JPEG 생성을 활성화합니다. 몇몇 경우 웹브라우저 같은 뷰어에서 파일 전체를 다운로드하기 전에 이미지 해상도가 떨어져 보이기도 할 것입니다. 하지만 진행형 JPEG을 전혀 읽지 못 하는 응용 프로그램도 몇 있습니다. GDAL은 진행형 JPEG을 읽을 수 있지만, 그 진행형 성질을 활용하지는 못 합니다.

-  **INTERNAL_MASK=YES/NO**:
   필요한 경우, 픽셀이 무결하지 않은 데이터인지 식별하기 위해 기본적으로 내부 마스크를 "파일에 첨부된 ZLib 압축 마스크" 접근법으로 작성합니다. 이 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

-  **ARITHMETIC=YES/NO**:
   산술 코딩을 활성화합니다. 법적 제약이 있을 수 있기 때문에 모든 libjpeg 빌드에서 활성화되지 않을 수도 있습니다.
-  **BLOCK=1...16**:
   (libjpeg 8c 이상 버전) DCT 블록 크기입니다. 1에서 16 사이의 모든 값을 설정할 수 있습니다. 기본값은 8(기준(baseline) 포맷)입니다. 8이 아닌 다른 값으로 설정하면 libjpeg 8c 이전 버전과 호환되지 않는 파일을 생성할 것입니다.

-  **COLOR_TRANSFORM=RGB or RGB1**:
   (libjpeg 9 이상 버전) 비손실 RGB를 위해 RGB1으로 설정하십시오.
   주의: RGB1으로 설정하면 libjpeg 9 이전 버전과 호환되지 않는 파일을 생성할 것입니다.

-  **SOURCE_ICC_PROFILE=value**:
   Base64로 인코딩된 ICC 프로파일입니다.

-  **COMMENT=string**:
   주석 JPEG 마커에 내장할 문자열입니다. 읽기 시, COMMENT 메타데이터 항목에 이런 문자열을 노출시킬 것입니다.

-  **EXIF_THUMBNAIL=YES/NO**:
   자체 JPEG 압축된 EXIF 섬네일(오버뷰)을 생성할지 여부를 선택합니다. 기본값은 NO입니다. 활성화하는 경우, THUMBNAIL_WIDTH 또는 THUMBNAIL_HEIGHT 둘 다 지정하지 않는 이상 섬네일의 최대 크기는 128이 될 것입니다.

-  **THUMBNAIL_WIDTH=n**:
   섬네일의 너비를 지정합니다. EXIF_THUMBNAIL을 YES로 설정한 경우에만 연산에 넣습니다.

-  **THUMBNAIL_HEIGHT=n**:
   섬네일의 높이를 지정합니다. EXIF_THUMBNAIL을 YES로 설정한 경우에만 연산에 넣습니다.

-  **WRITE_EXIF_METADATA=YES/NO**:
   (GDAL 2.3버전부터) EXIF 부분에 EXIF_xxxx 메타데이터를 작성할지 여부를 선택합니다.기본값은 YES입니다.

EXIF 및 GPS 태그
-----------------

다음 표들은 작성할 수 있는 EXIF 및 GPS 태그들의 목록입니다.

-  "메타데이터 항목 이름" 열은 소스 데이터셋에 추가할 메타데이터 항목의 이름입니다.
-  "헥스 코드" 열은 대응하는 TIFF EXIF/GPS 태그의 값입니다. (참조 전용)
-  "유형" 열은 관련 TIFF 유형입니다.

   -  ASCII는 널 종단(NULL-terminated) 텍스트 값을 의미합니다. (고정 길이 태그의 경우, 길이에 이 널 종단 문자가 포함됩니다.) 예: EXIF_Make=the_make
   -  BYTE/UNDEFINED는 어떤 바이트 값으로도 이루어질 수 있는 값입니다. 대응하는 GDAL 메타데이터 항목의 값이 EXIF_GPSVersionID=0x02 0x00 0x00 0x00 같은 16진수 서식 값의 문자열이어야만 합니다. GDAL은 EXIF_ExifVersion=0231 같은 ASCII 문자열도 입력받습니다.
   -  SHORT은 [0,65535] 범위의 부호 없는 정수값입니다. 일부 태그는 값 여러 개를 설정할 수 있는데, 이때 공백으로 구분해야만 합니다.
   -  LONG은 [0,4294967295] 범위의 부호 없는 정수값입니다. 일부 태그는 값 여러 개를 설정할 수 있는데, 이때 공백으로 구분해야만 합니다.
   -  RATIONAL은 양의 부동소수점형 값입니다. 일부 태그는 값 여러 개를 설정할 수 있는데, 이때 EXIF_GPSLatitude=49 2 3.5와 같이 공백으로 구분해야만 합니다.
   -  SRATIONAL은 양 또는 음의 부동소수점형 값입니다. 일부 태그는 값 여러 개를 설정할 수 있는데, 이때 공백으로 구분해야만 합니다.

   고정 개수의 값을 받는 항목에 고정 개수보다 많은 값들을 설정하는 경우, 경고과 함께 값들을 잘라낼(truncate) 것입니다. 필요한 개수보다 적은 값들을 설정하는 경우, 뒤를 알맞은 공백과 0들로 채울 것입니다.

-  "값의 개수" 열은 항목이 받는 값의 개수입니다. 제약 조건이 없다면 "가변(variable)"일 수도 있고, 아니면 고정값일 수도 있습니다. 유형이 ASCII인 경우 고정값이 널 종단 바이트를 포함하기 때문에, 실제로 출력 가능한 문자의 개수는 값의 개수에서 1을 뺀 숫자입니다.
-  "선택성" 열은 항목이 존재해야 하는지("필수(mandatory)"), "권장(recommended)" 또는 "선택적(optional)"인지 나타냅니다. GDAL은 이 선택성을 강제하지 않습니다.

많은 항목들이 다음 표에서 볼 수 없는 무결한 콘텐츠에 대한 제약 조건을 더 많이 가지고 있습니다. 자세한 정보를 원한다면 EXIF 사양 문서를 읽어보십시오.

============================== ======== ========= ================ =============
메타데이터 항목 이름            헥스코드 유형       값의 개수        선택성
============================== ======== ========= ================ =============
EXIF_Document_Name             0x010D   ASCII     가변             선택적
EXIF_ImageDescription          0x010E   ASCII     가변             권장
EXIF_Make                      0x010F   ASCII     가변             권장
EXIF_Model                     0x0110   ASCII     가변             권장
EXIF_Orientation               0x0112   SHORT     1                권장
EXIF_XResolution               0x011A   RATIONAL  1                **필수**
EXIF_YResolution               0x011B   RATIONAL  1                **필수**
EXIF_ResolutionUnit            0x0128   SHORT     1                **필수**
EXIF_TransferFunction          0x012D   SHORT     768              선택적
EXIF_Software                  0x0131   ASCII     가변             선택적
EXIF_DateTime                  0x0132   ASCII     20               권장
EXIF_Artist                    0x013B   ASCII     가변             선택적
EXIF_WhitePoint                0x013E   RATIONAL  2                선택적
EXIF_PrimaryChromaticities     0x013F   RATIONAL  6                선택적
EXIF_YCbCrCoefficients         0x0211   RATIONAL  3                선택적
EXIF_YCbCrPositioning          0x0213   SHORT     1                **필수**
EXIF_ReferenceBlackWhite       0x0214   RATIONAL  6                선택적
EXIF_Copyright                 0x8298   ASCII     가변             선택적
EXIF_ExposureTime              0x829A   RATIONAL  1                권장
EXIF_FNumber                   0x829D   RATIONAL  1                선택적
EXIF_ExposureProgram           0x8822   SHORT     1                선택적
EXIF_SpectralSensitivity       0x8824   ASCII     가변             선택적
EXIF_ISOSpeedRatings           0x8827   SHORT     가변             선택적
EXIF_OECF                      0x8828   UNDEFINED 가변             선택적
EXIF_SensitivityType           0x8830   SHORT     1                선택적
EXIF_StandardOutputSensitivity 0x8831   LONG      1                선택적
EXIF_RecommendedExposureIndex  0x8832   LONG      1                선택적
EXIF_ISOSpeed                  0x8833   LONG      1                선택적
EXIF_ISOSpeedLatitudeyyy       0x8834   LONG      1                선택적
EXIF_ISOSpeedLatitudezzz       0x8835   LONG      1                선택적
EXIF_ExifVersion               0x9000   UNDEFINED 4                **필수**
EXIF_DateTimeOriginal          0x9003   ASCII     20               선택적
EXIF_DateTimeDigitized         0x9004   ASCII     20               선택적
EXIF_OffsetTime                0x9010   ASCII     7                선택적
EXIF_OffsetTimeOriginal        0x9011   ASCII     7                선택적
EXIF_OffsetTimeDigitized       0x9012   ASCII     7                선택적
EXIF_ComponentsConfiguration   0x9101   UNDEFINED 4                **필수**
EXIF_CompressedBitsPerPixel    0x9102   RATIONAL  1                선택적
EXIF_ShutterSpeedValue         0x9201   SRATIONAL 1                선택적
EXIF_ApertureValue             0x9202   RATIONAL  1                선택적
EXIF_BrightnessValue           0x9203   SRATIONAL 1                선택적
EXIF_ExposureBiasValue         0x9204   SRATIONAL 1                선택적
EXIF_MaxApertureValue          0x9205   RATIONAL  1                선택적
EXIF_SubjectDistance           0x9206   RATIONAL  1                선택적
EXIF_MeteringMode              0x9207   SHORT     1                선택적
EXIF_LightSource               0x9208   SHORT     1                선택적
EXIF_Flash                     0x9209   SHORT     1                권장
EXIF_FocalLength               0x920A   RATIONAL  1                선택적
EXIF_SubjectArea               0x9214   SHORT     가변             선택적
EXIF_MakerNote                 0x927C   UNDEFINED 가변             선택적
EXIF_UserComment               0x9286   UNDEFINED 가변             선택적
EXIF_SubSecTime                0x9290   ASCII     가변             선택적
EXIF_SubSecTime_Original       0x9291   ASCII     가변             선택적
EXIF_SubSecTime_Digitized      0x9292   ASCII     가변             선택적
EXIF_FlashpixVersion           0xA000   UNDEFINED 4                **필수**
EXIF_ColorSpace                0xA001   SHORT     1                **필수**
EXIF_PixelXDimension           0xA002   LONG      1                **필수**
EXIF_PixelYDimension           0xA003   LONG      1                **필수**
EXIF_RelatedSoundFile          0xA004   ASCII     13               선택적
EXIF_FlashEnergy               0xA20B   RATIONAL  1                선택적
EXIF_SpatialFrequencyResponse  0xA20C   UNDEFINED 가변             선택적
EXIF_FocalPlaneXResolution     0xA20E   RATIONAL  1                선택적
EXIF_FocalPlaneYResolution     0xA20F   RATIONAL  1                선택적
EXIF_FocalPlaneResolutionUnit  0xA210   SHORT     1                선택적
EXIF_SubjectLocation           0xA214   SHORT     2                선택적
EXIF_ExposureIndex             0xA215   RATIONAL  1                선택적
EXIF_SensingMethod             0xA217   SHORT     1                선택적
EXIF_FileSource                0xA300   UNDEFINED 1                선택적
EXIF_SceneType                 0xA301   UNDEFINED 1                선택적
EXIF_CFAPattern                0xA302   UNDEFINED 가변             선택적
EXIF_CustomRendered            0xA401   SHORT     1                선택적
EXIF_ExposureMode              0xA402   SHORT     1                권장
EXIF_WhiteBalance              0xA403   SHORT     1                권장
EXIF_DigitalZoomRatio          0xA404   RATIONAL  1                선택적
EXIF_FocalLengthIn35mmFilm     0xA405   SHORT     1                선택적
EXIF_SceneCaptureType          0xA406   SHORT     1                권장
EXIF_GainControl               0xA407   RATIONAL  1                선택적
EXIF_Contrast                  0xA408   SHORT     1                선택적
EXIF_Saturation                0xA409   SHORT     1                선택적
EXIF_Sharpness                 0xA40A   SHORT     1                선택적
EXIF_DeviceSettingDescription  0xA40B   UNDEFINED 가변             선택적
EXIF_SubjectDistanceRange      0xA40C   SHORT     1                선택적
EXIF_ImageUniqueID             0xA420   ASCII     33               선택적
EXIF_CameraOwnerName           0xA430   ASCII     가변             선택적
EXIF_BodySerialNumber          0xA431   ASCII     가변             선택적
EXIF_LensSpecification         0xA432   RATIONAL  4                선택적
EXIF_LensMake                  0xA433   ASCII     가변             선택적
EXIF_LensModel                 0xA434   ASCII     가변             선택적
EXIF_LensSerialNumber          0xA435   ASCII     가변             선택적
============================== ======== ========= ================ =============

GPS 태그:

========================= ======== ========= ================ ===========
메타데이터 항목 이름       헥스코드 유형       값의 개수        선택성
========================= ======== ========= ================ ===========
EXIF_GPSVersionID         0x0000   BYTE      4                선택적
EXIF_GPSLatitudeRef       0x0001   ASCII     2                선택적
EXIF_GPSLatitude          0x0002   RATIONAL  3                선택적
EXIF_GPSLongitudeRef      0x0003   ASCII     2                선택적
EXIF_GPSLongitude         0x0004   RATIONAL  3                선택적
EXIF_GPSAltitudeRef       0x0005   BYTE      1                선택적
EXIF_GPSAltitude          0x0006   RATIONAL  1                선택적
EXIF_GPSTimeStamp         0x0007   RATIONAL  3                선택적
EXIF_GPSSatellites        0x0008   ASCII     가변             선택적
EXIF_GPSStatus            0x0009   ASCII     2                선택적
EXIF_GPSMeasureMode       0x000A   ASCII     2                선택적
EXIF_GPSDOP               0x000B   RATIONAL  1                선택적
EXIF_GPSSpeedRef          0x000C   ASCII     2                선택적
EXIF_GPSSpeed             0x000D   RATIONAL  1                선택적
EXIF_GPSTrackRef          0x000E   ASCII     2                선택적
EXIF_GPSTrack             0x000F   RATIONAL  1                선택적
EXIF_GPSImgDirectionRef   0x0010   ASCII     2                선택적
EXIF_GPSImgDirection      0x0011   RATIONAL  1                선택적
EXIF_GPSMapDatum          0x0012   ASCII     가변             선택적
EXIF_GPSDestLatitudeRef   0x0013   ASCII     2                선택적
EXIF_GPSDestLatitude      0x0014   RATIONAL  3                선택적
EXIF_GPSDestLongitudeRef  0x0015   ASCII     2                선택적
EXIF_GPSDestLongitude     0x0016   RATIONAL  3                선택적
EXIF_GPSDestBearingRef    0x0017   ASCII     2                선택적
EXIF_GPSDestBearing       0x0018   RATIONAL  1                선택적
EXIF_GPSDestDistanceRef   0x0019   ASCII     2                선택적
EXIF_GPSDestDistance      0x001A   RATIONAL  1                선택적
EXIF_GPSProcessingMethod  0x001B   UNDEFINED 가변             선택적
EXIF_GPSAreaInformation   0x001C   UNDEFINED 가변             선택적
EXIF_GPSDateStamp         0x001D   ASCII     11               선택적
EXIF_GPSDifferential      0x001E   SHORT     1                선택적
EXIF_GPSHPositioningError 0x001F   RATIONAL  1                선택적
========================= ======== ========= ================ ===========

FLIR 메타데이터
--------------

.. versionadded:: 3.3

``FLIR`` 메타데이터 도메인에서 FLIR (적외선 이미지) 규범에 따라 인코딩된 메타데이터를 사용할 수 있습니다.

다음 부분에서 나온 메타데이터를 지원합니다:

- Header
- RawData
- CameraInfo
- PaletteInfo
- GPSInfo

자세한 내용은 https://exiftool.org/TagNames/FLIR.html 을 읽어보십시오.

RAW 데이터 또는 PNG로 저장된 열화상(thermal image) 데이터를 ``JPEG:"filename.jpg":FLIR_RAW_THERMAL_IMAGE`` 라는 이름의 GDAL 하위 데이터셋으로 노출시킵니다.

참고
--------

-  `독립 JPEG 그룹 <http://www.ijg.org/>`_
-  `libjpeg-turbo <http://sourceforge.net/projects/libjpeg-turbo/>`_
-  :ref:`raster.gtiff`
-  `EXIF v2.31 사양 <http://www.cipa.jp/std/documents/e/DC-008-Translation-2016-E.pdf>`_
