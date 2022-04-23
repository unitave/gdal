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
  이 요소는 VRTDataset 전체, 또는 VRTRasterBand와 관련된 메타데이터 이름/값 쌍들의 목록을 담고 있습니다. 이 요소는 <MDI>(metadata item) 하위 요소를 가지고 있는데, 이 하위 요소는 "key" 속성과 그 값을 데이터로 가지고 있습니다. Metadata 요소는 여러 번 반복될 수 있는데 이 경우 반드시 메타데이터 도메인의 이름을 나타내는 "domain" 속성과 함께 쓰여야만 합니다.

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

- **SourceFilename**:
  이 밴드의 데이터를 담고 있는 RAW 파일의 이름입니다. relativeToVRT 속성을 사용해서 SourceFilename이 .vrt 파일과 관련되어 있는지 (속성값이 1) 아닌지 (속성값이 0) 나타낼 수 있습니다.

- **ImageOffset**:
  이 이미지 밴드의 데이터의 첫 번째 픽셀의 시작점에 적용할 바이트 단위 오프셋입니다. 기본값은 0입니다.

- **PixelOffset**:
  어떤 픽셀의 시작점과 같은 라인에 있는 다음 픽셀의 시작점에 적용할 바이트 단위 오프셋입니다. 패킹된 단일 밴드 데이터에서는 이 값이 **dataType** 의 바이트 단위 크기가 될 것입니다.

- **LineOffset**:
  어떤 데이터의 스캔 라인 시작점과 다음 데이터 스캔 라인 시작점에 적용할 바이트 단위 오프셋입니다. 패킹된 단일 밴드 데이터에서는 이 값이 PixelOffset * rasterXSize가 될 것입니다.

- **ByteOrder**:
  디스크 상에 있는 데이터의 바이트 순서를 정의합니다. 인텔 x86 시스템의 네이티브 바이트 순서인 LSB(최하위 바이트 우선) 또는 모토로라나 SPARC 시스템의 네이티브 바이트 순서인 MBS(최상위 바이트 우선) 가운데 하나입니다. 기본값은 로컬 머신이 사용하는 바이트 순서입니다.

기타 메모:

- 디스크 상에 있는 이미지 데이터는 VRTRawRasterBand의 밴드 **dataType** 과 동일한 데이터 유형이라고 가정합니다.

- 색상표, 메타데이터, NODATA 값, 색상 해석을 포함, VRTRasterBand의 소스 속성이 아닌 모든 속성들을 지원합니다.

- VRTRawRasterBand는 래스터의 제자리(in-place) 업데이트를 지원하지만, 소스 기반 VRTRasterBand는 항상 읽기 전용입니다.

- OpenEV 도구는 GUI에 RAW 래스터 파일을 살명하는 파라미터를 입력해서 그에 대응하는 .vrt 파일을 생성할 수 있는 파일 메뉴 옵션을 가지고 있습니다.

- .vrt 파일 하나에 있는 다중 밴드가 동일한 RAW 파일로부터 가져온 것일 수도 있습니다. 각 밴드의 ImageOffset, PixelOffset 및 LineOffset이 해당 특정 밴드의 픽셀에 어울리는지만 확인하십시오.

다음은 400x300 RGB 픽셀 교차삽입 이미지의 예시입니다.

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

VRT 드라이버는 몇 가지 방법으로 VRT 데이터셋을 생성할 수 있습니다. VRT 클래스에 직접 접근하려면 :file:`vrtdataset.h` 헤더 파일을 GDAL 핵심 헤더 파일과 함께 설치해야 합니다. 하지만 그러지 않더라도 표준 GDAL 인터페이스를 통해 대부분의 케이퍼빌리티를 계속 사용할 수 있습니다.

기존 데이터셋의 복사본인 VRT 데이터셋을 생성하려면 :cpp:func:`GDALDriver::CreateCopy` 메소드를 사용하십시오. 예를 들어 C++로 :file:`utm.tif` 를 :file:`wrk.vrt` 파일로 복사하려면 다음 명령어를 사용하면 됩니다:

.. code-block:: cpp

  GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
  GDALDataset *poSrcDS, *poVRTDS;

  poSrcDS = (GDALDataset *) GDALOpenShared( "utm.tif", GA_ReadOnly );

  poVRTDS = poDriver->CreateCopy( "wrk.vrt", poSrcDS, FALSE, NULL, NULL, NULL );

  GDALClose((GDALDatasetH) poVRTDS);
  GDALClose((GDALDatasetH) poSrcDS);

소스 데이터셋을 열 때 :cpp:func:`GDALOpenShared` 함수를 이용한다는 사실을 기억하십시오. 이 상황에서 :cpp:func:`GDALOpenShared` 사용을 권장하는 이유는 VRT 데이터셋 자체를 닫기 전에 VRT 데이터셋을 명확하게 가리키는 참조를 배포할 수 있기 때문입니다. 다시 말하자면 이 예시에서는 마지막 두 줄을 서로 바꿀 수 있지만, :cpp:func:`GDALOpen` 함수로 소스 데이터셋을 여는 경우 소스 데이터셋을 닫기 전에 VRT 데이터셋을 닫아야 합니다.

실제 파일로부터 텍스트를 읽어올 필요 없이 산출되는 :file:`wrk.vrt` 의 VRT XML을 가져오려면, 비어 있는 파일명을 가진 새 데이터셋을 열어서 "xml:VRT" 메타데이터 도메인을 사용하도록 앞의 코드를 수정하면 됩니다.

.. code-block:: cpp

  // 빈 파일명
  poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

  // VRT 파일에 담길 실제 XML 텍스트를 가져오기
  const char *xmlvrt = poVRTDS->GetMetadata("xml:VRT")[0];

다른 포맷에서는 변경하기 어려운 경우가 많은 메타데이터 또는 좌표계 같은 몇몇 속성을 추가 또는 변경해서 데이터셋의 가상 복사본을 생성하려면 다음 명령어 예시를 따라해도 됩니다. 이 경우, "메모리에" 비어 있는 파일명을 가진 가상 데이터셋을 가상으로 생성한 다음, :cpp:func:`GDALDriver::CreateCopy` 함수에 수정된 소스로 전송해서 TIFF 포맷으로 작성하게 합니다.

.. code-block:: cpp

  poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

  poVRTDS->SetMetadataItem( "SourceAgency", "United States Geological Survey");
  poVRTDS->SetMetadataItem( "SourceDate", "July 21, 2003" );

  poVRTDS->GetRasterBand( 1 )->SetNoDataValue( -999.0 );

  GDALDriver *poTIFFDriver = (GDALDriver *) GDALGetDriverByName( "GTiff" );
  GDALDataset *poTiffDS;

  poTiffDS = poTIFFDriver->CreateCopy( "wrk.tif", poVRTDS, FALSE, NULL, NULL, NULL );

  GDALClose((GDALDatasetH) poTiffDS);

이 예시에서는 NODATA 값을 -999로 설정했습니다. 어떤 밴드에 :cpp:func:`GDALRasterBand::SetMetadataItem` 함수를 사용하면 VRT 데이터셋의 해당 밴드에 있는 HideNoDataValue 요소를 설정할 수 있습니다.

.. code-block:: cpp

  poVRTDS->GetRasterBand( 1 )->SetMetadataItem( "HideNoDataValue" , "1" );

다음 예시에서는 :cpp:func:`GDALDriver::Create` 메소드로 가상 데이터셋을 생성하고 프로그램을 짜서 밴드와 소스를 추가하지만, 여전히 "일반" API를 통해 작업합니다. VRT 데이터셋의 특별한 속성은 특별 대상 도메인 "new_vrt_sources"를 대상으로 :cpp:func:`GDALRasterBand::SetMetadataItem` 함수에 소스를 서술하는 XML을 전송하면 VRTRasterBand에 (그러나 VRTRawRasterBand에는 불가능합니다) 소스를 추가할 수 있다는 점입니다. "vrt_sources" 대상 도메인도 사용할 수 있겠지만, 이 경우 새 소스를 추가하기 전에 모든 기존 소스를 폐기할 것입니다. 다음은 SimpleSource를 사용하는 대신 단순 평균 필터 소스를 구성하는 예시입니다.

.. code-block:: cpp

    // 단순 3x3 평균 필터 커널 소스 용 XML 구성.
    const char *pszFilterSourceXML  =
    "<KernelFilteredSource>"
    "  <SourceFilename>utm.tif</SourceFilename><SourceBand>1</SourceBand>"
    "  <Kernel>"
    "    <Size>3</Size>"
    "    <Coefs>0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111</Coefs>"
    "  </Kernel>"
    "</KernelFilteredSource>";

    // 가상 데이터셋 생성.
    poVRTDS = poDriver->Create( "", 512, 512, 1, GDT_Byte, NULL );
    poVRTDS->GetRasterBand(1)->SetMetadataItem("source_0",pszFilterSourceXML,
                                                "new_vrt_sources");

어떤 데이터소스를 입력하더라도 3x3 평균 필터로 필터링된 복사본을 생산할, 좀 더 일반적인 예시는 다음과 같이 보일 겁니다. 이 경우 `cpp:func:`GDALDriver::CreateCopy` 메소드가 생성한 SimpleSource를 대체하기 위해 일부러 "vrt_sources" 도메인에 필터링된 데이터소스를 설정했습니다. `cpp:func:GDALDriver::CreateCopy` 를 사용한 이유는 소스 데이터셋으로부터 나온 다른 메타데이터, 지리참조 정보 등등을 보전하기 위해서입니다. 이 예시에서 변경하는 정보는 각 밴드의 데이터소스뿐입니다.

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

:cpp:class:`VRTDataset` 클래스는 :cpp:func:`GDALDataset::AddBand` 메소드를 지원하도록 구현된 몇 안 되는 데이터셋 가운데 하나입니다. :cpp:func:`GDALDataset::AddBand` 메소드에 전송되는 옵션들을 사용해서 생성되는 밴드의 유형을 (VRTRasterBand, VRTRawRasterBand, VRTDerivedRasterBand) 제어하고, VRTRawRasterBand로 설정한 경우 다양한 파라미터를 설정할 수 있습니다. 표준 VRTRasterBand로 설정한다면 앞의 :cpp:func:`GDALRasterBand::SetMetadataItem` 예시를 이용해서 소스를 지정해야 할 것입니다.

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

소스 밴드로부터 픽셀 정보를 파생시킨 '파생' 밴드라는 특화된 밴드 유형이 있습니다. 이 밴드 유형을 사용한다면 산출 래스터를 생성할 책임을 지는 픽셀 함수도 지정해야만 합니다. 응용 프로그램으로 이 픽셀 함수를 작성한 다음, 유일(unique) 키를 이용해서 GDAL에 등록합니다.

파생 밴드를 이용하면 디스크 상에 새 밴드 파일을 생성할 필요없이 밴드를 실시간으로(on-the-fly) 조작하는 VRT 데이터셋을 생성할 수 있습니다. 예를 들면, 어떤 상수 y와 밴드 9개를 가진 입력 데이터셋으로부터 나온 밴드 4개를 (x0, x3, x4, 및 x8) 이용해서 밴드 1개를 생성하고 싶은 경우:

.. code-block:: c

  band_value = sqrt((x3*x3+x4*x4)/(x0*x8)) + y;

이 값을 계산할 픽셀 함수를 작성한 다음 "MyFirstFunction"이라는 이름으로 GDAL에 등록할 수 있습니다. 그러면 다음 VRT XML을 사용해서 이 파생 밴드를 출력할 수 있습니다:

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

    PixelFunctionArguments는 GDAL 3.4 이상 버전에서만 C++ 픽셀 함수와 함께 사용할 수 있습니다.

subClass(VRTDerivedRasterBand) 지정 및 PixelFunctionType 값뿐만 아니라, 편리하게 사용할 수 있는 SourceTransferType이라는 또다른 새 파라미터도 있습니다. 일반적으로 파생 밴드의 데이터 유형을 이용해서 소스 래스터를 가져옵니다. 하지만 생성되는 데이터 유형보다 더 높은 해상도를 가진 소스 데이터에 접근할 수 있는 픽셀 함수가 필요한 경우가 있을 수도 있습니다. 예를 들면 "CFloat32" 또는 "CFloat64" 유형의 단일 소스를 취해서 허수(imaginary) 부분만 반환하는 "Float" 유형의 파생 밴드가 있을 수도 있습니다. 이런 파생 밴드를 생성하려면, SourceTransferType을 "CFloat64"로 설정하십시오. 그렇지 않으면 픽셀 함수를 호출하기 전에 소스를 "Float" 유형으로 변환할 것이고, 그러면 허수 부분이 사라질 것입니다.

.. code-block:: xml

    <VRTDataset rasterXSize="1000" rasterYSize="1000">
        <VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">
            <Description>Magnitude</Description>
            <PixelFunctionType>MyFirstFunction</PixelFunctionType>
            <SourceTransferType>CFloat64</SourceTransferType>
            ...

기본 픽셀 함수
+++++++++++++++++++++++

GDAL은 새로운 코드를 짤 필요없이 사용할 수 있는 기본 픽셀 함수들의 집합을 제공합니다:


.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - PixelFunctionType
     - 입력 소스 개수
     - PixelFunctionArguments
     - 설명
   * - **cmul**
     - 2
     - -
     - 첫 번째 밴드에 두 번째 밴드의 복소 켤레(complex conjugate)를 곱합니다.
   * - **complex**
     - 2
     - -
     - 실수 및 허수 값으로 쓰이는 밴드 2개를 병합시켜 복소수형 밴드를 생성합니다.
   * - **conj**
     - 1
     - -
     - 단일 래스터 밴드의 복소 켤레를 계산합니다. (입력물이 복소수형이 아닌 경우 그냥 복사합니다.)
   * - **dB**
     - 1
     - ``fact`` (선택적)
     - (실수형 또는 복소수형) 단일 래스터 밴드의 절대값을 dB로 변환합니다:
       ``20. * log10( abs( x ) )``. 선택적인 ``fact`` 파라미터를 ``10`` 으로 설정하면 대체 공식 ``10. * log10( abs( x ) )`` 를 사용합니다.
   * - **dB2amp**
     - 1
     - -
     - 로그 값으로부터 선형 값으로 (진폭amplitude) 척도 변환합니다. (예: (실수형인 경우에만) 단일 래스터 밴드의 ``10 ^ ( x / 20 )`` ) 이 함수는 GDAL 3.5버전부터 중요도가 떨어져 더 이상 사용되지 않고 앞으로는 사라지게 될 것입니다. 예를 들면 ``base = 10.`` 과 ``fact = 0.05`` 를 사용해서 ``exp`` 픽셀 함수를 ``1./20`` 로 사용하십시오.
   * - **dB2pow**
     - 1
     - -
     - 로그 값으로부터 선형 값으로 (거듭제곱) 척도 변환합니다. perform scale conversion from logarithmic to linear (power) (예: (실수형인 경우에만) 단일 래스터 밴드의 ``10 ^ ( x / 10 )`` ) 이 함수는 GDAL 3.5버전부터 중요도가 떨어져 더 이상 사용되지 않고 앞으로는 사라지게 될 것입니다. 예를 들면 ``base = 10.`` 과 ``fact = 0.1`` 을 사용해서 ``exp`` 픽셀 함수를 ``1./10`` 로 사용하십시오.
   * - **diff**
     - 2
     - -
     - 래스터 밴드 2개의 차를 계산합니다. (``b1 - b2``)
   * - **div**
     - 2
     - -
     - 래스터 밴드를 다른 래스터 밴드로 나눕니다. (``b1 / b2``)
   * - **exp**
     - 1
     - ``base`` (선택적), ``fact`` (선택적)
     - (실수값을 가진) 입력 밴드 ``x`` 에 있는 각 요소의 지수(exponential)를 계산합니다:
       ``e ^ x``.
       이 함수는 다음 2개의 선택적인 파라미터도 입력받습니다:
       일반화된 공식 ``base ^ ( fact * x )`` 를 계산할 수 있게 해주는 ``base`` 및 ``fact`` 입니다.
       주의: 로그 척도(dB)를 변환할 때 이 함수를 사용할 것을 권장합니다. 이 경우 예를 들면 ``base = 10.`` 과 ``fact = 0.05`` 를 사용해서 ``1./20`` 로 사용하십시오.
   * - **imag**
     - 1
     - -
     - 단일 래스터 밴드로부터 허수 부분을 추출합니다. (복소수형이 아닌 경우 0을 반환합니다.)
   * - **intensity**
     - 1
     - -
     - (실수형 또는 복소수형) 단일 래스터 밴드의 강도(intensity) ``Re( x * conj(x) )`` 를 계산합니다.
   * - **interpolate_exp**
     - >= 2
     - ``t0``, ``dt``, ``t``
     - 입력 소스가 ``t0`` 위치에서 ``dt`` 간격으로 시작하는 경우 지수 보간법을 이용해서 ``t`` 시간(또는 위치)의 값을 보간합니다.
   * - **interpolate_linear**
     - >= 2
     - ``t0``, ``dt``, ``t``
     - 입력 소스가 ``t0`` 위치에서 ``dt`` 간격으로 시작하는 경우 선형 보간법을 이용해서 ``t`` 시간(또는 위치)의 값을 보간합니다.
   * - **inv**
     - 1
     - ``k`` (선택적)
     - 역함수 ``1./x`` 입니다. 선택적인 ``k`` 파라미터를 설정한 경우 결과값에 ``k`` 를 곱합니다(``k / x``).
   * - **log10**
     - 1
     - -
     - (실수형 또는 복소수형) 단일 래스터 밴드의 절대값의 상용로그(십진로그)를 계산합니다: ``log10( abs( x ) )``
   * - **mod**
     - 1
     - -
     - (실수형 또는 복소수형) 단일 래스터 밴드로부터 모듈을 추출합니다.
   * - **mul**
     - >= 2
     - ``k`` (선택적)
     - 2개 이상의 래스터 밴드들을 곱합니다. 선택적인 ``k`` 파라미터를 설정한 경우 결과값에 스칼라(scalar) ``k`` 를 곱합니다.
   * - **phase**
     - 1
     - -
     - [-PI,PI] 범위의 단일 래스터 밴드로부터 위상(phase)을 추출합니다. (복소수형이 아닌 경우 0 또는 PI를 반환합니다.)
   * - **polar**
     - 2
     - ``amplitude_type`` (선택적)
     - 입력 밴드를 이용해서 진폭 및 위상 값 ``b1 * exp( j * b2 )`` 를 위한 복소수형 밴드를 생성합니다.
       선택적인 (문자열) 파라미터 ``amplitude_type`` 은 ``AMPLITUDE`` (기본값), ``INTENSITY`` 또는 ``dB`` 가운데 하나로 설정할 수 있습니다.
       주의: ``amplitude_type`` 을 ``INTENSITY`` 로 설정한 경우 음의 값을 0에서 자릅니다.
   * - **pow**
     - 1
     - ``power``
     - 단일 래스터 밴드를 ``power`` 인자가 지정하는 거듭제곱 상수로 승격시킵니다. (실수형 전용)
   * - **real**
     - 1
     - -
     - 단일 래스터 밴드로부터 실수 부분을 추출합니다. (입력물이 복소수형이 아닌 경우 그냥 복사합니다.)
   * - **sqrt**
     - 1
     - -
     - 단일 래스터 밴드의 제곱근을 계산합니다. (실수형 전용)
   * - **sum**
     - >= 2
     - ``k`` (선택적)
     - 2개 이상의 래스터 밴드들을 더합니다. 선택적인 ``k`` 파라미터를 설정한 경우 결과값의 각 요소에 ``k`` 를 더합니다.
   * - **replace_nodata**
     - = 1
     - ``to`` (선택적)
     - 입력되는 ``NODATA`` 값을 새 값 -- 기본값은 IEEE 754 `nan` -- 으로 변환합니다.
   * - **scale**
     - = 1
     - -
     - 래스터 밴드의 ``offset`` 및 ``scale`` 값에 따라 크기 조정 작업을 수행합니다.

픽셀 함수 작성하기
+++++++++++++++++++++++

응용 프로그램은 (픽셀 함수를 이용하는 파생 밴드를 가진 VRT 데이터셋에 접근하기 전에) GDAL에 이 함수를 등록하기 위해 키와 :cpp:type:`GDALDerivedPixelFuncWithArgs` 로 :cpp:func:`GDALAddDerivedBandPixelFuncWithArgs` 를 호출합니다:

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

GDAL 드라이버를 등록한 경우 응용 프로그램이 시작할 때 호출하는 것이 좋습니다. ``pszMetadata`` 파라미터는 선택적이며 ``nullptr`` 일 수 있습니다. 이 파라미터를 사용하면 사용자에게 함수 서명(function signature)을 선언할 수 있고 데이터셋의 파라미터들 외에 추가적인 파라미터를 요청할 수 있습니다.

:cpp:type:`GDALDerivedPixelFuncWithArgs` 는 :cpp:func:`GDALRasterBand::IRasterIO` 와 비슷한 서명으로 정의됩니다:


.. cpp:function:: CPLErr TestFunction(void** papoSources, int nSources, void* pData, int nBufXSize, int nBufYSize, GDALDataType eSrcType, GDALDataType eBufType, int nPixelSpace, int nLineSpace, CSLConstList papszArgs)

   :param papoSources: 패킹된 래스터를 가리키는 포인트입니다. 소스 당 1개를 사용할 수 있습니다. 모든 데이터 유형은 ``eSrcType`` 파라미터에 지정된 유형과 동일할 것입니다.

   :param nSources: 소스 래스터의 개수입니다.

   :param pData: 해당 버퍼로 데이터를 읽어와야 할 버퍼, 또는 해당 버퍼로부터 데이터를 작성해야 할 버퍼입니다. 이 버퍼는 eBufType 유형의 워드(word)를 최소한 ``nBufXSize * nBufYSize`` 개 담고 있어야만 합니다. 이 버퍼는 좌측에서 우측, 상단에서 하단 픽셀 순서 구조입니다. ``nPixelSpace`` 및 ``nLineSpace`` 파라미터로 간격을 제어합니다.

   :param nBufXSize: 해당 버퍼로 원하는 영역을 읽어올 버퍼 이미지의 너비, 또는 해당 버퍼로부터 원하는 영역을 작성할 버퍼 이미지의 너비입니다.

   :param nBufYSize: 해당 버퍼로 원하는 영역을 읽어올 버퍼 이미지의 높이, 또는 해당 버퍼로부터 원하는 영역을 작성할 버퍼 이미지의 높이입니다.

   :param eSrcType: ``papoSources`` 래스터 배열에 있는 픽셀값들의 유형입니다.

   :param eBufType: 픽셀 함수가 ``pData`` 데이터 버퍼에 생성해야만 하는 픽셀값들의 유형입니다.

   :param nPixelSpace: ``pData`` 에 있는 어떤 픽셀값의 시작에서 같은 스캔 라인의 다음 픽셀값의 시작까지 적용할 바이트 단위 오프셋입니다. 기본값 0으로 설정하면 eBufType 데이터 유형의 크기를 사용합니다.

   :param nLineSpace: ``pData`` 에 있는 어떤 스캔 라인의 시작에서 다음 스캔 라인의 시작까지 적용할 바이트 단위 오프셋입니다.

   :param papszArgs: 지정한 함수 인자의 선택적인 문자열 목록입니다. (예: ``y=4``)


:cpp:func:`GDALAddDerivedBandPixelFunc` 를 사용해서 (최종 :cpp:type:`CSLConstList` 인자를 생략하는) :cpp:type:`GDALDerivedPixelFunc` 를 등록할 수도 있습니다.

다음은 픽셀 함수를 구현하는 예시입니다:

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

        // ---- 초기화 ----
        if (nSources != 4) return CE_Failure;

        const char *pszY = CSLFetchNameValue(papszArgs, "y");
        if (pszY == nullptr) return CE_Failure;

        double NoData = NAN;
        const char *pszNoData = CSLFetchNameValue(papszArgs, "NoData");
        if (pszNoData != nullptr)
        {
            NoData = std::strtod(pszNoData, &end);
            if (end == pszNoData) return CE_Failure; // 파싱할 수 없음
        }

        char *end = nullptr;
        double y = std::strtod(pszY, &end);
        if (end == pszY) return CE_Failure; // 파싱할 수 없음

        // ---- 픽셀 설정 ----
        for( iLine = 0; iLine < nYSize; iLine++ )
        {
            for( iCol = 0; iCol < nXSize; iCol++ )
            {
                ii = iLine * nXSize + iCol;
                /* SRCVAL 매크로로 소스 래스터 픽셀을 가져올 수도 있음 */
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

        // ---- 성공 반환 ----
        return CE_None;
    }

파생 밴드 사용하기 (파이썬 픽셀 함수 이용)
----------------------------------------------------

GDAL 2.2버전부터, :ref:`vrt_derived_bands` 단락에서 설명하는 C/C++로 작성된 픽셀 함수뿐만 아니라 파이썬으로 작성된 픽셀 함수도 사용할 수 있습니다. 런타임에 `CPython <https://www.python.org/>`_ 과 `NumPy <http://www.numpy.org/>`_  둘 다 필요합니다.

VRTRasterBand의 하위 요소들은 다음과 같습니다(VRTRasterBand의 subClass가 반드시 VRTDerivedRasterBand로 설정돼 있어야만 합니다):

- **PixelFunctionType**: (필수)
  PixelFunctionCode 요소에 그때 그때 즉시 처리되는(in-line) 파이썬 모듈로 정의될 함수 이름으로, 또는 외부 파이썬 모듈에 있는 함수를 참조하는 "module_name.function_name" 형식의 함수 이름으로 설정해야만 합니다.

- **PixelFunctionLanguage**: (필수)
  Python으로 설정해야만 합니다.

- **PixelFunctionCode**: (PixelFunctionType이 "function_name" 형식인 경우 필수, 아니라면 무시)
  파이썬 모듈의 그때 그때 즉시 처리되는(in-line) 코드입니다. 적어도 PixelFunctionType이 지정한 이름의 함수를 가지고 있어야만 합니다.

- **BufferRadius**: (선택적, 기본값은 0)
  원본 RasterIO() 요청을 만족시키기 위해 픽셀 함수에 전송되는 입력 및 산출 버퍼의 좌측, 우측, 하단 및 상단에서 가져올 추가 픽셀들의 양입니다. 이 버퍼 구역의 산출 버퍼의 값들을 무시할 것이라는 사실을 기억하십시오.

파이썬 픽셀 함수의 서명은 다음 인자들을 가지고 있어야만 합니다:

- **in_ar**:
  입력 NumPy 배열의 목록입니다. (각 소스 당 NumPy 배열 1개입니다.)

- **out_ar**:
  채워야 할 산출 NumPy 배열입니다. VRTRasterBand.dataType을 통해 입력 배열 차원과 동일한 차원으로 배열을 초기화합니다.

- **xoff**:
  밴드에서 접근한 영역의 좌상단 모서리에 적용할 픽셀 단위 오프셋입니다. 처리 과정이 래스터의 픽셀 위치에 따라 달라지는 경우가 아니라면 일반적으로는 필요하지 않습니다.

- **yoff**:
  밴드에서 접근한 영역의 좌상단 모서리에 적용할 라인 단위 오프셋입니다. 일반적으로는 필요하지 않습니다.

- **xsize**:
  밴드에서 접근한 영역의 영역 너비입니다. out_ar.shape[1]과 함께 사용하면 요청의 수평 리샘플링 비율을 판단할 수 있습니다.

- **ysize**:
  밴드에서 접근한 영역의 영역 높이입니다. out_ar.shape[0]과 함께 사용하면 요청의 수직 리샘플링 비율을 판단할 수 있습니다.

- **raster_xsize**:
  래스터 밴드의 총 너비입니다. 일반적으로는 필요하지 않습니다.

- **raster_ysize**:
  래스터 밴드의 총 높이입니다. 일반적으로는 필요하지 않습니다.

- **buf_radius**:
  in_ar 및 out_ar의 좌측, 우측, 상단 및 하단에 추가되는 버퍼의 (픽셀 단위) 반경입니다. 이 값은 원본 픽셀 요청을 지정하는 픽셀의 양으로 확장하기 위해 설정할 수 있는 선택적 BufferRadius 요소의 값입니다.

- **gt**:
  지리변형입니다. 더블(double)형 값 6개로 이루어진 배열입니다.

- **kwargs**:
  PixelFunctionArguments에 정의된 사용자 인자들의 딕셔너리(dictionary)입니다.

지정한 ``out_ar`` 배열은 반드시 제자리(in-place) 수정되어야만 합니다. 현재 픽셀 함수가 반환하는 어떤 값도 무시합니다.

.. note::

    다른 배열로부터 ``out_ar`` 를 채우고 싶다면, ``out_ar[:] = ...`` 문법을 사용하십시오.

예시
++++++++

- 소스 파일의 값에 1.5라는 인수를 곱하는 VRT

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

- 2개 (이상의) 래스터를 더하는 VRT

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

- 외부 라이브러리를 이용해서 음영기복을 계산하는 VRT

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

hillshading.py의 내용:

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

그때 그때 즉시 처리되는 파이썬 코드로부터 모듈을 가져오는 경우 또는 ("module_name.function_name" 형식의 PixelFunctionType 같은) OOL(out-of-line) 코드에 의존하는 경우, 파이썬 경로를 통해 모듈에 접근할 수 있는지 확인해야 합니다. 파이썬 대화형 해석기와는 반대로, GDAL에서 사용하는 경우 현재 경로를 자동으로 추가하지 않습니다. 따라서 ModuleNotFoundError 예외가 발생하면 사용자가 **PYTHONPATH** 환경설정 변수를 정의해야 할 수도 있습니다.

보안 영향
*********************

GDAL 사용자가 신뢰할 수 없을 수도 있는 데이터셋을 처리하는 경우, 파이썬 코드를 실행할 수 있는 환경은 수많은 잠재적인 취약성으로 향하는 문을 열어주는 것일 수도 있습니다. 이런 문제점을 피하려면, 기본적으로 파이썬 픽셀 함수를 실행할 수 없게 해야 합니다. :decl_configoption:`GDAL_VRT_ENABLE_PYTHON` 환경설정 옵션으로 이런 실행 정책을 제어할 수 있는데, 다음 세 가지 가운데 하나로 설정할 수 있습니다:

- YES:
  모든 VRT 스크립트를 신뢰할 수 있는 것으로 간주하고 픽셀 연산을 수반하는 경우 파이썬 픽셀 함수를 실행할 것입니다.

- NO:
  모든 VRT 스크립트를 신뢰할 수 없는 것으로 간주하고 어떤 파이썬 픽셀 함수도 실행하지 않을 것입니다.

- TRUSTED_MODULES: (기본 설정값)
  PixelFunctionCode 요소에 그때 그때 즉시 처리되는 파이썬 코드를 가지고 있는 모든 VRT 스크립트를 신뢰할 수 없는 것으로 간주하고 실행하지 않을 것입니다. VRT 스크립트가 "module_name.function_name" 형식의 PixelFunctionType을 사용한다면, :decl_configoption:`GDAL_VRT_TRUSTED_MODULES` 환경설정 옵션에 "module_name"을 사용할 수 있는 경우에만 신뢰할 수 있는 것으로 간주합니다. 이 환경설정 옵션의 값은 쉼표로 구분된 신뢰할 수 있는 모듈 이름 목록입니다. '*' 와일드카드를 문자열의 이름에 사용해서 '*' 문자 앞의 하위 문자열로 시작하는 모든 문자열 이름을 사용할 수 있습니다. 예를 들어 'every*'는 'every.thing' 또는 'everything' 모듈을 신뢰할 수 있는 모듈로 만들 것입니다. '*' 와일드카드를 모듈 또는 하위 모듈 이름과 정확하게 일치하도록 사용할 수도 있습니다. 예를 들면 'every.*'는 'every'와 'every.thing' 모듈을 신뢰할 수 있는 모듈로 만들지만, 'everything'은 신뢰할 수 없는 모듈로 만들 것입니다.

.. _linking_mechanism_to_python_interpreter:

파이썬 해석기에 메커니즘 링크하기
*****************************************

현재 CPython 2 및 3버전만 지원합니다. 빌드 시 어떤 CPython 라이브러리에도 GDAL 공유 객체를 명확하게 링크시키지 않습니다. GDAL이 파이썬 코드를 실행해야 할 경우, (프로그램 자체가 파이썬 해석기이거나, 또는 예를 들어 QGIS 같은 다른 프로그램이 이미 CPython 라이브러리를 불러온 경우처럼) 현재 프로세스에 파이썬 해석기를 불러왔는지부터 판단할 것입니다. 
그렇지 않았다면 :decl_configoption:`PYTHONSO` 환경설정 옵션이 정의되었는지 살펴볼 것입니다. 사용할 파이썬 라이브러리의 이름을 -- (일반적으로 /etc/ld.so.conf 또는 LD_LIBRARY_PATH 두 경로 가운데 하나에서) 리눅스 다이내믹 로더(dynamic loader)를 통해 접근할 수 있는 경우 "libpython2.7.so" 같은 단축명을, 아니면 "/usr/lib/x86_64-linux-gnu/libpython2.7.so" 같은 전체 경로를 -- 가리키도록 이 옵션을 설정할 수 있습니다.
윈도우 상에서도 동일합니다: PATH를 통해 접근할 수 있는 경우 "python27.dll" 같은 단축명을, 아니면 "c:\\python27\\python27.dll" 같은 전체 경로명을 설정할 수 있습니다. :decl_configoption:`PYTHONSO` 환경설정 옵션이 정의되지 않은 경우, PATH의 디렉터리들에서 "python" 바이너리를 찾아서 관련 공유 객체를 판단하려 시도할 것입니다. ("python"을 찾지 못 하는 경우 "python3"로 다시 시도할 것입니다.) 이런 방법들이 성공하지 못 했다면, 사전 정의된 공유 객체 이름 목록으로 시도할 것입니다. 이 단락 작성 당시, 2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.4, 3.3, 3.2 순서로 버전을 검색합니다. 디버그 정보를 활성화하면 (CPL_DEBUG=ON) 어떤 버전의 파이썬을 사용했는지를 출력할 것입니다.

JIT(Just-in-time) 컴파일 작업
++++++++++++++++++++++++++++

JIT(Just-in-time) 컴파일러를 사용하면 실행 시간을 상당히 단축시킬 수도 있습니다. `Numba <http://numba.pydata.org/>`_ 컴파일러가 성공적으로 테스트되었습니다. 더 나은 성능을 위해, JIT 컴파일러가 자신의 컴파일 작업을 캐시할 수도 있도록 오프라인 픽셀 함수를 사용할 것을 권장합니다.


다음 :file:`mandelbrot.py` 파일을 사용한다면:

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

(예를 들어 QGIS로 여는 데) 다음 VRT 파일을 사용할 수 있습니다:

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

왜곡(warped) VRT는 subClass="VRTWarpedDataset"인 VRTDataset입니다. 왜곡 작업 옵션을 설명하는 GDALWarpOptions 요소를 가지고 있습니다.

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

VRT는 `영상융합(pan-sharpen) 작업 <https://en.wikipedia.org/wiki/Pansharpened_image>`_ 으로부터 산출된 데이터셋을 서술할 수 있습니다. 영상융합 VRT는 입력 전정색(panchromatic) 밴드와 동일한 해상도의 산출 스펙트럼 밴드를 생성하기 위해 전정색 밴드와 더 낮은 해상도의 스펙트럼 밴드 여러 개를 융합합니다.

VRT 영상융합 작업은 전정색 밴드와 스펙트럼 밴드가 동일한 투영법을 사용한다고 (또는 투영법을 사용하지 않는다고) 가정합니다. 그렇지 않은 경우, 사전 단계에서 재투영해야만 합니다. 밴드들이 서로 다른 지리변형 행렬을 가지고 있을 수도 있는데 이 경우 기본적으로 산출되는 데이터셋이 모든 범위들을 융합한 범위를 가지게 될 것입니다.

현재 "가중치 적용(weighted)" 브로비(Brovey) 영상융합 알고리즘만 지원합니다. 이 알고리즘의 일반 원칙은 스펙트럼 밴드들을 전정색 밴드의 해상도로 리샘플링한 다음, 스펙트럼 밴드들의 가중치 적용 평균으로부터 의사 전정색의 강도(intensity)를 계산한다는 것입니다. 그러면 스펙트럼 밴드의 입력값에 실제 전정색 강도를 의사 전정색 강도로 나눈 값을 곱한 값이 해당 밴드의 산출값이 됩니다.

해당 의사(pseudo) 코드:

::

    pseudo_panchro[pixel] = sum(weight[i] * spectral[pixel][i] for i=0 to nb_spectral_bands-1)
    ratio = panchro[pixel] / pseudo_panchro[pixel]
    for i=0 to nb_spectral_bands-1:
        output_value[pixel][i] = input_value[pixel][i] * ratio

무결한 영상융합 VRT는 subClass="VRTPansharpenedDataset"을 VRTDataset의 최상위 요소의 속성으로 선언해야만 합니다. VRTDataset 요소는 **PansharpeningOptions** 하위 요소를 가지고 있어야만 합니다. 이 PansharpeningOptions 요소는 **PanchroBand** 하위 요소 하나와 **SpectralBand** 하위 요소 여러 개를 가지고 있어야만 합니다. PanchroBand 및 SpectralBand 요소는 데이터셋의 이름을 지정하는 **SourceFilename** 하위 요소를 적어도 하나 가지고 있어야만 합니다. 또한 데이터셋에 있는 밴드의 (1에서 시작하는) 번호를 지정하는 **SourceBand** 하위 요소도 가질 수 있습니다. 지정하지 않는 경우, 첫 번째 밴드라고 가정할 것입니다.

SpectralBand 요소는 일반적으로 입력 스펙트럼 밴드를 매핑시켜야만 하는 산출 밴드의 (1에서 시작하는) 번호를 지정하는 **dstBand** 속성을 반드시 가지고 있어야만 합니다. 이 속성을 지정하지 않는 경우, 영상융합 연산에 스펙트럼 밴드를 넣지만 산출 밴드로 노출시키지 않을 것입니다.

전정색 및 스펙트럼 밴드는 일반적으로 서로 다른 데이터셋으로부터 가져와야 합니다. GDAL 데이터셋의 밴드들은 모두 동일한 차원을 가진다고 가정하기 때문입니다. 스펙트럼 밴드들 자체도 데이터셋 하나 또는 여러 개로부터 가져온 것일 수 있습니다. 유일한 제약은 스펙트럼 밴드들이 모두 동일한 차원을 가져야 한다는 것입니다.

다음은 최소한으로 작동하는 VRT의 예시입니다. 이 VRT 스크립트는 multispectral.tif의 입력 스펙트럼 밴드 3개에 대응하는 산출 밴드 3개와 영상융합된 panchromatic.tif를 가진 데이터셋을 생성할 것입니다:

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

이 예시에서, 선언된 입력 스펙트럼 밴드 3개로부터 산출 영상융합 밴드 3개를 생성할 것입니다. 가중치는 1/3일 것입니다. 3차(cubic) 리샘플링 메소드를 사용할 것입니다. VRT 데이터셋에 전정색 밴드로부터 나온 투영법 및 지리변형을 재사용할 것입니다.

더 명확하고 선언적인 영상융합 VRT를 생성해서, 예를 들어 입력 스펙트럼 밴드의 일부만 산출하도록 할 수도 있습니다. (예를 들어 입력 다중 스펙트럼 데이터셋이 RGBNir 유형인 경우 RGB만 산출하도록 할 수 있습니다.) 영상융합 밴드에 "전형적인" VRTRasterBands를 추가할 수도 있습니다.

PansharpeningOptions 요소는 앞에서 언급했던 필수적인 PanchroBand와 SpectralBand 요소들만이 아니라, 다음과 같은 하위 요소들을 가질 수도 있습니다:

- **Algorithm**:
  영상융합 알고리즘을 지정합니다. 현재 WeightedBrovey만 지원합니다.

- **AlgorithmOptions**:
  영상융합 알고리즘의 옵션들을 지정합니다. WeightedBrovey 알고리즘이 지원하는 옵션은 **Weights** 하위 요소 하나뿐입니다. 이 하위 요소의 내용은 선언된 입력 스펙트럼 밴드 각각에 가중치를 할당하는 실수값들을 쉼표로 구분한 목록이어야만 합니다. 이 실수값들의 개수와 선언된 입력 스펙트럼 밴드들의 개수가 일치해야만 합니다.

- **Resampling**:
  스펙트럼 밴드들을 전정색 밴드의 해상도로 리샘플링하기 위해 쓰이는 리샘플링 커널을 지정합니다. Cubic(기본값), Average, Near, CubicSpline, Bilinear, Lanczos 가운데 하나로 지정할 수 있습니다.

- **NumThreads**:
  작업자 스레드의 개수를 지정합니다. 정수값 또는 ALL_CPUS로 지정할 수 있습니다. 이 옵션을 설정하지 않는 경우, :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 쿼리할 것입니다. (이 환경설정 옵션의 값도 정수값 또는 ALL_CPUS로 설정할 수 있습니다.)

- **BitDepth**:
  전정색 및 스펙트럼 밴드의 비트 심도를 (예: 12로) 지정할 수 있습니다. 이 요소를 지정하지 않는 경우, 전정색 밴드의 NBITS 메타데이터 항목이 존재한다면 그 값을 사용할 것입니다.

- **NoData**:
  전정색 및 스펙트럼 밴드 연산에 넣을 NODATA 값을 지정합니다. 산출물 NODATA 값으로도 사용될 것입니다. (다음과 같은 상황을 막기 위해 NoData 요소에 특별한 None 값을 넣지 않는 한) 이 요소를 지정하지 않았는데 모든 입력 밴드의 NODATA 값이 동일한 경우, 암묵적으로 그 값을 사용할 것입니다.

- **SpatialExtentAdjustment**:
  **Union** (기본값), **Intersection**, **None** 또는 **NoneWithoutWarning** 가운데 하나를 지정할 수 있습니다. 전정색 및 스펙트럼 밴드가 동일한 지리공간 범위를 가지고 있지 않은 경우의 습성을 제어합니다. 기본적으로, Union은 모든 공간 범위를 통합합니다. Intersection은 모든 공간 범위가 중첩하는 범위입니다. None은 어떤 조정도 진행하지 않지만 (어째서인지 지리변형이 더미(dummy)이고 모든 밴드의 좌상단과 우하단 모서리가 일치하는 경우 유용할 수도 있습니다) 경고를 발할 것입니다. NoneWithoutWarning 은 None과 동일하지만 경고를 발하지 않습니다.

다음 예시는 밴드 4개를 가진 VRT 데이터셋을 생성합니다. 첫 번째 밴드가 전정색 밴드입니다. 그 뒤의 밴드 3개는 적색, 녹색, 청색 및 근적외선 밴드를 가진 다중 스펙트럼 래스터로부터 계산된 적색, 녹색, 청색 영상융합 밴드들입니다. 의사 전정색 강도 계산에 근적외선 밴드도 들어가지만, 산출 밴드로 생성되지는 않습니다.

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

전용 :ref:`vrt_multidimensional` 페이지를 참조하십시오.

.. toctree::
   :maxdepth: 1
   :hidden:

   vrt_multidimensional

vrt:// 연결 문자열
------------------------

.. versionadded:: 3.1

어떤 맥락에서는, 파일을 생성할 필요없이 VRT의 기능을 사용하거나 또는 조금 장황한 VRT XML 내용을 연결 문자열로 제공하는 편이 유용할 수도 있습니다. 이런 목적으로, GDAL 3.1버전부터 데이터셋 이름을 지정하는 다음과 같은 URI 문법을 지원합니다.

::

    vrt://{path_to_gdal_dataset}?[bands=num1,...,numN]

다음은 그 예시입니다:

::

    vrt://my.tif?bands=3,2,1

현재 지원하는 옵션은 bands뿐입니다. 향후 다른 옵션들이 추가될 수도 있습니다.

이 옵션은 밴드 구성을 변경하는 효과를 냅니다. 지정한 값들은 소스 밴드의 (1에서 N 사이의) 번호로, 순서를 그대로 따라갈 수도 있고 뒤섞을 수도 있습니다. 전체 수준 마스크 밴드를 지정하려면 ``mask`` 값을 쓰면 됩니다. *gdal_translate -of VRT -b num1 ... -b numN* 명령어를 실행하는 것과 동일하다고 볼 수도 있습니다.

멀티스레딩 문제점
----------------------

.. warning::

    다음 단락은 GDAL 2.2 이하 버전에 적용됩니다. GDAL 2.3버전부터, VRT 데이터셋 사용 시 표준 GDAL 데이터셋 멀티스레드 작업 규칙을 따릅니다. (즉 동일한 스레드에서는 한번에 VRT 데이터셋 하나씩 처리할 수 있다는 뜻이지만, 동일한 VRT 파일에 데이터셋 핸들 여러 개를 열어서 서로 다른 스레드에서 사용할 수도 있습니다.)

멀티스레딩 환경에서 VRT 데이터셋을 사용하는 경우, 나중에 해당 VRT 데이터셋을 사용할 스레드에서 VRT 데이터셋을 여는 것을 조심해야 합니다. 그 이유는 VRT 데이터셋이 기저 데이터셋을 열 때 :cpp:func:`GDALOpenShared` 함수를 이용하기 때문입니다. 즉, 동일한 스레드에서 동일한 VRT 데이터셋을 두 번 열 경우, 두 VRT 데이터셋 모두 기저 데이터셋에 동일한 핸들을 공유하게 되기 때문입니다.

SourceFilename에서 shared 속성이 데이터셋을 공유해야 할지 (속성값은 1) 또는 공유하지 말아야 할지를 (속성값은 0) 나타냅니다. 기본값은 1입니다.
멀티스레드 맥락에서 동일한 기저 소스를 참조하는 VRT 데이터셋 여러 개를 사용하는 경우, shared 속성을 0으로 설정해야 합니다. 아니면 비공유 모드를 강제하기 위해 VRT_SHARED_SOURCE 환경설정 옵션을 0으로 설정할 수도 있습니다.

성능 고려 사항
--------------------------

VRT는 수많은 (수백, 수천, 또는 그 이상의) 데이터셋을 참조할 수 있습니다. 운영 체제의 제한에 의해, 그리고 VRT 파일을 열 때의 성능을 위해, 동시에 참조 데이터셋 전부를 여는 것은 타당하지도 가능하지도 않습니다. GDAL은 기본적으로 VRT 파일이 열 수 있는 데이터셋 "풀(pool)"의 최대 한계값을 100개로 제한합니다. GDAL이 VRT가 참조하는 데이터셋에 접근해야 하는 경우, GDAL은 해당 데이터셋이 이미 열려 있는 데이터셋 풀에 있는지 확인합니다. 없다면, 풀이 한계값에 도달한 경우, 새 데이터셋을 열기 위해 최저 사용 빈도를 가진 데이터셋을 닫습니다.
:decl_configoption:`GDAL_MAX_DATASET_POOL_SIZE` 환경설정 옵션을 더 큰 값으로 설정하면 풀의 최대 한계값을 늘릴 수 있습니다. 리눅스 상에서 전형적인 사용자 프로세스는 동시에 열 수 있는 파일 개수를 1,024개로 제한하기 때문에 공유 라이브러리 등등을 위한 예비 공간을 준비해야 한다는 사실을 기억하십시오.
gdal_translate 및 gdalwarp 유틸리티는 기본적으로 풀 크기를 450개로 늘립니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

