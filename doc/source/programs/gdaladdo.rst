.. _gdaladdo:

================================================================================
gdaladdo
================================================================================

.. only:: html

    오버뷰 이미지를 작성 또는 재작성합니다.

.. Index:: gdaladdo

개요
--------

.. code-block::

    gdaladdo [-r {nearest,average,rms,bilinear,gauss,cubic,cubicspline,lanczos,average_magphase,mode}]
            [-b band]* [-minsize val]
            [-ro] [-clean] [-oo NAME=VALUE]* [--help-general] filename [levels]

설명
-----------

:program:`gdaladdo` 유틸리티는 가장 많이 지원되는 파일 포맷에 대해 몇 가지 다운샘플링 알고리즘 가운데 하나로 오버뷰 이미지를 작성 또는 재작성할 수 있습니다.

.. program:: gdaladdo

.. option:: -r {nearest (default),average,rms,gauss,cubic,cubicspline,lanczos,average_magphase,mode}

    리샘플링 알고리즘을 선택합니다.

    ``nearest`` 최근접 이웃 (단순 샘플링) 리샘플링 도구(resampler)를 적용합니다.

    ``average`` NODATA가 아닌 모든 기여 픽셀(contributing pixel)의 평균을 계산합니다. GDAL 3.1버전부터, 이 평균은 대상 픽셀에 완전히 기여하지 않는 소스 픽셀의 가중치를 제대로 고려하는 가중 평균이 되었습니다.

    ``rms`` NODATA가 아닌 모든 기여 픽셀의 제곱평균제곱근(root mean squared)/이차평균(quadratic mean)을 계산합니다. (GDAL 3.3버전 이상)

    ``bilinear`` 이중선형 회선 커널(bilinear convolution kernel)을 적용합니다.

    ``gauss`` 오버뷰를 계산하기 전에 가우스 커널(Gaussian kernel)을 적용합니다. 대조(contrast)가 높거나 노이즈가 많은 패턴을 가진 뾰족한 경계가 있는 경우 단순 평균보다 결과물이 좋을 수 있습니다. 권고되는 수준값은 2, 4, 8, ...이어야 하기 때문에 3x3 리샘플링 가우스 커널을 선택합니다.

    ``cubic`` 3차 회선 커널(cubic convolution kernel)을 적용합니다.

    ``cubicspline`` B 스플라인 회선 커널(B-Spline convolution kernel)을 적용합니다.

    ``lanczos`` 란초시 창함수 싱크 회선 커널(Lánczos windowed sinc convolution kernel)을 적용합니다.

    ``average_magphase`` Magnitude/Phase 공간에서 복잡 데이터의 평균을 계산합니다.

    ``mode`` 샘플링된 모든 포인트들에서 가장 출현 빈도가 높은 값을 선택합니다.

.. option:: -b <band>

    입력 밴드에서 오버뷰 용 **밴드** 를 선택합니다. 밴드 번호는 1부터 시작합니다. 오버뷰를 작성할 입력 밴드를 여러 개 선택하기 위해 :option:`-b` 스위치를 여러 개 사용할 수도 있습니다.

.. option:: -ro

    (특히 GeoTIFF의 경우) 외부 오버뷰를 작성하기 위해 데이터셋을 읽기전용(read-only) 모드로 엽니다.

.. option:: -clean

    오버뷰를 모두 제거합니다.

.. option:: -oo NAME=VALUE

    데이터셋 열기 옵션 (특정 포맷 지원)

.. option:: -minsize <val>

    가장 작은 오버뷰 수준의 최대 너비 또는 높이입니다. 명확한 수준을 지정하지 않은 경우에만 고려합니다. 기본값은 256입니다.

    .. versionadded:: 2.3

.. option:: <filename>

    오버뷰를 작성할 (또는 오버뷰를 제거해야만 하는) 파일입니다.

.. option:: <levels>

    작성할 내장(integral) 오버뷰 수준들의 목록입니다. :option:`-clean` 옵션으로 무시됩니다.

    .. versionadded:: 2.3

        수준은 이제 오버뷰를 작성하기 위해 필수적이지 않습니다. 이런 경우, 가장 작은 오버뷰가 -minsize 스위치의 값 미만이 될 때까지 적절한 2의 거듭제곱 오버뷰 인수를 선택할 것입니다.

gdaladdo는 (RGB 이미지의 경우) 밴드 별로 입력 RGB의 각 값을 독립적으로 고려하지 않고, 입력 RGB의 세 값만을 NODATA 값으로 고려하도록 (특별 데이터셋 메타데이터인) NODATA_VALUES 투플(tuple)을 제대로 존중할 것입니다.

``2`` 같은 수준 값을 선택하면 기반 레이어의 해상도를 (각 차원마다) 1/2로 줄인 오버뷰 수준을 계산할 것입니다. 파일이 선택한 수준과 동일한 기존 오버뷰 수준을 가지고 있다면, 제자리(in place)에서 기존 수준을 재계산하고 재작성할 것입니다.

내부 GeoTIFF 오버뷰의 경우(또는 GeoTIFF 포맷으로 된 외부 오버뷰의 경우), -clean 옵션이 파일 용량을 줄이지 않는다는 사실을 기억하십시오. 나중에 오버뷰 수준과 함께 gdaladdo를 실행하더라도 이전에 삭제한 오버뷰 공간을 재사용하는 대신 파일을 확장할 것입니다. 이미 오버뷰를 계산한 파일에 대해 단지 리샘플링 메소드만 변경하고자 한다면, 기존 오버뷰를 삭제할 필요는 없습니다.

일부 포맷 드라이버는 오버뷰를 아예 지원하지 않습니다. 많은 포맷 드라이버가 실제로는 TIFF 포맷으로 된, .ovr 확장자의 부차적인 파일에 오버뷰를 저장합니다. 기본적으로 GeoTIFF 드라이버는 (쓰기 권한이 있는 경우) 작업 중인 파일에 오버뷰를 내부적으로 저장합니다. -ro 플래그를 지정하지 않았다면 말이죠.

드라이버 대부분은 Erdas Imagine 포맷을 사용하는, 대안 오버뷰 포맷도 지원합니다. 이 포맷을 사용하려면 :decl_configoption:`USE_RRD` =YES 환경설정 옵션을 지정하십시오. 이 옵션을 지정하면 (예: --config USE_RRD YES) GDAL 응용 프로그램은 물론 Imagine이나 ArcGIS에서 직접 사용하기에 적합한 관련 .aux 파일에 오버뷰를 저장할 것입니다.

GeoTIFF 포맷의 외부 오버뷰
------------------------------------

TIFF 포맷으로 생성된 외부 오버뷰는 :decl_configoption:`COMPRESS_OVERVIEW` 환경설정 옵션을 사용해서 압축되었을 수도 있습니다. 이 옵션을 통해 GeoTIFF 드라이버가 지원하는 모든 압축 메소드를 이용할 수 있습니다. (예: ``--config COMPRESS_OVERVIEW DEFLATE``) :decl_configoption:`PHOTOMETRIC_OVERVIEW`
=RGB/YCBCR/... 환경설정 옵션으로 측광(photometric) 해석을, 그리고 :decl_configoption:`INTERLEAVE_OVERVIEW` =PIXEL/BAND 환경설정 옵션으로 교차 삽입(interleaving)을 설정할 수 있습니다.

JPEG 압축 외부 및 내부 오버뷰의 경우, ``--config JPEG_QUALITY_OVERVIEW value`` 로 JPEG 품질을 설정할 수 있습니다.

WEBP 압축 외부 및 내부 오버뷰의 경우, ``--config WEBP_LEVEL_OVERVIEW value`` 로 WEBP 품질 수준을 설정할 수 있습니다. 설정하지 않으면 기본값 75를 사용할 것입니다.

LERC 압축 외부 및 내부 오버뷰의 경우, ``--config MAX_Z_ERROR_OVERVIEW value`` 로 최대 오류 한계값을 설정할 수 있습니다. 설정하지 않으면 기본값 0(비손실)을 사용할 것입니다. GDAL 3.4.1부터 추가되었습니다.

DEFLATE 또는 LERC_DEFLATE 압축 외부 및 내부 오버뷰의 경우, ``--config ZLEVEL_OVERVIEW value`` 로 압축 수준을 설정할 수 있습니다. 설정하지 않으면 기본값 6을 사용할 것입니다. GDAL 3.4.1부터 추가되었습니다.

ZSTD 또는 LERC_ZSTD 압축 외부 및 내부 오버뷰의 경우, ``--config ZSTD_LEVEL_OVERVIEW value`` 로 압축 수준을 설정할 수 있습니다. 설정하지 않으면 기본값 9를 사용할 것입니다. GDAL 3.4.1부터 추가되었습니다.

LZW, ZSTD 또는 DEFLATE 압축 외부 오버뷰의 경우, ``--config PREDICTOR_OVERVIEW 1|2|3`` 으로 예측 변수(predictor) 값을 설정할 수 있습니다.

가능한 한 가장 작은 JPEG-In-TIFF 오버뷰를 생성하려면 다음 옵션을 사용해야 합니다:

::

    --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL

다음 :decl_configoption:`BIGTIFF_OVERVIEW` 환경설정 옵션을 사용하면 BigTIFF 포맷으로 된 외부 오버뷰를 생성할 수 있습니다: ``--config BIGTIFF_OVERVIEW {IF_NEEDED|IF_SAFER|YES|NO}``

GDAL 2.3.0 버전부터 기본값은 IF_SAFER입니다(이전 버전에서는 IF_NEEDED). 이 옵션의 습성은 GeoTIFF 드라이버 문서에 정리된 BIGTIFF 생성 옵션과 정확히 일치합니다.

- YES는 BigTIFF를 강제합니다.
- NO는 대표적인 TIFF를 강제합니다.
- IF_NEEDED는 명확하게 필요한 경우에만 (비압축, 4GB보다 큰 오버뷰) BigTIFF를 생성할 것입니다.
- IF_SAFER는 산출되는 파일이 4GB를 넘을 *수도* 있는 경우 BigTIFF를 생성할 것입니다.

``--config SPARSE_OK_OVERVIEW ON`` 으로 (NODATA 값이 존재하는 경우 타일의 모든 픽셀이 NODATA 값이거나, 그렇지 않은 경우 0일 때 누락되는 타일들인) 빈약(sparse) GeoTIFF 오버뷰 파일들을 얻을 수 있습니다. GDAL 3.4.1부터 추가되었습니다.

이 모든 옵션들에 대한 자세한 설명을 보고 싶다면 :ref:`raster.gtiff` 드라이버 문서를 읽어보십시오.

Geotiff 오버뷰에 블록 크기 설정하기
---------------------------------------

``--config GDAL_TIFF_OVR_BLOCKSIZE <size>``

예시: ``--config GDAL_TIFF_OVR_BLOCKSIZE 256``

기본값은 128입니다. 또는 GDAL 3.1 버전부터 타일화된 GeoTIFF 파일을 대상으로 오버뷰를 생성하는 경우, 기본값은 전체 해상도 이미지의 타일 크기입니다. 주의: 이 설정이 없다면, 파일이 오버뷰 블록 크기와는 다른 블록 크기를 가진 전체 해상도 이미지를 가질 수 있습니다. (예를 들어 블록 크기가 256인 전체 해상도 이미지, 블록 크기가 128인 오버뷰)

멀티스레딩
--------------

.. versionadded:: 3.2

오버뷰 계산에 사용할 스레드의 개수를 지정하려면 :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 ``ALL_CPUS`` 또는 정수값으로 설정하면 됩니다.

C API
-----

C에서 :cpp:func:`GDALBuildOverviews` 를 호출하면 이 유틸리티의 기능을 수행할 수 있습니다.

예시
--------

입력 TIFF 파일에 내장되는 오버뷰를 자동으로 수준을 계산해서 생성하십시오(GDAL 2.3 이상 버전):

::

    gdaladdo -r average abc.tif

입력 TIFF 파일에 내장되는 오버뷰를 생성하십시오:

::

    gdaladdo -r average abc.tif 2 4 8 16

ERDAS .IMG 파일로부터 외부 압축 GeoTIFF 오버뷰 파일을 생성하십시오:

::

    gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE erdas.img 2 4 8 16

밴드 3개를 가진 RGB 데이터셋으로부터 외부 JPEG 압축 GeoTIFF 파일을 생성하십시오(데이터셋이 쓰기 가능한 GeoTIFF인 경우, 외부 오버뷰를 강제로 생성하기 위해 -ro 옵션도 추가해야 합니다):

::

    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR
             --config INTERLEAVE_OVERVIEW PIXEL rgb_dataset.ext 2 4 8 16

지정한 JPEG 파일에 대한 ERDAS Imagine 포맷 오버뷰를 생성하십시오:

::

    gdaladdo --config USE_RRD YES airphoto.jpg 3 9 27 81

특정 하위 데이터셋, 그러니까 예를 들어 GeoPackage에 포함되었을 수도 있는 많은 래스터 레이어들 가운데 하나에 대한 오버뷰를 생성하십시오("filename" 파라미터는 드라이버 접두어, 파일명 그리고 하위 데이터셋 이름이어야만 합니다. 예를 들면 gdalinfo가 표시하는 이름 말입니다):

::

    gdaladdo GPKG:file.gpkg:layer
