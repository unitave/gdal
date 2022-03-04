.. _gdal_calc:

================================================================================
gdal_calc.py
================================================================================

.. only:: html

    넘파이(NumPy) 문법을 사용하는 명령줄 래스터 계산기입니다.

.. Index:: gdal_calc

개요
--------

.. code-block::

    gdal_calc.py --calc=expression --outfile=out_filename [-A filename]
                 [--A_band=n] [-B...-Z filename] [other_options]


설명
-----------

# .. rubric::  DESCRIPTION
#   :name: description

넘파이(NumPy) 문법을 사용하는 명령줄 래스터 계산기입니다. 넘파이 배열이 지원하는 ``>`` 같은 논리 연산자와 함께 ``+``, ``-``, ``*``, 그리고 ``\`` 같은 기본 산술을 사용합니다. 모든 파일이 (extent 옵션을 사용하는 경우를 제외하면) 동일한 차원을 가지고 있어야만 하지만, (projectionCheck 옵션을 사용하는 경우를 제외하면) 투영법을 확인하지는 않는다는 사실을 기억하십시오.

.. option:: --help

    도움말 메시지를 표시하고 엑시트합니다.

.. option:: -h

    :option:`--help` 옵션과 동일합니다.

.. option:: --calc=expression

    ``+``, ``-``, ``/``, ``*``, 또는 (``log10()`` 같은) 모든 넘파이 배열 함수를 사용하는 넘파이 문법으로 계산합니다. 다중 밴드 파일을 생산하려면 ``--calc`` 옵션 여러 개의 목록을 사용하면 됩니다. (GDAL 3.2버전 이상)

.. option:: -A <filename>

    입력 GDAL 래스터 파일로, 어떤 문자든 (a-z, A-Z) 사용할 수 있습니다. (GDAL 3.3버전부터 소문자를 지원합니다.)

    한 문자가 반복될 수도 있고, 또는 (공백으로 구분된) 값 몇 개를 지정할 수도 있습니다. (GDAL 3.3버전 이상) GDAL 3.5버전부터, 모든 셸/플랫폼에서 (?, \*를 사용하는) 와일드카드 예외를 지원합니다. 이로써 3차원 넘파이 배열을 생성할 수 있습니다. 이런 경우, 계산 공식이 3차원 배열을 입력받아 2차원 배열을 반환해야만 합니다. (예시를 참조하십시오.) 계산 결과 2차원 배열을 반환하지 않는 경우 오류를 선언할 것입니다.

.. option:: --A_band=<n>

    파일 A의 래스터 밴드 개수. (기본값은 1)

.. option::  --outfile=<filename>

    생성하거나 채울 산출 파일.

.. option:: --NoDataValue=<value>

    산출 NODATA 값입니다. (기본 데이터 유형 특화 값) NODATA 값을 설정하지 않으려면 --NoDataValue=none 을 이용하십시오. (GDAL 3.3버전 이상)

    .. note::
        파이썬 API를 사용하는 경우:
        ``None`` 값이 기본 데이터 유형 특화 값을 나타내고, ``'none'`` 값은 NODATA 값을 설정하지 않는다는 것을 나타낼 것입니다.

.. option:: --hideNoData

    .. versionadded:: 3.3

    입력 밴드의 NODATA 값을 무시합니다. 기본적으로, 입력 밴드의 NODATA 값은 계산에 들어가지 않습니다. 이 옵션을 설정하면 입력 NODATA 값에 어떤 특별한 처리도 하지 않을 것입니다. 또한 다른 모든 값과 마찬가지로 계산에 들어가게 될 것입니다. 사용자가 --NoDataValue=<value>를 설정해서 NODATA 값을 특정한 값으로 명확하게 지정하지 않는 이상, 산출물은 설정된 NODATA 값을 가지지 않을 것입니다.

.. option:: --type=<datatype>

    산출물의 데이터 유형입니다. [``Int32``, ``Int16``, ``Float64``, ``UInt16``, ``Byte``, ``UInt32``, ``Float32``] 가운데 하나여야만 합니다.

    .. note::

       ``--type`` 을 사용해서 데이터 유형을 설정한다고 해도, 동일한 유형의 피연산자를 사용하는 중간(intermediate) 산술 연산을 하는 경우 연산 결과는 원본 데이터 유형을 따를 것입니다. 따라서 예기치 못 한 최종 결과물이 나올 수도 있습니다.

.. option:: --format=<gdal_format>

    산출 파일 용 GDAL 포맷입니다.

.. option:: color-table=<filename>

    산출 래스터에 사용될 (색상표 색인 해석을 가진) 색상표(또는 ColorTable 객체)의 파일명을 지정할 수 있게 해줍니다. 지원 포맷: (예를 들어 gdaldem에서와 비슷하지만 색상 이름을 지원하지 않는) txt, qlr, (예를 들면 QGIS로부터 내보낸) qml

.. option:: --extent=<option>

    .. versionadded:: 3.3

    이 옵션은 서로 다른 범위를 가진 래스터들을 처리하는 방법을 결정합니다. 이 옵션은 사용자 지정 범위를 지정하기 위해 쓰이는 `projwin` 옵션과 함께 사용할 수 없습니다. 다음에 나오는 모든 옵션에 대해 모든 입력 래스터의 픽셀 크기(해상도)와 공간 좌표계가 동일해야만 합니다.

    - ``ignore`` (기본값) - 래스터의 차원만 비교합니다. 차원이 일치하지 않는 경우 연산이 실패할 것입니다.
    - ``fail`` - 래스터의 차원 및 범위(경계)가 일치해야만 합니다. 그렇지 않는 경우 연산이 실패할 것입니다.
    - ``union`` - 산출물의 범위(경계)가 모든 입력물의 범위를 담고 있는 최소 직사각형이 될 것입니다.
    - ``intersect`` - 산출물의 범위(경계)가 모든 입력물의 범위 안에 포함되는 최대 직사각형이 될 것입니다.

.. option:: --projwin <ulx> <uly> <lrx> <lry>

    .. versionadded:: 3.3

    이 옵션은 산출물을 위한 사용자 지정 범위를 설정합니다. 이 옵션은 `extent` 옵션과 함께 사용할 수 없습니다.

.. option:: --projectionCheck

    .. versionadded:: 3.3

    기본적으로 어떤 투영법 확인도 하지 않지만, 이 옵션을 설정하면 모든 밴드의 투영법이 동일하지 않은 경우 연산이 실패할 것입니다.

.. _creation-option:

.. option:: --creation-option=<option>

    산출 포맷 드라이버에 생성 옵션을 전송(pass)합니다. :option:`-co` 옵션 여러 개를 목록화할 수도 있습니다. 각 포맷을 위한 정당한 생성 옵션을 알고 싶다면 :ref:`raster_drivers` 포맷 사양 문서를 읽어보십시오.

.. option:: --co=<option>

    creation-option_ 과 동일합니다.

.. option:: --allBands=[a-z, A-Z]

    입력 래스터(a-z, A-Z)의 모든 밴드를 처리합니다. 모든 밴드에 대해 --calc 옵션이 하나씩 필요합니다.

.. option:: --overwrite

    산출물 파일이 이미 존재하는 경우 덮어씁니다. 이때 덮어쓰기란 파일을 삭제한 다음 처음부터 다시 생성한다는 의미라는 것을 이해해야만 합니다. 이 옵션을 지정하지 *않았는데* 산출물 파일이 이미 존재한다면, 제자리(in place) 업데이트될 것입니다.

.. option:: --debug

    디버그 정보를 출력합니다.

.. option:: --quiet

    진행 상황 메시지를 출력하지 않습니다.


파이썬 옵션
--------------

.. versionadded:: 3.3

gdal_calc 계산기의 파이썬 인터페이스 기능을 사용하면 다음 옵션을 사용할 수 있습니다. 명령 프롬프트에서는 사용할 수 없습니다.

.. option:: user_namespace

    Calc 표현식에서 사용하기 위해 쓸 수 있는 사용자 지정 함수 또는 기타 이름들의 목록(dictionary)입니다.

.. option:: return_ds

    이 옵션을 활성화하면, 함수로부터 산출 데이터셋을 반환받은 다음에도 인터페이스가 종료되지 않을 것입니다.

.. option:: color_table

    산출 래스터에 사용될 (색상표 색인 해석을 가진) ColorTable 객체를 지정할 수 있게 해줍니다.

예시
-------

파일 2개를 함께 추가합니다:

.. code-block::

    gdal_calc.py -A input1.tif -B input2.tif --outfile=result.tif --calc="A+B"

레이어 2개의 평균을 계산합니다:

.. code-block::

    gdal_calc.py -A input1.tif -B input2.tif --outfile=result.tif --calc="(A+B)/2"

.. note::

   이전 예시에서 A 및 B 입력물이 동일한, 예를 들어 정수 데이터 유형인 경우, 나누기 연산을 하기 전에 피연산자 가운데 하나를 강제로 변환해야 할 수도 있습니다.

   .. code-block::

      gdal_calc.py -A input.tif -B input2.tif --outfile=result.tif --calc="(A.astype(numpy.float64) + B) / 2"

파일 3개를 함께 추가합니다(옵션 2개로 동일한 결과물):

.. code-block::

    gdal_calc.py -A input1.tif -B input2.tif -C input3.tif --outfile=result.tif --calc="A+B+C"

.. versionadded:: 3.3

.. code-block::

    gdal_calc.py -A input1.tif -A input2.tif -A input3.tif --outfile=result.tif --calc="numpy.sum(A,axis=0)".

레이어 3개의 평균을 계산합니다(옵션 2개로 동일한 결과물):

.. code-block::

    gdal_calc.py -A input1.tif -B input2.tif -C input3.tif --outfile=result.tif --calc="(A+B+C)/3"

.. versionadded:: 3.3

.. code-block::

    gdal_calc.py -A input1.tif input2.tif input3.tif --outfile=result.tif --calc="numpy.average(a,axis=0)".

레이어 3개의 최대값을 구합니다(옵션 2개로 동일한 결과물):

.. code-block::

    gdal_calc.py -A input1.tif -B input2.tif -C input3.tif --outfile=result.tif --calc="numpy.max((A,B,C),axis=0)"

.. versionadded:: 3.3

.. code-block::

    gdal_calc.py -A input1.tif input2.tif input3.tif --outfile=result.tif --calc="numpy.max(A,axis=0)"

0 이하의 값을 NULL로 설정합니다:

.. code-block::

    gdal_calc.py -A input.tif --outfile=result.tif --calc="A*(A>0)" --NoDataValue=0

논리 연산자를 사용해서 입력물에서 나온 값들의 범위를 유지합니다:

.. code-block::

    gdal_calc.py -A input.tif --outfile=result.tif --calc="A*logical_and(A>100,A<150)"

다중 밴드를 작업합니다:

.. code-block::

    gdal_calc.py -A input.tif --A_band=1 -B input.tif --B_band=2 --outfile=result.tif --calc="(A+B)/2" --calc="B*logical_and(A>100,A<150)"
