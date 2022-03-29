.. _raster.usgsdem:

================================================================================
USGSDEM -- USGS 아스키 DEM (및 CDED)
================================================================================

.. shortname:: USGSDEM

.. built_in_by_default::

GDAL은 USGS 아스키 DEM 파일 읽기를 지원합니다. 이 포맷은 USGS가 SDTS로 갈아타기 전에 사용했던 전통적인 포맷으로, CDED(Canada Digital Elevation Data) DEM 데이터에 사용되는 포맷입니다. USGS DEM 파일의 가장 유명한 변이형들을 좌표계 및 지리참조 배치 정보를 정확하게 인식해서 지원할 것입니다.

`7.5분 (UTM 그리드) USGS DEM <https://pubs.usgs.gov/of/2003/of03-150/arcview/metadata/dem/dem.htm>`_ 파일은 일반적으로 경계 주변에 NODATA 값으로 제대로 표시된 누락된 데이터 영역을 가지고 있을 것입니다. USGS DEM 파일의 표고값 단위는 미터 또는 피트이며, GDALRasterBand::GetUnitType()의 반환값이 이 단위를 ("m" 또는 "ft"로) 알려줄 것입니다.

USGS DEM 파일은 하나의 큰 타일로 표현된다는 사실을 기억하십시오. 이 때문에 GDAL 타일 캐시 용량이 작을 경우 캐시 충돌(cache thrashing) 문제가 발생할 수도 있습니다. 또한 첫 번째 픽셀을 읽어올 때 파일 전체를 가져올 것이기 때문에 상당한 지연 현상이 발생할 수도 있습니다.

``usgsdemdataset.cpp`` 를 구현하기 위한 코드 가운데 일부는 벤 디스코(Ben Discoe)가 개발한 VTP 코드로부터 파생되었습니다. VTP에 대해 더 알고 싶다면 `가상 지형 프로젝트(Virtual Terrain Project) <http://www.vterrain.org/>`_ 를 참조하십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

GDAL은 캐나다 연방 정부 사양을 준수하는 CDED 2.0 50K 상품 생성을 포함, 지리 (및 UTM) 좌표계를 사용하는 USGS DEM과 CDED 데이터 파일 내보내기를 지원합니다.

먼저 입력 데이터를 지리 또는 UTM 좌표계로 샘플링해야만 합니다. 기본적으로 입력 파일의 전체 영역을 산출할 것이지만, CDED 50K 상품의 경우 생성 작업 시 산출 파일을 지정한 해상도 및 상품의 타일 경계에서 샘플링할 것입니다.

입력 파일이 적절한 좌표계 정보 설정을 가지고 있다면, 특정 상품 포맷으로 내보내는 경우 서로 다른 좌표계를 입력받을 수 있습니다. (예를 들어 CDED 50K 상품의 경우 알베르스 정적원추 투영법을 NAD83 지리 좌표계로 변환할 수 있습니다.)

생성 옵션
---------

-  **PRODUCT=DEFAULT/CDED50K**:
   이 옵션을 CDED50K로 설정하는 경우, 산출 파일이 CDED 50K 상품 사양을 준수하도록 강제할 것입니다. 산출물 크기는 항상 1201x1201 크기로, (최북단 영역에서는 경도 간격이 더 넓어지겠지만) 일반적으로는 15분 x 15분 크기의 타일이 될 것입니다.

-  **TOPLEFT=long,lat**:
   CDED 50K 상품의 경우, 이 옵션을 사용해서 생성할 타일의 좌상단 모서리를 지정합니다. 이 모서리는 15분 경계 상에 있어야 하며, 십진수도 또는 도분 단위로 설정할 수 있습니다. (예: TOPLEFT=117d15w,52d30n)

-  **RESAMPLE=Nearest/Bilinear/Cubic/CubicSpline**:
   데이터를 대상 그리드로 리샘플링하기 위해 사용되는 리샘플링 커널을 설정합니다. CDED 50K 같은 특정 상품을 생성하는 경우에만 효과를 미칩니다. 기본값은 Bilinear입니다.

-  **DEMLevelCode=integer**:
   DEM 수준을 설정합니다. (1, 2, 3 가운데 하나로 설정할 수 있습니다.) 기본값은 1입니다.

-  **DataSpecVersion=integer**:
   데이터와 사양의 버전/리비전을 설정합니다. (예: 1020)

-  **PRODUCER=text**:
   생성된 파일의 생산자 필드에 저장할 60개까지의 문자입니다.

-  **OriginCode=text**:
   생성된 파일의 원점 코드 필드에 저장할 4개까지의 문자입니다. (예: 유콘(Yukon)의 경우 YT)

-  **ProcessCode=code**:
   생성된 파일의 처리 코드 필드에 저장할 문자 1개입니다. (예: 8=ANUDEM, 9=FME, A=TopoGrid)

-  **TEMPLATE=filename**:
   모든 산출 파일에 템플릿 파일을 지정할 수 있습니다. 템플릿 파일을 지정하는 경우 템플릿 파일로부터 데이터 생산자(Data Producer)를 포함하는 수많은 필드를 복사할 것입니다. 지정하지 않는다면 산출 파일의 필드들을 비워둘 것입니다.

-  **ZRESOLUTION=float**:
   DEM은 표고 정보를 양의 정수값으로 저장하고, "z 해상도"를 이용해서 이 정수값들을 크기 조정합니다. 기본적으로 이 해상도는 1.0으로 작성됩니다. 하지만 정수값을 부동소수점형 숫자로 크기 조정하고 싶다면 이 옵션에 다른 해상도를 지정할 수도 있습니다.

-  **NTS=name**:
   TOPLEFT를 파생시키기 위해 사용되는 NTS 맵시트(Mapsheet) 이름입니다. CDED 50K 같은 특정 상품을 생성하는 경우에만 효과를 미칩니다.

-  **INTERNALNAME=name**:
   파일 헤더에 작성할 데이터셋 이름입니다. CDED 50K 같은 특정 상품을 생성하는 경우에만 효과를 미칩니다.

예시
----

다음 명령어는 더 큰 DEM 커버리지 yk_3arcsec으로부터 좌상단 모서리가 -117w,60n인 타일을 하나 추출해서 단일 CDED 50K 타일을 생성할 것입니다. yk_template.dem 파일은 데이터 생산자, 처리 코드 및 원점 코드 필드를 포함하는 몇몇 상품 필드를 설정하기 위해 쓰입니다.

::

   gdal_translate -of USGSDEM -co PRODUCT=CDED50K -co TEMPLATE=yk_template.dem \
                  -co TOPLEFT=-117w,60n yk_3arcsec 031a01_e.dem

참고
----

-  ``gdal/frmts/usgsdem/usgsdemdataset.cpp`` 로 구현되었습니다.

-  GDAL의 USGS DEM 판독 코드는 `VTP <http://www.vterrain.org/>`_ 소프트웨어의 가져오기 기능으로부터 파생되었습니다. 내보내기 기능은 캐나다 유콘 준주 환경부의 재정 지원으로 개발되었습니다.
