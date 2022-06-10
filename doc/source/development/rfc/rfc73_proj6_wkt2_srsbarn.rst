.. _rfc-73:

=======================================================================================================
RFC 73: WKT2, 최신 바인딩 케이퍼빌리티, 시간 지원 및 통합 좌표계 데이터베이스를 위한 PROJ6 통합
=======================================================================================================

============ ==========================
저자:        이벤 루올
연락처:      even.rouault@spatialys.com
제안일:      2019년 1월 8일
최신 수정일: 2019년 5월 2일
상태:        승인, GDAL 3.0버전에 구현
============ ==========================

요약
----

이 RFC는 GDAL과 PROJ 6버전의 통합과 관련된 작업을 설명합니다. 이 통합으로 다음과 같은 케이퍼빌리티가 추가됩니다:

-  좌표계 WKT 2 지원
-  좌표계들 간의 좌표 변환을 위한 "최신 바인딩(late binding)" 케이퍼빌리티
-  좌표 작업을 위한 시간 차원 지원
-  통합 좌표계 데이터베이스 사용

동기
----

이 RFC를 제안하게 된 동기는 `https://gdalbarn.com/#why <https://gdalbarn.com/#why>`_ 에서 설명하고 있습니다. 그 내용을 발췌했습니다.

GDAL, PROJ, 및 libgeotiff의 좌표계는 현대적인 케이퍼빌리티를 누락하고 있기 때문에 철저한 리팩토링(refactoring)이 필요합니다:

-  PROJ_LIB 및 GDAL_DATA의 꺼려지는 즉석(ad hoc) CSV 데이터베이스는 사용자가 짜증을 내게 하고, 개발자에게는 문제를 일으키며, 좌표계 정의를 상호 운용하는 것을 방해합니다.

-  GDAL과 PROJ는 OGC WKT 2를 지원하지 않습니다.

-  PROJ 5.0 이상 버전은 더 이상 WGS84에서 최대 2미터까지 오류가 날 수도 있는 원점 변환 회전(datum transformation pivot)을 요구하지 않습니다. 그러나 다른 도구들이 이 이점을 취하지 않습니다.

CSV 데이터베이스
~~~~~~~~~~~~~~~~

EPSG 및 다른 좌표계 정의에 대해 SQLite 기반 데이터베이스를 사용하면 프로젝트에 더 많은 케이퍼빌리티(영역 인식 검증)를 추가할 수 있고, 프로젝트의 사용자 지정 고유 데이터 구조를 좀 더 보편적으로 사용할 수 있는 데이터 구조로 전환할 수 있으며, 소프트웨어 도구들이 다루는 수많은 좌표계들 간에 좌표계 정의 상호 운용성을 촉진할 수 있습니다.

WKT2
~~~~

`OGC WKT2 <https://docs.opengeospatial.org/is/12-063r5/12-063r5.html>`_ 가 오래 이어져 왔던 좌표계 정의 상호 운용성 불일치를 수정합니다. WKT 2는 시간 종속 좌표계를 설명하기 위한 도구를 담고 있습니다. PROJ 5 이상 버전은 이제 시간 종속 변환을 할 수 있지만, GDAL 및 다른 도구들이 아직 지원하지 않습니다.

몇몇 국가들이 국가 측지 인프라스트럭처가 시간 종속 좌표계를 포함시키도록 업데이트하고 있습니다. 예를 들면 호주와 미국이 각각 2020년과 2022년에 시간 종속 좌표계로 전환할 예정입니다. 북미에서 널리 쓰이던 NAD83 및 NAVD88을 NATRF2022 및 NAPGD2022로 대체하는 중이며, 산업계도 빠르건 늦건 이런 문제에 적응해 나가야 할 것입니다.

WGS84 회전
~~~~~~~~~~

예전 PROJ는 WGS84에서 파라미터 7개를 사용해서 회전(pivot)시키는 원점 변환을 요구했습니다. 이 회전은 실용적인 해결책이지만 약 2미터에 달하는 오류를 낼 수 있고, 또 수많은 레거시 원점들을 WGS84로 정의할 수 없기도 합니다. PROJ 5.0 이상 버전은 `변환 파이프라인 프레임워크 <https://proj.org/usage/transformation.html#geodetic-transformation>`_ 를 통해 최신 바인딩(late binding)을 지원하는 도구들을 제공하지만, GDAL과 다른 도구들은 아직 이 프레임워크를 사용하지 못 합니다. 정확도가 더 높은 새로운 변환은 WGS84를 거치지 않으며, 지역 측지 기관의 사이드카 데이터를 사용해서 추가 변환 단계를 없앱니다.

다른 라이브러리에서의 관련 작업
-------------------------------

이 RFC는 "`gdalbarn <https://gdalbarn.com/>`_" 작업의 마지막 단계입니다. 예전 단계들은 `PROJ RFC 2 <https://proj.org/community/rfc/rfc-2.html>`_ 에 따라 PROJ 마스터 저장소에 관련 변경 사항들을 구현하고 `libgeotiff 풀 요청 2번 <https://github.com/OSGeo/libgeotiff/pull/2>`_ 에 따라 libgeotiff 마스터 저장소에 관련 변경 사항들을 구현하는 단계들이었습니다.

제안
----

제3자 라이브러리 요구 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~

GDAL 마스터(향후 3.0버전)를 빌드하고 실행하려면 PROJ 마스터(향후 PROJ 6.0버전)와 libgeotiff 마스터(향후 libgeotiff 1.5 또는 2.0버전)가 필요할 것입니다.

PROJ와 관련해서, GDAL 마스터에 어떤 PROJ 내부 복사본도 내장시키지 않을 것입니다. PROJ 예전 버전들을 지원하는 것은 불가능합니다. GDAL로부터 PROJ로 완전히 옮겨진 다음 기능들의 이점을 이용하기 위해 :cpp:class:`OGRSpatialReference` 클래스를 상당 부분 재작성했기 때문입니다:

-  PROJ 문자열 가져오기 및 내보내기
-  WKT 문자열 가져오기 및 내보내기
-  EPSG 데이터베이스 이용

일부 GDAL 의존성이 시스템이 제공하는 libproj를 이용하는데 PROJ 마스터와 이 예전 libproj를 아무 생각 없이 혼합해서 런타임 크래시가 발생하는 복잡한 설정(setup)에서 GDAL 마스터와 PROJ 마스터를 좀 더 쉽게 이용하려면, PROJ 마스터의 공개 심볼의 별명을 지정하는 ``CFLAGS/CXXFLAGS=-DPROJ_RENAME_SYMBOLS`` 를 이용해서 PROJ를 빌드하면 됩니다. 이렇게 하면 GDAL이 이 사용자 지정 빌드를 사용할 수 있을 것입니다.
이 방법은 장기적으로 사용하기 위한 해결책이 아니라는 사실을 기억하십시오. 제대로 된 패키지 작업 솔루션은 결국 PROJ 6를 사용해서 모든 역 의존성을 재작성할 것이기 때문입니다. 환경설정 또는 nmake 시 PROJ가 필요하다는 사실도 기억해둬야 합니다. 런타임 시 dlopen() / LoadLibrary()를 통한 동적 불러오기를 더 이상 사용할 수 없기 때문입니다.

libgeotiff와 관련해서, :file:`frmts/gtiff/libgeotiff` 에 있는 복사본을 업스트림 libgeotiff 마스터의 내용으로 새로고침했습니다.

모든 지속적 통합(Continuous Integration) 시스템이 (Travis-CI 및 AppVeyor가) GDAL 빌드의 일부분으로 PROJ 마스터를 빌드하도록 업데이트했습니다.

OGRSpatialReference 재작성
~~~~~~~~~~~~~~~~~~~~~~~~~~

:cpp:class:`OGRSpatialReference` class is central in GDAL/OGR for all coordinate reference systems (CRS) manipulations.
Up to GDAL 2.4, this class contained mostly a OGR_SRSNode root node of a WKT 1 representation, and all getters and setters manipulated this tree representation.
As part of this work, the main object contained internally by OGRSpatialReference is now a PROJ PJ object, and methods call PROJ C API getters and setters on this PJ object.
This enables to be, mostly (\*), representation independent.

WKT1, WKT2, ESRI WKT, PROJ strings import and export is now delegated to PROJ.
The same holds for import of CRS from the EPSG database, that now relies on proj.db SQLite database.
Consequently all the :file:`data/*.csv` files that contained CRS related information have been removed from GDAL.
It should be noted that "morphing" from ESRI WKT is now done automatically when importing WKT.

While general semantics of methods like IsSame() or FindMatches() remain the same, underneath implementations are substantially different, which can lead to different results than previous GDAL versions in some cases.
In the FindMatches() case, identification of CRS to EPSG entries is generally improved due to enhanced query capabilities in the database.

*  The "mostly" precision is here since it was not practical to do this rewrite in every place.
So for some methods, an internal WKT1 export is still done.
This is the case for methods that take a path to a SRS node (like "GEOGCS|UNIT") as an argument, or some methods like SetProjection(), GetProjParm(), that expect a OGC WKT1 specific name.
Those are thought to be used mostly be drivers. Changing them to be EPSG names would impact a number of drivers, some of them little tested regarding SRS support, and which furthermore mostly support WKT1 representation only.

OGRCoordinateTransformation 변경 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since GDAL 2.3 and initial PROJ 5 support, when transforming between two
CRS we still relied on the PROJ.4 string export of the source and target
CRS to create a coordinate operation pipeline. So this limited to
"early-binding" operations, that is using the WGS84 pivot through
towgs84 or nadgrids PROJ keywords. Now PROJ new capabilities to find
appropriate coordinate operations between two CRS is used, offering
"late-binding" capabilities to take into account other pivots than WGS84
or area of uses.

OGRCreateCoordinateOperation() now takes an extra optional arguments to
define options.

One of those options is to define an area of interest that will be taken
into account when searching candidate operations. If several operations
match, the "best" (according to PROJ sorting criterion) will be
selected. Note: it will systematically be used even if later calls to
Transform() use coordinates outside of the initial area of interest.

Another option is the ability to specify the coordinate operation to
apply, so as an override of what GDAL / PROJ would have automatically
computed, either as a PROJ string (generally a +proj=pipeline), or a WKT
coordinate operation/concatenated operation. Users can typically select
a specific coordinate operation by using the new PROJ projinfo utility
that can return the candidate operations from a source_crs / target_crs
tuple.

When no option is specified, GDAL will use PROJ to list all candidate
coordinate operations. For each call to Transform(), it will compute the
average coordinate of the input coordinates and use it to determine the
best coordinate operation from the candidate ones.

The Transform() method now takes an extra argument to contain the
coordinate epoch (generally as a decimal year value) for coordinate
operations that are time-dependent. Related, the transform options of
the GDALTransform mechanism typically used by gdalwarp now accepts a
COORDINATE_EPOCH for the same purpose.

GDAL에서 OGRSpatialReference 사용
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently GDAL datasets accept and return a WKT 1 string to describe the
SRS. To be more independent of the actual encoding, and for example
allowing a GeoPackage raster dataset to be able to use WKT 2, it is
desirable to be able to attach a SRS that is not dependent of the
representation (WKT 1 or WKT 2), hence using a OGRSpatialReference
object instead of a const char\* string.

The following new methods are added in GDALDataset:

-  virtual const OGRSpatialReference\* GetSpatialRef() const;
-  virtual CPLErr SetSpatialRef(const OGRSpatialReference*);
-  virtual const OGRSpatialReference\* GetGCPSpatialRef() const;
-  virtual CPLErr SetGCPs(int nGCPCount, const GDAL_GCP *pasGCPList,
   const OGRSpatialReference*);

To ease the transition, the following non virtual methods are added in
GDALDataset:

-  const OGRSpatialReference\* GetSpatialRefFromOldGetProjectionRef()
   const;
-  CPLErr OldSetProjectionFromSetSpatialRef(const OGRSpatialReference\*
   poSRS);
-  const OGRSpatialReference\* GetGCPSpatialRefFromOldGetGCPProjection()
   const;
-  CPLErr OldSetGCPsFromNew( int nGCPCount, const GDAL_GCP \*pasGCPList,
   const OGRSpatialReference \* poGCP_SRS );

and the previous GetProjectionRef(), SetProjection(), GetGCPProjection()
and SetGCPs() are available as projected virtual methods, prefixed by an
underscore

This way to convert an existing driver, it is a matter of renaming its
GetProjectionRef() method as \_GetProjectionRef(), and adding:

::

   const OGRSpatialReference* GetSpatialRef() const override {
       return GetSpatialRefFromOldGetProjectionRef();
   }

기본 WKT 버전
~~~~~~~~~~~~~

OGRSpatialReference::exportToWkt() without options will report WKT 1
(with explicit AXIS nodes. See below "Axis order issues" paragraph) for
CRS compatibles of this representation, and otherwise use WKT2:2018
(typically for Geographic 3D CRS).

An enhanced version of exportToWkt() accepts options to specify the
exact WKT version used, if multi-line or single-line output must be
used, etc.

Alternatively the OSR_WKT_FORMAT configuration option can be used to
modify the WKT version used by exportToWk() (when no explicit version is
passed in the options of exportToWkt())

The gdalinfo, ogrinfo and gdalsrsinfo utililies will default to
outputting WKT2:2018

축 순서 문제점
~~~~~~~~~~~~~~

This is a recurring pain point. This RFC proposes a new approach
(without pretending to solving it completely) to what was initially done
per `RFC 20: OGRSpatialReference Axis Support <./rfc20_srs_axes>`_. The
issue is that CRS official definitions use axis orders that do not
conform to the way raster or vector data is traditionally encoded in GIS
applications. The typical example is the Geographic "WGS 84" definition
from EPSG, EPSG:4326, which uses latitude as the first axis and
longitude as the second axis. RFC 20 decided that by default the AXIS
definition would be stripped off from the WKT when the axis order from
the authority did not match the GIS friendly one (and use a custom EPSGA
authority to have WKT with official AXIS elements)

This was technically possible since the WKT 1 grammar makes the AXIS
element definition. However removal of the AXIS definitions was a
potential source of confusion as it was unclear which axis order was
actually used. Furthermore, in WKT2, the AXIS element is compulsory, and
the internal PROJ representation requires also a coordinate system to be
defined. So there would have been two unsatisfactory options:

-  return patched versions of the official definition with the GIS
   friendly order, while still using the official authority code.
   Practical since we keep the link with the source code, but a lie
   since we modify it. Users would not know whether they must trust the
   encoded order, or the official order from the authority.
-  return patched versions of the official definition with the GIS
   friendly order, but without the official authority code. This would
   be compliant, but we would lose the link with the authority code.

The solution put forward in this RFC is to add a "data axis to SRS axis
mapping" concept, which is a bit similar to what is done in WCS
DescribeCoverage response to explain how the SRS axis map to the grid
axis of a coverage

Extract from
`https://docs.geoserver.org/stable/en/user/extensions/wcs20eo/index.html <https://docs.geoserver.org/stable/en/user/extensions/wcs20eo/index.html>`_
for a coverage that uses EPSG:4326

::

         <gml:coverageFunction>
           <gml:GridFunction>
             <gml:sequenceRule axisOrder="+2 +1">Linear</gml:sequenceRule>
             <gml:startPoint>0 0</gml:startPoint>
           </gml:GridFunction>
         </gml:coverageFunction>

A similar mapping is added to define how the 'x' and 'y' components in
the geotransform matrix or in a OGRGeometry map to the axis defined by
the CRS definition.

Such mapping is given by a new method in OGRSpatialReference

::

   const std::vector<int>& GetDataAxisToSRSAxisMapping() const

To explain its semantics, imagine that it return 2,-1,3. That is
interpreted as:

-  2: the first axis of the CRS maps to the second axis of the data
-  -1: the second axis of the CRS maps to the first axis of the data,
   with values negated
-  3: the third axis of the CRS maps to the third axis of the data

This is similar to the PROJ axisswap operation:
`https://proj4.org/operations/conversions/axisswap.html <https://proj4.org/operations/conversions/axisswap.html>`_

By default, on a newly create OGRSpatialReference object,
GetDataAxisToSRSAxisMapping() returns the identity 1,2[,3], that is,
conform to the axis order defined by the authority.

As all GDAL and a vast majority of OGR drivers depend on using the "GIS
axis mapping", a method SetAxisMappingStrategy(
OAMS_TRADITIONAL_GIS_ORDER or OAMS_AUTHORITY_COMPLIANT or OAMS_CUSTOM )
is added to make their job of specifying the axis mapping easier;

OAMS_TRADITIONAL_GIS_ORDER means:

-  for geographic 2D CRS,

   -  for Latitude NORTH, Longitude EAST (such as EPSG:4326),
      GetDataAxisToSRSAxisMapping() returns {2,1}, meaning that the data
      order is longitude, latitude
   -  for Longitude EAST, Latitude NORTH (such as OGC:CRS84), returns
      {1,2}

-  for projected CRS,

   -  for EAST, NORTH (ie most projected CRS), return {1,2}
   -  for NORTH, EAST, return {2,1}
   -  for North Pole CRS, with East/SOUTH, North/SOUTH, such as
      EPSG:5041 ("WGS 84 / UPS North (E,N)"), would return {1,2}
   -  for North Pole CRS, with northing/SOUTH, easting/SOUTH, such as
      EPSG:32661 ("WGS 84 / UPS North (N,E)"), would return {2,1}
   -  similarly for South Pole CRS
   -  for all other cases, return {1,2}

OGRCreateCoordinateTransformation() now honors the data axis to srs axis
mapping.

Note: contrary to what I indicated in a previous email, gdaltransform
behavior is unchanged, since internally the GDALTransform mechanism
forces the GIS friendly order.

Raster datasets are modified to call
SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER) on the
OGRSpatialReference\* they return, and assumes it in SetSpatialRef()
(assumed and unchecked for now)

Vector layers mostly all call
SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER) on the
OGRSpatialReference\* returned by GetSpatialRef(). In the case of the
GML driver, if the user defines the INVERT_AXIS_ORDER_IF_LAT_LONG open
option, axis swapping is not done (as previously) and the
AUTHORITY_COMPLIANT strategy is used. ICreateLayer() when receiving a
OGRSpatialReference\* may decide (and most will do it) to change the
axis mapping strategy. That is: if it receives a OGRSpatialReference
with AUTHORITY_COMPLIANT order, it may decide to switch to
TRADITIONAL_GIS_ORDER and GetSpatialRef()::GetDataAxisToSRSAxisMapping()
will reflect that. ogr2ogr is modified to do the geometry axis swapping
in that case.

Related to that change, WKT 1 export now always return the AXIS element,
and EPSG:xxxx thus behaves identically to EPSGA:xxxx

So a summary view of this approach is that in the formal SRS definition,
we no longer do derogations regarding axis order, but we add an
additional interface to describe how we actually make our match match
with the SRS definition.

드라이버 변경 사항
~~~~~~~~~~~~~~~~~~

Raster drivers that returned / accepted a SRS as a WKT string through
the GetProjectionRef(), SetProjection(), GetGCPProjection() and
SetGCPs() methods have been upgraded to use the new virtual methods, in
most cases by using the compatibility layer.

The GDALPamDataset (PAM .aux.xml files) and the GDAL VRT drivers have
been fully upgraded to support the new interfaces, and
serialize/deserialize the data axis to SRS axis mapping values.

The GeoPackage driver now fully supports the official "gpkg_crs_wkt"
extension used to store WKT 2 string definitions in the
gpkg_spatial_ref_sys table. The driver attempts at not using the
extension when SRS can be encoded as WKT1 strings, and will
automatically add the "definition_12_063" column to an existing
gpkg_spatial_ref_sys table if a SRS requiring WKT2 (typically a
Geographic 3D CRS) is inserted.

유틸리티 변경 사항
~~~~~~~~~~~~~~~~~~

-  gdalinfo and ogrinfo reports the data axis to CRS axis mapping
   whenever a CRS is reported. They will also output WKT2_2018 by
   default, unless "-wkt_format wkt1" is specified.

::

   Driver: GTiff/GeoTIFF
   Files: out.tif
   Size is 20, 20
   Coordinate System is:
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
       USAGE[
           SCOPE["unknown"],
           AREA["World"],
           BBOX[-90,-180,90,180]],
       ID["EPSG",4326]]
   Data axis to CRS axis mapping: 2,1 <-- here
   Origin = (2.000000000000000,49.000000000000000)
   Pixel Size = (0.100000000000000,-0.100000000000000)

-  gdalwarp, ogr2ogr and gdaltransform have gained a -ct switch that can
   be used by advanced users to specify a coordinate operation, either
   as a PROJ string (generally a +proj=pipeline), or a WKT coordinate
   operation/concatenated operation, as explained in the above
   "OGRCoordinateTransformation changes" paragraph. Note: the pipeline
   must take into account the axis order of the CRS, even if the
   underlying raster/vector drivers use the "GIS friendly" order. For
   example "+proj=pipeline +step +proj=axisswap +order=2,1 +step
   +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=31
   +ellps=WGS84" when transforming from EPSG:4326 to EPSG:32631.

-  gdalsrsinfo is enhanced to be able to specify the 2 new supported WKT
   variants: WKT2_2015 and WKT2_2018. It will default to outputting
   WKT2_2018

SWIG 바인딩 변경 사항
~~~~~~~~~~~~~~~~~~~~~

The enhanced ExportToWkt() and OGRCoordinateTransformation methods are
available through SWIG bindings. May require additional typemaps for
non-Python languages (particularly for the support of 4D X,Y,Z,time
coordinates)

하위 호환성
-----------

This work is intended to be *mostly* backward compatible, yet inevitable
differences will be found. For example the WKT 1 and PROJ string export
has been completely rewritten in PROJ, and so while being hopefully
equivalent to what GDAL 2.4 or earlier generated, this is not strictly
identical: number of significant digits, order of PROJ parameters,
rounding, etc etc...

MIGRATION_GUIDE.TXT has been updated to reflect some differences:

-  OSRImportFromEPSG() takes into account official axis order.
-  removal of OPTGetProjectionMethods(), OPTGetParameterList() and
   OPTGetParameterInfo() No equivalent.
-  removal of OSRFixup() and OSRFixupOrdering(): no longer needed since
   objects constructed are always valid
-  removal of OSRStripCTParms(). Use OSRExportToWktEx() instead with the
   FORMAT=SQSQL option
-  exportToWkt() outputs AXIS nodes
-  OSRIsSame(): now takes into account data axis to CRS axis mapping,
   unless IGNORE_DATA_AXIS_TO_SRS_AXIS_MAPPING=YES is set as an option
   to OSRIsSameEx()
-  ogr_srs_api.h: SRS_WKT_WGS84 macro is no longer declared by default
   since WKT without AXIS is too ambiguous. Preferred remediation: use
   SRS_WKT_WGS84_LAT_LONG. Or #define USE_DEPRECATED_SRS_WKT_WGS84
   before including ogr_srs_api.h

Out-of-tree raster drivers will be impacted by the introduction of the
new virtual methods GetSpatialRef(), SetSpatialRef(), GetGCPSpatialRef()
and SetGCPs(..., const OGRSpatialReference\* poSRS), and the removal of
their older equivalents using WKT strings instead of a
OGRSpatialReference\* instance.

문서화
------

New methods have been documented, and documentation of existing methods
has been changed when appropriate during the development. That said, a
more thorough pass will be needed. The tutorials will also have to be
updated.

테스트
------

The autotest suite has been adapted in a number of places since the
expected results have changed for a number of reasons (AXIS node
exported in WKT, differences in WKT and PROJ string generation). New
tests have been added for the new capabilities.

It should be noted that autotest not necessarily checks everything, and
issues have been discovered and fixed through manual testing. The
introduction of the "data axis to CRS axis mapping" concept is also
quite error prone, as it requires setting the OAMS_TRADITIONAL_GIS_ORDER
strategy in a lot of different places.

So users and developers are kindly invited to thoroughly test GDAL once
this work has landed in master.

구현
----

이벤 루올(`Spatialys <http://www.spatialys.com>`_)이 `gdalbarn <https://gdalbarn.com/>`_ 의 후원을 받아 이 RFC를 구현했습니다.

제안한 구현은 `풀 요청 1185번 <https://github.com/OSGeo/gdal/pull/1185>`_ 에서 사용할 수 있습니다.

While it is provided as a multiple commit for """easier""" review, it will be probably squashed in a single commit for inclusion in master, as intermediate steps are not all buildable, due to PROJ symbol renames having occurred during the development, which would break bisectability.

투표 이력
---------

-  하워드 버틀러 +1
-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

수정 사항
---------

2019년 5월 2일: GDAL 2.5를 GDAL 3.0으로 변경

