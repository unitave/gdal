.. _rfc-61:

=======================================================================================
RFC 61 : 측정 도형 지원
=======================================================================================

저자: 아리 욜마(Ari Jolma)

연락처: ari.jolma@gmail.com

상태: 승인, GDAL 2.1버전에 구현

요약
----

이 RFC는 측정(measured) 도형을 구현하는 방법을 정의합니다. (측정 도형이란 포인트가 M 좌표를 가진, 예를 들어 XYM 또는 XYZM인 도형을 말합니다.)

근거
----

"측정값(measure)으로도 알려진 M 좌표는 도형의 각 포인트에 저장할 수 있는 추가적인 값입니다. (`IBM 기술 메모 <https://www.ibm.com/support/pages/what-are-semantics-m-coordinate-measure>`_ 를 참조하십시오.)

M 좌표는 OGC 단순 피처(Simple Feature) 모델에 포함되며 많은 벡터 데이터 포맷에서 사용됩니다.

변경 사항
---------

C++ API에 변경 사항을 적용해야 하며, C API를 개선해야 합니다. 이 개선 사항을 이용하기 위해서는 물론 C++ API의 변경 때문에라도 몇몇 드라이버를 변경해야 합니다.

공통 API
~~~~~~~~

새로운 OGRwkbGeometryType 값이 필요합니다. SFSQL 1.2 및 ISO SQL/MM Part 3를, 예를 들어 M에 대해 2차원 유형 + 2000을 그리고 ZM에 대해 2차원 유형 + 3000을 사용할 것입니다. (또한 현재 구현되지은 않았지만 완벽성을 위해 Tin, PolyhedralSurface 및 Triangle 같은 유형들을 추가할 수 있습니다.) (`#6401 티켓 <https://trac.osgeo.org/gdal/ticket/6401>`_ 에 따라) wkbCurve 및 wkbSurface를 #define으로부터 OGRwkbGeometryType 열거형으로 이동시켰고, 그 Z/M/ZM 변이형들도 추가했습니다.

좀 더 일반적으로 말하자면, 깔끔한 값들의 집합을 사용하는 경로가 있을 수 있으며 (있어야 하며?) 레거시 지원을 예외로 할 수 있습니다.

추상 유형을 정의하는데 열거형의 일부로 정의하지는 않습니다.

::

   // OGRwkbGeometryType 열거형에 추가
       wkbCurve = 13,          /**< 곡선 (추상 유형). ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbSurface = 14,        /**< 면 (추상 유형). ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolyhedralSurface = 15,/**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTIN = 16,              /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTriangle = 17,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */

       wkbCurveZ = 1013,           /**< Z 구성 요소를 가진 wkbCurve. ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbSurfaceZ = 1014,         /**< Z 구성 요소를 가진 wkbSurface. ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolyhedralSurfaceZ = 1015,  /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTINZ = 1016,                /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTriangleZ = 1017,           /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */

       wkbPointM = 2001,              /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbLineStringM = 2002,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolygonM = 2003,            /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiPointM = 2004,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiLineStringM = 2005,    /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiPolygonM = 2006,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbGeometryCollectionM = 2007, /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCircularStringM = 2008,     /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCompoundCurveM = 2009,      /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCurvePolygonM = 2010,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiCurveM = 2011,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiSurfaceM = 2012,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCurveM = 2013,              /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbSurfaceM = 2014,            /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolyhedralSurfaceM = 2015,  /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTINM = 2016,                /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTriangleM = 2017,           /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */

       wkbPointZM = 3001,              /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbLineStringZM = 3002,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolygonZM = 3003,            /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiPointZM = 3004,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiLineStringZM = 3005,    /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiPolygonZM = 3006,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbGeometryCollectionZM = 3007, /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCircularStringZM = 3008,     /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCompoundCurveZM = 3009,      /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCurvePolygonZM = 3010,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiCurveZM = 3011,         /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbMultiSurfaceZM = 3012,       /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbCurveZM = 3013,              /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbSurfaceZM = 3014,            /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbPolyhedralSurfaceZM = 3015,  /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTINZM = 3016,                /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */
       wkbTriangleZM = 3017,           /**< ISO SQL/MM Part 3. GDAL 2.1 이상 버전 */

   // M에 대한 테스트 추가
   #define wkbHasM(x)     OGR_GT_HasM(x)
   #define wkbSetM(x)     OGR_GT_SetM(x)

   OGRwkbGeometryType CPL_DLL OGR_GT_SetM( OGRwkbGeometryType eType );
   int                CPL_DLL OGR_GT_HasM( OGRwkbGeometryType eType );
           

C++ API
~~~~~~~

:cpp:class:`OGRGeometry` 클래스에 있는 ``int nCoordinateDimension`` 속성을 ``int`` 플래그로 대체할 것입니다. 다음 플래그들을 가질 수도 있습니다:

::

   #define OGR_G_NOT_EMPTY_POINT 0x1
   #define OGR_G_3D 0x2
   #define OGR_G_MEASURED 0x4
   #define OGR_G_IGNORE_MEASURED 0x8

하위 호환성을 위해 내부적으로 "ignore" 플래그가 필요합니다. OGR_G_NOT_EMPTY_POINT 플래그는 :cpp:class:`OGRPoint` 객체가 비어 있음을 나타내기 위해서만 사용합니다.

현재 비어 있는 포인트를 나타내기 위해 nCoordDimension를 음의 값으로 설정하는 꼼수를 사용하고 있습니다.

nCoordinateDimension을 제거하면 이를 가져오거나 설정하는 드라이버 등등을 변경해야 할 수도 있습니다.

다음을 테스트합니다:

::

   Is3D = flags & OGR_G_3D
   IsMeasured = flags & OGR_G_MEASURED

세터(setter) 및 게터(getters)를 ``|=`` 및 ``&=`` 로 구현합니다.

이 플래그들 가운데 하나라도 설정하거나 설정 해제하는 경우, 대응하는 데이터가 무결하지 않게 되어 폐기될 수도 있습니다.

다음 메소드들이 원래 의미 체계를 가지도록, 예를 들어 좌표 차원을 2 또는 3으로 유지하지만, 퇴출시키십시오. 문서에 일부 모순점들이 존재합니다. 메소드 문서에는 비어 있는 포인트에 대해 0을 반환할 수도 있다고 적혀 있지만 :file:`ogrpoint.cpp` 에는 비어 있는 포인트에 대해 음의 nCoordDimension 값을 사용하고 포인트의 getCoordinateDimension 메소드는 nCoordDimension의 절대값을 -- 따라서 0이 아닌 값을 -- 반환한다고 되어 있습니다. 문서를 수정하는 것으로 충분할 것입니다.

::

   int getCoordinateDimension();
   void setCoordinateDimension(int nDimension);
   void flattenTo2D()

getCoordinateDimension()을 대체할 새 메소드를 추가할 수 있다고 제안합니다. set3D() 및 setMeasured()가 setCoordinateDimension() 및 flattenTo2D()를 대체할 것입니다. 다음을 참조하십시오.

:cpp:class:`OGRGeometry` 클래스:

::

   //추가할 수도 있는 메소드들 (SF 공통 아키텍처):
   int Dimension(); // 비어 있는 도형의 경우 (정의되지 않았다는 사실을 나타내는) -1, 포인트의 경우 0, 곡선의 경우 1, 면의 경우2, 도형 집합의 경우 구성 요소들의 최대값
   char *GeometryType(); // OGRToOGCGeomType을 호출합니다. (개선이 필요합니다.)

   //추가할 메소드들 (SF 공통 아키텍처) 구현에 대해서는 앞을 참조하십시오:
   int CoordinateDimension(); // 3차원이 아니고 측정되지 않은 경우 2, 3차원이거나 측정된 경우 3, 3차원이고 측정된 경우 4
   OGRBoolean Is3D() const;
   OGRBoolean IsMeasured() const;

   //추가할 메소드들 (비표준; 두 번째 unset* 메소드 대신 메소드 하나를 사용한다는 사실을 기억하십시오):
   virtual void set3D(OGRBoolean bIs3D);
   virtual void setMeasured(OGRBoolean bIsMeasured);

   //지금 또는 나중에 추가할 메소드들:
   virtual OGRGeometry *LocateAlong(double mValue);
   virtual OGRGeometry *LocateBetween(double mStart, double mEnd);

   //importPreambleFromWkb에서 b3D 제거: 사용되지 않으며, 메소드 내부에서 플래그들을 관리합니다.

``int CoordinateDimension()`` 이 새 의미 체계를 가져야 합니다. 단순 피처 문서에 있는 메소드 이름에는 사실 ``get`` 접두어가 없습니다.

set3D() 및 setMeasured()가 도형 집합에 있는 하위(children) 도형에 영향을 미쳐야 하는지 여부가 문제점입니다. 현재 setCoordinateDimension() 문서에는 "도형 집합의 차원을 설정하는 것이 하위 도형에 영향을 미칠 것"이라고 적혀 있기 때문에, 이미 도형 집합에 있는 하위 도형의 차원을 유지하기로 한 것입니다. set3D() 및 setMeasured() 메소드가 (하위일 수도 있는 도형 포함) 도형에서 Z 또는 M 값을 추가하거나 제거할 것을 제안합니다. 일반적으로 Z와 관련한 기존 (예를 들어 제거 또는 추가) 전략을 따라야 할 것입니다.

:cpp:class:`OGRPoint` 클래스에 ``double m`` 속성을 추가합니다. 이를 위한 구성자, 게터 및 세터를 추가합니다.

:cpp:class:`OGRSimpleCurve` 클래스에 ``double *padfM`` 속성을 추가합니다. 이를 위한 구성자, 게터 및 세터를 추가합니다. XYM 데이터에 대해 접미어 M이 붙은 새 세터가 필요합니다. 객체가 세터에서 XY로부터 XYZ로 업드레이드될 수도 있기 때문입니다. Make3D() 및 Make2D()와 비슷한 의미 체계를 가진 RemoveM() 및 AddM() 메소드도 추가합니다.

setCoordinateDimension()이 대체되는 클래스들에서 set3D() 및 setMeasured() 메소드를 대체합니다.

이름이 ``_`` 로 시작하고 "int b3D" 파라미터를 가진 메소드들의 의미 체계를 변경합니다. 이 파라미터는 예를 들어 Z 및 M에 대해 알려주는 "int" 같은 플래그인 "int coordinates"가 될 것입니다.

C API
~~~~~

:file:`ogr_core.h`:

::

   OGRwkbGeometryType CPL_DLL OGR_GT_SetM( OGRwkbGeometryType eType );
   int                CPL_DLL OGR_GT_HasM( OGRwkbGeometryType eType );

현재 습성은 좌표 차원이 2인 도형에 SetPoint()를 호출하면 좌표 차원을 3으로 업드레이드하는 것입니다. 2차원 포인트로 유지하려면 SetPoint_2D() 2차원 메소드를 사용해야만 합니다. 따라서 M 및 ZM 도형에 대해서도 개별 함수가 필요합니다. AddPoint()에 대해 예를 들어 SetPointM(), SetPointZM()처럼 접미어 M 및 ZM을 붙일 것을 제안합니다.

현재 SetPoints_2D() 함수가 존재하지 않습니다. SetPoints() 함수의 'pabyZ' 파라미터의 주석에는 "2차원 객체의 경우 기본값이 NULL"이라고 되어 있지만 그렇지 않은 것으로 보입니다. `#6344 티켓 <https://trac.osgeo.org/gdal/ticket/6344>`_ 을 참조하십시오. 이 티켓에 적힌 대로 수정된다면, SetPointsZM()만 필요합니다.

GetPoint() 및 GetPoints()에는 2차원 버전이 없기 때문에, ``*ZM`` 버전만 필요합니다.

:file:`ogr_api.h`:

::

   void   CPL_DLL OGR_G_Is3D( OGRGeometryH );
   void   CPL_DLL OGR_G_IsMeasured( OGRGeometryH );

   void   CPL_DLL OGR_G_Set3D( OGRGeometryH, int );
   void   CPL_DLL OGR_G_SetMeasured( OGRGeometryH, int );

   double CPL_DLL OGR_G_GetM( OGRGeometryH, int );

:file:`ogr_p.h` (공개 헤더이기 때문에 새 함수들이 필요합니다):

::

   const char CPL_DLL * OGRWktReadPointsM( const char * pszInput,
                                          OGRRawPoint **ppaoPoints, 
                                          double **ppadfZ,
                                           double **ppadfM,
                                          int * pnMaxPoints,
                                          int * pnReadPoints );
   void CPL_DLL OGRMakeWktCoordinateM( char *, double, double, double, double, int ); // int = flags OGR_G_3D OGR_G_MEASURED
   // OGRReadWKBGeometryType의 의미 체계 변경: b3D를 사용하지 않으며 반환되는 eGeometryType이 어떤 무결한 유형이라도 될 수 있습니다.

:file:`pggeometry.h` 는 내부 헤더이기 때문에 함수 프로토타입을 변경할 수 있습니다:

::

   void OGRCreateFromMultiPatchPart(OGRMultiPolygon *poMP,
                                    OGRPolygon*& poLastPoly,
                                    int nPartType,
                                    int nPartPoints,
                                    double* padfX,
                                    double* padfY,
                                    double* padfZ,
                                    double* padfM);

'padfM' 파라미터를 사용하기 때문에 OpenFileGDB 드라이버를 변경해야 합니다.

GEOS, 필터 및 기타 문제점
~~~~~~~~~~~~~~~~~~~~~~~~~

측정값을 가진 도형을 GEOS로 전송하거나 필터로 사용하는 경우 M 좌표를 무시합니다.

LocateAlong() 및 LocateBetween()만이 M을 사용하는 표준 메소드지만, 예를 들어 M의 범위를 가져오는 다른 메소드가 존재할 수 있습니다. 현재 그런 메소드를 추가할 계획은 없지만 향후 추가할 수도 있습니다.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

새 C API 함수들을 SWIG을 통해 노출시켜야 합니다. 언어 바인딩들이 좌표를 인식하느냐에 따라 다음 변경 사항들이 달라집니다. 적어도 파이썬과 펄은 좌표를 인식합니다.

i 파일에 새 도형 유형들을 포함시킬 것입니다.

M에 대해 몇몇 새로운 세터와 게터가 필요합니다. Is3D(), IsMeasured(), Set3D() 및 SetMeasured() 메소드는 물론 OGR_GT_HasM() 메소드도 추가해야 합니다.

드라이버
--------

C++ 변경 사항 때문에 영향을 받을 수도 있는 (CoordinateDimension API를 사용하는) 드라이버들은 최소한 다음과 같습니다:

   -  PG
   -  MSSQLSpatial
   -  SQLite
   -  DB2
   -  MySQL
   -  GML
   -  PGDump
   -  GeoJSON
   -  LibKML
   -  GPKG
   -  WASP
   -  GPX
   -  FilegDB
   -  VFK
   -  BNA
   -  DXF

현재 퇴출된 CoordinateDimension API를 ``*3D()`` 및 ``*Measured()`` 호출로 대체할 것을 제안합니다.

M 좌표에 대한 지원이 자리를 잡으면 드라이버가 해당 지원을 노출시킬 것입니다.

이 RFC의 작업 내용은 Memory, Shapefile 및 PG 드라이버에 M 좌표 지원을 빌드하는 것을 포함합니다. 다른 드라이버들에 지원을 구현하는 것은 향후 작업할 계획입니다.

유틸리티
--------

최소 요구 사항 및 새로운 가능성이 있습니다.

-  ogrinfo: 측정 도형 유형 및 측정값을 리포트합니다.
-  ogr2ogr: 측정 도형 유형을 리포트합니다.
-  ogrlineref: 분명히 측정값을 처리하는 것으로 보이며, 더 많은 생각이 필요합니다.
-  gdal_rasterize: 작성(burn-in) 값을 위해 측정값을 사용할 수 있습니다.
-  gdal_contour: 측정값을 "표고" 값으로 사용할 수 있습니다.
-  gdal_grid: 측정값을 "Z" 값으로 사용할 수 있습니다.

문서화
------

새 메소드 및 함수를 모두 문서화합니다.

테스트 스위트
-------------

펄 유닛 테스트(:file:`swi/perl/t/measures-\*.t`)로 적어도 초기 테스트를 수행할 것입니다. 향후 자동 테스트 스위트를 확장할 것입니다. 기존 테스트들은 통과할 것입니다.

호환성 문제점
-------------

측정값을 지원하는 드라이버 (실제로는 데이터셋 및 레이어) 다수에 해당 지원을 추가해야 합니다. 다음을 이용해서 지원 사실을 노출시켜야 합니다:

::

   #define ODsCMeasuredGeometries   "MeasuredGeometries"
   #define OLCMeasuredGeometries    "MeasuredGeometries"

레이어 생성을 위한 입구점(entry point)은 :cpp:class:`GDALDataset` 에 있는 CreateLayer() 메소드입니다. 데이터셋이 측정 도형을 지원하지 않는 경우 이 메소드가 파라미터로 가져오는 도형 유형의 측정 플래그를 제거할 것입니다. 이 습성은 비선형 도형 유형 및 데이터셋이 측정 도형을 지원하지 않는 현재 습성과 일관성을 유지합니다.

레이어 생성 케이퍼빌리티를 구현한 모든 드라이버가 가지고 있는 ICreateLayer()는 도형 유형을 인자로 가지고 있습니다. 이 메소드는 CPLError()를 CPLE_NotSupported로 호출해서 드라이버가 측정값을 지원하지 않는 경우 NULL을 반환해야 합니다. ICreateFeature() 및 ISetFeature()도 마찬가지입니다.

사용자 지향 API 함수(CreateLayer, CreateFeature 및 SetFeature)는 측정값을 지원하지 않는 드라이버에 있는 ``I*()`` 메소드로 진행하기 전에 측정값을 (암묵적으로) 제거해야 합니다. 몇몇 사용례 시나리오에서는 이런 부작용을 원하지 않겠지만 이미 비선형 도형 작업 시 수행한 패턴을 따를 것입니다. 이런 내용을 문서화해야 합니다.

이에 대한 대안은 M 값(들)을 (또는 WKT/WKB를) (도형 유형에 따라 스칼라(scalar) 또는 벡터) 속성으로 저장하는 것입니다.

결정이 필요합니다.

몇몇 불호환성이 어쩔 수 없이 발생할 것입니다. 예를 들어 Shapefile 드라이버에서 현재의 XYM과 XYZ를 동일하게(XYM-as-XYZ) 취급하는 꼼수는 제대로 된 XYM으로 대체될 것입니다.

관련 티켓
---------

-  `#6063 티켓 <https://trac.osgeo.org/gdal/ticket/6063>`_
-  `#6331 티켓 <https://trac.osgeo.org/gdal/ticket/6331>`_

구현
----

아리 욜마가 이 RFC를 구현할 것입니다.

제안한 구현은 `https://github.com/ajolma/GDAL-XYZM <https://github.com/ajolma/GDAL-XYZM>`_ 에 있을 것입니다.

투표 이력
---------

-  이벤 루올 +1
-  세케레시 터마시 +1
-  유카 라흐코넨 +1
-  대니얼 모리셋 +1

