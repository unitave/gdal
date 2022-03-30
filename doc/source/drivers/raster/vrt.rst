.. _raster.vrt:

================================================================================
VRT -- GDAL 가상 포맷
================================================================================

.. shortname:: VRT

.. built_in_by_default::

소개
------------

VRT 드라이버는 GDAL 용 포맷 드라이버로, 다른 GDAL 데이터셋으로부터 재배치 작업, 적용될 가능성이 있는 알고리즘은 물론 다양한 종류의 메타데이터를 수정 또는 추가해서 가상 GDAL 데이터셋을 구성할 수 있습니다. 일반적으로 .vrt 확장자를 가진 XML 포맷에 이 가상 데이터셋의 VRT 설명을 저장할 수 있습니다.

이 VRT 포맷은 :ref:`gdal_vrttut_warped` 및 :ref:`gdal_vrttut_pansharpen` 도 서술할 수 있습니다.

예를 들어 :file:`utm.tif` 로부터 불러온 1밴드 512x512 데이터셋을 참조하는 단순한 .vrt 파일은 다음과 같이 보일 수도 있습니다:

.. code-block:: xml

    <VRTDataset rasterXSize="512" rasterYSize="512">
        <GeoTransform>440720.0, 60.0, 0.0, 3751320.0, 0.0, -60.0</GeoTransform>
        <VRTRasterBand dataType="Byte" band="1">
            <ColorInterp>Gray</ColorInterp>
            <SimpleSource>
            <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
            <SourceBand>1</SourceBand>
            <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            </SimpleSource>
        </VRTRasterBand>
    </VRTDataset>

VRT 파일의 많은 면면들은 여러 요소들의 의미를 이해하기 위해 자세히 읽어봐야 할 :ref:`raster_data_model` 을 직접 XML 인코딩한 것입니다.

VRT 포맷으로 변환하면 VRT 파일을 생성할 수 있습니다. 이렇게 산출된 파일을 편집해서 매핑을 수정하고, 메타데이터 또는 다른 용도들을 추가할 수 있습니다. 여러 가지 수단을 통해 VRT 파일을 프로그램적으로 생성할 수도 있습니다.

이 교육 교재는 .vrt 파일 포맷을 (사용자가 .vrt 파일을 편집할 수 있을 정도로) 설명하고, 개발자가 프로그램을 짜서 .vrt 파일을 생성하고 조작할 수 있는 방법을 설명할 것입니다.

.vrt 포맷
-----------

`GDAL VRT 포맷의 XML 스키마 <https://raw.githubusercontent.com/OSGeo/gdal/master/data/gdalvrt.xsd>`_ 를 읽어보십시오.

가상 파일은 하드디스크에 다음 요소들을 가지고 있는 XML 포맷으로 저장됩니다.

**VRTDataset**:
전체 GDAL 데이터셋의 루트 요소입니다. VRTDataset 루트 요소는 데이터셋의 너비와 높이를 픽셀 단위로 서술하는 rasterXSize 및 rasterYSize 속성을 가지고 있어야만 합니다. VRTWarpedDataset (:ref:`gdal_vrttut_warped`) 또는 VRTPansharpenedDataset (:ref:`gdal_vrttut_pansharpen`) 값을 가진 subClass 속성을 가지고 있을 수도 있습니다. SRS, GeoTransform, GCPList, Metadata, MaskBand 및 VRTRasterBand 하위 요소들을 가지고 있을 수도 있습니다.

.. code-block:: xml

    <VRTDataset rasterXSize="512" rasterYSize="512">

VRTDataset
++++++++++

VRTDataset이 가지고 있을 수 있는 하위 요소들은 다음과 같습니다:

- **SRS**:
  이 요소는 OGC WKT 서식으로 된 공간 좌표계를 담고 있습니다. OGC WKT 서식을 XML 용으로 제대로 이스케이프시켜야만 한다는 사실을 기억하십시오. 즉 따옴표 같은 항목들을 앤드 기호('&') 이스케이프 시퀀스로 대체할 것입니다. SRS 요소에서 :cpp:func:`OGRSpatialReference::SetFromUserInput` 메소드에 WKT는 물론, (잘 알려진 GEOGCS 이름들과 PROJ.4 서식 같은) 무결한 문자열을 입력할 수도 있습니다.

.. code-block:: xml

  <SRS dataAxisToSRSAxisMapping="1,2">PROJCS[&quot;NAD27 / UTM zone 11N&quot;,GEOGCS[&quot;NAD27&quot;,DATUM[&quot;North_American_Datum_1927&quot;,SPHEROID[&quot;Clarke 1866&quot;,6378206.4,294.9786982139006,AUTHORITY[&quot;EPSG&quot;,&quot;7008&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6267&quot;]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4267&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,-117],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;26711&quot;]]</SRS>

  GDAL 3.0버전부터 좌표계 정의에 나타난 축과 지리변형 또는 GCP 메타데이터의 축 간의 관계를 설명하기 위해 **dataAxisToSRSAxisMapping** 속성을 사용할 수 있습니다. 이 속성의 값은 쉼표로 구분된 정수 목록입니다. 이 목록의 요소 개수는 좌표계의 축 개수여야만 합니다. 정수값은 1부터 시작합니다. 이 속성의 배열 값들을 m으로 나타내는 경우, 좌표계의 첫 번째 축을 뜻하는 데이터 축 번호는 m[0]이 됩니다. 이 속성이 누락된 경우 좌표계 축에 OAMS_TRADITIONAL_GIS_ORDER 데이터 축을 매핑하는 전략을 취합니다.

- **GeoTransform**:
  이 요소는 데이터셋의 픽셀/라인 좌표와 지리참조 좌표를 매핑하는 아핀 지리변형 값 6개를 담고 있습니다.

.. code-block:: xml

  <GeoTransform>440720.0,  60,  0.0,  3751320.0,  0.0, -60.0</GeoTransform>

- **GCPList**:
  이 요소는 데이터셋의 픽셀/라인 좌표와 지리참조 좌표를 매핑하는 지상기준점(Ground Control Point) 목록을 담고 있습니다. 투영법 속성이 SRS 요소와 동일한 서식으로 된 지리참조 좌표를 사용하는 공간 좌표계를 담고 있어야 합니다. dataAxisToSRSAxisMapping 속성은 SRS 요소에서와 동일합니다.

.. code-block:: xml

    <GCPList Projection="EPSG:4326">
        <GCP Id="1" Info="a" Pixel="0.5" Line="0.5" X="0.0" Y="0.0" Z="0.0" />
        <GCP Id="2" Info="b" Pixel="13.5" Line="23.5" X="1.0" Y="2.0" Z="0.0" />
    </GCPList>

- **Metadata**:
  이 요소는 VRTDataset 전체, 또는 VRTRasterBand와 관련된 메타데이터 이름/값 쌍들의 목록을 담고 있습니다. 이 요소는 <MDI>(metadata item) 하위 요소를 가지고 있는데, 이 하위 요소는 "key" 속성과 값을 데이터로 가지고 있습니다. Metadata 요소는 여러 번 반복될 수 있는데 이 경우 반드시 메타데이터 도메인의 이름을 나타내는 "domain" 속성과 함께 쓰여야만 합니다.

.. code-block:: xml

  <Metadata>
    <MDI key="md_key">Metadata value</MDI>
  </Metadata>

- **MaskBand**:
  이 요소는 데이터셋의 모든 밴드가 공유하는 마스크 밴드를 표현합니다. (RFC 15의 GMF_PER_DATASET을 참조하십시오.) 마스크 밴드 자체를 서술하는 단일 VRTRasterBand 하위 요소를 담고 있어야만 합니다.
.. code-block:: xml

  <MaskBand>
    <VRTRasterBand dataType="Byte">
      <SimpleSource>
        <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
        <SourceBand>mask,1</SourceBand>
        <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
        <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
      </SimpleSource>
    </VRTRasterBand>
  </MaskBand>

- **OverviewList**: (GDAL 3.2.0 이상 버전, VRTPansharpenedDataset의 경우 사용할 수 없음)
  이 요소는 "가상 오버뷰"를 생성하기 위한 오버뷰 인자들을 공백으로 구분해서 담고 있습니다. 예를 들면 ``2 4`` 처럼 말입니다. VRT 데이터셋의 밴드들이 오버뷰를 선언하도록 하기 위해 사용할 수 있습니다. 이 밴드들에 추가된 소스 자체가, 선언된 인자와 호환되는 오버뷰를 가지고 있을 경우에만 이 요소를 사용하는 의미가 있습니다. 일반적으로는 이 메커니즘을 사용할 필요가 없습니다. VRT 데이터셋/밴드에 픽셀 다운샘플링을 요청하면 VRT 밴드가 오버뷰를 선언하지 않았더라도 소스의 오버뷰를 사용할 수 있기 때문입니다. 오버뷰가 VRT 수준에서 명확하게 필요한 한 가지 상황은 VRT를 더 낮은 해상도로 왜곡하는 경우입니다.
  :decl_configoption:`VRT_VIRTUAL_OVERVIEWS` 환경설정 옵션을 ``YES`` 로 설정해서 :cpp:func:`GDALDataset::BuildOverviews` 또는 :program:`gdaladdo` 를 실행하면 이 요소를 기존 VRT 데이터셋과 함께 사용할 수도 있습니다. 가상 오버뷰는 **VRTRasterBand** 수준의 **Overview** 요소 또는 생성된 .vrt.ovr 파일과 비교할 때 가장 낮은 우선 순위를 가집니다.

- **VRTRasterBand**:
  이 요소는 데이터셋의 밴드 1개를 표현합니다.

VRTRasterBand
+++++++++++++

VRTRasterBand의 속성들은 다음과 같습니다:

- **dataType**: (선택적)
  이 밴드와 관련된 픽셀 데이터의 유형입니다. (Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, CInt16, CInt32, CFloat32 또는 CFloat64 가운데 하나의 이름입니다.) 지정하지 않는 경우 기본값은 1입니다.

- **band**: (선택적)
  이 요소가 표현하는 밴드의 번호입니다. (1에서 시작하는 숫자값입니다.)

- **blockXSize**: (선택적, GDAL 3.3 이상 버전)
  블록 너비입니다.
  지정하지 않는 경우, 기본값은 최소 래스터 너비 및 128입니다.

- **blockYSize**: (선택적, GDAL 3.3 이상 버전)
  블록 높이입니다.
  지정하지 않는 경우, 기본값은 최소 래스터 높이 및 128입니다.

이 요소는 SimpleSource, ComplexSource 등과 같은 여러 종류의 소스 요소들은 물론 Metadata, ColorInterp, NoDataValue, HideNoDataValue, ColorTable, GDALRasterAttributeTable, Description 및 MaskBand 하위 요소들도 가질 수 있습니다. 래스터 밴드는 어디에서 실제 래스터 데이터를 가져와야 할지, 그리고 래스터 밴드 픽셀 공간에 그 데이터를 어떻게 매핑해야 할지를 나타내는 많은 "소스"들을 가지고 있을 수도 있습니다.

VRTRasterBand가 가지고 있을 수 있는 하위 요소들은 다음과 같습니다:

- **ColorInterp**:
  이 요소의 데이터는 색상 해석 유형의 이름이어야 합니다. Gray, Palette, Red, Green, Blue, Alpha, Hue, Saturation, Lightness, Cyan, Magenta, Yellow, Black, 또는 Unknown 가운데 하나입니다.

.. code-block:: xml

  <ColorInterp>Gray</ColorInterp>:

- **NoDataValue**:
  구성할 입력 데이터셋이 이 래스터 밴드에 NODATA 값을 가지고 있는 경우, VRT에 반영될 수 있도록 이 요소의 값을 해당 NODATA 값으로 설정하십시오. VRTComplexSource 요소의 NODATA 요소와 이 요소를 절대로 혼동해서는 안 됩니다.

.. code-block:: xml

  <NoDataValue>-100.0</NoDataValue>

- **HideNoDataValue**:
  이 요소의 값이 1인 경우, NODATA 값을 리포트하지 않을 것입니다. 본질적으로, 호출자가 NODATA 픽셀을 읽더라도 NODATA 픽셀인지 모를 것입니다. 이 요소를 가진 데이터셋으로부터 복사 또는 변환된 어떤 데이터셋도 NODATA 값을 가지지 않을 것입니다. 사용자가 데이터셋에 고정 배경값을 지정하고자 할 때 유용합니다. NoDataValue 요소가 지정한 값이 배경값이 될 것입니다. 이 요소가 생략된 경우 기본값은 0입니다.

.. code-block:: xml

  <HideNoDataValue>1</HideNoDataValue>

- **ColorTable**:
  이 요소는 색상표 항목들을 정의하는 Entry 요소 집합의 상위 요소입니다. 현재 c1이 적색, c2가 녹색, c3가 청색 그리고 c4가 알파인 RGBA 색상표만 지원합니다. 이 항목들은 번호가 매겨져 있으며, 색상표 항목 0번에서 시작한다고 가정할 것입니다.

.. code-block:: xml

    <ColorTable>
      <Entry c1="0" c2="0" c3="0" c4="255"/>
      <Entry c1="145" c2="78" c3="224" c4="255"/>
    </ColorTable>

- **GDALRasterAttributeTable**: (GDAL 2.3 이상 버전)
  이 요소는 래스터 속성 테이블의 열들을 정의하는 FieldDefn 요소 집합의 상위 요소입니다. 이 요소 뒤에 각 행의 열의 값을 정의하는 Row 요소 집합이 옵니다.

.. code-block:: xml

    <GDALRasterAttributeTable>
      <FieldDefn index="0">
        <Name>Value</Name>
        <Type>0</Type>
        <Usage>0</Usage>
      </FieldDefn>
      <FieldDefn index="1">
        <Name>Red</Name>
        <Type>0</Type>
        <Usage>6</Usage>
      </FieldDefn>
      <FieldDefn index="2">
        <Name>Green</Name>
        <Type>0</Type>
        <Usage>7</Usage>
      </FieldDefn>
      <FieldDefn index="3">
        <Name>Blue</Name>
        <Type>0</Type>
        <Usage>8</Usage>
      </FieldDefn>
      <Row index="0">
        <F>-500</F>
        <F>127</F>
        <F>40</F>
        <F>65</F>
      </Row>
      <Row index="1">
        <F>-400</F>
        <F>154</F>
        <F>168</F>
        <F>118</F>
      </Row>
    </GDALRasterAttributeTable>

- **Description**:
  이 요소는 선택적인 래스터 밴드 설명을 래스터 밴드의 텍스트 값으로 담고 있습니다.

.. code-block:: xml

  <Description>Crop Classification Layer</Description>

- **UnitType**:
  이 선택적인 요소는 표고 밴드 데이터 용 수직 단위를 담고 있습니다. 미터를 뜻하는 "m"과 피트를 뜻하는 "ft" 가운데 하나입니다. 기본적으로 미터 단위를 가정합니다.

.. code-block:: xml

  <UnitType>ft</UnitType>

- **Offset**:
  이 선택적인 요소는 래스터 밴드 상에서 크기 조정된 픽셀값으로부터 "실제/실수" 픽셀 값을 계산하는 경우 적용해야 할 오프셋을 담고 있습니다. 기본값은 0.0입니다.

.. code-block:: xml

  <Offset>0.0</Offset>

- **Scale**:
  이 선택적인 요소는 래스터 밴드 상에서 크기 조정된 픽셀값으로부터 "실제/실수" 픽셀 값을 계산하는 경우 적용해야 할 척도를 담고 있습니다. 기본값은 1.0입니다.

.. code-block:: xml

  <Scale>0.0</Scale>

- **Overview**:
  이 선택적인 요소는 밴드의 오버뷰 수준 하나를 서술합니다. SourceFilename 및 SourceBand 하위 요소들을 가지고 있어야 합니다. SourceFilename은 relativeToVRT 불(boolean) 속성을 가질 수도 있습니다. 오버뷰 여러 개를 서술하기 위해 이 요소를 여러 번 사용할 수도 있습니다.

.. code-block:: xml

    <Overview>
      <SourceFilename relativeToVRT="1">yellowstone_2.1.ntf.r2</SourceFilename>
      <SourceBand>1</SourceBand>
    </Overview>

- **CategoryNames**:
  이 선택적인 요소는 범주화된 래스터 밴드의 카테고리 이름들을 가지고 있는 Category 하위 요소 목록을 담고 있습니다.

.. code-block:: xml

  <CategoryNames>
    <Category>Missing</Category>
    <Category>Non-Crop</Category>
    <Category>Wheat</Category>
    <Category>Corn</Category>
    <Category>Soybeans</Category>
  </CategoryNames>

- **SimpleSource**:
  SimpleSource_ 란 개별 데이터셋으로부터 각각 래스터 데이터와 밴드를 읽어오고 해당 밴드의 래스터 공간에 데이터를 매핑해야 할 방법을 나타내는 데이터셋을 의미합니다.

- **AveragedSource**:
  AveragedSource는 SimpleSource로부터 파생되었으며, 대상 직사각형의 크기가 소스 직사각형의 크기와 다를 경우 SimpleSource처럼 최근접 이웃 알고리즘 대신 평균 리샘플링 알고리즘을 사용하는 점을 제외하면 동일한 속성을 공유합니다. 주의: 리샘플링 알고리즘을 지정하려면 더 일반적인 메커니즘을 쓸 수 있습니다. 다음 단락에서 'resampling' 속성에 관한 정보를 참조하십시오.

- **ComplexSource**:
  ComplexSource_ 는 SimpleSource로부터 파생되었지만 (따라서 SourceFilename, SourceBand, SrcRect 및 DstRect 요소를 공유합니다) 소스 값들의 범위를 다시 크기 조정하고 오프셋시킬 수 있는 기능을 지원합니다. NODATA 값을 지정해서 또는 GDAL 3.3버전부터 <UseMaskBand>true</UseMaskBand> 요소를 사용해서 소스의 특정 영역을 마스크할 수 있습니다.

- **KernelFilteredSource**:
  KernelFilteredSource_ 는 SimpleSource로부터 파생된 픽셀 소스지만 (따라서 SourceFilename, SourceBand, SrcRect 및 DstRect 요소를 공유합니다) Kernel 요소가 지정한 단순 필터링 커널을 통해 데이터를 전송합니다.

- **MaskBand**:
  이 요소는 상위 요소인 VRTRasterBand에 특화된 마스크 밴드를 표현합니다. 마스크 밴드 자체를 서술하는 단일 VRTRasterBand 하위 요소를 담고 있어야만 합니다.

소스
*******

SimpleSource
~~~~~~~~~~~~

SimpleSource는 SourceFilename, SourceBand, SrcRect, 및 DstRect 하위 요소들을 가질 수도 있습니다. SrcRect 요소는 지정한 소스 파일 상에서 어떤 직사각형을 읽어와야 할지를 나타내고, DstRect 요소는 소스 데이터의 해당 직사각형을 어떻게 VRTRasterBands 공간으로 매핑시켜야 할지를 나타냅니다.

SourceFilename 요소의 relativeToVRT 속성은 (속성값이 1) 파일명을 .vrt 파일과 관련된 것으로 해석해야 할지 (속성값이 0) .vrt 파일과 관련되지 않은 것으로 해석해야 할지를 나타냅니다. 기본값은 0입니다.

VRT 드라이버가 데이터셋으로부터 데이터를 정말로 읽어와야 할 때까지 소스 데이터셋을 여는 것을 연기하도록 하려면 선택적인 ``SourceProperties`` 요소에 소스 밴드의 몇몇 특성들을 지정해주면 됩니다. 소스 데이터셋 개수가 엄청나게 많은 VRT들을 작성하는 경우 특히 유용합니다. 래스터 차원, 블록 크기 및 데이터 유형 파라미터가 필요합니다. SourceProperties 태그가 생략된 경우, VRT 자체를 여는 것과 동시에 소스 데이터셋도 열 것입니다.

.. note::

    GDAL 3.4버전부터, 더 이상 소스 데이터셋 열기를 연기하기 위해 ``SourceProperties`` 요소를 사용할 필요가 없습니다.

SourceBand 하위 요소의 내용은 마스크 밴드를 참조할 수 있습니다. 예를 들어 "mask,1"은 첫 번째 소스 밴드의 마스크밴드를 의미합니다.

.. code-block:: xml

    <SimpleSource>
      <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="512" RasterYSize="512" DataType="Byte" BlockXSize="128" BlockYSize="128"/>
      <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
      <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
    </SimpleSource>

OpenOptions 하위 요소를 추가해서 소스 데이터셋을 열 때 적용할 열기 옵션을 지정할 수 있습니다. 이 요소는 "key" 속성과 값을 요소 데이터로 가지는 <OOI>(open option item) 하위 요소를 가지고 있습니다.

.. code-block:: xml

    <SimpleSource>
      <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
      <OpenOptions>
          <OOI key="OVERVIEW_LEVEL">0</OOI>
      </OpenOptions>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="256" RasterYSize="256" DataType="Byte" BlockXSize="128" BlockYSize="128"/>
      <SrcRect xOff="0" yOff="0" xSize="256" ySize="256"/>
      <DstRect xOff="0" yOff="0" xSize="256" ySize="256"/>
    </SimpleSource>

대상 직사각형의 크기가 소스 직사각형의 크기와 다를 경우 사용하는 리샘플링 알고리즘을 지정하려면 SimpleSource 또는 ComplexSource 요소에 resampling 속성을 지정하면 됩니다. nearest, bilinear, cubic, cubicspline, lanczos, average, mode 가운데 하나를 지정할 수 있습니다.

.. code-block:: xml

    <SimpleSource resampling="cubic">
      <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="256" RasterYSize="256" DataType="Byte" BlockXSize="128" BlockYSize="128"/>
      <SrcRect xOff="0" yOff="0" xSize="256" ySize="256"/>
      <DstRect xOff="0" yOff="0" xSize="128" ySize="128"/>
    </SimpleSource>

ComplexSource
~~~~~~~~~~~~~

선형 크기 조정의 대체제로서, 거듭제곱 함수를 사용하는 비선형 크기 조정을 사용해서 Exponent, SrcMin, SrcMax, DstMin 및 DstMax 요소들을 지정할 수 있습니다. SrcMin과 SrcMax를 지정하지 않는 경우, (소스 데이터셋 전체를 분석해야 할 수도 있는) 소스의 최소값과 최대값으로부터 계산합니다. Exponent는 양의 값이어야만 합니다. (gdal_translate의 -exponent 및 -scale 옵션을 이용하면 이 5개의 값을 설정할 수 있습니다.)

ComplexSource는 소스 값을 대상 값으로 변환하기 위한 사용자 지정 검색 테이블을 추가할 수 있습니다. 다음 형식을 이용하면 LUT를 지정할 수 있습니다:

.. code-block:: xml

    <LUT>[src value 1]:[dest value 1],[src value 2]:[dest value 2],...</LUT>

선형 보간을 이용해서 해당 범위의 양 끝 대상 값 사이의 중간(intermediary) 값을 계산합니다.

ComplexSource는 색상표를 가진 소스 래스터 밴드로부터 색상 구성요소를 가져올 수 있습니다. ColorTableComponent 값은 추출할 색상 구성요소의 색인입니다: 1은 적색 밴드, 2는 녹색 밴드, 3은 청색 밴드, 4는 알파 밴드입니다.

소스 값을 변환하는 경우 다음과 같은 순서로 작업을 수행합니다:

- NODATA 요소가 설정되어 있지 않거나, 또는 GDAL 3.3버전부터 UseMaskBand가 참으로 설정되어 있고 소스 밴드가 마스크 밴드를 가지고 있는 경우 마스크 작업을 수행합니다. 이 작업은 바이너리 전용이기 때문에 마스크 밴드가 실제로 0이 아닌 또는 255가 아닌 값을 가진 알파 밴드인 경우 알파 혼합 작업(blending)을 하지 않습니다.
- 색상표를 확장합니다.
- 선형 크기 조정 작업의 경우, 척도 비율을 적용한 다음 척도 오프셋을 적용합니다.
- 비선형 크기 조정 작업의 경우, (DstMax-DstMin) * pow( (SrcValue-SrcMin) / (SrcMax-SrcMin), Exponent) + DstMin을 적용합니다.
- 검색 테이블을 추가합니다.

.. code-block:: xml

    <ComplexSource>
      <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <ScaleOffset>0</ScaleOffset>
      <ScaleRatio>1</ScaleRatio>
      <ColorTableComponent>1</ColorTableComponent>
      <LUT>0:0,2345.12:64,56789.5:128,2364753.02:255</LUT>
      <NODATA>0</NODATA>  <!-- if the mask is a mask or alpha band, use <UseMaskBand>true</UseMaskBand> -->
      <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
      <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
    </ComplexSource>

비선형 크기 조정:

.. code-block:: xml

    <ComplexSource>
      <SourceFilename relativeToVRT="1">16bit.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <Exponent>0.75</Exponent>
      <SrcMin>0</SrcMin>
      <SrcMax>65535</SrcMax>
      <DstMin>0</DstMin>
      <DstMax>255</DstMax>
      <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
      <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
    </ComplexSource>


KernelFilteredSource
~~~~~~~~~~~~~~~~~~~~

Kernel 요소는 Size 및 Coefs 하위 요소 2개를 가지고 있어야 하고, 기본값이 0(거짓)인 정규화된 불 속성을 가질 수도 있습니다. Size 요소는 항상 홀수여야만 하고, Coefs 요소는 공백으로 구분된 Size * Size 항목들을 가지고 있어야만 합니다. 현재 서브샘플링 또는 오버샘플링된 데이터에 Kernel을 적용하지 않습니다.

.. code-block:: xml

    <KernelFilteredSource>
      <SourceFilename>/debian/home/warmerda/openev/utm.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <Kernel normalized="1">
        <Size>3</Size>
        <Coefs>0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111</Coefs>
      </Kernel>
    </KernelFilteredSource>

GDAL 2.3버전부터, 개별 Kernel을 사용할 수도 있습니다. 이런 경우 Coefs의 항목 개수는 Size 값과 일치해야 합니다. Coefs는 각 축을 따라 연속으로 적용되는 1차원 Kernel을 지정하기 때문에 실행 속도가 훨씬 빨라집니다. 흔히 쓰이는 많은 이미지 처리 필터들을 분리할 수 있습니다. 예를 들어 가우스 흐리기(Gaussian blur)의 경우는 다음과 같습니다:

.. code-block:: xml

    <KernelFilteredSource>
      <SourceFilename>/debian/home/warmerda/openev/utm.tif</SourceFilename>
      <SourceBand>1</SourceBand>
      <Kernel normalized="1">
        <Size>13</Size>
        <Coefs>0.01111 0.04394 0.13534 0.32465 0.60653 0.8825 1.0 0.8825 0.60653 0.32465 0.13534 0.04394 0.01111</Coefs>
      </Kernel>
    </KernelFilteredSource>

오버뷰
---------

GDAL은 다운샘플링을 수반하는 RasterIO() 요청을 처리할 때 밴드를 구성하는 소스에서 사용할 수 있는 오버뷰를 효율적으로 사용할 수 있습니다. 하지만 일반적인 경우, VRT 밴드 자체는 오버뷰를 노출시키지 않을 것입니다.

다음 경우를 제외하면 말입니다. (우선 순위가 높은 것으로부터 낮은 것 순서입니다.):

- VRTRasterBand 요소에 **Overview** 요소가 존재하는 경우. 앞의 내용을 참조하십시오.
- 또는 외부 .vrt.ovr 오버뷰를 작성한 경우.
- (GDAL 3.2버전부터) VRTDataset 요소에서 **OverviewList** 요소를 선언하는 경우 명확한 가상 오버뷰를 사용합니다. 앞의 내용을 참조하십시오.
  나중에 작성될 수도 있는 외부 .vrt.ovr 오버뷰는 이런 가상 오버뷰를 숨길 것입니다.
- (GDAL 2.1 버전부터) VRTRasterBand가 오버뷰를 가진 단일 SimpleSource 또는 ComplexSource로 이루어진 경우 명확한 가상 오버뷰를 사용합니다.
  나중에 작성될 수도 있는 외부 .vrt.ovr 오버뷰는 이런 가상 오버뷰를 숨길 것입니다.

RAW 파일을 위한 .vrt 설명
-------------------------------

이제까지 GDAL이 지원하는 기존 파일로부터 새 가상 데이터셋을 파생시키는 방법을 설명했습니다. 하지만, 데이터의 정규 레이아웃은 알려져 있지만 포맷 특화 드라이버는 존재하지 않는 RAW 바이너리 래스터 파일을 활용해야 하는 경우도 많습니다. RAW 파일을 서술하는 .vrt 파일을 작성하면 이런 RAW 파일을 사용할 수 있습니다.

예를 들어, 다음 .vrt 파일은 *l2p3hhsso.img* 라는 파일에 부동소수점형 복소수 픽셀을 담고 있는 RAW 래스터 파일을 서술합니다. 이미지 데이터는 첫 번째 바이트부터 (ImageOffset=0) 시작합니다. 픽셀 간의 바이트 오프셋은 CFloat32의 크기인 8(PixelOffset=8)입니다. 어떤 라인의 시작으로부터 다음 라인의 시작까지의 바이트 오프셋은 너비(1,172)와 픽셀 크기(8)를 곱한 9,376바이트(LineOffset=9376)입니다.

.. code-block:: xml

    <VRTDataset rasterXSize="1172" rasterYSize="1864">
        <VRTRasterBand dataType="CFloat32" band="1" subClass="VRTRawRasterBand">
            <SourceFilename relativetoVRT="1">l2p3hhsso.img</SourceFilename>
            <ImageOffset>0</ImageOffset>
            <PixelOffset>8</PixelOffset>
            <LineOffset>9376</LineOffset>
            <ByteOrder>MSB</ByteOrder>
        </VRTRasterBand>
    </VRTDataset>

기억해둘 점이 있는데, VRTRasterBand가 "VRTRawRasterBand" 라는 subClass 지정자(specifier)를 가지고 있다는 사실입니다. 또한 VRTRawRasterBand는 이전에 볼 수 없었던 요소들을 여러 개 담고 있지만 "소스" 정보는 담고 있지 않습니다. VRTRawRasterBand는 아마도 (SimpleSource 같은) 소스를 절대 가지지 못 할 테지만, 앞에서 언급했던 모든 정규 "메타데이터" 요소들은 물론 지금도 지원하고 있는 다음과 같은 요소들도 담을 수 있을 것입니다.

- **SourceFilename**: The name of the raw file containing the data for this band.  The relativeToVRT attribute can be used to indicate if the SourceFilename is relative to the .vrt file (1) or not (0).

- **ImageOffset**: The offset in bytes to the beginning of the first pixel of data of this image band.   Defaults to zero.

- **PixelOffset**: The offset in bytes from the beginning of one pixel and the next on the same line.  In packed single band data this will be the size of the **dataType** in bytes.

- **LineOffset**: The offset in bytes from the beginning of one scanline of data and the next scanline of data.  In packed single band data this will be PixelOffset * rasterXSize.

- **ByteOrder**: Defines the byte order of the data on disk. Either LSB (Least Significant Byte first) such as the natural byte order on Intel x86 systems or MSB (Most Significant Byte first) such as the natural byte order on Motorola or Sparc systems.  Defaults to being the local machine order.

A few other notes:

- The image data on disk is assumed to be of the same data type as the band **dataType** of the VRTRawRasterBand.

- All the non-source attributes of the VRTRasterBand are supported, including color tables, metadata, nodata values, and color interpretation.

- The VRTRawRasterBand supports in place update of the raster, whereas the source based VRTRasterBand is always read-only.

- The OpenEV tool includes a File menu option to input parameters describing a raw raster file in a GUI and create the corresponding .vrt file.

- Multiple bands in the one .vrt file can come from the same raw file. Just ensure that the ImageOffset, PixelOffset, and LineOffset definition for each band is appropriate for the pixels of that particular band.

Another example, in this case a 400x300 RGB pixel interleaved image.

.. code-block:: xml

    <VRTDataset rasterXSize="400" rasterYSize="300">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTRawRasterBand">
        <ColorInterp>Red</ColorInterp>
        <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
        <ImageOffset>0</ImageOffset>
        <PixelOffset>3</PixelOffset>
        <LineOffset>1200</LineOffset>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTRawRasterBand">
        <ColorInterp>Green</ColorInterp>
        <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
        <ImageOffset>1</ImageOffset>
        <PixelOffset>3</PixelOffset>
        <LineOffset>1200</LineOffset>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTRawRasterBand">
        <ColorInterp>Blue</ColorInterp>
        <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
        <ImageOffset>2</ImageOffset>
        <PixelOffset>3</PixelOffset>
        <LineOffset>1200</LineOffset>
    </VRTRasterBand>
    </VRTDataset>

VRT 데이터셋 생성
------------------------

The VRT driver supports several methods of creating VRT datasets.
The :file:`vrtdataset.h` include file should be installed with the core
GDAL include files, allowing direct access to the VRT classes.  However,
even without that most capabilities remain available through standard GDAL
interfaces.

To create a VRT dataset that is a clone of an existing dataset use the
:cpp:func:`GDALDriver::CreateCopy` method.  For example to clone
:file:`utm.tif` into a :file:`wrk.vrt` file in C++ the following could be used:

.. code-block:: cpp

  GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
  GDALDataset *poSrcDS, *poVRTDS;

  poSrcDS = (GDALDataset *) GDALOpenShared( "utm.tif", GA_ReadOnly );

  poVRTDS = poDriver->CreateCopy( "wrk.vrt", poSrcDS, FALSE, NULL, NULL, NULL );

  GDALClose((GDALDatasetH) poVRTDS);
  GDALClose((GDALDatasetH) poSrcDS);

Note the use of :cpp:func:`GDALOpenShared` when opening the source dataset. It is advised
to use :cpp:func:`GDALOpenShared` in this situation so that you are able to release
the explicit reference to it before closing the VRT dataset itself. In other
words, in the previous example, you could also invert the 2 last lines, whereas
if you open the source dataset with :cpp:func:`GDALOpen`, you'd need to close the VRT dataset
before closing the source dataset.

To create a virtual copy of a dataset with some attributes added or changed
such as metadata or coordinate system that are often hard to change on other
formats, you might do the following.  In this case, the virtual dataset is
created "in memory" only by virtual of creating it with an empty filename, and
then used as a modified source to pass to a :cpp:func:`GDALDriver::CreateCopy` written out in TIFF
format.

.. code-block:: cpp

  poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

  poVRTDS->SetMetadataItem( "SourceAgency", "United States Geological Survey");
  poVRTDS->SetMetadataItem( "SourceDate", "July 21, 2003" );

  poVRTDS->GetRasterBand( 1 )->SetNoDataValue( -999.0 );

  GDALDriver *poTIFFDriver = (GDALDriver *) GDALGetDriverByName( "GTiff" );
  GDALDataset *poTiffDS;

  poTiffDS = poTIFFDriver->CreateCopy( "wrk.tif", poVRTDS, FALSE, NULL, NULL, NULL );

  GDALClose((GDALDatasetH) poTiffDS);

In the above example the nodata value is set as -999. You can set the
HideNoDataValue element in the VRT dataset's band using :cpp:func:`GDALRasterBand::SetMetadataItem` on
that band.

.. code-block:: cpp

  poVRTDS->GetRasterBand( 1 )->SetMetadataItem( "HideNoDataValue" , "1" );

In this example a virtual dataset is created with the :cpp:func:`GDALDriver::Create` method, and
adding bands and sources programmatically, but still via the "generic" API.
A special attribute of VRT datasets is that sources can be added to the VRTRasterBand
(but not to VRTRawRasterBand) by passing the XML describing the source into :cpp:func:`GDALRasterBand::SetMetadataItem` on the special
domain target "new_vrt_sources".  The domain target "vrt_sources" may also be
used, in which case any existing sources will be discarded before adding the
new ones.  In this example we construct a simple averaging filter source
instead of using the simple source.

.. code-block:: cpp

    // construct XML for simple 3x3 average filter kernel source.
    const char *pszFilterSourceXML  =
    "<KernelFilteredSource>"
    "  <SourceFilename>utm.tif</SourceFilename><SourceBand>1</SourceBand>"
    "  <Kernel>"
    "    <Size>3</Size>"
    "    <Coefs>0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111</Coefs>"
    "  </Kernel>"
    "</KernelFilteredSource>";

    // Create the virtual dataset.
    poVRTDS = poDriver->Create( "", 512, 512, 1, GDT_Byte, NULL );
    poVRTDS->GetRasterBand(1)->SetMetadataItem("source_0",pszFilterSourceXML,
                                                "new_vrt_sources");

A more general form of this that will produce a 3x3 average filtered clone
of any input datasource might look like the following.  In this case we
deliberately set the filtered datasource as in the "vrt_sources" domain
to override the SimpleSource created by the `cpp:func:`GDALDriver::CreateCopy` method.  The fact
that we used `cpp:func:GDALDriver::CreateCopy` ensures that all the other metadata, georeferencing
and so forth is preserved from the source dataset ... the only thing we are
changing is the data source for each band.

.. code-block:: cpp

    int   nBand;
    GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
    GDALDataset *poSrcDS, *poVRTDS;

    poSrcDS = (GDALDataset *) GDALOpenShared( pszSourceFilename, GA_ReadOnly );

    poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

    for( nBand = 1; nBand <= poVRTDS->GetRasterCount(); nBand++ )
    {
        char szFilterSourceXML[10000];

        GDALRasterBand *poBand = poVRTDS->GetRasterBand( nBand );

        sprintf( szFilterSourceXML,
            "<KernelFilteredSource>"
            "  <SourceFilename>%s</SourceFilename><SourceBand>%d</SourceBand>"
            "  <Kernel>"
            "    <Size>3</Size>"
            "    <Coefs>0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111</Coefs>"
            "  </Kernel>"
            "</KernelFilteredSource>",
            pszSourceFilename, nBand );

        poBand->SetMetadataItem( "source_0", szFilterSourceXML, "vrt_sources" );
    }

The :cpp:class:`VRTDataset` class is one of the few dataset implementations that supports the :cpp:func:`GDALDataset::AddBand`
method. The options passed to the :cpp:func:`GDALDataset::AddBand` method can be used to control the type of the
band created (VRTRasterBand, VRTRawRasterBand, VRTDerivedRasterBand), and in the case of
the VRTRawRasterBand to set its various parameters. For standard VRTRasterBand, sources
should be specified with the above :cpp:func:`GDALRasterBand::SetMetadataItem` examples.

.. code-block:: cpp

  GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
  GDALDataset *poVRTDS;

  poVRTDS = poDriver->Create( "out.vrt", 512, 512, 0, GDT_Byte, NULL );
  char** papszOptions = NULL;
  papszOptions = CSLAddNameValue(papszOptions, "subclass", "VRTRawRasterBand"); // if not specified, default to VRTRasterBand
  papszOptions = CSLAddNameValue(papszOptions, "SourceFilename", "src.tif"); // mandatory
  papszOptions = CSLAddNameValue(papszOptions, "ImageOffset", "156"); // optional. default = 0
  papszOptions = CSLAddNameValue(papszOptions, "PixelOffset", "2"); // optional. default = size of band type
  papszOptions = CSLAddNameValue(papszOptions, "LineOffset", "1024"); // optional. default = size of band type * width
  papszOptions = CSLAddNameValue(papszOptions, "ByteOrder", "LSB"); // optional. default = machine order
  papszOptions = CSLAddNameValue(papszOptions, "relativeToVRT", "true"); // optional. default = false
  poVRTDS->AddBand(GDT_Byte, papszOptions);
  CSLDestroy(papszOptions);

  delete poVRTDS;

.. _vrt_derived_bands:

파생 밴드 사용하기 (C/C++ 픽셀 함수 이용)
---------------------------------------------------

A specialized type of band is a 'derived' band which derives its pixel
information from its source bands.  With this type of band you must also
specify a pixel function, which has the responsibility of generating the
output raster.  Pixel functions are created by an application and then
registered with GDAL using a unique key.

Using derived bands you can create VRT datasets that manipulate bands on
the fly without having to create new band files on disk.  For example, you
might want to generate a band using four source bands from a nine band input
dataset (x0, x3, x4, and x8) and some constant y:

.. code-block:: c

  band_value = sqrt((x3*x3+x4*x4)/(x0*x8)) + y;

You could write the pixel function to compute this value and then register
it with GDAL with the name "MyFirstFunction".  Then, the following VRT XML
could be used to display this derived band:


.. code-block:: xml

    <VRTDataset rasterXSize="1000" rasterYSize="1000">
        <VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">
            <Description>Magnitude</Description>
            <PixelFunctionType>MyFirstFunction</PixelFunctionType>
            <PixelFunctionArguments y="4" />
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>1</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>4</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>5</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>9</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
        </VRTRasterBand>
    </VRTDataset>

.. note::

    PixelFunctionArguments can only be used with C++ pixel functions in GDAL versions 3.4 and greater.


In addition to the subclass specification (VRTDerivedRasterBand) and
the PixelFunctionType value, there is another new parameter that can come
in handy: SourceTransferType.  Typically the source rasters are obtained
using the data type of the derived band.  There might be times,
however, when you want the pixel function to have access to
higher resolution source data than the data type being generated.
For example, you might have a derived band of type "Float", which takes
a single source of type "CFloat32" or "CFloat64", and returns the imaginary
portion.  To accomplish this, set the SourceTransferType to "CFloat64".
Otherwise the source would be converted to "Float" prior to
calling the pixel function, and the imaginary portion would be lost.

.. code-block:: xml

    <VRTDataset rasterXSize="1000" rasterYSize="1000">
        <VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">
            <Description>Magnitude</Description>
            <PixelFunctionType>MyFirstFunction</PixelFunctionType>
            <SourceTransferType>CFloat64</SourceTransferType>
            ...

기본 픽셀 함수
+++++++++++++++++++++++

GDAL provides a set of default pixel functions that can be used without writing new code:


.. list-table::
   :widths: 15 10 20 55
   :header-rows: 1

   * - PixelFunctionType
     - Number of input sources
     - PixelFunctionArguments
     - Description
   * - **cmul**
     - 2
     - -
     - multiply the first band for the complex conjugate of the second
   * - **complex**
     - 2
     - -
     - make a complex band merging two bands used as real and imag values
   * - **conj**
     - 1
     - -
     - computes the complex conjugate of a single raster band (just a copy if the input is non-complex)
   * - **dB**
     - 1
     - ``fact`` (선택적)
     - perform conversion to dB of the abs of a single raster band (real or complex): ``20. * log10( abs( x ) )``. The optional ``fact`` parameter can be set to ``10`` to get the alternative formula: ``10. * log10( abs( x ) )``
   * - **dB2amp**
     - 1
     - -
     - perform scale conversion from logarithmic to linear (amplitude) (i.e. ``10 ^ ( x / 20 )`` ) of a single raster band (real only). Deprecated in GDAL v3.5. Please use the ``exp`` pixel function with ``base = 10.`` and ``fact = 0.05`` i.e. ``1./20``
   * - **dB2pow**
     - 1
     - -
     - perform scale conversion from logarithmic to linear (power) (i.e. ``10 ^ ( x / 10 )`` ) of a single raster band (real only). Deprecated in GDAL v3.5. Please use the ``exp`` pixel function with ``base = 10.`` and ``fact = 0.1`` i.e. ``1./10``
   * - **diff**
     - 2
     - -
     - computes the difference between 2 raster bands (``b1 - b2``)
   * - **div**
     - 2
     - -
     - divide one rasted band by another (``b1 / b2``)
   * - **exp**
     - 1
     - ``base`` (선택적), ``fact`` (선택적)
     - computes the exponential of each element in the input band ``x`` (of real values): ``e ^ x``. The function also accepts two optional parameters: ``base`` and ``fact`` that allow to compute the generalized formula: ``base ^ ( fact * x )``. Note: this function is the recommended one to perform conversion form logarithmic scale (dB): `` 10. ^ (x / 20.)``, in this case ``base = 10.`` and ``fact = 0.05`` i.e. ``1. / 20``
   * - **imag**
     - 1
     - -
     - extract imaginary part from a single raster band (0 for non-complex)
   * - **intensity**
     - 1
     - -
     - computes the intensity ``Re( x * conj(x) )`` of a single raster band (real or complex)
   * - **interpolate_exp**
     - >= 2
     - ``t0``, ``dt``, ``t``
     - interpolate a value at time (or position) ``t`` given input sources beginning at position ``t0`` with spacing ``dt`` using exponential interpolation
   * - **interpolate_linear**
     - >= 2
     - ``t0``, ``dt``, ``t``
     - interpolate a value at time (or position) ``t`` given input sources beginning at ``t0`` with spacing ``dt`` using linear interpolation
   * - **inv**
     - 1
     - ``k`` (선택적)
     - inverse (``1./x``). If the optional ``k`` parameter is set then the result is multiplied by ``k`` (``k / x``)
   * - **log10**
     - 1
     - -
     - compute the logarithm (base 10) of the abs of a single raster band (real or complex): ``log10( abs( x ) )``
   * - **mod**
     - 1
     - -
     - extract module from a single raster band (real or complex)
   * - **mul**
     - >= 2
     - ``k`` (선택적)
     - multiply 2 or more raster bands. If the optional ``k`` parameter is provided then the result is multiplied by the scalar ``k``.
   * - **phase**
     - 1
     - -
     - extract phase from a single raster band [-PI,PI] (0 or PI for non-complex)
   * - **polar**
     - 2
     - ``amplitude_type`` (선택적)
     - make a complex band using input bands for amplitude and phase values ``b1 * exp( j * b2 )``. The optional (string) parameter ``amplitude_type`` can be ``AMPLITUDE`` (default) ``INTENSITY`` or ``dB``. Note: if ``amplitude_type`` is set to ``INTENSITY`` then negative values are clipped to zero.
   * - **pow**
     - 1
     - ``power``
     - raise a single raster band to a constant power, specified with argument ``power`` (real only)
   * - **real**
     - 1
     - -
     - extract real part from a single raster band (just a copy if the input is non-complex)
   * - **sqrt**
     - 1
     - -
     - perform the square root of a single raster band (real only)
   * - **sum**
     - >= 2
     - ``k`` (선택적)
     - sum 2 or more raster bands. If the optional ``k`` parameter is provided then it is added to each element of the result
   * - **replace_nodata**
     - = 1
     - ``to`` (선택적)
     - convert incoming ``NoData`` values to a new value, IEEE 754 `nan` by default
   * - **scale**
     - = 1
     - -
     - perform scaling according to the ``offset`` and ``scale`` values of the raster band

픽셀 함수 작성하기
+++++++++++++++++++++++

To register this function with GDAL (prior to accessing any VRT datasets
with derived bands that use this function), an application calls
:cpp:func:`GDALAddDerivedBandPixelFuncWithArgs` with a key and a :cpp:type:`GDALDerivedPixelFuncWithArgs`:

.. code-block:: cpp

    static const char pszMetadata[] =
    "<PixelFunctionArgumentsList>"
    "   <Argument name='y' description='y' type='double' mandatory='1' />"
    "   <Argument type='builtin' value='offset' />"
    "   <Argument type='builtin' value='scale' />"
    "   <Argument type='builtin' value='NoData' />"
    "   <Argument name='customConstant' type='constant' value='42'>"
    "</PixelFunctionArgumentsList>";
    GDALAddDerivedBandPixelFuncWithArgs("MyFirstFunction", TestFunction, pszMetadata);

A good time to do this is at the beginning of an application when the
GDAL drivers are registered. ``pszMetadata`` is optional and can be ``nullptr``.
It can be used to declare the function signature to the user and to request additional
parameters aside from the ones from the Dataset.

A :cpp:type:`GDALDerivedPixelFuncWithArgs` is defined with a signature similar to :cpp:func:`GDALRasterBand::IRasterIO`:


.. cpp:function:: CPLErr TestFunction(void** papoSources, int nSources, void* pData, int nBufXSize, int nBufYSize, GDALDataType eSrcType, GDALDataType eBufType, int nPixelSpace, int nLineSpace, CSLConstList papszArgs)

   :param papoSources: A pointer to packed rasters; one per source.  The
    datatype of all will be the same, specified in the ``eSrcType`` parameter.

   :param nSources: The number of source rasters.

   :param pData: The buffer into which the data should be read, or from which
    it should be written.  This buffer must contain at least ``nBufXSize *
    nBufYSize`` words of type eBufType.  It is organized in left to right, top
    to bottom pixel order.  Spacing is controlled by the ``nPixelSpace`` and
    ``nLineSpace`` parameters.

   :param nBufXSize: The width of the buffer image into which the desired
    region is to be read, or from which it is to be written.

   :param nBufYSize: The height of the buffer image into which the desired
    region is to be read, or from which it is to be written.

   :param eSrcType: The type of the pixel values in the ``papoSources`` raster
    array.

   :param eBufType: The type of the pixel values that the pixel function must
    generate in the ``pData`` data buffer.

   :param nPixelSpace: The byte offset from the start of one pixel value in
    ``pData`` to the start of the next pixel value within a scanline.  If
    defaulted (0) the size of the datatype eBufType is used.

   :param nLineSpace: The byte offset from the start of one scanline in
    pData to the start of the next.

   :param papszArgs: An optional string list of named function arguments (e.g. ``y=4``)


It is also possible to register a :cpp:type:`GDALDerivedPixelFunc` (which omits the final :cpp:type:`CSLConstList` argument) using :cpp:func:`GDALAddDerivedBandPixelFunc`.

The following is an implementation of the pixel function:

.. code-block:: cpp

    #include "gdal.h"

    CPLErr TestFunction(void **papoSources, int nSources, void *pData,
                        int nXSize, int nYSize,
                        GDALDataType eSrcType, GDALDataType eBufType,
                        int nPixelSpace, int nLineSpace,
                        CSLConstList papszArgs)
    {
        int ii, iLine, iCol;
        double pix_val;
        double x0, x3, x4, x8;

        // ---- Init ----
        if (nSources != 4) return CE_Failure;

        const char *pszY = CSLFetchNameValue(papszArgs, "y");
        if (pszY == nullptr) return CE_Failure;

        double NoData = NAN;
        const char *pszNoData = CSLFetchNameValue(papszArgs, "NoData");
        if (pszNoData != nullptr)
        {
            NoData = std::strtod(pszNoData, &end);
            if (end == pszNoData) return CE_Failure; // Could not parse
        }

        char *end = nullptr;
        double y = std::strtod(pszY, &end);
        if (end == pszY) return CE_Failure; // Could not parse

        // ---- Set pixels ----
        for( iLine = 0; iLine < nYSize; iLine++ )
        {
            for( iCol = 0; iCol < nXSize; iCol++ )
            {
                ii = iLine * nXSize + iCol;
                /* Source raster pixels may be obtained with SRCVAL macro */
                x0 = SRCVAL(papoSources[0], eSrcType, ii);
                x3 = SRCVAL(papoSources[1], eSrcType, ii);
                x4 = SRCVAL(papoSources[2], eSrcType, ii);
                x8 = SRCVAL(papoSources[3], eSrcType, ii);

                if (x0 == NoData || x3 == NoData || x4 == NoData || x8 == NoData)
                    pix_val = NAN;
                else
                    pix_val = sqrt((x3*x3+x4*x4)/(x0*x8)) + y;

                GDALCopyWords(&pix_val, GDT_Float64, 0,
                            ((GByte *)pData) + nLineSpace * iLine + iCol * nPixelSpace,
                            eBufType, nPixelSpace, 1);
            }
        }

        // ---- Return success ----
        return CE_None;
    }

파생 밴드 사용하기 (파이썬 픽셀 함수 이용)
----------------------------------------------------

Starting with GDAL 2.2, in addition to pixel functions written in C/C++ as
documented in the :ref:`vrt_derived_bands` section, it is possible to use
pixel functions written in Python. Both `CPython <https://www.python.org/>`_
and `NumPy <http://www.numpy.org/>`_ are requirements at run-time.

The subelements for VRTRasterBand (whose subclass specification must be
set to VRTDerivedRasterBand) are :

- **PixelFunctionType** (required): Must be set to a function name that will be defined as a inline Python module in PixelFunctionCode element or as the form "module_name.function_name" to refer to a function in an external Python module

- **PixelFunctionLanguage** (required): Must be set to Python.

- **PixelFunctionCode** (required if PixelFunctionType is of the form "function_name", ignored otherwise). The in-lined code of a Python module, that must be at least have a function whose name is given by PixelFunctionType.

- **BufferRadius** (optional, defaults to 0): Amount of extra pixels, with respect to the original RasterIO() request to satisfy, that are fetched at the left, right, bottom and top of the input and output buffers passed to the pixel function. Note that the values of the output buffer in this buffer zone willbe ignored.

The signature of the Python pixel function must have the following arguments:

- **in_ar**: list of input NumPy arrays (one NumPy array for each source)
- **out_ar**: output NumPy array to fill. The array is initialized at the right dimensions and with the VRTRasterBand.dataType.
- **xoff**: pixel offset to the top left corner of the accessed region of the band. Generally not needed except if the processing depends on the pixel position in the raster.
- **yoff** line offset to the top left corner of the accessed region of the band. Generally not needed.
- **xsize**: width of the region of the accessed region of the band. Can be used together with out_ar.shape[1] to determine the horizontal resampling ratio of the request.
- **ysize**: height of the region of the accessed region of the band. Can be used together with out_ar.shape[0] to determine the vertical resampling ratio of the request.
- **raster_xsize**: total with of the raster band. Generally not needed.
- **raster_ysize**: total with of the raster band. Generally not needed.
- **buf_radius**: radius of the buffer (in pixels) added to the left, right, top and bottom of in_ar / out_ar. This is the value of the optional BufferRadius element that can be set so that the original pixel request is extended by a given amount of pixels.
- **gt**: geotransform. Array of 6 double values.
- **kwargs**: dictionary with user arguments defined in PixelFunctionArguments

The provided ``out_ar`` array must be modified in-place. Any value currently
returned by the pixel function is ignored.

.. note::

    If wanting to fill ``out_ar`` from another array, use the ``out_ar[:] = ...``
    syntax.

예시
++++++++

VRT that multiplies the values of the source file by a factor of 1.5
********************************************************************

.. code-block:: xml

    <VRTDataset rasterXSize="20" rasterYSize="20">
        <SRS>EPSG:26711</SRS>
        <GeoTransform>440720,60,0,3751320,0,-60</GeoTransform>
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTDerivedRasterBand">
            <PixelFunctionType>multiply</PixelFunctionType>
            <PixelFunctionLanguage>Python</PixelFunctionLanguage>
            <PixelFunctionArguments factor="1.5"/>
            <PixelFunctionCode><![CDATA[
                import numpy as np
                def multiply(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                                raster_ysize, buf_radius, gt, **kwargs):
                    factor = float(kwargs['factor'])
                    out_ar[:] = np.round_(np.clip(in_ar[0] * factor,0,255))
                ]]>
            </PixelFunctionCode>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">byte.tif</SourceFilename>
            </SimpleSource>
        </VRTRasterBand>
    </VRTDataset>

VRT that adds 2 (or more) rasters
*********************************

.. code-block:: xml

    <VRTDataset rasterXSize="20" rasterYSize="20">
        <SRS>EPSG:26711</SRS>
        <GeoTransform>440720,60,0,3751320,0,-60</GeoTransform>
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTDerivedRasterBand">
            <PixelFunctionType>add</PixelFunctionType>
            <PixelFunctionLanguage>Python</PixelFunctionLanguage>
            <PixelFunctionCode><![CDATA[
                import numpy as np
                def add(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                                raster_ysize, buf_radius, gt, **kwargs):
                    np.round_(np.clip(np.sum(in_ar, axis = 0, dtype = 'uint16'),0,255),
                            out = out_ar)
                ]]>
            </PixelFunctionCode>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">byte.tif</SourceFilename>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">byte2.tif</SourceFilename>
            </SimpleSource>
        </VRTRasterBand>
    </VRTDataset>

VRT that computes hillshading using an external library
*******************************************************

.. code-block:: xml

    <VRTDataset rasterXSize="121" rasterYSize="121">
        <SRS>EPSG:4326</SRS>
        <GeoTransform>-80.004166666666663,0.008333333333333,0,
        44.004166666666663,0,-0.008333333333333</GeoTransform>
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTDerivedRasterBand">
            <ColorInterp>Gray</ColorInterp>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">n43.dt0</SourceFilename>
            </SimpleSource>
            <PixelFunctionLanguage>Python</PixelFunctionLanguage>
            <PixelFunctionType>hillshading.hillshade</PixelFunctionType>
            <PixelFunctionArguments scale="111120" z_factor="30" />
            <BufferRadius>1</BufferRadius>
            <SourceTransferType>Int16</SourceTransferType>
        </VRTRasterBand>
    </VRTDataset>

with hillshading.py:

.. code-block:: python

    # Licence: MIT
    # Copyright 2016, Even Rouault
    import math

    def hillshade_int(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                            raster_ysize, radius, gt, z, scale):
        ovr_scale_x = float(out_ar.shape[1] - 2 * radius) / xsize
        ovr_scale_y = float(out_ar.shape[0] - 2 * radius) / ysize
        ewres = gt[1] / ovr_scale_x
        nsres = gt[5] / ovr_scale_y
        inv_nsres = 1.0 / nsres
        inv_ewres = 1.0 / ewres

        az = 315
        alt = 45
        degreesToRadians = math.pi / 180

        sin_alt = math.sin(alt * degreesToRadians)
        azRadians = az * degreesToRadians
        z_scale_factor = z / (8 * scale)
        cos_alt_mul_z_scale_factor = \
                math.cos(alt * degreesToRadians) * z_scale_factor
        cos_az_mul_cos_alt_mul_z_scale_factor_mul_254 = \
                    254 * math.cos(azRadians) * cos_alt_mul_z_scale_factor
        sin_az_mul_cos_alt_mul_z_scale_factor_mul_254 = \
                    254 * math.sin(azRadians) * cos_alt_mul_z_scale_factor
        square_z_scale_factor = z_scale_factor * z_scale_factor
        sin_alt_mul_254 = 254.0 * sin_alt

        for j in range(radius, out_ar.shape[0]-radius):
            win_line = in_ar[0][j-radius:j+radius+1,:]
            for i in range(radius, out_ar.shape[1]-radius):
                win = win_line[:,i-radius:i+radius+1].tolist()
                x = inv_ewres * ((win[0][0] + win[1][0] + win[1][0] + win[2][0])-\
                                (win[0][2] + win[1][2] + win[1][2] + win[2][2]))
                y = inv_nsres * ((win[2][0] + win[2][1] + win[2][1] + win[2][2])-\
                                (win[0][0] + win[0][1] + win[0][1] + win[0][2]))
                xx_plus_yy = x * x + y * y
                cang_mul_254 = (sin_alt_mul_254 - \
                    (y * cos_az_mul_cos_alt_mul_z_scale_factor_mul_254 - \
                        x * sin_az_mul_cos_alt_mul_z_scale_factor_mul_254)) / \
                    math.sqrt(1 + square_z_scale_factor * xx_plus_yy)
                if cang_mul_254 < 0:
                    out_ar[j,i] = 1
                else:
                    out_ar[j,i] = 1 + round(cang_mul_254)

    def hillshade(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                raster_ysize, radius, gt, **kwargs):
        z = float(kwargs['z_factor'])
        scale= float(kwargs['scale'])
        hillshade_int(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                    raster_ysize, radius, gt, z, scale)

파이썬 모듈 경로
++++++++++++++++++

When importing modules from inline Python code or when relying on out-of-line
code (PixelFunctionType of the form "module_name.function_name"), you need
to make sure the modules are accessible through the python path. Note that
contrary to the Python interactive interpreter, the current path is not
automatically added when used from GDAL. So you may need to define the
**PYTHONPATH** environment variable if you get ModuleNotFoundError exceptions.

보안 영향
*********************

The ability to run Python code potentially opens the door to many potential
vulnerabilities if the user of GDAL may process untrusted datasets. To avoid
such issues, by default, execution of Python pixel function will be disabled.
The execution policy can be controlled with the :decl_configoption:`GDAL_VRT_ENABLE_PYTHON`
configuration option, which can accept 3 values:

- YES: all VRT scripts are considered as trusted and their Python pixel functions will be run when pixel operations are involved.
- NO: all VRT scripts are considered untrusted, and none Python pixelfunction will be run.
- TRUSTED_MODULES (default setting): all VRT scripts with inline Python code in their PixelFunctionCode elements will be considered untrusted and will not be run. VRT scripts that use a PixelFunctionType of the form "module_name.function_name" will be considered as trusted, only if "module_name" is allowed in the :decl_configoption:`GDAL_VRT_TRUSTED_MODULES` configuration option. The value of this configuration option is a comma separated listed of trusted module names. The '*' wildcard can be used at the name of a string to match all strings beginning with the substring before the '*' character. For example 'every*' will make 'every.thing' or 'everything' module trusted. '*' can also be used to make all modules to be trusted. The ".*" wildcard can also be used to match exact modules or submodules names. For example 'every.*' will make 'every' and 'every.thing' modules trusted, but not 'everything'.

.. _linking_mechanism_to_python_interpreter:

파이썬 해석기에 메커니즘 링크하기
*****************************************

Currently only CPython 2 and 3 is supported. The GDAL shared object
is not explicitly linked at build time to any of the CPython library. When GDAL
will need to run Python code, it will first determine if the Python interpreter
is loaded in the current process (which is the case if the program is a Python
interpreter itself, or if another program, e.g. QGIS, has already loaded the
CPython library). Otherwise it will look if the :decl_configoption:`PYTHONSO` configuration option is
defined. This option can be set to point to the name of the Python library to
use, either as a shortname like "libpython2.7.so" if it is accessible through
the Linux dynamic loader (so typically in one of the paths in /etc/ld.so.conf or
LD_LIBRARY_PATH) or as a full path name like "/usr/lib/x86_64-linux-gnu/libpython2.7.so".
The same holds on Windows will shortnames like "python27.dll" if accessible through
the PATH or full path names like "c:\\python27\\python27.dll". If the :decl_configoption:`PYTHONSO`
configuration option is not defined, it will look for a "python" binary in the
directories of the PATH and will try to determine the related shared object
(it will retry with "python3" if no "python" has been found). If the above
was not successful, then a predefined list of shared objects names
will be tried. At the time of writing, the order of versions searched is 2.7,
3.5, 3.6, 3.7, 3.8, 3.9, 3.4, 3.3, 3.2. Enabling debug information (CPL_DEBUG=ON) will
show which Python version is used.

JIT(Just-in-time) 컴파일 작업
++++++++++++++++++++++++++++

The use of a just-in-time compiler may significantly speed up execution times.
`Numba <http://numba.pydata.org/>`_ has been successfully tested. For
better performance, it is recommended to use a offline pixel function so that
the just-in-time compiler may cache its compilation.

Given the following :file:`mandelbrot.py` file :

.. code-block:: python

    # Trick for compatibility with and without numba
    try:
        from numba import jit
        #print('Using numba')
        g_max_iterations = 100
    except:
        class jit(object):
            def __init__(self, nopython = True, nogil = True):
                pass

            def __call__(self, f):
                return f

        #print('Using non-JIT version')
        g_max_iterations = 25

    # Use a wrapper for the entry point regarding GDAL, since GDAL cannot access
    # the jit decorated function with the expected signature.
    def mandelbrot(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                            raster_ysize, r, gt, **kwargs):
        mandelbrot_jit(out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize,
    g_max_iterations)

    # Will make sure that the code is compiled to pure native code without Python
    # fallback.
    @jit(nopython=True, nogil=True, cache=True)
    def mandelbrot_jit(out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                            raster_ysize, max_iterations):
        ovr_factor_y = float(out_ar.shape[0]) / ysize
        ovr_factor_x = float(out_ar.shape[1]) / xsize
        for j in range( out_ar.shape[0]):
            y0 = 2.0 * (yoff + j / ovr_factor_y) / raster_ysize - 1
            for i in range(out_ar.shape[1]):
                x0 = 3.5 * (xoff + i / ovr_factor_x) / raster_xsize - 2.5
                x = 0.0
                y = 0.0
                x2 = 0.0
                y2 = 0.0
                iteration = 0
                while x2 + y2 < 4 and iteration < max_iterations:
                    y = 2*x*y + y0
                    x = x2 - y2 + x0
                    x2 = x * x
                    y2 = y * y
                    iteration += 1

                out_ar[j][i] = iteration * 255 / max_iterations

The following VRT file can be used (to be opened with QGIS for example)

.. code-block:: xml

    <VRTDataset rasterXSize="100000000" rasterYSize="100000000">
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTDerivedRasterBand">
            <PixelFunctionLanguage>Python</PixelFunctionLanguage>
            <PixelFunctionType>mandelbrot.mandelbrot</PixelFunctionType>
            <Metadata>
            <MDI key="STATISTICS_MAXIMUM">255</MDI>
            <MDI key="STATISTICS_MEAN">127</MDI>
            <MDI key="STATISTICS_MINIMUM">0</MDI>
            <MDI key="STATISTICS_STDDEV">127</MDI>
            </Metadata>
            <ColorInterp>Gray</ColorInterp>
            <Histograms>
            <HistItem>
                <HistMin>-0.5</HistMin>
                <HistMax>255.5</HistMax>
                <BucketCount>256</BucketCount>
                <IncludeOutOfRange>0</IncludeOutOfRange>
                <Approximate>1</Approximate>
                <HistCounts>0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
        0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0</HistCounts>
            </HistItem>
            </Histograms>
        </VRTRasterBand>
    </VRTDataset>

.. _gdal_vrttut_warped:

왜곡 VRT
----------

A warped VRT is a VRTDataset with subClass="VRTWarpedDataset". It has a
GDALWarpOptions element which describe the warping options.

.. code-block:: xml

    <VRTDataset rasterXSize="20" rasterYSize="20" subClass="VRTWarpedDataset">
        <SRS>PROJCS["NAD27 / UTM zone 11N",GEOGCS["NAD27",DATUM["North_American_Datum_1927",SPHEROID["Clarke 1866",6378206.4,294.9786982138982,AUTHORITY["EPSG","7008"]],AUTHORITY["EPSG","6267"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4267"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","26711"]]</SRS>
        <GeoTransform>  4.4072000000000000e+05,  6.0000000000000000e+01,  0.0000000000000000e+00,  3.7513200000000000e+06,  0.0000000000000000e+00, -6.0000000000000000e+01</GeoTransform>
        <Metadata>
            <MDI key="AREA_OR_POINT">Area</MDI>
        </Metadata>
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTWarpedRasterBand">
            <ColorInterp>Gray</ColorInterp>
        </VRTRasterBand>
        <BlockXSize>20</BlockXSize>
        <BlockYSize>20</BlockYSize>
        <GDALWarpOptions>
            <WarpMemoryLimit>6.71089e+07</WarpMemoryLimit>
            <ResampleAlg>NearestNeighbour</ResampleAlg>
            <WorkingDataType>Byte</WorkingDataType>
            <Option name="INIT_DEST">0</Option>
            <SourceDataset relativeToVRT="1">byte.vrt</SourceDataset>
            <Transformer>
            <ApproxTransformer>
                <MaxError>0.125</MaxError>
                <BaseTransformer>
                <GenImgProjTransformer>
                    <SrcGeoTransform>440720,60,0,3751320,0,-60</SrcGeoTransform>
                    <SrcInvGeoTransform>-7345.33333333333303,0.0166666666666666664,0,62522,0,-0.0166666666666666664</SrcInvGeoTransform>
                    <DstGeoTransform>440720,60,0,3751320,0,-60</DstGeoTransform>
                    <DstInvGeoTransform>-7345.33333333333303,0.0166666666666666664,0,62522,0,-0.0166666666666666664</DstInvGeoTransform>
                </GenImgProjTransformer>
                </BaseTransformer>
            </ApproxTransformer>
            </Transformer>
            <BandList>
            <BandMapping src="1" dst="1" />
            </BandList>
        </GDALWarpOptions>
    </VRTDataset>

.. _gdal_vrttut_pansharpen:

영상융합 VRT
----------------

.. versionadded:: 2.1

A VRT can describe a dataset resulting from a
`pansharpening operation <https://en.wikipedia.org/wiki/Pansharpened_image>`_
The pansharpening VRT combines a panchromatic band with several spectral bands
of lower resolution to generate output spectral bands of the same resolution as
the panchromatic band.

VRT pansharpening assumes that the panchromatic and spectral bands have the same
projection (or no projection). If that is not the case, reprojection must be done in a prior step.
Bands might have different geotransform matrices, in which case, by default, the
resulting dataset will have as extent the union of all extents.

Currently the only supported pansharpening algorithm is a "weighted" Brovey algorithm.
The general principle of this algorithm is that, after resampling the spectral bands
to the resolution of the panchromatic band, a pseudo panchromatic intensity is computed
from a weighted average of the spectral bands. Then the output value of the spectral
band is its input value multiplied by the ratio of the real panchromatic intensity
over the pseudo panchromatic intensity.

Corresponding pseudo code:

::

    pseudo_panchro[pixel] = sum(weight[i] * spectral[pixel][i] for i=0 to nb_spectral_bands-1)
    ratio = panchro[pixel] / pseudo_panchro[pixel]
    for i=0 to nb_spectral_bands-1:
        output_value[pixel][i] = input_value[pixel][i] * ratio

A valid pansharpened VRT must declare subClass="VRTPansharpenedDataset" as an
attribute of the VRTDataset top element. The VRTDataset element must have a
child **PansharpeningOptions** element. This PansharpeningOptions element must have
a **PanchroBand** child element and one of several **SpectralBand** elements.
PanchroBand and SpectralBand elements must have at least a **SourceFilename** child
element to specify the name of the dataset. They may also have a **SourceBand** child
element to specify the number of the band in the dataset (starting with 1). If not
specify, the first band will be assumed.

The SpectralBand element must generally have a **dstBand** attribute to specify the
number of the output band (starting with 1) to which the input spectral band must be mapped.
If the attribute is not specified, the spectral band will be taken into account
in the computation of the pansharpening, but not exposed as an output band.

Panchromatic and spectral bands should generally come from different datasets,
since bands of a GDAL dataset are assumed to have all the same dimensions.
Spectral bands themselves can come from one or several datasets. The only
constraint is that they have all the same dimensions.

An example of a minimalist working VRT is the following. It will generates a dataset with 3 output
bands corresponding to the 3 input spectral bands of multispectral.tif, pansharpened
with panchromatic.tif.

.. code-block:: xml

    <VRTDataset subClass="VRTPansharpenedDataset">
        <PansharpeningOptions>
            <PanchroBand>
                <SourceFilename relativeToVRT="1">panchromatic.tif</SourceFilename>
                <SourceBand>1</SourceBand>
            </PanchroBand>
            <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">multispectral.tif</SourceFilename>
                <SourceBand>1</SourceBand>
            </SpectralBand>
            <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">multispectral.tif</SourceFilename>
                <SourceBand>2</SourceBand>
            </SpectralBand>
            <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">multispectral.tif</SourceFilename>
                <SourceBand>3</SourceBand>
            </SpectralBand>
        </PansharpeningOptions>
    </VRTDataset>

In the above example, 3 output pansharpend bands will be created from the 3 declared
input spectral bands. The weights will be 1/3. Cubic resampling will be used. The
projection and geotransform from the panchromatic band will be reused for the VRT
dataset.

It is possible to create more explicit and declarative pansharpened VRT, allowing
for example to only output part of the input spectral bands (e.g. only RGB when
the input multispectral dataset is RGBNir). It is also possible to add "classic"
VRTRasterBands, in addition to the pansharpened bands.

In addition to the above mentioned required PanchroBand and SpectralBand elements,
the PansharpeningOptions element may have the following children elements :

- **Algorithm**: to specify the pansharpening algorithm. Currently, only WeightedBrovey is supported.
- **AlgorithmOptions**: to specify the options of the pansharpening algorithm. With WeightedBrovey algorithm, the only supported option is a **Weights** child element whose content must be a comma separated list of real values assigning the weight of each of the declared input spectral bands. There must be as many values as declared input spectral bands.
- **Resampling**: the resampling kernel used to resample the spectral bands to the resolution of the panchromatic band. Can be one of Cubic (default), Average, Near, CubicSpline, Bilinear, Lanczos.
- **NumThreads**: Number of worker threads. Integer number or ALL_CPUS. If this option is not set, the :decl_configoption:`GDAL_NUM_THREADS` configuration option will be queried (its value can also be set to an integer or ALL_CPUS)
- **BitDepth**: Can be used to specify the bit depth of the panchromatic and spectral bands (e.g. 12). If not specified, the NBITS metadata item from the panchromatic band will be used if it exists.
- **NoData**: Nodata value to take into account for panchromatic and spectral bands. It will be also used as the output nodata value. If not specified and all input bands have the same nodata value, it will be implicitly used (unless the special None value is put in NoData to prevent that).
- **SpatialExtentAdjustment**: Can be one of **Union** (default), **Intersection**, **None** or **NoneWithoutWarning**. Controls the behavior when panchromatic and spectral bands have not the same geospatial extent. By default, Union will take the union of all spatial extents. Intersection the intersection of all spatial extents. None will not proceed to any adjustment at all (might be useful if the geotransform are somehow dummy, and the top-left and bottom-right corners of all bands match), but will emit a warning. NoneWithoutWarning is the same as None, but in a silent way.

The below examples creates a VRT dataset with 4 bands. The first band is the
panchromatic band. The 3 following bands are than red, green, blue pansharpened
bands computed from a multispectral raster with red, green, blue and near-infrared
bands. The near-infrared bands is taken into account for the computation of the
pseudo panchromatic intensity, but not bound to an output band.

.. code-block:: xml

    <VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
        <SRS>WGS84</SRS>
        <GeoTransform>-180, 0.45, 0, 90, 0, -0.45</GeoTransform>
        <Metadata>
            <MDI key="DESCRIPTION">Panchromatic band + pan-sharpened red, green and blue bands</MDI>
        </Metadata>
        <VRTRasterBand dataType="Byte" band="1" >
            <SimpleSource>
                <SourceFilename relativeToVRT="1">world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
            </SimpleSource>
        </VRTRasterBand>
        <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
            <ColorInterp>Red</ColorInterp>
        </VRTRasterBand>
        <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
            <ColorInterp>Green</ColorInterp>
        </VRTRasterBand>
        <VRTRasterBand dataType="Byte" band="4" subClass="VRTPansharpenedRasterBand">
            <ColorInterp>Blue</ColorInterp>
        </VRTRasterBand>
        <BlockXSize>256</BlockXSize>
        <BlockYSize>256</BlockYSize>
        <PansharpeningOptions>
            <Algorithm>WeightedBrovey</Algorithm>
            <AlgorithmOptions>
                <Weights>0.25,0.25,0.25,0.25</Weights>
            </AlgorithmOptions>
            <Resampling>Cubic</Resampling>
            <NumThreads>ALL_CPUS</NumThreads>
            <BitDepth>8</BitDepth>
            <NoData>0</NoData>
            <SpatialExtentAdjustment>Union</SpatialExtentAdjustment>
            <PanchroBand>
                <SourceFilename relativeToVRT="1">world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
            </PanchroBand>
            <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">world_rgbnir.tif</SourceFilename>
                <SourceBand>1</SourceBand>
            </SpectralBand>
            <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">world_rgbnir.tif</SourceFilename>
                <SourceBand>2</SourceBand>
            </SpectralBand>
                <SpectralBand dstBand="4">
                <SourceFilename relativeToVRT="1">world_rgbnir.tif</SourceFilename>
                <SourceBand>3</SourceBand>
            </SpectralBand>
            <SpectralBand> <!-- note the absence of the dstBand attribute, to indicate
                                that the NIR band is not bound to any output band -->
                <SourceFilename relativeToVRT="1">world_rgbnir.tif</SourceFilename>
                <SourceBand>4</SourceBand>
            </SpectralBand>
        </PansharpeningOptions>
    </VRTDataset>

다중 차원 VRT
---------------------

.. versionadded:: 3.1

See the dedicated :ref:`vrt_multidimensional` page.

.. toctree::
   :maxdepth: 1
   :hidden:

   vrt_multidimensional

vrt:// 연결 문자열
------------------------

.. versionadded:: 3.1

In some contexts, it might be useful to benefit from features of VRT without
having to create a file or to provide the rather verbose VRT XML content as
the connection string. For that purpose, the following URI syntax is supported for
the dataset name since GDAL 3.1

::

    vrt://{path_to_gdal_dataset}?[bands=num1,...,numN]

For example:

::

    vrt://my.tif?bands=3,2,1

The only supported option currently is bands. Other may be added in the future.

The effect of this option is to change the band composition. The values specified
are the source band numbers (between 1 and N), possibly out-of-order or with repetitions.
The ``mask`` value can be used to specify the global mask band. This can also
be seen as an equivalent of running `gdal_translate -of VRT -b num1 ... -b numN`.

멀티스레딩 문제점
----------------------

.. warning::

    The below section applies to GDAL <= 2.2. Starting with GDAL 2.3, the use
    of VRT datasets is subject to the standard GDAL dataset multi-threaded rules
    (that is a VRT dataset handle may only be used by a same thread at a time,
    but you may open several dataset handles on the same VRT file and use them
    in different threads)

When using VRT datasets in a multi-threading environment, you should be
careful to open the VRT dataset by the thread that will use it afterwards. The
reason for that is that the VRT dataset uses :cpp:func:`GDALOpenShared` when opening the
underlying datasets. So, if you open twice the same VRT dataset by the same
thread, both VRT datasets will share the same handles to the underlying
datasets.

The shared attribute, on the SourceFilename indicates whether the
dataset should be shared (value is 1) or not (value is 0). The default is 1.
If several VRT datasets referring to the same underlying sources are used in a multithreaded context,
shared should be set to 0. Alternatively, the VRT_SHARED_SOURCE configuration
option can be set to 0 to force non-shared mode.

성능 고려 사항
--------------------------

A VRT can reference many (hundreds, thousands, or more) datasets. Due to
operating system limitations, and for performance at opening time, it is
not reasonable/possible to open them all at the same time. GDAL has a "pool"
of datasets opened by VRT files whose maximum limit is 100 by default. When it
needs to access a dataset referenced by a VRT, it checks if it is already in
the pool of open datasets. If not, when the pool has reached its limit, it closes
the least recently used dataset to be able to open the new one. This maximum
limit of the pool can be increased by setting the :decl_configoption:`GDAL_MAX_DATASET_POOL_SIZE`
configuration option to a bigger value. Note that a typical user process on
Linux is limited to 1024 simultaneously opened files, and you should let some
margin for shared libraries, etc...
gdal_translate and gdalwarp, by default, increase the pool size to 450.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

