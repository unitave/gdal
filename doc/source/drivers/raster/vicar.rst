.. _raster.vicar:

================================================================================
VICAR -- VICAR
================================================================================

.. shortname:: VICAR

.. built_in_by_default::

.. note::
    PDS3 데이터셋이 VICAR 헤더를 가지고 있을 수 있습니다. 이런 경우 GDAL은 기본적으로 :ref:`PDS <raster.pds>` 드라이버를 사용할 것입니다. GDAL 3.1버전부터, :decl_configoption:`GDAL_TRY_PDS3_WITH_VICAR` 환경설정 옵션을 YES로 설정한 경우 VICAR 드라이버가 데이터셋을 열 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::


메타데이터
---------

GDAL 3.1버전부터, VICAR 라벨을 json:VICAR 메타데이터 도메인에 있는 JSON 직렬화 콘텐츠로 가져올 수 있습니다.

다음은 그 예시입니다:

.. codeblock:: python

   $ python
   from osgeo import gdal
   ds = gdal.Open('../autotest/gdrivers/data/test_vicar_truncated.bin')
   print(ds.GetMetadata_List('json:VICAR')[0])
   {
    "LBLSIZE":9680,
    "FORMAT":"BYTE",
    "TYPE":"IMAGE",
    "BUFSIZ":2097152,
    "DIM":3,
    "EOL":0,
    "RECSIZE":4840,
    "ORG":"BSQ",
    "NL":1000,
    "NS":400,
    "NB":1,
    "N1":4000,
    "N2":1000,
    "N3":1,
    "N4":0,
    "NBB":0,
    "NLB":0,
    "HOST":"X86-64-LINX",
    "INTFMT":"LOW",
    "REALFMT":"RIEEE",
    "BHOST":"X86-LINUX",
    "BINTFMT":"LOW",
    "BREALFMT":"RIEEE",
    "BLTYPE":"M94_HRSC",
    "COMPRESS":"NONE",
    "EOCI1":0,
    "EOCI2":0,
    "PROPERTY":{
        "M94_ORBIT":{
            "ORBIT_NUMBER":5273,
            "ASCENDING_NODE_LONGITUDE":118.46,
            "ORBITAL_ECCENTRICITY":1.23,
            "ORBITAL_INCLINATION":4.56,
            "PERIAPSIS_ARGUMENT_ANGLE":7.89,
            "PERIAPSIS_TIME":"PERIAPSIS_TIME",
            "PERIAPSIS_ALTITUDE":333.16,
            "ORBITAL_SEMIMAJOR_AXIS":1.23,
            "SPACECRAFT_SOLAR_DISTANCE":4.56,
            "SPACECRAFT_CLOCK_START_COUNT":"1\/1",
            "SPACECRAFT_CLOCK_STOP_COUNT":"1\/2",
            "START_TIME":"start_time",
            "STOP_TIME":"stop_time",
            "SPACECRAFT_POINTING_MODE":"NADIR",
            "RIGHT_ASCENSION":-1.0000000000000001e+32,
            "DECLINATION":-1.0000000000000001e+32,
            "OFFSET_ANGLE":-1.0000000000000001e+32,
            "SPACECRAFT_ORIENTATION":[
                0.000000,
                -1.000000,
                0.000000
            ]
        },
        [...]
        "PHOT":{
            "PHO_FUNC":"NONE"
        }
    },
    "TASK":{
        "HRCONVER":{
            "USER":"mexsyst",
            "DAT_TIM":"DAT_TIM",
            "SPICE_FILE_NAME":[
                "foo"
            ],
            "SPICE_FILE_ID":"(LSK,SCLK,ON)",
            "DETECTOR_TEMPERATURE":1.23,
            "DETECTOR_TEMPERATURE__UNIT":"degC",
            "FOCAL_PLANE_TEMPERATURE":8.5833,
            "FOCAL_PLANE_TEMPERATURE__UNIT":"degC",
            "INSTRUMENT_TEMPERATURE":2.34,
            "INSTRUMENT_TEMPERATURE__UNIT":"degC",
            "LENS_TEMPERATURE":4.56,
            "LENS_TEMPERATURE__UNIT":"degC",
            "SOURCE_FILE_NAME":"SOURCE_FILE_NAME",
            "MISSING_FRAMES":0,
            "OVERFLOW_FRAMES":0,
            "ERROR_FRAMES":1
        }
      }
    }

또는

::

   $ gdalinfo -json ../autotest/gdrivers/data/test_vicar_truncated.bin -mdd all

바이너리 접두어
---------------

GDAL 3.1버전부터, VICAR 라벨이 ('NBB' 라벨 항목을 통해) 바이너리 접두어 길이가 0이 아니라고 선언하는 경우, GDAL이 'BLTYPE' 라벨 항목에 해당하는 항목이 있는지 'vicar.json' 환경설정 파일을 검색하고, 일치하는 항목이 존재한다면 각 이미지 레코드 당 객체 하나를 가진 OGR 벡터 레이어를 사용할 수 있을 것입니다.

다음은 그 예시입니다:

::

    $ ogrinfo h0038_0000.bl2.16 -al -q

    Layer name: binary_prefixes
    OGRFeature(binary_prefixes):0
        EphTime (Real) = 127988268.646895
        Exposure (Real) = 40.1072692871094
        COT (Integer) = 28275
        FEETemp (Integer) = 28508
        FPMTemp (Integer) = 29192
        OBTemp (Integer) = 28295
        FERT (Integer) = 27001
        LERT (Integer) = 28435
        CmpDataLen (Integer) = 146
        FrameCount (Integer) = 486
        Pischel (Integer) = 5
        ActPixel (Integer) = 5120
        RSHits (Integer) = 0
        DceInput (Integer) = 0
        DceOutput (Integer) = 4
        FrameErr1 (Integer) = 0
        FrameErr2 (Integer) = 0
        Gob1 (Integer) = 0
        Gob2 (Integer) = 0
        Gob3 (Integer) = 0
        DSS (Integer) = 97
        DecmpErr1 (Integer) = 0
        DecmpErr2 (Integer) = 0
        DecmpErr3 (Integer) = 0
        FillerFlag (Integer) = 5


생성 지원
----------------

GDAL 3.1버전부터, VICAR 드라이버는 CreateCopy() 및 Create() 인터페이스를 통해 기존 데이터셋의 영상 업데이트 및 새 데이터셋 생성을 지원합니다.

gdal_translate 또는 gdalwarp로 CreateCopy() 사용 시, VICAR를 VICAR로 변환하는 경우 원본 라벨을 가능한 한 보전하려고 노력할 것입니다. USE_SRC_LABEL 생성 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

다음 데이터셋 생성 옵션들을 사용할 수 있습니다:

-  **GEOREF_FORMAT=MIPL/GEOTIFF**: (GDAL 3.4 이상 버전)
   지리참조 정보를 인코딩할 방법을 설정합니다. 기본값 MIPL은 ``MAP`` 속성 그룹을 이용합니다. GEOTIFF로 설정하는 경우, GeoTIFF 키와 태그를 사용하는 ``GEOTIFF`` 속성 그룹을 이용할 것입니다. GEOTIFF 인코딩으로 설정하면 COORDINATE_SYSTEM_NAME, POSITIVE_LONGITUDE_DIRECTION 및 TARGET_NAME 생성 옵션을 무시할 것입니다.

-  **COORDINATE_SYSTEM_NAME=PLANETOCENTRIC/PLANETOGRAPHIC**:
   MAP.COORDINATE_SYSTEM_NAME의 값을 설정합니다. 기본값은 PLANETOCENTRIC입니다.
   이 옵션을 설정하고 USE_SRC_MAP 옵션이 영향을 미치는 경우, 소스 COORDINATE_SYSTEM_NAME을 무시하고 이 옵션의 값을 연산에 넣을 것입니다.

-  **POSITIVE_LONGITUDE_DIRECTION=EAST/WEST**:
   MAP.override의 값을 설정합니다. 기본값은 EAST입니다.
   이 옵션을 설정하고 USE_SRC_MAP 옵션이 영향을 미치는 경우, 소스 POSITIVE_LONGITUDE_DIRECTION을 무시하고 이 옵션의 값을 연산에 넣을 것입니다.

-  **TARGET_NAME=string**:
   MAP.TARGET_NAME의 값을 설정합니다. 일반적으로는 공간 좌표계 원점 이름으로부터 추정하는 값입니다.
   이 옵션을 설정하고 USE_SRC_MAP 옵션이 영향을 미치는 경우, 소스 TARGET_NAME을 무시하고 이 옵션의 값을 연산에 넣을 것입니다.

-  **USE_SRC_LABEL=YES/NO**:
   VICAR를 VICAR로 변환할 때 소스 라벨을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

-  **LABEL=string**:
   사용할 라벨을 JSON 문자열 또는 JSON 문자열을 담고 있는 파일명 가운데 하나로 설정합니다.
   이 옵션을 설정한 경우, USE_SRC_LABEL 옵션보다 이 옵션을 우선합니다.

-  **COMPRESS=NONE/BASIC/BASIC2**:
   압축 메소드를 설정합니다. 기본값은 NONE입니다.
   상호 운용성(interoperability)을 최대화하려면, 사양이 제대로 정의되지 않았기 때문에 VICAR 호환 응용 프로그램에서 항상 사용할 수 있다고 보장할 수 없는 BASIC 또는 BASIC2를 설정하지 마십시오.


참고
--------

- ``gdal/frmts/pds/vicardataset.cpp`` 로 구현되었습니다.

- `VICAR 문서 <https://www-mipl.jpl.nasa.gov/vicar.html>`_

- `VICAR 파일 포맷 <https://www-mipl.jpl.nasa.gov/external/VICAR_file_fmt.pdf>`_

