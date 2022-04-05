.. _vector.oda:

오픈 디자인 얼라이언스 - ODA 플랫폼
===================================

GDAL이 오토캐드 DWG 및 마이크로스테이션 DGN 버전 8 파일의 읽기를 지원하기 위해서는 예전에 Teigha라는 이름이었던 ODA(Open Design Alliance) 플랫폼이 필수적입니다.
이 드라이버들을 활성화하려면 GDAL/OGR를 반드시 ODA 지원과 함께 빌드해야만 합니다.

ODA 요구 사항
---------------------

ODA 플랫폼은 SDK 몇 개를 포함합니다. Drawings SDK는 객체지향 API를 통해 .dwg 및 .dgn 파일의 모든 데이터에 접근할 수 있습니다. GDAL을 컴파일해야 합니다. 모든 상품에 Kernel SDK가 필수이기 때문에, 다음 두 상품을 다운로드해야만 합니다:

-  Kernel
-  Drawings

이 라이브러리들은 공개되지 않았습니다. 이 라이브러리들을 사용하려면 멤버십을 구매해야 합니다. 멤버십 인증 후 `ODA 멤버 다운로드 <https://www.opendesign.com/members/memberfiles>`_ 에서 라이브러리를 다운로드할 수 있습니다.

라이브러리 다운로드
-----------------

알맞은 파일을 선택해서 다운로드하려면, 다음 (리눅스 용) ODA 명명 규범을 고려하십시오:

-  lnx - 리눅스
-  X86, X64 - X86 또는 X64 플랫폼을 나타냅니다.
-  4.4, 4.7, 4.8, 4.9, 5.2, 5.3, 6.3, 7.2, 8.3 - GCC 버전
-  dll - 공유 라이브러리 버전을 나타냅니다.
-  pic - 위치 독립 코드(Position Independent Code; PIC)로 컴파일되었습니다.

ODA 압축 파일은 배포판들을 구분하기 위해 21.2 또는 21.6 같은 배포판 접미어를 포함하고 있습니다.

리눅스 용 필수 파일을 다운로드하려면, 다음 파일들을 다운로드하면 됩니다:

-  `Kernel_lnxX64_7.2dll_21.6.tar.gz`
-  `Drawings_lnxX64_7.2dll_21.6.tar.gz`

이 예시에서 파일명의 의미는:

-  `lnx`: 리눅스 용
-  `X64`: X64 아키텍처 용
-  `7.2`: GCC 7.2버전
-  `dll`: 공유 라이브러리 버전
-  `21.6` ODA 2021년 배포판, 빌드 6

라이브러리 컴파일 작업
-----------------------

컴파일하기 전에 라이브러리들을 반드시 병합해야만 합니다.

.. code:: bash

   cd ~/dev/cpp/ODA21.6
   mkdir base_7.2
   tar xvzf Kernel_lnxX64_7.2dll_21.6.tar.gz -C base_7.2
   tar xvzf Drawings_lnxX64_7.2dll_21.6.tar.gz -C base_7.2

컴파일하려면 활성화 키(activation key)가 필수입니다. ODA 상품 활성화(ODA Products Activation)에서 활성화 키를 요청할 수 있습니다. ``ThirdParty/activation/`` 에 이 활성화 키를 복사해야만 합니다.

::

   cp OdActivationInfo base_7.2/ThirdParty/activation/

다음 명령어로 ODA 라이브러리들을 컴파일하십시오:

::

   cd base_7.2
   ./configure
   make -j8

사용자의 GCC 주 버전이 ODA 라이브러리 GCC 버전과 일치하는지 확인하십시오. 예를 들어 우분투 상에서는 서로 다른 GCC/G++ 버전들을, 그러니까 버전 7, 8, 그리고 9를 함께 설치할 수 있습니다. 다음 명령어로 사용할 버전을 선택하십시오:

::

   sudo update-alternatives --config gcc
   sudo update-alternatives --config g++

ODA 라이브러리 경로
------------------

ODA 라이브러리를 컴파일했다면, 라이브러리가 표준 검색 경로가 아닌 위치에 생성되었을 것입니다. 라이브러리를 표준 검색 경로 위치로 복사하도록 하는 ``make install`` 명령어가 없기 때문에 문제가 될 수도 있습니다.

GDAL/OGR를 ODA와 함께 컴파일하고 실행할 수 있는 서로 다른 대체 방법이 몇 가지 있습니다:

-  ODA 라이브러리를 표준 위치로 복사합니다.

-  LD_LIBRARY_PATH를 설정합니다. (예: `LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/jgr/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll`)

-  시스템 라이브러리 경로에 ODA 폴더를 추가합니다.

   ::

      echo "/home/jgr/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll" | sudo tee -a /etc/ld.so.conf.d/z_gdal-ODA.conf

-  GDAL을 컴파일할 때 런타임 경로(`rpath`)를 설정합니다. (예: `LDFLAGS="-Wl,-rpath=/home/jgr/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll"`)

ODA 라이브러리 이름
~~~~~~~~~~~~~~~~~

몇몇 ODA 라이브러리 이름은 일반적인 리눅스 표준 `lib*.so` 를 따르지 않습니다. 앞에 나열한 대체 방법들 가운데 `rpath` 를 사용하지 않는 방법을 사용하는 경우, 실제 이름으로부터 심볼릭 링크를 생성해야 할 수도 있습니다. 다음은 그 예시입니다:

::

   cd ~/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll
   for f in *.tx
   do
      echo "Processing $f"
      ln -s $f lib$f.so
   done
   sudo ldconfig

이제 모든 ODA 라이브러리를 볼 수 있는지 `ldconfig -v` 명령어로 확인하십시오.

GDAL 컴파일하기
--------------

ODA 라이브러리를 컴파일한 다음, 추가적인 두 방법으로 GDAL을 빌드할 수 있습니다:

-  `--with-teigha=/home/jgr/dev/cpp/ODA21.6/base_7.2`
-  `--with-teigha-plt=lnxX64_7.2dll`

`--with-teigha` 의 값은 ODA 라이브러리들을 병합하고 컴파일한 폴더의 전체 경로입니다.

`--with-teigha-plt` 의 값은 ODA가 사용하는 플랫폼 이름과 일치해야만 합니다. 이 플랫폼 이름은 `Platforms` 폴더 아래에 있는 폴더명입니다:

::

   ls -l Platforms/
   lnxX64_7.2dll

GDAL 컴파일 작업
----------------

사용자 자신의 GDAL 빌드 환경설정을 이용해서 앞에서 언급한 옵션들을 추가하십시오. `configure` 를 실행한 다음, 'Teigha(DWG 및 DGNv8)' 지원이 환경설정되었는지 확인하십시오.

예를 들면, GDAL을 다음과 같이 컴파일할 수도 있습니다:

::

   cd gdal
   ./autogen.sh
   ./configure --without-libtool LDFLAGS="-L/usr/lib/x86_64-linux-gnu" --with-python=python3 --with-proj=/usr/local --with-pg=yes --with-poppler --with-teigha=/home/jgr/dev/cpp/ODA21.6/base_7.2 --with-teigha-plt=lnxX64_7.2dll  
   make -j8
   sudo make install
   sudo ldconfig
   # Python support
   cd swig/python
   python3 setup.py build
   sudo python3 setup.py install   

ODA의 `libpcre`, `libcurl` 등등 대신 시스템 라이브러리를 사용하기 위해 `LDFLAGS="-L/usr/lib/x86_64-linux-gnu"` 를 추가했습니다.

테스트
-------

GDAL을 컴파일한 다음, 새 `DGNV8` 및 `DWG` 드라이버가 지원되는지 다음 명령어로 확인할 수 있습니다:

::

   ./apps/ogrinfo --formats | grep 'AutoCAD\|Microstation'
   DGN -vector- (rw+v): Microstation DGN
   DWG -vector- (ro): AutoCAD DWG
   DGNV8 -vector- (rw+): Microstation DGNv8
   DXF -vector- (rw+v): AutoCAD DXF
   CAD -raster,vector- (rovs): AutoCAD Driver

파일이 DGN 버전 8인 경우, 파일을 열 때 해당 드라이버가 실행되는 것을 볼 수 있을 것입니다:

::

   ogrinfo ~/dev/cpp/gdal/autotest/ogr/data/dgnv8/test_dgnv8.dgn
   INFO: Open of `/home/jgr/dev/cpp/gdal/autotest/ogr/data/dgnv8/test_dgnv8.dgn'
         using driver `DGNV8' successful.
   1: my_model

문제 해결
---------------

링크 오류가 발생하는 경우, ODA 라이브러리 위치로부터 ODA 라이브러리를 찾을 수 있도록 하기 위해 `LD_LIBRARY_PATH` 또는 `LDFLAGS` 환경 변수를 설정하면 됩니다.

`ldconfig -v` 명령어를 이용해서 ODA 라이브러리 폴더가 목록화되어 있는지 확인할 수 있습니다.

예를 들면 다음을 시도해볼 수 있습니다:

::

   export LD_LIBRARY_PATH=/home/jgr/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll
   ./configure --without-libtool LDFLAGS="-L/usr/lib/x86_64-linux-gnu" --with-python=python3 --with-proj=/usr/local --with-pg=yes --with-poppler --with-teigha=/home/jgr/dev/cpp/ODA21.6/base_7.2 --with-teigha-plt=lnxX64_7.2dll   

다음 명령어로 런타임 위치를 (`rpath` 로) 강제할 수 있습니다:

::

   ./configure --without-libtool LDFLAGS="-L/usr/lib/x86_64-linux-gnu -Wl,-rpath=/home/jgr/dev/cpp/ODA21.6/base_7.2/bin/lnxX64_7.2dll" --with-python=python3 --with-proj=/usr/local --with-pg=yes --with-poppler --with-teigha=/home/jgr/dev/cpp/ODA21.6/base_7.2 --with-teigha-plt=lnxX64_7.2dll   


사용자의 빌드 환경에 맞춰 이 설정들을 조정하십시오. 

참고
--------

-  `ODA 플랫폼 소개 <https://www.opendesign.com/products>`_

-  :ref:`오토캐드 DWG <vector.dwg>` 드라이버

-  :ref:`마이크로스테이션 DGN 버전 8 <vector.dgnv8>` 드라이버

