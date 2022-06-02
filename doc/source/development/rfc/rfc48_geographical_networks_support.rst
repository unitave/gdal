.. _rfc-48:

=======================================================================================
RFC 48: 지리 네트워크 지원
=======================================================================================

Author: 미하일 구세프(Mikhail Gusev), 드미트리 바리시니코프(Dmitry Baryshnikov)

연락처: gusevmihs@gmail.com, polimax@mail.ru

상태: 승인, GDAL 2.1버전에 구현

개요
----

이 RFC는 GSoC(Google Summer of Code) 2014 프로젝트 "GDAL/OGR 지리 네트워크(Geography Network) 지원"의 결과물을 GDAL 라이브러리로 통합할 것을 제안합니다. GNM(Geographical Network Model)의 목적은 GDAL의 공간 데이터 상에 빌드된 네트워크를 생성하고, 관리하고, 분석할 수 있는 케이퍼빌리티를 제공하는 것입니다.

-  `GSoC 프로젝트 설명 <https://trac.osgeo.org/gdal/wiki/geography_network_support>`_

-  `트렁크의 모든 변경 사항이 있는 GDAL 포크 <https://github.com/MikhanGusev/gdal>`_

-  `GSoC 블로그 <https://gsoc2014gnm.blogspot.com/>`_

제안 및 설명
------------

GDAL(이전 OGR)이 공간 벡터 포맷에 대한 도구를 제공하는 것처럼 GDAL에는 한편으로 서로 다른 기존 네트워크 포맷들(pgRouting, OSRM, GraphHopper, SpatiaLite 네트워크 등등)에 추상화(abstraction)를 제공하는 도구가 필요하고, 다른 한편으로는 네트워크 기능이 전혀 없는 (Shapefile) 공간 포맷에 네트워크 기능을 제공하는 도구도 필요합니다.

GNM이라는 별도의 C++ 클래스 집합으로 이런 도구를 구현합니다. 이 가운데 추상 네트워크(:cpp:class:`GNMNetwork` 클래스) 그리고 "GDAL 네이티브(GDAL-native)" 네트워크 또는 일반 포맷 네트워크(:cpp:class:`GNMGenericNetwork` 클래스)를 표현하는 두 클래스가 중요합니다.
추상 네트워크는 사용자가 자신의 네트워크 데이터를 관리하기 위한 공통 인터페이스로 사용됩니다. 이때 더 많은 네트워크 포맷을 지원하기 위해, GDAL 드라이버 목록과 마찬가지로 기저 포맷 특화 클래스 목록도 언제든지 확장할 수 있습니다.
"GDAL 네이티브" 포맷은 추상 네트워크를 구현하고 GDAL이 이미 지원하는 공간 포맷들에 네트워크 기능을 제공하기 위해 사용됩니다. 이 포맷의 모든 네트워크 데이터는 공간 데이터셋에 있는 공간 데이터와 함께 특수 레이어 집합에 저장됩니다. (내부적으로 :cpp:class:`GDALDataset` 및 :cpp:class:`OGRLayer` 를 광범위하게 사용합니다.)

네트워크 작업 인터페이스가 하는 일은 다음을 포함합니다:

   -  네트워크 생성/제거
   -  공간 데이터 상에 네트워크 위상을 직접 또는 자동 생성
   -  공통 방법으로 산출되는 연결 읽어오기
   -  네트워크에 공간 레이어/피처 추가/제거
   -  네트워크의 비즈니스 로직(business logic) 정의 (예: 서로 다른 레이어 피처들과의 연결을 적용하거나 거부하는 방식)
   -  네트워크 분석 방법 여러 개

더 자세한 내용 및 이 클래스 집합이 내부적으로 작동하는 방식은 클래스 아키텍처 문서(:file:`gdal/gnm/gnm_arch.dox`)를 참조하십시오.

바인딩
------

:file:`gdal/gnm/gnm_api.h` 에서 C API 래퍼(wrapper) 함수들을 선언합니다. SWIG 인터페이스 파일에 모든 현재 파이썬 바인딩이 구현되어 있으며, 이 C 함수들을 사용합니다.

응용 프로그램 모음
------------------

GDAL 소스 트리에 GNM을 사용하는 다음 응용 프로그램 2개를 포함시킬 것을 제안합니다:

   -  gnmmanage:
      gdalmanage 유틸리티의 목적과 유사합니다. "GDAL 네이티브" 포맷의 네트워크를 관리 -- 네트워크 생성 및 제거, 위상 직접 또는 자동 작성 -- 합니다. (:cpp:class:`GNMNetwork` 가 :cpp:class:`GDALDataset` 으로부터 상속받기 때문에 gdalmanage를 :cpp:class:`GNMNetwork` 와 함께 사용할 수 있습니다.)

   -  gnmanalyse:
      GNM의 분석 케이퍼빌리티를 사용합니다. 현재 최단 경로(들) 분석 및 연결된 구성 요소 검색이 가능합니다.

더 자세한 내용은 해당 문서에 있는 이 응용 프로그램들의 설명을 참조하십시오.

구현
----

깃허브에 이 RFC를 구현한 `풀(pull) 요청 <https://github.com/OSGeo/gdal/pull/60>`_ 이 이미 존재합니다.

GDAL을 GNM 지원과 함께 빌드하기
-------------------------------

GNM 지원 빌드는 기본적으로 비활성화되어 있습니다. GNM 지원을 빌드하려면 환경설정에 "--with-gnm" 키를 추가하거나 :file:`nmake.opt` 에서 적절한 줄을 주석 해제해야 합니다.

테스트
------

자동 테스트 스위트의 gnm 테스트로 :cpp:class:`GNMNetwork` 의 모든 공개(public) 메소드를 테스트했습니다.
:cpp:class:`GNMGenericNetwork` 용 테스트를 몇 개 추가했습니다.
:file:`autotest/utilities` 에서 콘솔 응용 프로그램(gnmmanage 및 gnmanalyse)을 테스트했습니다.

모든 테스트는 일반 규칙 -- 테스트를 파이썬으로 작성하고 :file:`/autotest` 폴더에 저장할 것 -- 에 따라 구현되었습니다:

   -  GNM 기본 테스트:
      테스트 용 저용량 shapefile 몇 개를 이용해서 기본 "GDAL 네트워크(GDAL-network)" 기능을 테스트합니다.

   -  GNM 유틸리티 테스트:
      gnmmanage 및 gnmanalyse 유틸리티의 단순 테스트입니다. ogrinfo 테스트와 비슷합니다.

문서 구조
---------

모든 새 메소드와 GNM 클래스를 문서화했습니다. 필요한 경우 GDAL 문서를 업데이트합니다.

:file:`/gnm` 및 :file:`/apps` 디렉터리에 있는 다음 새 Doxyfile들은 "관련 페이지" 부분의 주 자동 생성 HTML에 자동으로 빌드됩니다. 모든 Doxyfile들은 OGR 문서와 비슷합니다:

   -  GNM 아키텍처:
      모든 C++ GNM 클래스의 목적 및 설명

   -  GNM 예제:
      C++ GNM 클래스 사용 방법 지침

   -  GNM 유틸리티:
      GNM 유틸리티 2개에 대한 참조

   -  gnmmanage:
      gnmmanage 유틸리티의 설명 및 사용례

   -  gnmanalyse:
      gnmanalyse 유틸리티의 설명 및 사용례

소스 코드 트리 구성
-------------------

-  *추가된 내용*:
   이 통합으로 헤더, 소스, make 및 doc 파일을 가진 새 폴더를 '추가'할 것입니다:

   -  :file:`gcore/gdal.h`: 새 GNM 드라이버 유형 추가

      -  :file:`gdal/gnm`: GNM의 주 폴더

   -  :file:`gdal/apps` 에 응용 프로그램의 소스 코드 및 문서 파일 추가

   -  :file:`autotest/gnm` 및 :file:`autotest/utilities` 에 파이썬 테스트 스크립트 추가

   -  :file:`autotest/gnm/data` 테스트 용 shapefile 2개 추가 (7KB 이하)

   -  :file:`gdal/swig/include` 에 SWIG 인터페이스 파일 추가

-  *수정된 내용*:
   기존 GDAL 파일의 '변경 사항'은 '사소할 것입니다':

   -  :file:`/gdal` 및 :file:`/gdal/apps` 에 있는 GNUMakefile, :file:`makefile.vc` 및 그 환경설정 수정

      -  :file:`/autotest/run_all.py` 에 gnm 테스트 추가

   -  :file:`/autotest/pymod/test_cli_utilities.py` 에 유틸리티 테스트 명령어 추가

      -  :file:`/autotest/utilities/test_gnmutils.py`

   -  :file:`/swig/python/setup.py` 및 :file:`setup.cfg` 에 gnm 모듈 추가

      -  :file:`/swig/java` 에 있는 GNUMakefile 및 :file:`makefile.vc` 수정

향후의 아이디어
---------------

향후 GNM이 유용하고 흥미로운 방식으로 확장될 수 있습니다:

-  더 많은 포맷 지원하기:
   향후 가장 먼저 구현되어야만 하는 중요한 사항입니다. GNM의 목적이 가능한 한 많은 네트워크 포맷과 작동하는 것이기 때문입니다. 이때 :cpp:class:`GNMGdalNetwork` 포맷 지원만 포함하지 않습니다. 예를 들어 다른 GDAL 공간 포맷과 작동하는지에 대한 테스트도 포함해야 합니다. (현재 shapefile과 PostGIS에 대해서만 테스트되었습니다.) 예를 들면:

   -  :cpp:class:`GNMPGRoutingNetwork` 포맷. pgRouting 테이블과 작동합니다. 다음은 몇 가지 아이디어입니다:

      -  :cpp:func:`OGRFeature::setField` 를 통해 "source" 및 "target" 열에 값에 따라 :cpp:func:`GNMPGRoutingNetwork::ConnectFeatures` 를 추가할 것입니다.
      -  :cpp:func:`GNMPGRoutingNetwork::AutoConnect` 가 내부적으로 ``pgr_createTopology`` 메소드를 호출할 것입니다.

   -  :cpp:class:`GNMSQLiteNetwork` 포맷. SpatiaLite VirtualNetwork 네트워크와 작동합니다. 다음은 몇 가지 아이디어입니다:

      -  "Roads_net_data" 테이블 및 대응하는 "NodeFrom" 및 "NodeTowrite" 열에 모든 네트워크 데이터를 작성합니다.

   -  :cpp:class:`GNMGMLNetwork` 포맷. GML 위상과 작동합니다. 다음은 몇 가지 아이디어입니다:

      -  `gml::TopoComplex <gml::TopoComplex>`_, `gml::Node <gml::Node>`_ 및 `gml::Edge <gml::Edge>`_ 에 네트워크 데이터를 직접 작성합니다.

-  "GDAL 네트워크"에서 위상 작성의 보다 효율적인 알고리즘:
   현재 알고리즘은 모든 네트워크 포맷의 기본값으로 구현되어 있으며 라인 및 포인트 레이어의 양에 상관없이 연결할 수 있지만 그렇게 효율적이지는 않습니다 -- 대용량 네트워크의 경우 너무 오래 연결하고 있기 때문입니다. :cpp:class:`GNMGenericNetwork` 가 더 효율적인 기본 알고리즘을 가질 수 있습니다.

-  "GDAL 네트워크"에 더 많은 규칙을 추가:
   예를 들면 다음을 서술하는 더 복잡한 문법을 도입할 수 있습니다:

   -  라인의 기하 길이로부터 추출한 비용
   -  피처의 제약 역할 전환
   -  더 복잡한 연결 규칙:
      연결할 수 있는 피처 개수 제한 및 더 복잡한 표현식 설정

-  응용 프로그램:
   GNM으로 빌드할 수 있는 가장 유용한 응용 프로그램 가운데 하나는 'network2network'일 것입니다. 이 유틸리티는 데이터셋의 네트워크와 공간 데이터를 한 포맷으로부터 다른 포맷으로 (예를 들어 pgRouting으로부터 오라클 Spatial 네트워크로) 변환합니다.

-  분석:
   서로 다른 경로 검색(routing)을 위해, 그리고 엔지니어링 목적으로도 서로 다른 도표(graph) 유형 및 이 유형들과 작동하는 일고리즘을 지원해야 합니다. 예를 들면:

   -  `Boost 라이브러리 <https://www.boost.org/>`_
   -  수축 계층(Contraction Hierarchies) 기술 (대용량 도표 용)

투표 이력
---------

-  유카 라흐코넨 +1
-  세케레시 터마시 +1
-  이벤 루올 +1

