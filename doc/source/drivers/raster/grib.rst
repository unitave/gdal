.. _raster.grib:

================================================================================
GRIB -- 바이너리 형식의 WMO 일반 정규 배포 정보 (WMO General Regularly-distributed Information in Binary form)
================================================================================

.. shortname:: GRIB

.. built_in_by_default::

GDAL은 공통 좌표계, 지리참조 및 기타 메타데이터를 위한 지원과 함께 GRIB1(읽기) 및 GRIB2(읽기와 쓰기) 포맷을 지원합니다. GRIB 포맷은 기상 정보의 배포에 흔히 쓰이며, 세계 기상 기구(World Meteorological Organization)가 전파하고 있습니다.

GDAL GRIB 드라이버는 NOAA NWS NDFD(MDL)의 아서 테일러(Arthur Taylor)가 처음 작성한 degrib 응용 프로그램의 수정본을 기반으로 합니다. degrib 응용 프로그램은 (그리고 GDAL GRIB 드라이버는) NOAA NWS NCEP의 존 허들스턴(John Huddleston)이 처음 작성한 g2clib grib 디코딩 라이브러리 상에서 빌드되었습니다.

경도/위도 그리드 상에 투영되지 않는 GRIB2 파일은, [0,360] 범위에서 경도를 사용하고 다른 보통 데이터셋들처럼 본초 자오선(prime meridian)에서 나뉘는 것이 아니라 반대 자오선(anti-meridian)에서 나뉜다는 특성을 가지고 있습니다. GDAL 3.4.0버전부터, 이런 파일을 읽어오는 경우 경도를 [-180,180] 범위로 알기 쉽게 변환하고 데이터를 본초 자오선에서 나뉘도록 수정할 것입니다. 이를 분할 및 바꾸기(split and swap) 모드라고 합니다. 이 모드를 비활성화시키려면 :decl_configoption:`GRIB_ADJUST_LONGITUDE_RANGE` 환경설정 옵션을 NO로 설정하면 됩니다.

GRIB 포맷 래스터 데이터를 위한 인코딩 스키마가 여러 개 있습니다. PNG 인코딩을 포함, 가장 흔히 쓰이는 스키마들을 지원할 것입니다. GDAL JPEG2000 드라이버 가운데 하나를 통해 JPEG2000 지원과 함께 GDAL을 빌드한 경우, JPEG2000으로 인코딩된 GRIB 파일을 당연히 지원할 것입니다.

시계열(time sequence)을 표현하는 몇몇 밴드 집합들 때문에, GDAL에서 GRIB 파일이 수많은 밴드를 가지고 있는 것으로 나타날 수도 있습니다. GRIB 밴드는 실제 값과 상관없이 Float64(배정밀도 부동소수점형)로 나타납니다. GRIB 메타데이터는 밴드 별 메타데이터로 수집되며 다음과 비슷한 방식으로 밴드 설명을 설정하기 위해 쓰입니다:

::

     Description = 100000[Pa] ISBL="Isobaric surface"
       GRIB_UNIT=[gpm]
       GRIB_COMMENT=Geopotential height [gpm]
       GRIB_ELEMENT=HGT
       GRIB_SHORT_NAME=100000-ISBL
       GRIB_REF_TIME=  1201100400 sec UTC
       GRIB_VALID_TIME=  1201104000 sec UTC
       GRIB_FORECAST_SECONDS=3600 sec

GRIB2 파일도 `식별 섹션 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect1.shtml>`_,
`상품 정의 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect4.shtml>`_ 템플릿 번호(GRIB_PDS_PDTN, 옥텟(octet) 8-9), 그리고 상품 정의 템플릿 값(GRIB_PDS_TEMPLATE_NUMBERS, 옥텟 10+) 같은 기타 메타데이터에서 추출한 내용을 메타데이터로 포함할 수도 있습니다. 다음은 그 예시입니다:

::

       GRIB_DISCIPLINE=0(Meteorological)
       GRIB_IDS=CENTER=7(US-NCEP) SUBCENTER=0 MASTER_TABLE=8 LOCAL_TABLE=1 SIGNF_REF_TIME=1(Start_of_Forecast) REF_TIME=2017-10-20T06:00:00Z PROD_STATUS=0(Operational) TYPE=1(Forecast)
       GRIB_PDS_PDTN=32
       GRIB_PDS_TEMPLATE_NUMBERS=5 7 2 0 0 0 0 0 1 0 0 0 0 1 0 31 1 29 67 140 2 0 0 238 217
       GRIB_PDS_TEMPLATE_ASSEMBLED_VALUES=5 7 2 0 0 0 0 1 0 1 31 285 17292 2 61145

GRIB_DISCIPLINE은 GDAL 2.3.0부터 추가되었으며, 메시지의 0번 섹션의 `Discipline <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table0-0.shtml>`_ 필드입니다.

GRIB_IDS는 2.3.0부터 추가되었으며, 메시지의 1번 섹션 또는 `식별 섹션
<http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table0-0.shtml>`_ 입니다.

GRIB_PDS_TEMPLATE_ASSEMBLED_VALUES는 2.3.0부터 추가되었으며, 템플릿 항목을 16비트 또는 32비트 부호 있는/부호 없는 정수형으로 만드는 몇몇 바이트를 모으기 위해 템플릿 정의를 사용합니다. 반면에 GRIB_PDS_TEMPLATE_NUMBERS는 RAW 바이트를 노출시킵니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

환경설정 옵션
---------------------

이 단락에서는 GRIB 드라이버의 기본 습성을 변경하기 위해 설정할 수 있는 환경설정 옵션들을 나열합니다.

-  GRIB_NORMALIZE_UNITS=YES/NO : 기본값은 YES입니다. GDAL이 단위를 미터법으로 정규화하는 일을 막으려면 NO로 설정하면 됩니다. 기본적으로 (GRIB_NORMALIZE_UNITS=YES) 기온을 섭씨 온도(°C)로 리포트합니다. GRIB_NORMALIZE_UNITS=NO인 경우, 기온을 켈빈 온도(°K)로 리포트합니다.
-  GRIB_RESOURCE_DIR=path : grib2_*.csv 테이블이 있는 디렉터리를 가리키는 경로입니다. 지정하지 않는 경우, 모든 GDAL 리소스에 쓰인 GDAL_DATA 환경설정 옵션을 (또는 하드 코딩된 경로를) 사용할 것입니다.

열기 옵션
------------

-  **USE_IDX=YES/NO**: (GDAL 3.4버전부터)
   사용할 수 있는 경우, 외부 wgrib2 색인 파일 자동 읽기를 활성화합니다. 기본값은 YES입니다. GDAL이 데이터셋과 같은 위치에 있는 ``<GRIB>.idx`` 를 찾을 것입니다. 이 파일을 API 또는 명령줄 도구와 함께 조심해서 활용하면 모든 밴드를 읽지 않고서도 GRIB2 파일을 열 수 있습니다. 특히, (AWS S3 상의 NOMADS 같은) 원격 저장소에 있는 대용량 GRIB2 파일로부터 선택한 밴드를 추출해오는 경우 속도 단위의 자릿수가 달라집니다. 불필요한 I/O를 피하려면 밴드의 텍스트 설명에만 접근해야 합니다. 메타데이터에 접근하면 밴드 헤더를 반드시 불러와야 하기 때문입니다. gdal_translate에서 이 옵션을 사용할 수 있지만, gdalinfo에서는 안 됩니다. 다중 차원 API를 이용하는 경우 이 옵션을 무시합니다. (그리고 색인을 무시합니다.)

GRIB2 쓰기 지원
-------------------

GDAL 2.3.0부터 GRIB2 쓰기를 CreateCopy() 또는 gdal_translate 인터페이스를 통해 지원합니다.

입력 데이터셋의 각 밴드를 GRIB2 메시지로 변환하고, 통례를 따라 단일 파일에 모든 메시지들을 연결합니다.

입력 데이터셋은 지리참조되어야만 하며, 지리 경도/위도, 메르카토르 1SP/2SP, 횡축 메르카토르, 극 입체(Polar Stereographic), 람베르트 정각원추 1SP/2SP, 알베르스 정적원추 및 람베르트 정적방위 투영법을 지원합니다.

아래 단락에서 사용할 수 있는 생성 옵션 여러 개를 설명하고 있습니다. 이 생성 옵션들은 모든 밴드에 적용할 수 있습니다. 그러나 이런 전체 수준 설정을 밴드 별로 무시할 수도 있습니다. 동일한 키를 사용하고 BAND_X\_ 접두어가 붙는 생성 옵션을 정의하면 됩니다. 이때 X는 1에서 총 밴드 개수 사이의 밴드 번호입니다. 예를 들면 BAND_1_PDS_PDTN 같은 생성 옵션 말입니다.

상품 식별 정보 및 정의
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

사용자가 `0번 섹션 / "Indicator" <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect0.shtml>`_, `1번 섹션 / "Identification section" <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect1.shtml>`_ 및 `4번 섹션 / "Product definition section" <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect4.shtml>`_ 을 적절하게 채우기 위해 필요한 정보를 다음 생성 옵션들과 함께 제공할 것을 강력히 권장합니다. 그렇게 하지 않는 경우 GDAL이 기본값으로 채울 것이지만, 판독기가 이런 기본값들로 생성된 GRIB2 데이터셋을 활용하는 데 문제가 생길 수도 있습니다.

-  **DISCIPLINE**\ =integer: 0번 섹션의 Discipline 필드를 설정합니다. `Table 0.0 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table0-0.shtml>`_ 이 지정하는 값을 사용해야 합니다:

   -  0: 기상(meteorology) 상품. 기본값입니다.
   -  1: 수문(hydrology) 상품
   -  2: 지표면(land surface) 상품
   -  3, 4: 우주(space) 상품
   -  10: 해양(oceanography) 상품

-  **IDS**\ =string. 1번 섹션 / Identification section의 필드를 채우기 위한 서로 다른 요소를 가진 문자열입니다. 이 문자열의 값은 보통 기존 GRIB 상품의 GRIB_IDS 메타데이터로부터 가져옵니다. 예를 들면 "IDS=CENTER=7(US-NCEP) SUBCENTER=0 MASTER_TABLE=8 SIGNF_REF_TIME=1(Start_of_Forecast) REF_TIME=2017-10-20T06:00:00Z PROD_STATUS=0(Operational) TYPE=1(Forecast)" 같은 문자열입니다. 더 공식적으로 말하자면, 이 문자열의 서식은 공백으로 구분된 KEY=VALUE 항목들의 목록입니다. CENTER, SUBCENTER, MASTER_TABLE, SIGNF_REF_TIME, REF_TIME, PROD_STATUS 및 TYPE 키를 입력할 수 있습니다. 이 갑에서 숫자 부분만 연산에 넣습니다. (괄호 사이의 정밀도는 무시할 것입니다.) 이 IDS 생성 옵션과, IDS의 xxx 키에 대응하며 IDS의 xxx 키를 무시할 특정 IDS_xxx 생성 옵션을 둘 다 사용할 수도 있습니다. 예를 들면 앞의 예에서 "IDS=CENTER=7(US-NCEP)..."와 "IDS_CENTER=8"을 둘 다 정의하는 경우, 실제 사용되는 값은 8입니다.
-  **IDS_CENTER**\ =integer. `Table 0 <http://www.nco.ncep.noaa.gov/pmb/docs/on388/table0.html>`_ 에 지정된 값을 사용하는 발신/생성 기지의 식별정보입니다. 기본값은 255 또는 누락(Missing)입니다.
-  **IDS_SUBCENTER**\ =integer. Identification of originating/generating
   center, according to `Table C <http://www.nco.ncep.noaa.gov/pmb/docs/on388/tablec.html>`_ 에 지정된 값을 사용하는 발신/생성 기지의 식별정보입니다. 기본값은 65535 또는 누락입니다.
-  **IDS_MASTER_TABLE**\ =integer. `Table 1.0 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table1-0.shtml>`_ 에 지정된 값을 사용하는 GRIB 마스터 테이블 버전 숫자입니다. 기본값은 2입니다.
-  **IDS_SIGNF_REF_TIME**\ =integer. `Table 1.2 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table1-2.shtml>`_ 에 지정된 값을 사용하는 기준 시간의 의미입니다. 기본값은 0 또는 Analysis입니다.
-  **IDS_REF_TIME**\ =datetime as YYYY-MM-DD[THH:MM:SSZ]. 기준 시간입니다. 기본값은 1970-01-01T00:00:00Z입니다.
-  **IDS_PROD_STATUS**\ =integer. Production status of processed data,
   according to `Table 1.3 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table1-3.shtml>`_ 에 지정된 값을 사용하는 처리된 데이터의 생산 상태입니다. 기본값은 255 또는 누락입니다.
-  **IDS_TYPE**\ =integer. `Table 1.4 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table1-4.shtml>`_ 에 지정된 값을 사용하는 처리된 데이터의 유형입니다. 기본값은 255 또는 누락입니다.
-  **PDS_PDTN**\ =integer. `Table 4.0 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table4-0.shtml>`_ 에 지정된 값을 사용하는 상품 정의 템플릿 번호입니다. 기본값은 0 또는 Analysis, 또는 수평선 수준 또는 수평선 레이어에서의 어떤 시간의 기상 예보입니다. 이 기본 템플릿 번호를 사용하는데 PDS_TEMPLATE_NUMBERS 또는 PDS_TEMPLATE_ASSEMBLED_VALUES 둘 다 지정하지 않은 경우, 필드 대부분을 누락으로 설정한 채로 기본 템블릿 정의를 사용합니다.
-  **PDS_TEMPLATE_NUMBERS**\ =string. 상품 정의 템플릿 RAW 번호입니다. 이 문자열은 공백으로 구분된 (각각 0에서 255 사이의) 바이트 값들의 목록입니다. 값들의 개수와 의미(semantics)는 PDS_PDTN이 지정하는 템플릿 번호에 따라 달라지며, 사용자는 `Table 4.0 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table4-0.shtml>`_ 이 가리키는 템플릿 구조를 연구해야 합니다. 이 항목의 값으로 기존 GRIB2 상품이 리포트하는 GRIB_PDS_TEMPLATE_NUMBERS를 사용하는 편이 쉬울 수도 있습니다. 드라이버의 읽기 향에서 템플릿 구조를 알고 있다면, 템플릿 구조를 기준으로 템플릿 번호의 개수의 무결성을 검증하려 할 것입니다. (필요한 것보다 많은 요소를 지정한 경우 경고를 발할 것입니다.) 드라이버의 읽기 향에서 구현되지 않았거나 부분적으로 구현된 템플릿도 정의할 수 있습니다.
-  **PDS_TEMPLATE_ASSEMBLED_VALUES**\ =string. 상품 정의 템플릿의 조합된 값들입니다. 이 문자열은 공백으로 구분된 (항목에 따라 부호 있는/부호 없는 1바이트, 2바이트 또는 4바이트 길이의 정수형 범위를 가지는) 값들의 목록입니다. 값들의 개수와 의미(semantics)는 PDS_PDTN이 지정하는 템플릿 번호에 따라 달라지며, 사용자는 `Table 4.0 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table4-0.shtml>`_ 이 가리키는 템플릿 구조를 연구해야 합니다. 이 항목의 값으로 기존 GRIB2 상품이 리포트하는 GRIB_PDS_TEMPLATE_ASSEMBLED_VALUES를 사용하는 편이 쉬울 수도 있습니다. PDS_TEMPLATE_NUMBERS와 PDS_TEMPLATE_ASSEMBLED_VALUES 옵션은 함께 사용할 수 없습니다. 이 생성 옵션을 사용하려면, 드라이버의 읽기 향에서 템플릿 구조를 알고 있어야만 합니다.

데이터 인코딩
~~~~~~~~~~~~~

GRIB2에는 인코딩 스키마가 몇 개 존재합니다. (`5번 섹션 / "Data representation section" <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_sect5.shtml>`_ 참조) GDAL은 기본적으로 입력 데이터의 범위를 보전하기에 적합한 데이터 인코딩을 **DATA_ENCODING**, **NBITS**, **DECIMAL_SCALE_FACTOR**, **JPEG200_DRIVER**, **COMPRESSION_RATIO** 및 **SPATIAL_DIFFERENCING_ORDER** 생성 옵션으로 선택할 것입니다.

사용자는 다음 생성 옵션들을 이용해서 그런 기본값들을 무시할 수 있습니다:

-  **DATA_ENCODING**\ =AUTO / SIMPLE_PACKING / COMPLEX_PACKING / IEEE_FLOATING_POINT / PNG / JPEG2000:
   `데이터 표현 템플릿 번호 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_table5-0.shtml>`_ 를 선택합니다. 기본값은 AUTO입니다.

   -  AUTO 모드에서는, 입력 밴드가 NODATA 값을 가지고 있는 경우 COMPLEX_PACKING을 선택합니다. 그렇지 않고 입력 밴드 데이터 유형이 Float32 또는 Float64인 경우, IEEE_FLOATING_POINT를 선택합니다. 그 외의 경우 SIMPLE_PACKING을 선택합니다.
   -  `SIMPLE_PACKING <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-0.shtml>`_:
      오프셋과 소수점 자리 그리고/또는 바이너리 크기 조정을 이용해서 내부적으로 정수형 표현을 사용합니다. 즉 어떤 데이터 유형도 사용할 수 있습니다.
   -  COMPLEX_PACKING: NODATA를 처리할 수 있는, SIMPLE_PACKING의 진화형입니다. 기본적으로 `비공간 차별화(non-spatial differencing) 인코딩 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-2.shtml>`_ 을 사용하지만, SPATIAL_DIFFERENCING_ORDER가 1 또는 2인 경우 
      but if SPATIAL_DIFFERENCING_ORDER=1 or 2, `공간 차별화 복잡 패킹(complex packing) <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-3.shtml>`_ 을 사용합니다.
   -  `IEEE_FLOATING_POINT <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-4.shtml>`_: 값들을 IEEE-754 단정밀도 또는 배정밀도 숫자형으로 저장합니다.
   -  `PNG <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-41.shtml>`_: SIMPLE_PACKING과 동일한 준비 단계를 거치지만 정수형 값들을 PNG 인코딩합니다.
   -  `JPEG2000 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp5-40.shtml>`_: SIMPLE_PACKING과 동일한 준비 단계를 거치지만 정수형 값들을 JPEG2000 인코딩합니다.

-  **NBITS**\ =integer: 1에서 31 사이의 정수입니다. 각 샘플 값에 대한 비트 길이를 의미합니다. 일부 DATA_ENCODING만 이 값을 느슨하게 존중할 수도 있습니다. 지정하지 않는다면, 정수 데이터 유형의 경우 입력 값들의 범위로부터 비트 길이를 자동 계산하거나 또는 Float32/Float64 데이터 유형의 경우 기본값인 8을 사용합니다.
-  **DECIMAL_SCALE_FACTOR**\ =integer_value: 정수 인코딩 전에 입력 값들을 10^DECIMAL_SCALE_FACTOR로 곱합니다. (디코딩 시 자동적으로 이 값으로 나누기 때문에, 정밀도에만 영향을 미칩니다.) 예를 들어 데이터가 부동소수점 데이터 유형의 기온인 경우 데이터의 정밀도가 1/10도라는 것을 지정하려면 DECIMAL_SCALE_FACTOR를 1로 설정하면 됩니다. 기본값은 0(사전 곱셈 없음)입니다.
-  **SPATIAL_DIFFERENCING_ORDER**\ =0/1/2: COMPLEX_PACKING을 지정한 경우에만 쓰입니다. 공간 차별화의 순서를 정의합니다. 0으로 설정하면 값들을 독립적으로 인코딩하고, 1로 설정하면 연속되는 값들의 차를 인코딩하며, 2로 설정하면 연속되는 값들의 차의 차를 인코딩합니다. 기본값은 0입니다.
-  **COMPRESSION_RATIO**\ =integer_value: 1에서 100 사이의 정수입니다. 기본값은 1로, 비손실 JPEG2000 인코딩을 의미합니다. JPEG2000 인코딩의 경우에만 쓰입니다. 1을 초과하는 값을 지정하는 경우, 손실 JPEG2000 압축을 사용합니다. 이 값은 비압축 데이터에 반비례하는, 사용자가 원하는 압축 인자를 뜻합니다. 예를 들어 10이라는 값은 원하는 JPEG2000 코드스트림이 (픽셀 당 NBITS 비트를 가진) 대상 비압축 파일보다 10배 작아야 한다는 의미입니다.
-  **JPEG2000_DRIVER**\ =JP2KAK/JP2OPENJPEG/JPEG2000/JP2ECW: (GDAL 빌드에서 실제로 사용할 수 있는 JPEG2000 드라이버에 따라 설정할 수 있는 값이 달라집니다.) 어떤 JPEG2000 드라이버를 사용해야 할지를 지정합니다. 지정하지 않는 경우, 목록에 지정된 순서대로 드라이버를 검색합니다.

데이터 단위
~~~~~~~~~~

GRIB은 내부적으로 값을 국제단위계(International System of Units) 단위로 (예: 미터법으로) 저장합니다. 따라서 기온은 켈빈 온도로 저장되어야 합니다. 그러나 드라이버의 읽기 향에서는 (GRIB_NORMALIZE_UNITS 환경설정 옵션을 NO로 설정하지 않는 이상) 기온 필드를 섭씨 온도로 노출시킵니다. 드라이버의 쓰기 향은 일관성을 위해 입력 데이터셋의 (생산 정의 템플릿의 첫 번째 값이, 예를 들어 *Parameter category* 가 0=Temperature인 경우 탐지되는) 기온 값이 섭씨 온도 단위일 것이라고 가정하고 자동적으로 켈빈 온도로 오프셋시킬 것입니다. **INPUT_UNIT** 생성 옵션을 C(섭씨 온도) 또는 K(켈빈 온도)로 설정하면 이런 습성을 제어할 수 있습니다. 기본값은 C입니다.

GRIB2를 GRIB2로 변환
~~~~~~~~~~~~~~~~~~~~~~~~~~
gdal_translate를 (또는 CreateCopy()를) 이용해서 GRIB2를 GRIB2로 변환하는 경우 (생성 옵션으로 무시하지 않는 한) 기본적으로 소스 데이터셋 밴드의 GRIB_DISCIPLINE, GRIB_IDS, GRIB_PDS_PDTN 및 GRIB_PDS_TEMPLATE_NUMBERS 메타데이터 항목들을 이용합니다.

GRIB 특수 메타데이터 도메인으로부터 DECIMAL_SCALE_FACTOR와 NBITS도 가져오려고 시도할 것입니다.

예시
~~~~~~~~

::

   gdal_translate in.tif out.grb2 -of GRIB \
       -co "IDS=CENTER=8(US-NWSTG) SIGNF_REF_TIME=1(Start_of_Forecast) REF_TIME=2008-02-21T17:00:00Z PROD_STATUS=0(Operational) TYPE=1(Forecast)" \
       -co "PDS_PDTN=8" \
       -co "PDS_TEMPLATE_ASSEMBLED_VALUES=0 5 2 0 0 255 255 1 43 1 0 0 255 -1 -2147483647 2008 2 23 12 0 0 1 0 3 255 1 12 1 0"

참고:
---------

-  `NOAA NWS NDFD "degrib" GRIB2 디코더 <https://www.weather.gov/mdl/degrib_archive>`_
-  `NOAA NWS NCEP g2clib grib 디코딩 라이브러리 <http://www.nco.ncep.noaa.gov/pmb/codes/GRIB2/>`_
-  `WMO GRIB1 포맷 문서 <http://www.wmo.int/pages/prog/www/WDM/Guides/Guide-binary-2.html>`_
-  `NCEP WMO GRIB2 문서 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/>`_

감사의 말
--------

GRIB2 쓰기 지원은 캐나다 기상청의 재정 지원으로 개발되었습니다.
