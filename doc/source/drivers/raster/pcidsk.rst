.. _raster.pcidsk:

================================================================================
PCIDSK -- PCI 지리정보(Geomatics) 데이터베이스 파일
================================================================================

.. shortname:: PCIDSK

.. built_in_by_default::

PCI EASI/PACE 소프트웨어가 이미지 분석을 위해 PCIDSK 데이터베이스 파일을 사용합니다. GDAL은 PCIDSK 데이터베이스 파일의 읽기 및 쓰기를 지원합니다. 모든 픽셀 데이터 유형 및 데이터 구조(교차삽입된 픽셀, 교차삽입된 밴드, 교차삽입되고 타일화된 파일)을 지원할 것입니다. 현재 LUT 부분(segment)은 무시하지만, PCT 부분은 밴드와 관련된 것으로 취급할 것입니다. 대체로 파일 및 밴드 특화 메타데이터가 이미지 또는 밴드와 정확하게 연동될 것입니다.

지리참조 작업을 지원하지만, 원점(datum) 및 타원체 지원에 몇몇 제약이 있을 수도 있습니다. GCP 부분은 무시합니다. RPC 부분은 GDAL 스타일 RPC 메타데이터로 반환될 것입니다.

내부 (피라미드 구조) 오버뷰 이미지도 정확하게 읽어오지만, 새로 요청하는 오버뷰는 외부 .ovr 파일로 작성할 것입니다.

이 드라이버는 벡터 부분도 지원합니다.

생성 옵션
----------------

PCIDSK 파일은 항상 픽셀 교차삽입으로 생성된다는 사실을 기억하십시오.
물론 다른 데이터 구조도 읽을 수 있습니다.

-  **INTERLEAVING=PIXEL/BAND/FILE/TILED**:
   파일 래스터 데이터에 사용할 교차삽입 방식을 설정합니다.

-  **COMPRESSION=NONE/RLE/JPEG**:
   사용할 압축 방식을 설정합니다. 교차삽입 방식을 TILED로 설정한 경우에만 기본값 NONE이 아닌 다른 값을 사용할 수 있습니다.
   JPEG으로 설정한 경우, 1에서 100 사이의 품질값을 포함시킬 수도 있습니다. 예: COMPRESSION=JPEG40

-  **TILESIZE=n**:
   INTERLEAVING 생성 옵션을 TILED로 설정한 경우, 이 파라미터를 통해 타일 크기를 선택할 수도 있습니다.
   기본값은 127x127이라는 의미의 127입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

참고
---------

-  ``gdal/frmts/pcidsk/pcidskdataset2.cpp`` 로 구현되었습니다.

-  `PCIDSK SDK <https://web.archive.org/web/20130730111701/http://home.gdal.org/projects/pcidsk/index.html>`_
