.. _osr_api_tut:

================================================================================
OGR 좌표계 및 좌표 변환 예제
================================================================================

.. highlight:: cpp

.. toctree::
   :hidden:

   wktproblems

개요
----

:cpp:class:`OGRSpatialReference` 클래스가 (일반적으로 측지 원점을 가진 맵 투영법과 관련된 투영 좌표계 같은 좌표계 또는 공간 좌표계로 알려진) 좌표계를 표현하고, :cpp:class:`OGRCoordinateTransformation` 클래스는 이들을 서로 변환합니다. 이 클래스들은 오픈GIS 좌표 변환 사양을 느슨하게 기반으로 하고 있으며, 좌표계를 서술하기 위해 WKT(Well Known Text) 포맷을 (OGC WKT 1, ESRI WKT, WKT2:2015 및 WKT2:2018 등 다양한 버전으로) 사용합니다.

참조 및 적용 가능한 표준
------------------------

-  `PROJ 문서 <https://proj4.org>`_: 투영 메소드 및 좌표 작업
-  `ISO:19111 및 WKT 표준 <https://proj4.org/development/reference/cpp/cpp_general.html#standards>`_
-  `GeoTIFF 투영법 변환 목록 <http://geotiff.maptools.org/proj_list>`_: GeoTIFF 용 WKT 투영법 공식 이해하기
-  `EPSG 측지 웹페이지 <https://epsg.org/>`_ 도 유용한 리소스 가운데 하나입니다.

지리 좌표계 정의하기
--------------------

:cpp:class:`OGRSpatialReference` 클래스에서 좌표계를 요약하고 있습니다. :cpp:class:`OGRSpatialReference` 객체를 여러 가지 방법으로 무결한 좌표계로 초기화할 수 있습니다. 좌표계는 주요 유형 2개로 구분할 수 있습니다. 첫 번째 유형은 (위치를 경도/위도로 측정하는) 지리 좌표계이고 두 번째 유형은 (UTM처럼 위치를 미터 또는 피트 단위로 측정하는) 투영 좌표계입니다.

지리 좌표계는 (긴반지름과 역 평탄화로 서술되는 회전 타원체를 암시하는) 원점(datum), (일반적으로 그리니치) 본초자오선, 그리고 일반적으로 도 단위인 각도 단위에 대한 정보를 담고 있습니다. 다음 코드는 사용자가 볼 수 있는 지리 좌표계 이름과 함께 이 모든 정보를 지정해서 지리 좌표계를 초기화하는 예시입니다.

.. code-block::

    OGRSpatialReference oSRS;

    oSRS.SetGeogCS( "My geographic CRS",
                    "World Geodetic System 1984",
                    "My WGS84 Spheroid",
                    SRS_WGS84_SEMIMAJOR, SRS_WGS84_INVFLATTENING,
                    "Greenwich", 0.0,
                    "degree", SRS_UA_DEGREE_CONV );

.. note::

    :cpp:func:`OGRSpatialReference::SetGeogCS` 함수명에서 축약형 "CS"는 현재 측지학 용어에 따르면 적절하지 않습니다. "CRS"로 이해해야 합니다.

이런 값들 가운데, "My geographic CRS", "My WGS84 Spheroid", "Greenwich" 및 "degree"는 옵션 키가 아니라 사용자에게 표시하기 위해 사용되는 값입니다. 하지만 원점 이름 "World Geodetic System 1984"는 원점을 식별하는 키로 사용되며 EPSG 레지스트리에서 알려진 값으로 설정해야 합니다. 그래야 좌표 작업 동안 원점 변환을 제대로 할 수 있기 때문입니다. `geodetic_datum.sql <https://github.com/OSGeo/PROJ/blob/master/data/sql/geodetic_datum.sql>`_ 파일의 세 번째 열에서 무결한 측지 원점 목록을 볼 수 있습니다.

.. note::

    WKT 1버전에서는 원점 이름에 있는 공백 문자를 일반적으로 언더바로 대체합니다.
    그리고 "World Geodetic System 1984"의 별명으로 WGS_1984를 사용합니다.

:cpp:class:`OGRSpatialReference` 는 몇몇 잘 알려진 좌표계에 대한 지원을 내장하고 있습니다. :cpp:func:`OGRSpatialReference::SetWellKnownGeogCS` 메소드에 호출 한 번으로 정의할 수 있는 "NAD27", "NAD83", "WGS72" 및 "WGS84" 좌표계가 포함됩니다.

.. code-block::

    oSRS.SetWellKnownGeogCS( "WGS84" );

.. note::

    :cpp:func:`SetWellKnownGeogCS` 함수명에서 축약형 "CS"는 현재 측지학 용어에 따르면 적절하지 않습니다. "CRS"로 이해해야 합니다.

여기에 더해, EPSG 데이터베이스를 사용할 수 있다면 EPSG 데이터베이스에 있는 어떤 지리 좌표계라도 GCS 코드 번호로 설정할 수 있습니다.

.. code-block::

    oSRS.SetWellKnownGeogCS( "EPSG:4326" );

다른 패키지에 투영법 정의를 직렬화해서 전송하기 위해, 좌표계 용 오픈GIS WKT를 사용합니다. WKT로부터 :cpp:class:`OGRSpatialReference` 를 초기화하거나, :cpp:class:`OGRSpatialReference` 를 다시 WKT로 변환할 수 있습니다. GDAL 3.0버전까지, WKT 내보내기 기본 포맷은 아직 WKT 1버전입니다.

.. code-block::

    char *pszWKT = NULL;
    oSRS.SetWellKnownGeogCS( "WGS84" );
    oSRS.exportToWkt( &pszWKT );
    printf( "%s\n", pszWKT );
    CPLFree(pszWKT);

다음을 출력합니다:

::

    GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,
    AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,
    AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,
    AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],
    AUTHORITY["EPSG","4326"]]

또는 좀더 읽기 쉬운 형식으로 바꾸면:

::

    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AXIS["Latitude",NORTH],
        AXIS["Longitude",EAST],
        AUTHORITY["EPSG","4326"]]

GDAL 3.0버전부터, :cpp:func:`OGRSpatialReference::exportToWkt` 메소드에 옵션을 지정할 수 있습니다.

.. code-block::

        char *pszWKT = nullptr;
        oSRS.SetWellKnownGeogCS( "WGS84" );
        const char* apszOptions[] = { "FORMAT=WKT2_2018", "MULTILINE=YES", nullptr };
        oSRS.exportToWkt( &pszWKT, apszOptions );
        printf( "%s\n", pszWKT );
        CPLFree(pszWKT);

::

    GEOGCRS["WGS 84",
        DATUM["World Geodetic System 1984",
            ELLIPSOID["WGS 84",6378137,298.257223563,
                LENGTHUNIT["metre",1]]],
        PRIMEM["Greenwich",0,
            ANGLEUNIT["degree",0.0174532925199433]],
        CS[ellipsoidal,2],
            AXIS["geodetic latitude (Lat)",north,
                ORDER[1],
                ANGLEUNIT["degree",0.0174532925199433]],
            AXIS["geodetic longitude (Lon)",east,
                ORDER[2],
                ANGLEUNIT["degree",0.0174532925199433]],
        ID["EPSG",4326]]

옵션을 가진 이 메소드는 C 언어에서 :cpp:func:`OSRExportToWktEx` 함수로 사용할 수 있습니다.

:cpp:func:`OGRSpatialReference::importFromWkt` 메소드를 사용해서 WKT 좌표계 정의로부터 :cpp:class:`OGRSpatialReference` 를 설정할 수 있습니다.

좌표계와 축 순서
----------------

앞에서 생략된 "상세 사항" 하나는 좌표계에서의 좌표 축 순서라는 주제입니다. ISO:19111 모델링에 따르면 지리 좌표계는 측지 원점과 `좌표 시스템 <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html#42>`_ 2개의 주요 구성요소로 이루어져 있습니다. 2차원 지리 좌표계의 경우, 좌표 시스템 축은 경도와 위도이며 이 축들을 따라 측정되는 값들은 일반적으로 도 단위로 표현됩니다. (예전 프랑스 기반 좌표계는 그라디안(gradian)을 사용할 수도 있습니다.)

좌표가 지정되는 순서, 그러니까 경도 먼저 위도 나중 순서 또는 그 반대 순서는 끊임없이 혼란을 불러오는 문제로 측지 기관, GIS 사용자, 파일 포맷, 그리고 프로토콜 사양 등등이 사용하는 규범에 따라 달라집니다. 이 순서는 다양한 상호호환성 문제점들의 원인입니다.

GDAL 3.0 이전 버전의 경우, :cpp:class:`OGRSpatialReference` 클래스가 좌표계를 정의하는 기관이 규정하는 축 순서를 존중하지 않았기 때문에 결과적으로 축 순서가 위도 먼저 경도 나중인 경우 WKT 문자열로부터 축 순서 정보를 빼버렸습니다. :cpp:class:`OGRCoordinateTransformation` 클래스를 이용한 좌표 변환도 이 클래스의 :cpp:func:`Transform` 메소드가 전송하거나 반환하는 지리 좌표가 경도, 위도 순서라고 가정했습니다.

GDAL 3.0버전부터, :cpp:class:`OGRCoordinateTransformation` 클래스가 기본적으로 좌표계를 정의하는 기관이 규정하는 축 순서를 존중하고, 항상 WKT 1버전으로 내보냅니다. 결과적으로 "EPSG:4326" 또는 "WGS84" 문자열로 생성된 좌표계는 위도 먼저 경도 나중 축 순서를 사용합니다.

아직도 경도, 위도 순서를 가진 좌표계를 사용하는 코드 베이스로부터의 마이그레이션을 도와주기 위해, 좌표 변환이라는 목적 하에 :cpp:class:`OGRSpatialReference` 인스턴스에 메타데이터 정보를 추가해서 전송되거나 반환되는 값들이 사실상 경도, 위도 순서일 것이라고 지정할 수 있습니다. 이를 위해 다음 메소드를 호출해야만 합니다.

.. code-block::

    oSRS.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER);

:cpp:func:`OGRSpatialReference::SetAxisMappingStrategy` 에 전송되는 인자가 데이터 축과 좌표계 축을 매핑하는 전략입니다.

-  :c:macro:`OAMS_TRADITIONAL_GIS_ORDER`:
   위도/경도 순서인 지리 좌표계의 경우 그래도 데이터는 경도/위도 순서일 것이라는 의미입니다. 마찬가지로 편북/편동 순서인 투영 좌표계의 경우, 그래도 데이터는 편동/편북 순서일 것입니다.

-  :c:macro:`OAMS_AUTHORITY_COMPLIANT`:
   데이터 축이 좌표계 축과 동일할 것이라는 의미입니다. :cpp:class:`OGRSpatialReference` 를 인스턴스화할 때의 기본값입니다.

-  :c:macro:`OAMS_CUSTOM`:
   데이터 축들이 :cpp:func:`SetDataAxisToSRSAxisMapping` 으로 사용자 정의된다는 의미입니다.

이 단락에서 지리 좌표계의 특정 사례에 대해 논의한 내용은 투영 좌표계에도 적용됩니다. 투영 좌표계 대부분은 편동 먼저 편북 나중 규범을 사용하지만, EPSG 레지스트리에 정의된 몇몇 투영 좌표계는 반대 순서 규범을 사용합니다.

잘 알려진 몇몇 특정 좌표계에 대해 전통적인 GIS 순서를 계속 사용할 수 있는 또다른 방법은 "NAD27", "NAD83" 및 "WGS84" 대신 각각 "CRS27", "CRS83" 또는 "CRS84"로 :cpp:func:`OGRSpatialReference::SetWellKnownGeogCS` 를 호출하는 것입니다.

.. code-block::

    oSRS.SetWellKnownGeogCS( "CRS84" );

투영 좌표계 정의하기
--------------------

(UTM, 람베르트 정각원추도법 등등 같은) 투영 좌표계는 기저 지리 좌표계는 물론 (미터 또는 피트 단위로 된) 선형 위치와 각도 단위 경도/위도 위치 간의 변환에 쓰이는 투영 변환 용 정의를 필요로 합니다. 다음 코드는 WGS84의 기저 지리 좌표계(원점)을 가진 UTM 17구역 투영 좌표계를 정의합니다.

.. code-block::

    OGRSpatialReference oSRS;

    oSRS.SetProjCS( "UTM 17 (WGS84) in northern hemisphere." );
    oSRS.SetWellKnownGeogCS( "WGS84" );
    oSRS.SetUTM( 17, TRUE );

:cpp:func:`OGRSpatialReference::SetProjCS` 메소드를 호출해서 사용자 지정 투영 좌표계 이름을 설정하고 좌표 시스템이 투영된 것이라는 사실을 확립합니다. :cpp:func:`OGRSpatialReference::SetWellKnownGeogCS` 메소드는 지리 좌표계를 연결시키고, :cpp:func:`OGRSpatialReference::SetUTM` 을 호출해서 자세한 투영 변환 파라미터들을 설정합니다.
이때 무결한 좌표계 정의를 생성하려면 앞에서 설명한 축 순서가 중요하지만, 향후 :cpp:class:`OGRSpatialReference` 객체가 좌표계 정의를 무결하게 유지하기 위해 필요한 대로 내부 표현을 자동으로 재정렬할 것입니다.

.. caution::

    현재로서는 OGRSpatialReference를 정의하는 단계들의 순서를 주의하십시오!

앞 예시 코드는 다음과 비슷하게 보이는 WKT 버전을 반환할 것입니다. UTM 17이 UTM 구역의 상세한 횡축 메르카토르 정의로 확장되었다는 사실을 기억하십시오.

::

    PROJCS["UTM 17 (WGS84) in northern hemisphere.",
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG",7030]],
                TOWGS84[0,0,0,0,0,0,0],
                AUTHORITY["EPSG",6326]],
            PRIMEM["Greenwich",0,AUTHORITY["EPSG",8901]],
            UNIT["DMSH",0.0174532925199433,AUTHORITY["EPSG",9108]],
            AXIS["Lat",NORTH],
            AXIS["Long",EAST],
            AUTHORITY["EPSG",4326]],
        PROJECTION["Transverse_Mercator"],
        PARAMETER["latitude_of_origin",0],
        PARAMETER["central_meridian",-81],
        PARAMETER["scale_factor",0.9996],
        PARAMETER["false_easting",500000],
        PARAMETER["false_northing",0]]

:cpp:func:`OGRSpatialReference::SetTM` (횡축 메르카토르 도법), :cpp:func:`OGRSpatialReference::SetLCC` (람베르트 정각원추도법) 및 :cpp:func:`OGRSpatialReference::SetMercator` 를 포함, 투영법 용 메소드들이 다수 존재합니다.

좌표계 쿼리하기
---------------

:cpp:class:`OGRSpatialReference` 를 확정하고 나면, 이에 관한 다양한 정보를 쿼리할 수 있습니다. :cpp:func:`OGRSpatialReference::IsProjected` 및 :cpp:func:`OGRSpatialReference::IsGeographic` 메소드를 이용해서 투영 좌표계인지 지리 좌표계인지 판단할 수 있습니다.
:cpp:func:`OGRSpatialReference::GetSemiMajor`, :cpp:func:`OGRSpatialReference::GetSemiMinor` 및 :cpp:func:`OGRSpatialReference::GetInvFlattening` 메소드를 이용하면 PROJCS, GEOGCS, DATUM, SPHEROID, 그리고 PROJECTION 이름 문자열을 가져올 수 있습니다.
:cpp:func:`OGRSpatialReference::GetProjParm` 메소드를 이용해서 투영 파라미터를 가져올 수 있습니다.
:cpp:func:`OGRSpatialReference::GetLinearUnits` 메소드를 이용하면 선형 단위 유형을 가져와서 미터 단위로 변환할 수 있습니다.

투영법 및 파라미터들의 이름은 WKT 1버전 문자열에 있는 이름이라는 사실을 기억하십시오.

다음 코드는 :cpp:func:`OGRSpatialReference::GetAttrValue` 메소드를 이용해서 투영법을, :cpp:func:`OGRSpatialReference::GetProjParm` 메소드로 투영 파라미터를 가져옵니다.
:cpp:func:`GetAttrValue` 메소드는 WKT 텍스트 표현에 명명된 항목과 연결된 첫 번째 "값" 노드를 검색합니다. :cpp:func:`GetProjParm` 메소드로 투영 파라미터를 가져오는 경우 투영 파라미터에 대해 '#define'으로 정의된 (SRS_PP_CENTRAL_MERIDIAN 같은) 상수값을 사용해야 합니다.
:file:`ogrspatialreference.cpp` 에 있는 다양한 투영법들의 ``Set`` 메소드들을 위한 코드를 살펴보고 어떤 투영법에 어떤 파라미터가 사용되는지 알아보십시오.

.. code-block::

    const char *pszProjection = poSRS->GetAttrValue("PROJECTION");

    if( pszProjection == NULL )
    {
        if( poSRS->IsGeographic() )
            sprintf( szProj4+strlen(szProj4), "+proj=longlat " );
        else
            sprintf( szProj4+strlen(szProj4), "unknown " );
    }
    else if( EQUAL(pszProjection,SRS_PT_CYLINDRICAL_EQUAL_AREA) )
    {
        sprintf( szProj4+strlen(szProj4),
        "+proj=cea +lon_0=%.9f +lat_ts=%.9f +x_0=%.3f +y_0=%.3f ",
                poSRS->GetProjParm(SRS_PP_CENTRAL_MERIDIAN,0.0),
                poSRS->GetProjParm(SRS_PP_STANDARD_PARALLEL_1,0.0),
                poSRS->GetProjParm(SRS_PP_FALSE_EASTING,0.0),
                poSRS->GetProjParm(SRS_PP_FALSE_NORTHING,0.0) );
    }
    ...

좌표 변환
---------

:cpp:class:`OGRCoordinateTransformation` 클래스는 서로 다른 좌표계 사이에 위치를 변환하기 위해 사용됩니다. :cpp:func:`OGRCreateCoordinateTransformation` 메소드를 사용해서 새 변환 객체들을 생성한 다음 :cpp:func:`OGRCoordinateTransformation::Transform` 메소드로 서로 다른 좌표계 사이에 포인트 좌표를 변환할 수 있습니다.

.. code-block::

    OGRSpatialReference oSourceSRS, oTargetSRS;
    OGRCoordinateTransformation *poCT;
    double x, y;

    oSourceSRS.importFromEPSG( atoi(papszArgv[i+1]) );
    oTargetSRS.importFromEPSG( atoi(papszArgv[i+2]) );

    poCT = OGRCreateCoordinateTransformation( &oSourceSRS,
                                              &oTargetSRS );
    x = atof( papszArgv[i+3] );
    y = atof( papszArgv[i+4] );

    if( poCT == NULL || !poCT->Transform( 1, &x, &y ) )
        printf( "Transformation failed.\n" );
    else
    {
        printf( "(%f,%f) -> (%f,%f)\n",
                atof( papszArgv[i+3] ),
                atof( papszArgv[i+4] ),
                x, y );
    }


There are a couple of points at which transformations can
fail.  First, OGRCreateCoordinateTransformation() may fail,
generally because the internals recognize that no transformation
between the indicated systems can be established, and will
return a NULL pointer.

The OGRCoordinateTransformation::Transform() method itself can
also fail.  This may be as a delayed result of one of the above
problems, or as a result of an operation being numerically
undefined for one or more of the passed in points.  The
Transform() function will return TRUE on success, or FALSE
if any of the points fail to transform.  The point array is
left in an indeterminate state on error.

Though not shown above, the coordinate transformation service can
take 3D points, and will adjust elevations for elevation differences
in spheroids, and datums. Elevations given on a geographic or projected CRS
are assumed to be ellipsoidal heights. When using a compound CRS made of a
horizontal CRS (geographic or projected) and a vertical CRS, elevations will
be related to a vertical datum (mean sea level, gravity based, etc.).

Starting with GDAL 3.0, a time value (generally as a value in decimal years) can
also be specified for time-dependent coordinate operations.

The following example shows how to conveniently create a long/lat coordinate
system using the same geographic CRS as a projected coordinate
system, and using that to transform between projected coordinates and
long/lat. The returned coordinates will be in longitude, latitude order due to
the call to SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)

.. code-block::

    OGRSpatialReference    oUTM, *poLongLat;
    OGRCoordinateTransformation *poTransform;

    oUTM.SetProjCS("UTM 17 / WGS84");
    oUTM.SetWellKnownGeogCS( "WGS84" );
    oUTM.SetUTM( 17 );

    poLongLat = oUTM.CloneGeogCS();
    poLongLat->SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER);

    poTransform = OGRCreateCoordinateTransformation( &oUTM, poLongLat );
    if( poTransform == NULL )
    {
        ...
    }

    ...

    if( !poTransform->Transform( nPoints, x, y, z ) )
    ...

Advanced Coordinate Transformation
----------------------------------

OGRCreateCoordinateTransformation() under-the-hood may determine several candidate
coordinate operations transforming from the source CRS to the target CRS. Those
candidate coordinate operations each have their own area of use. When Transform()
is invoked, it will determine the most appropriate coordinate operation based on
the coordinates of the point to transform and area of use. For example,
there are several dozens of possible coordinate operations for the NAD27 to WGS84
transformation.

If a bounding box of the area of interest into which coordinates to transform
are located is known, it is possible to specify it to restrict the candidate
coordinate operations to consider:

.. code-block::

    OGRCoordinateTransformationOptions options;
    options.SetAreaOfInterest(-100,40,-99,41);
    poTransform = OGRCreateCoordinateTransformation( &oNAD27, &oWGS84, options );

For cases where a particular coordinate operation must be used, it is possible
to specify it as as a PROJ string (single step operation or multiple step string
starting with +proj=pipeline), a WKT2 string describing a CoordinateOperation,
or a urn:ogc:def:coordinateOperation:EPSG::XXXX URN

.. code-block::

    OGRCoordinateTransformationOptions options;

    // EPSG:8599, NAD27을 WGS 84 (46)으로, 1.15 m, USA - Indiana
    options.SetCoordinateOperation(
        "+proj=pipeline +step +proj=axisswap +order=2,1 "
        "+step +proj=unitconvert +xy_in=deg +xy_out=rad "
        "+step +proj=hgridshift +grids=conus "
        "+step +proj=hgridshift +grids=inhpgn.gsb "
        "+step +proj=unitconvert +xy_in=rad +xy_out=deg +step "
        "+proj=axisswap +order=2,1", false );

    // 또는
    // options.SetCoordinateOperation(
    //      "urn:ogc:def:coordinateOperation:EPSG::8599", false);

    poTransform = OGRCreateCoordinateTransformation( &oNAD27, &oWGS84, options );


Alternate Interfaces
--------------------

A C interface to the coordinate system services is defined in
ogr_srs_api.h, and Python bindings are available via the osr.py module.
Methods are close analogs of the C++ methods but C and Python bindings
are missing for some C++ methods.

C bindings
++++++++++

.. code-block:: c

    typedef void *OGRSpatialReferenceH;
    typedef void *OGRCoordinateTransformationH;

    OGRSpatialReferenceH OSRNewSpatialReference( const char * );
    void    OSRDestroySpatialReference( OGRSpatialReferenceH );

    int     OSRReference( OGRSpatialReferenceH );
    int     OSRDereference( OGRSpatialReferenceH );

    void OSRSetAxisMappingStrategy( OGRSpatialReferenceH,
                                    OSRAxisMappingStrategy );

    OGRErr  OSRImportFromEPSG( OGRSpatialReferenceH, int );
    OGRErr  OSRImportFromWkt( OGRSpatialReferenceH, char ** );
    OGRErr  OSRExportToWkt( OGRSpatialReferenceH, char ** );
    OGRErr  OSRExportToWktEx( OGRSpatialReferenceH, char **,
                            const char* const* papszOptions );

    OGRErr  OSRSetAttrValue( OGRSpatialReferenceH hSRS, const char * pszNodePath,
                            const char * pszNewNodeValue );
    const char *OSRGetAttrValue( OGRSpatialReferenceH hSRS,
                                const char * pszName, int iChild);

    OGRErr  OSRSetLinearUnits( OGRSpatialReferenceH, const char *, double );
    double  OSRGetLinearUnits( OGRSpatialReferenceH, char ** );

    int     OSRIsGeographic( OGRSpatialReferenceH );
    int     OSRIsProjected( OGRSpatialReferenceH );
    int     OSRIsSameGeogCS( OGRSpatialReferenceH, OGRSpatialReferenceH );
    int     OSRIsSame( OGRSpatialReferenceH, OGRSpatialReferenceH );

    OGRErr  OSRSetProjCS( OGRSpatialReferenceH hSRS, const char * pszName );
    OGRErr  OSRSetWellKnownGeogCS( OGRSpatialReferenceH hSRS,
                                const char * pszName );

    OGRErr  OSRSetGeogCS( OGRSpatialReferenceH hSRS,
                        const char * pszGeogName,
                        const char * pszDatumName,
                        const char * pszEllipsoidName,
                        double dfSemiMajor, double dfInvFlattening,
                        const char * pszPMName ,
                        double dfPMOffset ,
                        const char * pszUnits,
                        double dfConvertToRadians );

    double  OSRGetSemiMajor( OGRSpatialReferenceH, OGRErr * );
    double  OSRGetSemiMinor( OGRSpatialReferenceH, OGRErr * );
    double  OSRGetInvFlattening( OGRSpatialReferenceH, OGRErr * );

    OGRErr  OSRSetAuthority( OGRSpatialReferenceH hSRS,
                            const char * pszTargetKey,
                            const char * pszAuthority,
                            int nCode );
    OGRErr  OSRSetProjParm( OGRSpatialReferenceH, const char *, double );
    double  OSRGetProjParm( OGRSpatialReferenceH hSRS,
                            const char * pszParamName,
                            double dfDefault,
                            OGRErr * );

    OGRErr  OSRSetUTM( OGRSpatialReferenceH hSRS, int nZone, int bNorth );
    int     OSRGetUTMZone( OGRSpatialReferenceH hSRS, int *pbNorth );

    OGRCoordinateTransformationH
    OCTNewCoordinateTransformation( OGRSpatialReferenceH hSourceSRS,
                                    OGRSpatialReferenceH hTargetSRS );

    void OCTDestroyCoordinateTransformation( OGRCoordinateTransformationH );

    int OCTTransform( OGRCoordinateTransformationH hCT,
                    int nCount, double *x, double *y, double *z );

    OGRCoordinateTransformationOptionsH OCTNewCoordinateTransformationOptions(;

    int OCTCoordinateTransformationOptionsSetOperation(
        OGRCoordinateTransformationOptionsH hOptions,
        const char* pszCO, int bReverseCO);

    int OCTCoordinateTransformationOptionsSetAreaOfInterest(
        OGRCoordinateTransformationOptionsH hOptions,
        double dfWestLongitudeDeg,
        double dfSouthLatitudeDeg,
        double dfEastLongitudeDeg,
        double dfNorthLatitudeDeg);

    void OCTDestroyCoordinateTransformationOptions(OGRCoordinateTransformationOptionsH);

    OGRCoordinateTransformationH
    OCTNewCoordinateTransformationEx( OGRSpatialReferenceH hSourceSRS,
                                    OGRSpatialReferenceH hTargetSRS,
                                    OGRCoordinateTransformationOptionsH hOptions );

Python bindings
+++++++++++++++

.. code-block:: python

    class osr.SpatialReference
        def __init__(self,obj=None):
        def SetAxisMappingStrategy( self, strategy ):
        def ImportFromWkt( self, wkt ):
        def ExportToWkt(self, options = None):
        def ImportFromEPSG(self,code):
        def IsGeographic(self):
        def IsProjected(self):
        def GetAttrValue(self, name, child = 0):
        def SetAttrValue(self, name, value):
        def SetWellKnownGeogCS(self, name):
        def SetProjCS(self, name = "unnamed" ):
        def IsSameGeogCS(self, other):
        def IsSame(self, other):
        def SetLinearUnits(self, units_name, to_meters ):
        def SetUTM(self, zone, is_north = 1):

    class CoordinateTransformation:
        def __init__(self,source,target):
        def TransformPoint(self, x, y, z = 0):
        def TransformPoints(self, points):

History and implementation considerations
-----------------------------------------

Before GDAL 3.0, the OGRSpatialReference class was strongly tied to OGC WKT (WKT 1)
format specified by `Coordinate Transformation Services (CT) specification (01-009) <http://portal.opengeospatial.org/files/?artifact_id=999>`_,
and the way
it was interpreted by GDAL, which various caveats detailed in
the :ref:`wktproblems` page.
The class mostly contained an in-memory tree-like representation of WKT 1 strings.
The class used to directly implement import and export to OGC WKT 1, WKT-ESRI and PROJ.4
formats. Reprojection services were only available if GDAL had been build against
the PROJ library.

Starting with GDAL 3.0, the `PROJ <https://proj4.org>`_ >= 6.0 library
has become a required dependency of GDAL.
PROJ 6 has built-in support for OGC WKT 1, ESRI WKT, OGC WKT 2:2015
and OGC WKT 2:2018 representations. PROJ 6 also implements a C++ object class
hierarchy of the ISO-19111 / OGC Abstract Topic 2 "Referencing by coordinate" standard.
Consequently the OGRSpatialReference class has been modified to act mostly as
a wrapper on top of PROJ PJ* CRS objects, and tries to abstract away from
the OGC WKT 1 representation as much as possible. However, for backward compatibility,
some methods still expect arguments or return values that are specific of OGC WKT 1.
The design of th OGRSpatialReference class is also still monolithic. Users wanting
direct and fine grained access to CRS representations might want to directly use
the PROJ 6 C or C++ API.
