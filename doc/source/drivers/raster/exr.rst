.. _raster.exr:

================================================================================
EXR -- 확장된 동적 범위 이미지 파일 포맷
================================================================================

.. versionadded:: 3.1

.. shortname:: EXR

.. build_dependencies:: libopenexr

OpenEXR는 광역 동적 범위(high dynamic range) 래스터 파일 포맷입니다. 이 드라이버는 해당 포맷으로 작성된 이미지 읽기 및 쓰기를 지원합니다.

EXR 헤더 메타데이터에 지리참조를 WKT CRS 문자열과 3x3 지리변형 행렬로 작성합니다.

"심도 이미지(deep image)"는 지원하지 않습니다.

생성 옵션
----------------

-  **COMPRESS=[NONE/RLE/ZIPS/ZIP/PIZ/PXR24/B44/B44A/DWAA/DWAB]**: 압축 메소드를 선택합니다. 기본값은 ZIP입니다. 압축 형식에 대한 상세 정보는 `위키피디아 페이지 <https://en.wikipedia.org/wiki/OpenEXR#Compression_methods>`_ 를 참조하십시오.

-  **PIXEL_TYPE=HALF/FLOAT/UINT**: 인코딩을 위해 쓰이는 픽셀 유형을 선택합니다.

   - ``HALF`` 는 IEEE-754 16비트 부동소수점형 값에 대응합니다.
   - ``FLOAT`` 는 IEEE-754 32비트 부동소수점형 값에 대응합니다.
   - ``UINT`` 는 32비트 부호 없는 정수형 값에 대응합니다.

   지정하지 않는 경우, 다음과 같이 GDAL 데이터 유형을 매핑할 것입니다:

   - ``Byte`` ==> HALF
   - ``Int16`` ==> HALF (손실 가능성)
   - ``UInt16`` ==> HALF (손실 가능성)
   - ``Int32`` ==> FLOAT (손실 가능성)
   - ``UInt32`` ==> UINT
   - ``Float32`` ==> FLOAT
   - ``Float64`` ==> FLOAT (일반적으로 손실)

-  **TILED=YES/NO**: 이 옵션을 NO로 설정하지 않는 한 기본적으로 타일화된 파일을 생성할 것입니다. Create() 모드에서는 TILED=NO 설정이 불가능합니다.

-  **BLOCKXSIZE=n**: 타일 너비를 설정합니다. 기본값은 256입니다.

-  **BLOCKYSIZE=n**: 타일 높이를 설정합니다. 기본값은 256입니다.

-  **OVERVIEWS=YES/NO**: 오버뷰 생성 여부를 제어합니다. 기본값은 NO입니다. CreateCopy() 모드에서만 작동합니다.

-  **OVERVIEW_RESAMPLING=NEAR/AVERAGE/CUBIC/...**: 오버뷰 생성 시 사용할 리샘플링 메소드를 선택합니다. 기본값은 CUBIC입니다.

-  **PREVIEW=YES/NO**: 미리보기 생성 여부를 제어합니다. 기본값은 NO입니다. CreateCopy() 모드에서 바이트형 RGB(A) 데이터를 작업하는 경우에만 작동합니다.

-  **AUTO_RESCALE=YES/NO**: 0-255 범위의 바이트형 RGB(A) 값을 EXR 생태계에서 일반적으로 쓰이는 0-1 범위로 크기 조정할지 여부를 제어합니다.

-  **DWA_COMPRESSION_LEVEL=n**: DWA 압축 수준입니다. 높게 설정할수록 이미지가 더 압축될 (그리고 품질은 떨어질) 것입니다. OpenEXR 2.4버전의 기본값은 45입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

    이 드라이버는 타일화된 데이터 전용으로, 각 타일을 거의 한번에 작성해야만 하고, 데이터셋을 닫기 전에는 작성한 타일을 다시 읽어올 수 없다는 경고를 발합니다.

.. supports_georeferencing::

.. supports_virtualio::
