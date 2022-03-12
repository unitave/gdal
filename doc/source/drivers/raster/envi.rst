.. _raster.envi:

================================================================================
ENVI -- ENVI .hdr Labelled 래스터
================================================================================

.. shortname:: ENVI

.. built_in_by_default::

GDAL은 포맷을 설명하는 관련 ENVI 스타일 .hdr 파일을 가진 raw 래스터 파일의 몇몇 변이형들을 지원합니다. 기존 ENVI 래스터 파일을 선택하려면 (.hdr 파일이 아니라) 데이터를 담고 있는 바이너리 파일을 선택하십시오. 그러면 GDAL이 데이터셋 확장자를 .hdr로 바꿔서 .hdr 파일을 찾아낼 것입니다.

GDAL은 BIL, BIP 및 BSQ 교차삽입(interleaving) 포맷 읽기를 지원할 것입니다. 8비트 부호 없는 정수형, 16 및 32비트 부호 있는/부호 없는 정수형, 32 및 64비트 부동소수점형 그리고 32 및 64비트 복소수 부동소수점형을 포함하는 픽셀 유형 대부분을 지원합니다. 좌표계와 지리참조를 이용한 map_info 키워드 식별을 제한적으로 지원합니다. 특히, UTM 및 State Plane은 잘 작동할 것입니다.

모든 ENVI 헤더 파일은 ENVI 메타데이터 도메인에 저장되며, 저장된 모든 내용을 헤더 파일로 작성할 수 있습니다.

생성 옵션:

-  **INTERLEAVE=BSQ/BIP/BIL**: 지정한 교차삽입 유형을 강제로 생성합니다.
  
   - **BSQ** -- 밴드 단위 영상(band sequential) (기본값)
   - **BIP** --- 픽셀 단위 영상(data interleaved by pixel)
   - **BIL** -- 라인 단위 영상(data interleaved by line)
   
   GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 가진 다중 밴드를 가진 소스 데이터셋으로부터 복사할 때 INTERLEAVE 생성 옵션을 지정하지 않는다면 소스 데이터셋의 INTERLEAVE를 자동적으로 연산에 넣을 것입니다.

-  **SUFFIX=REPLACE/ADD**: 지정한 파일명에 ".hdr" 접미어를 강제로 추가합니다. 예를 들어 사용자가 산출 데이터셋에 "file.bin"이라는 이름을 선택했다면 "file.bin.hdr" 헤더 파일을 생성할 것입니다. 기본적으로 헤더 파일 접미어가 바이너리 파일의 접미어를 대체합니다. 예를 들어 "file.bin"이라는 이름을 선택했다면 "file.hdr" 헤더 파일을 생성할 것입니다.

주의: ``gdal/frmts/raw/envidataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

