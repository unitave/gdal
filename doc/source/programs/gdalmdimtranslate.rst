.. _gdalmdimtranslate:

================================================================================
gdalmdimtranslate
================================================================================

.. only:: html

    .. versionadded:: 3.1

    다중차원 데이터를 서로 다른 포맷으로 변환하고, 
    Converts multidimensional data between different formats, and perform subsetting.

.. Index:: gdalmdimtranslate

개요
--------

.. code-block::

    gdalmdimtranslate [--help-general] [-co "NAME=VALUE"]*
                      [-of format] [-array <array_spec>]*
                      [-group <group_spec>]*
                      [-subset <subset_spec>]*
                      [-scaleaxes <scaleaxes_spec>]*
                      [-oo NAME=VALUE]*
                      <src_filename> <dst_filename>


설명
-----------

:program:`gdalmdimtranslate` 프로그램은 다중차원 래스터를 서로 다른 포맷으로 변환하고, 그리고/또는 특정 배열 및 그룹들의 선별적인 변환을 수행할 수 있고, 그리고/또는 하위 집합 작업(subsetting operation)을 수행할 수 있습니다.

다음 명령줄 파라미터들은 어떤 순서로도 사용할 수 있습니다:

.. program:: gdalmdimtranslate

.. option:: -of <format>

    산출물 포맷을 선택합니다. (:ref:`raster.netcdf`, :ref:`vrt_multidimensional` 처럼) 다중차원 산출물을 지원하는 포맷일 수도 있고, 또는 달리 지정한 변환 작업의 결과물이 단일 2차원 배열 1개뿐인 경우 "대표적인" 2차원 포맷일 수도 있습니다. 이 옵션을 지정하지 않는 경우, 대상 파일명의 확장자를 사용할 수 있다면 확장자로부터 포맷을 추정합니다.

.. option:: -co <NAME=VALUE>

    많은 포맷들이 생성된 파일에 대한 특정 요소들을 제어하기 위해 사용할 수 있는 선택적인 생성 옵션을 하나 이상 가지고 있습니다.

    포맷 드라이버에 따라 사용할 수 있는 생성 옵션이 다양하며, 몇몇 단순 포맷들의 경우 어떤 생성 옵션도 가지고 있지 않기도 합니다. 어떤 포맷이 어떤 옵션을 지원하는지에 대한 목록은 :ref:`--formats <raster_common_options_formats>` 명령줄 옵션으로 볼 수 있지만, 해당 포맷에 대한 문서야말로 드라이버 생성 옵션 관련 최종 정보 소스입니다. 각 포맷의 정당한 생성 옵션에 대해 알고 싶다면 :ref:`raster_drivers` 포맷 특화 문서를 읽어보십시오.

    배열 수준의 생성 옵션에 ``ARRAY:`` 라는 접두어를 추가하면 옵션을 전송할 수도 있습니다. 이런 옵션들에 대해 더 자세히 알고 싶다면 :cpp:func:`GDALGroup::CopyFrom` 을 읽어보십시오.

.. option:: -array <array_spec>

    데이터셋 전체를 변환하는 대신, 배열 하나를 선택해서 작업을 수행할 수 있습니다. 서로 다른 배열들을 작업하려면 이 옵션을 여러 번 지정하면 됩니다.

    <array_spec>은 어쩌면 완전히 검증된 문법을 사용하는, 배열 이름일 뿐일 수도 있고 (/group/subgroup/array_name) 또는 다음과 같은 문법을 사용하는 옵션들의 조합일 수도 있습니다: name={src_array_name}[,dstname={dst_array_name}][,transpose=[{axis1},{axis2},...][,view={view_expr}]

    [{axis1},{axis2},...]는 :cpp:func:`GDALMDArray::Transpose` 함수의 인자입니다. 예를 들면, transpose=[1,0] 인자는 2차원 배열의 축 순서를 바꿉니다.

    {view_expr}는 :cpp:func:`GDALMDArray::GetView` 함수의 *viewExpr* 인자의 값입니다.

    차원에 대해 분할(slice) 또는 하위 집합 작업을 수행하는 view_expr를 지정하는 경우, 대응하는 색인 작업 변수에 그에 상당한 작업을 적용할 것입니다.

.. option:: -group <group_spec>

    데이터셋 전체를 변환하는 대신, 그룹 하나를 선택해서 작업을 수행할 수 있습니다. 서로 다른 그룹들을 작업하려면 이 옵션을 여러 번 지정하면 됩니다. 그룹 하나만 지정하는 경우, 대상 루트(root) 그룹에 지정한 그룹의 내용을 직접 복사할 것입니다. 그룹 여러 개를 지정하면, 대상 루트 그룹 아래로 복사합니다.

    <group_spec>은 어쩌면 완전히 검증된 문법을 사용하는, 배열 이름일 뿐일 수도 있고 (/group/subgroup/subsubgroup_name) 또는 다음과 같은 문법을 사용하는 옵션들의 조합일 수도 있습니다: name={src_group_name}[,dstname={dst_group_name}][,recursive=no]

.. option:: -subset <subset_spec>

    차원을 따라 하위 집합(다듬기(trim) 또는 분할(slice)) 작업을 수행합니다. 이때 숫자 또는 문자열 데이터 유형인 1차원 변수가 이 차원을 색인 작업하고 그 값들을 단조롭게(monotonically) 정렬했을 거라고 가정합니다. <subset_spec>은 하위 집합 작업 시 `OGC WCS 2.0 KVP 인코딩 <https://portal.opengeospatial.org/files/09-147r3>`_ 문법을 정확하게 따릅니다.

    이 문법이란 dim_name(min_val,max_val) 또는 dim_name(sliced_val)입니다. 전자의 문법은 dim_name 차원의 [min_val,max_val] 범위에 있는 값들로 하위 집합을 생성할 것입니다. 후자의 문법은 dim_name 차원을 sliced_val 값에서 분할할 것입니다. (그리고 이 차원을 참조하는 배열로부터 이 차원을 제거할 것입니다.)

    -array 옵션에서 *view* 를 지정했다면 -subset 옵션을 함께 사용할 수 없습니다.

.. option:: -scaleaxes <scaleaxes_spec>

    차원 하나 또는 여러 개에 (리샘플링하지 않고) 값 N개마다 값 1개를 추출하는 내장(integral) 크기 조정 인자를 적용합니다.

    <scaleaxes_spec>은 `OGC WCS 2.0 크기 조정 확장 프로그램 <https://portal.opengeospatial.org/files/12-039>`_ 의 SCALEAXES 파라미터의 KVP 인코딩 문법을 정확하게 따르지만, 정수형 크기 조정 인자에만 국한됩니다.

    이 문법이란 dim1_name(scale_factor)[,dim2_name(scale_factor)]*입니다.

    -array 옵션에서 *view* 를 지정했다면 -scaleaxes 옵션을 함께 사용할 수 없습니다.

.. option:: -oo <NAME=VALUE>

    .. versionadded:: 3.4

    소스 데이터셋 열기 옵션 (특정 포맷 지원)

.. option:: <src_dataset>

    소스 데이터셋의 이름입니다.

.. option:: <dst_dataset>

    대상 파일의 이름입니다.

C API
-----

C에서 :cpp:func:`GDALMultiDimTranslate` 로도 이 유틸리티를 호출할 수 있습니다.

예시
--------

- netCDF 파일을 다중차원 VRT 파일로 변환

.. code-block::

    $ gdalmdimtranslate in.nc out.vrt

- 시간, Y, X 배열을 2차원 분할해서 추출

.. code-block::

    $ gdalmdimtranslate in.nc out.tif -subset 'time("2010-01-01")' -array temperature

- X 및 Y 축을 따라 하위 집합 샘플링

.. code-block::

    $ gdalmdimtranslate in.nc out.nc -scaleaxes "X(2),Y(2)"

- 시간, Y, X 배열의 값들을 Y축을 따라 하향(top-to-bottom)에서 상향(bottom-to-top)으로 (또는 그 반대로) 재배열

.. code-block::

    $ gdalmdimtranslate in.nc out.nc -array "name=temperature,view=[:,::-1,:]"

- X, Y, 시간 차원을 가진 배열의 순서를 시간, Y, X로 뒤바꾸기(transpose)

.. code-block::

    $ gdalmdimtranslate in.nc out.nc -array "name=temperature,transpose=[2,1,0]"
