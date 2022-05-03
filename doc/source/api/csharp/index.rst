.. _csharp:

================================================================================
C# 바인딩
================================================================================

GDAL 프로젝트가 (예전에는 세케레시 터마시(Szekeres Tamás)가) SWIG(Simplified Wrapper and Interface Generator)이 생성한 GDAL 및 OGR 용 C# 바인딩을 유지/관리합니다.

일반적으로, 클래스 및 메소드 대부분은 GDAL과 OGR의 대응하는 C++ 클래스와 일치하지만, 현재 이 웹사이트 이외의 C# 특화 문서는 존재하지 않습니다.

VB.Net 같은 다른 .NET 언어들에서도 C# 바인딩을 사용할 수 있습니다.

C# 인터페이스는 다른 (파이썬, 자바 같은) SWIG 생성 래퍼(wrapper)들과 동일한 라이브러리를 대상으로 빌드되었습니다. 따라서 클래스 이름, 클래스 멤버 이름, 그리고 메소드 서명이 관습적인 .NET 명명 지침을 따르지 않고 GDAL+SWIG 규범을 준수할 수도 있습니다. 하지만 GDAL/OGR API 문서에서 일치하는 문서를 쉽게 식별할 수 있을 것입니다.

GDAL/OGR C# 클래스는 관리 및 비관리 코드 사이의 통신에 .NET P/Invoke 메커니즘을 사용합니다. 모든 클래스가 IDisposable 인터페이스를 구현해서 모든 래퍼 클래스가 참조하는 기저 비관리 메모리의 마무리(finalization)를 제어합니다.

지원 플랫폼
-------------------

현재 다음 플랫폼 상에서 인터페이스를 컴파일하고 지원할 수 있습니다:

-  Microsoft.NET 및 MONO 프레임워크를 대상으로 하는 다양한 Win32 및 Win64 플랫폼들
-  MONO 프레임워크를 사용하는 GNU 리눅스/macOS 시스템
-  윈도우, macOS 및 리눅스 상의 유니티(Unity) 시스템 (현재 MONO 프레임워크만 지원, IL2CPP는 지원하지 않음)

C# 용 GDAL 가져오기
-------------------

다음을 포함하지만 이에 국한되지 않는 여러 가지 방법으로 C# 바인딩을 가져올 수 있습니다:

-  `gisinternals <http://www.gisinternals.com/sdk>`_ 사이트, "윈도우 빌드 SDK" 단락 참조
-  `conda 패키지 <https://anaconda.org/conda-forge/gdal-csharp>`_, 아래 지침 참조
-  gdal.netcore NuGet 패키지, 아래 링크 참조
-  유니티의 경우, `GDAL을 설치하는 UPM 패키지 <https://openupm.com/packages/com.virgis.gdal/?subPage=readme>`_ (윈도우, 맥, 리눅스 상에서 사용할 수 있습니다)

(이 모든 방법 각각에 커뮤니티 지원이 존재합니다.)

관련 문서
-----------------
   .. toctree::
       :maxdepth: 1

       csharp_compile_legacy
       csharp_compile_cmake
       csharp_raster
       csharp_vector
       csharp_usage
       csharp_conda

유용한 링크
------------

-  GDAL 프로젝트 트리의 `/swig/csharp/apps <https://github.com/OSGeo/gdal/tree/master/swig/csharp/apps>`_ 폴더에서 다양한 C# 예시 프로그램들을 찾아볼 수 있습니다.

-  `conda Feedstock <https://github.com/conda-forge/conda-feedstock>`_

-  `MaxRev-Dev/gdal.netcore <https://github.com/MaxRev-Dev/gdal.netcore>`_ 는 .NET 코어 용 GDAL 3.2버전 라이브러리의 (문자 그대로) 단순한 빌드 엔진입니다.

-  `ViRGiS 프로젝트 <https://www.virgis.org/>`_ 은 유니티 환경에서 C#으로 된 GDAL을 광범위하게 사용합니다.

(이 단락에 사용자의 프로젝트를 추가해주십시오.)

윈도우 빌드 SDK
------------------

세케레시 터마시가 윈도우 상에서 소스로부터 GDAL을 컴파일하기 위한 `빌드 SDK 패키지 <http://www.gisinternals.com/sdk>`_ 를 유지/관리합니다. 이 빌드 시스템은 매일 최신 안정 버전 및 개발 버전 용 빌드 바이너리 패키지를 업데이트합니다.

