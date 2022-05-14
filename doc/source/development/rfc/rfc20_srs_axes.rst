.. _rfc-20:

================================================================================
RFC 20: OGRSpatialReference 축 지원
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인

요약
----

:cpp:class:`OGRSpatialReference` 및 :cpp:class:`OGRCoordinateTransformation` 클래스는 모든 좌표계가 [편동, 편북] 좌표 순서를 (또는 지리 좌표계 용어로는 [경도, 위도] 순서를) 사용한다고 가정합니다. 실제로는 (크르조바크(Křovák) 투영법 같은) 몇몇 좌표계가 대체 축 방향(axis orientation)을 사용하며, 몇몇 (GML, WMS 1.3, WCS 1.1) 표준은 자신의 지리 좌표가 모두 [위도, 경도] 좌표 순서라는 EPSG 선언을 준수할 것을 요구합니다.

이 RFC는 :cpp:class:`OGRSpatialReference` 및 :cpp:class:`OGRCoordinateTransformation` 클래스가 대체 축 방향을 지원하도록 확장하고 선택된 (GML, WMS, WCS, GMLJP2) 드라이버들이 축 순서를 제대로 지원하도록 업데이트하려 합니다.

WKT 축 표현
-----------

다음 예시에서 (OGC 01-???을 따르는) OGC WKT 공간 좌표계 서식이 이미 좌표계 축을 정의하는 방법을 보여줍니다:

.. code-block:: wkt

   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           TOWGS84[0,0,0,0,0,0,0],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0,
           AUTHORITY["EPSG","8901"]],
       UNIT["degree",0.0174532925199433,
           AUTHORITY["EPSG","9108"]],
       AXIS["Lat",NORTH],
       AXIS["Long",EAST],
       AUTHORITY["EPSG","4326"]]

튜플(tuple) 안에서의 위치와 관련된 순서로 축 당 하나의 AXIS 정의가 있습니다. 첫 번째 인자는 축의 사용자 이름이며 정확한 값을 지정하지 않습니다. 두 번째 인자가 방향으로, NORTH, SOUTH, EAST 또는 WEST 가운데 하나로 지정할 수 있습니다.

딜레마
------

이 RFC의 핵심 도전 과제는 EPSG 좌표계를 광범위하게 사용하지만 축 방향을 무시하고 EPSG가 뭐라고 선언하든 상관없이 좌표를 경도, 위도 순서로 취급해야 한다고 가정하는 기존 파일 및 코드를 손상시키지 않고, 적절한 경우 지리 좌표계에 대해 올바른 EPSG 축 순서를 준수하도록 하는 것을 포함해서 축 순서 지원을 추가하는 것입니다.

특히 EPSG:4326 같은 지리 좌표계를 사용하는 파일을 경도/위도로 취급해야 하는 경우와 위도/경도로 취급할 경우를 판단하기 위한 적절한 정책 및 메커니즘을 제안해야 합니다. 광범위한 기존 관행 때문에, 기존 관행의 편에 서서 오류를 발생시키고 EPSG 축 순서를 준수할 것을 "동의"해야 할 필요가 있습니다.

꼼수
----

이런 딜레마를 피해 작동할 수 있도록 이 RFC가 제안하는 주요 메커니즘은 AXIS 값이 설정된 지리 좌표계와 설정되지 않은 지리 좌표계를 구분하는 것입니다. 특히, (4326 같은) EPSG 기관 코드가 설정되어 있지만 축이 선언되지 않은 WKT 좌표계를 EPSG:4326의 정의와는 상반되지만 경도, 위도 순서라고 가정할 것입니다. EPSG 축 순서를 준수해야 한다는 사실을 정말로 '알고 있는' 경우에만 축 선언을 실제 위도, 경도 순서로 채울 것입니다.

이런 꼼수를 통해, 특정 상황을 제외하면 EPSG 축 순서를 준수할 필요없이 EPSG:4326 정의를 계속 사용(오용)할 수 있게 해줄 것이라 희망합니다.

OGRSpatialReference
-------------------

새 열거형
~~~~~~~~~

.. code-block:: cpp

   typedef enum { 
     OAO_Unknown = 0,
     OAO_North = 1,
     OAO_South = 2,
     OAO_East = 3,
     OAO_West = 4
   } OGRAxisOrientation;

새 메소드
~~~~~~~~~

축 하나에 관한 정보를 가져옵니다('iAxis'는 0에서 시작합니다):

.. code-block:: cpp

   const char *GetAxis( const char *pszTargetKey, int iAxis, 
                        OGRAxisOrientation *peOrientation );

지정한 대상 키(PROJCS 또는 GEOGCS)에 대해 X 및 Y 축을 정의합니다:

.. code-block:: cpp

   OGRErr      SetAxes( const char *pszTargetKey, 
                        const char *pszXAxisName, OGRAxisOrientation eXAxisOrientation,
                        const char *pszYAxisName, OGRAxisOrientation eYAxisOrientation,
                        const char *pszZAxisName=NULL, OGRAxisOrientation eZAxisOrientation = OAO_Unknown );

EPSG 때문에 이 좌표계를 위도/경도로 취급해야 하는 경우 EPSG 코드를 기반으로 참을 반환합니다. 표준 때문에 EPSG:4326을 위도/경도로 해석해야 하는 WMS 1.3버전 같은 맥락에서 유용합니다.

.. code-block:: cpp

   int         EPSGTreatsAsLatLong();

다음은 :cpp:func:`importFromEPSG` 처럼 작동하지만 EPSG가 정의하는 AXIS 정의를 할당할 것입니다:

.. code-block:: cpp

   OGRErr      importFromEPSGA( int );

축 정의가 필요없는 곳에 ``OGRSpatialReference::StripNodes( "AXIS" );`` 를 이용해서 축 정의를 삭제할 수 있다는 사실을 기억하십시오.

importFromURN
~~~~~~~~~~~~~

:cpp:func:`importFromURN` 이 EPSG 및 OGC 지리 좌표계에 AXIS 값을 적절하게 설정할 수 있도록 수정합니다. 즉 EPSG 규범을 정말로 준수하기 위해 ``urn:...:EPSG:`` 를 가정할 것입니다.

SetWellKnownGeogCS()
~~~~~~~~~~~~~~~~~~~~

이 메소드는 다음을 수행할 수 있는 유일한 코드로 보입니다:

-  :cpp:func:`SetWellKnownGeogCS` 가 AXIS 값을 설정하지 '않도록' 수정하면, 하드코딩된 다른 모든 WKT 정의에서 AXIS 값을 삭제합니다.

importFromEPSG()
~~~~~~~~~~~~~~~~

-  :cpp:func:`importFromEPSG` 는 계속해서 GEOGCS 좌표계에 AXIS 값을 설정하지 '않을' 것입니다.
-  :cpp:func:`importFromEPSG` 는 이제 (적어도 기본 축 방향이 아닌 크르조바크(Křovák) 투영법 같은 경우) 투영 좌표계에 AXIS 값을 설정할 것입니다.
-  :cpp:func:`importFromEPSGA` 를 호출해서 반환되는 정의의 지리 부분으로부터 축 정의를 삭제함으로써 :cpp:func:`importFromEPSG` 를 구현할 것입니다.

SetFromUserInput()
~~~~~~~~~~~~~~~~~~

-  이 메소드는 (``EPSG:n`` 을 :cpp:func:`importFromEPSG` 로 전송하는 것과 비슷하게) ``EPSGA:`` 접두어를 앞에 붙인 값을 :cpp:func:`importFromEPSGA` 로 전송하는 새 옵션 하나를 가질 것입니다.

OGRCoordinateTransformation
---------------------------

소스 그리고/또는 대상 좌표계 상에 AXIS 값이 설정된 경우, PROJ를 호출하기 전에 :cpp:class:`OGRCoordinateTransformation` 코드가 일반적인 편북/편동으로 변환시킬 것입니다.

"GDAL_IGNORE_AXIS_ORIENTATION" CPL 환경설정 옵션을 "TRUE"로 설정하면 :cpp:class:`OGRCoordinateTransformation` 의 확인 작업 및 축 방향 변경 적용을 비활성화시킬 수도 있습니다. 이는 실질적으로 이 RFC의 핵심 영향을 비활성화시킬 수 있는 백도어입니다.

영향을 받는 드라이버
--------------------

-  GMLJP2 (:file:`gcore/gdalgmlcoverage.cpp` 및 :file:`gcore/gdaljp2metadata.cpp` 에 있는 클래스들)
-  WCS (URN 해석 기반)
-  WMS (아마도? 사실, 케이퍼빌리티로부터 실제 좌표계를 가져오지 못 할 것이라고 의심하고 있습니다)
-  OGR GML (아마도? GML3만 영향을 받을 수도?)
-  BSB, SAR_CEOS, ENVISAT, HDF4, JDEM, L1B, LAN, SRTMHGT:
   :cpp:func:`SetWellKnownGeogCS` 처럼 이 드라이버들 모두 하드코딩된 고유 WGS84 좌표계에 위도/경도 AXIS 사양을 포함하고 있습니다. 이 드라이버들이 좌표를 기본적으로 경도/위도로 해석하도록 이 하드코딩된 좌표계 사양을 제거해야 합니다.

버전
----

GDAL/OGR 1.5.x버전에 적용될 다음 사항들을 제외하고, 모든 작업은 GDAL/OGR 1.6.0버전을 위한 트렁크에서 이루어질 것입니다:

-  :cpp:func:`SetWellKnownGeogCS` 및 하드코딩된 WKT 문자열을 가진 여러 드라이버들로부터 지리 좌표계 용 기존 AXIS 지정자(specifier)를 삭제할 것입니다.
-  GMLJP2 (그리고 아마도 WCS) 코드에 EPSG 기관 위도/경도 값들의 순서를 뒤바꾸기 위한 어떤 종류의 꼼수를 도입해야 할 것입니다.

구현
----

프랑크 바르메르담이 이 RFC를 구현할 것입니다. (투영 좌표계의 축 순서를 제대로 수집하는 등의) 몇몇 측면은 당장 구현되지 않을 수도 있습니다.

호환성 문제점
-------------

가장 우려되는 사항은 GDAL/OGR 1.6.0버전이 (예를 들면 VRT 파일 또는 .aux.xml 파일에서와 같이) 위도/경도 축 순서를 가진 기존의 모든 WKT 좌표계를 GDAL/OGR 1.5.0버전과 다르게 해석할 것이라는 점입니다. BSB 또는 HDF4 같은 포맷으로 된 파일을 (.aux.xml 관련 파일을 가진 JPEG 같은) WKT 좌표계를 사용하는 포맷으로 변환하는 경우 이런 일이 쉽게 일어날 수 있습니다. 이런 호환성 문제점을 부분적으로 완화하기 위해, GDAL 1.5.1버전에서 AXIS 정의를 제거할 것을 제안합니다.

지원 정보
---------

-  OSGeo 위키 요약:
   `https://wiki.osgeo.org/wiki/Axis_Order_Confusion <https://wiki.osgeo.org/wiki/Axis_Order_Confusion>`_

