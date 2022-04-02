.. _raster.wms:

================================================================================
WMS -- Web Map Services
================================================================================

.. shortname:: WMS

.. build_dependencies:: libcurl

GDAL에서 WMS 포맷을 사용하면 서로 다른 여러 유형의 웹 이미지 서비스에 접근할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

XML 설명 파일
--------------------

로컬 서비스 설명 XML 파일을 생성해서 웹 이미지 서비스에 접근할 수 있습니다. 다음 표는 지원하는 이미지 서비스 각각의 예시입니다. ``<GDAL_WMS>`` 요소 앞에 어떤 공백이나 다른 내용도 없다는 사실이 중요합니다.

.. list-table:: Local Service Description XML File for WMS
   :header-rows: 0

   * - <GDAL_WMS>
     - 
   * - <Service name="WMS">
     - 어떤 미니 드라이버(minidriver)를 사용할지 정의하십시오. 현재 WMS, WorldWind, TileService, TMS, TiledWMS, VirtualEarth 또는 AGS를 지원합니다. (필수)
   * - <Version>1.1.1</Version>
     - WMS 버전입니다. (선택적, 기본값은 1.1.1)
   * - <ServerUrl>http://host.domain.com/wms.cgi?</ServerUrl>
     - WMS 서버 URL (필수)
   * - <SRS>EPSG:4326</SRS>
     - 이미지 투영법입니다. (선택적, WMS 1.1.1 이하 버전에서만 WMS 기본값은 EPSG:4326이고 ArcGIS 서버의 AGS 기본값은 102100입니다.) ArcGIS 서버의 경우 공간 좌표계를 WKID(Well-Known ID) 또는 `공간 참조 JSON 객체 <http://resources.arcgis.com/en/help/rest/apiref/geometry.html#sr>`_ 가운데 하나로 지정할 수 있습니다.
   * - <CRS>CRS:83</CRS>
     - 이미지 투영법입니다. (선택적, WMS 1.3.0 이상 버전에서만 기본값은 EPSG:4326입니다.)
   * - <ImageFormat>image/jpeg</ImageFormat>
     - 데이터를 이 포맷으로 요청합니다. image/gif 같은 색상표 포맷은 RGB로 변환할 것입니다. (선택적, 기본값은 image/jpeg)
   * - <Transparent>FALSE</Transparent>
     - WMS GetMap 요청에 "transparent=TRUE"를 포함시키려면 TRUE로 설정하십시오. (선택적, 기본값은 거짓) 요청하는 포맷과 BandsCount가 알파 채널을 지원해야 합니다.
   * - <Layers>modis%2Cglobal_mosaic</Layers>
     - URL로 인코딩된, 쉼표로 구분된 레이어 문자열 (필수, TiledWMS는 예외)
   * - <TiledGroupName>Clementine</TiledGroupName>
     - 쉼표로 구분된 레이어 목록 (TiledWMS에 필수)
   * - <Styles></Styles>
     - 쉼표로 구분된 스타일 목록 (선택적)
   * - <BBoxOrder>xyXY</BBoxOrder>
     - 경계 상자 좌표를 임의로 재배열합니다. 1.3버전 서버의 경우 필수일 수도 있습니다. (선택적) x - 하단 X 좌표, y - 하단 Y 좌표, X - 상단 X 좌표, Y - 상단 Y 좌표
   * - </Service>
     - 
   * - <DataWindow>
     - 데이터 크기 및 범위를 정의합니다. (필수, TiledWMS와 VirtualEarth는 예외)
   * - <UpperLeftX>-180.0</UpperLeftX>
     - 좌상단 모서리의 X (경도) 좌표 (선택적, 기본값은 -180.0, VirtualEarth는 예외)
   * - <UpperLeftY>90.0</UpperLeftY>
     - 좌상단 모서리의 Y (위도) 좌표 (선택적, 기본값은 90.0, VirtualEarth는 예외)
   * - <LowerRightX>180.0</LowerRightX>
     - 우하단 모서리의 X (경도) 좌표 (선택적, 기본값은 180.0, VirtualEarth는 예외)
   * - <LowerRightY>-90.0</LowerRightY>
     - 우하단 모서리의 Y (위도) 좌표 (선택적, 기본값은 -90.0, VirtualEarth는 예외)
   * - <SizeX>2666666</SizeX>
     - 픽셀 단위 이미지 크기
   * - <SizeY>1333333</SizeY>
     - 픽셀 단위 이미지 크기
   * - <TileX>0</TileX>
     - 최상위 해상도에서 타일에 추가되는 X값 (WMS의 경우 무시, 타일화 이미지 소스 전용, 선택적, 기본값은 0)
   * - <TileY>0</TileY>
     - 최상위 해상도에서 타일에 추가되는 Y값 (WMS의 경우 무시, 타일화 이미지 소스 전용, 선택적, 기본값은 0)
   * - <TileLevel>0</TileLevel>
     - 최상위 해상도에서의 타일 수준 (타일화 이미지 소스 전용, 선택적, 기본값은 0)
   * - <TileCountX>0</TileCountX>
     - 이미지 크기를 정의하기 위해 사용할 수 있습니다. SizeX = TileCountX \* BlockSizeX \* 2\ :sup:`TileLevel` (타일화 이미지 소스 전용, 선택적, 기본값은 0)
   * - <TileCountY>0</TileCountY>
     - 이미지 크기를 정의하기 위해 사용할 수 있습니다. SizeY = TileCountY \* BlockSizeY \* 2\ :sup:`TileLevel` (타일화 이미지 소스 전용, 선택적, 기본값은 0)
   * - <YOrigin>top</YOrigin>
     - 타일 그리드 관점에서 Y 원점의 위치를 정의하기 위해 사용할 수 있습니다. 'top', 'bottom' 및 'default' 가운데 하나로 설정할 수 있습니다. 이때 기본 습성은 미니 드라이버 특화 습성입니다. (TMS 미니 드라이버 전용, 선택적, 기본값은 TMS의 경우 'bottom')
   * - </DataWindow>
     - 
   * - <Projection>EPSG:4326</Projection>
     - 이미지 투영법 (선택적, 기본값은 미니 드라이버가 리포트한 값 또는 EPSG:4326)
   * - <IdentificationTolerance>2</IdentificationTolerance>
     - 식별 허용 오차 (선택적, 기본값은 2)
   * - <BandsCount>3</BandsCount>
     - 밴드/채널 개수입니다. 1은 회색조 데이터, 3은 RGB, 4는 RGBA입니다. (선택적, 기본값은 3)
   * - <DataType>Byte</DataType>
     - 밴드 데이터 유형입니다. Byte, Int16, UInt16, Int32, UInt32, Float32, Float64 등등 가운데 하나로 설정할 수 있습니다. (선택적, 기본값은 Byte)
   * - <DataValues NoData="0 0 0" min="1 1 1" max="255 255 255" />
     - 밴드의 NODATA 그리고/또는 최소값 그리고/또는 최대값을 정의합니다. nodata_values, min_values, max_values는 단일값 하나일 수도, 또는 공백으로 구분된 밴드 별 값일 수도 있습니다.
   * - <BlockSizeX>1024</BlockSizeX>
     - 픽셀 단위 블록 크기 (선택적, 기본값은 1024, VirtualEarth는 예외)
   * - <BlockSizeY>1024</BlockSizeY>
     - 픽셀 단위 블록 크기 (선택적, 기본값은 1024, VirtualEarth는 예외)
   * - <OverviewCount>10</OverviewCount>
     - 각각 해상도가 2배 낮아지는 감퇴 해상도 레이어의 개수 (선택적, 기본값은 런타임 시 계산됩니다.)
   * - <Cache>
     - 로컬 디스크 캐시를 활성화합니다. 오프라인 작업 시 사용할 수 있습니다.
       (선택적이지만 자동 생성된 서비스 파일에 존재합니다. 이 요소가 없는 경우 또는 GDAL_ENABLE_WMS_CACHE=NO 환경설정 옵션으로 무시되는 경우 캐시를 비활성화합니다.)
   * - <Path>./gdalwmscache</Path>
     - 캐시 파일을 저장할 위치입니다. 서로 다른 데이터소스에 동일한 캐시 경로를 사용하는 편이 안전합니다. 임시 인메모리 캐시를 사용할 수 있게 해주는 /vsimem/ 경로를 지원합니다.
       (선택적, GDAL_DEFAULT_WMS_CACHE_PATH 환경설정 옵션을 지정하지 않는 경우 기본값은 ./gdalwmscache 입니다.)
   * - <Depth>2</Depth>
     - 디렉터리 레이어의 개수입니다. 2로 설정하면 파일을 cache_path/A/B/ABCDEF... 로 작성할 것입니다. (선택적, 기본값은 2)
   * - <Extension>.jpg</Extension>
     - 캐시 파일에 추가할 확장자입니다. (선택적, 기본값은 없습니다.)
   * - <Type>file</Type>
     - 캐시 유형입니다. 현재 'file' 유형만 지원합니다. 'file' 캐시 유형은 파일 시스템 폴더에 파일을 저장합니다. (선택적, 기본값은 'file')
   * - <Expires>604800</Expires>
     - 캐시 파일의 초 단위 제한 시간입니다. 캐시된 파일의 제한 시간이 지나면, 캐시 최대 용량에 도달했을 때 제한 시간이 지난 파일을 삭제합니다.
       제한 시간이 지난 파일을 웹으로부터 온 새 파일로 덮어쓸 수도 있습니다. 기본값은 7일(604,800초)입니다.
   * - <MaxSize>67108864</MaxSize>
     - 캐시의 바이트 단위 최대 용량입니다. 캐시 최대 용량에 도달했을 때 제한 시간이 지난 파일을 삭제할 것입니다. 기본값은 64Mb(67,108,864바이트)입니다.
   * - <CleanTimeout>120</CleanTimeout>
     - 초 단위 청소 스레드(Clean Thread) 실행 제한 시간입니다. 제한 시간이 지난 파일을 찾아서 삭제하는 청소 스레드를 얼마나 자주 실행할지 정의합니다. 기본값은 120초입니다.
       0으로 설정하면 청소 스레드를 비활성화합니다. (실질적으로 캐시 용량을 무제한으로 만듭니다.)
       대용량 캐시를 사용하려는 경우, 제한 시간이 지난 파일을 찾기 위해 캐시 파일들을 스캔하는 데 시간이 오래 걸릴 수도 있기 때문에 캐시 청소를 비활성화하거나 훨씬 긴 제한 시간을 사용해야 할 수도 있습니다.
       (GDAL 2.2 이하 버전에서는 "disabled" 로만 설정할 수 있습니다. GDAL 2.3 이상 3.1 이하 버전에서는 "120초"로만 설정할 수 있습니다.)
   * - <Unique>True</Unique>
     - 참으로 설정하면 경로에 ServerURL의 MD5 해시를 추가합니다. 기본값은 참입니다.
   * - </Cache>
     - 
   * - <MaxConnections>2</MaxConnections>
     - 최대 동시 연결 개수입니다. (선택적, 기본값은 2) :decl_configoption:`GDAL_MAX_CONNECTIONS` 환경설정 옵션으로도 설정할 수 있습니다. (GDAL 3.2 이상 버전)
   * - <Timeout>300</Timeout>
     - 초 단위 연결 제한 시간입니다. (선택적, 기본값은 300)
   * - <OfflineMode>true</OfflineMode>
     - 어떤 새 이미지도 다운로드하지 않고, 캐시에 있는 이미지만 사용합니다. 캐시를 활성화한 경우에만 유용합니다. (선택적, 기본값은 거짓)
   * - <AdviseRead>true</AdviseRead>
     - AdviseRead API 호출을 활성화합니다 -- 캐시에 이미지를 다운로드합니다. (선택적, 기본값은 거짓)
   * - <VerifyAdviseRead>true</VerifyAdviseRead>
     - 캐시에 이미지를 작성하기 전에 다운로드한 이미지를 각각 열어서 몇몇 기본 확인 작업을 수행합니다.
       서버가 항상 정확한 이미지를 반환한다고 신뢰하는 경우, 거짓으로 설정하면 CPU 사이클을 절약할 수 있습니다. (선택적, 기본값은 참)
   * - <ClampRequests>false</ClampRequests>
     - 부분적으로 정의된 데이터 윈도우 바깥에 있을 블록을 잘라내도록 요청해서 블록 크기 요청보다 작은 데이터를 반환받을 것입니다. (선택적, 기본값은 참)
   * - <UserAgent>GDAL WMS driver (http://www.gdal.org/frmt_wms.html)</UserAgent>
     - HTTP 사용자 에이전트(user agent) 문자열입니다. 일부 서버는 "Mozilla/5.0" 같은 잘 알려진 사용자 에이전트를 요구할 수도 있습니다. (선택적, 기본값은 "GDAL WMS driver (http://www.gdal.org/frmt_wms.html)")
       오픈스트리트맵 서버 같은 일부 서버를 이용하는 경우, 기본 사용자 에이전트가 블락당했다면 다시 블락당하는 일이 없도록 사용자 지정 사용자 에이전트를 삽입할 것을 강력히 권장합니다.
   * - <Accept>mimetype</Accept>
     - 서버의 예상 산출물의 MIME 유형을 지정하는 HTTP Accept 헤더입니다. 기본적으로 비어 있습니다.
   * - <UserPwd>user:password</UserPwd>
     - HTTP 인증 용 사용자 ID 및 비밀번호입니다. (선택적)
   * - <UnsafeSSL>true</UnsafeSSL>
     - SSL 인증서 검증을 건너뜁니다. 서버가 자체 서명한 인증서를 사용하는 경우 필요할 수도 있습니다. (선택적, 기본값은 거짓)
   * - <Referer>http://example.foo/</Referer>
     - HTTP 리퍼러(HTTP Referer) 문자열입니다. 일부 서버가 요구할 수도 있습니다. (선택적)
   * - <ZeroBlockHttpCodes>204,404</ZeroBlockHttpCodes>
     - 요청 중단 대신 0으로 채워진 이미지로 (예를 들어 3밴드의 경우 검은색, 4밴드의 경우 투명으로) 해석될, 쉼표로 구분된 HTTP 응답 코드 목록입니다. (선택적, 기본값은 204)
   * - <ZeroBlockOnServerException>true</ZeroBlockOnServerException>
     - 서버가 반환한 서비스 예외(Service Exception)를 요청 중단 대신 0으로 채워진 이미지로 취급할지 여부를 선택합니다. (선택적, 기본값은 거짓)
   * - </GDAL_WMS>
     - 

GDAL 2.3버전부터, GDAL_HTTP_HEADER_FILE 환경설정 옵션이 "key: value" HTTP 헤더를 가지고 있는 텍스트 파일의 파일명을 가리키도록 설정하면 추가적인 HTTP 헤더를 전송할 수 있습니다.

미니 드라이버
------------

GDAL WMS 드라이버는 몇몇 내부 '미니 드라이버(minidriver)'를 지원합니다. 이 미니 드라이버들은 각각 서로 다른 웹 매핑 서비스에 접근할 수 있도록 해줍니다. 각 서비스는 Service 블록에 있는 서로 다른 옵션 집합을 지원할 수도 있습니다.

WMS
~~~

OGC WMS 서버와 통신합니다. 타일화 및 비타일화 요청을 모두 지원합니다.

gdallocationinfo 유틸리티를 (GetFeatureInfo 요청을 통해) 이용하면, 또는 밴드 객체에 GetMetadataItem("Pixel_iCol_iLine", "LocationInfo")를 호출하면 WMS 레이어를 쿼리할 수 있습니다.

::

   gdallocationinfo "WMS:http://demo.opengeo.org/geoserver/gwc/service/wms?SERVICE=WMS&VERSION=1.1.1&
                               REQUEST=GetMap&LAYERS=og%3Abugsites&SRS=EPSG:900913&
                               BBOX=-1.15841845090625E7,5479006.186718751,-1.1505912992109375E7,5557277.703671876&
                               FORMAT=image/png&TILESIZE=256&OVERVIEWCOUNT=25&MINRESOLUTION=0.0046653459640220&TILED=true"
                              -geoloc -11547071.455 5528616 -xml -b 1


산출물:

::

   Report pixel="248595" line="191985">
     <BandReport band="1">
       <LocationInfo>
         <wfs:FeatureCollection xmlns="http://www.opengis.net/wfs"
                                   xmlns:wfs="http://www.opengis.net/wfs"
                                   xmlns:gml="http://www.opengis.net/gml"
                                   xmlns:og="http://opengeo.org"
                                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                   xsi:schemaLocation="http://opengeo.org http://demo.opengeo.org/geoserver/wfs?service=WFS&version=1.0.0&request=DescribeFeatureType&typeName=og%3Abugsites http://www.opengis.net/wfs http://demo.opengeo.org/geoserver/schemas/wfs/1.0.0/WFS-basic.xsd">
           <gml:boundedBy>
             <gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml#26713">
               <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">601228,4917635 601228,4917635</gml:coordinates>
             </gml:Box>
           </gml:boundedBy>
           <gml:featureMember>
             <og:bugsites fid="bugsites.40946">
               <gml:boundedBy>
                 <gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml#26713">
                   <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">601228,4917635 601228,4917635</gml:coordinates>
                 </gml:Box>
               </gml:boundedBy>
               <og:cat>86</og:cat>
               <og:str1>Beetle site</og:str1>
               <og:the_geom>
                 <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#26713">
                   <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">601228,4917635</gml:coordinates>
                 </gml:Point>
               </og:the_geom>
             </og:bugsites>
           </gml:featureMember>
         </wfs:FeatureCollection>
       </LocationInfo>
       <Value>255</Value>
     </BandReport>
   </Report>


TileService
~~~~~~~~~~~

WorldWind `TileService <http://www.worldwindcentral.com/wiki/TileService>`_ 와의 통신을 지원합니다.
언제나 타일 기반으로 접근합니다.

WorldWind
~~~~~~~~~

웹 기반 WorldWind 타일 서비스에 접근합니다. 언제나 타일 기반으로 접근합니다.

TMS
~~~

TMS 미니 드라이버는 주로 `TMS 사양 <http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification>`_ 사용자를 지원하기 위해 설계되었습니다.
이 서비스는 타일 접근만 지원합니다.

TMS가 웹 상의 다른 많은 'x/y/z' 계열 서비스와 유사하기 때문에, 이 서비스를 이용해서 이런 서비스들에도 접근할 수 있습니다. 이 서비스를 이런 방식으로 이용하려면, ${x}, ${y} 등의 서식으로 된 대체 변수를 사용하면 됩니다.

다음 변수들을 지원합니다(이름의 대소문자를 구분합니다):

-  ${x} -- 타일의 x 위치입니다.

-  ${y} -- 타일의 y 위치입니다. YOrigin 파라미터가 참 또는 거짓으로 설정되었느냐에 따라, 타일셋의 최상단 또는 최하단일 수 있습니다.

-  ${z} -- 타일의 z 위치 -- 확대/축소 수준 -- 입니다.

-  ${version} -- 환경설정 파일에 설정된 버전 파라미터입니다. 기본값은 1.0.0입니다.

-  ${format} -- 환경설정 파일에 설정된 포맷 파라미터입니다. 기본값은 'jpg'입니다.

-  ${layer} -- 환경설정 파일에 설정된 레이어 파라미터입니다. 기본값은 없습니다.

전형적인 ServerURL은 다음과 같이 보일 것입니다:

``http://tilecache.osgeo.org/wms-c/Basic.py/${version}/${layer}/${z}/${x}/${y}.${format}``

TMS 사용자에게 적합하도록, "${"를 담고 있지 않은 모든 URL에 ("Basic.py/" 뒤의) 문자열을 자동으로 추가할 것입니다.

TMS 서비스는 다른 서비스들과 차별되는 XML 환경설정 요소 3개를 가지고 있습니다:

-  ``Format``: 기본값 ``jpg``
-  ``Layer``: 기본값 없음
-  ``Version``: 기본값 ``1.0.0``

뿐만 아니라, TMS 서비스는 DataWindow 수준에서 또 하나의 추가 파라미터 YOrigin 요소를 준수합니다. 이 요소의 값은 (TMS 기본값인) ``bottom`` 또는 오픈스트리트맵 및 다른 많은 유명한 타일 서비스와 일치하는 ``top`` 가운데 하나여야 합니다.

TMS 서비스 활용 예시 2개가 아래 예시에 포함되어 있습니다.

OnEarth 타일화 WMS
~~~~~~~~~~~~~~~~~~

OnEarth 타일화(Tiled) WMS 미니 드라이버는 JPL OnEarth 드라이버의 사양 별로 구현된 `타일화 WMS 사양 <http://web.archive.org/web/20130511182803/http://onearth.jpl.nasa.gov/tiled.html>`_ 을 지원합니다.

ServerUrl과 TiledGroupName만 필요하며, 연결 시 GetTileService 메소드를 이용해서 원격 서버로부터 필요한 정보 대부분을 자동으로 가져옵니다.

전형적인 OnEarth 타일화 WMS 환경설정 파일은 다음과 같이 보일 것입니다:

::

   <GDAL_WMS>
       <Service name="TiledWMS">
       <ServerUrl>https://gibs.earthdata.nasa.gov/twms/epsg4326/best/twms.cgi?</ServerUrl>
       <TiledGroupName>MODIS Terra CorrectedReflectance TrueColor tileset</TiledGroupName>
       <Change key="${time}">2020-02-02</Change>
       </Service>
   </GDAL_WMS>

TiledWMS 미니 드라이버는 다음 열기 옵션들을 사용할 수 있습니다:

-  **TiledGroupName**:
   이 옵션의 값은 서버에서 사용할 수 있는 타일화 서비스 가운데 하나를 식별하는 문자열입니다.

-  **Change**:
   서버로 전송할 <Key>:<Value> 쌍입니다. 키는 서버가 해당 타일화 그룹에 선언하는 변경 키(change key)와 일치해야 합니다. 서로 다른 키들을 위해 이 옵션을 여러 번 사용할 수 있습니다.

   *  예시: Change=time:2020-02-02

환경설정 파일에 대응하는 XML 요소가 없는 경우에만 이 열기 옵션을 받아들입니다.

VirtualEarth
~~~~~~~~~~~~

웹 기반 Virtual Earth 타일 서비스에 접근합니다. 언제나 타일 기반으로 접근합니다.

ServerUrl 요소에 반드시 ${quadkey} 변수가 있어야만 합니다.

DataWindow 요소를 생략할 수도 있습니다. 기본값은 다음과 같습니다:

-  UpperLeftX = -20037508.34
-  UpperLeftY = 20037508.34
-  LowerRightX = 20037508.34
-  LowerRightY = -20037508.34
-  TileLevel = 21
-  OverviewCount = 20
-  SRS = EPSG:3857
-  BlockSizeX = 256
-  BlockSizeY = 256

ArcGIS REST API
~~~~~~~~~~~~~~~

ArcGIS REST `맵 서비스 리소스 <http://resources.arcgis.com/en/help/rest/apiref/mapserver.html>`_ 에 접근합니다. (비타일화 요청)

gdallocationinfo 유틸리티를 (GetFeatureInfo 요청을 통해) 이용하면, 또는 밴드 객체에 GetMetadataItem("Pixel_iCol_iLine", "LocationInfo")를 호출하면 AGS 레이어를 `쿼리 <http://resources.arcgis.com/en/help/rest/apiref/identify.html>`_ 할 수 있습니다.

::

   gdallocationinfo -wgs84 "<GDAL_WMS><Service name=\"AGS\"><ServerUrl>http://sampleserver1.arcgisonline.com/ArcGIS/rest/services/Specialty/ESRI_StateCityHighway_USA/MapServer</ServerUrl><BBoxOrder>xyXY</BBoxOrder><SRS>3857</SRS></Service><DataWindow><UpperLeftX>-20037508.34</UpperLeftX><UpperLeftY>20037508.34</UpperLeftY><LowerRightX>20037508.34</LowerRightX><LowerRightY>-20037508.34</LowerRightY><SizeX>512</SizeX><SizeY>512</SizeY></DataWindow></GDAL_WMS>" -75.704 39.75


인터넷 이미징 프롵토콜(IIP) (GDAL 2.1 이상 버전)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`IIP(Internet Imaging Protocol) <https://en.wikipedia.org/wiki/Internet_Imaging_Protocol>`_ 를 통해 서비스되는 이미지에 접근합니다. 서버가 IIP 프로토콜의 (타일을 완전한 JFIF 이미지로 가져오는) JTL 확장 사양을 지원해야만 합니다.

XML 문법을 사용하는 경우, ServerURL이 FIF 파라미터를 담고 있어야만 합니다.

그렇지 않은 경우 "IIP:http://foo.com/FIF=image_name" 문법을 연결 문자열로 사용해서 서버로부터 전체 해상도 크기 및 해상도 수준 개수에 관한 정보를 가져올 수도 있습니다.

그러면 ``gdal_translate IIP:http://foo.com/FIF=image_name out.xml -of WMS`` 명령어로 XML 정의를 생성할 수 있습니다.

예시
--------

-  `onearth_global_mosaic.xml <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_onearth_global_mosaic.xml>`_:
   `OnEarth <http://onearth.jpl.nasa.gov/>`_ WMS 서버의 랜드샛 모자이크

   ::

      gdal_translate -of JPEG -outsize 500 250 onearth_global_mosaic.xml onearth_global_mosaic.jpg

   ::

      gdal_translate -of JPEG -projwin -10 55 30 35 -outsize 500 250 onearth_global_mosaic.xml onearth_global_mosaic2.jpg

   주의: 이 특정 서버는 더 이상 정규 WMS 쿼리를 받아들이지 않습니다.

-  `metacarta_wmsc.xml <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_metacarta_wmsc.xml>`_:
   오버뷰 개수를 지정하고 '블록 크기'를 캐시의 타일 크기로 지정하면 WMS 서버가 WMS-C 캐시를 준수하도록 환경설정할 수 있습니다. 다음은 19수준 "Global Profile" WMS-C 캐시를 설정하는 예시입니다:

   ::

      gdal_translate -of PNG -outsize 500 250 metacarta_wmsc.xml metacarta_wmsc.png

   .. only:: html

        .. image:: http://sydney.freeearthfoundation.com/gdalwms/metacarta_wmsc.png

-  `tileservice_bmng.xml <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_tileservice_bmng.xml>`_:
   TileService, Blue Marble NG (1월)

   ::

      gdal_translate -of JPEG -outsize 500 250 tileservice_bmng.xml tileservice_bmng.jpg

   .. only:: html

        .. image:: http://sydney.freeearthfoundation.com/gdalwms/tileservice_bmng.jpg

-  `tileservice_nysdop2004.xml <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_tileservice_nysdop2004.xml>`_:
   TileService, NYSDOP 2004

   ::

      gdal_translate -of JPEG -projwin -73.687030 41.262680 -73.686359 41.262345 -outsize 500 250 tileservice_nysdop2004.xml tileservice_nysdop2004.jpg

   .. only:: html

        .. image:: http://sydney.freeearthfoundation.com/gdalwms/tileservice_nysdop2004.jpg

-  `오픈스트리트맵 TMS 서비스 예시 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_openstreetmap_tms.xml>`_:
     오픈스트리트맵 타일 서비스에 연결합니다. 이 파일이 타일 캐시를 이용한다는 사실을 기억하십시오. 타일 캐시 환경 설정에 관한 자세한 정보는 앞에서 설명하고 있습니다. 기본 사용자 에이전트를 사용하다가 너무 많은 트래픽을 일으켜서 OSM 서버가 블락할 가능성을 피하기 위해, <UserAgent>도 변경해주십시오.

   ::

      gdal_translate -of PNG -outsize 512 512 frmt_wms_openstreetmap_tms.xml openstreetmap.png

-  `MetaCarta TMS 레이어 예시 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_metacarta_tms.xml>`_:
    기본 MetaCarta TMS 레이어에 접근합니다.

   ::

      gdal_translate -of PNG -outsize 512 256 frmt_wms_metacarta_tms.xml metacarta.png

-  `BlueMarble 아마존 S3 예시 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_bluemarble_s3_tms.xml>`_:
   TMS 미니 드라이버로 접근합니다.

-  `구글 맵 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_googlemaps_tms.xml>`_:
   TMS 미니 드라이버로 접근합니다.

-  `ArcGIS MapServer 타일 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_arcgis_mapserver_tms.xml>`_:
   TMS 미니 드라이버로 접근합니다.

-  OnEarth 타일화 WMS의 `Clementine <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_twms_Clementine.xml>`_, `daily <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_twms_daily.xml>`_ 및 `srtm <https://github.com/OSGeo/gdal/blob/master/gdal/frmts/wms/frmt_twms_srtm.xml>`_ 예시

-  `VirtualEarth 항공사진 레이어 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_virtualearth.xml>`_:
   VirtualEarth 미니 드라이버로 접근합니다.

-  `ArcGIS 온라인 샘플 서버 레이어 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_ags_arcgisonline.xml>`_:
   ArcGIS 서버 REST API 미니 드라이버로 접근합니다.

-  `IIP 온라인 샘플 서버 레이어 <https://github.com/OSGeo/gdal/blob/master/frmts/wms/frmt_wms_iip.xml>`_:
   IIP 미니 드라이버로 접근합니다.

열기 문법
-----------

WMS 드라이버는 다음을 열 수 있습니다:

-  로컬 서비스 설명 XML 파일:

   ::

      gdalinfo description_file.xml

-  파일명으로 제공되는 설명 XML 파일의 내용:

   ::

      gdalinfo "<GDAL_WMS><Service name=\"TiledWMS\"><ServerUrl>https://gibs.earthdata.nasa.gov/twms/epsg4326/best/twms.cgi?</ServerUrl><TiledGroupName>MODIS Terra CorrectedReflectance Bands367 tileset</TiledGroupName></Service></GDAL_WMS>"

-  *WMS:* 접두어가 붙은 WMS 서비스의 기반 URL:

   ::

      gdalinfo "WMS:http://wms.geobase.ca/wms-bin/cubeserv.cgi"

   해당 서버에 대한 GetCapabilities 요청의 결과물을 파싱해서 생성된 하위 데이터셋 목록을 반환할 것입니다.

-  바로 위의 예시에서 반환된 하위 데이터셋 이름 같은 의사 GetMap 요청:

   ::

      gdalinfo "WMS:http://wms.geobase.ca/wms-bin/cubeserv.cgi?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=DNEC_250K%3AELEVATION%2FELEVATION&SRS=EPSG:42304&BBOX=-3000000,-1500000,6000000,4500000"

-  *WMS:* 접두어가 붙고 request=GetTileService가 GET 인자인 타일화 WMS 서비스의 기반 URL:

   ::

      gdalinfo "WMS:https://gibs.earthdata.nasa.gov/twms/epsg4326/best/twms.cgi?request=GetTileService"

   해당 서버에 대한 GetTileService 요청의 결과물을 파싱해서 생성된 하위 데이터셋 목록을 반환할 것입니다.

-  ArcGIS MapServer 용 REST 정의의 URL:

   ::

      gdalinfo "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer?f=json&pretty=true"

-  (GDAL 2.1.0 이상 버전) IIP 이미지의 URL:

   ::

      gdalinfo "IIP:http://merovingio.c2rmf.cnrs.fr/fcgi-bin/iipsrv.fcgi?FIF=globe.256x256.tif"

WMS 서비스 설명 XML 파일 생성
----------------------------------------------

WMS 서비스 설명 XML 파일을 직접 생성할 수도, 또는 소스 데이터셋 자체가 WMS 데이터셋인 경우에만 WMS 드라이버의 CreateCopy() 작업의 산출물로 생성할 수도 있습니다. 그렇지 않은 경우, 앞의 "열기 문법"에서 언급된 문법 아무거나 gdal_translate의 소스 데이터셋으로 사용해서 XML 파일을 산출할 수도 있습니다. 다음은 그 예시입니다:

::

   gdal_translate "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer?f=json" wms.xml -of WMS

이렇게 생성된 파일은 사용자가 편집해야 할 수도 있는 기본값을 가질 것입니다.

참고
--------

-  `OGC WMS 표준 <http://www.opengeospatial.org/standards/wms>`_

-  `WMS 타일 작업 클라이언트 권장 사항(WMS-C) <http://wiki.osgeo.org/index.php/WMS_Tiling_Client_Recommendation>`_

-  `WorldWind TileService <http://www.worldwindcentral.com/wiki/TileService>`_

-  `TMS 사양 <http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification>`_

-  `OnEarth 타일화 WMS 사양 <http://web.archive.org/web/20130511182803/http://onearth.jpl.nasa.gov/tiled.html>`_

-  `ArcGIS 서버 REST API <http://resources.arcgis.com/en/help/rest/apiref/>`_

-  :ref:`raster.wmts` 드라이버

