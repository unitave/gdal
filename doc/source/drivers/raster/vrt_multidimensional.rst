.. _vrt_multidimensional:

================================================================================
다중 차원 VRT
================================================================================

.. versionadded:: 3.1

다중 차원 VRT는 다중 차원 배열을 :ref:`multidim_raster_data_model` 에 따라 표현하기 위해 특화된 :ref:`raster.vrt` 포맷의 변이형입니다.

다음은 다중 차원 VRT 파일의 예시입니다:

.. code-block:: xml

    <VRTDataset>
        <Group name="/">
            <Dimension name="Y" size="4"/>
            <Dimension name="X" size="3"/>

            <Array name="temperature">
                <DataType>Float64</DataType>
                <DimensionRef ref="Y"/>
                <DimensionRef ref="X"/>
                <Source>
                    <SourceFilename>my.nc</SourceFilename>
                    <SourceArray>temperature</SourceArray>
                    <SourceSlab offset="1,1" count="2,2" step="2,1"/>
                    <DestSlab offset="2,1"/>
                </Source>
            </Array>
        </Group>
    </VRTDataset>

.vrt 포맷
-----------

`GDAL VRT 포맷의 XML 스키마 <https://raw.githubusercontent.com/OSGeo/gdal/master/data/gdalvrt.xsd>`_ 를 읽어보십시오.

가상 파일은 하드디스크에 다음 요소들을 가지고 있는 XML 포맷으로 저장됩니다.

**VRTDataset**:
전체 GDAL 데이터셋의 루트 요소입니다. VRTDataset 루트 요소는 속성을 가지고 있지 않으며, name 속성을 "/"로 설정한 단일 Group 하위 요소를 가지고 있어야만 합니다.

.. code-block:: xml

    <VRTDataset>
        <Group name="/">


**Group**:
이 요소는 :cpp:class:`GDALGroup` 클래스를 표현합니다. VRTDataset 요소 바로 아래에 name 속성이 "/"인 루트 그룹이 최소한 1개 있습니다. Group은 반드시 *name* 속성을 가지고 있어야만 하며, 0:n 다중도(multiplicity)를 가진 Dimension, Attribute, Array, Group 하위 요소들을 가질 수도 있습니다.

**Dimension**:
이 요소는 :cpp:class:`GDALDimension` 클래스를 표현합니다. *name* (필수), *size* (필수), *type* 및 *direction* 속성을 가지고 있습니다.

.. code-block:: xml

    <Dimension name="X" size="30" type="HORIZONTAL_X" direction="EAST"/>


**Attribute**:
이 요소는 :cpp:class:`GDALAttribute` 클래스를 표현합니다. *name* 속성과 *DataType* 하위 요소를 가지고 있어야만 합니다. 속성값들은 하나 이상의 *Value* 하위 요소(들)에 저장됩니다.

*DataType* 의 값은 String, Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, CInt16, CInt32, CFloat32 또는 CFloat64 가운데 하나일 수 있습니다.

.. code-block:: xml

    <Attribute name="foo">
        <DataType>String</DataType>
        <Value>bar</Value>
    </Attribute>


**Array**:
이 요소는 :cpp:class:`GDALMDArray` 클래스를 표현합니다. *name* 속성과 *DataType* 하위 요소를 가지고 있어야만 합니다. 이 요소의 차원을 정의하기 위한 *DimensionRef* 또는 *Dimension* 하위 요소를 0개 이상 가질 수 있습니다. 또한 이 요소의 속성을 지정하는 *SRS*, *Unit*, *NoDataValue*, *Offset* 및 *Scale* 하위 요소를 가질 수도 있습니다.
이 요소의 값을 정의하기 위해 *RegularlySpacedValues* 하위 요소 1개, 아니면 *ConstantValue*, *InlineValues*, *InlineValuesWithValueElement* 또는 *Source* 가운데 0개, 1개 또는 그 이상을 가질 수도 있습니다.

.. code-block:: xml

    <Array name="longitude">
        <DataType>Float64</DataType>
        <DimensionRef ref="longitude"/>
        <RegularlySpacedValues start="-180" step="0.5"/>
    </Array>

.. code-block:: xml

    <Array name="time">
        <DataType>String</DataType>
        <DimensionRef ref="time"/>
        <InlineValuesWithValueElement>
            <Value>2010-01-01</Value>
            <Value>2011-01-01</Value>
            <Value>2012-01-01</Value>
        </InlineValuesWithValueElement>
    </Array>

.. code-block:: xml

    <Array name="temperature">
        <DataType>Float64</DataType>
        <DimensionRef ref="Y"/>
        <Dimension name="X" size="3"/>
        <SRS dataAxisToSRSAxisMapping="2,1">EPSG:32631</SRS>
        <Unit>Kelvin</Unit>
        <NoDataValue>-999</NoDataValue>
        <Offset>0</Offset>
        <Scale>1</Scale>
        <Source>
            <SourceFilename>my.nc</SourceFilename>
            <SourceArray>temperature</SourceArray>
        </Source>
    </Array>

**Source**:
이 요소는 래스터 데이터를 개별 데이터셋으로부터 읽어와야 할지를 나타냅니다. Source 요소는 *SourceFilename* 하위 요소는 물론, (소스가 다중 차원 데이터셋인 경우) *SourceArray* 또는 (소스가 전형적인 2차원 데이터셋인 경우) *SourceTranspose* 하위 요소 가운데 하나를 가지고 있어야만 합니다.
이 요소는 :cpp:func:`GDALMDArray::Transpose` 작업을 적용하기 위한 *SourceTranspose* 하위 요소와 분할(slice)/다듬기(trim) 작업 또는 복합 데이터 유형의 구성요소 추출 작업을 적용하기 위한 *SourceView* 하위 요소를 가질 수도 있습니다. (:cpp:func:`GDALMDArray::GetView` 함수를 참조하십시오.)
이 요소는 각각 소스의 시작 오프셋, 각 차원을 따라 존재하는 값들의 개수, 그리고 소스 요소들 간의 단계를 정의하는 *offset*, *count* 및 *step* 속성을 가진 *SourceSlab* 하위 요소를 가질 수도 있습니다. 대상 배열에 소스 데이터를 배치할 위치를 정의하는 *offset* 속성을 가진 *DestSlab* 하위 요소를 가질 수도 있습니다. SourceSlab 요소를 지정하는 경우 SourceView 요소의 산출물을 작업하는데, SourceView 요소를 지정하는 경우 SourceView 요소의 산출물은 SourceTranspose의 산출물을 작업합니다.

.. code-block:: xml

        <Source>
            <SourceFilename>my.nc</SourceFilename>
            <SourceArray>temperature</SourceArray>
            <SourceTranspose>1,0</SourceTranspose>
            <SourceView>[...]</SourceView>
            <SourceSlab offset="1,1" count="2,2" step="2,1"/>
            <DestSlab offset="2,1"/>
        </Source>
