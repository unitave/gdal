.. _rfc-78:

===========================================
RFC 78: gdal-utils 패키지
===========================================

============ =========================
저자:        이단 미아라(Idan Miara)
연락처:      idan@miara.com
제안일:      2020년 12월 3일
최신 수정일: 2021년 3월 26일
상태:        승인, GDAL 3.3버전에 구현
============ =========================

요약
----

이 RFC는 `PyPI(Python Package Index) <https://pypi.org/>`_ 상에 GDAL 코어 SWIG 바인딩으로부터 나온 것들을 제외한 모든 (스크립트 형식의) GDAL 파이썬 모듈을 고유 배포판으로 패키징할 것을 제안합니다. (GDAL 3.2버전에서 도입된) GDAL 파이썬 하위 패키지 ``osgeo.utils`` 를 ``osgeo_utils`` 라는 이름의 패키지로 재명명할 것입니다.

GDAL 3.2버전에서 GDAL 3.1 이하 버전으로부터 나온 독립형 파이썬 스크립트들을 ``osgeo.utils`` 로 변환했었습니다. 하위 호환성을 위해 이 스크립트들은 계속 존재하며, 파이썬 모듈을 감싸는 작은 래퍼(tiny wrapper)로 기능합니다. 이 RFC는 이 스크립트들의 사용자에게 영향을 미치지 않을 것입니다. 이 스크립트들이 GDAL 3.3버전에서도 GDAL 3.2 이하 버전들에서와 동일한 방식으로 계속 기능할 것이기 때문입니다.

하위 호환성을 최대한 보장하기 위해, 'PyPI'에서 (GDAL 코어 SWIG 바인딩을 포함하는) ``osgeo`` 패키지 및 ``osgeo_utils`` 패키지를 계속 ``gdal`` 이라는 이름의 단일 'sdist(source distribution)'로 배포할 것입니다.

뿐만 아니라 'PyPI'에서 ``gdal-utils`` 이라는 이름 아래 순수 파이썬 'wheel' 배포판을 사용할 수 있을 것입니다.

이렇게 하면 바인딩을 업그레이드 하지 않은 채 유틸리티를 업그레이드하고자 하는 사용자들이 ``pip install --upgrade gdal-utils`` 명령어를 이용해서 그렇게 할 수 있습니다. (더 자세한 내용은 다음 단락을 읽어보십시오.)

동기
----

윈도우 상에서 (그리고 아마도 다른 플랫폼들 상에서도) GDAL 파이썬 개발자의 편이성 증대:
   ``gdal`` 을 복제하고 파이썬 경로에 (PyCharm에서는 'Source Root'로 표시되는) :file:`gdal/swig/python` 을 추가하는 간단한 방법은 :file:`gdal/swig/python/osgeo` 에서 :file:`pyc` 파일들이 누락되어 있기 때문에 작동하지 않을 것입니다. 따라서 파이썬 경로에 :file:`osgeo` 를 추가하면 이미 설치되어 있을 수도 있는 GDAL 바이너리 설치본을 (예를 들면 ``osgeo4w`` 또는 크리스토프 골케(Christoph Gohlke)의 바이너리 윈도우 'wheel'을) 마스킹할 것입니다.
   :file:`osgeo` 디렉터리에 :file:`pyc` 파일들을 복사하는 미봉책은 다음과 같은 자체적인 문제를 일으킵니다:

   -  서로 다른 ``gdal`` 버전을 가진 해석기들을 뒤바꾸는 것은 더 많은 문제를 일으킵니다.
   -  정리된 깃(git) 작업 트리가 없기 때문에 깃에 변경 사항을 커밋하기가 더 어렵습니다.

   ``gdal-utils`` 를 또다른 루트로 이동시키면 이 문제를 완벽하게 방지합니다.

``gdal`` 및 ``gdal-utils`` 버전 혼합 허용:
   파이썬 코드가 GDAL 코어와는 반독립적으로 발전하고 특정 GDAL 버전에 직접적으로 의존하지 않기 때문에, 최신 ``gdal-utils`` 패키지를 예전 버전의 ``gdal`` 코어 바인딩과 함께, 또는 그 반대로 사용하고 싶을 수도 있습니다. 현재 이렇게 하려면 서로 다른 ``gdal`` 패키지들의 콘텐츠를 혼합해야 할 것입니다.

   ``gdal`` 패키지가 플랫폼별로 특화되어 있고 컴파일을 필요로 하기 때문에, 일부 배포판에서는 새로운 GDAL 버전으로 업그레이드하는 데 시간이 더 걸릴 수도 있습니다. 즉 ``pip install --upgrade gdal-utils`` 명령어를 사용하면 ``gdal-utils`` 패키지를 쉽게 그리고 ``gdal`` 패키지 업그레이드와는 독립적으로 업그레이드할 수 있습니다.

   다른 한편으로는, RFC 77에서 한 것처럼 또다른 파이썬 버전 지원으로 중단하는 경우 더 최신인 (여전히 예전 파이썬 버전을 지원할 수도 있는) GDAL 코어 바인딩을 파이썬 버전 지원을 더 빨리 중단할 수도 있는 예전 ``gdal-utils`` 와 함께 계속 사용할 수도 있습니다.

   사용자가 최신 GDAL로 업그레이드할 수 없을 수도 있는 이유는 다음과 같습니다:

   -  (데비안 같은) LTS 배포판 또는 (QGIS LTS 같은) LTS 응용 프로그램을 사용하는 경우
   -  (LTS가 아니어도) 사용자의 플랫폼 또는 배포판에서 최신 GDAL을 사용할 수 없는 경우
   -  사용자 코드가 특정 GDAL 버전에서만 사용할 수 있는 몇몇 바이너리 GDAL 플러그인에 의존하는 경우

   현재 QGIS(또는 QGIS LTS)를 GDAL 3.1버전과 함께 사용하는데 'gdal_calc' 유틸리티에 추가된 깔끔한 기능을 사용하려는 경우가 구체적인 예시일 것입니다. 이 RFC가 적용되면 ``pip install --upgrade gdal-utils`` 명령어만 실행하면 됩니다. 이 패키지는 순수 파이썬이기 때문에 업그레이드하기 쉬울 것입니다.

   ``gdal-utils`` 각 버전을 동등한 버전의 ``gdal`` 에 대해서만 테스트할 것이긴 하지만, 대부분의 경우 서로 다른 버전들이 계속 호환될 것입니다. 그러나 보장은 못 합니다.

   이 RFC는 향후 이 패키지들의 서로 다른 버전들 사이의 호환성을 쉽게 테스트할 수 있도록 할 것입니다. 그 첫 번째 단계로 ``gdal-utils`` 패키지를 ``gdal`` 패키지로부터 완전하게 독립적으로 만드는 일을 고려할 수 있습니다. 이렇게 하면 이후 혹시라도 ``gdal`` 'wheel' 배포판으로부터 유틸리티를 제거하고 ``gdal-utils`` 'wheel' 배포판에만 유지할 것을 결정하는 경우, 상위 호환성을 보장할 수 있게 될 가능성도 있습니다.

패키지 이름 및 PyPi 배포
------------------------

이 RFC는 사용자가 변경해야 할 사항들을 최소화하는 동시에 혼합 버전을 사용할 수 있게 하기 위해 유틸리티들을 패키지로만 배포할 뿐만 아니라 올인원(all-in-one) 패키지로 유지할 것을 제안합니다:

-  https://pypi.org/project/GDAL/

``gdal`` 이라는 이름의 단일 pypi.org 'wheel'의 배포를 유지하고 두 패키지를 모두 포함시킬 것입니다. 이렇게 하면 원활환 전환 및 최대 하위 호환성을 보장할 것입니다.

-  https://pypi.org/project/gdal-utils/

``osgeo_utils`` 패키지만 포함하는 새로운 pypi.org 패키지를 도입합니다. 이렇게 하면 바인딩을 업그레이드하지 않은 채 유틸리티를 업그레이드할 수 있을 것입니다.

``gdal`` PyPI 패키지 이름과의 일관성을 유지하기 위해, 유틸리티 PyPI 패키지를 ``gdal-utils`` 로 명명합니다.

``osgeo_utils`` 라는 이름은 ``osgeo`` 이름공간 및 모듈 이름들과 일관성을 유지합니다.

.. code-block::

    pip install gdal
    pip install gdal-utils

.. code-block:: Python

    from osgeo import gdal
    from osgeo_utils import gdal_calc, ogr_foo, osr_bar

바인딩 업그레이드 없이 유틸리티를 업그레이드하는 방법
-----------------------------------------------------

> ``gdal`` 올인원 패키지를 설치한 다음 ``gdal-utils`` 패키지를 설치하는 경우 충돌하지 않겠습니까?

'wheel' 배포판을 ``pip install`` 하면 (다른 패키지로 설치했더라도) 모든 기존 파일을 덮어씁니다. 즉 ``pip install gdal`` 명령어 다음에 ``pip install gdal-utils`` 명령어를 실행하면 ``gdal-utils`` 의 유틸리티를 사용하게 됩니다. 이후 다시 다른 버전의 ``pip install gdal`` 명령어를 실행하면 다시 ``gdal`` 의 유틸리티를 사용하게 됩니다.
(어떤 버전 번호가 더 높은지가 아니라 어떤 버전을 더 나중에 설치했느냐가 중요한 것으로 보입니다.)

``pip install gdal`` 명령어 다음에 ``pip install gdal-utils`` 를 실행하고 그 다음 ``pip uninstall gdal-utils`` 를 실행하는 경우, 유틸리티가 설치 제거되어 유틸리티가 없는 GDAL이 남게 될 것입니다. 이때 다시 유틸리티를 사용하려면 ``pip install gdal-utils`` 또는 ``pip install gdal --ignore-installed`` 명령어를 실행하면 됩니다. (다른 버전을 설치하는 경우 ``--ignore-installed`` 옵션은 필요없습니다.)

제한 사항 및 범위
-----------------

이 RFC의 범위는 SWIG 바인딩을 제외한 GDAL 파이썬 코드에만 적용됩니다. GDAL이 지원하는 다른 어떤 언어에도 영향을 미치지 않습니다. 파이썬 SWIG 바인딩을 이용해서 GDAL 코어를 테스트하기 때문에, 이 RFC는 어떤 방식으로든 이를 변경하자고 제안하지 않습니다.
과거에 바이너리 'wheel' 배포판에 대해 논의했으며, 이는 이 RFC의 아이디어와 연결되어 있습니다.

``gdal`` 및 ``gdal-utils`` 호환성
---------------------------------

이 RFC는 ``gdal-utils`` 를 계속 동일 버전의 ``gdal`` 을 대상으로만 테스트할 것을 제안합니다. 대부분의 경우 서로 다른 버전들이 계속 호환될 것입니다. 그러나 보장은 못 합니다.

에너지를 가장 적게 들이는 접근법은 ``gdal-utils`` 가 버전이 'x.y'가 아닌 몇몇 ``gdal`` 버전들과 호환되도록 유지하는 것일 수도 있습니다. ``gdal-utils`` 의 :file:`setup.py` 에 새로운 GDAL 최저 지원 버전을 지정해서 너무 오래된 GDAL 버전 지원을 공식적으로 중단할 수도 있습니다.

하위 호환성을 최대화하기 위해 그리고 ``gdal`` 을 동일 버전의 ``gdal-utils`` 을 대상으로만 테스트할 것이기 때문에, 유틸리티만 가진 새로운 개별 'wheel' 배포판뿐만 아니라 ``osgeo`` 및 ``osgeo_utils`` 도 계속해서 단일 'wheel' 배포판 안에 배포할 것입니다.

``gdal-utils`` 모듈 또는 함수가 실제로 특정 최저 버전의 ``gdal`` 을 요구하는 경우 (예를 들어 새 GDAL C API에 의존하는 경우) 런타임 시 ``osgeo.__version__`` 과 비교해서 호환성을 확인할 수 있습니다.

버전 번호 매기기
----------------

``gdal-utils`` 이 여전히 GDAL의 개발과 연계되어 개발될 것이기 때문에, 계속 GDAL과 동일한 'x.y.z' 버전 번호로 GDAL과 함께 배포될 것입니다. 어떤 이유로 ``gdal-utils`` 에 핫픽스(hotfix)가 필요한 경우, 'x.y.z.p' 버전을 사용할 수도 있습니다. 이런 버전 번호는 -- '3.3.0' < '3.3.0.1' < '3.3.1' 처럼 -- 'z+1' 버전의 배포에 영향을 미치지 않을 것입니다.

하위 호환성 문제점
------------------

-  ``osgeo.utils`` 를 ``osgeo_utils`` 로 대체해야 할 것입니다:
  GDAL 3.2버전에서만 단일 문자만 바꾸는, 유일한 주요 변경 사항입니다.

-  :file:`swig/python/scripts`:
   (유틸리티를 감싸는 얇은 래퍼인) GDAL 스크립트의 사용자에게 영향을 미치지 않습니다.

폴더 구조 변경
--------------

-  :file:`gdal/swig/python/osgeo/utils` -> :file:`gdal/swig/python/gdal-utils/osgeo_utils`

-  :file:`gdal/swig/python/osgeo/setup.py`:
   ``gdal-utils`` 폴더 아래 있는 새로운 위치에 있는 유틸리티들을 포함하도록 업데이트했습니다.

-  :file:`gdal/swig/python/gdal-utils/setup.py`:
   ``gdal-utils`` 를 위한 추가적인 단계를 추가했습니다.

CI에 미치는 영향
----------------

예를 들면 `풀 요청 3579번 <https://github.com/OSGeo/gdal/pull/3579>`_ 에서처럼 CI에 ``gdal-utils`` 'wheel' 빌드 작업을 추가할 수 있습니다. 그 이외의 영향은 없습니다.

GDAL 코어에 미치는 영향
-----------------------

없음.

SWIG 바인딩 변경 사항
---------------------

없음.

보안에 미치는 영향
------------------

없음.

성능에 미치는 영향
------------------

없음.

문서화
------

:file:`README` 에 이 변경 사항의 영향을 문서화해야 합니다.

테스트
------

:file:`pytest` 를 살짝 변경했습니다.

예전 논의
---------

이 RFC의 주제는 과거에 논의된 적이 있습니다:

-  https://lists.osgeo.org/pipermail/gdal-dev/2020-November/053020.html

관련 풀 요청
------------

- https://gdal.org/development/rfc/rfc77_drop_python2_support.html
- https://github.com/OSGeo/gdal/pull/3131
- https://github.com/OSGeo/gdal/pull/3117
- https://github.com/OSGeo/gdal/pull/3247

구현
----

이단 미아라가 이 RFC를 구현했습니다.

투표 이력
---------

https://lists.osgeo.org/pipermail/gdal-dev/2021-March/053729.html

-  이벤 루올 +1
-  하워드 버틀러 +1

-  커트 슈베어 +0
-  유카 라흐코넨 +0

-  션 길리스 -0

