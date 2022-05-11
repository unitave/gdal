.. _rfc-8:

===========================
RFC 8: 개발자 지침
===========================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 초안

목적
----

이 문서에서는 GDAL/OGR 프로젝트를 위한 개발자 관행을 문서화하려 합니다. 이 문서는 계속 진화할 것입니다.

이식성
------

GDAL은 32비트 및 64비트 컴퓨팅 환경에 널리 이식될 수 있도록 노력합니다. 여러 가지 방법으로 -- 컴파일러 특화 지시문을 사용하지 않고, 새롭지만 널리 사용할 수는 없는 C++의 면면을 사용하지 않으며, 가장 중요한 방법으로 :file:`gdal/port` 디렉터리에 있는 CPL 함수들에 플랫폼 특화 작업들을 추상화함으로써 -- 이를 달성하고 있습니다.

일반적으로 메모리 할당, 경로 파싱, 파일 시스템 I/O, 멀티스레딩 기능, 그리고 ODBC 접근 같은 작업을 위한 운영 체제 기능들보다는 사용할 수 있는 CPL 함수들을 먼저 사용해야 합니다.

변수 명명
---------

기존 GDAL 및 OGR 코드 가운데 다수는 수정 헝가리안 표기법 규범을 사용합니다. 반드시 이 규범을 따라야 할 필요는 없지만, 이 규범을 사용해서 코드를 유지/관리하는 경우 변경 사항을 적용할 때 이 규범을 계속 준수하는 편이 좋습니다. 가장 중요한 점은 이 규범을 적절하지 않게 사용하지 않는 것입니다. 아주 혼란스러울 수 있기 때문입니다.

헝가리안 접두어의 경우 접두어가 유형 정보를 말해주며, 변수의 의미를 담고 있을 수도 있습니다. 다음은 GDAL/OGR에서 사용되는 접두어들 몇몇의 예시입니다.

-  *a*: 배열(array)
-  *b*: C++ 불(boolean). C 언어에서 오직 TRUE/FALSE 값만 가지고 있는 정수형에도 사용됩니다.
-  *by*: 바이트(GByte / 부호 없는 문자형)
-  *df*: 부동소수점형 값(배정밀도)
-  *e*: 목록(enumeration)
-  *i*: 배열 또는 루프 색인으로 사용되는, 0에서 시작하는 정수형 값
-  *f*: 부동소수점형 값(단정밀도)
-  *h*: (GDALDatasetH 같은) 불분명한(opaque) 핸들
-  *n*: 정수형 숫자 (범위 미지정)
-  *o*: C++ 객체
-  *os*: CPLString
-  *p*: 포인터
-  *psz*: 0으로 끝나는 문자열을 가리키는 포인터 (예: "char \*pszName;")
-  *sz*: 0으로 끝나는 문자열 (예: "char szName[100];")
-  할 일: (전체 수준 또는 전체 파일 수준 가운데) 상수의 접두어는? 'k'를 제안합니다.

접두어를 여러 개 붙일 수 있습니다. 다음은 접두어가 의미를 담고 있는 몇몇 변수들의 예시입니다.

-  \*char !\*\ *papszTokens*: 문자열 배열을 가리키는 포인터
-  \*int *panBands*: 숫자형 배열의 첫 번째 요소를 가리키는 포인터
-  \*double *padfScanline*: 더블형 배열의 첫 번째 요소를 가리키는 포인터
-  \*double *pdfMeanRet*: 더블형 값 하나를 가리키는 포인터
-  \*GDALRasterBand *poBand*: 단일 객체를 가리키는 포인터
-  \*GByte *pabyHeader*: 바이트형 배열을 가리키는 포인터

변수명을 위한 표준 규범은 변수명에 들어가는 각 단어의 첫 글자를 대문자로 작성하는 것이라는 사실도 알아두면 좋습니다.

메모리 할당
-----------

`RFC 19: GDAL에서 더 안전한 메모리 할당 <./rfc19_safememalloc>`_ 에 따라, CPLMalloc(x \* y) 또는 VSIMalloc(x \* y) 대신 VSIMalloc2(x, y)를 사용할 수 있습니다. VSIMalloc2 함수는 곱셈에서 오버플로우 가능성을 탐지해서 오버플로우가 발생하는 경우 NULL 포인터를 반환할 것입니다. 이 함수는 x 및 y가 래스터 차원 또는 래스터 블록 크기와 관련된 GDAL 래스터 드라이버에서 유용할 수 있습니다. 마찬가지로, CPLMalloc(x \* y \* z) 대신 VSIMalloc3(x, y, z)를 사용할 수 있습니다.

헤더 및 주석 블록
-----------------

.. _misc-notes:

기타 메모
---------

-  소문자 파일명을 사용하십시오.
-  C++ 파일에 (.cc가 아니라) .cpp 확장자를 사용하십시오.
-  파일 또는 디렉터리 이름에 공백 또는 다른 특수 문자를 사용하지 마십시오.
-  문자 4개 들여쓰기 수준을 사용하십시오.
-  소스 코드에 탭 문자 대신 공백을 사용하십시오.
-  각 줄을 문자 79개 이하로 유지하려 노력하십시오.

참고
----

-  `http://erouault.blogspot.com/2016/01/software-quality-improvements-in-gdal.html <http://erouault.blogspot.com/2016/01/software-quality-improvements-in-gdal.html>`_
-  `https://travis-ci.org/OSGeo/gdal/builds <https://travis-ci.org/OSGeo/gdal/builds>`_
-  `https://ci.appveyor.com/project/OSGeo/gdal/history <https://ci.appveyor.com/project/OSGeo/gdal/history>`_
-  `https://travis-ci.org/rouault/gdal_coverage/builds <https://travis-ci.org/rouault/gdal_coverage/builds>`_
-  `https://ci.appveyor.com/project/rouault/gdal-coverage/history <https://ci.appveyor.com/project/rouault/gdal-coverage/history>`_
-  `https://gdalautotest-coverage-results.github.io/coverage_html/index.html <https://gdalautotest-coverage-results.github.io/coverage_html/index.html>`_

파이썬 코드
-----------

-  :file:`autotest`, :file:`swig/python/scripts` 및 :file:`swig/python/samples` 에 있는 모든 파이썬 코드는 Pyflakes 검사기(현재 사용 버전: 0.8.1)에서 OK로 통과되어야 합니다. "Travis-CI" 작업이 이를 요구합니다.

-  파이썬 2 및 3버전 둘 다 호환되도록 파이썬 코드를 작성해야 합니다.

