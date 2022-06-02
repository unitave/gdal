.. _rfc-49:

=======================================================================================
RFC 49: 만곡 도형
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

현재 GDAL 1.x버전의 도형 모델은 포인트, 라인, 폴리곤과 그 조합(멀티포인트, 멀티라인, 멀티폴리곤 및 도형 집합)을 사용합니다. 이 모델은 "오픈GIS 단순 피처 접근 1부: 공통 아키텍처"(1.1.0버전)의 도형 클래스 계층으로부터 나왔습니다.

이 RFC는 `ISO/IEC 13249 Part 3 Spatial (약칭 ISO SQL/MM Part 3) <https://www.iso.org/standard/60343.html>`_ 에 추가된 새 도형 유형을 추가할 것을 제안합니다:

-  원호 스트링(circular string):
   원호의 첫 번째 포인트, 중간(intermediate) 포인트 그리고 마지막 포인트라는 3개의 포인트로 설명되는 원호(circular arc) 또는 연결된 원호의 순열(sequence)

-  복합 곡선(compound curve):
   연결된 곡선의 순열, 라인스트링 또는 원호 스트링 가운데 하나

-  만곡 폴리곤(curve polygon):
   1개의 외곽 고리와 0개 이상의 내곽 고리로 이루어진 폴리곤. 각 고리는 라인스트링, 원호 스트링, 복합 곡선이라는 곡선 구현 가운데 하나일 수 있습니다.

-  다중 곡선(multicurve):
   곡선 집합 (라인스트링, 원호 스트링, 복합 곡선)

-  다중 면(multisurface):
   면 집합 (폴리곤, 만곡 폴리곤)

이 RFC의 범위는 다음으로 이루어져 있습니다:

-  기존 도형 클래스 계층에 새 도형 클래스들을 각각 대응하는 WKT(Well Known Text) 및 WKB(Well Known Binary) 인코딩으로 가져오기 기능(importer) 및 내보내기 기능(exporter)과 함께 추가하기

-  이 만곡 도형들과 각각의 근사치의 선형 도형들을 각각 변환/역변환할 수 있는 메소드를 추가하기

-  이런 도형들을 지원할 수 있는 몇몇 드라이버를 업그레이드하기:

   -  GML (그리고 비간접적으로 NAS, WFS)
   -  PostGIS/PGDump
   -  GeoPackage
   -  SQLite
   -  CSV
   -  VRT

참조 문서
---------

이 RFC의 구현을 위해 다음 문서들을 사용했습니다:

-  `2004년 5월 9일 작성된 ISO/IEC 13249 Part 3 Spatial(약칭 ISO SQL/MM Part 3)의 예전 초안 <http://jtc1sc32.org/doc/N1101-1150/32N1107-WD13249-3--spatial.pdf>`_:
   137페이지부터 있는 WKB 코드가 최신 코드가 아니므로 주의하십시오. 단순 피처 접근(Simple Feature Access) 1.2.1버전을 참조하십시오.

-  `오픈GIS 단순 피처 접근 1부: 공통 아키텍처 1.2.1버전, 약칭 SFA 1.2.1 <https://portal.ogc.org/files/?artifact_id=25355>`_

-  `WKT 인코딩의 BNF(Backus–Naur form) <https://github.com/postgis/postgis/blob/svn-trunk/doc/bnf-wkt.txt>`_:
   SQL/MM Part 3로부터 추출

-  `WKB 인코딩의 BNF(Backus–Naur form) <https://github.com/postgis/postgis/blob/svn-trunk/doc/bnf-wkb.txt>`_:
   SQL/MM Part 3로부터 추출

핵심 변경 사항
--------------

새 클래스 계층
~~~~~~~~~~~~~~

새 클래스 계층은 다음과 같으며 대부분 SQL/MM Part 3와 일치합니다.

.. image:: ../../../images/rfc49/classOGRGeometry.png

유일한 예외는 다음과 같습니다:

-  OGRLinearRing:
   GDAL 1.x버전에 존재하는 이 클래스는 하위 호환성 때문에 그리고 SQL/MM Part 3에서는 빠졌지만 SFA 1.2.1버전에는 아직 존재하기 때문에 유지되었습니다.

-  OGRSimpleCurve:
   이 추상 클래스는 :cpp:class:`OGRLineString` 에만 있던 코드를 공유해서 :cpp:class:`OGRCircularString` 의 구현을 단순화하는 OGR의 구현 세부 정보입니다.

도형 유형
~~~~~~~~~

OGRwkbGeometryType 열거형(enumeration)을 다음 값들로 확장했습니다:

::

       wkbCircularString = 8,  /**< 끝과 끝이 연결된 하나 이상의 원호 선분들,
                                *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbCompoundCurve = 9,   /**< 인접 곡선들의 순열, ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbCurvePolygon = 10,   /**< 평면, 곡선인 외곽 경계선과 0개 이상의 내곽 경계선으로 정의,
                                *    ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbMultiCurve = 11,     /**< 곡선의 도형 집합(GeometryCollection of Curves),
                                *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbMultiSurface = 12,   /**< 면의 도형집합, ISO SQL/MM Part 3. GDAL 2.0버전 이상 */

       wkbCircularStringZ = 1008,  /**< Z 구성 요소를 가진 wkbCircularString,
                                    *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbCompoundCurveZ = 1009,   /**< Z 구성 요소를 가진 wkbCompoundCurve,
                                    *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbCurvePolygonZ = 1010,    /**< Z 구성 요소를 가진 wkbCurvePolygon,
                                    *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbMultiCurveZ = 1011,      /**< Z 구성 요소를 가진 wkbMultiCurve,
                                    *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */
       wkbMultiSurfaceZ = 1012,    /**< Z 구성 요소를 가진 wkbMultiSurface,
                                    *   ISO SQL/MM Part 3. GDAL 2.0버전 이상 */

코드는 SFA 1.2.1버전에서 가져왔고, PostGIS 2버전 구현과 일치합니다. ISO SQL/MM Part 3이 wkbCircularString에 대해 대안 값을 (8 또는 1000001) 허용한다는 사실을 기억하십시오. 앞에서 언급한 초안에 있는 표 15를 참조하십시오. 10000XX 범위에 있는 값들은 아마도 더 예전의 초안으로부터 나온 값일 것입니다. OGR은 이 값들을 가져오지만, WKB로 내보낼 때에는 SFA 1.2.1버전의 값들을 사용할 것입니다.

ISO SQL/MM Part 3 / SFA 1.2.1의 WKB 코드를 준수하기 위해 기존 2.5차원 도형(wkbPoint25D 등등)의 열거형 값들을 수정할 가치가 있는지 고려해봤지만, OGR API의 기존 사용자들에 대한 영향이라는 측면에서 그렇게 할 만한 분명한 장점이 없었습니다.

주의: Z 차원을 표현하는 서로 다른 방법들("예전" 도형 유형의 경우 wkb25DBit 비트, 그리고 "새로운" 도형 유형의 경우 +1000)을 혼합하는 것은 도형을 WKB로 내보내는 데 직접적으로 아무런 영향을 미치지 않습니다. OGRwkbGeometryType의 값과 WKB 도형으로 전송되는 값 사이에는 직접적인 관련이 없습니다. :cpp:class:`OGRGeometry` 의 exportToWkb() 메소드는 원하는 WKB 변이형을 선택하기 위해 'wkbVariant' 파라미터를 입력받습니다.

도형 유형이 3차원인지 테스트하기 위해 가끔 사용되었던 wkb25DBit 값(0x8000000)은 새 도형 유형과 작동하지 않을 것이기 때문에 이제 분명하게 퇴출되었습니다. 각각 도형 유형이 3차원인지 테스트하기 위해 그리고 도형 유형을 3차원으로 수정하기 위해 wkbHasZ() 및 wkbSetZ() 메소드를 추가했습니다. wkb25DBit 상수는 이제 GDAL의 모든 코드에서 비활성화되었습니다. (그러나 사용자 코드로는 아직 접근할 수 있습니다.) 모든 드라이버도 새 매크로를 사용하도록 변환했습니다.

도형 유형들에 대해 작업하는 데 새로운 함수 계열을 사용합니다:

::

   OGRwkbGeometryType CPL_DLL OGR_GT_Flatten( OGRwkbGeometryType eType );
       --> 전송된 도형 유형에 대응하는 2차원 도형 유형을 반환합니다.

   OGRwkbGeometryType CPL_DLL OGR_GT_SetZ( OGRwkbGeometryType eType );
       --> 전송된 도형 유형에 대응하는 3차원 도형 유형을 반환합니다.

   OGRwkbGeometryType CPL_DLL OGR_GT_SetModifier( OGRwkbGeometryType eType, int bSetZ, int bSetM );
       --> 파라미터에 따라 2차원 또는 3차원 도형 유형을 반환합니다.

   int                CPL_DLL OGR_GT_HasZ( OGRwkbGeometryType eType );
       --> 도형 유형이 3차원 도형 유형인지 여부를 반환합니다.

   int                CPL_DLL OGR_GT_IsSubClassOf( OGRwkbGeometryType eType,
                                                   OGRwkbGeometryType eSuperType );
       --> 도형 유형이 또다른 도형 유형의 하위 클래스인지 여부를 반환합니다.

   int                CPL_DLL OGR_GT_IsCurve( OGRwkbGeometryType );
       -->  도형 유형이 곡선의 인스턴스인지 여부를 반환합니다.
            (예: wkbLineString, wkbCircularString 또는 wkbCompoundCurve)

   int                CPL_DLL OGR_GT_IsSurface( OGRwkbGeometryType );
       -->  도형 유형이 면의 인스턴스인지 여부를 반환합니다.
            (예: wkbPolygon 또는 wkbCurvePolygon)

   int                CPL_DLL OGR_GT_IsNonLinear( OGRwkbGeometryType );
       --> 도형 유형이 비선형 도형 유형인지 여부를 반환합니다.
           이런 도형 유형에는 wkbCircularString, wkbCompoundCurve, wkbCurvePolygon,
           wkbMultiCurve, wkbMultiSurface 및 각각의 3차원 변이형들이 있습니다.

   OGRwkbGeometryType CPL_DLL OGR_GT_GetCollection( OGRwkbGeometryType eType );
       -->  전송된 도형 유형을 담을 수 있는 집합 유형을 반환합니다.

   OGRwkbGeometryType CPL_DLL OGR_GT_GetCurve( OGRwkbGeometryType eType );
       --> 전송된 도형 유형을 담을 수 있는 만곡 도형 유형을 반환합니다.
           다음 변환을 처리할 수 있습니다: wkbPolygon -> wkbCurvePolygon,
           wkbLineString->wkbCompoundCurve, wkbMultiPolygon->wkbMultiSurface
           그리고 wkbMultiLineString->wkbMultiCurve.

   OGRwkbGeometryType CPL_DLL OGR_GT_GetLinear( OGRwkbGeometryType eType );
       --> 전송된 도형 유형을 담을 수 있는 비만곡 도형 유형을 반환합니다.
           다음 변환을 처리할 수 있습니다: wkbCurvePolygon -> wkbPolygon,
           wkbCircularString->wkbLineString, wkbCompoundCurve->wkbLineString,
           wkbMultiSurface->wkbMultiPolygon 그리고 wkbMultiCurve->wkbMultiLineString.

이제 기존 wkbFlatten()은 OGR_GT_Flatten()의 별명이고, 새 wkbHasZ()는 OGR_GT_HasZ()의 별명이며, wkbSetZ()는 OGR_GT_SetZ()의 별명입니다.

새 메소드
~~~~~~~~~

-  :cpp:class:`OGRGeometry` 클래스:

::


       virtual OGRBoolean hasCurveGeometry(int bLookForNonLinear = FALSE) const;

   /**
    * \brief 이 도형이 만곡 도형인지 또는 만곡 도형을 가지고 있는지를 반환합니다.
    *
    * 도형이 CIRCULARSTRING, COMPOUNDCURVE, CURVEPOLYGON, MULTICURVE 또는
    * MULTISURFACE인지, 가지고 있는지 또는 가지고 있을 수도 있는지를 반환합니다.
    *
    * bLookForNonLinear를 TRUE로 설정한 경우, 도형 또는 그 하위 도형이 비선형
    * 도형인지 또는 담고 있는지를 실제로 살펴볼 것입니다. 이 메소드가 TRUE를
    * 반환하는 경우 getLinearGeometry()가 이 도형의 근사치 버전을 반환할 것입니다.
    * 그렇지 않다면 getLinearGeometry()가 변환을 수행하지만 "비손실" 변환하도록
    * COMPOUNDCURVE -> LINESTRING, MULTICURVE -> MULTILINESTRING 또는
    * MULTISURFACE -> MULTIPOLYGON 처럼 컨테이너 유형만 변환할 것입니다.
    */

       virtual OGRGeometry* getCurveGeometry(const char* const* papszOptions = NULL) const;

   /**
    * \brief 이 도형의 만곡 버전을 반환합니다.
    *
    * 만곡 도형의 역근사치를 계산해서 CIRCULARSTRING, COMPOUNDCURVE,
    * CURVEPOLYGON, MULTICURVE 또는 MULTISURFACE를 담고 있을 수도 있는 도형을
    * 반환합니다.
    *
    * 도형에 만곡 부분이 없는 경우, 입력 도형의 복사본을 반환합니다.
    *
    * 호출자가 반환 도형을 소유합니다.
    *
    * 이 메소드의 역은 OGRGeometry::getLinearGeometry()입니다.
    *
    * 이 함수는 C 함수 OGR_G_GetCurveGeometry()와 동일합니다.
    *
    * @param papszOptions NULL로 종료되는 문자열 목록 옵션입니다.
    *                     현재 사용하지 않습니다. NULL로 설정해야만 합니다.
    */

       virtual OGRGeometry* getLinearGeometry(double dfMaxAngleStepSizeDegrees = 0,
                                                const char* const* papszOptions = NULL) const;


   /**
    * \brief 이 도형의 -- 근사치 버전일 수도 있는 -- 비만곡 버전을 반환합니다.
    *
    * 만곡 도형의 근사치를 계산해서 어떤 CIRCULARSTRING, COMPOUNDCURVE,
    * CURVEPOLYGON, MULTICURVE 또는 MULTISURFACE도 담고 있지 않은 도형을
    * 반환합니다.
    *
    * 호출자가 반환 도형을 소유합니다.
    *
    * 이 메소드의 역은 OGRGeometry::getCurveGeometry()입니다.
    *
    * 이 함수는 C 함수 OGR_G_GetLinearGeometry()와 동일합니다.
    *
    * @param dfMaxAngleStepSizeDegrees 원호를 따라 도 단위로 가장 큰 단계,
    *                                  기본 설정을 사용하려면 0으로 설정하십시오.
    * @param papszOptions NULL로 종료되는 문자열 목록 옵션입니다.
    *                     무결한 옵션에 대해서는 OGRGeometryFactory::curveToLineString()을
    *                     참조하십시오.
    */

-  :cpp:class:`OGRGeometryFactory` 클래스:

::


   static OGRLineString* curveToLineString(
                                               double x0, double y0, double z0,
                                               double x1, double y1, double z1,
                                               double x2, double y2, double z2,
                                               int bHasZ,
                                               double dfMaxAngleStepSizeDegrees,
                                               const char*const* papszOptions )
   /**
    * \brief 원호로 이루어진 원을 근사치 라인스트링으로 변환합니다.
    *
    * 원호로 이루어진 원은 첫 번째 포인트, 중간(intermediate) 포인트 그리고
    * 마지막 포인트라는 3개의 포인트로 정의됩니다.
    *
    * 제공된 dfMaxAngleStepSizeDegrees가 힌트입니다. 이산화(discretization)
    * 알고리즘은 약간 다른 값을 선택할 수도 있습니다.
    *
    * 공통 원호를 공유하는 만곡 폴리곤을 렌더링할 때 틈(gap)을 방지하기 위해
    * 반전된 첫 번째 및 마지막 포인트와 동일한 중간 포인트로 호출하는 경우
    * 이 메소드가 반전된 꼭짓점을 가진 라인을 반환하도록 보장합니다.
    *
    * @param x0 첫 번째 포인트의 x
    * @param y0 첫 번째 포인트의 y
    * @param z0 첫 번째 포인트의 z
    * @param x1 중간 포인트의 x
    * @param y1 중간 포인트의 y
    * @param z1 중간 포인트의 z
    * @param x2 마지막 포인트의 x
    * @param y2 마지막 포인트의 y
    * @param z2 마지막 포인트의 z
    * @param bHasZ Z를 연산에 넣어야만 하는 경우 TRUE
    * @param dfMaxAngleStepSizeDegrees 원호를 따라 도 단위로 가장 큰 단계,
    *                                  기본 설정을 사용하려면 0으로 설정하십시오.
    * @param papszOptions NULL로 종료되는 문자열 목록 옵션입니다.
    * 인식하는 옵션:
    * <ul>
    * <li>ADD_INTERMEDIATE_POINT=STEALTH/YES/NO: (기본값은 STEALTH)
    *         중간 포인트를 라인스트링으로 산출해야만 하는지 그리고 어떻게
    *         산출해야만 하는지 결정합니다.
    *         STEALTH로 설정하는 경우, 어떤 명확한 중간 포인트도 추가하지
    *         않지만 OGRGeometryFactory::curveFromLineString()이 그 속성을
    *         디코딩할 수 있도록 속성을 중간 포인트의 하위 비트(low significant bit)로
    *         인코딩합니다. 이는 OGR에서 차선책(roundtrip)에 대한 최상의 절충안이며
    *         PostGIS <a href="http://postgis.org/docs/ST_LineToCurve.html">ST_LineToCurve()</a>
    *         와 더 나은 결과를 보입니다.
    *         YES로 설정하는 경우, 라인스트링에 중간 포인트를 명확하게 추가합니다.
    *         NO로 설정하는 경우, 라인스트링에 중간 포인트를 추가하지 않습니다.
    * </li>
    * </ul>
    */

   --> OGRCircularString::getLinearGeometry()가 이 메소드를 사용합니다.

   OGRCurve* OGRGeometryFactory::curveFromLineString(const OGRLineString* poLS,
                                                     CPL_UNUSED const char*const* papszOptions)

   /**
    * \brief 곡선과 근사치인 라인스트링을 곡선으로 변환하려 시도합니다.
    *
    * 이 메소드는 COMPOUNDCURVE, CIRCULARSTRING 또는 LINESTRING을 반환할 수 있습니다.
    *
    * 이 메소드는 curveToLineString()의 역입니다.
    *
    * @param poLS 변환할 도형을 가리키는 핸들입니다.
    * @param papszOptions NULL로 종료되는 문자열 목록 옵션입니다.
    *                     현재 사용하지 않습니다. NULL로 설정해야만 합니다.
    */

   --> OGRLineString::getCurveGeometry()가 이 메소드를 사용합니다.


   OGRGeometry* OGRGeometryFactory::forceTo( OGRGeometry* poGeom,
                                             OGRwkbGeometryType eTargetType,
                                             const char*const* papszOptions )
    *
    * 입력 도형을 지정한 도형 유형으로 강제 변환하려 시도합니다.
    *
    * '단일' 도형 유형을 대응하는 집합 유형(OGR_GT_GetCollection() 참조)으로
    * 승격시키거나 그 반대로 변환할 수 있습니다. 비선형 도형이 담고 있을 수도
    * 있는 원호의 근사치를 계산해서 비선형 도형 유형을 대응하는
    * 선형 도형 유형(OGR_GT_GetLinear() 참조)으로 변환할 수 있습니다.
    * 선형 도형 유형으로부터 만곡 도형 유형으로 변환하는 것과 관련해서,
    * 오직 "래핑(wrapping)"만 수행할 것입니다. 역근사치를 계산해서 다듬기를
    * 통해 잠재적인 원호를 가져오려 시도하지 않습니다. 그런 목적이라면
    * OGRGeometry::getCurveGeometry()를 사용하면 됩니다.
    *
    * 입력 도형을 소비해서 새 도형을 반환합니다. (또는 동일한 도형일 가능성도 있습니다.)
    *
    * @param poGeom 입력 도형 - 소유권이 메소드로 이전됩니다.
    * @param eTargetType 대상 산출 도형 유형입니다.
    * @param papszOptions NULL로 종료되는 문자열 목록 옵션 또는 NULL입니다.
    * @return 새 도형을 반환합니다.
    */

   --> 이 메소드는 새 도형 유형들을 처리할 수 잇도록 기존 forceToPolygon(), forceToLineString(), forceToMultiPolygon(), forceToMultiLineString()을 확장해서 일반화한 것입니다. forceTo()는 요청받은 변환을 위해 사용할 수 있는 경우 기존 메소드를 실제로 호출하고, 선형 및 비선형 도형 유형들 간의 변환도 처리합니다.

기존 OGRGeometry 메소드 구현
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

현재 `GEOS <https://libgeos.org/>`_ 가 만곡 도형을 지원하지 않기 때문에, Intersects()처럼 불(boolean) 값을 반환하는 작업이나 Intersection()처럼 새 도형을 반환하는 작업과 같은 모든 GEOS 관련 작업들이 비선형 도형을 먼저 대응하는 선형 근사치로 변환하도록 수정했습니다. (향후 GEOS가 만곡 도형을 지원하게 되면 다시 수정해야 할 수도 있습니다.) GEOS가 도형을 반환하는데 입력 파라미터 가운데 하나가 비선형 도형인 경우, 만곡 도형을 가능한 한 많이 가져오려 시도하는 역작업을 수행합니다. 물론 일반적으로 결과물이 완벽하지는 않지만, 없는 것보다는 낫습니다.

다음은 인접한 2개의 반원을 통합(union)하는 간단한 예시입니다:

::

       g1 = ogr.CreateGeometryFromWkt('CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING (0 0,1 1,2 0),(2 0,0 0)))')
       g2 = ogr.CreateGeometryFromWkt('CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING (0 0,1 -1,2 0),(2 0,0 0)))')
       g3 = g1.Union(g2)
       assert g3.ExportToWkt() == 'CURVEPOLYGON (CIRCULARSTRING (0 0,1 1,2 0,1 -1,0 0))'

또는 버퍼 작업의 결과물에 대해 명확하게 GetCurveGeometry()를 사용하는 예시입니다:

::

       g1 = ogr.CreateGeometryFromWkt('POINT(1 2)')
       g2 = g1.Buffer(0.5)
       g3 = g2.GetCurveGeometry()
       assert g3.ExportToWkt() != 'CURVEPOLYGON (CIRCULARSTRING (1.5 2.0,0.5 2.0,1.5 2.0))'

:cpp:class:`OGRCircularString` (그리고 따라서 :cpp:class:`OGRCompoundCurve`)에 대한 Length() 작업은 선형 근사치 계산으로 돌아가지 않고 원 도형을 사용해서 정확한 길이를 계산합니다. :cpp:class:`OGRCurvePolygon` 에 대한 Area() 작업은 일반적으로 선형 근사치 계산을 수행해야 할 것입니다. 완전한 원 또는 볼록한 만곡 폴리곤에 대해 작업하는 경우 이를 피하기 위해 최적화를 수행합니다. (설명의 원호 부분을 포함하는 모든 꼭짓점으로 형성된 꼭짓점의 면적을 계산하고 거기에 `원호 선분 <https://ko.wikipedia.org/wiki/%ED%99%9C%EA%BC%B4>`_ 의 면적을 더합니다.)

C API 변경 사항
~~~~~~~~~~~~~~~

설명:

-  wkb25DBit가 여전히 존재하지만, 새 도형 유형과 호환되지 않기 때문에 퇴출되었습니다. wkbFlatten(), wkbHasZ(), wkbSetZ() 매크로를 대신 사용하십시오.

추가 사항:

-  OGR_GT_xxxx (도형 유형 용): 앞에서 설명했습니다.

-  OGRErr OGR_G_ExportToIsoWkb( OGRGeometryH, OGRwkbByteOrder, unsigned char*):
   도형을 ISO SQL/MM Part 3를 준수하는 WKB로 내보냅니다.

-  OGRErr OGR_G_ExportToIsoWkt( OGRGeometryH, char \*\* ):
   도형을 ISO SQL/MM Part 3를 준수하는 WKT로 내보냅니다. 예를 들어 2.5차원 도형의 이름 뒤에 "POINT Z (1 2 3)"와 같이 " Z" 접미어를 붙입니다.

-  OGRGeometryH OGR_G_Value( OGRGeometryH, double dfDistance ):
   기존 :cpp:func:`OGRGeometry::Value` 의 매핑입니다.

-  int OGR_G_HasCurveGeometry( OGRGeometryH, int bLookForNonLinear ) :
   :cpp:func:`OGRGeometry::hasCurveGeometry` 의 매핑입니다.

-  OGRGeometryH OGR_G_GetLinearGeometry( OGRGeometryH hGeom, double dfMaxAngleStepSizeDegrees, char*\* papszOptions):
   :cpp:func:`OGRGeometry::hasCurveGeometry` 의 매핑입니다.

-  OGRGeometryH OGR_G_GetCurveGeometry( OGRGeometryH hGeom, char*\* papszOptions ):
   :cpp:func:`OGRGeometry::hasCurveGeometry` 의 매핑입니다.

-  void OGRSetNonLinearGeometriesEnabledFlag(int bFlag):
   하위 호환성 단락에서 논의합니다.

-  int OGRGetNonLinearGeometriesEnabledFlag():
   하위 호환성 단락에서 논의합니다.

드라이버 변경 사항
------------------

-  GML 도형 가져오기 기능(importer):
   Arc, ArcString, ArcByBulge, ArcByCenterPoint, Circle 및 CircleByCenterPoints GML 요소들을 원호 스트링 OGR 도형들로 반환할 것입니다. 이 GML 요소들이 CurveComposite, MultiCurve, Surface 같은 다른 GML 요소에 포함되어 있는 경우 그에 대응하는 비선형 OGR 도형들도 반환할 것입니다. Surface, MultiSurface, Curve, MultiCurve로 만들어진 또는 구성된 도형을 읽어오는 경우 가능한 한 선형 유형 OGR 도형 클래스를 반환하려 노력합니다. 예를 들면 도형 안에 원호 스트링이 있는 경우에만 :cpp:class:`OGRCurvePolygon`, :cpp:class:`OGRCompoundCurve` 등등을 반환할 것입니다.

-  GML 도형 내보내기 기능(xporter):
   원호 스트링을 가진 도형을 전송하는 경우 ArcString 및 Circle GML 요소를 생성할 수 있습니다.

-  GML 드라이버:
   모든 새 도형 유형을 읽고 쓸 수 있습니다. GML3 응용 프로그램 스키마를 읽어올 때, CurvePropertyType, SurfacePropertyType, MultiCurvePropertyType 또는 MultiSurfacePropertyType 같은 도형 필드 선언도 잠재적인 비선형 도형으로 해석하고 대응하는 OGR 도형 유형을 레이어 도형 유형으로 사용하기 때문에 피처의 도형도 해당 레이어 도형 유형을 따를 것입니다. WFS 드라이버에 영향을 미칠 수 있습니다.

-  NAS 드라이버:
   새 도형 유형들을 반환할 수 있습니다. NAS 파일이 원호를 담고 있는 경우에만 NAS 레이어에 새 도형 유형을 사용할 것입니다.

-  PG/PostGIS 드라이버:
   PostGIS 2.x 및 PostGIS 1.x 버전 둘 다 모든 새 도형 유형들을 읽고 쓸 수 있습니다. PostGIS 1.x 버전의 호환성을 위해 importFromWkb()/exportToWkb()가 PostGIS 1.x 버전이 만곡 폴리곤, 다중 곡선 및 다중 면에 사용하는 비표준 코드들을 처리할 수 있도록 특수 처리 과정을 수행해야만 합니다. 이를 위해 이 메소드들이 사용하는 OGRwkbVariant 열거형에 wkbVariantPostGIS1 값을 추가했습니다.

-  PGDump 드라이버:
   모든 새 도형 유형들을 쓸 수 있습니다. 앞에서 버전 사이의 차이점에 관련한 내용 때문에 POSTGIS_VERSION 데이터셋 생성 옵션을 정확하게 지정하는 것이 중요합니다.

-  GeoPackage:
   모든 새 도형 유형들을 읽고 쓸 수 있습니다.
   주의: 지오패키지 사양의 핵심은 아니지만, 그래도 등록된 확장 사양입니다.

-  SQLite 드라이버:
   SpatiaLite 데이터베이스가 '아닌' 데이터베이스에 모든 새 도형 유형들을 읽고 쓸 수 있습니다. SpatiaLite가 만곡 도형 유형을 지원하지 않기 때문입니다. 하지만 SQLite SQL 방언을 계속 사용할 수 있도록 시도(해킹)했습니다. 기본적으로 OGR 도형을 SpatiaLite로 변환할 때 OGR 도형이 만곡 도형 유형 가운데 하나인 경우, 산출되는 블랍(blob)이 처음에는 선형 도형의 SpatiaLite 호환 블랍을 담고 있다가 나중에는 만곡 도형의 WKB를 담고 있을 것입니다. SpatiaLite 함수는 -- 예를 들어 ``ST_*`` 함수로 호출하는 경우 -- 후자를 무시할 것입니다. SQLite로부터 블랍을 읽어올 때 추가된 만곡 도형 WKB가 블랍에 여전히 존재하는 경우 만곡 도형 WKB를 사용할 것입니다. 존재하지 않는다면 SpatiaLite 도형 블랍을 사용할 것입니다. 따라서 도형 열에 대해 아무 작업도 하지 않고 도형 열을 선택하기만 하는 SELECT 문은 만곡 도형을 보전할 것입니다.

-  MEM 드라이버:
   모든 새 도형 유형을 읽고 쓸 수 있습니다.

-  CSV 드라이버:
   모든 새 도형 유형을 읽고 쓸 수 있습니다.

-  VRT 드라이버:
   모든 새 도형 유형과 호환된다고 선언합니다. 실제 케이퍼빌리티는 VRT가 감싸고(wrap) 있는 기저 레이어에 따라 달라집니다.

유틸리티 변경 사항
------------------

-  ogr2ogr:
   "-nlt" 옵션에서 새 도형 이름(CIRCULARSTRING 등등)을 지원합니다. 만곡 도형을 대응하는 선형 근사치 버전으로 변환할 것을 요청하는 데 "-nlt CONVERT_TO_LINEAR" 같은 옵션도 사용할 수 있습니다. (이를 수행하기 위해 ``forceTo(xxx, OGR_GT_GetLinear())`` 가 사용됩니다.)
   주의: 모든 드라이버가 하위 호환성 단락에서 설명하는 호환성 메커니즘으로 비선형 도형 유형을 처리할 수 있어야 하기 때문에 이 유틸리티가 반드시 필요하지는 않습니다. 그러나 소스가 비선형 도형을 담고 있는 경우에도 선형 도형 유형으로 PostGIS 테이블 또는 GeoPackage 데이터베이스를 생성하는 데 유용할 수도 있습니다.
   "-nlt CONVERT_TO_LINEAR"를 "-nlt PROMOTE_TO_MULTI"와 결합할 수 있습니다.

SWIG 바인딩 변경 사항
---------------------

다음을 추가합니다:

-  ogr.wkbXXXXX로서의 새 도형 유형들
-  ogr.ForceTo()
-  Geometry.ExportToIsoWkt()
-  Geometry.ExportToIsoWkb()
-  Geometry.HasCurveGeometry(int bLookForCircular = FALSE)
-  Geometry.GetLinearGeometry(double dfMaxAngleStepSizeDegrees = 0.0,char*\* options = NULL)
-  Geometry.GetCurveGeometry(char*\* options = NULL)
-  ogr.SetNonLinearGeometriesEnabledFlag(int bFlag)
-  ogr.GetNonLinearGeometriesEnabledFlag()
-  ogr.GT_xxxxx 함수들

ogr.wkb25DBit를 사용하면 퇴출 관련 경고를 발할 것입니다.

이 RFC에 포함되지 '않은' 관련 변경 사항
---------------------------------------

-  다면체 표면(Polyhedral Surface), TIN(Triangulated Irregular Network), Triangle 같은 다른 ISO SQL/MM 도형에 대한 지원

- 도형의 M(Measure) 차원에 대한 지원

-  만곡 도형을 사용할 수 있는 다른 드라이버들의 업그레이드:
   MSSQL Spatial, Oracle Spatial, DXF, DWG, ...

-  임의의 새 도형 유형 지원:
   개념적으로는, 예를 들어 :cpp:class:`OGRCurve` (베지어 곡선(Bezier Curve) 또는 스플라인 곡선(Spline Curve))를 확장하는 새 클래스를 OGR 코어를 건드리지 않은 채 추가할 수 있기를 바랄 수 있습니다. 하지만 현재 이는 불가능합니다. :cpp:class:`OGRGeometryFactory` 및 ``OGR_GT\_*`` 함수들을 변경하면 몇몇 하드코딩된 가정들을 제거해야 할 것이기 때문입니다.

하위 호환성
-----------

GDAL을 사용하는 코드 측면
~~~~~~~~~~~~~~~~~~~~~~~~~

많은 응용 프로그램들이 이제 몇몇 드라이버가 반환할 수도 있는 새 도형 유형을 제대로 처리할 수 없을 것입니다. 도형 유형을 테스트하거나 변환 함수를 명확하게 호출하기를 바라지 않는다면 응용 프로그램이 ``OGRSetNonLinearGeometriesEnabledFlag(FALSE)`` 를 호출하면 됩니다. (이 플래그의 기본값은 TRUE입니다. 이 경우 비선형 도형을 반환할 수 있게 됩니다.) FALSE로 호출한 경우 OGR_G_ForceTo()를 이용, 선형 근사치를 계산해서 만곡 도형 유형을 가장 가까운 선형 도형으로 변환할 것입니다.

이 플래그는 OGR_F_GetGeometryRef(), OGR_F_GetGeomFieldRef(), OGR_L_GetGeomType(), OGR_GFld_GetType() 및 OGR_FD_GetGeomType() C API 그리고 SWIG 바인딩에서 대응하는 메소드들에만 영향을 미칩니다.

라이브러리는 일반적으로 이 메소드를 사용해서는 '안 됩니다'. 다른 라이브러리 또는 응용 프로그램과 충돌할 수 있기 때문입니다.

이 메소드는 C++ API의 습성에 영향을 주지 '않는다'는 사실을 기억하십시오. 드라이버가 예를 들면 GetGeomType()을 호출할 수도 있기 때문에 드라이버를 혼동시킬 수 있으므로 C++ 수준에서 이를 시도하는 것은 위험하거나 복잡한 것으로 간주되었습니다.

OGR 드라이버 측면
~~~~~~~~~~~~~~~~~

새 도형 유형들을 처리할 수 있는 드라이버가 새로운 데이터셋 수준 ODsCCurveGeometries 케이퍼빌리티 그리고 레이어 수준 OLCCurveGeometries 케이퍼빌리티를 선언해야 합니다. 드라이버가 구현하는 CreateFeature() 및 SetFeature() 가상 메소드를 ICreateFeature() 및 ISetFeature()로 재명명했습니다.
:cpp:class:`OGRLayer` 는 이제 레이어가 만곡 도형을 지원할 수 있는지 확인하는 CreateFeature() 및 SetFeature() 비가상 메소드를 가집니다. 이들을 가지고 있지 않고, 전송된 피처가 비선형 도형을 가진 경우, 드라이버의 ICreateFeature()/ISetFeature() 메소드를 호출하기 전에 비선형 도형을 대응하는 선형 근사치 버전으로 투명하게 변환할 것입니다. 마찬가지로 데이터소스 수준의 CreateLayer() 메소드도 필요한 경우 전송된 도형 유형을 대응하는 비선형 유형으로 변환할 것입니다.

모든 인트리(in-tree) 드라이버에서 CreateFeature()를 ICreateFeature()로 그리고 SetFeature()를 ISetFeature()로 변환했습니다. 트리에 없는 드라이버들도 마찬가지로 수정해야 합니다. 그렇지 않으면 이 메소드들이 실패할 것입니다. (:cpp:class:`OGRLayer` 의 이제 가상이 아닌 메소드들은 동일한 클래스의 기본 구현을 생성하려 시도하지만 실패할 것입니다.)

문서화
------

새로운 메소드들과 OGR 도형 클래스들 모두 문서화합니다.
필요한 경우 드라이버 문서를 업데이트합니다.
:file:`MIGRATION_GUIDE.TXT` 를 이 RFC를 요약한 내용으로 업데이트합니다.

테스트
------

아주 적은 변경 사항만 적용했기 때문에 기존 자동 테스트 스위트는 계속 통과합니다.
:file:`ogr_geom.py` 및 :file:`ogr_gml_geom.py` 에 새 도형 클래스들과 변환 메소드들에 대한 매우 포괄적인 테스트를 추가했습니다. 업데이트된 드라이버들도 새로운 테스트를 받았습니다.

구현
----

이벤 루올이 이 RFC를 구현할 것입니다. Sourcepole과 협력하고 (`QGIS 개선 8: 도형 재설계 <https://github.com/mhugent/QGIS-Enhancement-Proposals/blob/master/QEP-8-geometry_redesign.rst>`_ 참조) 스위스 QGIS 사용자 그룹의 후원을 받았습니다.

제안한 구현은 `"curve_geometries" 브랜치 <https://github.com/rouault/gdal2/tree/curve_geometries>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/curve_geometries>`_

투표 이력
---------

-  세케레시 터마시 +1
-  유카 라흐코넨 +1
-  이벤 루올 +1

