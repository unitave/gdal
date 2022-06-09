.. _rfc-69:

=======================================================================================
RFC 69: C/C++ 코드 서식
=======================================================================================

이 문서에서는 GDAL의 C 및 C++ 소스 코드 전반에 사용할 바람직한 코드 서식 스타일을 제안하고 설명합니다.

======== ======================================
저자:    커트 슈베어(Kurt Schwehr)
연락처:  schwehr@google.com / schwehr@gmail.com
제안일:  2017년 5월 4일
Status:  진행 중
======== ======================================

이 RFC는 마테우시 워스코트(Mateusz Łoskot)가 작성한 `GEOS RFC 4 <https://trac.osgeo.org/geos/wiki/RFC4>`_ 를 기반으로 합니다.

**할 일**: 서식 예시 추가

요약
----

이 RFC는 C 및 C++ 언어로 GDAL을 프로그래밍하기 위한 기본 코드 서식 스타일 지침을 제안하고 설명합니다.

이 문서의 목표는 기본 코드 서식 스타일에 대한 합의에 도달하기 위한 과정을 시작하는 것입니다.

동기
----

GDAL 소스 코드의 서식을 결정하고 GDAL C/C++ 코드베이스에 이런 전체 수준에서 일관성을 가지는 서식을 적용할 필요가 있습니다.

코드베이스 전반에 걸쳐 동일한 서식 스타일은 기존 코드를 쉽게 읽고 이해할 수 있게 해주고, 새로운 개발이라는 중요한 측면에서 코드 작성에 집중하고 즐길 수 있게 해주며, 패치 작업 또는 풀(pull) 요청 코드 리뷰의 부하를 줄여주고 `사소한 일에 대한 종교적 논쟁 <https://wiki.c2.com/?WhereDoTheBracesGo>`_ 을 막아줍니다. 작은 프로젝트에서조차도 기여 개발자들은 코드 서식에 대한 합의 없이 작업하는 데 대한 문제들을 맞닥뜨리곤 합니다.

수많은 오픈 소스 소프트웨어 프로젝트에서 이런 지침의 활용성이 증명되었습니다.

이 제안의 범위는 서식 스타일 지침으로 분명히 제한되어 있습니다. 명명법 같은 소프트웨어 작성의 다른 측면을 다루는 일반 코드 작업 지침을 개발하려는 것이 아닙니다.

제안
----

개발자들이 제대로 된 서식을 갖춘 코드를 수월하게 생산할 수 있도록 하는 것이 중요합니다.

이 제안은 `clang-format <https://clang.llvm.org/docs/ClangFormat.html>`_ 3.8 이상 버전을 사용해서 GDAL 코드를 위한 C++ 코드 서식 규칙을 정의할 것을 제안합니다.

``clang-format`` 은 C/C++ 코드의 서식을 자동으로 교정해주는 도구로, 개발자가 서식 스타일 문제점에 관해 걱정할 필요가 없게 해줍니다. 자신만의 파서(parser)를 사용하는 다른 도구들과는 달리, ``clang-format`` 은 `클랭(Clang) <https://ko.wikipedia.org/wiki/%ED%81%B4%EB%9E%AD>`_ 토크나이저(tokenizer)를 이용해서 클랭 컴파일러와 동일한 C++ 소스 코드를 지원합니다. ``clang-format`` 은 이렇게 정확한 산출물 생성을 보장하고 다른 도구들에는 없는 기능들을 제공합니다. (예를 들면 AStyle은 할 수 없는, 코드, 문자열, 배열에 상관없이 긴 줄을 감쌀(wrap) 수 있는 기능이 있습니다.)

:file:`.clang-format` 환경설정 파일에 스타일 설정을 정의할 수 있지만, 가능한 한 작업을 쉽게 만들기 위해 기본 스타일(LLVM 스타일?)을 사용할 것입니다.

``clang-format`` 은 실행하기 쉽고 독립형 도구, 또는 수많은 편집기 통합 또는 다른 맞춤형 유틸리티 가운데 하나로서 개발 워크플로를 지원할 수 있습니다. (예: ``git cl format`` [Chromium])

코드 서식 재구성(code reformatting)의 자동화는 제안하지 않습니다. 코드 서식 표준을 따르지 않는 개발자라는 원인이 아니라 증상을 다루게 될 것이기 때문입니다.

기본 서식 스타일을 강제할 수 있는 어떤 수단도 제안하지 않지만, 현재 사용되는 (Travis CI 같은) CI(Continuous Integration) 서비스를 커밋 이후 안전성 밸브로 이용할 수도 있습니다. (예를 들어 MongoDB가 사용하는 `clang_format.py <https://github.com/mongodb/mongo/blob/master/buildscripts/clang_format.py>`_ 빌드 스크립트처럼) ``clang-format`` `린트(lint) <https://ko.wikipedia.org/wiki/%EB%A6%B0%ED%8A%B8_(%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4)>`_ 가 실패하는 경우 컴파일이 중단될 것입니다. 아니면 SVN/깃(Git)에 게이트키퍼를 설치해서 코드 포맷 스타일을 준수하지 않는 코드가 포함된 커밋을 거부할 수도 있습니다.

코드 서식 규칙
--------------

어떤 코드 서식 규칙을 사용할 것인가?

   "*성숙한 엔지니어라면 어떤 표준이냐보다 표준이 있다는 것이 더 중요하다는 사실을 알고 있습니다.*"
   ~[MongoDB]

``clang-format`` 이 기본 규칙 (예: LLVM, 모질라, 리눅스, 구글 C++ 스타일) 몇 개를 제공합니다.

이 제안은 어떤 수정도 하지 않은 기본 스타일 가운데 하나를 사용할 것을 권장합니다. 환경설정을 미세 조정할 수는 있지만, 이 RFC는 단순성을 목표로 삼고 있습니다.

그 이유는 두 가지입니다:

-  GDAL 코드를 제대로 확립된 광범위한 C/C++ 프로젝트 영역들과 통합합니다.
-  기나긴 논쟁 및 종교 전쟁을 방지합니다.

``.clang-format``
~~~~~~~~~~~~~~~~~

코드베이스에 :file:`.clang-format` 환경설정 파일이 필요할 일이 없기를 바랍니다.

``.editorconfig``
~~~~~~~~~~~~~~~~~

`EditorConfig <https://editorconfig.org/>`_ 이 현재 사용 중이며, ``.editorconfig`` 파일을 제공해서 유명 코드 편집기들에 평문 텍스트 파일의 고유한 유형에 대해 들여쓰기, 공백 문자 및 새줄 문자 같은 기본 스타일 설정에 관해 자동적으로 알려줍니다.

:file:`.clang-format` 환경설정이 필요한 경우 선택한 :file:`.clang-format` 설정에 맞춰 :file:`.editorconfig` 파일을 업데이트해야 할 것입니다.

EOL
~~~

``clang-format`` 은 줄 끝(end of line)을 강제하지 않습니다.

EOL 마커는 어떤 코드 작업 스타일의 일부분이 아니라 `파일 인코딩 결정의 일부분 <https://lists.llvm.org/pipermail/cfe-commits/Week-of-Mon-20130930/090200.html>`_ 으로 간주됩니다.

EOL 마커를 :file:`.gitattributes` 및 :file:`.editorconfig` 파일이 제어하는 프로젝트 수준 설정으로서 강제할 수 있습니다.

하지만, 그렇다고 하더라도 EOL 마커는 프로젝트 수준 설정으로부터 독립적인, 개발자가 선택한 환경에서 환경설정할 수 있는 (예: ``git config``) 설정으로 남겨두어야 할 것입니다.

대규모 서식 재구성
~~~~~~~~~~~~~~~~~~

기존 코드는 어떻게 할 것인가?

이 제안은 코드베이스를 한 번만 대규모로 서식 재구성할 것을 권장합니다.

이렇게 하면 저장소 로그(예: ``svn blame``)가 난잡해질 수도 있지만, 드물게 (예를 들면 1년 단위로) 작업하고 작업 시 전체 코드베이스에 적용한다면 소스 코드 이력에 큰 지장을 주지는 않을 것입니다. 이력이 편향되는 일을 막기 위해 커밋 비교 시 공백 문자를 무시하는 ``git blame -w`` 를 사용하는 것도 한 가지 방법입니다.

코드 서식 규칙을 부분적으로 적용하면 [MongoDB]의 이점을 완전하게 이용하지 못 한 채 서로 다른 스타일이 혼합된 코드베이스를 생성하게 되기 때문에 더 많은 작업을 해야 할 것입니다.

브랜치
^^^^^^

대규모 서식 재구성을 실행할 브랜치들은 다음과 같습니다:

-  ``trunk``
-  [STRIKEOUT:``branches/2.2``]
-  [STRIKEOUT:``branches/2.1``]
-  [STRIKEOUT:``branches/2.0``]

대규모 서식 재구성 이후
-----------------------

코드베이스의 자연적인 엔트로피에 대응하는 방법:

-  코드를 작성하는 동안 ``clang-format`` 통합을 사용할 것을 강력하게 권장합니다.

-  커밋 또는 풀 요청 전에 코드 서식을 점검하십시오.

-  코드 서식 변경 사항을 커밋해야 하는 경우, 개별 커밋으로 수행하십시오. 코드와 서식 변경을 함께 커밋하지 마십시오.

   -  저장소의 이력이 난잡해진다는 단점이 있긴 하지만, 이 제안은 서로 다른 스타일이 혼합된 코드베이스가 더 나쁘다고 주장합니다.

   "*결국, 코드 서식 또는 그에 대한 논의에 낭비되는 모든 시간이 사라집니다.*"
   ~[MongoDB]

구현
----

MongoDB가 사용하는 :file:`clang_format.py` 빌드 스크립트에서 쓰이는 접근법을 기반으로 ``clang-format`` 린트만을 실행하기 위한 Travis CI "스타일 안전성 밸브"를 설정합니다.

기타
----

GDAL을 GCC 6 이상 버전으로 빌드하는 사용자는 일관적인 코드 서식 스타일이 `새로운 컴파일러 경고 <https://developers.redhat.com/blog/2016/02/26/gcc-6-wmisleading-indentation-vs-goto-fail>`_ 몇십 개를 피할 수 있게 해주기 때문에 이를 환영할 수도 있습니다:

::

   src/geom/Polygon.cpp: In member function ‘virtual int geos::geom::Polygon::getCoordinateDimension() const’:
   src/geom/Polygon.cpp:154:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
        if( shell != NULL )
        ^~
   src/geom/Polygon.cpp:157:2: note: ...this statement, but the latter is misleadingly indented as if it is guarded by the ‘if’
     size_t nholes=holes->size();
     ^~~~~~

참조
----

-  [MongoDB] ClangFormat으로 성공하기: `1부 <https://engineering.mongodb.com/post/succeeding-with-clangformat-part-1-pitfalls-and-planning/>`_, `2부 <https://engineering.mongodb.com/post/succeeding-with-clangformat-part-2-the-big-reformat/>`_, `3부 <https://engineering.mongodb.com/post/succeeding-with-clangformat-part-3-persisting-the-change/>`_

-  [Chromium] `크로미움 C++ 코드에 clang-format 사용하기 <https://chromium.googlesource.com/chromium/src/+/master/docs/clang_format.md>`_

-  `clang-format 대화형 지침 및 빌더 <https://github.com/adamyanalunas/clangformat.com>`_

-  `https://zed0.co.uk/clang-format-configurator/ <https://zed0.co.uk/clang-format-configurator/>`_

-  `GEOS RFC 4 <https://trac.osgeo.org/geos/wiki/RFC4>`_

