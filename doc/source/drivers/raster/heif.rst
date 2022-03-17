.. _raster.heif:

================================================================================
HEIF / HEIC -- ISO/IEC 23008-12:2017 고효율 이미지 파일 포맷
================================================================================

.. versionadded:: 3.2

.. shortname:: HEIF

.. build_dependencies:: libheif (1.1 이상 버전), libde265 대상으로 빌드

고효율 이미지 파일 포맷(High Efficiency Image File Format; HEIF)은 개별 이미지 및 이미지 시퀀스를 위한 컨테이너 포맷입니다.
이 드라이버는 주로 고효율 비디오 코딩(High Efficiency Video Coding; HEVC, ITU-T H.265) 코덱을 사용하는 이미지를 읽을 수 있도록 개발되고 테스트되었습니다. 이런 이미지를 보통 HEIC(HEVC 압축 HEIF)이라고 하는데, .heic 확장자를 사용합니다.
iOS 11이 이런 파일을 생성할 수 있습니다.

채널 당 8비트 이상을 가진 이미지를 지원하려면 libheif 1.4 이상 버전이 필요합니다.

이 드라이버는 (``EXIF`` 메타데이터 도메인에 노출돼 있는) EXIF 메타데이터와 (``xml:XMP`` 메타데이터 도메인에 노출돼 있는) XMP 메타데이터를 읽어올 수 있습니다.

이 드라이버는 (섬네일의 밴드 개수가 전체 해상도 이미지의 밴드 개수와 일치하는 경우) 섬네일을 오버뷰로 노출시킬 것입니다.

HEIF 파일이 최상위 이미지 여러 개를 담고 있는 경우, GDAL 하위 데이터셋으로 노출시킬 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio:: if libheif >= 1.4


윈도우 상에서의 빌드 힌트
-----------------------

* https://github.com/strukturag/libheif 에서 libheif 용 소스 압축 파일을, https://github.com/strukturag/libde265 에서 libde265 용 소스 압축 파일을 다운로드하십시오.

* 압축 파일을 (예를 들면 libde265-1.0.5.tar.gz 및 libheif-1.7.0.tar.gz 파일을) 압축 해제하십시오.

* libde265 빌드:

    ::

        cd libde265-1.0.5
        mkdir build
        cd build
        cmake -G "Visual Studio 15 2017 Win64" .. -DCMAKE_INSTALL_PREFIX=c:/dev/install-libheif
        cmake --build . --config Release --target install
        cd ..
        copy libde265\de265.h c:/dev/install-libheif/include/libde265
        copy libde265\de265-version.h c:/dev/install-libheif/include/libde265
        cd ..

* libheif를 libde265 지원과 함께 빌드:

    ::

        cd libheif-1.7.0
        mkdir build
        cd build
        cmake -G "Visual Studio 15 2017 Win64" .. \
            -DCMAKE_INSTALL_PREFIX=c:/dev/install-libheif \
            -DLIBDE265_FOUND=ON \
            -DLIBDE265_CFLAGS=/Ic:/dev/install-libheif/include \
            -DLIBDE265_LIBRARIES=c:/dev/install-libheif/lib/libde265


* GDAL을 빌드하기 전에 GDAL의 nmake.local 파일에 다음 내용을 추가하십시오:

    ::

        HEIF_INC = -Ic:\dev\install-libheif\include
        HEIF_LIB = C:\dev\install-libheif\lib\heif.lib
