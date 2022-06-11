.. _rfc-75:

================================================================================
RFC 75: 다중차원 배열
================================================================================

============ ==========================
저자:        이벤 루올
연락처:      even.rouault@spatialys.com
제안일:      2019년 5월 24일
최신 수정일: 2019년 7월 22일
상태:        승인, GDAL 3.1버전에 구현
============ ==========================

요약
----

이 RFC는 GDAL 코어 및 몇몇 선택한 드라이버에 특히 3차원 이상의 다중차원 배열(multidimensional array)을 위한 읽기/쓰기 지원을 추가할 것을 제안합니다.

동기
----

(초입방체(hypercube)라고도 알려진) 다중차원 배열은 점점 더 많이 사용할 수 있게 되고 있는 시공간(spatio-temporal, 2차원 래스터의 시계열) 데이터 또는 수직 시공간(spatio-vertical-temporal, 2차원 + Z 차원 + 시간 차원) 데이터를 모델링하는 방법입니다. 하지만 GDAL의 현재 래스터 모델은 주로 2차원 지향입니다. netCDF, HDF4, HDF5 같은 다수의 드라이버들은 래스터 밴드 또는 하위 데이터셋을 사용해서 본질적으로 2차원을 초과하는 다중차원 데이터셋의 2차원 슬라이스 여러 개를 노출시키는 방법으로 이런 제한을 피해 작동합니다.
이런 다중차원 배열을 그대로 노출시킬 수 있고 이 배열에 대해 슬라이스 및 다듬기(trim) 작업을 수행할 수 있는 제대로 된 API와 드라이버를 지원하는 것이 바람직합니다.

과거에 이미 이 주제에 대한 논의가, 특히 이 `메일링 리스트 스레드 <https://lists.osgeo.org/pipermail/gdal-dev/2017-October/047472.html>`_ 에서 이루어졌습니다.

제안 변경 사항
--------------

GDAL의 기존 래스터 API 가운데 다수가 주로 2차원 지향적입니다. 이런 API와 드라이버 코드가 전부 임의의 N차원을 지원하도록 업그레이드하기보다 -- 이런 작업은 소수의 드라이버들에만 혜택을 주기 위해 엄청난 노력을 들이는 일이 될 것입니다 -- 다중차원 배열을 지원하는 새로운 전용 API를 추가할 것을 제안합니다. 또한 `HDF5 포맷 및 데이터 모델 <https://portal.ogc.org/files/81716>`_ 에서 찾아볼 수 있는 계층 데이터 구조도 지원하고자 합니다. 이 모델은 HDF4, netCDF, GRIB, WCS 같은 다중차원 케이퍼빌리티를 가진 다른 포맷/드라이버의 필요성을 포함할 수 있습니다. 따라서 HDF5 라이브러리 자체의 API가 제안한 API에 커다란 영향을 미치게 될 것입니다.

데이터 모델
~~~~~~~~~~~

`다중차원 래스터 데이터 모델 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/user/multidim_raster_data_model.rst>`_ 에서 이 데이터 모델을 설명하고 있습니다.


C++ API
~~~~~~~

새로운 클래스 및 메소드를 추가할 것입니다. 
`다중차원 배열 API <https://github.com/rouault/gdal/blob/rfc75/gdal/gcore/gdal_priv.h#L1715>`_ 를 참조하십시오.

다중차원 래스터를 지원하는 드라이버에 새로운 드라이버 케이퍼빌리티를 추가할 것입니다:

::

    #define GDAL_DCAP_MULTIDIM_RASTER     "DCAP_MULTIDIM_RASTER"


:cpp:func:`GDALOpenEx` 에 새로운 열기 옵션 ``GDAL_OF_MULTIDIM_RASTER`` 를 추가할 것입니다. 이 옵션을 지정하면, 다중차원 래스터를 지원하는 드라이버가 루트 :cpp:class:`GDALGroup` 을 반환할 것입니다. 지정하지 않으면 이런 드라이버의 일반적인 현재 2차원 모드를 계속 사용할 것입니다.

다중차원 데이터셋, 그룹, 차원, 배열 및 속성 생성 옵션에 새로운 생성 옵션 메타데이터 항목들을 추가합니다:

.. code-block:: c++

    /** 다중차원 데이터셋 생성 옵션을 가진 XML 조각입니다.
    * @since GDAL 3.1
    */
    #define GDAL_DMD_MULTIDIM_DATASET_CREATIONOPTIONLIST "DMD_MULTIDIM_DATASET_CREATIONOPTIONLIST"

    /** 다중차원 그룹 생성 옵션을 가진 XML 조각입니다.
    * @since GDAL 3.1
    */
    #define GDAL_DMD_MULTIDIM_GROUP_CREATIONOPTIONLIST "DMD_MULTIDIM_GROUP_CREATIONOPTIONLIST"

    /** 다중차원 차원 생성 옵션을 가진 XML 조각입니다.
    * @since GDAL 3.1
    */
    #define GDAL_DMD_MULTIDIM_DIMENSION_CREATIONOPTIONLIST "DMD_MULTIDIM_DIMENSION_CREATIONOPTIONLIST"

    /** 다중차원 배열 생성 옵션을 가진 XML 조각입니다.
    * @since GDAL 3.1
    */
    #define GDAL_DMD_MULTIDIM_ARRAY_CREATIONOPTIONLIST "DMD_MULTIDIM_ARRAY_CREATIONOPTIONLIST"

    /** 다중차원 속성 생성 옵션을 가진 XML 조각입니다.
    * @since GDAL 3.1
    */
    #define GDAL_DMD_MULTIDIM_ATTRIBUTE_CREATIONOPTIONLIST "DMD_MULTIDIM_ATTRIBUTE_CREATIONOPTIONLIST"

다음은 netCDF 드라이버의 예시입니다:

.. code-block:: xml

    <MultiDimDatasetCreationOptionList>
    <Option name="FORMAT" type="string-select" default="NC4">
        <Value>NC</Value>
        <Value>NC2</Value>
        <Value>NC4</Value>
        <Value>NC4C</Value>
    </Option>
    <Option name="CONVENTIONS" type="string" default="CF-1.6" description="Value of the Conventions attribute" />
    </MultiDimDatasetCreationOptionList>


    <MultiDimDimensionCreationOptionList>
    <Option name="UNLIMITED" type="boolean" description="Whether the dimension should be unlimited" default="false" />
    </MultiDimDimensionCreationOptionList>


    <MultiDimArrayCreationOptionList>
    <Option name="BLOCKSIZE" type="int" description="Block size in pixels" />
    <Option name="COMPRESS" type="string-select" default="NONE">
        <Value>NONE</Value>
        <Value>DEFLATE</Value>
    </Option>
    <Option name="ZLEVEL" type="int" description="DEFLATE compression level 1-9" default="1" />
    <Option name="NC_TYPE" type="string-select" default="netCDF data type">
        <Value>AUTO</Value>
        <Value>NC_BYTE</Value>
        <Value>NC_INT64</Value>
        <Value>NC_UINT64</Value>
    </Option>
    </MultiDimArrayCreationOptionList>


    <MultiDimAttributeCreationOptionList>
    <Option name="NC_TYPE" type="string-select" default="netCDF data type">
        <Value>AUTO</Value>
        <Value>NC_BYTE</Value>
        <Value>NC_CHAR</Value>
        <Value>NC_INT64</Value>
        <Value>NC_UINT64</Value>
    </Option>
    </MultiDimAttributeCreationOptionList>


C API
~~~~~

모든 C++ 메소드들을 C API에 매핑합니다.
`다중차원 API_api <https://github.com/rouault/gdal/blob/rfc75/gdal/gcore/gdal.h#L1397>`_ 를 참조하십시오.

드라이버 변경 사항
~~~~~~~~~~~~~~~~~~

-  MEM 드라이버에 읽기 및 쓰기 지원을 구현할 것입니다.

-  VRT 드라이버가 다중차원 드라이버로부터 2차원/대표 드라이버로는 물론 다중차원 드라이버로부터 다중차원 드라이버로도 2차원 슬라이스를 추출할 수 있게 변경할 것입니다.

-  netCDF 드라이버에 읽기 및 쓰기 지원을 구현할 것입니다.

-  HDF4 및 HDF5 드라이버에 읽기 지원을 구현할 것입니다.

-  GRIB 드라이버에 (타임스탬프만 다른 GRIB 메시지에 대해 X, Y, 시간 배열을 노출시켜) 읽기 지원을 구현할 것입니다.

새로운 유틸리티
~~~~~~~~~~~~~~~

-  계층 구조 및 콘텐츠를 리포트하는 새 gdalmdiminfo 유틸리티를 추가합니다. 이 유틸리티의 산출물은 JSON 서식입니다.
   `gdalmdiminfo 유틸리티 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/programs/gdalmdiminfo.rst>`_ 문서를 참조하십시오.

-  서로 다른 포맷들 간에 다중차원 래스터를 변환하고, 그리고/또는 특정 배열 및 그룹의 선택적인 변환을 수행할 수 있으며, 그리고/또는 부분 집합 작업을 수행할 수 있는 새 gdalmdimtranslate 유틸리티를 추가합니다. 이 유틸리티는 다중차원 드라이버로부터 2차원/대표 드라이버로 2차원 슬라이스도 추출할 수 있습니다.
   `gdalmdimtranslate 유틸리티 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/programs/gdalmdimtranslate.rst>`_ 문서를 참조하십시오.

SWIG 바인딩 변경 사항
~~~~~~~~~~~~~~~~~~~~~

C API를 SWIG 바인딩에 매핑합니다. 파이썬 바인딩의 경우 이 RFC의 범위가 완료되었습니다.
다른 언어의 경우 누락된 유형 매핑을 추가해야 하지만, 이는 이 RFC의 작업 범위를 벗어납니다.
파이썬 바인딩에 NumPy를 통합했습니다.

제한 사항
---------

이 RFC의 목적은 다중차원 배열이라는 주제에 대한 예비 작업입니다. 정의된 범위에서 다중차원 배열을 사용할 수 있도록 하고자 하는 목적이지만, 다음과 같은 기능 그리고/또는 성능의 틈을 메꾸기 위해 아마도 향후 개선이 필요할 것입니다.

-  블록 캐시 메커니즘이 없습니다 (이 메커니즘이 필요한지는 확신할 수 없습니다)

-  하위 픽셀(sub-pixel) 요청 또는 최근접이 아닌 서브샘플링이 없습니다.

-  WCS 드라이버 또는 다른 드라이버에 잠재적인 다중차원 케이퍼빌리티를 추가하는 것은 이 RFC의 범위를 벗어납니다.

-  SWIG 바인딩: 파이썬 바인딩만 이 RFC의 전체 범위에 들어갑니다.

하위 호환성
-----------

하위 호환성 문제점은 없습니다. API와 유틸리티만 추가했습니다.

문서화
------

-  `데이터 모델 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/user/multidim_raster_data_model.rst>`_
-  `API 예제 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/tutorials/multidimensional_api_tut.rst>`_
-  `gdalmdiminfo <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/programs/gdalmdiminfo.rst>`_
-  `gdalmdimtranslate <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/programs/gdalmdimtranslate.rst>`_
-  `VRT 드라이버 <https://github.com/rouault/gdal/blob/rfc75/gdal/doc/source/drivers/raster/vrt_multidimensional.rst>`_

테스트
------

수정된 드라이버들과 새로운 유틸리티들을 테스트하기 위해 GDAL 자동 테스트 스위트를 확장했습니다.
utilities.

구현
----

이벤 루올이 이 RFC를 구현할 것입니다. 예비 구현은 `풀 요청 1704번 <https://github.com/OSGeo/gdal/pull/1704>`_ 에 있습니다.

투표 이력
---------

-  하워드 버틀러 +1
-  노먼 바커 +1
-  이벤 루올 +1

