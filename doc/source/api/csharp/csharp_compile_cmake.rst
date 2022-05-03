.. _csharp_compile_cmake:

================================================================================
C# 바인딩 컴파일 작업 - CMake 스크립트
================================================================================

이 페이지에서는 새 CMake 스크립트를 이용해서 소스로부터 GDAL/OGR C# 바이너리를 생성할 때의 주요 단계들을 설명합니다.

대부분의 경우 이럴 필요는 없고 `GisInternals <https://gisinternals.com/>`_ 또는 "conda" 같은 사전에 컴파일된 소스들 가운데 하나를 사용하는 편이 낫습니다.

바인딩을 전체 GDAL 빌드의 일부로 또는 기존 설치본 위에 독립형으로 빌드할 수 있습니다.

요구 사항
+++++++++

빌드 환경은 다음 의존성을 가집니다:

-  CMake 3.10 이상 버전
-  알맞은 C++ 빌드 환경 (예: gcc 또는 비주얼 스튜디오 등)
-  SWIG 4버전
-  .NET 5.0 또는 MONO

.NET 빌드 도구 체인
+++++++++++++++++++

빌드 스크립트는 .NET 5.0버전과 :file:`dotnet.exe` 또는 MONO와 :file:`msc.exe` 가운데 하나를 사용해서 바인딩을 컴파일할 수 있습니다.

모든 플랫폼 상에서 .NET이 있는 경우 .NET을 선호하지만 명령줄 변수를 이용해서 MONO를 강제로 사용할 수 있습니다.

GDAL 빌드의 일부로 빌드하기
+++++++++++++++++++++++++++

빌드 환경이 다음 변수들을 사용합니다:

.. list-table::
   :header-rows: 1

   * - 이름
     - 유형
     - 역할
   * - CSHARP_MONO
     - 불(boolean)
     - MONO 사용을 강제합니다.
   * - CSHARP_LIBRARY_VERSION
     - 문자열
     - 공유 라이브러리 용 .NET 버전을 설정합니다.
   * - CSHARP_APPLICATION_VERSION
     - 문자열
     - 샘플 프로그램 용 .NET 버전을 설정합니다.
   * - GDAL_CSHARP_ONLY
     - 불(boolean)
     - GDAL 바이너리 위에 독립형으로 빌드합니다.
   * - BUILD_CSHARP_BINDINGS
     - 불(boolean)
     - C# 바인딩을 빌드합니다. 기본값은 ON입니다.

.NET으로 빌드하기
-----------------

빌드 환경에 .NET 5.0버전이 설치되어 있고 GDAL이 빌드되어 있다면, 기본적으로 .NET을 이용해서 C# 바인딩을 빌드할 것입니다.

GDAL 빌드에 대한 상세 정보는 다른 곳에 문서화되어 있지만, GDAL 저장소의 루트 디렉터리에서 다음과 비슷한 명령어를 실행하면 됩니다:

.. code-block::

    cmake -DCMAKE_INSTALL_PREFIX ../install -B ../build -S .
    cmake --build ../build --config Release
    cmake --build ../build --config Release --target install

C# 바인딩 및 샘플 프로그램들은 설치 디렉터리에 (앞의 예시에서는 :file:`share/csharp` 하위 폴더 안에 있는 :file:`../install` 폴더일 것입니다) 설치됩니다. 이 디렉터리에 다음 파일들이 있을 것입니다:

-  :file:`gdal_csharp.dll`
-  :file:`ogr_csharp.dll`
-  :file:`osr_csharp.dll`
-  :file:`gdalconst_csharp.dll`
-  :file:`gdal_wrap.dll` 또는 :file:`libgdal_wrap.so` 또는 :file:`libgdal_wrap.dylib`
-  :file:`ogr_wrap.dll` 또는 :file:`libogr_wrap.so` 또는 :file:`libogr_wrap.dylib`
-  :file:`osr_wrap.dll` 또는 :file:`libosr_wrap.so` 또는 :file:`libosr_wrap.dylib`
-  :file:`osr_wrap.dll` 또는 :file:`libosr_wrap.so` 또는 :file:`libosr_wrap.dylib`
-  :file:`gdalconst_wrap.dll` 또는 :file:`libgdalconst_wrap.so` 또는 :file:`libgdalconst_wrap.dylib`
-  다양한 샘플 프로그램들:
   윈도우 상에서는 \*.exe 파일, 또는 유닉스 상에서는 그냥 \-  파일, 그리고 각 프로그램 및 런타임 환경설정 파일에 대한 \*.dll 파일

샘플 프로그램 각각에 대한 환경설정 파일을 담고 있는 하위 디렉터리들도 존재합니다.

다음 NuGET 패키지들도 있습니다:

-  :file:`OSGeo.GDAL`
-  :file:`OSGeo.OGR`
-  :file:`OSgeo.OSR`
-  :file:`OSGeo.GDAL.CONST`
-  다양한 샘플 프로그램들

.NET 바인딩 이용하기
--------------------

개발 환경에서 바인딩을 가장 쉽게 사용하는 방법은 생성된 NuGET 패키지를 사용하는 방법일 것입니다.

NuGET 패키지를 사용하려면 GDAL 설치 디렉터리를 가리키는 로컬 저장소를 추가해야 합니다. 
To do this you need to add a local repistory pointing to the GDAL install directory. `여기 <https://docs.microsoft.com/ko-kr/nuget/hosting-packages/local-feeds>`_ 에서 그 방법을 설명하고 있습니다.

로컬 저장소를 추가한 다음, 평소대로 사용자 프로젝트에 GDAL 패키지를 추가하십시오.

.. note:: 

   이 패키지는 바인딩만 설치할 뿐 GDAL 코어를 설치하지는 않습니다. 검색 경로에서 GDAL 바이너리를 사용할 수 있도록 확인하는 것은 개발자의 몫입니다.

.. note:: 

   NuGET 패키지는 빌드 시스템에 있는 GDAL 버전과 동일한 버전 번호로 생성됩니다.
   GIT 저장소에서 빌드하는 경우, 빌드 시스템이 버전을 "x.y.z-dev pre-release" 태그로 자동 생성할 것입니다.
   다시 말해 (예를 들어) 비주얼 스튜디오에 패키지를 불러오려면 "사전 배포판" 체크박스를 체크해야 한다는 뜻입니다.
   이 모든 것은 계획적인 것으로 버그가 아닙니다.

MONO 상에서 빌드하기
--------------------

빌드 환경에 .NET 5.0버전이 없거나, msbuild가 설치되어 있고 GDAL이 빌드되어 있는 경우, 기본적으로 MONO를 사용해서 C# 바인딩을 빌드할 것입니다. ``CSHARP_MONO`` 변수를 설정해서 MONO로 강제 빌드할 수도 있습니다.

GDAL 빌드에 대한 상세 정보는 다른 곳에 문서화되어 있지만, GDAL 저장소의 루트 디렉터리에서 다음과 비슷한 명령어를 실행하면 됩니다:

.. code-block::

    cmake -DCMAKE_INSTALL_PREFIX ../install -DCSHARP_MONO=ON -B ../build -S .
    cmake --build ../build --config Release
    cmake --build ../build --config Release --target install

C# 바인딩 및 샘플 프로그램들은 설치 디렉터리에 (앞의 예시에서는 :file:`share/csharp` 하위 폴더 안에 있는 :file:`../install` 폴더일 것입니다) 설치됩니다. 이 디렉터리에 다음 파일들이 있을 것입니다:

-  :file:`gdal_csharp.dll`
-  :file:`ogr_csharp.dll`
-  :file:`osr_csharp.dll`
-  :file:`gdalconst_csharp.dll`
-  :file:`gdal_wrap.dll` 또는 :file:`libgdal_wrap.so` 또는 :file:`libgdal_wrap.dylib`
-  :file:`ogr_wrap.dll` 또는 :file:`libogr_wrap.so` 또는 :file:`libogr_wrap.dylib`
-  :file:`osr_wrap.dll` 또는 :file:`libosr_wrap.so` 또는 :file:`libosr_wrap.dylib`
-  :file:`osr_wrap.dll` 또는 :file:`libosr_wrap.so` 또는 :file:`libosr_wrap.dylib`
-  :file:`gdalconst_wrap.dll` 또는 :file:`libgdalconst_wrap.so` 또는 :file:`libgdalconst_wrap.dylib`
-  다양한 샘플 프로그램들:
   모든 플랫폼 상에서 \*.exe 파일

MONO 바인딩 사용하기
--------------------

이렇게 생성한 바인딩은 MONO 프레임워크에서만 작동할 것이라는 사실을 기억하십시오.

사전 빌드된 실행 파일 가운데 하나를 실행하려면 다음과 같이 MONO로 실행하면 됩니다:

:program:`mono GDALInfo.exe`

관리 라이브러리(예: DLL 파일들) 및 비관리 라이브러리 둘 다 MONO에서 사용할 수 있어야만 합니다. `MONO 문서 <https://www.mono-project.com/docs/advanced/pinvoke/>`_ 에서 더 자세한 정보를 찾을 수 있습니다.

독립형 빌드하기
+++++++++++++++

예를 들면 conda 배포판처럼 'include' 파일들 및 라이브러리들을 포함하고 있는 기존 GDAL 구현 위에 .NET 또는 MONO 도구 체인(toolchain)을  둘 다 이용하는 바인딩을 빌드할 수 있습니다.

독립형으로 빌드하려면, ``GDAL_CSHARP_ONLY`` 플래그를 설정해서 Cmake를 실행해야만 하며, 다음 대상 가운데 하나만 빌드해야 합니다:

.. list-table::
   :header-rows: 0

   * - csharp_binding
     - 바인딩만 빌드합니다.
   * - csharp_samples
     - 바인딩과 샘플 프로그램을 빌드합니다.

.. note::

   독립형 실행 도중 설치 대상을 빌드하지 마십시오. 실패할 것입니다!

.. note::

   이 빌드에 대해 ``ctest`` 명령어를 혼자 실행하지 마십시오. 실패할 수 있습니다!
   그 대신 ``ctest -R "^csharp.*"`` 같은 명령어를 사용하십시오.

다음은 빌드 명령어 예시입니다:

.. code-block::

    cmake -DGDAL_CSHARP_ONLY=ON -B ../build -S .
    cmake --build ../build --config Release --target csharp_samples

이 빌드의 산출물은 앞에서 설명한 바이너리들과 동일하지만, 산출물이 `../build/swig/csharp` 및 몇몇 하위 폴더에 저장될 것입니다.

