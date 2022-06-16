.. _raster.jpegxl:

================================================================================
JPEGXL -- JPEG-XL 파일 포맷
================================================================================

.. versionadded:: 3.6

.. shortname:: JPEGXL

.. build_dependencies:: libjxl

JPEG-XL 파일의 읽기 및 (CreateCopy()를 통해) 배치(batch) 쓰기를 지원하지만 제자리(in-place) 업데이트는 지원하지 않습니다.

이 드라이버는 읽기와 쓰기를 지원합니다:

-  지리참조: JUMBF 상자 안에 있는 GeoJP2 UUID 상자로 인코딩합니다.
-  xml:XMP 메타데이터 도메인에 있는 XMP
-  EXIF 메타데이터 도메인에 있는 EXIF
-  COLOR_PROFILE 메타데이터 도메인에 있는 색상 프로파일

읽기 또는 쓰기는 전체 비압축 이미지를 메모리로 불러오기를 수반합니다. 현재 libjxl 구현 때문에 특히 압축에 메모리를 많이 요구합니다. 따라서 대용량 (너비 또는 높이가 10,000픽셀을 초과하는 정도의) 이미지의 경우 :ref:`raster.gtiff` 코덱으로 JPEGXL를 압축할 것을 권장합니다.

:decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 정수값 또는 (기본값) ``ALL_CPUS`` 로 설정하면 멀티스레딩 압축 및 압축 해제에 사용할 작업자 스레드의 개수를 설정할 수 있습니다.

.. note::

   XMP와 EXIF 읽기 및 쓰기 그리고 지리참조 정보 작성을 지원하기 위해서는 0.6.1버전 배포판 이후의 libjxl 주 브랜치로부터 빌드한 libjxl 버전이 필요합니다.

드라이버 케이퍼빌리티
---------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

색상 프로파일 메타데이터
------------------------

GDAL은 COLOR_PROFILE 도메인에 있는 다음 색상 프로파일 메타데이터를 처리할 수 있습니다:

-  SOURCE_ICC_PROFILE (파일에 내장된, Base64로 인코딩된 ICC 프로파일)

생성 옵션
---------

libjxl 0.6.1버전은 밴드가 1개(회색조), 2개(회색조 + 알파), 3개(RGB), 그리고 4개(RGBA)인 소스 이미지만 지원합니다. 이후 libjxl 버전은 밴드 개수에 상관없이 작성할 수 있습니다. 지원 데이터 유형은 Byte, UInt16 및 Float32입니다.

손실 압축 옵션을 지정하지 않고 (정규) JPEG 파일로부터 복사해오는 경우, 콘텐츠를 비손실 방식으로 그리고 JPEGXL 코드스트림으로부터 JPEG 파일을 재생성할 수 있게 하는 재구성 데이터로 다시 인코딩합니다.

다음 생성 옵션들을 사용할 수 있습니다:

-  **LOSSLESS=YES/NO**:
   JPEGXL 압축이 비손실 방식이어야 할지 여부를 지정합니다.
   (DISTANCE 또는 QUALITY 옵션을 지정하지 않는 한) 기본값은 YES입니다.

-  **EFFORT=[1-9]**:
   압축 수준을 지정합니다. 높은 값으로 지정할수록 파일 용량이 적어지고 압축 시간은 늘어납니다. 기본값은 5입니다.

-  **DISTANCE=[0.1-15]**:
   손실 압축 용 거리 수준을 지정합니다. 0은 수학적으로 비손실, 1.0은 시각적으로 비손실이며 일반적인 범위는 [0.5,3]입니다. 기본값은 1.0입니다.

-  **QUALITY=[-inf,100]**:
   DISTANCE를 대체해서 손실 압축을 지정할 수 있는 옵션입니다. [0,100] 범위 안에서 설정되는 libjpeg 품질과 대략적으로 일치합니다. 기본값은 90.0입니다.

-  **NBITS=n**:
   Byte 유형의 경우 1에서 7까지의 값을, 또는 UInt16 유형의 경우 9에서 15까지의 값을 전송해서 샘플 당 8비트 미만인 파일을 생성합니다.

-  **NUM_THREADS=number_of_threads/ALL_CPUS**:
   멀티스레딩 압축 및 압축 해제에 사용할 작업자 스레드의 개수를 설정합니다. 기본값은 ALL_CPUS입니다.
   설정하지 않는 경우, :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션으로도 제어할 수 있습니다.

-  **SOURCE_ICC_PROFILE=value**:
   Base64로 인코딩된 ICC 프로파일입니다. 소스 데이터셋의 ICC 프로파일을 사용하지 않으려면 빈 문자열로 설정하면 됩니다.

-  **WRITE_EXIF_METADATA=YES/NO**: (libjxl 0.6.1 초과 버전)
   Exif 상자에 소스 데이터셋의 EXIF 메타데이터 도메인의 EXIF 메타데이터를 작성할지 여부를 지정합니다. 기본값은 YES입니다.

-  **WRITE_XMP=YES/NO**: (libjxl 0.6.1 초과 버전)
   xml 상자에 소스 데이터셋의 xml:XMP 메타데이터 도메인의 XMP 메타데이터를 작성할지 여부를 지정합니다. 기본값은 YES입니다.

-  **WRITE_GEOJP2=YES/NO**: (libjxl 0.6.1 초과 버전)
   JUMBF UUID 상자에 GeoJP2 인코딩을 사용해서 지리참조 정보를 작성할지 여부를 지정합니다. 기본값은 YES입니다.

-  **COMPRESS_BOXES=YES/NO**: (libjxl 0.6.1 초과 버전)
   `Brotli <https://github.com/google/brotli>`_ 압축 방법을 이용해서 Exif/XMP/GeoJP2 상자를 압축 해제할지 여부를 지정합니다. 기본값은 NO입니다.

참고
----

-  `JPEG-XL 홈페이지 <https://jpeg.org/jpegxl/>`_
-  `libjxl <https://github.com/libjxl/libjxl/>`_

