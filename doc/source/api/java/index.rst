.. _java:

================================================================================
자바 바인딩
================================================================================

GDAL 프로젝트는 SWIG이 생성한 GDAL 및 OGR 용 자바 바인딩을 가지고 있습니다.

일반적으로, 클래스 및 메소드 대부분은 GDAL과 OGR의 대응하는 C++ 클래스와 일치합니다. GDAL 1.7.0 이상 배포판들을 위한 자바 바인딩의 API `​Javadoc <https://gdal.org/java/>`_ 을 찾을 수 있습니다.

자바 가비지 수거기가 주 스레드와는 다른 개별 스레드에서 동작하기 때문에, 자바 스레드 여러 개에서 GDAL API를 사용하는 경우가 아니더라도 GDAL이 멀티스레딩을 지원하도록 환경설정해줘야 합니다.

자바 바인딩을 빌드하기 위해 요구되는 자바 최저 버전은 자바 7입니다.

아파치 메이븐 사용자
--------------------

`메이븐 센트럴(Maven Central) <https://search.maven.org/>`_ 저장소에서 자바 바인딩을 찾을 수 있습니다. 해야 할 일은 의존성을 선언하는 것뿐입니다:

.. code-block:: xml

   <dependency>
      <groupId>org.gdal</groupId>
      <artifactId>gdal</artifactId>
      <version>1.11.2</version>
   </dependency>

유용한 링크
-----------

-  GDAL 1.7.0 이상 배포판들을 위한 자바 바인딩의 API `​Javadoc <https://gdal.org/java/>`_

-  `gdalinfo.java <https://github.com/OSGeo/gdal/tree/master/swig/java/apps/gdalinfo.java>`_:
   gdalinfo 유틸리티와 유사한 샘플 자바 프로그램입니다. (GDAL 1.7.0dev 버전의 자바 바인딩의 API를 사용합니다.)

-  `모든 자바 샘플 프로그램 <https://github.com/OSGeo/gdal/tree/master/swig/java/apps/>`_

-  `세케레시 터마시(Szekeres Tamás)의 윈도우 일일 빌드 <http://www.gisinternals.com/sdk>`_:
   세케레시 터마시가 GDAL 자바 바인딩을 포함하는 (VC2003/VC2005/VC2008/VC2010로 컴파일한) Win32 및 Win64 바이너리 패키지의 완전한 모음을 유지/관리합니다. 이 패키지들은 매일 GDAL SVN으로부터 최신 안정 버전 및 개발 버전 브랜치를 기반으로 빌드됩니다. "\*-devel" 패키지는 (문서 작성 당시 1.9.0dev) 개발 버전 기반이고 "\*-stable" 패키지는 최신 (문서 작성 당시 1.8버전) 안정 브랜치 기반입니다.

-  `Image I/O-Ext <https://imageio-ext.dev.java.net/>`_:
   이 프로젝트의 주요 핵심 모듈은 'gdalframework'로, 데이터 포맷 집합의 도달 범위에 대한 지원을 제공하기 위해 SWIG이 생성한 자바 바인딩을 통해 GDAL을 활용하는 프레임워크입니다. (**주의**: 이 프레임워크가 반드시 최신 배포된 GDAL 버전을 담고 있지는 않습니다.)

-  `GdalOgrInJavaBuildInstructions <https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructions>`_:
   **윈도우** 상에서 처음부터 GDAL 자바 바인딩을 빌드하기 위한 완전한 지침입니다.

-  `GdalOgrInJavaBuildInstructionsUnix <https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix>`_:
   유닉스/리눅스(?)/MinGW 상에서 GDAL 자바 바인딩을 빌드하기 위한 지침입니다.

