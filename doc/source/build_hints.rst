.. _build_hints:

================================================================================
빌드 힌트 (cmake)
================================================================================

빌드 요구 사항
--------------------------------------------------------------------------------

최소 요구 사항:

- CMake 3.10 이후 버전, 그리고 관련 빌드 체계 (make, ninja, Visual Studio 등등)
- C99 컴파일러
- C++11 컴파일러
- PROJ 6.0 이상 버전

그러나 대부분의 빌드에 선택적인 라이브러리 여러 개를 추가할 것을 강력히 추천합니다:
SQLite3, expat, libcurl, zlib, libtiff, libgeotiff, libpng, libjpeg 등등

CMake
--------------------------------------------------------------------------------

CMake 빌드 체계를 통해 거의 모든 플랫폼에서 GDAL을 컴파일해서 설치할 수 있습니다.
소스 배포 압축 파일을 압축 해제한 다음 소스 트리 구조로 들어가십시오:

    cd gdal-{VERSION}

빌드 디렉터리를 생성한 다음 해당 디렉터리로 가십시오:

    mkdir build
    cd build

이제 빌드 디렉터리에서 CMake를 환경설정하고, 바이너리를 빌드해서 설치할 수 있습니다:

    cmake ..
    cmake --build .
    cmake --build . --target install

윈도우에서는 생성기(generator)를 지정해야 할 수도 있습니다:

    cmake -G "Visual Studio 15 2017" ..

의존성이 사용자 지정 위치에 설치되어 있다면,
include 디렉터리와 라이브러리를 가리키는 경로를 지정하십시오:

    cmake -DSQLITE3_INCLUDE_DIR=/opt/SQLite/include -DSQLITE3_LIBRARY=/opt/SQLite/lib/libsqlite3.so ..

아니면, 사용자 지정 접두어를 지정해도 됩니다:

    cmake -DCMAKE_PREFIX_PATH=/opt/SQLite ..

기존에 캐시된 변수를 CMake의 -U 스위치를 사용해서 설정 해제시킬 수 있습니다. 예를 들어 와일드카드 문자를 사용한다면:

    cmake .. -UGDAL_USE_*


.. warning::

    의존성을 추가/수정/제거하기 위해 GDAL 환경설정을 반복하는 경우, 이전에
    실행했던 캐시 변수 일부가 CMakeCache.txt에 남아서 새 설정과 충돌할 수도
    있습니다. Cmake 실행 도중 이상한 오류가 발생하는 경우, CMakeCache.txt를
    제거해서 깨끗한 상태에서 시작해볼 수도 있습니다.


CMake 일반 환경설정 옵션
+++++++++++++++++++++++++++++++

CMake 환경설정 옵션들은 ``-D<var>=<value>`` 명령어를 통해 제공됩니다.
빌드 디렉터리에서 ``cmake -LAH`` 명령어를 실행하면 캐시된 모든 항목들을 볼 수 있습니다.

.. option:: BUILD_APPS=ON

    응용 프로그램을 빌드합니다. 기본값은 ON 입니다.

.. option:: BUILD_SHARED_LIBS

    공유 GDAL 라이브러리를 빌드합니다. 기본값은 ON 입니다.
    `BUILD_SHARED_LIBS
    <https://cmake.org/cmake/help/v3.10/variable/BUILD_SHARED_LIBS.html>`_
    를 위한 CMake 문서도 참조하세요.

.. option:: CMAKE_BUILD_TYPE

    빌드 유형을 선택합니다. 다음과 같은 옵션들이 있습니다:
    None (기본값), Debug, Release, RelWithDebInfo, 또는 MinSizeRel.
    `CMAKE_BUILD_TYPE
    <https://cmake.org/cmake/help/v3.10/variable/CMAKE_BUILD_TYPE.html>`_.
    을 위한 CMake 문서도 참조하세요.

    .. note::
        환경설정 도중 ``-DCMAKE_BUILD_TYPE=Release`` 로 (또는 비슷한 옵션으로)
        또는 CMake 다중 환경설정(multi-configuration) 빌드 도구의 
        ``--config Release`` 로 지정해주지 않을 경우, 기본 빌드는 최적화되지
        않습니다.

.. option:: CMAKE_C_COMPILER

    C 컴파일러입니다. 비주얼 스튜디오 같은 몇몇 생성기의 경우 무시됩니다.

.. option:: CMAKE_C_FLAGS

    모든 빌드 유형 도중 C 컴파일러가 사용하는 플래그입니다.
    :envvar:`CFLAGS` 환경 변수에 의해 초기화됩니다.

.. option:: CMAKE_CXX_COMPILER

    C++ 컴파일러입니다. 비주얼 스튜디오 같은 몇몇 생성기의 경우 무시됩니다.

.. option:: CMAKE_CXX_FLAGS

    모든 빌드 유형 도중 C++ 컴파일러가 사용하는 플래그입니다.
    :envvar:`CXXFLAGS` 환경 변수에 의해 초기화됩니다.

.. option:: CMAKE_INSTALL_PREFIX

    소프트웨어 설치 위치를 설정합니다.
    유닉스 계열의 기본값은 ``/usr/local/`` 입니다.

.. option:: CMAKE_PREFIX_PATH

    외부 의존성을 검색할 때 검색 대상이 될 설치 접두어(prefix)를 지정하는
    디렉터리 목록입니다.

    CMake 3.12 버전부터, 특정 패키지를 위한 접두어를 정의하는 데
    ``<Packagename>_ROOT`` 변수를 사용할 수도 있습니다.
    https://cmake.org/cmake/help/latest/release/3.12.html?highlight=root#commands
    페이지를 참조하세요.

.. option:: ENABLE_IPO=OFF

    사용할 수 있는 경우, 컴파일러의 `프로시저 간 최적화(IPO; interprocedural optimization)
    <https://ko.wikipedia.org/wiki/%ED%94%84%EB%A1%9C%EC%8B%9C%EC%A0%80_%EA%B0%84_%EC%B5%9C%EC%A0%81%ED%99%94>`_
    를 사용하는 빌드 라이브러리입니다. 기본값은 OFF입니다.

CMake 패키지 의존 옵션
+++++++++++++++++++++++++++++++

.. Put packages in alphabetic order.

일반적으로, 패키지(외부 의존성)가 CMake가 사용하는 기본 위치에 있을 경우
패키지를 자동으로 발견할 것입니다. ``CMAKE_PREFIX_PATH`` 변수를 가진 예시에
대해서도 이렇게 조정할 수 있습니다.

CMake 3.12 버전부터, ``<Packagename>_ROOT`` 변수를 이용해서 특정 패키지를
위한 접두어를 정의할 수도 있습니다.
https://cmake.org/cmake/help/latest/release/3.12.html?highlight=root#commands
를 읽어보세요. _ROOT, _INCLUDE_DIR 및 _LIBRARY 변수의 경우 패키지 이름의 대소문자를
구분한다는 사실을 기억하십시오.

다음 옵션을 설정하면 검색 가능한 대부분의 의존성을 비활성화시킬 수도 있습니다:

.. option:: GDAL_USE_<Packagename_in_upper_case>:BOOL=ON/OFF

    검색된 의존성을 GDAL 빌드에 사용할 수 있는지 여부를 제어합니다.

다음 옵션을 OFF로 설정하면 GDAL이 기본적으로 (필수 의존성인 PROJ를 제외한)
어떤 외부 의존성도 사용하지 않도록 설정할 수도 있습니다.
그 다음 GDAL_USE_<Packagename_in_upper_case>:BOOL=ON 을 사용하면
개별 라이브러리가 각각 활성화될 것입니다.

.. option:: GDAL_USE_EXTERNAL_LIBS:BOOL=ON/OFF

     CMakeCache.txt를 생성하기 전에 이 옵션을 설정해야 합니다. CMakeCache.txt를
     생성한 다음 이 옵션을 OFF로 설정하면 이전에 탐지된 라이브러리들의 활성화를
     취소하기 위해 CMake를 "-UGDAL_USE_*" 로 재호출해야 합니다.

Armadillo
*********

`Armadillo <http://arma.sourceforge.net/>`_ C++ 라이브러리는 TPS(Thin Plate Spline)
변환기 관련 계산 속도를 높이기 위해 쓰입니다.
자세한 내용은 https://cmake.org/cmake/help/latest/module/FindArmadillo.html 을 참조하세요.
Conda-Forge 의존성을 사용하는 윈도우 빌드에서는 다음 패키지들도 설치해야 할 수도 있습니다:
``blas blas-devel libblas libcblas liblapack liblapacke``

.. option:: GDAL_USE_ARMADILLO=ON/OFF

    Armadillo를 사용할지 여부를 제어합니다. Armadillo가 검색되는 경우 기본값은 ON입니다.


Blosc
*****

`Blosc <https://github.com/Blosc/c-blosc>`_ 는 서로 다른 (LZ4, Snappy, Zlib, Zstd 등등)
백엔드를 가진, 메타 압축을 제공하는 라이브러리입니다. :ref:`raster.zarr` 드라이버가
이 라이브러리를 사용합니다.

.. option:: BLOSC_INCLUDE_DIR

    ``blosc.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: BLOSC_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_BLOSC=ON/OFF

    Blosc를 사용할지 여부를 제어합니다. Blosc가 검색되는 경우 기본값은 ON입니다.


CFITSIO
*******

`C FITS I/O <https://heasarc.gsfc.nasa.gov/fitsio/>`_ 는 :ref:`raster.fits`
드라이버를 사용하기 위한 필수 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.

.. option:: CFITSIO_INCLUDE_DIR

    ``fitsio.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: CFITSIO_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_CFITSIO=ON/OFF

    CFITSIO를 사용할지 여부를 제어합니다. CFITSIO가 검색되는 경우 기본값은 ON입니다.


CharLS
******

`CharLS <https://github.com/team-charls/charls>`_ 는 비손실(lossless) 및
준-비손실(near-lossless) 이미지 압축 및 압축해제를 위한 JPEG-LS 표준을
C++로 구현(implementation)한 라이브러리입니다. :ref:`raster.jpegls`
드라이버가 사용합니다. pkg-config으로 탐지할 수 있습니다.

.. option:: CHARLS_INCLUDE_DIR

    ``charls/charls.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: CHARLS_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_CHARLS=ON/OFF

    CharLS를 사용할지 여부를 제어합니다. CharLS가 검색되는 경우 기본값은 ON입니다.


Crnlib
******

`Crnlib / crunch <https://github.com/rouault/crunch/tree/build_fixes>`_ 는
:ref:`raster.dds` 드라이버를 사용하기 위한 필수 라이브러리입니다.

.. option:: Crnlib_INCLUDE_DIR

  ``crunch/crnlib.h`` 헤더 파일을 가진 Crnlib include 디렉터리를 가리키는 경로입니다.

.. option:: Crnlib_LIBRARY

  링크될 Crnlib 라이브러리를 가리키는 경로입니다.

.. option:: GDAL_USE_CRNLIB=ON/OFF

    Crnlib를 사용할지 여부를 제어합니다. Crnlib가 검색되는 경우 기본값은 ON입니다.


CURL
****

`libcurl <https://curl.se/>`_ 은 모든 (HTTP 등등) 네트워크 접근에 필수적인 라이브러리입니다.

.. option:: CURL_INCLUDE_DIR

    ``curl`` 디렉터리를 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: CURL_LIBRARY_RELEASE

    ``libcurl.dll``, ``libcurl.so``, ``libcurl.lib``, 또는 다른 이름 같은
    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_CURL=ON/OFF

    Curl을 사용할지 여부를 제어합니다. Curl이 검색되는 경우 기본값은 ON입니다.


CryptoPP
********

`Crypto++ <https://github.com/weidai11/cryptopp>`_ 는 구글 클라우드의 인증 메소드 가운데
일부가 사용하는 RSA SHA256 서명 기능에 쓰일 수 있는 라이브러리입니다. :ref:`raster.eedai`
이미지 또는 :ref:`/vsigs/ <vsigs>` 가상 파일 시스템을 필수적으로 사용해야 할 수도 있습니다.
:ref:`/vsicrypt/ <vsicrypt>` 가상 파일 시스템에서도 필수적으로 사용해야 합니다.

.. option:: CRYPTOPP_INCLUDE_DIR

    기반(base) include 디렉터리를 가리키는 경로입니다.

.. option:: CRYPTOPP_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을 빌드하기 위해
    비슷한 라이브러리에 비슷한 ``CRYPTOPP_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: CRYPTOPP_USE_ONLY_CRYPTODLL_ALG=ON/OFF

    기본값은 OFF입니다. cryptopp.dll에 링크하는 경우 필수적으로 ON으로 설정해야 할 수도
    있습니다.

.. option:: GDAL_USE_CRYPTOPP=ON/OFF

    CryptoPP를 사용할지 여부를 제어합니다. CryptoPP가 검색되는 경우 기본값은 ON입니다.


Deflate
*******

`libdeflate <https://github.com/ebiggers/libdeflate>`_ 는 비손실 Deflate/Zip
압축 알고리즘을 제공하는 압축 라이브러리입니다. ZLib보다 빠른 성능을 제공하지만,
완전히 대체할 수는 없기 때문에 결과적으로 ZLib을 보조하는 형태로 사용해야만 합니다.

.. option:: Deflate_INCLUDE_DIR

    ``libdeflate.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: Deflate_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을 빌드하기 위해
    비슷한 라이브러리에 비슷한 ``Deflate_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_DEFLATE=ON/OFF

    Deflate를 사용할지 여부를 제어합니다. Deflate가 검색되는 경우 기본값은 ON입니다.


ECW
***

Hexagon ECW SDK(사유(私有) 소스)는 :ref:`raster.ecw` 드라이버를 사용하기 위해
필수적인 라이브러리입니다. 현재 ECW SDK 3.3과 5.5만 지원합니다.

ECW SDK 5.5버전의 경우, ECW_ROOT 또는 CMAKE_PREFIX_PATH 환경 변수가 일반적으로
ERDAS-ECW_JPEG_2000_SDK-5.5.0/Desktop_Read-Only 로 끝나는 include 및 lib
하위 디렉터리들이 있는 디렉터리를 가리켜야 합니다.

.. option:: ECW_INCLUDE_DIR

    ``NCSECWClient.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: ECW_LIBRARY

    libNCSEcw 라이브러리 파일을 가리키는 경로

.. option:: ECWnet_LIBRARY

    libNCSCnet 라이브러리 파일을 가리키는 경로 (SDK 3.3에서만 필요)

.. option:: ECWC_LIBRARY

    libNCSEcwC 라이브러리 파일을 가리키는 경로 (SDK 3.3에서만 필요)

.. option:: NCSUtil_LIBRARY

    libNCSUtil 라이브러리 파일을 가리키는 경로 (SDK 3.3에서만 필요)

.. option:: GDAL_USE_ECW=ON/OFF

    ECW를 사용할지 여부를 제어합니다. ECW가 검색되는 경우 기본값은 ON입니다.


EXPAT
*****

`Expat <https://github.com/libexpat/libexpat>`_ 은 스트림 향(stream-oriented)
XML 파서(parser; 구문 분석기)로, 주요 OGR 드라이버(GML, GeoRSS, GPX, KML,
LVBAG, OSM, ODS, SVG, WFS, XSLX 등등)의 XML 파싱 기능을 활성화하기 위해
필수적인 라이브러리입니다. 이 라이브러리를 설치할 것을 강력히 추천합니다.
ILI 또는 GMLAS 같은 기타 드라이버에는 XercesC 라이브러리가 필수입니다.

.. option:: EXPAT_INCLUDE_DIR

    ``expat.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: EXPAT_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_EXPAT=ON/OFF

    EXPAT을 사용할지 여부를 제어합니다. EXPAT이 검색되는 경우 기본값은 ON입니다.


FileGDB
*******

`FileGDB SDK <https://github.com/Esri/file-geodatabase-api>`_ (사유 소스)는
:ref:`vector.filegdb` 드라이버를 사용하기 위해 필수적인 라이브러리입니다.
(외부 필수 요소가 없는 :ref:`vector.openfilegdb` 드라이버와 혼동하지 마십시오.)

FileGDB_ROOT 또는 CMAKE_PREFIX_PATH 환경 변수가 SDK 디렉터리를 가리켜야 합니다.

.. option:: FileGDB_INCLUDE_DIR

    ``FileGDBAPI.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: FileGDB_LIBRARY

    라이브러리 파일을 가리키는 경로

.. option:: FileGDB_LIBRARY_RELEASE

    배포판 라이브러리 파일을 가리키는 경로 (윈도우에서만)

.. option:: FileGDB_LIBRARY_DEBUG

    디버그 라이브러리 파일을 가리키는 경로 (윈도우에서만)

.. option:: GDAL_USE_FILEGDB=ON/OFF

    FileGDB를 사용할지 여부를 제어합니다. FileGDB가 검색되는 경우 기본값은 ON입니다.


FreeXL
******

`FreeXL <https://www.gaia-gis.it/fossil/freexl/index>`_ 은 :ref:`vector.xls`
드라이버를 사용하기 위해 필수적인 라이브러리입니다.

.. option:: FREEXL_INCLUDE_DIR

    ``freexl.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: FREEXL_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_FREEXL=ON/OFF

    FreeXL을 사용할지 여부를 제어합니다. FreeXL이 검색되는 경우 기본값은 ON입니다.


FYBA
****

`OpenFyba <https://github.com/kartverket/fyba>`_ 는 :ref:`vector.sosi`
드라이버를 빌드하는 데 필요한 라이브러리입니다.

.. option:: FYBA_INCLUDE_DIR

    ``fyba.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: FYBA_FYBA_LIBRARY

   ``fyba`` 라이브러리 파일을 가리키는 경로

.. option:: FYBA_FYGM_LIBRARY

    ``fygm`` 라이브러리 파일을 가리키는 경로

.. option:: FYBA_FYUT_LIBRARY

    ``fyut`` 라이브러리 파일을 가리키는 경로

.. option:: GDAL_USE_FYBA=ON/OFF

    FYBA를 사용할지 여부를 제어합니다. FYBA가 검색되는 경우 기본값은 ON입니다.


GEOTIFF
*******

:ref:`raster.gtiff` 드라이버는 물론 몇몇 기타 드라이버를 사용하기 위해
필수적인 라이브러리입니다. 이 라이브러리를 찾을 수 없는 경우, libgeotiff
내부 복사본을 사용할 것입니다.

.. option:: GEOTIFF_INCLUDE_DIR

    libgeotiff 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: GEOTIFF_LIBRARY_RELEASE

    ``geotiff.dll``, ``libgeotiff.so``, ``geotiff.lib``, 또는 다른 이름 같은
    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을 빌드하기 위해
    비슷한 라이브러리에 비슷한 ``GEOTIFF_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_GEOTIFF=ON/OFF

    외부 libgeotiff를 사용할지 여부를 제어합니다.
    외부 libgeotiff가 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_GEOTIFF_INTERNAL=ON/OFF

    내부 libgeotiff 복사본을 사용할지 여부를 제어합니다.
    외부 libgeotiff가 설치되지 않은 경우 기본값은 ON입니다.


GEOS
****

`GEOS <https://github.com/libgeos/geos>`_ 는 2차원 벡터 도형 상에서 연산을 수행하기
위한 C++ 라이브러리입니다. OGR에서 사용할 수 있는 대부분의 (교차, 버퍼 등등) 도형 처리
연산을 위한 백엔드로 쓰입니다. ``geos-config`` 프로그램으로 이 라이브러리를 탐지할 수
있습니다.

.. option:: GEOS_INCLUDE_DIR

    ``geos_c.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: GEOS_LIBRARY

    공유 또는 정적 라이브러리 파일(libgeos_c)을 가리키는 경로입니다.

.. option:: GDAL_USE_GEOS=ON/OFF

    GEOS를 사용할지 여부를 제어합니다. GEOS가 검색되는 경우 기본값은 ON입니다.


GIF
***

`giflib <http://giflib.sourceforge.net/>`_ 은 :ref:`raster.gif` 드라이버를
사용하기 위해 필수적인 라이브러리입니다. 이 라이브러리를 찾을 수 없는 경우,
내부 복사본을 사용할 것입니다.

.. option:: GIF_INCLUDE_DIR

    ``gif_lib.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: GIF_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_GIF=ON/OFF

    외부 giflib을 사용할지 여부를 제어합니다.
    외부 giflib이 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_GIF_INTERNAL=ON/OFF

    내부 giflib 복사본을 사용할지 여부를 제어합니다.
    외부 giflib이 설치되지 않은 경우 기본값은 ON입니다.


GTA
***

`GTA <https://marlam.de/gta/>`_ 는 :ref:`raster.gta` 드라이버를 사용하기 위해
필수적인 라이브러리입니다.

.. option:: GTA_INCLUDE_DIR

    ``gta/gta.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: GTA_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_GTA=ON/OFF

    GTA를 사용할지 여부를 제어합니다. GTA가 검색되는 경우 기본값은 ON입니다.


HEIF
****

`HEIF <https://github.com/strukturag/libheif>`_ (1.1 이상 버전)는 :ref:`raster.heif`
드라이버가 사용하는 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.

.. option:: HEIF_INCLUDE_DIR

    ``libheif/heif.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: HEIF_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_HEIF=ON/OFF

    HEIF를 사용할지 여부를 제어합니다. HEIF가 검색되는 경우 기본값은 ON입니다.

HDF4
****

`HDF4 <https://support.hdfgroup.org/products/hdf4/>`_ 는 :ref:`raster.hdf4`
드라이버를 사용하기 위해 필요한 C 라이브러리입니다.

.. option:: HDF4_INCLUDE_DIR

    ``hdf.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: HDF4_df_LIBRARY_RELEASE

    공유 또는 정적 ``dfalt`` 또는 ``df`` 라이브러리 파일을 가리키는 경로입니다.
    디버그 배포판을 빌드하기 위해 비슷한 라이브러리에 비슷한 ``HDF4_df_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.

.. option:: HDF4_mfhdf_LIBRARY_RELEASE

    공유 또는 정적 ``mfhdfalt`` 또는 ``mfhdf`` 라이브러리 파일을 가리키는 경로입니다.
    디버그 배포판을 빌드하기 위해 비슷한 라이브러리에 비슷한 ``HDF4_mfhdf_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.

.. option:: HDF4_xdr_LIBRARY_RELEASE

    공유 또는 정적 ``xdr`` 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``HDF4_xdr_LIBRARY_DEBUG`` 변수를
    지정할 수도 있습니다.
    리눅스 빌드의 경우 일반적으로 필요없습니다.

.. option:: HDF4_szip_LIBRARY_RELEASE

    공유 또는 정적 ``szip`` 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``HDF4_szip_LIBRARY_DEBUG`` 변수를
    지정할 수도 있습니다.
    리눅스 빌드의 경우 일반적으로 필요없습니다.

.. option:: HDF4_COMPONENTS

    이 옵션의 값은 기본값이 ``df;mfhdf;xdr;szip`` 으로 되어 있는 목록입니다.
    HDF4 링크 작업에 서로 다른 라이브러리들이 필수인 경우 사용자 지정할 수도 있습니다.
    이 경우 라이브러리 파일을 환경설정하기 위해 HDF4_{comp_name}_LIBRARY_[RELEASE/DEBUG]
    변수를 사용할 수 있을 것입니다.

.. option:: GDAL_USE_HDF4=ON/OFF

    HDF4를 사용할지 여부를 제어합니다. HDF4가 검색되는 경우 기본값은 ON입니다.


HDF5
****

`HDF5 <https://github.com/HDFGroup/hdf5>`_ 는 :ref:`raster.hdf5` 와 :ref:`raster.bag`
드라이버를 사용하기 위해 필요한 C 라이브러리입니다. :ref:`raster.kea` 드라이버를
사용하기 위해서는 HDF5 CXX 라이브러리가 필요합니다.
https://cmake.org/cmake/help/latest/module/FindHDF5.html 모듈을 사용해서
HDF5 라이브러리를 탐지할 수 있습니다.

.. option:: GDAL_USE_HDF5=ON/OFF

    HDF5를 사용할지 여부를 제어합니다. HDF5가 검색되는 경우 기본값은 ON입니다.


HDFS
****

`Hadoop File System <https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/LibHdfs.html>`_
은 :ref:`/vsihdfs/ <vsihdfs>` 가상 파일 시스템을 사용하기 위해 필요한 네이티브 라이브러리입니다.

.. option:: HDFS_INCLUDE_DIR

    ``hdfs.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: HDFS_LIBRARY

    공유 또는 정적 ``hdfs`` 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_HDFS=ON/OFF

    HDFS를 사용할지 여부를 제어합니다. HDFS가 검색되는 경우 기본값은 ON입니다.


Iconv
*****

`Iconv <https://www.gnu.org/software/libiconv/>`_ 라이브러리는 텍스트의
인코딩을 변환하는 데 쓰입니다. 일반적으로 유닉스 계열 시스템에서는 시스템
라이브러리로 사용할 수 있습니다. 윈도우에서는, GDAL이 운영 체제의 API를
이용해서 몇몇 기본(base) 변환을 할 수 있지만, Iconv를 사용하면 더 많은
변환 기능을 쓸 수 있습니다.

.. option:: Iconv_INCLUDE_DIR

    ``iconv.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: Iconv_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_ICONV=ON/OFF

    Iconv를 사용할지 여부를 제어합니다. Iconv가 검색되는 경우 기본값은 ON입니다.


IDB
***

IDB(Informix DataBase) 클라이언트 SDK(사유 소스)는 :ref:`vector.idb` 드라이버를
빌드하기 위해 필요합니다. IDB_ROOT or CMAKE_PREFIX_PATH 환경 변수가 SDK 디렉터리를
가리켜야 합니다.

.. option:: IDB_INCLUDE_DIR

    ``c++/it.h`` 헤더 파일을 가진 (전형적으로 ``incl`` 로 끝나는) include 디렉터리를 가리키는 경로입니다.

.. option:: IDB_IFCPP_LIBRARY

    (전형적으로 ``lib/c++`` 하위 디렉터리에 있는) ``ifc++`` 라이브러리 파일을 가리키는 경로

.. option:: IDB_IFDMI_LIBRARY

    (전형적으로 ``lib/dmi`` 하위 디렉터리에 있는) ``ifdmi`` 라이브러리 파일을 가리키는 경로

.. option:: IDB_IFSQL_LIBRARY

    (전형적으로 ``lib/esql`` 하위 디렉터리에 있는) ``ifsql`` 라이브러리 파일을 가리키는 경로

.. option:: IDB_IFCLI_LIBRARY

    (전형적으로 ``lib/cli`` 하위 디렉터리에 있는) ``ifcli`` 라이브러리 파일을 가리키는 경로

.. option:: GDAL_USE_IDB=ON/OFF

    IDB를 사용할지 여부를 제어합니다. IDB가 검색되는 경우 기본값은 ON입니다.


JPEG
****

libjpeg은 :ref:`raster.jpeg` 드라이버를 사용하기 위해 필수적인 라이브러리로,
몇몇 다른 (:ref:`raster.gpkg`, :ref:`raster.marfa`, 내부 libtiff 등등) 드라이버도
사용할 수 있습니다. 검색되지 않을 경우, libjpeg의 내부 복사본(6b)을 사용할 것입니다.
최적의 성능을 발휘하려면 `libjpeg-turbo <https://github.com/libjpeg-turbo/libjpeg-turbo>`_
를 사용할 것을 강력히 권장합니다. 이 라이브러리를 탐지하는 방법에 대해 더 자세히
알고 싶다면 https://cmake.org/cmake/help/latest/module/FindJPEG.html 을
읽어보십시오.

.. note::

    libjpeg-turbo를 사용하는 경우, JPEG_LIBRARY[_RELEASE/_DEBUG]가
    TurboJPEG가 아니라 libjpeg ABI를 가진 라이브러리를 가리켜야 합니다.
    그 차이점에 대해서는 https://libjpeg-turbo.org/About/TurboJPEG 을 참조하세요.

.. option:: JPEG_INCLUDE_DIR

    ``jpeglib.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: JPEG_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``JPEG_LIBRARY_DEBUG`` 변수를
    지정할 수도 있습니다.

.. option:: GDAL_USE_JPEG=ON/OFF

    외부 libjpeg을 사용할지 여부를 제어합니다.
    외부 libjpeg이 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_JPEG_INTERNAL=ON/OFF

    내부 libjpeg 복사본을 사용할지 여부를 제어합니다.
    외부 libjpeg이 검색되지 않는 경우 기본값은 ON입니다.


JPEG12
******

libjpeg-12 비트는 12비트 심도의 JPEG 이미지를 처리하기 위해 :ref:`raster.jpeg`,
(내부 libtiff를 사용하는 경우) :ref:`raster.gtiff`, :ref:`raster.jpeg`,
:ref:`raster.marfa` 및 :ref:`raster.nitf` 드라이버가 사용하는 라이브러리입니다.
이 라이브러리는 내부 libjpeg(6b)과 함께 사용할 경우에만 지원됩니다.
정규 8비트 JPEG에 대해 외부 또는 내부 libjpeg을 사용할 경우에만 이 라이브러리를
독립적으로 사용할 수 있습니다.

.. option:: GDAL_USE_JPEG12_INTERNAL=ON/OFF

    내부 libjpeg-12 복사본을 사용할지 여부를 제어합니다. 기본값은 ON입니다.


JSON-C
******

`json-c <https://github.com/json-c/json-c>`_ 는 JSON 콘텐츠를 읽고 쓰기
위해 필수적인 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.
검색되지 않을 경우, json-c의 내부 복사본을 사용할 것입니다.

.. option:: JSONC_INCLUDE_DIR

    ``json.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: JSONC_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_JSONC=ON/OFF

    JSON-C를 사용할지 여부를 제어합니다. JSON-C가 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_JSONC_INTERNAL=ON/OFF

    내부 JSON-C 복사본을 사용할지 여부를 제어합니다.
    외부 JSON-C가 검색되지 않는 경우 기본값은 ON입니다.


JXL
***

`libjxl <https://github.com/libjxl/libjxl>` :ref:`raster.gtiff` 드라이버가
내부 libtiff를 대상으로 빌드된 경우 사용하는 라이브러리입니다.
pkg-config으로 탐지할 수 있습니다.

.. option:: JXL_INCLUDE_DIR

    ``jxl/decode.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: JXL_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_JXL=ON/OFF

    JXL을 사용할지 여부를 제어합니다. JXL이 검색되는 경우 기본값은 ON입니다.


KDU
***

카카두(Kakadu)는 :ref:`raster.jp2kak` 및 :ref:`raster.jpipkak` 드라이버를
사용하기 위해 필수적인 (사유 소스) 라이브러리입니다. 표준화된 설치 지침(install
layout)도 없고 정해진 라이브러리 파일명도 없기 때문에 카카두 요소를 탐지하기는
조금 어렵습니다. 현재 리눅스, 맥OS 그리고 윈도우 x86_64 빌드에서만 KDU_ROOT
변수로부터 카카두 요소를 자동적으로 검색하도록 구현되어 있습니다. 다른 플랫폼의 경우,
사용자가 직접 KDU_LIBRARY와 KDU_AUX_LIBRARY 변수를 지정해줘야 합니다.

.. option:: KDU_INCLUDE_DIR

    카카두 빌드 트리의 루트를 가리키는 경로입니다.
    ``coresys/common/kdu_elementary.h`` 헤더 파일이 이 경로에 있어야 합니다.

.. option:: KDU_LIBRARY

    유닉스의 경우 libkdu_vXYR.so 또는 윈도우의 경우 kdu_vXYR.lib (이때 X.Y는
    카카두 버전입니다) 같은 이름의 공유 라이브러리 파일을 가리키는 경로입니다.

.. option:: KDU_AUX_LIBRARY

    유닉스의 경우 libkdu_aXYR.so 또는 윈도우의 경우 kdu_aXYR.lib (이때 X.Y는
    카카두 버전입니다) 같은 이름의 공유 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_KDU=ON/OFF

    KDU를 사용할지 여부를 제어합니다. KDU가 검색되는 경우 기본값은 ON입니다.

KEA
***

`KEA <http://www.kealib.org/>`_ 는 :ref:`raster.kea` 드라이버를 사용하기
위해 필수적인 라이브러리입니다. HDF5 CXX 라이브러리도 필수적입니다.

.. option:: KEA_INCLUDE_DIR

    ``libkea/KEACommon.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: KEA_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_KEA=ON/OFF

    KEA를 사용할지 여부를 제어합니다. KEA가 검색되는 경우 기본값은 ON입니다.


LERC
****

`LERC <https://github.com/esri/lerc>`_ (V2)은 (RGB 또는 바이트만이 아니라)
모든 픽셀 유형에 대해 빠른 인코딩과 디코딩을 지원하는 오픈 소스 이미지 또는 래스터
포맷입니다. 사용자가 인코딩 도중 픽셀 당 최대 압축 오류를 설정하기 때문에,
(사용자가 정의한 오류 범위 안에서) 원본 입력 이미지의 정확도를 보전합니다.

.. warning::

    현재 (내부 LERC 복사본이 필수적인) :ref:`raster.marfa` 드라이버가 이용할 수 없기
    때문에 외부 LERC 라이브러리 사용을 권장하지 않습니다. 내부 LERC 복사본도 이용할 수
    있는 내부 libtiff만 외부 LERC 라이브러리를 이용할 수 있습니다.


.. option:: LERC_INCLUDE_DIR

    ``Lerc_c_api.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: LERC_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_LERC=ON/OFF

    LERC (V2)를 사용할지 여부를 제어합니다. LERC (V2)가 검색되는 경우 기본값은 *OFF* 입니다.

.. option:: GDAL_USE_LERC_INTERNAL=ON/OFF

    LERC (V2) 내부 라이브러리를 사용할지 여부를 제어합니다.
    GDAL_USE_LERC 옵션이 ON으로 설정돼 있지 않는 한 기본값은 ON입니다.


LERCV1
******

:ref:`raster.marfa` 드라이버가 사용하는 내부 라이브러리입니다.
LERC v1 압축을 제공합니다.

.. option:: GDAL_USE_LERCV1_INTERNAL=ON/OFF

    Lerc V1 내부 라이브러리를 사용할지 여부를 제어합니다. 기본값은 ON입니다.

LibKML
******

`LibKML <https://github.com/libkml/libkml>`_ 은 :ref:`vector.libkml` 드라이버를'
사용하기 위해 필수적인 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.

.. option:: LIBKML_INCLUDE_DIR

    기반 include 디렉터리를 가리키는 경로입니다.

.. option:: LIBKML_BASE_LIBRARY

    ``kmlbase`` 용 공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: LIBKML_DOM_LIBRARY

    ``kmldom`` 용 공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: LIBKML_ENGINE_LIBRARY

    ``kmlengine`` 용 공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_LIBKML=ON/OFF

    LibKML을 사용할지 여부를 제어합니다. LibKML이 검색되는 경우 기본값은 ON입니다.


LibLZMA
*******

`LibLZMA <https://tukaani.org/xz/>`_ 는 비손실 LZMA2 압축 알고리즘을 제공하는
압축 라이브러리입니다. 내부 libtiff 라이브러리 또는 :ref:`raster.zarr` 드라이버가
이 라이브러리를 사용합니다.

.. option:: LIBLZMA_INCLUDE_DIR

    ``lzma.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: LIBLZMA_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_LIBLZMA=ON/OFF

    LibLZMA를 사용할지 여부를 제어합니다. LibLZMA가 검색되는 경우 기본값은 ON입니다.


LibXml2
*******

`LibXml2 <http://xmlsoft.org/>`_ 처리 라이브러리는 몇몇 (PDF, GMLAS, GML OGR VRT)
드라이버에서 XML 스키마를 대상으로 XML 파일의 무결성 검증을 수행하는 데 사용되며,
또 GMLJP2v2 세대에서 고급 기능을 사용하기 위해 쓰입니다.

.. option:: LIBXML2_INCLUDE_DIR

    기반 include 디렉터리를 가리키는 경로입니다.

.. option:: LIBXML2_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_LIBXML2=ON/OFF

    LibXml2를 사용할지 여부를 제어합니다. LibXml2가 검색되는 경우 기본값은 ON입니다.



LURATECH
********

Luratech JPEG2000 SDK(사유 소스)는 :ref:`raster.jp2lura` 드라이버를
사용하기 위해 필수적인 라이브러리입니다.

LURATECH_ROOT 또는 CMAKE_PREFIX_PATH 환경 변수는 SDK 디렉터리를 가리켜야 합니다.

.. option:: LURATECH_INCLUDE_DIR

    ``lwf_jp2.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: LURATECH_LIBRARY

    lib_lwf_jp2.a / lwf_jp2.lib 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_LURATECH=ON/OFF

    LURATECH를 사용할지 여부를 제어합니다. LURATECH가 검색되는 경우 기본값은 ON입니다.


LZ4
***

`LZ4 <https://github.com/lz4/lz4>`_ 는 비손실 LZ4 압축 알고리즘을 제공하는
압축 라이브러리입니다. :ref:`raster.zarr` 드라이버가 이 라이브러리를 사용합니다.

.. option:: LZ4_INCLUDE_DIR

    ``lz4.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: LZ4_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을 빌드하기 위해
    비슷한 라이브러리에 비슷한 ``LZ4_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_LZ4=ON/OFF

    LZ4를 사용할지 여부를 제어합니다. LZ4가 검색되는 경우 기본값은 ON입니다.


MONGOCXX
********

`MongoCXX <https://github.com/mongodb/mongo-cxx-driver>`_ 및 BsonCXX 라이브러리는
:ref:`vector.mongodbv3` 드라이버를 빌드하기 위해 필요합니다.
pkg-config으로 탐지할 수 있습니다.

.. option:: MONGOCXX_INCLUDE_DIR

    ``mongocxx/client.hpp`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: BSONCXX_INCLUDE_DIR

    ``bsoncxx/config/version.hpp`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: MONGOCXX_LIBRARY

    ``mongocxx`` 라이브러리 파일을 가리키는 경로

.. option:: BSONCXX_LIBRARY

    ``bsoncxx`` 라이브러리 파일을 가리키는 경로

.. option:: GDAL_USE_MONGOCXX=ON/OFF

    MONGOCXX를 사용할지 여부를 제어합니다. MONGOCXX가 검색되는 경우 기본값은 ON입니다.


MRSID
*****

MRSID 래스터 DSDK(사유 소스)는 :ref:`raster.mrsid` 드라이버를 사용하기 위해
필수적인 라이브러리입니다.

MRSID_ROOT 또는 CMAKE_PREFIX_PATH 환경 변수는 Raster_DSDK로 끝나는 SDK
디렉터리를 가리켜야 합니다. 리눅스 상에서 응용 프로그램들의 링크 작업이 성공하려면
그리고 libtbb.so를 검색 가능하게 하려면 이 라이브러리의 하위 디렉터리가
LD_LIBRARY_PATH에 정의돼 있어야 한다는 사실을 기억하십시오.

.. option:: MRSID_INCLUDE_DIR

    ``lt_base.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: MRSID_LIBRARY

    libltidsdk 라이브러리 파일을 가리키는 경로

.. option:: GDAL_ENABLE_DRIVER_JP2MRSID

    MrSID SDK를 통해 JPEG2000 지원을 활성화할지 여부를 설정합니다.
    이 옵션의 기본값은 OFF입니다.

.. option:: GDAL_USE_MRSID=ON/OFF

    MRSID를 사용할지 여부를 제어합니다. MRSID가 검색되는 경우 기본값은 ON입니다.


MSSQL_NCLI
**********

마이크로소프트 SQL 네이티브 클라이언트 라이브러리(사유 소스)는
:ref:`vector.mssqlspatial` 드라이버에서 대량(bulk) 복사를 활성화하기 위해
필수적인 라이브러리입니다. MSSQL_NCLI와 MSSQL_ODBC 둘 다 검색되고
활성화된 경우, MSSQL_ODBC를 사용할 것입니다. 표준 위치에 설치되어 있고
11 버전인 경우, 이 라이브러리는 보통 검색됩니다.

.. option:: MSSQL_NCLI_VERSION

    네이티브 클라이언트의 주요 버전, 일반적으로 11

.. option:: MSSQL_NCLI_INCLUDE_DIR

    ``sqlncli.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: MSSQL_NCLI_LIBRARY

    링크될 라이브러리를 가리키는 경로입니다.

.. option:: GDAL_USE_MSSQL_NCLI=ON/OFF

    MSSQL_NCLI를 사용할지 여부를 제어합니다. MSSQL_NCLI가 검색되는 경우 기본값은 ON입니다.


MSSQL_ODBC
**********

마이크로소프트 SQL 네이티브 ODBC 드라이버 라이브러리(사유 소스)는
:ref:`vector.mssqlspatial` 드라이버에서 대량(bulk) 복사를 활성화하기 위해
필수적인 라이브러리입니다. MSSQL_NCLI와 MSSQL_ODBC 둘 다 검색되고
활성화된 경우, MSSQL_ODBC를 사용할 것입니다. 표준 위치에 설치되어 있고
17 버전인 경우, 이 라이브러리는 보통 검색됩니다.

.. option:: MSSQL_ODBC_VERSION

    네이티브 클라이언트의 주요 버전, 일반적으로 17

.. option:: MSSQL_ODBC_INCLUDE_DIR

    ``msodbcsql.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: MSSQL_ODBC_LIBRARY

    링크될 라이브러리를 가리키는 경로입니다.

.. option:: GDAL_USE_MSSQL_ODBC=ON/OFF

    MSSQL_ODBC를 사용할지 여부를 제어합니다. MSSQL_ODBC가 검색되는 경우 기본값은 ON입니다.


MYSQL
*****

MySQL 또는 MariaDB 클라이언트 라이브러리는 :ref:`vector.mysql` 드라이버를
활성화시키기 위해 필수적인 라이브러리입니다.

.. option:: MYSQL_INCLUDE_DIR

    ``mysql.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: MYSQL_LIBRARY

    링크될 라이브러리를 가리키는 경로입니다.

.. option:: GDAL_USE_MYSQL=ON/OFF

    MYSQL을 사용할지 여부를 제어합니다. MYSQL이 검색되는 경우 기본값은 ON입니다.


NetCDF
******

`netCDF <https://github.com/Unidata/netcdf-c>`_ 는 :ref:`raster.netcdf`
드라이버를 활성화시키기 위해 필수적인 라이브러리입니다.
``nc-config`` 프로그램으로 탐지할 수 있습니다.

.. option:: NETCDF_INCLUDE_DIR

    ``netcdf.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: NETCDF_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_NETCDF=ON/OFF

    netCDF를 사용할지 여부를 제어합니다. netCDF가 검색되는 경우 기본값은 ON입니다.


ODBC
****

ODBC는 :ref:`vector.odbc`, :ref:`vector.pgeo`, :ref:`vector.walk` 및
:ref:`vector.mssqlspatial` 등 다양한 드라이버를 사용하기 위해 필수적인
라이브러리입니다.
유닉스와 윈도우 상에서는 보통 시스템 디렉터리에서 자동적으로 검색됩니다.

.. option:: ODBC_INCLUDE_DIR

    ``sql.h`` 헤더 파일을 가진 ODBC include 디렉터리를 가리키는 경로입니다.

.. option:: ODBC_LIBRARY

    링크될 ODBC 라이브러리를 가리키는 경로입니다.

.. option:: GDAL_USE_ODBC=ON/OFF

    ODBC를 사용할지 여부를 제어합니다. ODBC가 검색되는 경우 기본값은 ON입니다.


OGDI
****

`OGDI <https://github.com/libogdi/ogdi/>`_ 는 :ref:`vector.ogdi` 드라이버를
사용하기 위해 필수적인 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.

.. option:: OGDI_INCLUDE_DIR

    ``ecs.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: OGDI_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_OGDI=ON/OFF

    OGDI를 사용할지 여부를 제어합니다. OGDI가 검색되는 경우 기본값은 ON입니다.


OpenCL
******

OpenCL 라이브러리는 일반적으로 GPU와 함께 왜곡 작업(warping) 계산의 속도를
올리기 위해 사용될 수 있습니다.

.. note::

    이 라이브러리는 검색된 경우라도 기본적으로 비활성화되어 있습니다.
    현재 OpenCL의 왜곡 작업 구현이 일반 구현의 속도보다 뒤쳐지기 때문입니다.

.. option:: OpenCL_INCLUDE_DIR

    ``CL/cl.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: OpenCL_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_OPENCL=ON/OFF

    OPENCL을 사용할지 여부를 제어합니다. OPENCL이 검색되는 경우 기본값은 *OFF* 입니다.


OpenEXR
*******

`OpenEXR <https://github.com/AcademySoftwareFoundation/openexr>`_ 는
:ref:`raster.exr` 드라이버를 사용하기 위해 필수적인 라이브러리입니다.

``OpenEXR_ROOT`` 변수가 하위 디렉터리 /lib 및 /include의, 예를 들어
/DEV/lib/openexr-3.0 같은 상위 디렉터리를 가리키도록 지정하십시오.
OpenEXR 3 이상 버전의 경우 추가로 ``Imath_ROOT`` 변수도 지정하십시오.
Imath는 이제, 예를 들면 /DEV/lib/imath-3.1.3 같은 별개의 라이브러리이기 때문입니다.

또는

OpenEXR의 pkgconfig를 찾으려면 ``CMAKE_PREFIX_PATH`` 변수에 루트 디렉터리를
추가로 지정하십시오.
예를 들면 -DCMAKE_PREFIX_PATH=/DEV/lib/openexr-3.0;/DEV/lib/imath-3.1.3 처럼 말이죠.

또는

정말로 명확하게 하려면 ``OpenEXR_INCLUDE_DIR``, ``Imath_INCLUDE_DIR``,
``OpenEXR_LIBRARY``, ``OpenEXR_UTIL_LIBRARY``, ``OpenEXR_HALF_LIBRARY``,
``OpenEXR_IEX_LIBRARY`` 변수들을 분명하게 설정하십시오.

.. option:: GDAL_USE_OPENEXR=ON/OFF

    OpenEXR를 사용할지 여부를 제어합니다. OpenEXR가 검색되는 경우 기본값은 ON입니다.


OpenJPEG
********

`OpenJPEG <https://github.com/uclouvain/openjpeg>`_ 라이브러리는 C 언어로
작성된 오픈 소스 JPEG-2000 코덱입니다. OpenJPEG은 :ref:`raster.jp2openjpeg`
드라이버, 또는 JPEG-2000 기능을 사용하는 다른 드라이버들을 사용하기 위해 필수적인
라이브러리입니다.

.. option:: OPENJPEG_INCLUDE_DIR

    ``openjpeg.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: OPENJPEG_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_OPENJPEG=ON/OFF

    OpenJPEG을 사용할지 여부를 제어합니다. OpenJPEG이 검색되는 경우 기본값은 ON입니다.


OpenSSL
*******

`OpenSSL <https://github.com/openssl/openssl>`_ 라이브러리의 Crypto 요소는
구글 클라우드의 인증 메소드 가운데 일부가 사용하는 RSA SHA256 서명 기능에 쓰일 수
있습니다. :ref:`raster.eedai` 이미지 또는 :ref:`/vsigs/ <vsigs>` 가상 파일
시스템을 필수적으로 사용해야 할 수도 있습니다.

이 라이브러리를 환경설정하는 방법에 대해 자세히 알고 싶다면
https://cmake.org/cmake/help/latest/module/FindOpenSSL.html
을 읽어보십시오.

.. option:: GDAL_USE_OPENSSL=ON/OFF

    OpenSSL을 사용할지 여부를 제어합니다. OpenSSL이 검색되는 경우 기본값은 ON입니다.


Oracle
******

오라클(Oracle) 인스턴스 클라이언트 SDK(사유 소스)는 :ref:`vector.oci` 및
:ref:`raster.georaster` 드라이버를 사용하기 위해 필수적인 라이브러리입니다.

.. option:: Oracle_ROOT

    오라클 인스턴스 클라이언트 SDK의 루트 디렉터리를 가리키는 경로입니다.

.. option:: GDAL_USE_ORACLE=ON/OFF

    오라클을 사용할지 여부를 제어합니다. 오라클이 검색되는 경우 기본값은 ON입니다.


PCRE2
*****

`PCRE2 <https://github.com/PhilipHazel/pcre2>`_ 는 펄(Perl) 호환 정규
표현식 지원을 구현합니다. SQLite3을 사용하는 드라이버에서 REGEXP 연산자 용으로
이 라이브러리를 사용합니다.

.. option:: PCRE2_INCLUDE_DIR

    ``pcre2.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: PCRE2_LIBRARY

    이름에 "pcre2-8" 이 포함된 공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_PCRE2=ON/OFF

    PCRE2를 사용할지 여부를 제어합니다. PCRE2가 검색되는 경우 기본값은 ON입니다.


PDFium
******

`PDFium <https://github.com/rouault/pdfium_build_gdal_3_4>`_ 라이브러리는
:ref:`raster.pdf` 드라이버 용 백엔드 후보 가운데 하나입니다.

.. option:: PDFium_INCLUDE_DIR

    ``public/fpdfview.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: PDFium_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_PDFIUM=ON/OFF

    PDFium을 사용할지 여부를 제어합니다. PDFium이 검색되는 경우 기본값은 ON입니다.


PNG
***

`libpng <https://github.com/glennrp/libpng>`_ 는 :ref:`raster.png` 드라이버를
사용하기 위해 필수적인 라이브러리로, 몇몇 다른 (:ref:`raster.grib`, :ref:`raster.gpkg` 등등)
드라이버가 사용할 수도 있습니다. 검색되지 않는 경우, libpng의 내부 복사본을 사용할 것입니다.
이 라이브러리를 탐지하는 방법에 대해 더 자세히 알고 싶다면
See https://cmake.org/cmake/help/latest/module/FindPNG.html 을 읽어보십시오.

.. option:: PNG_PNG_INCLUDE_DIR

    ``png.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: PNG_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을 빌드하기 위해
    비슷한 라이브러리에 비슷한 ``PNG_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_PNG=ON/OFF

    외부 libpng를 사용할지 여부를 제어합니다.
    외부 libpng가 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_PNG_INTERNAL=ON/OFF

    내부 libpng를 사용할지 여부를 제어합니다.
    외부 libpng가 검색되지 않는 경우 기본값은 ON입니다.


Poppler
*******

`Poppler <https://poppler.freedesktop.org/>`_ 라이브러리는
:ref:`raster.pdf` 드라이버 용 백엔드 후보 가운데 하나입니다.

.. option:: Poppler_INCLUDE_DIR

    ``poppler-config.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: Poppler_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_POPPLER=ON/OFF

    Poppler를 사용할지 여부를 제어합니다. Poppler가 검색되는 경우 기본값은 ON입니다.


PostgreSQL
**********

`PostgreSQL 클라이언트 라이브러리 <https://www.postgresql.org/>`_ 는
:ref:`vector.pg` 및 :ref:`raster.postgisraster` 드라이버를 사용하기 위해 필수적입니다.

.. option:: PostgreSQL_INCLUDE_DIR

    ``libpq-fe.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: PostgreSQL_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일 ``pq`` / ``libpq`` 를 가리키는 경로입니다.
    디버그 배포판을 빌드하기 위해 비슷한 라이브러리에 비슷한
    ``PostgreSQL_LIBRARY_DEBUG`` 변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_POSTGRESQL=ON/OFF

    PostgreSQL을 사용할지 여부를 제어합니다. PostgreSQL이 검색되는 경우 기본값은 ON입니다.


PROJ
****

`PROJ <https://github.com/OSGeo/PROJ/>`_ 6 이상 버전은 GDAL에 *필수적인* 의존성입니다.

.. option:: PROJ_INCLUDE_DIR

    ``proj.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: PROJ_LIBRARY_RELEASE

    ``proj.dll``, ``libproj.so``, ``proj.lib`` 또는 다른 이름 같은
    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``PROJ_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.


QHULL
*****

`QHULL <https://github.com/qhull/qhull>`_ 라이브러리는 gdal_grid의
선형 보간(linear interpolation)에 사용됩니다.
검색되지 않을 경우, 내부 복사본을 사용합니다.

.. option:: QHULL_PACKAGE_NAME

   pkg-config 패키지의 이름으로, 일반적으로 ``qhull_r`` 또는 ``qhullstatic_r`` 입니다.
   기본값은 ``qhull_r`` 입니다.

.. option:: QHULL_INCLUDE_DIR

    ``libqhull_r/libqhull_r.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: QHULL_LIBRARY

    오목(reentrant) 라이브러리의 공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_QHULL=ON/OFF

    QHULL을 사용할지 여부를 제어합니다. QHULL이 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_QHULL_INTERNAL=ON/OFF

    내부 QHULL 복사본을 사용할지 여부를 제어합니다.
    외부 QHULL이 검색되지 않는 경우 기본값은 ON입니다.


RASTERLITE2
***********

`RasterLite2 <https://www.gaia-gis.it/fossil/librasterlite2/index>`_ (1.1.0버전 이상)는
:ref:`raster.rasterlite2` 드라이버가 이용하는 라이브러리입니다.
pkg-config으로 탐지할 수 있습니다.

.. option:: RASTERLITE2_INCLUDE_DIR

    ``rasterlite2/rasterlite2.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: RASTERLITE2_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_RASTERLITE2=ON/OFF

    RasterLite2를 사용할지 여부를 제어합니다. RasterLite2가 검색되는 경우 기본값은 ON입니다.


rdb
***

`RDB <https://repository.riegl.com/software/libraries/rdblib>` (사유 소스)는
:ref:`raster.rdb` 드라이버를 사용하기 위해 필수적인 라이브러리입니다.
``CMAKE_PREFIX_PATH`` 변수에 설치 접두어를 지정하십시오.

.. option:: GDAL_USE_RDB=ON/OFF

    rdb를 사용할지 여부를 제어합니다. rdb가 검색되는 경우 기본값은 ON입니다.


SPATIALITE
**********

`Spatialite <https://www.gaia-gis.it/fossil/libspatialite/index>`_ 는
:ref:`vector.sqlite` 및 :ref:`vector.gpkg` 드라이버, 그리고 :ref:`sql_sqlite_dialect`
가 이용하는 라이브러리입니다. pkg-config으로 탐지할 수 있습니다.

.. option:: SPATIALITE_INCLUDE_DIR

    ``spatialite.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: SPATIALITE_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_SPATIALITE=ON/OFF

    Spatialite를 사용할지 여부를 제어합니다. Spatialite가 검색되는 경우 기본값은 ON입니다.


SQLite3
*******

`SQLite3 <https://sqlite.org/index.html>`_ 는 :ref:`vector.sqlite` 및
:ref:`vector.gpkg` 드라이버(그리고 다른 드라이버들도), 그리고
:ref:`sql_sqlite_dialect` 를 사용하기 위해 필수적인 라이브러리입니다.

.. option:: SQLite3_INCLUDE_DIR

    ``sqlite3.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: SQLite3_LIBRARY

    ``sqlite3.dll``, ``libsqlite3.so``, ``sqlite3.lib`` 또는 다른 이름 같은
    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_SQLITE3=ON/OFF

    SQLite3를 사용할지 여부를 제어합니다. SQLite3가 검색되는 경우 기본값은 ON입니다.


SFCGAL
******

`SFCGAL <https://github.com/Oslandia/SFCGAL>`_ 은 3D 작업(PolyhedralSurface,
TINs 등등)을 위한 ISO 19107:2013과 OGC 단순 피처 접근(OGC Simple Features Access)
1.2를 지원하는 도형 라이브러리입니다.

.. option:: SFCGAL_INCLUDE_DIR

    기반 include 디렉터리를 가리키는 경로입니다.

.. option:: SFCGAL_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``SFCGAL_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_SFCGAL=ON/OFF

    SFCGAL을 사용할지 여부를 제어합니다. SFCGAL이 검색되는 경우 기본값은 ON입니다.


SWIG
****

`SWIG <http://swig.org/>`_ 은 C와 C++로 작성된 프로그램을 다양한 고급 프로그래밍
언어들과 연결시켜주는 소프트웨어 개발 도구입니다. 파이썬, 자바 및 C# 바인딩을
위해 쓰입니다.

.. option:: SWIG_EXECUTABLE

    SWIG 실행 파일을 가리키는 경로입니다.


TEIGHA
******

TEIGHA / 오픈 디자인 동맹(Open Design Alliance) 라이브러리(사유 소스)는
:ref:`vector.dwg` 및 :ref:`vector.dgnv8` 드라이버를 사용하기 위해
필수적인 라이브러리입니다. 공유 라이브러리로 이루어진 SDK를 가진 리눅스 상에서
응용 프로그램들의 링크 작업이 성공하기 위해서는 SDK의 bin/{platform_name}
하위 디렉터리가 LD_LIBRARY_PATH에 지정돼 있어야 한다는 점을 기억하십시오.
TEIGHA_ROOT 변수는 설정돼 있어야만 합니다.

.. option:: TEIGHA_ROOT

    커널 및 드로잉(drawings) 패키지가 추출되어야만 하는 기반 디렉터리를
    가리키는 경로입니다.

.. option:: TEIGHA_ACTIVATION_FILE_DIRECTORY

    ``OdActivationInfo`` 파일이 있는 디렉터리를 가리키는 경로입니다.
    이 파일이 TEIGHA_ROOT 경로 아래 있는 경우, 자동적으로 검색될 것입니다.
    그렇지 않다면 최근 SDK 버전(최소 2021 이상)에 대해 이 변수를
    설정해야만 합니다.

.. option:: GDAL_USE_TEIGHA=ON/OFF

    TEIGHA를 사용할지 여부를 제어합니다. TEIGHA가 검색되는 경우 기본값은 ON입니다.


TIFF
****

`libtiff <https://gitlab.com/libtiff/libtiff/>`_ 는 :ref:`raster.gtiff`
드라이버와 몇몇 다른 드라이버들을 사용하기 위해 필수적인 라이브러리입니다.
이 라이브러리가 검색되지 않는 경우, 내부 libtiff 복사본을 사용할 것입니다.

.. option:: TIFF_INCLUDE_DIR

    ``tiff.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: TIFF_LIBRARY_RELEASE

    ``tiff.dll``, ``libtiff.so``, ``tiff.lib`` 또는 다른 이름 같은
    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``TIFF_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_TIFF=ON/OFF

    외부 libtiff를 사용할지 여부를 제어합니다.
    외부 libtiff가 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_TIFF_INTERNAL=ON/OFF

    내부 libtiff 복사본을 사용할지 여부를 제어합니다.
    외부 libtiff가 검색되지 않는 경우 기본값은 ON입니다.


TileDB
******

`TileDB <https://github.com/TileDB-Inc/TileDB>` 는 :ref:`raster.tiledb`
드라이버를 사용하기 위해 필수적인 라이브러리입니다.
``CMAKE_PREFIX_PATH`` 변수에 설치 접두어를 지정하십시오.

.. option:: GDAL_USE_TILEDB=ON/OFF

    TileDB를 사용할지 여부를 제어합니다. TileDB가 검색되는 경우 기본값은 ON입니다.


WebP
****

`WebP <https://github.com/webmproject/libwebp>`_ 는 이미지 압축 라이브러리입니다.
:ref:`raster.webp` 드라이버를 사용하기 위해 필수적이며, :ref:`raster.gpkg` 및
내부 libtiff 라이브러리가 이용할 수도 있습니다.

.. option:: WEBP_INCLUDE_DIR

    ``webp/encode.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: WEBP_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_WEBP=ON/OFF

    WebP를 사용할지 여부를 제어합니다. WebP가 검색되는 경우 기본값은 ON입니다.


XercesC
*******

`Xerces-C <https://github.com/apache/xerces-c>`_ 는 스트림 향(stream-oriented)
XML 파서(parser; 구문 분석기)로, :ref:`vector.nas`, :ref:`vector.ili` 및
:ref:`vector.gmlas` 드라이버의 XML 파싱 기능을 활성화하기 위해 필수적인 라이브러리입니다.
GML 드라이버의 경우 Expat 대신 이 라이브러리를 이용할 수도 있습니다.

.. option:: XercesC_INCLUDE_DIR

    기반 include 디렉터리를 가리키는 경로입니다.

.. option:: XercesC_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_XERCESC=ON/OFF

    XercesC를 사용할지 여부를 제어합니다. XercesC가 검색되는 경우 기본값은 ON입니다.


ZLIB
****

`ZLib <https://github.com/madler/zlib>`_ 은 비손실 Deflate/Zip 압축 알고리즘을
제공하는 압축 라이브러리입니다.

.. option:: ZLIB_INCLUDE_DIR

    ``zlib.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: ZLIB_LIBRARY_RELEASE

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다. 디버그 배포판을
    빌드하기 위해 비슷한 라이브러리에 비슷한 ``ZLIP_LIBRARY_DEBUG``
    변수를 지정할 수도 있습니다.

.. option:: GDAL_USE_ZLIB=ON/OFF

    ZLIB을 사용할지 여부를 제어합니다. ZLIB이 검색되는 경우 기본값은 ON입니다.

.. option:: GDAL_USE_ZLIB_INTERNAL=ON/OFF

    내부 zlib 복사본을 사용할지 여부를 제어합니다.
    외부 zlib이 검색되지 않는 경우 기본값은 ON입니다.


ZSTD
****

`ZSTD <https://github.com/facebook/zstd>`_ 는 비손실 ZStd 압축 알고리즘을
제공하는 압축 라이브러리입니다. (Deflate/ZIP보다 빠르지만, 호환되지는 않습니다.)
내부 libtiff 라이브러리 또는 :ref:`raster.zarr` 드라이버가 사용합니다.

.. option:: ZSTD_INCLUDE_DIR

    ``zstd.h`` 헤더 파일을 가진 include 디렉터리를 가리키는 경로입니다.

.. option:: ZSTD_LIBRARY

    공유 또는 정적 라이브러리 파일을 가리키는 경로입니다.

.. option:: GDAL_USE_ZSTD=ON/OFF

    ZSTD를 사용할지 여부를 제어합니다. ZSTD가 검색되는 경우 기본값은 ON입니다.


드라이버 선택
++++++++++++++++++++

기본적으로 빌드 필요조건을 만족하는 모든 드라이버는 GDAL 핵심 라이브러리에
내장될 것입니다.

드라이버 하위 집합(subset)을 선택하기 위해 다음 옵션들을 사용할 수 있습니다:

.. option:: GDAL_ENABLE_DRIVER_<driver_name>:BOOL=ON/OFF

.. option:: OGR_ENABLE_DRIVER_<driver_name>:BOOL=ON/OFF

    전체 수준 습성(global behavior)을 제어하는 옵션과는 별개로,
    이 옵션들로 드라이버를 독립적으로 활성화 또는 비활성화할 수 있습니다.

.. option:: GDAL_BUILD_OPTIONAL_DRIVERS:BOOL=ON/OFF

.. option:: OGR_BUILD_OPTIONAL_DRIVERS:BOOL=ON/OFF

    전체 수준에서 모든 GDAL/래스터 또는 OGR/벡터 드라이버를 활성화/비활성시킵니다.
    정확히 말하자면, 이 변수들을 ON으로 설정하면 (다음 변수들이 아직 설정되지 않은 경우)
    ``GDAL_ENABLE_DRIVER_<driver_name>`` 또는 ``OGR_ENABLE_DRIVER_<driver_name>``
    변수의 기본값에 영향을 끼칩니다.

    ``GDAL_ENABLE_DRIVER_<driver_name>:BOOL=ON`` 또는 ``OGR_ENABLE_DRIVER_<driver_name>:BOOL=ON``
    변수를 이용해서 이 습성을 드라이버 하위 집합의 개별 활성화와 결합할 수 있습니다.
    CMake를 처음 실행한 후 GDAL_BUILD_OPTIONAL_DRIVERS / OGR_BUILD_OPTIONAL_DRIVERS의
    값을 변경하더라도 개별 드라이버의 활성화는 변경되지 않는다는 사실을 기억하십시오.
    개별 드라이버의 상태를 리셋하려면 ``-UGDAL_ENABLE_DRIVER_* -UOGR_ENABLE_DRIVER_*`` 를
    전달(pass)해줘야 할 수도 있습니다.

JP2OpenJPEG 및 SVG 드라이버의 최소 빌드를 활성화하는 예시::

    cmake .. -UGDAL_ENABLE_DRIVER_* -UOGR_ENABLE_DRIVER_* \
             -DGDAL_BUILD_OPTIONAL_DRIVERS:BOOL=OFF -DOGR_BUILD_OPTIONAL_DRIVERS:BOOL=OFF \
             -DGDAL_ENABLE_DRIVER_JP2OPENPEG:BOOL=ON \
             -DOGR_ENABLE_DRIVER_SVG:BOOL=ON


드라이버를 플러그인으로 빌드
++++++++++++++++++++++++++

모든 드라이버는 아니지만, 중요한 드라이버 하위 집합을 플러그인으로 빌드할 수도 있습니다.
즉 GDAL 설치본의 ``gdalplugins`` 하위 디렉터리에 독립적인(standalone) .dll/.so
공유 라이브러리로써 설치되도록 말입니다. 이는 GDAL 핵심 라이브러리와는 다른
(상용, 카피레프트 등등) 사용허가를 가진 라이브러리를 의존하고 있는 드라이버의 경우
특히 유용할 수 있습니다.

플러그인으로 빌드할 수 있는 드라이버 목록은 다음과 같이 얻을 수 있습니다::

    cmake .. -L | grep -e "_ENABLE.*PLUGIN"

드라이버의 플러그인/내장(builtin) 상태를 선택하려면 다음 옵션들을 사용할 수 있습니다:

.. option:: GDAL_ENABLE_DRIVER_<driver_name>_PLUGIN:BOOL=ON/OFF

.. option:: OGR_ENABLE_DRIVER_<driver_name>_PLUGIN:BOOL=ON/OFF

    전체 수준 습성(global behavior)을 제어하는 옵션과는 별개로,
    이 옵션들로 드라이버를 독립적으로 활성화 또는 비활성화할 수 있습니다.

    빌드될 드라이버의 경우 해당하는 기반 ``GDAL_ENABLE_DRIVER_{driver_name}:BOOL=ON``
    또는 ``OGR_ENABLE_DRIVER_{driver_name}:BOOL=ON`` 옵션을 설정해야만 한다는
    사실을 기억하십시오.

.. option:: GDAL_ENABLE_PLUGINS:BOOL=ON/OFF

    전체 수준에서 (플러그인으로 빌드할 수 있는) 모든 GDAL 및 OGR의 드라이버들을
    플러그인으로 빌드하는 작업을 활성화/비활성화시킵니다. 정확히 말하자면, 이 변수를
    ON으로 설정하면 (다음 변수들이 아직 설정되지 않은 경우)
    ``GDAL_ENABLE_DRIVER_<driver_name>_PLUGIN`` 또는
    ``OGR_ENABLE_DRIVER_<driver_name>_PLUGIN`` 변수의 기본값에 영향을 끼칩니다.

    ``GDAL_ENABLE_DRIVER_{driver_name}_PLUGIN:BOOL`` 또는
    ``OGR_ENABLE_DRIVER_{driver_name}_PLUGIN:BOOL``
    변수를 이용해서 이 습성을 플러그인 상태의 개별 활성화/비활성화와 결합할 수 있습니다.
    CMake를 처음 실행한 후 GDAL_ENABLE_PLUGINS의 값을 변경하더라도 개별 드라이버의
    플러그인 상태의 활성화는 변경되지 않는다는 사실을 기억하십시오.
    개별 드라이버의 플러그인 상태를 리셋하려면 ``-UGDAL_ENABLE_DRIVER_* -UOGR_ENABLE_DRIVER_*`` 를
    전달(pass)해줘야 할 수도 있습니다.

JP2OpenJPEG을 제외하고, 플러그인으로 빌드할 수 있는 모든 드라이버를 플러그인으로 빌드하는 예시::

    cmake .. -UGDAL_ENABLE_DRIVER_* -UOGR_ENABLE_DRIVER_* \
             -DGDAL_ENABLE_PLUGINS:BOOL=ON \
             -DGDAL_ENABLE_DRIVER_JP2OPENPEG_PLUGIN:BOOL=OFF

``GDAL_ENABLE_PLUGINS:BOOL=ON`` 변수의 경우 미묘한 점이 존재합니다. 이 변수는
플러그인으로 빌드할 수 있는 드라이버 가운데 GDAL 핵심 의존성의 한 부분이 아니라
외부 의존성을 가지고 있는 (예: netCDF, HDF4, Oracle, PDF 등등) 드라이버의
플러그인 상태만 제어합니다.

.. option:: GDAL_ENABLE_PLUGINS_NO_DEPS:BOOL=ON/OFF

    전체 수준에서 (플러그인으로 빌드할 수 있는) 모든 GDAL 및 OGR의 드라이버들 가운데
    외부 의존성을 가지고 있지 않은 (예: BMP, FlatGeobuf) 드라이버를, 또는 GDAL 핵심
    의존성의 한 부분인 의존성을 가지고 있는 (예: GPX) 드라이버를 플러그인으로 빌드하는
    작업을 활성화/비활성화시킵니다. 일반적으로 이런 드라이버들을 빌드하는 작업은 필요하지
    않기 때문에, GDAL_ENABLE_PLUGINS와는 다른 옵션을 사용하는 것입니다.

어떤 상황에서는, GDAL 플러그인을 불러오지 않는 것이 적절할 수도 있습니다.
다음과 같이 설정하면 됩니다:

.. option:: GDAL_AUTOLOAD_PLUGINS:BOOL=ON/OFF

    OFF로 설정하면 GDAL 플러그인을 불러오는 것을 막습니다. 기본값은 ON입니다.


파이썬 바인딩 옵션
+++++++++++++++++++++++

.. option:: BUILD_PYTHON_BINDINGS:BOOL=ON/OFF

    파이썬 바인딩을 빌드해야 하는지 여부를 설정합니다. 기본값은 ON이지만,
    파이썬 설치본이 검색된 경우에만 유효합니다.

명목상의 파이썬 설치본은 (3.6버전 이상의) 파이썬 런타임과 셋업 도구 모듈로 이루어져
있어야 합니다. 넘파이(NumPy)와 넘파이 헤더 및 개발 라이브러리도 강력히 권장합니다.

파이썬 설치본은 경로에 설정되었거나 또는 파이썬 설치 관리자의 기타 표준 설치 메커니즘을
통해 등록된 경우 보통 검색됩니다.
https://cmake.org/cmake/help/git-stage/module/FindPython.html 에서 자세히
설명하고 있는 대로, 변수 몇 개를 사용해서 지정할 수도 있습니다.

GDAL도 다음 옵션을 제공하고 있습니다:

.. option:: Python_LOOKUP_VERSION:STRING=major.minor.patch

    이 옵션을 지정하면, Python_FIND_STRATEGY=VERSION 옵션도 지정되어 있을 것이라고
    상정합니다. EXACT 전략을 취하기 때문에 패치 숫자를 지정해야만 한다는 사실을
    기억하세요.

기타 유용한 옵션들:

.. option:: Python_FIND_VIRTUALENV

    virtualenv를 활성화해서 사용하려면 'ONLY'라고 지정하십시오.

.. option:: Python_ROOT

    파이썬 설치 접두어를 지정하십시오.

예시::

    cmake -DPython_LOOKUP_VERSION=3.6.0 ..
    cmake -DPython_FIND_VIRTUALENV=ONLY ..
    cmake -DPython_ROOT=C:\Python36 ..


다음은 고급 옵션들로 ``install`` CMake 대상(target)인 도중에만 적용됩니다.

.. option:: GDAL_PYTHON_INSTALL_PREFIX

    ``CMAKE_INSTALL_PREFIX`` 옵션을 무시(override)하기 위해 이 옵션을
    디렉터리 이름으로 지정할 수 있습니다.
    이 옵션은 ``python setup.py install`` 의 ``--prefix`` 옵션의 값을
    설정하기 위해 쓰입니다.

.. option:: GDAL_PYTHON_INSTALL_LAYOUT

    ``python setup.py install`` 의 ``--install-layout`` 옵션의 값을
    설정하기 위해 이 옵션을 지정할 수 있습니다. 파이썬 설치 과정에서
    ``site-packages`` 하위 디렉터리를 찾고 있다는 사실이 탐지되는 경우
    기본적으로 설치 지침(install layout)을 ``deb`` 으로 설정합니다.
    그렇지 않으면 지정하지 않습니다.

.. option:: GDAL_PYTHON_INSTALL_LIB

    ``python setup.py install`` 의 ``--install-lib`` 옵션의 값을
    설정하기 위해 이 옵션을 지정할 수 있습니다. 이 옵션은 맥OS 상에서
    파이썬이 프레임워크로 설치되는 경우에만 적용됩니다.

자바 바인딩 옵션
+++++++++++++++++++++

.. option:: BUILD_JAVA_BINDINGS:BOOL=ON/OFF

    자바 바인딩을 빌드해야 하는지 여부를 설정합니다. 기본값은 ON이지만,
    자바 런타임과 개발 패키지가 검색된 경우에만 유효합니다.
    https://cmake.org/cmake/help/latest/module/FindJava.html 및
    https://cmake.org/cmake/help/latest/module/FindJNI.html 에서
    설정할 수 있는 관련 옵션들을 설명하고 있습니다.
    ``ant`` 바이너리 또한 PATH에서 사용할 수 있어야만 합니다.

.. option:: GDAL_JAVA_INSTALL_DIR

    gdalalljni 라이브러리와 .jar 파일들을 설치할 하위 디렉터리입니다.
    기본값은 "${CMAKE_INSTALL_DATADIR}/java"입니다.

유지관리자만 사용할 옵션:

.. option:: GPG_KEY

    빌드 요소들을 서명하기 위한 GPG 키입니다.
    bundle.jar를 생성해야 합니다.

.. option:: GPG_PASS

    빌드 요소들을 서명하기 위한 GPG 비밀구절(pass phrase)입니다.


드라이버 특정 옵션
+++++++++++++++++++++++

.. option:: GDAL_USE_PUBLICDECOMPWT

    :ref:`raster.msg` 드라이버는 이 옵션이 ON으로 설정된 경우에만 (기본값은 OFF) 빌드됩니다.
    이 옵션이 ON인 경우 https://gitlab.eumetsat.int/open-source/PublicDecompWT.git 저장소를
    빌드 트리로 다운로드해서 필요한 파일들을 드라이버로 빌드합니다.


윈도우에서 콘다 의존성과 비주얼 스튜디오로 빌드하기
--------------------------------------------------------------------------------

이 방법은 GDAL의 디버그 빌드 용으로는 vcpkg 같은 다른 방법들보다 조금 부적합합니다.

git 설치
+++++++++++

`git <https://git-scm.com/download/win>`_ 을 설치하십시오.

miniconda 설치
+++++++++++++++++

`miniconda <https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe>`_ 를
설치하십시오.

GDAL 의존성 설치
+++++++++++++++++++++++++

콘다(Conda) 활성 콘솔을 시작한 다음 c:\\dev 디렉터리가 존재한다고 가정합니다.

::

    cd c:\dev
    conda create --name gdal
    conda activate gdal
    conda install --yes --quiet curl libiconv icu git python=3.7 swig numpy pytest zlib clcache
    conda install --yes --quiet -c conda-forge compilers
    conda install --yes --quiet -c conda-forge \
        cmake proj geos hdf4 hdf5 \
        libnetcdf openjpeg poppler libtiff libpng xerces-c expat libxml2 kealib json-c \
        cfitsio freexl geotiff jpeg libpq libspatialite libwebp-base pcre postgresql \
        sqlite tiledb zstd charls cryptopp cgal jasper librttopo libkml openssl xz

.. note::

    ``compilers`` 패키지가 CMake가 선택할 수 있는 적절한 환경을 설정하기 위해
    (문서 작성 당시) ``vs2017_win-64`` 를 설치할 것입니다. 비주얼 스튜디오 2019를
    사용할 예정이라면 ``vs2019_win-64`` 패키지를 사용해도 됩니다.

GDAL 소스 체크아웃
+++++++++++++++++++++

::

    cd c:\dev
    git clone https://github.com/OSGeo/gdal.git

GDAL 빌드
++++++++++

콘다(Conda) 활성 콘솔에서

::

    conda activate gdal
    cd c:\dev\gdal
    cmake -S . -B build -DCMAKE_PREFIX_PATH:FILEPATH="%CONDA_PREFIX%" \
                        -DCMAKE_C_COMPILER_LAUNCHER=clcache
                        -DCMAKE_CXX_COMPILER_LAUNCHER=clcache
    cmake --build build --config Release -j 8

.. only:: FIXME

    GDAL 테스트 실행
    ++++++++++++++++

    ::

        cd c:\dev\GDAL
        cd _build.vs2019
        ctest -V --build-config Release
