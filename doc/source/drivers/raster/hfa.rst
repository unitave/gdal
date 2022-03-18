.. _raster.hfa:

================================================================================
HFA -- ERDAS IMAGINE .img
================================================================================

.. shortname:: HFA

.. built_in_by_default::

GDAL은 ERDAS IMAGINE .img 포맷 읽기 접근 및 쓰기를 지원합니다. HFA 드라이버는 오버뷰, 색상표 및 지리참조 정보 읽기를 지원합니다. ERDAS 밴드 u8, s8, u16, s16, u32, s32, f32, f64, c64 및 c128 유형도 지원합니다.

ERDAS 파일을 읽어올 때 파일에 있는 압축 타일 및 누락 타일을 적절히 처리해야 합니다. 용량이 2GB에서 4GB 사이인 파일은 윈도우 NT 상에서 작업할 수 있을 것이고, 일부 유닉스 플랫폼 상에서 작업할 수 있을 수도 있습니다. (2GB를 초과하는 데이터셋에 필요한) 외부 스필(spill) 파일의 읽기 및 쓰기도 지원합니다.

데이터셋 및 밴드 수준에서 메타데이터 읽기 및 쓰기를 지원하지만, GDAL 특화 메타데이터에 한정됩니다. IMAGINE이 식별하는 형태의 메타데이터는 읽거나 쓸 수 없습니다. 메타데이터는 GDAL_MetaData라는 테이블에 저장되며, 이 테이블의 각 열이 메타데이터 항목입니다. 열 제목이 키이고 1번 행의 값이 값입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

복소수 유형을 포함, GDAL이 정의하는 모든 밴드 유형으로 ERDAS IMAGINE 파일을 생성할 수 있습니다. 생성되는 파일의 밴드 개수에 제한은 없습니다. GDALDriver::CreateCopy() 메소드를 사용하는 경우 의사색상표(Pseudo-Color tables)를 작성할 것입니다. 일반적이지 않은 (WGS84, WGS72, NAD83 및 NAD27이 아닌) 원점(datum)을 변환하는 데 문제가 발생할 수도 있지만, 대부분의 투영법을 지원할 것입니다.

생성 옵션
~~~~~~~~

-  **BLOCKSIZE=blocksize**:
   타일 너비/높이(32~2048)입니다. 기본값은 64입니다.
-  **USE_SPILL=YES**:
   스필 파일을 강제로 생성합니다. (기본적으로 이미지 용량이 2GB를 초과하는 경우에만 스필 파일을 생성합니다.) 기본값은 NO입니다.
-  **COMPRESSED=YES**:
   압축 파일을 생성합니다. 스필 파일을 생성하는 경우 압축이 비활성화됩니다. 기본값은 NO입니다.
-  **NBITS=1/2/4**:
   특수 하위 바이트(sub-byte) 데이터 유형을 생성합니다.
-  **PIXELTYPE=[DEFAULT/SIGNEDBYTE]**:
   이 옵션을 SIGNEDBYTE로 설정하면, 새 바이트형 파일을 강제로 부호 있는 바이트형으로 작성할 수 있습니다.
-  **AUX=YES**:
   .aux 파일을 생성합니다. 기본값은 NO입니다.
-  **IGNOREUTM=YES**:
   좌표계 선택 시 UTM을 무시합니다. 횡축 메르카토르 좌표계를 사용할 것입니다. Create() 메소드를 사용하는 경우에만 이 옵션을 설정할 수 있습니다. 기본값은 NO입니다.
-  **STATISTICS=YES**:
   통계와 히스토그램을 생성합니다. 기본값은 NO입니다.
-  **DEPENDENT_FILE=filename**:
   의존(dependent) 파일의 이름을 설정합니다. (절대 경로로 설정하지 마십시오.) 선택 옵션입니다.
-  **FORCETOPESTRING=YES**:
   파일에 IMAGINE 좌표계 서식 대신 ArcGIS PE 문자열을 강제로 사용합니다. 이 옵션을 설정하면 ArcGIS 좌표계 호환성이 향상되는 경우가 가끔 있습니다.

ERDAS IMAGINE 포맷은 (예를 들면 gdaladdo를 이용한) 오버뷰의 외부 생성을 지원합니다. 오버뷰를 (원본 .img 안이 아니라) .rrd 파일로 강제 생성하려면 전체 수준 환경설정 옵션 HFA_USE_RRD를 YES로 설정하십시오.

래스터 밴드 객체에 GDALSetDescription/GDALGetDescription 호출을 통해 레이어 이름을 설정하고 가져올 수 있습니다.

몇몇 HFA 밴드 메타데이터를 GDAL 메타데이터로 내보냅니다:

-  LAYER_TYPE - 레이어 유형 (테마 없음 등등)
-  OVERVIEWS_ALGORITHM - 레이어 오버뷰 알고리즘 ('IMAGINE 2X2 Resampling', 'IMAGINE 4X4 Resampling' 및 기타)

환경설정 옵션
---------------------

HFA 드라이버가 현재 지원하는 `런타임 환경설정 옵션 <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 은 3개입니다:

-  **HFA_USE_RRD=YES/NO** :
   외부 오버뷰를 .rrd 파일명 확장자를 가진 ERDAS RRD 포맷으로 강제로 생성할지 여부를 선택합니다. (gdaladdo를 -ro --config USE_RRD YES 옵션 조합으로 실행하면 .aux 확장자를 가진 오버뷰 파일을 생성합니다.)
-  **HFA_COMPRESS_OVR=YES/NO** :
   오버뷰를 압축해서 생성할지 여부를 선택합니다. 기본값은 파일이 압축 파일인 경우에만 압축 오버뷰를 생성하는 것입니다.

   이 환경설정 옵션을 이용하면 ERDAS IMAGINE 포맷이 아닌 기반 이미지의 외부 오버뷰를 작성할 수 있습니다. 산출되는 오버뷰 파일은 RRD 구조를 사용하지만 확장자는 .aux일 것입니다.

   ::

      gdaladdo out.tif --config USE_RRD YES --config HFA_COMPRESS_OVR YES 2 4 8

   ERDAS IMAGINE과 예전 ArcGIS 버전들이 몇몇 이미지 포맷들의 오버뷰를 - 그 오버뷰가 .rrd 확장자를 가지고 있는 경우에만 - 식별할 수도 있습니다. 이런 경우 다음 명령어를 사용하십시오:

   ::

      gdaladdo out.tif --config USE_RRD YES --config HFA_USE_RRD YES --config HFA_COMPRESS_OVR YES 2 4 8

-  (GDAL 2.3 이상 버전) **GDAL_HFA_OVR_BLOCKSIZE** 환경설정 옵션을 32에서 2048 사이의 2의 거듭제곱 값으로 설정하면 오버뷰에 사용되는 블록 크기(타일 너비/높이)를 설정할 수 있습니다. 기본값은 64입니다.

참고
--------

-  ``gdal/frmts/hfa/hfadataset.cpp`` 로 구현되었습니다.
-  archive.org에 저장된 `IMAGINE (.img) 판독기 <http://web.archive.org/web/20130730133056/http://home.gdal.org/projects/imagine/hfa_index.html>`_ 페이지에서 더 많은 정보 및 다른 도구들을 찾아볼 수 있습니다.
-  `ERDAS.com <http://www.erdas.com/>`_
