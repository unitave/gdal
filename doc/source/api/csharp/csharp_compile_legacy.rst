.. _csharp_compile_legacy:

================================================================================
C# 바인딩 컴파일 작업 - 레거시 스크립트
================================================================================

이 페이지에서는 소스로부터 GDAL/OGR C# 바이너리를 생성할 때의 주요 단계들을 설명합니다.

대부분의 경우 이럴 필요는 없고 `GisInternals <https://gisinternals.com/>`_ 또는 "conda" 같은 사전에 컴파일된 소스들 가운데 하나를 사용하는 편이 낫습니다.

윈도우 빌드 작업
----------------

C# 인터페이스를 빌드하려면, GDAL 코어의 컴파일된 버전이 필요합니다. GDAL 코어를 직접 컴파일하거나 사전 빌드된 바이너리들 가운데 하나를 링크하면 됩니다. 예전에는 GDAL을 빌드하기 위해 사용하는 깃허브 저장소의 클론에서 다음을 실행해야 했고 환경을 생성하기 위한 단계들은 필요가 없었습니다.

요구 사항
+++++++++

빌드 환경은 다음 의존성을 가집니다:

-  nmake / 비주얼 스튜디오
-  SWIG 3/4

.. note::

   `GDAL 테스트 스크립트 <https://github.com/OSGeo/gdal/blob/master/.github/workflows/windows_build.yml>`_ 는 비주얼 스튜디오 2019(MSVC 1920버전)를 사용하기 때문에 동일한 버전을 사용하는 편이 좋습니다.

.. note::

   `SWIG <http://www.swig.org/>`_ 을 사용해서 API 바인딩을 빌드합니다. GDAL 테스트 스크립트는 3버전을 그리고 conda 빌드는 4버전을 사용합니다. 두 버전 모두 작동합니다.

빌드 환경
+++++++++

빌드 환경을 설정해야 합니다. 비주얼 스튜디오 2019를 사용하는 경우, 다음 명령어를 사용할 수도 있습니다:

:program:`VsDevCmd.bat -arch=x64`

.. note::

   :program:`VsDevCmd.bat` 명령어는 일반적으로 :file:`C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Enterprise\\Common7\\Tools` 또는 커뮤니티 에디션의 경로에서 찾을 수 있습니다.

제대로 된 ``vcvars*.bat`` 파일을 찾아서 실행하는 것이 귀찮다면 개발 환경 특화 명령 프롬프트를 이용해서 빌드 환경을 설정할 수도 있습니다. Win64 컴파일을 이용하는 경우 사용자 시스템에 설치된 x64 버전 명령 프롬프트를 활성화시켜야 한다는 사실을 기억하십시오.

.. note::

   로컬에서 GDAL을 컴파일하는 데 사용되지 않은 환경에서 실행하는 경우, 환경설정해줘야 할 변수가 여러 개 있습니다. conda ``gdal-feedstock`` 환경설정 `build.bat <https://github.com/conda-forge/gdal-feedstock/blob/master/recipe/set_bld_opts.bat>`_ 프로그램을 변수 설정 지침서로서 사용할 수 있습니다.

SWIG 인터페이스 코드 생성하기
+++++++++++++++++++++++++++++

첫 번째 단계는 SWIG 인터페이스 코드를 생성하는 것입니다. ``.dll`` 파일로 컴파일될 ``.cs`` 정의 집합을 생성할 것입니다.

인터페이스를 생성하려면 (``swig\csharp`` 디렉터리에서) 다음 명령어를 실행하십시오:

.. code-block::

    nmake /f makefile.vc interface`

.. note::

   nmake.opt 파일에 :file:`swig.exe` 파일의 실제 위치를 추가해줘야 합니다.

코드 컴파일하기
+++++++++++++++

인터페이스를 생성한 다음 (``swig\csharp`` 디렉터리에서) 다음 명령어로 코드를 컴파일할 수 있습니다:

.. code-block::

    nmake /f makefile.vc

컴파일이 성공했다면 다음 파일들이 생성되었을 것입니다:

-  :file:`gdal_csharp.dll`
-  :file:`ogr_csharp.dll`
-  :file:`osr_csharp.dll`
-  :file:`gdalconst_csharp.dll`
-  :file:`gdal_wrap.dll`
-  :file:`ogr_wrap.dll`
-  :file:`osr_wrap.dll`
-  :file:`gdalconst_wrap.dll`
-  다양한 샘플 프로그램들

:file:`\*_csharp.dll` 바이너리들이 인터페이스의 관리 부분입니다. 인터페이스의 클래스들을 사용하려면 이 바이너리 파일들을 가리키는 참조를 추가해야 합니다. 이 :file:`\*_csharp.dll` 파일들이 각각 대응하는 :file:`\*_wrap.dll` 파일들을 불러올 것입니다. :file:`\*_wrap.dll` 파일들은 GDAL 코어의 코드를 호스팅하고 있는, 인터페이스의 비관리 부분입니다.

컴파일 성공 여부 테스트하기
+++++++++++++++++++++++++++

컴파일된 바이너리를 테스트하려면 다음 명령어를 실행하면 됩니다:

.. code-block::

    nmake /f makefile.vc test`

이 명령어가 몇몇 샘플 프로그램을 호출할 것입니다.

.. note::

   이 테스트가 작동하려면 PATH에서 Proj 및 GDAL DLL을 사용할 수 있어야 합니다.

윈도우 상에서 MONO 사용하기
+++++++++++++++++++++++++++

윈도우 용 버전 MONO 패키지가 설치되어 있는 경우 MONO 컴파일러를 이용해서 C# 코드를 컴파일할 수 있습니다. 이 경우 csharp.opt 파일에서 다음 항목을 주석 해제하십시오:

:program:`MONO = YES` 

.. note::

   PATH에서 mcs.exe 파일을 사용할 수 있어야만 합니다.


리눅스/macOS 빌드 작업
----------------------

요구 사항
+++++++++

빌드 환경은 다음 의존성을 가집니다:

-  make
-  SWIG 3/4
-  MONO (아마도 모든 합당한 버전)

빌드 환경
+++++++++

빌드 환경을 정확하게 환경설정해야 합니다. 로컬에서 GDAL을 빌드하는 데 사용되지 않은 환경에서 실행하는 경우, GDAL 루트 디렉터리에서 :program:`configure` 명령어를 실행해야 합니다.

conda ``gdal-feedstock`` 환경설정 `build.sh <https://github.com/conda-forge/gdal-feedstock/blob/master/recipe/build.sh>`_ 프로그램을 환경설정 예시로서 사용할 수 있습니다.

SWIG 인터페이스 코드 생성하기
+++++++++++++++++++++++++++++

첫 번째 단계는 SWIG 인터페이스 코드를 생성하는 것입니다. ``.dll`` 파일로 컴파일될 ``.cs`` 정의 집합을 생성할 것입니다.

인터페이스를 생성하려면 (``swig/csharp`` 디렉터리에서) 다음 명령어를 실행하십시오:

.. code-block::

    make generate

.. warning::

   GDAL 3.3.0 미만 버전들에서는 이 명령어가 정확한 이름공간이 없는 부정확한 인터페이스를 생성할 것입니다. `#3670 <https://github.com/OSGeo/gdal/pull/3670/commits/777c9d0e86602740199cf9a4ab44e040c52c2283>`_ 을 참조하십시오.

코드 컴파일하기
+++++++++++++++

인터페이스를 생성한 다음 (``swig/csharp`` 디렉터리에서) 다음 명령어로 코드를 컴파일할 수 있습니다:

.. code-block::

    make

컴파일이 성공했다면 다음 파일들이 생성되었을 것입니다:

-  :file:`gdal_csharp.dll` 및 :file:`gdal_csharp.dll.config`
-  :file:`ogr_csharp.dll` 및 :file:`ogr_csharp.dll.config`
-  :file:`osr_csharp.dll` 및 :file:`osr_csharp.dll.config`
-  :file:`gdalconst_csharp.dll` 및 :file:`gdalconst_csharp.dll.config`
-  :file:`libgdalcsharp.so / .dylib` 등
-  :file:`libogrcsharp.so / .dylib` 등
-  :file:`libosrcsharp.so / .dylib` 등
-  :file:`libgdalconst_wrap.so / .dylib` 등
-  다양한 샘플 프로그램들 (:file:`\*.exe`)

:file:`\*_csharp.dll` 바이너리들이 인터페이스의 관리 부분입니다. 인터페이스의 클래스들을 사용하려면 이 바이너리 파일들을 가리키는 참조를 추가해야 합니다.

이 :file:`\*_csharp.dll` 파일들이 각각 대응하는 :file:`\*_wrap.dll` 파일들을 불러오려 시도할 것이며, :file:`libxxxcsharp.\*` 라이브러리로 리다이렉트시킵니다. :file:`libxxxcsharp.\*` 라이브러리는 :file:`\*.dll.config` 정의에 따라 GDAL 코어의 코드를 호스팅하고 있는, 인터페이스의 비관리 부분입니다.

컴파일 성공 여부 테스트하기
+++++++++++++++++++++++++++

컴파일된 바이너리를 테스트하려면 다음 명령어를 실행하면 됩니다:

.. code-block::

    nmake test

이 명령어가 몇몇 샘플 프로그램을 호출할 것입니다.

.. note::

   이 테스트가 작동하려면 PATH에서 Proj 및 GDAL 라이브러리를 사용할 수 있어야 합니다.

유닉스 상에서 바인딩 사용하기
+++++++++++++++++++++++++++++

현재 이렇게 생성한 바인딩은 MONO 프레임워크에서만 작동할 것이라는 사실을 기억하십시오.

사전 빌드된 실행 파일 가운데 하나를 실행하려면 다음과 같이 MONO로 실행하면 됩니다:

:program:`mono GDALInfo.exe`

관리 라이브러리(예: DLL 파일들) 및 비관리 라이브러리 둘 다 MONO에서 사용할 수 있어야만 합니다. `MONO 문서 <https://www.mono-project.com/docs/advanced/pinvoke/>`_ 에서 더 자세한 정보를 찾을 수 있습니다.

.. note::

   이 문서는 `https://trac.osgeo.org/gdal/wiki/GdalOgrCsharpCompile <https://trac.osgeo.org/gdal/wiki/GdalOgrCsharpCompile>`_ 에 있는 이전 버전을 수정한 것입니다.

