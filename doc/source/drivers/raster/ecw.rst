.. _raster.ecw:

================================================================================
ECW -- 향상된 압축 웨이블릿 (.ecw)
================================================================================

.. shortname:: ECW

.. build_dependencies:: ECW SDK

GDAL은 헥사곤 지오스페이셜(Hexagon Geospatial; 예전의 Intergraph, ERDAS, ERMapper) 사가 개발한 ERDAS ECW/JP2 SDK를 이용해서 ECW 읽기와 쓰기를 지원합니다. 이 지원은 선택 옵션으로 ECW/JP2 SDK 다운로드 페이지에서 사용할 수 있는 라이브러리들과 링크해야 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

사용 허가
---------

여러 사용 허가(license) 유형 아래 ERDAS ECW/JP2 SDK v5.x버전을 사용할 수 있습니다. 데스크톱 사용의 경우, 모든 크기의 ECW/JP2 이미지 디코딩을 무료로 사용할 수 있습니다. 서버 플랫폼에서 배포하기 위해 압축하거나, 또는 모바일 플랫폼 상에서 무제한 크기의 파일을 디코딩하려면 헥사곤 지오스페이셜 사로부터 사용 권한을 구매해야만 합니다.

이력
-------

-  v3.x - 2006년 배포 중지
-  v4.x - 2012년 배포 중지
-  v5.x - 2013년~현재 개발 중

생성 옵션
----------------

ERDAS ECW/JP2 v4.x 및 v5.x SDK는 이미지 압축 해제에 대해서만 무료로 사용할 수 있습니다. 이미지를 압축하려면 읽기/쓰기 SDK로 빌드하고 런타임(runtime)에 ERDAS로부터 구매해야 할 수도 있는 OEM 사용 권한 키를 입력해야 합니다.

아직도 ECW 3.3 SDK를 사용하고 있다면, 500MB 미만 이미지는 무료로 압축할 수도 있지만 용량이 그 이상인 이미지는 ERDAS로부터 사용 권한을 구매해야 합니다. 사용 허가 계약서와 LARGE_OK 옵션을 참조하십시오.

ECW 포맷으로 압축할 파일은 최소한 128x128 크기여야만 합니다. ECW 버전 2 파일의 경우, ECW는 현재 채널 당 8비트만 지원합니다. ECW 버전 3 파일은 채널당 16비트를 (Uint16 데이터 유형으로) 지원합니다. ECW 버전 3 파일 쓰기를 활성화하려면 생성 옵션들을 읽어보십시오.

ECW 파일에 좌표계 정보를 작성할 때, 덜 흔한 좌표계들은 많은 경우 제대로 매핑되지 않습니다. 사용자가 좌표계 용 ECW 이름을 알고 있다면 생성 시 PROJ 및 DATUM 생성 옵션으로 해당 좌표계를 강제로 설정할 수 있습니다.

ECW 포맷이 이미 "임의의(arbitrary) 오버뷰"에 대해 최적화되어 있다고 간주되기 때문에, ECW 포맷은 오버뷰 생성을 지원하지 않습니다.

.. _creation-options-1:

생성 옵션들:
~~~~~~~~~~~~~~~~~

-  **LARGE_OK=YES**: *(v3.x SDK 전용)* EULA 조건에 부합되는 경우 500MB를 초과하는 파일을 압축할 수 있습니다. v4.x부터 퇴출되었고, ECW_ENCODE_KEY와 ECW_ENCODE_COMPANY로 대체되었습니다.
-  **ECW_ENCODE_KEY=key**: *(v4.x SDK 이상)* 사용 허가된 기가픽셀 제한까지의 인코딩 케이퍼빌리티를 활성화하기 위한 OEM 인코딩 키를 입력합니다. 이 키의 길이는 약 129개의 16진법 자릿수입니다. 사용 권한을 구매한 회사와 키가 일치해야만 하며, SDK 버전이 오를 때마다 키를 재생성해야만 합니다. 환경설정 옵션으로 전체 수준에서 입력할 수도 있습니다.
-  **ECW_ENCODE_COMPANY=name**: *(v4.x SDK 이상)* 발행된 OEM 키(ECW_ENCODE_KEY 참조)에 있는 회사명을 입력합니다. 사용 권한을 구매한 회사와 키가 일치해야만 하며, SDK 버전이 오를 때마다 키를 재생성해야만 합니다. 환경설정 옵션으로 전체 수준에서 입력할 수도 있습니다.
-  **TARGET=percent**: 대상 크기 감소를 원본의 백분율로 설정합니다. 지정하지 않는 경우 기본값은 회색조 이미지의 경우 90%, RGB 이미지의 경우 95%입니다.
-  **PROJ=name**: 사용할 ECW 투영법 문자열의 이름입니다. 흔히 쓰이는 값으로는 NUTM11 또는 GEODETIC 등이 있습니다.
-  **DATUM=name**: 사용할 ECW 원점(datum) 문자열의 이름입니다. 흔히 쓰이는 값으로는 WGS84 또는 NAD83 등이 있습니다.
-  **UNITS=name**: 사용할 ECW 투영법 단위의 이름입니다. METERS(기본값) 또는 FEET(미국 피트)를 지정할 수 있습니다.
-  **ECW_FORMAT_VERSION=2/3**: ECW 5.x SDK로 빌드하는 경우 이 옵션을 설정하면 ECW 버전 3 파일을 생성할 수 있습니다. 가장 광범위한 호환성을 얻기 위해, 기본값은 2입니다.

환경설정 옵션
---------------------

ERDAS ECW SDK는 여러 객체들을 제어하기 위해 다양한 `런타임 환경설정 옵션 <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 을 지원합니다. 이런 옵션들 대부분은 GDAL 환경설정 옵션으로 노출됩니다. 이 옵션들의 의미를 완전하게 알고 싶다면 ECW SDK 문서를 읽어보십시오.

-  **ECW_CACHE_MAXMEM=bytes**: 인메모리(in-memory) 캐시 작업에 쓰이는 RAM의 최대 바이트를 설정합니다. 설정하지 않는 경우, SDK가 인메모리 캐시 작업을 위해 물리적 RAM의 1/4까지 사용할 것입니다.
-  **ECWP_CACHE_LOCATION=path**: ECWP의 결과물을 캐시하기 위해 사용하는 디렉터리를 가리키는 경로를 설정합니다. 설정하지 않는 경우 ECWP 캐시 작업이 활성화되지 않을 것입니다.
-  **ECWP_CACHE_SIZE_MB=number_of_megabytes**: ECWP의 결과물을 캐시하기 위해 사용하는 ECWP_CACHE_LOCATION의 용량의 최대 메가바이트 수를 설정합니다.
-  **ECWP_BLOCKING_TIME_MS**: ecwp:// 프로토콜의 블록 작업 읽기(blocking read)가 반환하기 전에 대기할 시간을 설정합니다. 기본값은 10,000밀리초입니다.
-  **ECWP_REFRESH_TIME_MS**: 블록이 도착하는 시간과 다음 새로고침 콜백 사이의 시간 지연을 설정합니다. 기본값은 10,000밀리초입니다. GDAL의 목적 상, 이 값은 드라이버가 최종 결과물이 아직 반환되지 않은 ECWP 연결 상에서 더 많은 데이터를 받기 위해 대기할 시간입니다. RasterIO() 요청 미만으로 설정하면 결과물의 해상도가 저하되는 경우가 많습니다.
-  **ECW_TEXTURE_DITHER=TRUE/FALSE**: ECW 파일 압축 해제 시 디더링을 비활성화하려면 이 옵션을 FALSE로 설정할 수도 있습니다. 기본값은 TRUE입니다.
-  **ECW_FORCE_FILE_REOPEN=TRUE/FALSE**: 각 연결이 생성될 때마다 각 파일에 대해 파일 핸들(file handle)을 강제로 열려면 이 옵션을 TRUE로 설정할 수도 있습니다. 기본값은 FALSE입니다.
-  **ECW_CACHE_MAXOPEN=number**: ECW 파일 핸들 캐시 작업을 위해 열고 있어야 하는 파일의 최대 개수를 설정합니다. 기본값은 무제한입니다.
-  **ECW_RESILIENT_DECODING=TRUE/FALSE**: 판독기가 파일에 있는 오류를 무시해야 하는지, 사용할 수 있는만큼 많은 데이터를 반환하려 해야 하는지 여부를 제어합니다. 기본값은 TRUE입니다. FALSE로 설정하면 무결하지 않은 파일이 오류를 발생시킬 것입니다.

GDAL 특화 옵션:

-  **ECW_ALWAYS_UPWARD=TRUE/FALSE**: TRUE로 설정하는 경우, 이 드라이버는 음의 Y 해상도 값을 설정하고 이미지가 항상 "Upward" 방향이라고 (Y좌표가 위쪽으로 증가한다고) 가정합니다. 드라이버가 "Downward" 방향을 가진 (Y좌표가 아래쪽으로 증가하며 Y 해상도가 양의 값인) 드문 이미지를 정확히 처리할 수 있도록 하기 위해 이미지의 Y 해상도 (부호) 값을 이용해서 실제 이미지 방향을 의존하도록 하려면 FALSE로 설정할 수도 있습니다. 기본값은 TRUE입니다.

ECW 버전 3 파일
~~~~~~~~~~~~~~~~~~~

ECW 5.x SDK는 다음과 같은 새 파일 포맷을 도입했습니다:

#. 파일 헤더 안에 데이터 통계, 히스토그램, 메타데이터, RPC 정보를 저장
#. UInt16 데이터 유형 지원
#. 기존 ECW 버전 3 파일 내에서 영역(region)을 업데이트할 수 있는 기능
#. 용량을 절약하기 위한 다른 최적화 기술 도입

주의: 이 버전은 하위 호환되지 않기 때문에 ECW/JP2 SDK의 v3.x 또는 v4.x에서 디코딩하는 경우 실패할 것입니다. 파일의 VERSION 메타데이터가 해당 파일이 ECW v2인지 ECW v3인지를 알려줄 것입니다.

ECWP
~~~~

이 드라이버는 로컬 파일뿐만 아니라 ERDAS APOLLO 상품의 상용 "ECWP" 프로토콜을 이용하는 스트리밍 네트워크 영상 서비스 접근도 지원합니다. ecwp://로 시작하는 전체 데이터셋 URL을 입력하면 됩니다. ECW/JP2 SDK v4.1 이상으로 빌드한 경우, ECWP 서비스에 비동기(asynchronous)/점진적(progressive) 스트리밍 접근하기 위해 :ref:`rfc-24` 도 활용할 수 있습니다.

메타데이터/지리참조
~~~~~~~~~~~~~~~~~~~~~~~~~

ECW 메타데이터 도메인에 ECW 헤더에서 찾은 PROJ, DATUM 및 UNITS를 리포트합니다. 기존 ECW 파일을 업데이트 모드로 열어서 영상을 수정하는 일 없이 헤더 정보만 업데이트하려면 이 메타데이터들을 SetMetadataItem() 메소드로 설정하면 됩니다.

지리변형 및 투영법도 SetGeoTransform() 및 SetProjection() 메소드로 수정할 수 있습니다. 투영법을 SetProjection()으로 설정하고 PROJ, DATUM 또는 UNITS를 SetMetadataItem()으로 설정한 경우, 후자의 값이 투영법 문자열로부터 작성된 값을 무시할 것입니다.

`gdal_edit.py <gdal_edit.html>`_ 유틸리티의 -a_ullr, -a_srs 또는 -mo 스위치를 사용하면 이 모든 값들을 수정할 수 있습니다.

예시:

::

   gdal_edit.py -mo DATUM=WGS84 -mo PROJ=GEODETIC -a_ullr 7 47 8 46 test.ecw

   gdal_edit.py -a_srs EPSG:3068 -a_ullr 20800 22000 24000 19600 test.ecw

파일 메타데이터 키:
~~~~~~~~~~~~~~~~~~~

-  FILE_METADATA_ACQUISITION_DATE
-  FILE_METADATA_ACQUISITION_SENSOR_NAME
-  FILE_METADATA_ADDRESS
-  FILE_METADATA_AUTHOR
-  FILE_METADATA_CLASSIFICATION
-  FILE_METADATA_COMPANY - ECW_ENCODE_COMPANY로 설정해야 합니다.
-  FILE_METADATA_COMPRESSION_SOFTWARE - 재압축 과정에서 업데이트됩니다.
-  FILE_METADATA_COPYRIGHT
-  FILE_METADATA_EMAIL
-  FILE_METADATA_TELEPHONE
-  CLOCKWISE_ROTATION_DEG
-  COLORSPACE
-  COMPRESSION_DATE
-  COMPRESSION_RATE_ACTUAL
-  COMPRESSION_RATE_TARGET - 대상 압축 파일 용량을 비압축 파일 용량으로 나눈 백분율입니다. 이 값은 TARGET이 파일 생성 시 사용된 TARGET 생성 옵션의 값일 때 100 / (100 - TARGET) 과 동일합니다. 따라서 COMPRESSION_RATE_TARGET=1은 TARGET=0(예: 비압축)과 같고, COMPRESSION_RATE_TARGET=5는 TARGET=80(예: 비압축 파일 용량을 5로 나누기)과 같으며, ...
-  VERSION

참고
--------

-  ``gdal/frmts/ecw/ecwdataset.cpp`` 로 구현되었습니다.
-  `www.hexagongeospatial.com <http://hexagongeospatial.com/products/data-management-compression/ecw/erdas-ecw-jp2-sdk>`_ 에서 ECW/JP2 SDK를 다운로드할 수 있습니다.
-  `사용자 지침서 <http://hexagongeospatial.com/products/data-management-compression/ecw/erdas-ecw-jp2-sdk/literature>`_ 에서 상품 정보를 더 자세히 볼 수 있습니다.
-  GDAL 특화가 아닌 문제에 대한 지원을 받으려면 `헥사곤 지오스페이셜 공공 포럼 <https://sgisupport.intergraph.com/infocenter/index?page=forums&forum=507301383c17ef4e013d8dfa30c2007ef1>`_ 에 문의해보십시오.
-  `GDAL ECW 빌드 힌트 <http://trac.osgeo.org/gdal/wiki/ECW>`_
