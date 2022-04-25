.. _multidim_raster_data_model:

================================================================================
다중차원 래스터 데이터 모델
================================================================================

이 문서에서는 GDAL 3.1버전에서 추가된 GDAL 다중차원 데이터 모델을 설명하려 합니다. GDAL 다중차원 데이터 저장소가 담을 수 있는 정보의 유형 및 그 의미를 서술합니다.

다중차원 래스터 API는 3차원, 4차원 또는 그 이상의 차원 데이터셋을 처리하기 위해 전통적인 :ref:`raster_data_model` 을 일반화한 것입니다. 현재 기본적인 읽기/쓰기 API로 제한되어 있으며, 다른 고급 수준 유틸리티의 플러그인으로 제대로 구현되지 않았습니다.

이 모델은 netCDF 및 HDF5의 API와 데이터 모델로부터 크게 영향을 받았습니다. `HDF5 포맷 및 데이터 모델 <https://portal.opengeospatial.org/files/81716>`_ 을 참조하십시오.

다중차원 콘텐츠를 가진 :cpp:class:`GDALDataset` 클래스는 루트 :cpp:class:`GDALGroup` 클래스를 담고 있습니다.

그룹
-----

(`HDF5 그룹 <https://portal.opengeospatial.org/files/81716#_hdf5_group>`_ 을 모델링한) :cpp:class:`GDALGroup` 클래스는 GDALAttribute, GDALMDArray 또는 다른 GDALGroup의 명명 컨테이너입니다. 즉 GDALGroup이 객체의 계층(hierarchy)을 서술할 수 있습니다.

속성
---------

(`HDF5 속성 <https://portal.opengeospatial.org/files/81716#_hdf5_attribute>`_ 을 모델링한) :cpp:class:`GDALAttribute` 클래스는 이름과 값을 가지며, 일반적으로 메타데이터 항목을 서술하는 데 쓰입니다. (HDF5 포맷의 경우) 이 값은 일반적으로 "모든" 유형의 다중차원 배열이 될 수 있습니다. (대부분의 경우, 문자열 또는 숫자 유형의 단일값일 것입니다.)

다중차원 배열
----------------------

(`HDF5 데이터셋 <https://portal.opengeospatial.org/files/81716#_hdf5_dataset>`_ 을 모델링한) :cpp:class:`GDALMDArray` 클래스는 이름, 다중차원 배열 및 GDALAttribute 목록을 가지며 GDALDimension 여러 개를 참조합니다.

대부분의 드라이버는 차원에 행 우선(row-major) 규범을 사용합니다. 다시 말하자면 메모리에 배열 요소들을 연속해서 저장한다고 할 때, 첫 번째 차원이 가장 느린 가변 차원(2차원 이미지에서의 행)이고 마지막 차원이 가장 빠른 가변 차원(2차원 이미지에서의 열)이라는 뜻입니다. 이 규범이 NumPy 배열, MEM 드라이버와 HDF5 및 netCDF API에 사용되는 기본 규범입니다. :cpp:func:`GDALAbstractMDArray::Read` 및 :cpp:func:`GDALAbstractMDArray::Write` 메소드에 NULL 배열을 'stride' 파라미터로 전송하는 경우를 제외하고, 대부분의 경우 GDAL API는 이 규범을 이해하지 못 하더라도 기능을 수행할 수 있습니다. 
`다중차원 배열 색인 작업 순서 문제점에 관한 NumPy 문서 <https://docs.scipy.org/doc/numpy/reference/internals.html#multidimensional-array-indexing-order-issues>`_ 를 참조하십시오.

GDALMDArray는 선택적인 속성도 가지고 있습니다:

    - 좌표계: :cpp:class:`OGRSpatialReference`
    - NODATA 값
    - 단위
    - 오프셋: ``unscaled_value = offset + scale * raw_value``
    - 척도: ``unscaled_value = offset + scale * raw_value``

배열에 :cpp:func:`GDALMDArray::Transpose()`, :cpp:func:`GDALMDArray::GetView()` 등등의 여러 작업을 적용해서 배열의 수정된 뷰를 얻을 수 있습니다.

:cpp:func:`GDALMDArray::Cache()` 메소드를 사용해서 사이드카 파일에 뷰 배열의 값을 캐시할 수 있습니다.

차원
---------

:cpp:class:`GDALDimension` 클래스는 다중차원 배열을 색인하기 위해 사용되는 차원/축을 서술합니다. 이 클래스는 다음 속성들을 가집니다:

  - 이름

  - 크기:
    차원을 따라 색인할 수 있는 값의 개수입니다.

  - 유형:
    차원의 본질을 나타내는 문자열로, HORIZONTAL_X, HORIZONTAL_Y, VERTICAL, TEMPORAL, 그리고 PARAMETRIC 값이 사전 정의되어 있습니다. 다른 값을 사용할 수도 있습니다. 비어 있는 값은 알 수 없다는 의미입니다.

  - 방향:
    EAST, WEST, SOUTH, NORTH, UP, DOWN, FUTURE, 그리고 PAST 값이 사전 정의되어 있습니다. 다른 값을 사용할 수도 있습니다. 비어 있는 값은 알 수 없다는 의미입니다.

  - 참조:
    차원이 취하는 값을 설명하는, 일반적으로 1차원인 GDALMDArray를 가리킵니다. 지리참조된 GDALMDArray와 그 X 차원의 경우, 일반적으로 각 그리드 포인트에 대한 편동/경도의 값일 것입니다.

데이터 유형
---------

(`HDF5 데이터 유형 <https://portal.opengeospatial.org/files/81716#_hdf5_datatype>`_ 을 모델링한) :cpp:class:`GDALExtendedDataType` 클래스는 GDALAttribute 또는 GDALMDArray의 개별 값이 취하는 유형을 서술합니다. NUMERIC, STRING 또는 COMPOUND 클래스 가운데 하나일 수 있습니다.
NUMERIC 클래스의 경우, 기존 :cpp:enum:`GDALDataType` 값들의 목록을 지원합니다.
COMPOUND 클래스의 데이터 유형은 복합 구조(compound structure) 및 GDALExtendedDataType에 있는 바이트 단위 오프셋인 각 멤버를 이름으로 설명하는 멤버 목록입니다.

.. note::

   HDF5 모델화는 더 복잡한 데이터 유형을 사용할 수 있게 해줍니다.

.. note::

   HDF5는 복소수형 값에 대한 네이티브 데이터 유형을 가지고 있지 않은 반면 GDALDataType은 가지고 있습니다. 따라서 드라이버가 복소수 값을 표현하는 HDF5 복합 데이터 유형으로부터 GDT\_Cxxxx 데이터유형을 노출시키도록 결정할 수도 있습니다.

GDAL 2차원 래스터 데이터 모델과의 차이점
----------------------------------------------

- 다중차원 데이터에 대해 GDALRasterBand 개념을 더 이상 사용하지 않습니다. 다른 GDALMDArray로 모델링하거나, 또는 복합 데이터 유형을 사용해서 모델링할 수 있습니다.

전통적인 GDAL 2차원 래스터 데이터 모델과 다중차원 데이터 모델 사이의 가교
---------------------------------------------------------------------------------

:cpp:func:`GDALRasterBand::AsMDArray` 및 :cpp:func:`GDALMDArray::AsClassicDataset` 함수를 사용해서 각각 래스터 밴드를 다중차원 배열로 또는 2차원 데이터셋을 다중차원 배열로 변환할 수 있습니다.

응용 프로그램
---------------------------------------------------------------------------------

다음 응용 프로그램들을 사용해서 다중차원 데이터셋을 조사하고 조정할 수 있습니다:

- :ref:`gdalmdiminfo`
- :ref:`gdalmdimtranslate`

