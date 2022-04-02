.. _raster.wmts:

================================================================================
WMTS -- OGC 웹 맵 타일 서비스
================================================================================

.. shortname:: WMTS

.. versionadded:: 2.1

.. build_dependencies:: libcurl

GDAL WMTS 클라이언트 드라이버로 WMTS 레이어에 접근할 수 있습니다. (cURL을 지원해야 합니다.)
RESTful 및 KVP 프로토콜 둘 다 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

열기 문법
-----------

WMTS 드라이버는 다음을 열 수 있습니다:

-  로컬 서비스 설명 XML 파일, 이 파일의 문법은 아래에서 설명합니다:

   ::

      gdalinfo gdal_wmts.xml

-  파일명으로 제공되는 설명 XML 파일의 내용:

   ::

      gdalinfo "<GDAL_WMTS><GetCapabilitiesUrl>http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml</GetCapabilitiesUrl><Layer>lb</Layer></GDAL_WMTS>"

-  WMTS 서비스의 로컬 GetCapabilities 응답:

   ::

      gdalinfo WMTSCapabilities.xml

-  WMTS 서비스의 GetCapabilitiesthe 응답을 가리키는 URL:

   ::

      gdalinfo "http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml"

-  *WMS:* 접두어가 붙고 선택적인 layer, tilematrixset, tilematrix/zoom_level, style 및 extendbeyonddateline 파라미터를 가지고 있을 수도 있는 WMTS 서비스의 GetCapabilitiesthe 응답을 가리키는 URL

   문법: *WMTS:url[,layer=layer_id][,tilematrixset=tms_id][,tilematrix=tm_id|,zoom_level=level][,style=style_id][,extendbeyonddateline=yes/no]*

   ::

      gdalinfo "WMTS:http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml"

   ::

      gdalinfo "WMTS:http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml,layer=lb"

-  *WMS:* 접두어가 붙은 열기 옵션:

   ::

      gdalinfo WMTS: -oo URL=http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml -oo LAYER=lb

이 모든 문법들에서, 레이어 여러 개를 표현하는 데 레이어 파라미터 또는 열기 옵션으로 레이어를 명확하게 정의하지 않는 경우 또는 레이어가 스타일 또는 타일 행렬 집합을 하나 이상 가지고 있는 경우, 하위 데이터셋 목록을 반환할 것입니다. 레이어가 하나인 경우 기본 스타일로 레이어를 열고 첫 번째 타일 행렬 집합을 목록화할 것입니다.

열기 옵션
------------

다음과 같은 열기 옵션을 사용할 수 있습니다:

- **URL**:
  GetCapabilities 응답 문서를 가리키는 URL(또는 로컬 파일의 파일명)입니다. 연결 문자열에 지정되지 않은 경우 (예를 들어 "WMTS:"만 사용하는 경우) 필수입니다.

- **LAYER**:
  레이어 식별자입니다.

- **TILEMATRIXSET**:
  타일 행렬 집합의 식별자입니다. 이 식별자는 레이어를 노출시킬 좌표계를 결정합니다. 레이어에 목록화된 타일 행렬 가운데 하나여야만 합니다.

- **TILEMATRIX**:
  타일 행렬의 식별자입니다. 레이어에 대해 선택한 타일 행렬 집합의 목록화된 타일 행렬 가운데 하나여야만 합니다. ZOOM_LEVEL과 함께 사용할 수 없습니다. 지정하지 않는 경우 마지막 타일 행렬, 예를 들면 최고 해상도를 가진 타일 행렬을 선택합니다.

- **ZOOM_LEVEL**:
  전체 해상도 GDAL 래스터셋에 사용할 최고 확대/축소 수준 타일 행렬의 색인입니다. (더 낮은 확대/축소 수준들은 오버뷰에 사용될 것입니다.) 첫 번째 행렬은 (즉 최저 해상도 행렬 가운데 하나는) 0으로 색인됩니다. TILEMATRIX와 함께 사용할 수 없습니다. 지정하지 않는 경우 마지막 타일 행렬, 즉 최고 해상도를 가진 행렬을 선택합니다.

- **STYLE**:
  스타일 식별자입니다. 레이어의 스타일 식별자 가운데 하나여야만 합니다.

- **EXTENDBEYONDDATELINE=YES/NO**:
  범위가 날짜 변경선(date line)을 넘도록 해서 타일 요청을 왜곡(warp)시킬지 여부를 선택합니다. 자세한 내용은 아래에서 설명하는 로컬 서비스 설명 XML 파일의 ExtendBeyondDateLine 파라미터를 참조하십시오.

- **EXTENT_METHOD=AUTO/LAYER_BBOX/TILE_MATRIX_SET/MOST_PRECISE_TILE_MATRIX**:
  GDAL은 레이어의 범위를 가져와야 합니다. 
  레이어 수준에서의 WGS84BoundingBox 요소, 레이어 수준에서 좌표계 여러 개를 가지고 있을 수도 있는 BoundingBox 요소, 모든 레이어가 공유하는 TileMatrixSet 정의의 BoundingBox, 그리고 레이어 수준에서의 TileMatrixSet 정의 등 서로 다른 소스로부터 가져올 수 있습니다.
  기본적으로 (AUTO) GDAL은 먼저 선택한 TileMatrixSet이 나타내는 좌표계에 대응하는 WGS84BoundingBox/BoundingBox를 시도할 것입니다. 이를 사용할 수 없는 경우, 또다른 좌표계를 사용하는 BoundingBox로 돌아가서 선택한 좌표계로 재투영할 것입니다. 그럴 수 없다면, 선택한 TileMatrixSet에서 가장 정밀한 타일 행렬로 돌아가서 레이어의 TileMatrixLimit의 가장 정밀한 확대/축소 수준이 나타내는 경계 상자로 잘라낼 것입니다.
  LAYER_BBOX를 지정하는 경우, WGS84BoundingBox/BoundingBox 요소들만 고려합니다.
  TILE_MATRIX_SET을 지정하면, 선택한 TileMatrixSet의 BoundingBox 요소를 사용할 것입니다.
  MOST_PRECISE_TILE_MATRIX를 지정하는 경우, 가장 정밀한 타일 행렬이 나타내는 범위를 사용할 것입니다.

- **CLIP_EXTENT_WITH_MOST_PRECISE_TILE_MATRIX=YES/NO**: (GDAL 3.4.2 이상 버전)
  가장 정밀한 TileMatrix가 나타내는 범위를 이용해서 레이어 범위를 잘라낼지 여부를 선택합니다.
  (레이어 경계 상자를 사용하는 경우 기본값은 NO이고, 그렇지 않은 경우 YES입니다.)

- **CLIP_EXTENT_WITH_MOST_PRECISE_TILE_MATRIX_LIMITS=YES/NO**: (GDAL 3.4.2 이상 버전)
  가장 정밀한 TileMatrixLimit가 나타내는 범위를 이용해서 레이어 범위를 잘라낼지 여부를 선택합니다.
  (레이어 경계 상자를 사용하는 경우 기본값은 NO이고, 그렇지 않은 경우 YES입니다.)

로컬 서비스 설명 XML 파일
----------------------------------

``<GDAL_WMTS>`` 요소 앞에 어떤 공백이나 다른 내용도 없다는 사실이 중요합니다.

.. list-table:: Local Service Description XML File for WMTS
   :header-rows: 0

   * - <GDAL_WMTS>
     - 
   * - <GetCapabilitiesUrl>http://foo/WMTSCapabilities.xml</GetCapabilitiesUrl>
     - GetCapabilities 응답 문서를 가리키는 URL(또는 로컬 파일의 파일명)입니다. (필수) KVP 전용 서버의 경우, http://end_point?SERVICE=WMTS&amp;REQUEST=GetCapabilities 같은 서식일 것입니다.
   * - <Layer>layer_id</Layer>
     - 레이어 식별자입니다. (선택적이지만 레이어 여러 개를 명확하게 구분하기 위해 필요할 수도 있습니다.)
   * - <Style>style_id</Style>
     - 스타일 식별자입니다. 레이어에 목록화된 스타일 식별자 가운데 하나여야만 합니다. (선택적이지만 스타일 여러 개를 명확하게 구분하기 위해 필요할 수도 있습니다.)
   * - <TileMatrixSet>tile_matrix_set_id</TileMatrixSet>
     - 타일 행렬 집합 식별자입니다. 레이어에 목록화된 타일 행렬 집합 식별자 가운데 하나여야만 합니다. (선택적이지만 타일 행렬 집합 여러 개를 명확하게 구분하기 위해 필요할 수도 있습니다.)
   * - <TileMatrix>tile_matrix_id</TileMatrix>
     - 타일 행렬 식별자입니다. 레이어에서 선택한 타일 행렬 집합의 목록화된 타일 행렬 식별자 가운데 하나여야만 합니다. (GDAL 2.2 이상 버전에서 선택적입니다. ZoomLevel과 함께 사용할 수 없습니다. 지정하지 않는 경우 마지막 타일 행렬, 즉 최고 해상도를 가진 행렬을 선택합니다.)
   * - <ZoomLevel>int_value</ZoomLevel>
     - 최고 확대/축소 수준 타일 행렬의 색인입니다. 첫 번째 행렬은 (즉 최저 해상도 행렬 가운데 하나는) 0으로 색인됩니다. (GDAL 2.2 이상 버전에서 선택적입니다. TileMatrix와 함께 사용할 수 없습니다. 지정하지 않는 경우 마지막 타일 행렬, 즉 최고 해상도를 가진 행렬을 선택합니다.)
   * - <Format>image/png</Format>
     - GetTile 요청이 사용하는 타일 포맷입니다. 레이어에 목록화된 포맷 가운데 하나여야만 합니다. (선택적이지만 포맷 여러 개를 명확하게 구분하기 위해 필요할 수도 있습니다.)
   * - <InfoFormat>application/xml</InfoFormat>
     - GetFeatureInfo 요청이 사용하는 정보 서식입니다. 레이어에 목록화된 정보 서식 가운데 하나여야만 합니다. (선택적이지만 InfoFormat 여러 개를 명확하게 구분하기 위해 필요할 수도 있습니다.)
   * - <DataWindow>
     - 데이터 범위를 정의합니다. (선택적, 지정하지 않는 경우 드라이버가 레이어의 선언된 범위를 쿼리하고 선언된 범위가 없다면 잠재적인 타일 행렬 집합 제한을 연산에 넣고 선택한 타일 행렬 집합의 범위로 돌아갈 것입니다.)
   * - <UpperLeftX>-180.0</UpperLeftX>
     - 좌상단 모서리의 타일 행렬 집합의 공간 좌표계 단위 X (경도/편동) 좌표입니다. (DataWindow가 존재하는 경우 필수)
   * - <UpperLeftY>90.0</UpperLeftY>
     - 좌상단 모서리의 타일 행렬 집합의 공간 좌표계 단위 Y (위도/편북) 좌표입니다. (DataWindow가 존재하는 경우 필수)
   * - <LowerRightX>180.0</LowerRightX>
     - 우하단 모서리의 타일 행렬 집합의 공간 좌표계 단위 X (경도/편동) 좌표입니다. (DataWindow가 존재하는 경우 필수)
   * - <LowerRightY>-90.0</LowerRightY>
     - 우하단 모서리의 타일 행렬 집합의 공간 좌표계 단위 Y (위도/편북) 좌표입니다. (DataWindow가 존재하는 경우 필수)
   * - </DataWindow>
     - 
   * - <Projection>EPSG:4326</Projection>
     - TileMatrixSet 가운데 하나가 바람직하지 않은 경우 선언되는 투영법입니다. (선택적, 기본값은 TileMatrixSet의 값)
   * - <BandsCount>4</BandsCount>
     - 밴드/채널 개수입니다. 1은 회색조 데이터, 3은 RGB, 4는 RGBA입니다. (선택적, 기본값은 4)
   * - <DataType>Byte</DataType>
     - 밴드 데이터 유형입니다. Byte, Int16, UInt16, Int32, UInt32, Float32, Float64 등등 가운데 하나로 설정할 수 있습니다. (선택적, 기본값은 Byte)
   * - <ExtendBeyondDateLine>false</ExtendBeyondDateLine>
     - 범위가 날짜 변경선(date line)을 넘도록 해서 타일 요청을 왜곡(warp)시킬지 여부를 선택합니다. 다음 두 가지 조건을 만족하는 경우에만 사용할 수 있습니다. (선택적, 기본값은 거짓)

          - 측지 공간 좌표계 또는 EPSG:3857의 경우, 경도 전체 범위 [-180,18]가 정수 개수의 타일로 완전히 덮혀 있는 타일 행렬 집합이어야 한다. (예: GoogleMapsCompatible)
          - **그리고**
          
              - 타일 행렬 집합의 공간 좌표계 단위로 된 레이어 BoundingBox가 경도 전체 범위 [-180,18]를 덮고 있고, 경도 180도 주변에 중심을 둔 또다른 공간 좌표계 단위로 된 또다른 BoundingBox가 있어야 한다. GetCapabilities 문서에 이런 대체 BoundingBox가 없는 경우, DataWindow를 명확하게 지정해야 한다.
              - **또는** 타일 행렬 집합의 공간 좌표계 단위로 된 레이어 BoundingBox가 날짜 변경선을 넘어서야 한다.
   * - <Cache>
     - 로컬 디스크 캐시를 활성화합니다. 오프라인 작업 시 사용할 수 있습니다. (선택적, 이 요소가 없는 경우 비활성화, 그러나 자동 생성 XML 파일에 존재, GDAL_ENABLE_WMS_CACHE=NO 환경설정 옵션으로 무시 가능)
   * - <Path>./gdalwmscache</Path>
     - 캐시 파일을 저장할 위치입니다. 서로 다른 데이터소스에 동일한 캐시 경로를 사용하는 편이 안전합니다. (선택적, GDAL_DEFAULT_WMS_CACHE_PATH 환경설정 옵션을 지정하지 않은 경우 기본값은 ./gdalwmscache) 임시 인메모리 캐시를 사용할 수 있게 해주는 /vsimem/ 경로를 지원합니다.
   * - <Type>file</Type>
     - 캐시 유형입니다. 현재 'file' 유형만 지원합니다. 'file' 캐시 유형은 파일 시스템 폴더에 파일을 저장합니다. (선택적, 기본값은 'file')
   * - <Depth>2</Depth>
     - 디렉터리 레이어의 개수입니다. 2로 설정하면 파일을 cache_path/A/B/ABCDEF... 로 작성할 것입니다. (선택적, 기본값은 2)
   * - <Extension>.jpg</Extension>
     - 캐시 파일에 추가할 확장자입니다. (선택적, 기본값은 없음)
   * - </Cache>
     - 
   * - <MaxConnections>2</MaxConnections>
     - 최대 동시 연결 개수입니다. (선택적, 기본값은 2)
   * - <Timeout>300</Timeout>
     - 초 단위 연결 제한 시간입니다. (선택적, 기본값은 300)
   * - <OfflineMode>true</OfflineMode>
     - 어떤 새 이미지도 다운로드하지 않고, 캐시에 있는 이미지만 사용합니다. 캐시를 활성화한 경우에만 유용합니다. (선택적, 기본값은 거짓)
   * - <UserAgent>GDAL WMS driver (http://www.gdal.org/frmt_wms.html)</UserAgent>
     - HTTP 사용자 에이전트(user agent) 문자열입니다. 일부 서버는 "Mozilla/5.0" 같은 잘 알려진 사용자 에이전트를 요구할 수도 있습니다. (선택적, 기본값은 "GDAL WMS driver (http://www.gdal.org/frmt_wms.html)")
   * - <UserPwd>user:password</UserPwd>
     - HTTP 인증 용 사용자 ID 및 비밀번호입니다. (선택적)
   * - <UnsafeSSL>true</UnsafeSSL>
     - SSL 인증서 검증을 건너뜁니다. 서버가 자체 서명한 인증서를 사용하는 경우 필요할 수도 있습니다. (선택적, 기본값은 거짓, 그러나 자동 생성 XML에서는 참으로 설정)
   * - <Referer>http://example.foo/</Referer>
     - HTTP 리퍼러(HTTP Referer) 문자열입니다. 일부 서버가 요구할 수도 있습니다. (선택적)
   * - <ZeroBlockHttpCodes>204,404</ZeroBlockHttpCodes>
     - 요청 중단 대신 0으로 채워진 이미지로 (예를 들어 3밴드의 경우 검은색, 4밴드의 경우 투명으로) 해석될, 쉼표로 구분된 HTTP 응답 코드 목록입니다. (선택적, 기본값은 설정하지 않음, 그러나 자동 생성 XML에서는 204,204로 설정)
   * - <ZeroBlockOnServerException>true</ZeroBlockOnServerException>
     - 서버가 반환한 서비스 예외(Service Exception)를 요청 중단 대신 0으로 채워진 이미지로 취급할지 여부를 선택합니다. (선택적, 기본값은 거짓, 그러나 자동 생성 XML에서는 참으로 설정)
   * - </GDAL_WMTS>
     - 

GDAL 2.3버전부터, GDAL_HTTP_HEADER_FILE 환경설정 옵션이 "key: value" HTTP 헤더를 가지고 있는 텍스트 파일의 파일명을 가리키도록 설정하면 추가적인 HTTP 헤더를 전송할 수 있습니다.

GetFeatureInfo 요청
----------------------

gdallocationinfo 유틸리티를 (GetFeatureInfo 요청을 통해) 이용하면, 또는 밴드 객체에 GetMetadataItem("Pixel_iCol_iLine", "LocationInfo")를 호출하면 WMTS 레이어를 쿼리할 수 있습니다.

::

   gdallocationinfo my_wmts.xml -geoloc -11547071.455 5528616 -xml -b 1

WMTS 서비스 설명 XML 파일 생성
-----------------------------------------------

WMTS 서비스 설명 XML 파일을 직접 생성할 수도, 또는 소스 데이터셋 자체가 WMTS 데이터셋인 경우에만 WMTS 드라이버의 CreateCopy() 작업의 산출물로 생성할 수도 있습니다. 그렇지 않은 경우, 앞의 "열기 문법"에서 언급된 문법 아무거나 gdal_translate의 소스 데이터셋으로 사용해서 XML 파일을 산출할 수도 있습니다. 다음은 그 예시입니다:

::

   gdal_translate "WMTS:http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml,layer=lb" wmts.xml -of WMTS

다음 파일을 생성합니다:

.. code-block:: xml

   <GDAL_WMTS>
     <GetCapabilitiesUrl>http://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities.xml</GetCapabilitiesUrl>
     <Layer>lb</Layer>
     <Style>farbe</Style>
     <TileMatrixSet>google3857</TileMatrixSet>
     <DataWindow>
       <UpperLeftX>1800035.8827671</UpperLeftX>
       <UpperLeftY>6161931.622311067</UpperLeftY>
       <LowerRightX>1845677.148953537</LowerRightX>
       <LowerRightY>6123507.385072636</LowerRightY>
     </DataWindow>
     <BandsCount>4</BandsCount>
     <Cache />
     <UnsafeSSL>true</UnsafeSSL>
     <ZeroBlockHttpCodes>404</ZeroBlockHttpCodes>
     <ZeroBlockOnServerException>true</ZeroBlockOnServerException>
   </GDAL_WMTS>

이렇게 생성된 파일은 사용자가 편집해야 할 수도 있는 기본값을 가질 것입니다.

참고
--------

-  `OGC WMTS 표준 <http://www.opengeospatial.org/standards/wmts>`_

-  :ref:`raster.wms` 드라이버

