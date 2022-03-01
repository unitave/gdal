.. _faq:

================================================================================
FAQ
================================================================================

.. TODO maybe migrate the chapters 2 and following of https://trac.osgeo.org/gdal/wiki/FAQ

.. only:: not latex

    .. contents::
       :depth: 3
       :backlinks: none

GDAL은 어떤 뜻인가요?
+++++++++++++++++++++

GDAL - Geospatial Data Abstraction Library

누구는 (구글과 비슷한 발음의) "구-돌" 로 발음하고, 다른 이는 "지-돌" 이라 발음하며, "지-달" 이라 발음하는 이도 있습니다.

프랑크 바르메르담(Frank Warmerdam)이 GDAL을 어떻게 발음하는지 그리고 이 약어의 역사에 대해 `들어보세요 <https://soundcloud.com/danabauer/how-do-you-pronounce-gdal#t=00:02:58>`__.

이 OGR이란 게 뭐죠?
+++++++++++++++++++

OGR은 GDAL에서 분리되었던 OpenGIS 단순 피처(OpenGIS Simple Features)에 영감을 받은 개별 벡터 IO 라이브러리였습니다. GDAL 2.0 배포와 함께, GDAL과 OGR 구성요소들이 함께 통합되었습니다.

OGR은 어떤 뜻인가요?
++++++++++++++++++++

OGR은 OpenGIS 단순 피처 기준 구현(OpenGIS Simple Features Reference Implementation)의 약어였습니다. 하지만 OGR이 OpenGIS 단순 피처 사양을 완전히 준수하지 않고 해당 사양의 기준 구현으로 인정받지도 못 했기 때문에 그 이름도 OGR 단순 피처 라이브러리(OGR Simple Features Library)로 변경되었습니다. 이 이름에서 OGR의 의미는 그저 역사상의 뜻일 뿐입니다. OGR은 라이브러리의 소스에서 클래스 이름, 파일명 등등 모든 곳에 접두어로도 사용되고 있습니다.

CPL은 어떤 뜻인가요?
++++++++++++++++++++

공통 이식성 라이브러리(Common Portability Library)입니다. GDAL 내부의 크로스 플랫폼 표준 라이브러리로 생각하십시오. GDAL 개발 초기 시절, 크로스 플랫폼 개발은 물론 컴파일러의 호환성 및 표준 준수도 힘들었을 무렵 GDAL/OGR의 원활한 이식성을 위해 CPL이 필요했습니다.

CPL, 또는 CPL의 부분들이 GDAL 외부의 일부 (예:MITAB, libgeotiff) 프로젝트에 쓰이고 있습니다.

GDAL 프로젝트는 언제 시작됐나요?
++++++++++++++++++++++++++++++++

1998년 말, 프랑크 바르메르담이 독립 개발자로서 GDAL/OGR 라이브러리를 작업하기 시작했습니다.

GDAL/OGR은 독점 소프트웨어인가요?
+++++++++++++++++++++++++++++++++

아뇨, GDAL/OGR은 자유 오픈 소스 소프트웨어입니다.

GDAL/OGR이 사용하는 사용허가는 무엇인가요?
++++++++++++++++++++++++++++++++++++++++++

:ref:`license` 참조

GDAL-OGR이 실행되는 운영 체제는 무엇인가요?
+++++++++++++++++++++++++++++++++++++++++++

유닉스의 모든 현대 플레이버(리눅스, FreeBSD, 맥OS X), 마이크로 소프트 윈도우의 모든 지원 버전, 모바일 환경(안드로이드와 iOS)에서 GDAL/OGR을 사용할 수 있습니다. 32비트와 64비트 아키텍처를 모두 지원합니다.

GDAL/OGR에 그래픽 사용자 인터페이스가 있나요?
+++++++++++++++++++++++++++++++++++++++++++++

:ref:`software_using_gdal` 참조:

.. toctree::
   :hidden:

   software_using_gdal

GDAL/OGR을 빌드하려면 어떤 컴파일러를 써야 하나요?
++++++++++++++++++++++++++++++++++++++++++++++++++

GDAL/OGR은 C++11 호환 컴파일러로 컴파일할 수 있습니다.

이 페이지에는 답이 없는 질문이 있습니다. 어디에서 자세한 정보를 찾을 수 있을까요?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

:ref:`community` 참조

당신이 어떻게 질문하느냐에 따라 얻을 수 있는 답도 달라진다는 사실을 명심하십시오. 이 사실에 대한 설명을 더 자세히 알고 싶다면, 에릭 S. 레이몬드(Eric S. Raymond)가 쓴 `똑똑하게 질문하는 방법(How To Ask Questions The Smart Way) <http://www.catb.org/~esr/faqs/smart-questions.html>`_ 이라는 수필을 읽어보세요.

어떻게 새 포맷을 위한 지원을 추가할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++

이제 :ref:`raster_driver_tut` 및 :ref:`vector_driver_tut` 이 이에 대한 답을 어느 정도 다루고 있습니다.

어떻게 GDAL을 인용하나요?
+++++++++++++++++++++++++

`CITATION`_ 참조

.. _`CITATION`: https://github.com/OSGeo/gdal/blob/master/CITATION
