.. _coordinate_epoch:

================================================================================
좌표 시대(epoch) 지원
================================================================================

.. versionadded:: 3.4

동적 좌표계 및 좌표 시대(epoch)
--------------------------------

이 문서에서는 동적 좌표계에 링크된 좌표 시대를 문서화하려 합니다.

동적 좌표계에서, 지구 표면 상에 있는 한 포인트의 좌표는 시간에 따라 달라질 수도 있습니다. 명확하게 말하자면 해당 좌표가 언제나 좌표가 무결한 시대라는 조건을 갖추어야만 한다는 뜻입니다. 좌표 시대가 반드시 관측 정보가 수집된 시대일 필요는 없습니다.

동적 좌표계의 예로는 ``WGS84 (G1762)``, ``ITRF2014``, ``ATRF2014`` 등이 있습니다.

일반 EPSG:4326 WGS84 좌표계도 동적 좌표계로 간주되긴 하지만, 위치 정확도가 2미터인 원점(datum) 집합을 기반으로 하기 때문에 사용을 권장하지 않습니다. 오히려 WGS84(G1762) 같은 구현 가운데 하나를 사용하는 편이 낫습니다.

:cpp:func:`OGRSpatialReference::IsDynamic` 메소드를 사용해서 어느 좌표계가 동적 좌표계인지 테스트할 수 있습니다.

:cpp:func:`OGRSpatialReference::SetCoordinateEpoch` 및 :cpp:func:`OGRSpatialReference::GetCoordinateEpoch` 메소드를 사용해서 좌표계와 연결된 좌표 시대를 설정하고 가져올 수 있습니다. 좌표 시대는 십진년(decimal year)으로 (예: 2021.3) 표현됩니다.

공식적으로, 관측 정보의 좌표 시대는 관측 정보에 속합니다. 하지만 거의 모든 포맷이 관측 정보별 시대 저장을 지원하지 않기 때문에, 일반적으로 동일 시대의 관측 정보 집합을 사용하게 됩니다. 따라서 시대를 좌표계의 속성(property)으로 저장합니다. 다시 말해 해당 시대 값이 모든 관측 정보의 일부였던 것처럼 취급하게 된다는 뜻입니다. 이런 선택으로 대부분의 사용례에서 처리 과정, 저장 및 포맷 복잡성이 용이해집니다. 현재로서는 포인트들이 서로 다른 시대를 가지고 있는 데이터셋을 처리하지 못 한다는 의미입니다.

벡터 포맷의 경우, 도형별 좌표 시대도 의미가 있을 수 있지만, 대부분의 포맷이 레이어별 좌표계만 지원하기 때문에 현재로서는 좌표 시대 지원을 레이어 수준으로 제한하고 있습니다. 좌표 변환 메커니즘 자체는 꼭짓점별 좌표 시대를 지원할 수 있습니다.

래스터 및 벡터 포맷에서의 지원
------------------------------------

이 문서 작성 당시, GDAL/OGR가 처리하는 포맷 가운데 좌표 시대를 인코딩하는 표준화된 방식을 가지고 있는 포맷은 없습니다. 그 결과 기존 판독기들과 가능한 한 하위 호환되는 것을 목표로 인코딩 방법을 선택했습니다. 대응하는 공식 사양이 이 개념을 고려하도록 진화하는 경우 이 인코딩 방법이 변경될 수도 있습니다.
생성되는 레이어/데이터셋의 공간 좌표계에 추가하는 경우에만 좌표 시대를 작성합니다.

FlatGeoBuf
++++++++++

FlatGeoBuf 파일의 ``Crs.wkt`` 헤더 필드에 설정된 `COORDINATEMETADATA <http://docs.opengeospatial.org/is/18-010r7/18-010r7.html#130>`_ 구조의 ``EPOCH`` 하위 노드를 이용해서 좌표 시대를 WKT:2019 문자열로 인코딩합니다.

::

    COORDINATEMETADATA[
        GEOGCRS["WGS84 (G1762)",
            DYNAMIC[FRAMEEPOCH[2005.0]],
            DATUM["World Geodetic System 1984 (G1762)",
              ELLIPSOID["WGS84",6378137,298.257223563,LENGTHUNIT["metre",1.0]]
            ],
            CS[ellipsoidal,3],
              AXIS["(lat)",north,ANGLEUNIT["degree",0.0174532925199433]],
              AXIS["(lon)",east,ANGLEUNIT["degree",0.0174532925199433]],
              AXIS["ellipsoidal height (h)",up,LENGTHUNIT["metre",1.0]]
        ],
        EPOCH[2016.47]
    ]

.. note:: 

   GDAL 3.4 미만 버전들은 이런 구조를 이해하지 못 하지만, 좌표계가 관련 EPSG 코드를 가지고 있는 경우 이런 예전 GDAL 버전들에서 문제를 일으키지는 않을 것입니다.

지오패키지 벡터/래스터
++++++++++++++++++++++++

관련 좌표 시대를 가지고 있는 각 벡터/래스터 테이블이 ``gpkg_spatial_ref_sys`` 테이블의 ``epoch`` 열에 좌표 시대를 `좌표계 WKT 확장 사양의 확장 버전 <https://github.com/opengeospatial/geopackage/pull/600>`_ 을 이용해서 인코딩합니다.

GeoTIFF
+++++++

좌표 시대를 5120 코드와 DOUBLE 데이터 유형인 새 GeoTIFF 지오키(GeoKey) ``CoordinateEpochGeoKey`` 로 인코딩합니다.

::

    Geotiff_Information:
       Version: 1
       Key_Revision: 1.0
       Tagged_Information:
          ModelTiepointTag (2,3):
             0                 0                 0
             440720            3751320           0
          ModelPixelScaleTag (1,3):
             60                60                0
          End_Of_Tags.
       Keyed_Information:
          GTModelTypeGeoKey (Short,1): ModelTypeProjected
          GTRasterTypeGeoKey (Short,1): RasterPixelIsArea
          GTCitationGeoKey (Ascii,22): "WGS84 / UTM zone 11N"
          GeogCitationGeoKey (Ascii,7): "WGS84"
          GeogAngularUnitsGeoKey (Short,1): Angular_Degree
          ProjectedCSTypeGeoKey (Short,1): PCS_WGS84_UTM_zone_11N
          ProjLinearUnitsGeoKey (Short,1): Linear_Meter
          CoordinateEpochGeoKey (Double,1): 2021.3
          End_Of_Keys.
       End_Of_Geotiff.

JPEG2000
++++++++

GeoJP2 상자는 앞의 GeoTIFF 인코딩을 사용합니다.

영구 보조 메타데이터 (.aux.xml)
++++++++++++++++++++++++++++++++++++++++

좌표 시대를 ``SRS`` 요소의 ``coordinateEpoch`` 속성(attribute)으로 인코딩합니다.

.. code-block:: xml

    <PAMDataset>
      <SRS dataAxisToSRSAxisMapping="1,2" coordinateEpoch="2021.3">PROJCS["WGS84 / UTM zone 11N",GEOGCS["WGS84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32611"]]</SRS>
      <!-- snip -->
    </PAMDataset>

GDAL VRT
++++++++

좌표 시대를 ``SRS`` 요소의 ``coordinateEpoch`` 속성(attribute)으로 인코딩합니다.

.. code-block:: xml

    <VRTDataset rasterXSize="20" rasterYSize="20">
      <SRS dataAxisToSRSAxisMapping="1,2" coordinateEpoch="2021.3">PROJCS["WGS84 / UTM zone 11N",GEOGCS["WGS84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32611"]]</SRS>
      <!-- snip -->
    </VRTDataset>

유틸리티에서의 지원
--------------------

:program:`gdalinfo` 및 :program:`ogrinfo` 는 좌표 시대가 데이터셋/레이어 공간 좌표계에 추가된 경우 좌표 시대를 리포트합니다.

:program:`gdal_translate` 및 :program:`ogr2ogr` 는 ``-a_srs`` 와 함께 사용되는 ``-a_coord_epoch`` 옵션을 가지고 있으며, 공간 좌표계 관련 옵션을 하나도 지정하지 않는 경우 소스 공간 좌표계로부터 산출 공간 좌표계에 좌표 시대를 보전합니다.

:program:`gdalwarp` 및 :program:`ogr2ogr` 는 소스 (그리고 대상) 좌표계의 좌표 시대를 대체/설정하기 위한 ``-s_srs`` 와 함께 사용되는 ``-s_coord_epoch`` 옵션을 (그리고 ``-t_srs`` 와 함께 사용되는 ``-t_coord_epoch`` 옵션을) 가지고 있습니다. 현재 두 동적 좌표계 사이의 변환을 제대로 지원하지 않기 때문에 ``-s_coord_epoch`` 및 ``-t_coord_epoch`` 를 함께 사용할 수 없습니다.

:program:`gdalwarp` 는 적당한 경우 산출 공간 좌표계에 좌표 시대를 보전합니다.

좌표계 변환에서의 지원
----------------------

:cpp:class:`OGRCoordinateTransformation` 클래스는 꼭짓점별로 전송되는 좌표 시대를 기반으로 정적 및 동적 좌표계 사이의 시간 종속(time-dependent) 변환을 수행할 수 있습니다.

정적 및 동적 좌표계 사이의 시간 종속(time-dependent) 변환을 수행하는 경우 동적 좌표계와 관련된 좌표 시대를 연산에 넣을 수도 있습니다. :decl_configoption:`OGR_CT_USE_SRS_COORDINATE_EPOCH` 환경설정 옵션을 NO로 설정하면 소스 또는 대상 좌표계와 관련된 좌표 시대의 사용을 비활성화시킬 수 있습니다.

꼭짓점별 시간이 지정된 경우, 좌표계와 연결된 시간을 대체합니다.

현재 동적 좌표계를 동적 좌표계로 변환하는 작업은 지원하지 않는다는 사실을 기억하십시오.

