.. _rfc-64:

=======================================================================================
RFC 64: 삼각형, 다면체 표면 및 TIN
=======================================================================================

저자: 아비야브 쿠마르 싱(Avyav Kumar Singh), 이벤 루올

연락처: avyavkumar@gmail.com, even.rouault@spatialys.com

상태: 승인, GDAL 2.2버전에 구현

요약
----

현재로서는, (모든 하위 유형이 이로부터 파생되는 기반 클래스인) :cpp:class:`OGRGeometry` 클래스가 OGRCompoundCurve, OGRCircularString, OGRLinearRing, OGRMultiLineString, OGRMultiPoint, OGRMultiPolygon, OGRMultiCurve, OGRSimpleCurve, OGRCurvePolygon 그리고 OGRPolygon으로 제한되어 있습니다.

이 RFC는 :cpp:class:`OGRGeometry` 에 다음과 같은 새로운 도형들을 추가할 것을 제안합니다:

-  Triangle(삼각형):
   폴리곤의 부분 집합으로, 궁극적인 차이는 노드 3개만으로 (실제로는 마지막 노드가 첫 번째 노드의 반복인 노드 4개로) 이루어지며 외부 경계선이 **하나 뿐** 이며 내부 폴리곤은 **없다*** 는 점입니다.
   
-  PolyhedralSurface(다면체 표면):
   폴리곤으로만 이루어진 3차원 형상입니다.

-  TriangulatedSurface(삼각분할 표면):
   PolyhedralSurface의 부분 집합으로, Triangle로만 이루어진 3차원 형상입니다.

참조 문서
---------

-  `오픈GIS 단순 피처 접근(Simple Feature Access) 1부: 공통 아키텍처, v 1.2.1 <http://portal.opengeospatial.org/files/?artifact_id=25355>`_, 약칭 SFA 1.2.1

-  `WKT 인코딩의 BNF <https://github.com/postgis/postgis/blob/svn-trunk/doc/bnf-wkt.txt>`_:
   SQL/MM Part 3로부터 발췌

-  `WKB 인코딩의 BNF <https://github.com/postgis/postgis/blob/svn-trunk/doc/bnf-wkb.txt>`_:
   SQL/MM Part 3로부터 발췌

핵심 변경 사항
--------------

새 클래스 계층(hierarchy)은 다음과 같으며, 대부분 SQL/MM Part 3와 일치합니다.

.. image:: ../../../images/rfc64/classOGRGeometry_RFC64.png

이 제안 이전에 이미 :file:`ogr_core.h` 에 필요한 WKB 코드를 포함시키는 등 몇몇 기초 작업을 수행했습니다.

뿐만 아니라, `SFCGAL <http://www.sfcgal.org/>`_ 라이브러리는 GDAL의 새로운 선택적 의존성입니다. (현재 유닉스 상에서만 빌드를 지원합니다.) 빌드를 테스트한 최저 버전은 (우분투 16.04에서 찾아볼 수 있는) 1.2.2입니다. SFCGAL 라이브러리 홈페이지에서 언급했듯이, "SFCGAL은 CGAL을 감싸는 C++ 래퍼(wrapper) 라이브러리로 그 목적은 3차원 작업을 위해 ISO 19107:2013 및 OGC 단순 피처 접근 1.2버전을 지원하는 것입니다." PostGIS가 이 라이브러리를 잠재적인 도형 백엔드(backend)로 주로 사용합니다. 이 라이브러리는 C API를 가지고 있는데, 이를 사용할 것입니다.

도형 피연산자 가운데 하나가 Triangle, PolyhedralSurface 또는 TIN(Triangulated Irregular Network)인 즉시, :cpp:class:`OGRGeometry` 의 메소드들(현재 IsValid(), Distance(), ConvexHull(), Intersection(), Union(), Difference(), SymDifference(), Crosses())이 SFCGAL 함수들을 사용할 수도 있습니다.

SFCGAL 도형과 OGR 도형 간의 변환을 위해 새로운 :cpp:class:`OGRGeometry` 메소드 2개를 사용합니다:

::

   static sfcgal_geometry_t* OGRexportToSFCGAL(OGRGeometry *poGeom);
   static OGRGeometry* SFCGALexportToOGR(sfcgal_geometry_t* _geometry);

SFCGAL 이외에도, 어떤 경우 GEOS 메소드를 계속 사용하지만 다음과 같은 제한 사항이 있습니다:

   -  Triangle은 외곽 고리 하나를 가진 폴리곤으로 변환됩니다.
   -  PolyhedralSurface 및 TriangulatedSurface는 폴리곤의 GeometryCollection(도형 집합)으로 변환됩니다. (TriangulatedSurface에 있는 Triangle은 각각 앞에서 설명한 폴리곤으로 변환됩니다.)

이번에 도입된 새 도형들을 위한 API는 다음을 포함합니다:

-  Triangle API의 경우 폴리곤 용 기존 메소드를 덮어씁니다. 다음은 완전한 API입니다:

::

   class CPL_DLL OGRTriangle : public OGRPolygon
   {
     private:
       bool quickValidityCheck() const;

     protected:
   //! @cond Doxygen_Suppress
       virtual OGRSurfaceCasterToPolygon   GetCasterToPolygon() const CPL_OVERRIDE;
       virtual OGRErr importFromWKTListOnly( char ** ppszInput, int bHasZ, int bHasM,
                                          OGRRawPoint*& paoPoints, int& nMaxPoints,
                                          double*& padfZ ) CPL_OVERRIDE;
   //! @endcond

     public:
       OGRTriangle();
       OGRTriangle(const OGRPoint &p, const OGRPoint &q, const OGRPoint &r);
       OGRTriangle(const OGRTriangle &other);
       OGRTriangle(const OGRPolygon &other, OGRErr &eErr);
       OGRTriangle& operator=(const OGRTriangle& other);
       virtual ~OGRTriangle();
       virtual const char *getGeometryName() const CPL_OVERRIDE;
       virtual OGRwkbGeometryType getGeometryType() const CPL_OVERRIDE;

       // IWks 인터페이스
       virtual OGRErr importFromWkb( unsigned char *, int = -1,
                                     OGRwkbVariant=wkbVariantOldOgc ) CPL_OVERRIDE;
       virtual OGRErr importFromWkt( char ** ) CPL_OVERRIDE;

       // OGRPolygon/OGRCurvePolygon/OGRGeometry virtual OGRErr 
       // addRingDirectly( OGRCurve * poNewRing ) CPL_OVERRIDE로부터 재작성된 새 메소드들;

   //! @cond Doxygen_Suppress
       static OGRGeometry* CastToPolygon(OGRGeometry* poGeom);
   //! @endcond
   };

-  PolyhedralSurface API는 :cpp:class:`OGRSurface` 로부터 파생됩니다. 내부적으로 이 API는 PolyhedralSurface를 구성하는 모든 폴리곤을 저장하기 위해 :cpp:class:`OGRMultiPolygon` 을 사용합니다. 메소드들의 구현 대부분은 이 조건이 유지되도록 보장하는 확인과 함께 대응하는 :cpp:class:`OGRMultiPolygon` 메소드들을 참조할 뿐입니다:

::

   class CPL_DLL OGRPolyhedralSurface : public OGRSurface
   {
     protected:
   //! @cond Doxygen_Suppress
       friend class OGRTriangulatedSurface;
       OGRMultiPolygon oMP;
       virtual OGRSurfaceCasterToPolygon      GetCasterToPolygon() const CPL_OVERRIDE;
       virtual OGRSurfaceCasterToCurvePolygon GetCasterToCurvePolygon() const CPL_OVERRIDE;
       virtual OGRBoolean         isCompatibleSubType( OGRwkbGeometryType ) const;
       virtual const char*        getSubGeometryName() const;
       virtual OGRwkbGeometryType getSubGeometryType() const;
       OGRErr exportToWktInternal (char ** ppszDstText, OGRwkbVariant eWkbVariant, const char* pszSkipPrefix ) const;

       virtual OGRPolyhedralSurfaceCastToMultiPolygon GetCasterToMultiPolygon() const;
       static OGRMultiPolygon* CastToMultiPolygonImpl(OGRPolyhedralSurface* poPS);
   //! @endcond

     public:
       OGRPolyhedralSurface();
       OGRPolyhedralSurface(const OGRPolyhedralSurface &poGeom);
       virtual ~OGRPolyhedralSurface();
       OGRPolyhedralSurface& operator=(const OGRPolyhedralSurface& other);

       // IWks 인터페이스
       virtual int WkbSize() const CPL_OVERRIDE;
       virtual const char *getGeometryName() const CPL_OVERRIDE;
       virtual OGRwkbGeometryType getGeometryType() const  CPL_OVERRIDE;
       virtual OGRErr importFromWkb( unsigned char *, int=-1, OGRwkbVariant=wkbVariantOldOgc ) CPL_OVERRIDE;
       virtual OGRErr exportToWkb( OGRwkbByteOrder, unsigned char *, OGRwkbVariant=wkbVariantOldOgc ) const CPL_OVERRIDE;
       virtual OGRErr importFromWkt( char ** )  CPL_OVERRIDE;
       virtual OGRErr exportToWkt( char ** ppszDstText, OGRwkbVariant=wkbVariantOldOgc ) const  CPL_OVERRIDE;

       // IGeometry 메소드
       virtual int getDimension() const  CPL_OVERRIDE;

       virtual void empty()  CPL_OVERRIDE;

       virtual OGRGeometry *clone() const  CPL_OVERRIDE;
       virtual void getEnvelope(OGREnvelope * psEnvelope) const  CPL_OVERRIDE;
       virtual void getEnvelope(OGREnvelope3D * psEnvelope) const  CPL_OVERRIDE;

       virtual void flattenTo2D() CPL_OVERRIDE;
       virtual OGRErr transform(OGRCoordinateTransformation*) CPL_OVERRIDE;
       virtual OGRBoolean Equals(OGRGeometry*) const CPL_OVERRIDE;
       virtual double get_Area() const CPL_OVERRIDE;
       virtual OGRErr PointOnSurface(OGRPoint*) const CPL_OVERRIDE;

       static OGRMultiPolygon* CastToMultiPolygon(OGRPolyhedralSurface* poPS);
       virtual OGRBoolean hasCurveGeometry(int bLookForNonLinear = FALSE) const CPL_OVERRIDE;
       virtual OGRErr addGeometry( const OGRGeometry * );
       OGRErr addGeometryDirectly(OGRGeometry *poNewGeom);
       int getNumGeometries() const;
       OGRGeometry* getGeometryRef(int i);
       const OGRGeometry* getGeometryRef(int i) const;

       virtual OGRBoolean  IsEmpty() const CPL_OVERRIDE;
       virtual void setCoordinateDimension( int nDimension ) CPL_OVERRIDE;
       virtual void set3D( OGRBoolean bIs3D ) CPL_OVERRIDE;
       virtual void setMeasured( OGRBoolean bIsMeasured ) CPL_OVERRIDE;
       virtual void swapXY() CPL_OVERRIDE;
       OGRErr removeGeometry( int iIndex, int bDelete = TRUE );
   };

-  TriangulatedSurface API는 PolyhedralSurface API와 유사하며, Triangle 형태의 하위 도형들을 구성하기 위해 실행되는 메소드를 포함시키기 위해 :cpp:class:`OGRMultiPolygon` 클래스를 약간 조정했습니다. (멀티폴리곤은 엄격하게 말해 폴리곤의 선택 집합입니다.) 이런 메소드들은 :cpp:class:`OGRMultiPolygon` 의 내부 메소드로 공개 사용자가 접근할 수 없습니다. 예를 들면, :cpp:func:`OGRMultiPolygon::addGeometryDirectly` 메소드는 추가되는 하위 도형이 POLYGON 유형이어야 하는지 확인합니다. 기존 함수를 건드리기보다, 이 확인 과정을 구현하지 않은 새 함수를 작성했습니다:

::

   /************************************************************************/
   /*                         _addGeometryDirectly()                       */
   /*             OGRTriangulatedSurface와만 함께 사용해야 합니다.         */
   /*                     다른 위치에서 사용하지 마십시오.                 */
   /************************************************************************/

   OGRErr OGRMultiPolygon::_addGeometryDirectly( OGRGeometry * poNewGeom )
   {
       if ( wkbFlatten(poNewGeom->getGeometryType()) != wkbTriangle)
           return OGRERR_UNSUPPORTED_GEOMETRY_TYPE;

       if( poNewGeom->Is3D() && !Is3D() )
           set3D(TRUE);

       if( poNewGeom->IsMeasured() && !IsMeasured() )
           setMeasured(TRUE);

       if( !poNewGeom->Is3D() && Is3D() )
           poNewGeom->set3D(TRUE);

       if( !poNewGeom->IsMeasured() && IsMeasured() )
           poNewGeom->setMeasured(TRUE);

       OGRGeometry** papoNewGeoms = (OGRGeometry **) VSI_REALLOC_VERBOSE( papoGeoms,
                                                sizeof(void*) * (nGeomCount+1) );
       if( papoNewGeoms == NULL )
           return OGRERR_FAILURE;

       papoGeoms = papoNewGeoms;
       papoGeoms[nGeomCount] = poNewGeom;
       nGeomCount++;

       return OGRERR_NONE;
   }

-  TriangulatedSurface API는 다음과 같습니다:

::

   class CPL_DLL OGRTriangulatedSurface : public OGRPolyhedralSurface
   {
     protected:
   //! @cond Doxygen_Suppress
       virtual OGRBoolean         isCompatibleSubType( OGRwkbGeometryType ) const CPL_OVERRIDE;
       virtual const char*        getSubGeometryName() const CPL_OVERRIDE;
       virtual OGRwkbGeometryType getSubGeometryType() const CPL_OVERRIDE;

       virtual OGRPolyhedralSurfaceCastToMultiPolygon GetCasterToMultiPolygon() const CPL_OVERRIDE;
       static OGRMultiPolygon* CastToMultiPolygonImpl(OGRPolyhedralSurface* poPS);
   //! @endcond

     public:
       OGRTriangulatedSurface();
       OGRTriangulatedSurface(const OGRTriangulatedSurface &other);
       ~OGRTriangulatedSurface();

       OGRTriangulatedSurface& operator=(const OGRTriangulatedSurface& other);
       virtual const char *getGeometryName() const CPL_OVERRIDE;
       virtual OGRwkbGeometryType getGeometryType() const CPL_OVERRIDE;

       // IWks 인터페이스
       virtual OGRErr addGeometry( const OGRGeometry * ) CPL_OVERRIDE;

       static OGRPolyhedralSurface* CastToPolyhedralSurface(OGRTriangulatedSurface* poTS);
   };

도형 유형
---------

새 도형들의 WKB 값은 다음과 같습니다:

.. list-table:: WKB values of Triangle, PolyhedralSurface and TIN
   :header-rows: 1

   * - 도형 유형
     - 2차원
     - Z
     - M
     - ZM
   * - PolyhedralSurface
     - 0015
     - 1015
     - 2015
     - 3015
   * - TIN
     - 0016
     - 1016
     - 2016
     - 3016
   * - Triangle
     - 0017
     - 1017
     - 2017
     - 3017

도형 변환
---------

:cpp:func:`OGRGeometryFactory::forceTo` 및 :cpp:func:`OGRGeometryFactory::forceToMultiPolygon` 메소드가 새 도형 유형들 간의 그리고 멀티폴리곤으로의 변환을 지원하도록 개선했습니다. TIN 또는 PolyhedralSurface 유형을 멀티폴리곤 유형으로 변환하는 것은 멀티폴리곤이 동일 평면에 도형들을 담아야 하기 때문에 의미 체계적으로 올바르지 않지만, 이런 새로운 도형 유형들을 지원하지 않는 포맷으로 변환하는 경우 도움이 될 수도 있다는 사실을 기억하십시오. (이런 변환은 예전에, 예를 들어 Shapefile 드라이버의 읽기 쪽에서 암묵적으로 수행되었습니다.)

드라이버 변경 사항
------------------

PostGIS
~~~~~~~

드라이버에 명확하게 어떤 변경도 하지 않았지만, PG <-> OGR 호환성이 유지되는지 확인했습니다. PostGIS 3차원 함수들은 OGR, 단순 스크립트 작업에 대해 동작합니다. 예를 들면 :file:`autotest/ogr/ogr_pg.py` 에는 다음과 같은 코드가 있습니다:

::

   wkt_list = ['POLYHEDRALSURFACE (((0 0 0,0 0 1,0 1 1,0 1 0,0 0 0)),((0 0 0,0 1 0,1 1 0,1 0 0,0 0 0)),((0 0 0,1 0 0,1 0 1,0 0 1,0 0 0)),((1 1 0,1 1 1,1 0 1,1 0 0,1 1 0)),((0 1 0,0 1 1,1 1 1,1 1 0,0 1 0)),((0 0 1,1 0 1,1 1 1,0 1 1,0 0 1)))',
                   'TIN (((0 0 0,0 0 1,0 1 0,0 0 0)),((0 0 0,0 1 0,1 1 0,0 0 0)))',
                   'TRIANGLE ((48 36 84,32 54 64,86 11 54,48 36 84))' ]

   for i in range(0,3):
           gdaltest.pg_ds.ExecuteSQL( "INSERT INTO zgeoms (field_no, wkb_geometry) VALUES (%d,GeomFromEWKT('%s'))" % ( i, wkt_list[i] ) )

Shapefile
~~~~~~~~~

Shapefile에는 "MultiPatch(멀티패치)" 객체라는 개념이 존재합니다. 멀티패치는 다음과 같은 여러 부분들로 이루어질 수 있습니다:

-  TriangleStrip:
   삼각형을 연결한 스트립으로, (처음 두 꼭짓점 이후의) 모든 꼭짓점이 새로운 삼각형을 완성합니다. 언제나 바로 이전의 두 꼭짓점에 새 꼭짓점을 연결해서 새 삼각형을 형성합니다.

-  TriangleFan:
   삼각형을 연결한 팬(fan)으로, (처음 두 꼭짓점 이후의) 모든 꼭짓점이 새로운 삼각형을 완성합니다. 언제나 바로 이전의 꼭짓점과 해당 부분의 첫 번째 꼭짓점에 새 꼭짓점을 연결해서 새 삼각형을 형성합니다.

-  Ring(외곽 고리, 내곽 고리, 첫 번째 고리, "유형이 정의되지 않은(non-typed)" 고리):
   지금까지는 멀티패치를 멀티폴리곤으로 읽어왔습니다. 이제 일반적으로 TriangleStrip/TriangleFan에 대응하는 0개 이상의 TIN과 모든 고리를 가진 0개 또는 1개의 멀티폴리곤을 가진 GeometryCollection을 반환할 것입니다. TIN 하나만 또는 멀티폴리곤 하나만 존재하는 경우 SHPT 레이어 생성 옵션이 MULTIPATCH 값을 인식하도록 확장되고, 레이어의 도형 유형 또는 첫 번째 피처의 도형 유형으로부터 형상(shape) 유형을 추측하는 현재 로직이 MULTIPATCH를 지원하도록 확장됩니다. MULTIPATCH 레이어는 TIN, POLYHEDRALSURFACE, MULTIPOLYGON 또는 GEOMETRYCOLLECTION(이 유형의 하위 도형은 앞의 세 가지 유형입니다) 유형의 도형을 받아들이고 멀티패치 객체로 변환하는데, 삼각형이 예상 순서인 경우 TriangleStrip 및 TriangleFan을 사용하려 시도합니다.

FileGDB, OpenFileGDB
~~~~~~~~~~~~~~~~~~~~

FileGDB 포맷은 한 가지 확장 사양과 함께 멀티패치 객체도 지원합니다. 이 확장 사양은 삼각형 여러 개로 이루어져 있지만 그 구조가 TriangleStrip 또는 TriangleFan이 아닌 새로운 유형의 부분(part)입니다. 두 드라이버 모두 읽기 쪽에서 ShapeFile 드라이버처럼 작동하도록 업그레이드했습니다. 쓰기 쪽에서는, 레이어의 도형 유형이 TIN 또는 PolyhedralSurface인 경우 FileGDB 드라이버가 자동적으로 멀티패치를 작성할 것입니다. CREATE_MULTIPATCH=YES 레이어 옵션 이전에 존재했던 레이어 옵션을 여전히 사용해서 멀티패치로 강제 작성할 수 있습니다.

GML
~~~

GML 드라이버의 입력 및 산출에 대해, Triangle, PolyhedralSurface 및 TriangulatedSurface 유형을 GML 문서로부터 읽어오거나 GML 문서에 작성할 수 있도록 수정했습니다. 샘플 예시에 다음과 같은 내용이 포함되어 있습니다:

::

   'TRIANGLE ((0 0,0 1,0 1,0 0))' 을 다음과 같이 파싱합니다:
   '<gml:Triangle>
       <gml:exterior>
           <gml:LinearRing>
               <gml:posList>0 0 0 1 0 1 0 0</gml:posList>
           </gml:LinearRing>
       </gml:exterior>
   </gml:Triangle>'

   <gml:PolyhedralSurface>
      <gml:polygonPatches>
          <gml:PolygonPatch>
              <gml:exterior>
                  <gml:LinearRing>
                      <gml:posList srsDimension="3">1 2 3 4 5 6 7 8 9 1 2 3</gml:posList>
                  </gml:LinearRing>
              </gml:exterior>
          </gml:PolygonPatch>
          <gml:PolygonPatch>
              <gml:exterior>
                  <gml:LinearRing>
                      <gml:posList srsDimension="3">10 11 12 13 14 15 16 17 18 10 11 12</gml:posList>
                  </gml:LinearRing>
              </gml:exterior>
              <gml:interior>
                  <gml:LinearRing>
                      <gml:posList srsDimension="3">19 20 21 22 23 24 25 26 27 19 20 21</gml:posList>
                  </gml:LinearRing>
              </gml:interior>
          </gml:PolygonPatch>
      </gml:polygonPatches>
   </gml:PolyhedralSurface>"""

   는 'POLYHEDRALSURFACE Z (((1 2 3,4 5 6,7 8 9,1 2 3)),((10 11 12,13 14 15,16 17 18,10 11 12),(19 20 21,22 23 24,25 26 27,19 20 21)))'로 파싱됩니다.

   PolygonPatch/Patch는 각각 PolyhedralSurface에 있는 Polygon 하나에 대응합니다.

   마지막으로, 'POLYHEDRALSURFACE EMPTY'를 다음과 같이 파싱합니다:
   '<gml:PolyhedralSurface>
       <gml:polygonPatches>
       </gml:polygonPatches>
   </gml:PolyhedralSurface>'

쓰기 쪽에서는 GML 3 산출물에 대해서만 이 도형들을 생성한다는 사실을 기억하십시오.

DXF
~~~

DXF 드라이버의 변경 사항 가운데 하나는 (PolyLine의 하위 유형인) PolyFaceMesh를 PolyhedralSurface로 변환하는 것입니다. GDAL의 `#6246 티켓 <https://trac.osgeo.org/gdal/ticket/6246>`_ 의 버그가 이를 설명하고 있습니다. PolyFaceMesh는 초기에 특정 코드를 사용해서 정의한 포인트들로 이루어지며, 이후 이 포인트들을 폴리곤의 부분으로 서술합니다. (폴리곤 하나가 최대 4개의 포인트를 가질 수 있습니다.) 현재 OGR이 PolyFaceMesh 읽기를 지원하지만, 이제 (저자가 현재 변경 사항 모음에서 구현하지는 않았지만) 쓰기 지원도 가능할 것입니다.

GeoPackage
~~~~~~~~~~

지오패키지 핵심 사양은 [Multi]Point, [Multi]LineString, [Multi]Polygon 및 GeometryCollection을 지원합니다. 곡선 도형도 등록된 확장 사양으로 언급되어 있지만, Triangle, PolyhedralSurface 또는 TIN은 전혀 언급이 없습니다. 하지만 지오패키지의 도형 블랍(blob) 포맷이 ISO WKB를 기반으로 하기 때문에 새로운 도형 유형 지원을 위해 실제로 새로운 코드를 작성해야 할 필요는 없습니다. 따라서 새로운 도형 유형 3개의 읽기/쓰기라는 가능성은 유지하지만, 쓰기 쪽에서는 비표준 확장 사양을 사용할 것이라는 경고를 발할 것입니다.

기타 드라이버
~~~~~~~~~~~~~

CSV, VRT, PGDump, SQLite 드라이버가 새 도형 유형들을 지원합니다. (그러나 SpatiaLite 드라이버는 지원하지 않습니다.) 새 도형 유형들을 지정하는 경우 쓰기 쪽에서 충돌을 일으키지 않도록 드라이버 몇 개를 수정했습니다. 앞에서 언급한 드라이버 이외에도, 충돌을 일으키지 않는다고 검증된 (그러나 오류가 발생하거나 인식하지 못 하는 도형을 건너뛸 수도 있는) 드라이버들은 다음과 같습니다:

   -  MySQL
   -  OCI
   -  KML
   -  LIBKML
   -  GeoJSON
   -  MapInfo

문서화
------

표준 독시젠(Doxygen) 문서화 과정을 사용합니다.

호환성
------

많은 응용 프로그램이 일부 드라이버가 이제 반환할 수도 있는 새 도형 유형들을 제대로 처리할 수 없을 것입니다. GDAL 2.1버전에서, 향후 GDAL이 반환할 수도 있는 새로운 유형들을 언급하며 도입했습니다. 코드는 새 도형을 건너뛰든지, 제대로 처리하든지, 또는 코드가 지원하는 도형 유형으로 변환하기 위해 OGR_G_ForceTo() 함수를 사용해야 합니다.

테스트
------

변경 사항이 얼마 되지 않기 때문에 기존 자동 테스트 스위트를 계속 통과합니다. :file:`ogr_geom.py` 및 :file:`ogr_gml_geom.py` 에 새로운 도형 클래스와 변환 메소드를 추가했습니다. 업데이트된 드라이버들도 새로운 테스트를 받았습니다.

구현
----

GSoC(Google Summer of Code) 2016 프로그램에서 아비야브 쿠마르 싱이 구현했으며, 이벤 루올이 미세 조정, 확장 및 통합했습니다.

제안한 구현은 "gsoc-triangle-ps-tin-rebased" 브랜치 `"gsoc-triangle-ps-tin-rebased" 브랜치 <https://github.com/rouault/gdal2/tree/gsoc-triangle-ps-tin-rebased>`_ 저장소에 있습니다.

투표 이력
---------

-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  하워드 버틀러 +1
-  이벤 루올 +1

