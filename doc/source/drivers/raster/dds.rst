.. _raster.dds:

================================================================================
DDS -- DirectDraw Surface
================================================================================

.. shortname:: DDS

.. build_dependencies:: Crunch Lib

DirectDraw Surface 파일 포맷은 마이크로소프트 사가 개발했으며, S3 텍스처 손실 압축(S3TC)으로 압축된 데이터를 저장하기 위한 표준입니다. (파일 확장자는 DDS입니다.) 크런치 라이브러리가 DDS 포맷과 압축을 지원합니다.

GDAL 3.1버전부터 이 포맷의 읽기를 지원합니다. 이전 버전까지는 쓰기만 지원했습니다.

이 드라이버는 DXT1, DXT1A, DXT3(기본값), DXT5 및 ETC1 텍스처 포맷을 지원합니다. FORMAT 생성 옵션을 사용해서 텍스처 포맷을 설정할 수 있습니다.

이 드라이버는 SUPERFAST, FAST, NORMAL(기본값), BETTER 및 UBER 압축 품질을 지원합니다. QUALITY 생성 옵션을 사용해서 압축 품질을 설정할 수 있습니다.

더 자세한 정보는 `Crunch Lib <https://github.com/BinomialLLC/crunch>`_ 을 읽어보십시오.

주의: ``gdal/frmts/dds/ddsdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::


빌드 지침
------------------

크런치를 빌드하는 일은 조금 어려울 수도 있습니다. https://github.com/rouault/crunch/ 의 `build_fixes` 분기는 CMake 빌드 시스템은 물론 업스트림 저장소에는 없는 수정 사항 몇 가지를 포함하고 있습니다.

크런치 빌드
++++++++++++

리눅스
*****

.. code-block::

    git clone -b build_fixes https://github.com/rouault/crunch
    cd crunch
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/install-crunch -DCMAKE_BUILD_TYPE=Release
    make -j8 install

윈도우
*******

.. code-block::

    git clone -b build_fixes https://github.com/rouault/crunch
    cd crunch
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=c:\dev\install-crunch -G "Visual Studio 15 2017 Win64"
    cmake --build . --config Release --target install

크런치를 대상으로 GDAL 빌드
+++++++++++++++++++++++++

리눅스
*****

.. code-block::

    ./configure --with-dds=$HOME/install-crunch

윈도우
*******

nmake.local에 다음 내용을 추가하십시오:

.. code-block::

    CRUNCH_INC = -Ic:\dev\install-crunch\include\crunch
    CRUNCH_LIB = c:\dev\install-crunch\lib\crunch.lib
