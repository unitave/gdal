.. _csharp_conda:

================================================================================
C# 바인딩 콘다 패키지
================================================================================

GDAL C# 바인딩 콘다(Conda) 패키지는 커뮤니티 지원 프로젝트입니다.

설치
----

C# 바인딩을 가진 GDAL과 샘플 프로그램들을 다음 명령어를 사용해서 불러올 수 있습니다:

.. code-block::

    conda install -c conda-forge gdal-csharp

사용례
------

GDAL 3.5.0 이상 버전 용 콘다 패키지는 CMake 빌드 스크립트를 사용하기 때문에 빌드 과정 및 생성물이 변경되었습니다.

    :ref:`csharp_conda_35`

    :ref:`csharp_conda_34`

.. _csharp_conda_35:

GDAL 3.5.0 이상 버전
--------------------

GDAL 3.5.0 이상 버전 용 콘다 패키지는 새로운 CMake 빌드 스크립트를 사용해서 빌드됩니다.

.NET 대상 프레임워크
++++++++++++++++++++

모든 아키텍처 (예: 윈도우, 리눅스 및 맥) 상에서, 현재 (문서 작성 당시) LTS 버전과 마찬가지로 .NET6.0을 이용해서 바인딩을 컴파일합니다.

패키지 산출물
+++++++++++++

콘다 패키지는 다음 두 가지 생성물을 담고 있습니다:

* SWIG 래퍼(wrapper) DSO(Dynamic Shared Objects):
  :file:`gdal_wrap.dll` 또는 :file:`libgdal_wrap.so` 또는 :file:`libgdal_wrap.dylib` 등등입니다.
  콘다 패키지에 기대하는 대로 (예를 들면 윈도우에서는 :file:`bin` 폴더로 그리고 유닉스에서는 :file:`lib` 폴더로) 이들을 불러오기 때문에 정확한 버전의 GDAL DSO에 자동적으로 링크할 것입니다.

* 실제 C# 바인딩 용 로컬 NuGet 패키지:
  실제 C# 바인딩의 예를 들자면 :file:`gdal_csharp.dll`, :file:`gdalconst_csharp.dll`, :file:`osr_csharp.dll` 및 :file:`ogr_csharp.dll` 이 있습니다. 이들을 :file:`OSGeo.GDAL`, :file:`OSGeo.OSR` 및 :file:`OSGeo.OGR` 라는 패키지로 생성하고 :file:`share/gdal` 폴더로 불러옵니다.

사용례
++++++

사용자 응용 프로그램에서 바인딩을 사용하려면 기본적으로 다음을 수행해야 할 것입니다:

#. 사용자 응용 프로그램에 관련 패키지를 로컬 패키지로 추가하고
#. 응용 프로그램의 검색 경로에 DSO를 추가합니다.

전자는 복잡하지 않으며 로컬 소스를 (`여기에서 설명하는 대로 <https://docs.microsoft.com/en-us/nuget/hosting-packages/local-feeds>`_) 전체 수준에서 또는 다음 단락에서 볼 수 있는 대로 빌드 명령어 안에 정의하면 됩니다.

후자는 다음 단락에서 볼 수 있는 대로 콘솔 응용 프로그램 용 콘다를 기반으로 할 수 있지만, (콘다에 관해서는 아무것도 모르는 .NET IDE인) IDE에서 작업하는 경우 그리고/또는 (콘다 환경에서 실행되지 않을) GUI 응용 프로그램에서 작업하는 경우 직접 DSO를 선별해야 할 것입니다. 관련 DSO를 응용 프로그램 패키지로 복사해야 할 수도 있습니다.

사용 예시 - 윈도우
++++++++++++++++++

가장 간단한 예시는 다음과 같을 것입니다:

1. 새 응용 프로그램 생성 (비어 있는 전용 폴더 안에)

:program:`dotnet new console`

2. 간단한 응용 프로그램 생성 (:file:`Program.cs` 의 내용을 대체해서)

.. code-block:: c#

    using System;
    using OSGeo.GDAL;

    namespace testapp
    {
        class GdalTest
        {
            static void Main(string[] args)
            {
                Console.WriteLine("Testing GDAL C# Bindings");
                Gdal.UseExceptions();
                Console.WriteLine($"Gdal version {Gdal.VersionInfo(null)}");
            }
        }
    }

3. GDAL 패키지 추가

:program:`dotnet add package OSGeo.GDAL -s %CONDA_PREFIX%\\Library\\share\\gdal`

4. 컴파일 또는 실행

:program:`dotnet run`

("gdal-csharp" 패키지를 담고 있는) 콘다 환경에서 이 명령어들을 실행한다면 그냥 작동할 것입니다.

사용 예시 - 유닉스
++++++++++++++++++

1. 새 응용 프로그램 생성 (비어 있는 전용 폴더 안에)

:program:`dotnet new console`

2. 간단한 응용 프로그램 생성 (:file:`Program.cs` 의 내용을 대체해서)

.. code-block:: c#

    using System;
    using OSGeo.GDAL;

    namespace testapp
    {
        class GdalTest
        {
            static void Main(string[] args)
            {
                Console.WriteLine("Testing GDAL C# Bindings");
                Gdal.UseExceptions();
                Console.WriteLine($"Gdal version {Gdal.VersionInfo(null)}");
            }
        }
    }

3. GDAL 패키지 추가

:program:`dotnet add package OSGeo.GDAL -s $CONDA_PREFIX/share/gdal`

4. 컴파일 또는 실행

:program:`dotnet run`

.. warning:: 

   윈도우와는 다르게 라이브러리 검색 경로가 프로세스 검색 경로와 분리되어 있고 콘다가 설정하지 않기 때문에 유닉스에서는 그냥 작동하지 않을 것입니다.

   작동하게 하려면 라이브러리 검색 경로를 변경해야 할 수도 있을 것입니다. 개발 중에는 경로를 변경해도 괜찮지만 상품에 대해 허용해서는 안 됩니다. (다시 말해 응용 프로그램 검색 경로에 DSO를 복사해야 할 것이라는 뜻입니다.)

   리눅스 에서는:

   :program:`export LD_LIBRARY_PATH=$CONDA_PREFIX/lib`

   macOS에서는:

   :program:`export DYLD_LIBRARY_PATH=$CONDA_PREFIX/lib`

.. _csharp_conda_34:

GDAL 3.4.x 이전 버전
--------------------

윈도우
++++++

.. note::

   :program:`%CONDA_PREFIX%\\Library\\bin\\gcs\\gdal_test` 를 실행하면 콘다 환경에서 C# 바인딩이 작동하는지를 테스트할 수 있습니다.

DLL 파일들을 :file:`%CONDA_PREFIX%\\Library\\bin` 폴더로 불러옵니다. 콘다 환경에서는 일반적인 습성입니다.

C# .EXE 파일들을 :file:`%CONDA_PREFIX%\\Library\\bin\\gcs` 폴더로 불러옵니다. 이렇게 하지 않으면 표준 GDAL 도구들을 덮어쓰기 때문입니다.

샘플 프로그램을 (예: :file:`GDALinfo.exe` 파일을) 실행하려면 PATH에 :file:`%CONDA_PREFIX%\\Library\\bin\\gcs` 를 추가한 다음 :program:`gdalinfo` 를 실행하기만 하면 됩니다.

사용자 코드에 DLL 파일들을 링크하려면, 프로젝트에 DLL 파일들을 포함시켜야 할 것입니다. (거의 대부분의 경우 프로젝트 디렉터리에 DLL을 복사해 넣는다는 의미입니다.)

콘다 환경 안에서 실행되는 터미널 프로그램의 경우 (예: :program:`conda activate` 를 실행하는 경우) 컴파일이 완료되면 작동할 것입니다.

콘다 환경에서 실행할 수 없는 GUI 응용 프로그램 또는 다른 프로그램의 경우 해당 프로그램이 GDAL DLL 파일들을 사용할 수 있도록 환경을 설정해야 할 것입니다.

맥/리눅스
+++++++++

.. note::

   :program:`mono $CONDA_PREFIX/lib/gdal_test.exe` 를 실행하면 콘다 환경에서 C# 바인딩이 작동하는지를 테스트할 수 있습니다.

공유 오브젝트(예: :file:`\*.so` / :file:`\*.dylib`), .EXE, 그리고 .DLL 파일을 모두 (사용자가 예상했을 수도 있는 :file:`bin` 폴더가 아니라) :file:`$CONDA_PREFIX/lib` 폴더로 불러옵니다. `MMONO 문서 <https://www.mono-project.com/docs/getting-started/application-deployment/>`_ 에 따른 습성입니다.

샘플 프로그램 가운데 하나를 (예: :file:`GDALinfo.exe` 파일을) 실행하려면 :program:`mono $CONDA_PREFIX/lib/GDALinfo.exe` 를 실행하십시오.

MONO에서 터미널 프로그램을 빌드하려면, 콘다 환경에서 다음과 비슷한 명령어를 (소스 이름을 사용자 필요에 맞게 변경해서) 사용하면 됩니다:

.. code-block:: C#

    msc /r:gdal_csharp.dll /r:ogr_csharp.dll /r:osr_csharp.dll /r:System.Drawing.dll /out:gdal_test.exe gdal_test.cs

콘다 환경에서 컴파일된 실행 파일을 실행하는 경우, 이렇게 하면 작동할 것입니다. 좀 더 이식성이 높은 또는 GUI 응용 프로그램의 경우, 사용자 스스로 의존성 문제를 해결해야 합니다.

.NET 프로젝트에서도 예를 들면 비주얼 스튜디오에서 빌드된 DLL 파일을 사용할 수 있습니다. 그냥 DLL 파일들을 의존성으로 링크하십시오.

콘다 빌드의 차이점
+++++++++++++++++++

콘다 빌드는 "표준" GDAL 3.4.x 빌드와 몇 가지 면에서 다릅니다:

-  맥 및 리눅스 상에서, 윈도우 버전의 지침에 따라 SWIG 파일을 :file:`\*_wrap` 으로 빌드합니다. 즉 :file:`.config` 파일이 존재하지 않는다는 의미입니다. 가장 중요한 차이점은, MONO는 물론 .NET 및 유니티 프로젝트에서도 DLL 파일들을 사용할 수 있다는 뜻입니다.
-  윈도우 상에서, 샘플 프로그램을 .NET CORE 2.1버전이 아니라 .NET5로 빌드합니다.

이런 변경 사항들은 GDAL 3.5.x버전에 대한 표준 빌드를 대비하기 위한 것입니다.

