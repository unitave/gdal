.. _vector.vdv:

VDV - VDV-451/VDV-452/INTREST 데이터 포맷
=========================================

.. versionadded:: 2.1

.. shortname:: VDV

.. built_in_by_default::

VDV 드라이버는 VDV-451 포맷을 준수하는 텍스트 파일을 읽고 생성할 수 있습니다. 이 포맷은 CSV 파일과 비슷한 텍스트 포맷으로, 동일 파일 안에 레이어를 여러 개 담고 있을 수도 있습니다.

이 드라이버는 특히 다음 2개의 "프로파일" 읽기를 지원합니다:

-  (읽기/쓰기) 경로망/시간표 용 VDV-452 표준

-  (읽기 전용) `오스트리아 열린정부 도표 통합 교통 플랫폼 <https://www.data.gv.at/katalog/dataset/3fefc838-791d-4dde-975b-a4131a54e7c5>`_ 이 사용하는 "INTREST 데이터 포맷"

VDV-451/VDV-452 용 일반 판독기/작성기는 임의 크기의 대용량 파일을 지원합니다. INTREST 데이터의 경우, 단일 파일에 결합된 레이어들에 대해 이 드라이버는 'Link' 레이어를 재구성하기 위해 메모리에 전체 파일을 불러옵니다.

레이어를 여러 개 가진 파일에 있는 레이어들 사이에서 교차삽입 읽기를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
----------------

이 드라이버는 (동일 파일 안에, 또는 동일 디렉터리에 있는 개별 파일에) 새 레이어를 생성할 수 있습니다. 기존 파일에 새 레이어를 추가할 수 있지만, 기존 레이어에 객체를 추가, 편집, 삭제하거나 또는 객체를 작성한 다음 기존 레이어의 속성 구조를 수정할 수는 없습니다.

데이터셋 생성 옵션
------------------

다음 데이터셋 생성 옵션을 사용할 수 있습니다:

-  **SINGLE_FILE=YES/NO**:
   동일 파일에 레이어 여러 개를 넣어야 할지 여부를 선택합니다. NO로 설정하는 경우, 디렉터리 이름을 이름으로 가정합니다. 기본값은 YES입니다.

레이어 생성 옵션
----------------

다음 레이어 생성 옵션들을 사용할 수 있습니다:

-  **EXTENSION=string**:
   파일을 개별 레이어로 생성할 때 사용할 확장자를 지정합니다. SINGLE_FILE 데이터셋 생성 옵션이 NO로 설정된 경우에만 사용할 수 있습니다. 기본값은 x10입니다.

-  **PROFILE=GENERIC/VDV-452/VDV-452-ENGLISH/VDV-452-GERMAN**:
   기본값은 GENERIC입니다. 작성기가 어떤 프로파일을 준수해야 할지 설명합니다.
   VDV-452로 설정하면 레이어 및 필드 이름을 (영어 또는 독일어 가운데) VDV-452 표준이 허용하는 이름으로 제약할 것입니다.
   VDV-452-ENGLISH 또는 VDV-452-GERMAN으로 설정하면 지정한 언어의 VDV-452 표준이 허용하는 이름으로 제약할 것입니다.
   GDAL_DATA 디렉터리에 있는 `vdv452.xml <https://github.com/OSGeo/gdal/blob/master/data/vdv452.xml>`_ 파일이 VDV-452 테이블 및 필드 이름을 설명하는 환경설정 파일입니다.

-  **PROFILE_STRICT=YES/NO**: Whether checks of profile should be
   strict. In strict mode, unexpected layer or field names will be
   rejected. 기본값은 NO.

-  **CREATE_ALL_FIELDS=YES/NO**:
   레이어 생성 시 사전 정의된 프로파일의 필드를 모두 생성해야 할지 여부를 선택합니다. 기본값은 YES입니다.

-  **STANDARD_HEADER=YES/NO**:
   표준 헤더 필드들을 (mod, src, chs, ver, ifv, dve, fft를) 작성할지 여부를 선택합니다. NO로 설정하면 명확하게 지정한 HEADER_xxx 필드들을 작성할 것입니다. 기본값은 YES입니다.

-  **HEADER_SRC=string**:
   'src' 헤더 필드의 값을 지정합니다. 기본값은 UNKNOWN입니다.

-  **HEADER_SRC_DATE=string**:
   'src' 헤더 필드의 날짜를 DD.MM.YYYY 형식으로 지정합니다. 기본값은 (그리니치 표준시 기준) 현재 날짜입니다.

-  **HEADER_SRC_TIME=string**:
   'src' 헤더 필드의 시간을 HH.MM.SS 형식으로 지정합니다. 기본값은 (그리니치 표준시 기준) 현재 시간입니다.

-  **HEADER_CHS=string**:
   'chs' 헤더 필드의 값을 지정합니다. 기본값은 ISO8859-1입니다.

-  **HEADER_VER=string**:
   'ver' 헤더 필드의 값을 지정합니다. 기본값은 1.4입니다.

-  **HEADER_IFV=string**:
   'ifv' 헤더 필드의 값을 지정합니다. 기본값은 1.4입니다.

-  **HEADER_DVE=string**:
   'dve' 헤더 필드의 값을 지정합니다. 기본값은 1.4입니다.

-  **HEADER_FFT=string**:
   'fft' 헤더 필드의 값을 지정합니다. 기본값은 ''(빈 문자열)입니다.

-  **HEADER_xxx=string**:
   '*xxx*' (사용자 정의) 헤더 필드의 값을 지정합니다.

Links
-----

-  `VDV-451 파일 포맷 <https://www.vdv.de/vdv-schrift-451.pdfx?forced=true>`_ (독일어)
-  `VDV-452 데이터 모델 <https://www.vdv.de/452--sdsv15.pdfx?forced=true>`_ (독일어)
-  `오스트리아 INTREST 데이터 포맷 <https://gip.gv.at/assets/downloads/1908_dokumentation_gipat_ogd.pdf>`_ (독일어)

