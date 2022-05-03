.. _csharp_conda:

================================================================================
C# 바인딩 conda 패키지
================================================================================

설치
----

C# 바인딩을 가진 GDAL과 샘플 프로그램들을 다음 명령어를 사용해서 불러올 수 있습니다:

.. code-block::

    conda install -c conda-forge gdal-csharp

.. note::

   맥과 리눅스 상에서도 이 명령어가 MONO를 불러올 것입니다.

사용례 - 윈도우
---------------

.. note::

   :program:`%CONDA_PREFIX%\\Library\\bin\\gcs\\gdal_test` 를 실행하면 conda 환경에서 C# 바인딩이 작동하는지를 테스트할 수 있습니다.

DLL 파일들을 :file:`%CONDA_PREFIX%\\Library\\bin` 폴더로 불러옵니다. conda 환경에서는 일반적인 습성입니다.

C# .EXE 파일들을 :file:`%CONDA_PREFIX%\\Library\\bin\\gcs` 폴더로 불러옵니다. 이렇게 하지 않으면 표준 GDAL 도구들을 덮어쓰기 때문입니다.

샘플 프로그램을 (예: :file:`GDALinfo.exe` 파일을) 실행하려면 PATH에 :file:`%CONDA_PREFIX%\\Library\\bin\\gcs` 를 추가한 다음 :program:`gdalinfo` 를 실행하기만 하면 됩니다.

사용자 코드에 DLL 파일들을 링크하려면, 프로젝트에 DLL 파일들을 포함시켜야 할 것입니다. (거의 대부분의 경우 프로젝트 디렉터리에 DLL을 복사해 넣는다는 의미입니다.)

conda 환경 안에서 실행되는 터미널 프로그램의 경우 (예: :program:`conda activate` 를 실행하는 경우) 컴파일이 완료되면 작동할 것입니다.

conda 환경에서 실행할 수 없는 GUI 응용 프로그램 또는 다른 프로그램의 경우 해당 프로그램이 GDAL DLL 파일들을 사용할 수 있도록 환경을 설정해야 할 것입니다.

사용례 - 맥/리눅스
------------------

.. note::

   :program:`mono $CONDA_PREFIX/lib/gdal_test.exe` 를 실행하면 conda 환경에서 C# 바인딩이 작동하는지를 테스트할 수 있습니다.

공유 오브젝트(예: :file:`\*.so` / :file:`\*.dylib`), .EXE, 그리고 .DLL 파일을 모두 (사용자가 예상했을 수도 있는 :file:`bin` 폴더가 아니라) :file:`$CONDA_PREFIX/lib` 폴더로 불러옵니다. `MMONO 문서 <https://www.mono-project.com/docs/getting-started/application-deployment/>`_ 에 따른 습성입니다.

샘플 프로그램 가운데 하나를 (예: :file:`GDALinfo.exe` 파일을) 실행하려면 :program:`mono $CONDA_PREFIX/lib/GDALinfo.exe` 를 실행하십시오.

MONO에서 터미널 프로그램을 빌드하려면, conda 환경에서 다음과 비슷한 명령어를 (소스 이름을 사용자 필요에 맞게 변경해서) 사용하면 됩니다:

.. code-block:: C#

    msc /r:gdal_csharp.dll /r:ogr_csharp.dll /r:osr_csharp.dll /r:System.Drawing.dll /out:gdal_test.exe gdal_test.cs

conda 환경에서 컴파일된 실행 파일을 실행하는 경우, 이렇게 하면 작동할 것입니다. 좀 더 이식성이 높은 또는 GUI 응용 프로그램의 경우, 사용자 스스로 의존성 문제를 해결해야 합니다.

.NET 프로젝트에서도 예를 들면 비주얼 스튜디오에서 빌드된 DLL 파일을 사용할 수 있습니다. 그냥 DLL 파일들을 의존성으로 링크하십시오.

conda 빌드의 차이점
-------------------

conda 빌드는 "표준" GDAL 빌드와 몇 가지 면에서 다릅니다:

-  맥 및 리눅스 상에서, 윈도우 버전의 지침에 따라 SWIG 파일을 :file:`\*_wrap` 으로 빌드합니다. 즉 :file:`.config` 파일이 존재하지 않는다는 의미입니다. 가장 중요한 차이점은, MONO는 물론 .NET 및 유니티 프로젝트에서도 DLL 파일들을 사용할 수 있다는 뜻입니다.
-  윈도우 상에서, 샘플 프로그램을 .NET CORE 2.1버전이 아니라 .NET5로 빌드합니다.

