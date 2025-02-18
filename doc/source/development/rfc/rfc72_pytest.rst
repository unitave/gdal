.. _rfc-72:

=======================================================
RFC 72: pytest를 사용하도록 자동 테스트 스위트 업데이트
=======================================================

======= ====================================
저자:   크레이그 데 슈틱터(Craig de Stigter)
연락처: craig.destigter@koordinates.com
제안일: 2018년 9월 27일
상태:   승인, GDAL 2.4버전에 구현
======= ====================================

요약
----

이 RFC는 기존 파이썬 자동 테스트 스위트가 `pytest 프레임워크 <https://docs.pytest.org/en/latest/>`_ 를 사용하도록 변환할 것을 제안하고 설명합니다.

pytest를 사용하면 현재 자체 개발한 접근법과 비교할 때 파이썬 테스트의 작성, 읽기 및 디버깅에 대해 상당한 생산성 향상을 기대할 수 있습니다.

동기
----

현재의 자동 테스트 프레임워크는 (최소한) 2007년까지 거슬러 올라가며, 상당히 포괄적이긴 하지만 (그리고 파이썬 코드가 186,000줄이기 때문에) 개발자가 사용하고 확장하는 데 어려움이 있습니다.

-  자체 개발 프레임워크로서, GDAL 개발자들이 들인 노력보다 더 좋아질 수는 없습니다. 예시: 리포트, 테스트 범위, 병렬화, 속행(resumption), 로그/산출물 처리, 파라미터화 등등.

-  테스트 실패는 일반적으로 "실패" 정도로만 설명되며 원인을 확인하려면 테스트를 편집해야 합니다.

-  개별 테스트를 실행/재실행하기 어렵습니다.

-  테스트가 로컬 빌드에 무결하지 않을 수도 있는 컴파일 옵션 집합을 가정하는 경우가 많습니다.

-  테스트 트리 외부에 있는 스크립트는 다양한 지속적 통합(Continuous Integration; CI) 환경에서 테스트를 패치하거나 비활성화시키는데, 로컬에서 작업하는 개발자가 이런 내용을 알 수 없습니다.

-  일부 테스트들은 서로에게 그리고 특정 실행 순서에 의존하는데, 이런 테스트를 디버깅 및 확장하기 어렵습니다.

-  테스트 및 모듈 전반에 걸쳐 공유 기능이 반복됩니다.

-  일반적으로 새로운 기능에 대해서만 테스트를 작성할 뿐 재귀적으로 적용되지 않습니다.
   (대략적으로 작년 한 해에 이루어진 커밋 2,663개 가운데 자동 테스트 트리 관련은 725개뿐이었습니다.)

널리 사용되는 OSS(Open Source Software) 테스트 프레임워크를 채택하면 GDAL이 OSS 생태계를 활용해서 앞으로의 이점 및 개선 사항을 사용할 수 있게 할 수 있습니다. GDAL에서 자동화된 테스트의 활용성은 증명되었기 때문에, 가능한 한 테스트 작성을 쉽게 만들어야 할 필요가 있습니다.

제안
----

기존 파이썬 자동 테스트 스위트가 `pytest 프레임워크 <https://docs.pytest.org/en/latest/>`_ 를 사용하도록 포팅합니다. 어째서 pytest일까요? pytest가 널리 쓰이고, 광범위한 기능을 지원하며, 플러그인을 통해 확장 가능하고, 가능한 한 테스트 작성 및 디버깅을 -- 상투적인(boilerplate) 코드를 최소화하고 코드를 최대한 재활용해서 -- 쉽게 할 수 있게 하는 데 집중하기 때문입니다. `이 프레젠테이션 <http://thesoftjaguar.com/pres_pytest.html>`_ 이 (2014년 발표 자료이지만) pytest의 주요 이점을 간단히 소개해줍니다.

자동 테스트 스위트가 선호하는 pytest 접근법과 일치하도록 자동화된 코드 리팩토링(refactoring) 도구를 사용해서 이 포팅 작업의 대부분을 수행합니다. pytest가 모든 종류의 사용자 지정 테스트 모음 및 실행 메소드를 지원하긴 하지만, 개발자에게 앞으로의 이점을 더 많이 제공하려면 제대로 변환해야 합니다. 초기 목표는 기존 CI를 녹색으로 유지하면서 테스트들을 포팅하고 상투적인 코드를 가능한 한 많이 제거하는 것입니다. 향후 목표는 계속 상투적인 코드를 줄여가면서 각 테스트의 독립성을 높이는 것입니다.

그래도 최소한 다음 기존 기능들을 보전해야 할 것입니다:

-  기존 환경설정을 사용해서 모든 환경에서 모든 기존 CI 테스트를 실행할 수 있어야 합니다.

-  개별 테스트 모듈을 실행할 수 있어야 합니다.

-  기존 서브프로세스(subprocess)/멀티프로세스(multiprocess) 테스트를 지원해야 합니다.

-  파이썬 2.7 및 3버전에서 테스트할 수 있도록 지원해야 합니다.

-  `표명(assertion) <https://ko.wikipedia.org/wiki/%ED%91%9C%EB%AA%85>`_ 실패에 대한 `스택 추적(stack trace) <https://ko.wikipedia.org/wiki/%EC%8A%A4%ED%83%9D_%EC%B6%94%EC%A0%81>`_

새로운 테스트 스위트는 2018년 12월에 배포되는 GDAL 2.4.0버전에 포함될 것입니다. 이 변경 사항은 GDAL 2.3.x 이전 배포판 브랜치들로 하위 포팅되지 않을 것입니다.

참조
~~~~

-  `#949 이슈 <https://github.com/OSGeo/gdal/issues/949>`_
-  `gdal-dev 메일링 리스트 포스팅 <https://lists.osgeo.org/pipermail/gdal-dev/2018-October/049081.html>`_, 2018년 10월

예시
~~~~

일반적인 기존 GDAL 파이썬 단위 테스트의 예시가:

::

   def test_gdaladdo_1():
       if test_cli_utilities.get_gdaladdo_path() is None:
           return 'skip'

       shutil.copy('../gcore/data/mfloat32.vrt', 'tmp/mfloat32.vrt')
       shutil.copy('../gcore/data/float32.tif', 'tmp/float32.tif')

       (_, err) = gdaltest.runexternal_out_and_err(test_cli_utilities.get_gdaladdo_path() + ' tmp/mfloat32.vrt 2 4')
       if not (err is None or err == ''):
           gdaltest.post_reason('got error/warning')
           print(err)
           return 'fail'

       ds = gdal.Open('tmp/mfloat32.vrt')
       ret = tiff_ovr.tiff_ovr_check(ds)
       ds = None

       os.remove('tmp/mfloat32.vrt')
       os.remove('tmp/mfloat32.vrt.ovr')
       os.remove('tmp/float32.tif')

       return ret

'결국에는' 다음처럼 바뀔 수 있습니다:

::

   @pytest.mark.require_files('gcore/data/mfloat32.vrt', 'gcore/data/float32.tif')
   def test_gdaladdo_1(gdaladdo):
       gdaladdo('gcore/data/mfloat32.vrt 2 4')
       assert os.path.exists('gcore/data/mfloat32.vrt.ovr')

       tiff_ovr.tiff_ovr_check(gdal.Open('mfloat32.vrt'))

이 테스트가 실제로 무엇을 테스트하는지가 훨씬 명확하고, 공유 사용 픽스처(``gdaladdo`` 및 ``require_files``)가 정리(cleanup) 및 조건부 건너뛰기(conditional skipping)를 포함하는 모든 지원 기능을 처리합니다.

산출물 테스트
~~~~~~~~~~~~~

pytest는 격이 다를 정도로 가독성이 좋은 산출물을 출력하고, 이를 더 보기 좋게 만들어주는 ``pytest-sugar`` 플러그인으로 보강합니다:

-  테스트가 성공한 경우 산출물을 여러 줄 출력하지 않습니다. (기본적으로 테스트별로 ``.`` 또는 ``✓`` 문자 하나만 출력합니다.)

-  테스트가 실패한 경우 역추적 정보(traceback)를 출력합니다. 실패한 테스트가 생성하는 모든 로그, stdout 및 stderr도 출력합니다. 실패 원인을 디버깅하기 위한 훌륭한 시작점입니다.

-  실패한 표명(assertion)에 사용된 모든 표현식을 출력합니다.

-  터미널이 색상을 지원하는 경우 테스트 산출물에 확실하게 (적색/녹색으로) 색상을 입힙니다.
   `이 스크린샷 <https://trac.osgeo.org/gdal/wiki/rfc72_pytest#Testoutput>`_ 을 참조하십시오.

1기 계획
--------

진행 상황은 `963번 풀 요청 <https://github.com/OSGeo/gdal/pull/963>`_ 에서 볼 수 있습니다.

-  코드 자동화를 사용해서 기존 파이썬 자동 테스트 스위트가 pytest 스타일 표명을 사용하도록 변환합니다.

-  모든 테스트를 ``test_*()`` 로 재명명합니다. pytest는 정규 표현식을 대상으로 이름을 비교해서 일치하는 테스트를 찾는데 이것이 기본 정규 표현식입니다.

-  가능한 경우 ``post_reason()`` / ``return 'fail'`` 호출로부터 표명을 생성합니다.

-  모든 ``skip`` / ``fail`` / ``success`` 반환값을 대체합니다.

-  :file:`sys.path` 로부터 추가적인 :file:`../pymod` 를 제거합니다. 모든 테스트가 이제 단일 프로세스에서 실행됩니다.

-  테스트 파일들로부터 ``__main__`` 블록 및 ``gdaltest_list`` 를 제거합니다.

-  이 모든 변경 사항들이 총체적으로 더 나은 테스트 모음/선택, 산출물 캡처, 그리고 개선된 표명 및 리포트를 달성합니다.

-  동적으로 생성된 테스트가 `파라미터화 <https://docs.pytest.org/en/latest/how-to/parametrize.html>`_ 를 사용하도록 수동으로 변환합니다.

-  느린 또는 인터넷 테스트가 계속 그렇게 표시되고 기본적으로 이런 테스트를 건너뛰도록 확인합니다.

-  테스트 산출물을 보기 좋게 만들기 위해 `pytest-sugar <https://github.com/Teemu/pytest-sugar>`_ 를 사용합니다.
   ``pytest-sugar`` 가 Travis-CI의 산출물 버퍼링과 제대로 동작하지 않기 때문에 CI에서는 비활성화시킵니다.

-  환경 특화 테스트 건너뛰기를 CI로부터 테스트 스위트로 옮기고, 가능한 경우 추가적인 태그/표시도 옮깁니다.

-  기존 CI 테스트를 통과하는지 확인하고 모든 실패 사례를 디버깅합니다.

-  pytest 자체에 대한 문서 및 직관적인 설치 과정을 추가합니다.

주목할 만한 변경 사항 및 그 영향
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  이제 ``cd autotest ; pytest`` 로 테스트를 실행합니다.
   (처음 실행하는 경우 ``pip install -r requirements.txt`` 로 pytest를 설치해야 할 수도 있습니다.)

-  이제 모든 테스트가 단일 프로세스에서 실행됩니다. (예전에는 각 테스트 모듈에 대해 분기되었습니다.) 이는 다음을 의미합니다:

   -  이제 테스트 모음 도중 오류를 상세하게 출력하고, 역추적 정보와 함께 전체 테스트 실행를 즉시 중단시킵니다. 예전에는 파일의 문법 오류 및 모듈 수준에서의 오류 같은 내용을 놓치기 쉬웠습니다.

   -  단일 세그폴트(세그멘테이션 오류)가 전체 테스트 실행을 중단시킬 것입니다.

-  이제 전체 파일들만이 아니라 개별 테스트 파일을 실행할 수 있습니다. 하지만 테스트들이 '아직은 서로에게 의존하고 있습니다'. 따라서 개별 테스트를 실행하면 전체 모듈을 실행하는 경우와는 다르게 동작하게 될 수도 있습니다.

-  ``test_py_scripts.run_py_script`` 가 항상 스크립트를 서브프로세스로 실행하도록 수정했습니다. pytest를 사용하면 원래 메소드의 stdout 캡처가 이상하게 동작했기 때문입니다. 이 변경으로 ``/vsimem/`` 루트에 있는 파일들을 스크립트로 전송하는 데 의존하는 몇몇 테스트를 망가뜨렸기 때문에, 이런 테스트들이 ``tmp/`` 루트를 대신 사용하도록 변경했습니다.

-  파이썬 2.7 미만 버전들에 대해서는 테스트 스위트를 지원하지 않습니다.

.. _plan-phase-2--future-work:

2기 계획 / 향후 작업
--------------------

-  한 번에 전체 모듈을 실행해야 할 필요가 없도록 각 테스트의 독립성을 향상시킵니다.

-  전체 수준 ``gdaltest.<drivername>_drv`` 변수들을 제거하고 pytest 픽스처(fixture)로 대체합니다.

-  임시 파일 처리 및 정리에 픽스처를 사용합니다.

-  실제로 무엇이 컴파일되었는지를 기반으로 자동화된 테스트 건너뛰기를 더욱 자동화합니다.

-  `Black <https://github.com/ambv/black>`_ 을 사용해서 스타일 정리를 자동화합니다.

-  테스트 실행을 기본적으로 병렬화시키는 것을 고려합니다. (이를 위해 `사용할 수 있는 플러그인 <https://github.com/pytest-dev/pytest-xdist>`_ 이 몇 개 있습니다.)

투표 이력
---------

프로젝트 운영 위원회 다음 투표로 승인되었습니다:

-  이벤 루올 +1
-  대니얼 모리셋 +1
-  하워드 버틀러 +1
-  커트 슈베어 +1

-  유카 라흐코넨 +0

