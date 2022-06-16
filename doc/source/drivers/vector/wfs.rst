.. _vector.wfs:

WFS - OGC WFS 서비스
=====================

.. shortname:: WFS

.. build_dependencies:: libcurl

WFS 드라이버는 OGC WFS 서비스에 접속할 수 있습니다. 이 드라이버는 WFS 1.0, 1.1 및 2.0버전 프로토콜을 지원합니다. WFS 드라이버를 컴파일하기 위해서는 GDAL/OGR가 cURL 지원과 함께 빌드되어 있어야만 합니다. WFS 요청은 보통 결과물을 GML 포맷으로 반환하기 때문에, 일반적으로 읽기 지원을 위해 GML 드라이버를 설정해줘야 합니다. (따라서 GDAL/OGR가 Xerces 또는 Expat 지원과 함께 빌드되어 있어야 합니다.) 서버가 ("OUTPUTFORMAT=json"처럼) 대체 기저 포맷을 지원하는 경우 대체 포맷을 사용할 수도 있습니다.

이 드라이버는 읽기 전용 서비스는 물론 트랜잭션 서비스(WFS-T)도 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

WFS 데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   WFS:http://path/to/WFS/service
   
   또는
   
   http://path/to/WFS/service?SERVICE=WFS

WFS 사양에 지정된 대로 *TYPENAME*, *VERSION*, *MAXFEATURES* (WFS 2 미만 버전) or *COUNT* (WFS 2 이상 버전) 같은 선택적인 추가 파라미터를 지정할 수 있습니다.

TYPENAME 파라미터에 설정하는 이름이 OGR가 리포트한 레이어 이름 그대로여야만 합니다. 특히 이름공간(namespace) 접두어가 존재하는 경우 이름 앞에 이름공간 접두어를 붙여야 합니다.
주의: 유형 이름을 쉼표로 구분해서 여러 개 설정할 수 있습니다.

다음과 같은 문법을 따르는 내용을 가진 XML 파일의 이름도 지정할 수 있습니다(<OGRWFSDataSource> 요소가 파일의 첫 바이트여야만 합니다):

::

   <OGRWFSDataSource>
       <URL>http://path/to/WFS/service[?OPTIONAL_PARAMETER1=VALUE[&amp;OPTIONAL_PARAMETER2=VALUE]]</URL>
   </OGRWFSDataSource>

주의: URL을 XML 이스케이프 처리해야만 합니다. 예를 들면 '&' 문자를 '&amp;'로 작성해야만 합니다.

데이터셋을 처음 열 때, 나중에 해당 데이터셋을 다시 열 때 캐시로 불러올 수 있도록 파일에 *GetCapabilities* 요청 결과의 내용을 추가할 것입니다. 각 레이어의 필드 정의를 찾기 위해 발행하는 *DescribeFeatureType* 요청도 마찬가지입니다.

서비스 설명 파일은 ``OGRWFSDataSource`` 요소의 직계 하위 요소로 선택적으로 설정할 수도 있는 다음 추가 요소들을 가집니다:

-  **Timeout**:
   원격 서비스 요청에 사용할 제한 시간입니다. 이 요소를 지정하지 않는 경우, libcurl 기본값을 사용합니다.

-  **UserPwd**:
   원격 서버에 사용자 ID와 비밀번호를 전송하기 위해 *userid:password* 를 지정할 수도 있습니다.

-  **HttpAuth**:
   사용할 인증 스키마를 제어하기 위해 BASIC, NTLM 또는 ANY로 설정할 수도 있습니다.

-  **Version**:
   사용할 특정 WFS 버전을 (1.0.0 또는 1.1.0 가운데 하나로) 설정합니다.

-  **PagingAllowed**:
   페이지 작업을 활성화해야만 하는 경우 ON으로 설정합니다. "페이지 작업 요청" 단락을 참조하십시오.

-  **PageSize**:
   페이지 작업을 활성화한 경우 페이지 용량을 지정합니다. "페이지 작업 요청" 단락을 참조하십시오.

-  **BaseStartIndex**:
   페이지 작업을 활성화한 경우 색인 시작 번호를 (0 또는 1 가운데 하나로) 설정합니다. "페이지 작업 요청" 단락을 참조하십시오.

-  **COOKIE**:
   HTTP 요청에 전송되는 HTTP 쿠키로, 서식은 ``COOKIE1=VALUE1; COOKIE2=VALUE2; ...`` 입니다.
   GDAL 2.3버전부터, :decl_configoption:`GDAL_HTTP_HEADER_FILE` 환경설정 옵션을 "key: value" HTTP 헤더를 가진 텍스트 파일의 파일명을 가리키도록 설정하면 추가 HTTP 헤더를 전송할 수 있습니다.

페이지 작업 요청
--------------

WFS 드라이버는 GML 콘텐츠를 전체 파일이 아니라 스트림으로 읽어올 것입니다. 이렇게 하면 상호작용성을 향상시키고 콘텐츠 용량이 메모리 용량을 넘어서는 경우 도움이 될 것입니다. 스트림으로 읽어오는 것이 적절하지 않은 경우 (예를 들면 메모리로 불러올 수 있는 레이어를 여러 번 반복해서 읽는 경우) :decl_configoption:`OGR_WFS_USE_STREAMING` 환경설정 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다. 스트리밍을 활성화하는 경우, GZip 압축도 필요합니다. 실시간(on-the-fly) 압축을 할 수 없는 일부 WFS 서버가 콘텐츠의 첫 바이트를 인터넷으로 전송하기 전에 전송할 서버 쪽 캐시에 콘텐츠 전체를 저장할 것이라는 사실이 관찰되었습니다. 이를 피하려면 :decl_configoption:`CPL_CURL_GZIP` 환경설정 옵션을 NO로 설정하면 됩니다.

WFS 2.0 페이지 작업
+++++++++++++++++++

WFS 드라이버는 WFS 2.0 서버에 요청할 때 서버가 페이지 작업을 지원하는지 자동 탐지할 것입니다. 서버가 달리 선언하지 않는다면 페이지 용량(단일 요청으로 가져오는 객체 개수)는 기본적으로 100개로 제한되어 있습니다. :decl_configoption:`OGR_WFS_PAGE_SIZE` 환경설정 옵션으로 또는 연결 문자열의 URL에 COUNT를 쿼리 파라미터로 설정해서 페이지 용량을 변경할 수 있습니다.

첫 N개의 객체만 다운로드하면 되기 때문에 레이어 전체를 페이지 작업하는 것은 바람직하지 않은 경우, :decl_configoption:`OGR_WFS_PAGING_ALLOWED` 환경설정 옵션을 OFF로 설정해야 합니다.

WFS 1.0 또는 1.1 페이지 작업
++++++++++++++++++++++++++

(MapServer 6.0 이상 버전 같은) 일부 서버는 "페이지"별로 요청을 발행할 수 있게 해주는, 즉 단일 요청으로 레이어의 전체 콘텐츠를 다운로드하는 일을 막아주는 STARTINDEX 사용을 지원합니다. WFS 2.0.0버전에서 페이지 작업이 도입되었지만 WFS 1.0.0 및 1.1.0버전에서도 판매자 특화 옵션으로 페이지 작업을 지원할 수도 있습니다. OGR WFS 클라이언트는 :decl_configoption:`OGR_WFS_PAGING_ALLOWED` 환경설정 옵션을 명확하게 ON으로 설정한 경우 페이지 작업을 이용할 것입니다. 서버가 달리 선언하지 않는다면 페이지 용량(단일 요청으로 가져오는 객체 개수)는 기본적으로 100개로 제한되어 있습니다. :decl_configoption:`OGR_WFS_PAGE_SIZE` 환경설정 옵션으로 페이지 용량을 변경할 수 있습니다.

WFS 2.0.2버전 사양은 페이지 작업의 첫 번째 객체가 색인 0번이라는 사실을 명확하게 하고 있습니다. 그러나 (MapServer 6.2 이상 버전을 포함하는) 일부 서버의 WFS 페이지 작업 구현은 첫 번째 객체가 색인 1번이라고 간주합니다. 기반 색인 시작 번호 기본값은 사양이 요구하는 대로 0입니다. 하지만 :decl_configoption:`OGR_WFS_BASE_START_INDEX` 환경설정 옵션을 1로 설정하면 첫 번째 객체가 색인 1번이라고 간주하는 서버 구현과 호환시킬 수 있습니다.

페이지 작업 옵션
++++++++++++++

WFS XML 설명 파일에 이 옵션 3개(:decl_configoption:`OGR_WFS_PAGING_ALLOWED`, :decl_configoption:`OGR_WFS_PAGE_SIZE`, :decl_configoption:`OGR_WFS_BASE_START_INDEX`)를 비슷한 이름의 요소들로 (PagingAllowed, PageSize, BaseStartIndex) 설정할 수 있습니다.

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. 가능한 경우 (OGR SQL 언어를 OGC 필터 설명으로 변환해서) :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 모든 속성 필터도 서버로 포워딩하기 위해 최선을 다할 것입니다. 속성 필터를 서버로 포워딩할 수 없는 경우, 클라이언트 쪽에서만 필터링 작업을 할 것입니다. 이 작업은 서버로부터 모든 객체를 가져와야 하기 때문에 느릴 수도 있습니다.

다음 공간 함수들을 사용할 수 있습니다:

-  공간 바이너리 서술(predicate) 함수 8개:
   
   -  **ST_Equals**
   -  **ST_Disjoint**
   -  **ST_Touches**
   -  **ST_Contains**
   -  **ST_IntersectsST_Within**
   -  **ST_Crosses**
   -  **ST_Overlaps**
   
   이 함수들은 도형 인자 2개를 입력받습니다. 이 인자는 일반적으로 도형 열 이름과 ST_MakeEnvelope 또는 ST_GeomFromText 함수로 작성된 일정한(constant) 도형입니다.

-  **ST_DWithin(geom1,geom2,distance_in_meters)**

-  **ST_Beyond(geom1,geom2,distance_in_meters)**

-  **ST_MakeEnvelope(xmin,ymin,xmax,ymax[,srs])**:
   엔벨로프(envelope)를 작성합니다. 'srs'는 정수(EPSG 코드) 또는 gml:Envelope의 'srsName' 속성으로 직접 설정된 문자열일 수 있습니다. GDAL이 필요한 축 뒤바꾸기를 처리하기 때문에, 좌표를 "네이티브 GIS 순서"로 (예를 들면 측지 좌표계의 경우 [위도,경도]로) 표현할 것입니다.

-  **ST_GeomFromText(wkt,[srs])**:
   도형의 WKT 표현으로부터 도형을 작성합니다.

이런 공간 함수들은 서버 쪽 필터로만 지원된다는 사실을 기억하십시오.

레이어 결합
-----------

결합(join)을 지원하는 WFS 2.0 서버의 경우, 결합을 수반하는 SELECT 문을 서버 쪽에서 실행합니다. 서버가 공간 결합을 지원한다면 앞에서 설명한 공간 함수를 이용해서 공간 결합을 수행할 수도 있습니다.

서버가 결합의 복잡성에 대해 설정한 제약 조건이 있을 수도 있습니다. OGR WFS 드라이버도 열을 -- 별명 및 유형 캐스트일 수도 있는 -- 열 이름으로 선택할 수 있지만 표현식으로는 선택할 수 없다는 제약 조건을 가지고 있습니다. ON 및 WHERE 절도 서버 쪽에서 평가해야만 하기 때문에, 예를 들어 OGR 특수 필드는 사용할 수 없습니다. ORDER BY 절을 지원하지만, 이때 필드가 기본(primary) 테이블에 속해 있어야만 합니다.

다음은 무결한 SELECT 문의 예시입니다:

::

   SELECT t1.id, t1.val1, t1.geom, t2.val1 FROM my_table AS t1 JOIN another_table AS t2 ON t1.id = t2.t1id

또는

::

   SELECT * FROM my_table AS t1 JOIN another_table AS t2 ON ST_Intersects(t1.geom, t2.geom)

쓰기 지원 / WFS-T
---------------------

WFS-T 프로토콜은 사용자가 객체 수준에서만 작업할 수 있게 해줍니다. 데이터소스, 레이어 또는 필드를 생성할 수는 없습니다.

데이터소스를 업데이트 모드로 열었을 때만 쓰기 지원이 활성화됩니다.

WFS 트랜잭션 서비스 작업과 OGR 개념을 다음과 같이 매핑합니다:

-  OGRFeature::CreateFeature() <==> WFS 삽입 작업
-  OGRFeature::SetFeature() <==> WFS 업데이트 작업
-  OGRFeature::DeleteFeature() <==> WFS 삭제 작업

현재 잠금(lock) 작업을 (LockFeature 서비스를) 사용할 수 없습니다.

염두에 둬야 할 조심할 점이 몇 개 있습니다. OGR 객체 ID(FID)는 정수형 기반 값인 반면, WFS/GML gml:id 속성은 문자열입니다. 따라서 이 두 값이 항상 일치할 수는 없습니다. WFS 드라이버는 객체의 gml:id 속성을 'gml_id' 필드로 노출시킵니다.

CreateFeature() 메소드로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR가 반환되는 gml:id를 가져와서 그에 맞춰 객체의 'gml_id' 필드를 설정할 것입니다. gml:id가 ``layer_name.numeric_value`` 형식인 경우 OGR FID도 설정하려 시도할 것입니다. 이 형식이 아닌 경우 FID를 설정되지 않은 기본값으로 내버려둘 것입니다.

SetFeature() 메소드로 기존 객체를 업데이트하는 경우, OGR FID 필드를 무시할 것입니다. 드라이버에 발행된 요청이 객체의 gml:id 필드의 값인 경우에만 연산에 넣을 것입니다. DeleteFeature() 메소드의 경우에도 마찬가지입니다.

쓰기 지원 및 OGR 트랜잭션
----------------------------------

앞의 작업들은 기본적으로 OGR API 호출과 동시에 서버로 발행됩니다. 하지만 수많은 클라이언트/서버 교환 때문에 수많은 명령어들이 전송되는 경우, 이 때문에 성능이 저하될 수도 있습니다.

이 작업들을 :cpp:func:`OGRLayer::StartTransaction` 및 :cpp:func:`OGRLayer::CommitTransaction` 사이에 넣을 수도 있습니다. 이렇게 하면 메모리에 작업을 저장한 다음 CommitTransaction() 호출 시에만 실행할 것입니다.

CreateFeature() 메소드의 문제점은 사용자가 삽입하는 객체에 어떤 gml:id가 할당될지 알 수 없다는 점입니다. 이 문제를 해결하기 위해 WFS 드라이버에 특수 SQL 선언문이 도입되었습니다. OGRDataSource::ExecuteSQL()을 통해 ``SELECT _LAST_INSERTED_FIDS_ FROM layer_name`` 명령어를 발행하면 (이때 layer_name을 실제 레이어 이름으로 대체하십시오) 마지막으로 커밋된 트랜잭션 도중 삽입된 객체의 개수만큼의 행들을 가진 레이어를 반환할 것입니다. 이 행들의 gml_id 속성값은 모두 동일할 것입니다.

주의: 현재 CreateFeature() 메소드만 OGR 트랜잭션 메커니즘을 사용합니다. 지금도 SetFeature() 및 DeleteFeature() 메소드는 즉시 발행될 것입니다.

특수 SQL 명령어
--------------------

OGRDataSource::ExecuteSQL()에 전송되는 다음 SQL/유사 SQL 명령어는 WFS 드라이버에 특화된 특수 SQL 명령어입니다:

-  ``DELETE FROM layer_name WHERE expression``:
   이 명령어는 WFS 삭제 작업으로 귀결될 것입니다. 객체 하나 또는 여러 개를 빠르게 삭제할 수 있는 방법이 될 수 있습니다. 특히 gml:id를 알고 있는 경우 OGRLayer::DeleteFeature() 메소드보다 더 빠른 대체제가 될 수 있지만, 서버로부터 객체를 가져오지 않습니다.

-  ``SELECT _LAST_INSERTED_FIDS_ FROM layer_name``:
   앞 문단을 참조하십시오.

현재 다른 모든 SQL 명령어는 일반 레이어가 처리할 것입니다. 즉 클라이언트 쪽에서만 처리됩니다. 서버 쪽 공간 및 속성 필터링은 반드시 SetSpatialFilter() 및 SetAttributeFilter() 인터페이스를 통해 수행되어야만 합니다.

특수 레이어: WFSLayerMetadata
--------------------------------

"WFSLayerMetadata"라는 "숨겨진" 레이어는 각 WFS 레이어에 대한 메타데이터를 가진 레코드로 채워져 있습니다.

각 레코드는 :cpp:func:`OGRLayer::GetCapabilities` 메소드가 반환하는 문서로부터 나온 "layer_name", "title" 및 "abstract" 필드를 담고 있습니다.

``OGRLayer::GetLayerByName("WFSLayerMetadata")`` 를 통해 해당 레이어를 반환합니다.

특수 레이어: WFSGetCapabilities
----------------------------------

"WFSGetCapabilities"라는 "숨겨진" 레이어는 :cpp:func:`OGRLayer::GetCapabilities` 요청의 원시(raw) XML 결과물로 채워져 있습니다.


``OGRLayer::GetLayerByName("WFSGetCapabilities")`` 를 통해 해당 레이어를 반환합니다.

열기 옵션
------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **URL=url**:
   WFS 서버 종단점(endpoint)을 가리키는 URL을 지정합니다. "WFS:" 문자열을 연결 문자열로 사용하는 경우 필수입니다.

-  **TRUST_CAPABILITIES_BOUNDS=YES/NO**:
   더 빠른 GetExtent() 런타임을 위해 :cpp:func:`OGRLayer::GetCapabilities` 응답에 선언된 레이어 범위를 신뢰할지 여부를 선택합니다. 기본값은 NO입니다.

-  **EMPTY_AS_NULL=YES/NO**:
   기본적으로 (EMPTY_AS_NULL=YES) 비어 있는 내용을 가진 필드를 비어 있는 문자열 대신 NULL이라고 리포트합니다. 이 습성은 아주 오래 전의 습성이지만, 응용 프로그램 스키마가 이런 필드를 필수라고 선언하는 경우 해당 필드를 NULL이 될 수 없다(not-nullable)고 선언하는 일을 막을 수 있습니다. 즉 비어 있는 문자열을 그대로 리포트할 뿐만 아니라 필수 필드를 NULL이 될 수 없다(not-nullable)고 리포트하게 하려면 이 옵션을 NO로 설정하면 됩니다.

-  **INVERT_AXIS_ORDER_IF_LAT_LONG=YES/NO**:
   공간 좌표계 및 좌표 순서를 일반적인 GIS 순서로 표현할지 여부를 선택합니다. 기본값은 YES입니다.

-  **CONSIDER_EPSG_AS_URN=YES/NO/AUTO**: Whether to
   EPSG:XXXX 같은 srsName이 EPSG 축 순서를 준수한다고 간주할지 여부를 선택합니다. 기본값은 AUTO입니다.

-  **EXPOSE_GML_ID=YES/NO**:
   GML 객체의 gml:id 속성을 gml_id OGR 필드로 노출시킬지 여부를 선택합니다. gml_id 필드를 숨기는 경우 WFS-T가 작동하지 않을 것이라는 사실을 기억하십시오. 기본값은 YES입니다.

예시
--------

-  WFS 서버의 유형을 목록화하기:

   ::

      ogrinfo -ro WFS:http://www2.dmsolutions.ca/cgi-bin/mswfs_gmap

-  XML 파일 캐시에 레이어 구조를 저장한 WFS 서버의 유형을 목록화하기:

   ::

      ogrinfo -ro mswfs_gmap.xml

-  'popplace' 레이어의 객체를 공간 필터링해서 목록화하기:

   ::

      ogrinfo -ro WFS:http://www2.dmsolutions.ca/cgi-bin/mswfs_gmap popplace -spat 0 0 2961766.250000 3798856.750000

-  'tows:world' 레이어로부터 gml:id가 "world.2"과 "world.3"인 객체를 가져오기:

   ::

      ogrinfo "WFS:http://www.tinyows.org/cgi-bin/tinyows" tows:world -ro -al -where "gml_id='world.2' or gml_id='world.3'"

-  레이어 메타데이터를 출력하기:

   ::

      ogrinfo -ro -al "WFS:http://v2.suite.opengeo.org/geoserver/ows" WFSLayerMetadata

참고
--------

-  `OGC WFS 표준 <http://www.opengeospatial.org/standards/wfs>`_
-  :ref:`GML <vector.gml>` 드라이버
-  :ref:`OGC API - 객체 <vector.oapif>` 드라이버

