.. _raster.ktx2:

================================================================================
KTX2
================================================================================

.. versionadded:: 3.6

.. shortname:: KTX2

.. build_dependencies:: Basis Universal


https://github.com/BinomialLLC/basis_universal 에서 발췌:

    Basis Universal은 광범위한 GPU 압축/비압축 픽셀 포맷으로 고속 인코딩 변환(transcoding)할 수 있는 2개의 고압축 중간 파일 포맷(크로노스(Khronos) 그룹의 .basis 또는 .KTX2 오픈 표준 포맷)을 지원하는 "초압축(supercompressed)" GPU 텍스처 데이터 교환(interchange) 시스템입니다.

이 드라이버는 .ktx2 확장자를 가진 텍스처를 처리합니다. .basis 확장자의 경우 :ref:`raster.basisu` 드라이버를 참조하십시오. 이 드라이버는 KTX(1) 파일을 처리하지 *않는다는* 사실을 기억하십시오.

.ktx2 파일 포맷이 다른 GPU 픽셀 포맷으로 직접 인코딩 변환을 지원하는 반면, 이 GDAL 드라이버는 비압축 RGB(A) 데이터와 Basis Universal 텍스처 사이의 변환만을 지원한다는 사실을 기억하십시오.

파일이 이미지 여러 개로 이루어져 있는 경우, 이미지들을 ``KTX2:filename:layer_idx:face_idx`` 문법을 사용해서 하위 데이터셋으로 노출시킵니다.

Mipmaps 수준들은 GDAL 오버뷰로 노출시킵니다.

드라이버 케이퍼빌리티
---------------------

.. supports_createcopy::

.. supports_virtualio::

생성 옵션
---------

.ktx2 포맷은 내부적으로 `UASTC 압축 텍스처 포맷 <https://richg42.blogspot.com/2020/01/uastc-block-format-encoding.html>`_ 을 기반으로 하는 고품질 모드와 "ETC1S"라고 하는 ETC1의 부분 집합을 기반으로 하는 원본 저품질 모드, 두 가지 모드를 지원합니다. 기본값은 ETC1S입니다.
밴드 1개(회색조), 2개(회색조+알파), 3개(RGB) 또는 4개(RGB+알파)를 가진 바이트 유형만을 입력받습니다.
이 2개의 모드와 그 옵션들에 대한 상세 정보는 https://github.com/BinomialLLC/basis_universal 을 참조하십시오.

다음 생성 옵션들을 사용할 수 있습니다:

- **COMPRESSION=ETC1S/UASTC**:
  기본값은 ETC1S입니다.

- **UASTC_SUPER_COMPRESSION=ZSTD/NONE**:
  적용할 "초(super)" 압축 방법을 설정합니다. 기본적으로 ZSTD(ZStandard)를 적용합니다. ``COMPRESSION=UASTC`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **UASTC_LEVEL=integer**:
  [0,4] 범위의 정수를 설정합니다. 기본값은 2입니다. 높은 값으로 설정할수록 품질이 높아지지만 계산 시간은 늘어납니다. 4로 설정하면 도저히 사용할 수 없을 정도로 느려집니다. ``COMPRESSION=UASTC`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **UASTC_RDO_LEVEL=float**:
  비율 왜곡 최적화(Rate Distortion Optimization) 수준을 설정합니다. 낮은 값으로 설정할수록 품질이 높아지지만 파일 용량이 커집니다. 일반적인 범위는 [0.2,3]이며, 기본값은 1입니다. ``COMPRESSION=UASTC`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **ETC1S_LEVEL=integer**:
  [0,6] 범위의 정수를 설정합니다. 기본값은 1입니다. 높은 값으로 설정할수록 품질이 높아지지만 계산 시간은 늘어납니다. ``COMPRESSION=ETC1S`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **ETC1S_QUALITY_LEVEL=integer**:
  [1,255] 범위의 정수를 설정합니다. 기본값은 128입니다. 높은 값으로 설정할수록 품질이 높아지지만 파일 용량이 커집니다. ``COMPRESSION=ETC1S`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **ETC1S_MAX_ENDPOINTS_CLUSTERS=integer**:
  [1,16128] 범위의 정수를 설정합니다. 종단점(endpoint) 클러스터의 최대 개수입니다. 이 옵션을 설정하는 경우 ``ETC1S_MAX_SELECTOR_CLUSTERS`` 옵션도 설정해야만 합니다. ``ETC1S_QUALITY_LEVEL`` 옵션과 함께 사용할 수 없습니다.
  ``COMPRESSION=ETC1S`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **ETC1S_MAX_SELECTOR_CLUSTERS=integer**:
  [1,16128] 범위의 정수를 설정합니다. 선택기(selector) 클러스터의 최대 개수입니다. 이 옵션을 설정하는 경우 ``ETC1S_MAX_ENDPOINTS_CLUSTERS`` 옵션도 설정해야만 합니다. ``ETC1S_QUALITY_LEVEL`` 옵션과 함께 사용할 수 없습니다.
  ``COMPRESSION=ETC1S`` 인 경우에만 이 옵션을 사용할 수 있습니다.

- **NUM_THREADS=integer**:
  기본값은 사용할 수 있는 가상 CPU의 최대 개수입니다. :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션으로도 제어할 수 있습니다.

- **MIPMAP=YES/NO**:
  MIPMAP 생성을 활성화할지 여부를 설정합니다. 기본값은 NO입니다.

- **COLORSPACE=PERCEPTUAL_SRGB/LINEAR**:
  기본값은 PERCEPTUAL_SRGB입니다.
  입력물이 측광(photometric) 데이터가 아닌 경우 불필요한 부산물 생성을 피하려면 LINEAR로 설정하십시오.

빌드 지침
---------

현재 basisu를 라이브러리로 빌드하려면 https://github.com/rouault/basis_universal/tree/cmake 포크의 ``cmake`` 브랜치를 빌드해야 합니다.

.. code-block::

    git clone -b cmake https://github.com/rouault/basis_universal
    cd basis_universal
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/install-basisu -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON
    cmake --build . --config Release --target install

basisu를 빌드하고 나면, ``CMAKE_PREFIX_PATH`` 변수 또는 ``basisu_ROOT`` 변수에 있는 basisu 설치 접두어를 가리켜서 GDAL CMake 옵션을 환경설정해줘야만 합니다.

