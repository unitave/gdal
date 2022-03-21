.. _raster.jp2mrsid:

================================================================================
JP2MrSID -- MrSID SDK를 통한 JPEG2000
================================================================================

.. shortname:: JP2MrSID

.. build_dependencies:: MrSID SDK

MrSID DSDK로 JPEG2000 파일 포맷 읽기를 지원합니다.
MrSID ESDK로 JPEG2000 파일 포맷 쓰기도 지원합니다.

DSDK 및 ESDK 5.x 이상 버전에서만 JPEG2000 MrSID 지원을 사용할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

지리참조 작업
--------------

내부(GeoJP2 또는 GMLJP2 경계 상자), 월드 파일 .j2w/.wld 사이드카 파일, 또는 PAM(Persistent Auxiliary metadata) .aux.xml 사이드카 파일 등 서로 다른 소스들로부터 지리참조 정보를 얻을 수 있습니다. 기본적으로 PAM, GeoJP2, GMLJP2, WORLDFILE 순서대로 파일을 수집합니다. (첫 항목을 가장 우선합니다.)

GDAL 2.2버전부터, GDAL_GEOREF_SOURCES 환경설정 옵션으로 (또는 GEOREF_SOURCES 열기 옵션으로) 사용할 수 있는 소스와 그 우선 순위를 변경할 수 있습니다. 이 옵션의 값은 PAM, GEOJP2, GMLJP2, (GEOJP2, GMLJP2로 가는 단축 키인) INTERNAL, WORLDFILE, NONE이라는 키워드를 쉼표로 구분한 목록입니다. 목록의 첫 항목이 가장 우선되는 소스입니다. 목록에 없는 소스는 무시할 것입니다.

예를 들어 이 옵션을 "WORLDFILE,PAM,INTERNAL"로 설정하면 PAM이나 내부 JP2 경계 상자보다 잠재적인 월드 파일의 지리변형 행렬을 우선할 것입니다. "PAM,WORLDFILE,GEOJP2"로 설정하면 설정된 소스를 이용하고 GMLJP2 경계 상자는 무시할 것입니다.

생성 옵션
----------------

MrSID ESDK(5.x 이상 버전)를 소유하고 있다면, ESDK를 이용해서 JPEG2000 파일을 작성할 수 있습니다. 다음과 같은 생성 옵션들을 지원합니다:

-  **WORLDFILE=YES**:
   (.j2w 확장자를 가진) ESRI 월드 파일을 작성합니다.

-  **COMPRESSION=n**:
   원하는 압축률을 지정합니다. 0은 비손실 압축을 의미합니다. 20은 20:1 압축률을 의미할 것입니다. (이미지를 원본 용량의 1/20로 압축할 것입니다.)

-  **XMLPROFILE=[path to file]**:
   JPEG2000 인코딩 파라미터를 설정하는 데 사용할 수 있는 Extensis 특화 XML 프로파일을 가리키는 경로를 설정합니다. MrSID ESDK 또는 GeoExpress를 이용하거나, 다음 템플릿을 예시로 삼아 직접 입력해서 Extensis 특화 XML 프로파일을 생성할 수 있습니다:

   ::

      <?xml version="1.0"?>
      <Jp2Profile version="1.0">
        <Header>
          <name>Default</name>
          <description>Extensis preferred settings (20051216)</description>
        </Header>
        <Codestream>
          <layers>
            8
          </layers>
          <levels>
            99
          </levels>
          <tileSize>
            0 0
          </tileSize>
          <progressionOrder>
            RPCL
          </progressionOrder>
          <codeblockSize>
            64 64
          </codeblockSize>
          <pltMarkers>
            true
          </pltMarkers>
          <wavelet97>
            false
          </wavelet97>
          <precinctSize>
            256 256
          </precinctSize>
        </Codestream>
      </Jp2Profile>

참고
--------

-  ``gdal/frmts/mrsid/mrsiddataset.cpp`` 로 구현되었습니다.
-  `Extensis 웹사이트 <http://www.extensis.com/support/developers>`_
