.. _python:

================================================================================
파이썬 바인딩
================================================================================

이 파이썬 패키지 및 확장 사양은 `GDAL <https://gdal.org/>`_ 지리공간 데이터 추상 라이브러리를 프로그래밍하고 조정하기 위한 도구 모음입니다.
이 패키지는 실제로 2개의 라이브러리 -- 지리공간 래스터 데이터 용 GDAL과 지리공간 벡터 데이터용 OGR -- 이지만 이 문서의 목적을 위해 전체 패키지를 GDAL 라이브러리라고 부를 것입니다.

GDAL 프로젝트가 (예전에는 이벤 루올(Even Rouault)이) SWIG(Simplified Wrapper and Interface Generator)이 생성한 GDAL 및 OGR 용 파이썬 바인딩을 유지/관리합니다. 일반적으로, 클래스 및 메소드 대부분은 GDAL과 OGR의 대응하는 C++ 클래스와 일치합니다. 파이썬 특화 참조 문서는 존재하지 않지만, :ref:`예제 <tutorials>` 문서에 파이썬 예시가 포함되어 있습니다.

예제
---------

크리스 개러드(Chris Garrard)가 유타 주립 대학교에서 `"오픈소스 GIS를 이용한 파이썬 지리 정보 처리(Geoprocessing with Python using Open Source GIS)" <https://www.gis.usu.edu/~chrisg/python/>`_) 를 강의했습니다. 파이썬 GDAL/OGR 초심자에게 굉장히 도움이 될 수 있는 슬라이드, 예제, 테스트 데이터 및 과제가 많이 있습니다.

`http://pcjericks.github.io/py-gdalogr-cookbook/index.html <http://pcjericks.github.io/py-gdalogr-cookbook/index.html>`_ 웹사이트는 파이썬 GDAL/OGR 바인딩을 이용하기 위한 레시피를 가득 담고 있는 쿡북입니다.

예시
--------

-  `https://github.com/OSGeo/gdal/tree/master/swig/python/gdal-utils/osgeo_utils/samples <https://github.com/OSGeo/gdal/tree/master/swig/python/gdal-utils/osgeo_utils/samples>`_ 에서 다른 예시 모음을 볼 수 있으며, 그 중 몇몇은 :ref:`python_samples` 문서에서 설명하고 있습니다.
-  여러 `GDAL 유틸리티 <https://github.com/OSGeo/gdal/tree/master/swig/python/gdal-utils/osgeo_utils/>`_ 가 파이썬으로 구현되었으며 유용한 예시가 될 수 있습니다.
-  The majority of GDAL regression tests are written in Python. They are available at
  `https://github.com/OSGeo/gdal/tree/master/autotest <https://github.com/OSGeo/gdal/tree/master/autotest>`_
-  다음 스크립트에서 몇몇 GDAL/NumPy 통합의 예시를 찾아볼 수 있습니다:

   -  :ref:`gdal_calc.py`
   -  :ref:`val_repl.py`
   -  :ref:`gdal_merge.py`
   -  :ref:`gdal2tiles.py`
   -  :ref:`gdal2xyz.py`
   -  :ref:`pct2rgb.py`
   -  :ref:`gdallocationinfo.py`

`Gotcha <https://en.wikipedia.org/wiki/Gotcha_(programming)>`_
---------

GDAL의 그리고 OGR의 파이썬 바인딩이 기저 C++ 코드를 감싸는 꽤 "파이썬적인" 래퍼(wrapper)를 제공하긴 하지만, 이 파이썬 바인딩이 전형적인 파이썬 라이브러리와 다른 점이 몇 가지 있습니다.
파이썬 프로그래머에게 이런 차이점들이 예상치 못 하게 다가와 예상하지 못 한 결과로 이어질 수 있습니다. 이런 차이점들은 수명이 긴 대용량 라이브러리를 개발하면서 하위 호환성을 계속 유지하려 하는 과정에서 나타납니다. 시간이 지나면서 이런 차이점들이 수정되고 있지만, 모두 사라지기 전까지는 다음 :ref:`python_gotchas` 목록을 살펴보십시오.

의존성
------

   -  libgdal(3.2.0 이상 버전) 및 헤더 파일들(gdal-devel)
   -  NumPy(1.0.0 이상 버전) 및 헤더 파일들(numpy-devel) (반드시 필요한 것은 아니지만, 이게 없다면 많은 예시 및 유틸리티가 동작하지 않을 것입니다.)

설치
----

유닉스
~~~~~~

GDAL 파이썬 바인딩은 "distutils" 및 "setuptools" 패키지를 둘 다 지원합니다. 이 중에서 "setuptools" 사용을 권장합니다. "setuptools"를 가져올 수 있는 경우, 기본적으로 설정 프로그램(setup)이 이 패키지를 이용해서 에그(배포용 압축 파일)를 작성할 것입니다. "setuptools"를 가져올 수 없다면 단순 "distutils"이 루트에 GDAL 패키지를 (NumPy 의존성 연결 없이) 설치할 것입니다.

easy_install
~~~~~~~~~~~~

파이썬 CheeseShop으로부터 GDAL을 설치할 수 있습니다:

.. code-block:: Bash

    $ sudo easy_install GDAL

사용자가 지정한 플랫폼과 파이썬 버전을 위한 에그가 없기 때문에 easy_install이 소스 빌드를 할 거라고 예상되는 경우, libgdal 및 그 개발 헤더들이 설치되어 있어야 할 수도 있습니다.

setup.py
~~~~~~~~

"setup.py" 스크립트의 중요한 변수들은 "setup.cfg" 파일로 제어됩니다. "setup.cfg" 파일에서 포인터가 파일 및 라이브러리를 포함하도록 수정할 수 있습니다. 수정해야 할 가장 중요한 옵션은 'gdal_config' 파라미터입니다. 패키지로부터 GDAL을 설치한 경우, 이 프로그램의 위치는 대부분의 경우 ``/usr/bin/gdal-config`` 이지만 사용자 패키지 관리자가 어떻게 작동했느냐에 따라 다른 위치에 있을 수도 있습니다.

'gdal-config'의 위치를 수정한 다음, "setup.py" 스크립트로 빌드하고 설치할 수 있습니다:

.. code-block:: Bash

    $ python setup.py build
    $ python setup.py install

"setuptools" 패키지를 설치한 경우, 에그도 생성할 수 있습니다:

.. code-block:: Bash

    $ python setup.py bdist_egg

GDAL 라이브러리 소스 트리의 일부분으로 빌드하기
------------------------------------------------

사용자의 환경설정 줄에 '--with-python'을 지정하면 GDAL 파이썬 바인딩을 소스 빌드의 일부분으로도 빌드할 수 있습니다:

.. code-block:: Bash

    $ ./configure --with-python

설치를 완료하려면 일반적인 'make' 및 'make install' 명령어를 사용하십시오:

.. code-block:: Bash

    $ make
    $ make install

.. note::

    ``./configure`` 는 지정된 파이썬 바이너리의 트리에 (또는 실행 경로에) "setuptools"가 설치되어 있는지 탐지하려 시도해서, 탐지되는 경우 기본적으로 에그 빌드를 사용할 것입니다. "distutils"만 사용해서 설치해야 하는 경우 "setup.py" 스크립트의 HAVE_SETUPTOOLS 변수가 궁극적으로 False로 설정되도록 편집한 다음 일반적인 ``python setup.py install`` 명령어를 실행하십시오.

윈도우
~~~~~~~

윈도우 상에 GDAL 파이썬 바인딩 설치를 완료하려면 다음 항목이 필요할 것입니다:

-  `GDAL 윈도우 바이너리 <http://download.osgeo.org/gdal/win32/1.6/>`_:
   기본 설치는 "gdalwin32exe160.zip" 배포 파일을 요구합니다. 이 디렉터리에 있는 다른 파일들은 선택적인 다양한 플러그인 및 개발 헤더/인클루드 파일들을 위한 것입니다. ZIP 압축 파일을 다운로드한 다음, 사용자가 선택한 디렉터리에 압축 해제하십시오.

"README_EXE.txt" 파일에 설명된 대로, GDAL 바이너리를 압축 해제한 다음 사용자의 시스템 경로 및 변수들을 수정해야 할 것입니다. 어떻게 해야 할지 잘 모르겠다면 `마이크로소프트 지식 기반 문서 <http://support.microsoft.com/kb/310519>`_ 를 읽어보십시오.

1. 사용자 시스템 PATH에 설치 디렉터리 "bin" 폴더를 추가하십시오. 새 경로를 추가하기 전에 기존 경로 뒤에 쌍반점을 입력해야 한다는 사실을 기억하십시오:

.. code-block:: bat

    C:\gdalwin32-1.7\bin

2. 사용자 설치 디렉터리의 "data" 폴더로 새 사용자 및 시스템 변수를 생성하십시오:

.. code-block:: bat

    Name : GDAL_DATA
    Path : C:\gdalwin32-1.7\data

사용자 설치가 제대로 되었는지 테스트해보려면 `사용례 <https://trac.osgeo.org/gdal/wiki/GdalOgrInPython#usage>`_ 단락으로 건너뛰십시오. 리부트해야 할 수도 있다는 사실을 기억하십시오.

SWIG
----

GDAL 파이썬 패키지는 `SWIG <https://www.swig.org/>`_ 을 이용해서 빌드됩니다. 래퍼(wrapper) 코드 생성을 지원하는 최초 `SWIG <https://www.swig.org/>`_ 버전은 1.3.40입니다. 1.3.40 이전 버전으로 사용 가능한 바인딩을 빌드할 수는 있지만, 1.3.40 미만 버전을 대상으로는 어떤 개발도 진행되고 있지 않습니다. 바인딩 코드를 생성하기 위해 사용자 개발 트리에서 SWIG을 실행할 필요는 없습니다. 일반적으로 소스에 포함되어 있기 때문입니다. 하지만 재생성해야 하는 경우 ``./swig/python`` 디렉터리 안에서 다음 'make' 명령어를 실행하면 됩니다:

.. code-block:: Bash

    $ make generate

바인딩을 모두 재생성하도록 보장하려면, 'generate' 명령어를 실행하기 전에 바인딩 코드를 삭제하면 됩니다:

.. code-block:: Bash

    $ make veryclean

사용례
------

가져오기
~~~~~~~~

`GDAL <https://gdal.org/>`_ 파이썬 바인딩에 포함된 주요 모듈 5개가 있습니다:

.. code-block:: python

    >>> from osgeo import gdal
    >>> from osgeo import ogr
    >>> from osgeo import osr
    >>> from osgeo import gdal_array
    >>> from osgeo import gdalconst

뿐만 아니라 퇴출되었으며 곧 없어질 예정이라는 경고를 띄우는 호환성 모듈도 5개가 있습니다. GDAL 1.7 바인딩을 사용하는 경우 앞의 주요 모듈을 사용하기 위해 사용자의 가져오기를 업데이트해야 하지만, 다음 호환성 모듈도 GDAL 3.1버전까지는 작동할 것입니다:

.. code-block:: python

    >>> import gdal
    >>> import ogr
    >>> import osr
    >>> import gdalnumeric
    >>> import gdalconst

사용자가 전체 수준 모듈을 가져오는 예전 코드를 가지고 있기 때문에 구식 가져오기를 계속 지원해야 하는 경우 단순한 ``try ... except`` 가져오기를 사용하면 퇴출 경고를 띄우지 않고 모듈 이름을 본질적으로 예전과 동일하게 유지할 수 있습니다:

.. code-block:: python

    >>> try:
    ...     from osgeo import gdal
    ... except ImportError:
    ...     import gdal

닥스트링
~~~~~~~~~~

현재, OGR 모듈만 C/C++ API 독시젠(Doxygen) 자료로부터 생성된 파이썬 닥스트링(docstring)을 가지고 있습니다. 몇몇 인자 및 유형이 파이썬의 인자 및 유형과 정확하게 일치하지 않을 수도 있지만, 시작하기에는 충분할 것입니다. GDAL 및 OGR 용 닥스트링은 향후 배포될 예정입니다.

Numpy
-----

GDAL 파이썬 바인딩의 고급 기능 가운데 다른 언어 바인딩에서는 찾아볼 수 없는 고급 기능 하나는 파이썬 숫자형 배열 기능과의 통합입니다. ``gdal.Dataset.ReadAsArray()`` 메소드를 사용하면, 래스터 데이터를 파이썬 숫자형 배열 케이퍼빌리티에서 사용될 준비가 된 숫자형 배열로 읽어올 수 있습니다.

시간이 흐르면서 이 기능은 조금 진화했습니다. 예전에는 패키지가 "Numeric"이라고 알려져 있었으며 ``import Numeric`` 명령어로 가져왔습니다. 새로운 세대의 패키지는 ``import numpy`` 명령어로 가져옵니다. 현재 구세대 바인딩은 예전 "Numeric" 패키지만 지원하며, 신세대 바인딩은 신세대 "numpy" 패키지만 지원합니다. 대부분의 경우 서로 호환되며, "gdalnumeric"을 (또는 "osgeo.gdal_array"를) 가져오면 현재 바인딩 유형에 적절한 패키지를 얻을 것입니다.

예시
~~~~

`val_repl.py <https://github.com/OSGeo/gdal/blob/master/swig/python/gdal-utils/osgeo_utils/samples/val_repl.py>`_ 스크립트에서 GDAL/NumPy 통합의 예시를 하나 찾아볼 수 있습니다.

.. note::
   **성능 메모**

   ``gdal.Dataset.ReadAsArray()`` 메소드는 데이터가 함수 호출의 일부분으로 명확하게 부분 집합 지정되지 않은 이상 래스터 밴드 또는 데이터셋 전체를 복사할 것입니다. 대용량 데이터의 경우 이런 접근법은 엄청나게 메모리 집약적일 것으로 예상됩니다.

.. _GDAL API 예제: https://gdal.org/tutorials/
.. _GDAL 윈도우 바이너리: http://gisinternals.com/sdk/
.. _마이크로소프트 지식 기반 문서: http://support.microsoft.com/kb/310519
.. _파이썬 Cheeseshop: http://pypi.python.org/pypi/GDAL/
.. _val_repl.py: http://trac.osgeo.org/gdal/browser/trunk/gdal/swig/python/gdal-utils/osgeo_utils/samples/val_repl.py
.. _GDAL: http://www.gdal.org
.. _SWIG: http://www.swig.org

