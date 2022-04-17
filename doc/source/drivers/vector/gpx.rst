.. _vector.gpx:

GPX - GPS 정보 교환 포맷
=========================

.. shortname:: GPX

.. build_dependencies:: (읽기 지원에 libexpat 필요)

GPX(GPS Exchange Format)는 응용 프로그램과 인터넷 상의 웹 서비스 사이의 GPS 데이터(waypoint, route 및 track)를 교환하기 위한 가벼운 XML 데이터 포맷입니다.

OGR는 GPX 파일 쓰기 및 (GDAL이 *Expat* 라이브러리 지원과 함께 빌드된 경우) 읽기를 지원합니다.

지원 버전은 읽기의 경우 GPX 1.0 및 1.1버전, 쓰기의 경우 GPX 1.1버전입니다.

OGR GPX 드라이버는 모든 GPX 객체 유형의 읽기 및 쓰기를 지원합니다:

-  *waypoint* : OGR wkbPoint 유형 객체의 레이어
-  *route* : OGR wkbLineString 유형 객체의 레이어
-  *track* : OGR wkbMultiLineString 유형 객체의 레이어

독립 레이어(*route_points* 및 *track_points*)에 있는 경로(route) 포인트와 트랙(track) 포인트의 읽기도 지원하기 때문에, OGR가 이 포인트들의 속성도 사용할 수 있습니다:

-  경로의 각 경로 포인트는 GPX 속성뿐만 아니라, 속해 있는 경로의 FID를 가리키는 외래 키인 *route_fid* 및 경로에서의 순차 번호인 *route_point_id* 속성도 가지고 있습니다.
-  트랙 포인트도 마찬가지로 *track_fid*, *track_seg_id* 및 *track_seg_point_id* 속성을 가지고 있습니다. 모든 좌표는 WGS84 원점(EPSG:4326)에 상대적인 좌표입니다.

GPX_ELE_AS_25D 환경 변수를 YES로 설정하면, 표고 요소를 이용해서 웨이포인트, 경로 포인트 및 트랙 포인트의 Z좌표를 설정할 것입니다.

OGR GPX 드라이버는 웨이포인트, 경로 및 트랙에 대한 GPX 속성을 읽고 씁니다.

기본적으로, 객체는 *<link>* 요소를 2개까지 연산에 넣을 수 있습니다. 이 기본 개수는 GPX_N_MAX_LINKS 환경 변수로 변경할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

인코딩 문제점
---------------

Expat 라이브러리는 다음 내장 인코딩 읽기를 지원합니다:

-  US-ASCII
-  UTF-8
-  UTF-16
-  ISO-8859-1
-  Windows-1252

OGR가 반환하는 콘텐츠는 파일 헤더에 언급된 인코딩으로 변환한 다음 UTF-8로 인코딩될 것입니다.

GPX 파일이 앞의 인코딩 가운데 하나로 인코딩되지 않은 경우, GPX 드라이버는 해당 파일을 파싱하지 않을 것입니다. 해당 파일을 지원되는 인코딩 가운데 하나로 -- 예를 들면 *iconv* 유틸리티를 이용해서 -- 변환한 다음 XML 헤더에 있는 *encoding* 파라미터를 그에 맞춰 변경할 수도 있습니다.

GPX 파일 작성 시, 이 드라이버는 UTF-8 콘텐츠가 전송되어 올 것으로 예상합니다.

확장 사양 요소 읽기
--------------------------

GPX 파일에서 *<extensions>* 요소를 탐지한 경우, OGR는 해당 요소의 하위 요소를 필드로 노출시킬 것입니다. 하위 요소의 복잡 콘텐츠는 XML 블랍(blob)으로 노출될 것입니다.

다음과 같은 GPX 콘텐츠 시퀀스를:

.. code-block:: xml

       <extensions>
           <navaid:name>TOTAL RF</navaid:name>
           <navaid:address>BENSALEM</navaid:address>
           <navaid:state>PA</navaid:state>
           <navaid:country>US</navaid:country>
           <navaid:frequencies>
           <navaid:frequency type="CTAF" frequency="122.900" name="CTAF"/>
           </navaid:frequencies>
           <navaid:runways>
           <navaid:runway designation="H1" length="80" width="80" surface="ASPH-G">
           </navaid:runway>
           </navaid:runways>
           <navaid:magvar>12</navaid:magvar>
       </extensions>

OGR 단순 피처 모델에서 다음과 같이 해석할 것입니다:

::

     navaid_name (String) = TOTAL RF
     navaid_address (String) = BENSALEM
     navaid_state (String) = PA
     navaid_country (String) = US
     navaid_frequencies (String) = <navaid:frequency type="CTAF" frequency="122.900" name="CTAF" ></navaid:frequency>
     navaid_runways (String) = <navaid:runway designation="H1" length="80" width="80" surface="ASPH-G" ></navaid:runway>
     navaid_magvar (Integer) = 12

주의: GPX 드라이버는 확장 사양 요소가 GPX 파일의 첫 번째 레코드에 있는 경우에만 그 내용을 산출할 것입니다. 확장 사양이 첫 번째 레코드 이후에 나타나는 경우, :decl_configoption:`GPX_USE_EXTENSIONS` 환경 변수로 파일 전체를 강제로 명확하게 파싱할 수 있습니다.

생성 문제점
---------------

내보내기 작업 시, 단일 GPX 파일에 모든 레이어를 작성합니다. 현재 기존 파일의 업데이트는 지원하지 않습니다.

산출 파일이 이미 존재하는 경우, 작성하지 않을 것입니다. 먼저 기존 파일을 삭제해야 합니다.

다음 도형을 지원합니다:

-  *wpt* 요소에 작성된 wkbPoint/wkbPoint25D 유형의 객체
-  *rte* 요소에 작성된 wkbLineString/wkbLineString25D 유형의 객체
-  *trk* 요소에 작성된 wkbMultiLineString/wkbMultiLineString25D 유형의 객체
-  이 외에 다른 도형 유형은 지원하지 않습니다.

경로 포인트 및 트랙 포인트의 경우, Z좌표가 있다면 대응하는 포인트의 표고 요소를 채우는 데 사용합니다.

wkbPoint/wkbPoint25D 도형을 가진 "track_points"라는 이름의 레이어가 있다면, 해당 레이어에 있는 객체들의 순열(sequence)로부터 GPX 파일에 트랙을 작성할 것입니다. 이 방법으로 트랙 포인트에 원시(raw) 좌표뿐만 아니라 각 트랙 포인트에 대한 GPX 속성을 설정합니다. 'track_fid' 필드의 동일한 값 덕분에 포인트가 동일한 트랙에 속해 있는지를 식별할 수 있습니다. (그리고 'track_seg_id' 필드의 값에 따라 트랙을 트랙 선분(track segment)으로 분할할 것입니다.) 트랙 객체를 제대로 재구성하기 위해서는 트랙 선분들을 반드시 차례대로 작성해야만 합니다. 트랙의 <name> 요소를 채우려면 첫 번째 트랙 포인트에 'track_name' 필드를 설정하면 됩니다.
마찬가지로, wkbPoint/wkbPoint25D 도형을 가진 "route_points"라는 이름의 레이어가 있다면 'route_fid' 필드에 동일한 값을 가진 포인트들의 순열로부터 GPX 파일에 경로를 작성할 것입니다. 경로의 <name> 요소를 채우려면 첫 번째 경로 포인트에 'route_name' 필드를 설정하면 됩니다.

레이어 생성 옵션
----------------

-  **FORCE_GPX_TRACK**:
   객체 유형이 wkbLineString인 레이어 작성 시 GPX 드라이버는 기본적으로 wkbLineString 객체들을 경로로 작성하려 합니다. FORCE_GPX_TRACK=YES를 지정하면, 트랙으로 작성할 것입니다.
-  **FORCE_GPX_ROUTE**:
   객체 유형이 wkbMultiLineString인 레이어 작성 시 GPX 드라이버는 기본적으로 wkbMultiLineString 객체들을 트랙으로 작성하려 합니다. FORCE_GPX_ROUTE=YES를 지정하면, 멀티라인이 단일 라인 하나만으로 이루어져 있는 경우 경로로 작성할 것입니다.

데이터셋 생성 옵션
------------------

-  **GPX_USE_EXTENSIONS**:
   GPX 드라이버는 기본적으로 GPX XML 정의(name, cmt 등등)와 일치하지 않는 속성 필드들을 폐기할 것입니다.
   GPX_USE_EXTENSIONS=YES를 지정하면, *<extensions>* 태그 안에 추가 필드를 작성할 것입니다.
-  **GPX_EXTENSIONS_NS**:
   GPX_USE_EXTENSIONS=YES 그리고 GPX_EXTENSIONS_NS_URL을 지정한 경우에만 사용할 수 있습니다.
   확장 사양 태그 용으로 사용되는 이름공간 값입니다. 기본값은 "ogr"입니다.
-  **GPX_EXTENSIONS_NS_URL**:
   GPX_USE_EXTENSIONS=YES 그리고 GPX_EXTENSIONS_NS를 지정한 경우에만 사용할 수 있습니다.
   이름공간 URI입니다. 기본값은 "http://osgeo.org/gdal" 입니다.
-  **LINEFORMAT**:
   기본적으로 새 GPX 파일을 생성할 때 로컬 플랫폼의 새줄 문자 규범으로 (win32에서는 CR/LF로 또는 다른 모든 시스템에서는 LF로) 생성합니다. **CRLF** (도스 서식) 또는 **LF** (유닉스 서식) 값을 가질 수 있는 LINEFORMAT 데이터셋 생성 옵션을 이용하면 이 기본 습성을 대체할 수 있습니다.

XML 스키마를 기준으로 무결하려면 반드시 웨이포인트, 경로, 트랙 순서대로 작성해야만 합니다.

소스 데이터셋으로부터 변환할 때, 소스 데이터셋의 필드 이름을 <name>, <desc> 등등 같은 예상되는 GPX 속성 이름으로 재명명해야 할 수도 있습니다. 이 작업은 :ref:`OGR VRT <vector.vrt>` 데이터셋으로 할 수도 있고, 또는 ogr2ogr 유틸리티의 "-sql" 옵션을 사용해서 할 수도 있습니다.

shapefile로 변환 시 문제점
------------------------------------

-  *track_points* 레이어를 shapefile로 변환할 때, DBF 파일에서 "track_seg_id" 및 "track_seg_point_id" 필드 이름을 문자 10개 길이로 절단(truncate)하기 때문에 이름이 중복되게 됩니다.

   이런 상황을 막으려면, :decl_configoption:`GPX_SHORT_NAMES` 환경설정 옵션을 TRUE로 설정해서 이 이름들을 각각 "trksegid" 및 "trksegptid"로 리포트되게 만들어 DBF 파일에 유일명으로 변환될 수 있게 해주면 됩니다. *route_points* 레이어의 "route_point_id" 필드도 "rteptid"로 재명명될 것입니다. 그러나 확장 사양 필드 이름에 대해서는 어떤 특정한 처리도 하지 않을 것이라는 사실을 기억하십시오.

   GPX 파일의 track_points 레이어를 shapefile 집합으로 변환하기:

   ::

          ogr2ogr --config GPX_SHORT_NAMES YES out input.gpx track_points

-  shapefile은 날짜&시간 유형의 필드를 지원하지 않습니다. 날짜 유형의 필드만 지원합니다. 따라서 기본적으로 GPX 파일에 있는 *Time* 요소의 시:분:초 부분을 잃게 될 것입니다.

   OGR SQL CAST 연산자를 사용해서 *time* 필드를 문자열로 변환할 수 있습니다:

   ::

          ogr2ogr out input.gpx -sql "SELECT ele, CAST(time AS character(32)) FROM waypoints"

   모든 필드를 선택한 다음, 지정한 유형의 필드를 문자열로 변환하도록 요청할 수 있는 더 간편한 방법이 있습니다:

   ::

          ogr2ogr out input.gpx -fieldTypeToString DateTime

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

예시
-------

-  ogrinfo 유틸리티를 사용해서 GPX 데이터 파일의 내용을 덤프하기:

::

   ogrinfo -ro -al input.gpx

-  ogr2ogr 유틸리티를 사용해서 GPX를 GPX로 변환하기:

::

   ogr2ogr -f GPX output.gpx input.gpx waypoints routes tracks

   주의: GPX를 GPX로 변환하는 경우, route_points 및 track_points 레이어를 폐기하기 위해 레이어 이름을 지정해야 합니다.

-  산출물에 *<extensions>* 태그를 사용하면:

::

   ogr2ogr -f GPX  -dsco GPX_USE_EXTENSIONS=YES output.gpx input

   다음과 같은 산출물을 생성할 것입니다:

.. code-block:: xml

       <?xml version="1.0"?>
       <gpx version="1.1" creator="GDAL 1.5dev"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:ogr="http://osgeo.org/gdal"
       xmlns="http://www.topografix.com/GPX/1/1"
       xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
       <wpt lat="1" lon="2">
       <extensions>
           <ogr:Primary_ID>PID5</ogr:Primary_ID>
           <ogr:Secondary_ID>SID5</ogr:Secondary_ID>
       </extensions>
       </wpt>
       <wpt lat="3" lon="4">
       <extensions>
           <ogr:Primary_ID>PID4</ogr:Primary_ID>
           <ogr:Secondary_ID>SID4</ogr:Secondary_ID>
       </extensions>
       </wpt>
       </gpx>

-  "-sql" 옵션을 이용해서 필드 이름을 GPX 스키마가 허용하는 이름으로 다시 매핑하기:

::

   ogr2ogr -f GPX output.gpx input.shp -sql "SELECT field1 AS name, field2 AS desc FROM input"

FAQ
---

"ERROR 6: Cannot create GPX layer XXXXXX with unknown geometry type" 오류를 어떻게 해결할 수 있을까요?

생성할 레이어가 정확한 도형 유형을 노출하지 않고 일반 wkbUnknown 유형만 노출하는 경우 이 오류가 발생합니다. 예를 들면 ogr2ogr 유틸리티를 사용해서 PostgreSQL 데이터소스에 SQL 요청을 보내는 경우와 같습니다. 사용자가 "-nlt POINT" (또는 LINESTRING 또는 MULTILINESTRING)을 명확하게 지정해야만 합니다.

참고
--------

-  `GPX 포맷 홈페이지 <http://www.topografix.com/gpx.asp>`_

-  `GPX 1.1 포맷 문서 <http://www.topografix.com/GPX/1/1/>`_

