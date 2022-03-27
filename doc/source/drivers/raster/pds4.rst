.. _raster.pds4:

================================================================================
PDS4 -- NASA 행성 데이터 시스템 v4
================================================================================

.. shortname:: PDS4

.. built_in_by_default::

PDS4(Planetary Data System v4)는 NASA가 태양, 달 및 행성 영상 데이터를 저장하고 배포하기 위해 주로 사용하는 포맷입니다. GDAL은 PDS4 포맷 영상 데이터에 읽기전용 접근을 지원합니다.

PDS4 파일은 RAW 영상 파일을 참조하는 .xml 라벨 파일로 이루어져 있습니다. 이 드라이버는 RAW 영상 파일과 호환되는 스트립(strip) 구조를 가진 개별 비압축 GeoTIFF 파일에 저장된 영상도 지원합니다.

이 드라이버는 지리참조와 좌표계 정보는 물론 선택한 다른 헤더 메타데이터도 읽고 씁니다.

마스크 밴드가 각 소스 밴드에 첨부되어 있습니다. 픽셀값이 누락된 상수 가운데 하나인 경우 이 마스크 밴드의 값은 0입니다.

이 드라이버는 미국 지질조사국(United States Geological Survey)의 지원으로 구현되었습니다.

PDS4는 PDS와 ISIS3를 포함하는 관련 포맷 패밀리의 일원입니다.

GDAL 2.5버전부터, PDS4 드라이버는 고정 너비 아스키(ASCII fixed-width), 고정 너비 바이너리(binary fixed-width) 및 구분된(CSV) 테이블을 OGR 벡터 레이어로 읽고 쓰기를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

메타데이터
---------

PDS4 라벨을 xml:PDS4 메타데이터 도메인의 XML 직렬화(XML-serialized) 콘텐츠로 가져올 수 있습니다.

생성 작업 시, "xml:PDS4" 메타데이터 도메인에 소스 템플릿 라벨을 SetMetadata() 인터페이스를 통해 전송할 수 있습니다.

열기 옵션 (벡터 전용)
--------------------------

.. versionadded:: 3.0

PDS4 벡터 데이터셋을 열 때, 다음 열기 옵션들을 사용할 수 있습니다:

-  **LAT=string**:
   위도값을 담고 있는 필드명입니다. 기본값은 'Latitude'입니다.

-  **LONG=string**:
   경도값을 담고 있는 필드명입니다. 기본값은 'Longitude'입니다.

-  **ALT=string**:
   고도값을 담고 있는 필드명입니다. 기본값은 'Altitude'입니다.

-  **WKT=string**:
   WKT 값을 담고 있는 필드명입니다.

-  **KEEP_GEOM_COLUMNS=YES/NO**:
   원본 x, y, geometry 열들을 정규 필드로 노출시킬지 여부를 선택합니다. 기본값은 NO입니다.

생성 지원
----------------

PDS4 드라이버는 CreateCopy() 및 Create() 인터페이스를 통해 기존 데이터셋의 영상 업데이트 및 새 데이터셋 생성을 지원합니다.

gdal_translate 또는 gdalwarp로 CreateCopy() 사용 시, PDS4를 PDS4로 변환하는 경우 원본 라벨을 가능한 한 보전하려고 노력할 것입니다. USE_SRC_LABEL 생성 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

다음 데이터셋 생성 옵션들을 사용할 수 있습니다:

-  래스터 전용:

   -  **IMAGE_FILENAME=filename**:
      기본 외부 이미지 파일명을 대체합니다.

   -  **IMAGE_EXTENSION=ext**:
      외부 이미지 파일명의 기본 확장자를 대체합니다.
      IMAGE_FORMAT을 RAW로 설정한 경우 기본값은 'img', GEOTIFF로 설정한 경우 기본값은 'tif'입니다.

   -  **IMAGE_FORMAT=RAW/GEOTIFF**:
      이미지 파일 포맷을 설정합니다. RAW로 설정하는 경우, 파일명이 주 파일명에 확장자 .img인 RAW 파일에 영상을 넣습니다. GEOTIFF로 설정하면, 파일명이 주 파일명에 확장자 .tif인 개별 GeoTIFF 파일에 영상을 넣습니다. 기본값은 RAW입니다.

   -  **INTERLEAVE=BSQ/BIP/BIL**:
      이미지 파일의 픽셀 구조를 설정합니다. BSQ는 밴드 순차(Band SeQuential), BIP는 픽셀 별 밴드 교차삽입(Band Interleaved per Pixel) 그리고 BIL은 라인 별 밴드 교차삽입(Band Interleave Per Line)입니다. 기본값은 BSQ입니다. IMAGE_FORMAT을 GEOTIFF로 설정했다면 BIL을 사용해서는 안 됩니다.
      GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 가진 다중 밴드 소스 데이터셋으로부터 복사할 때 INTERLEAVE 생성 옵션을 지정하지 않으면, 소스 데이터셋의 INTERLEAVE를 자동으로 연산에 넣을 것입니다.

   -  **USE_SRC_LABEL=YES/NO**:
      PDS4를 PDS4로 변환할 때 소스 라벨을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

   -  **ARRAY_TYPE=Array/Array_2D/Array_2D_Image/Array_2D_Map/Array_2D_Spectrum/Array_3D/Array_3D_Image/Array_3D_Movie/Array_3D_Spectrum**:
      배열의 유형을 정의하는 XML 요소를 설정합니다. 기본값은 Array_3D_Image입니다.
      다중 밴드 이미지에 Array_2D\* 사용은 지원하지 않습니다.
      Array_2D\* 값을 설정하는 경우, INTERLEAVE 옵션을 무시할 것입니다.

   -  **ARRAY_IDENTIFIER=string**: (GDAL 3.0 이상 버전)
      배열 요소에 넣을 식별자를 설정합니다.

   -  **UNIT=string**: (GDAL 3.0 이상 버전)
      Element_Array.unit의 내용입니다. 이 옵션을 지정하지 않으면, 다른 래스터로부터 복사해오는 경우의 소스 밴드 단위를 (소스 밴드에 단위가 존재하는 경우) 사용할 것입니다.

   -  **CREATE_LABEL_ONLY=YES/NO**: (GDAL 3.1 이상 버전)
      YES로 설정하고 소스 데이터셋이 PDS4가 지원하는 RAW 바이너리 포맷과 호환되는 레이아웃을 가진 ENVI, GeoTIFF, ISIS3, VICAR, FITS 또는 PDS3 데이터셋인 gdal_translate / CreateCopy() 맥락에서 사용하는 경우, 소스 데이터셋의 RAW 바이너리 파일을 참조하는 XML 라벨 파일만 생성할 것입니다. 이런 경우에는 IMAGE_FILENAME, IMAGE_FORMAT 및 INTERLEAVE 생성 옵션들을 무시합니다.

-  래스터 및 벡터:

   -  **VAR_\*=string**:
      VAR_XXXX=yyyy 같은 옵션을 지정하면, 템플릿 라벨에 있는 모든 {XXXX} 문자열을 yyyy 값으로 대체할 것입니다.

   -  **TEMPLATE=filename**:
      사용할 템플릿 라벨 파일을 설정합니다. 이 옵션을 지정하지 않고 기존 PDS4 파일로부터도 생성하지 않는 경우, data/pds4_template.xml 파일을 사용할 것입니다. GDAL 유틸리티가 이 기본 PDS4 템플릿을 찾을 수 있도록 (특히 윈도우 빌드에서) 사용자 환경 변수에 GDAL data 디렉터리를 정의해야 합니다. 더 자세한 정보는 `위키 <https://trac.osgeo.org/gdal/wiki/FAQInstallationAndBuilding#HowtosetGDAL_DATAvariable>`_ 를 찾아보십시오.

   -  **LATITUDE_TYPE=Planetocentric/Planetographic**:
      latitude_type의 값을 설정합니다. 기본값은 Planetocentric입니다.

   -  **LONGITUDE_DIRECTION=Positive East/Positive West**:
      longitude_direction의 값을 설정합니다. 기본값은 Positive East입니다.

   -  **RADII=semi_major_radius,semi_minor_radius**:
      공간 좌표계의 반경을 대체합니다.
      첫 번째 값(semi_major_radius)을 사용해서 <pds:semi_major_radius> 및 <pds:semi_minor_radius> XML 요소를 설정하고, 두 번째 값(semi_minor_radius)을 사용해서 <pds:polar_radius> XML 요소를 설정할 것이라는 사실을 기억하십시오.

   -  **BOUNDING_DEGREES=west_lon,south_lat,east_lon,north_lat**:
      경계 상자를 직접 설정합니다.

레이어 생성 옵션 (벡터/테이블 데이터셋)
----------------------------------------------

(GDAL 3.0버전부터) PDS4 벡터 데이터셋 생성 또는 기존 테이블에 새 테이블 추가 작업 시 다음과 같은 레이어 생성 옵션들을 사용할 수 있습니다:

-  **TABLE_TYPE=DELIMITED/CHARACTER/BINARY**:
   생성할 PDS4 테이블의 유형을 설정합니다. 기본값은 DELIMITED로 (쉼표 필드 구분자를 가진)CSV 테이블 파일을 생성합니다. CHARACTER는 고정 너비 아스키 테이블을 생성합니다. BINARY는 고정 너비 테이블을 생성합니다. 고정 너비 테이블의 경우, OGR 필드 정의에 명확하게 설정된 필드가 없다면 문자열 필드에 임의의 64바이트 너비를 사용합니다. DELIMITED로 설정한 경우에만 도형을 WKT 문자열로 임의 인코딩할 수 있습니다. 다른 테이블 유형 2개는 지리 좌표 포인트(위도, 경도)만 지원합니다.

-  **LINE_ENDING= CRLF/LF**: (GDAL 3.4 이상 버전)
   새줄 문자 시퀀스를 설정합니다. TABLE_TYPE 옵션을 DELIMITED 또는 CHARACTER로 설정한 경우에만 적용됩니다. 기본값은 CRLF(Carriage Return and Line Feed)입니다. 줄바꿈(Line Feed) 문자만 사용하려면 LF로 설정하면 됩니다.

-  **GEOM_COLUMNS=AUTO/WKT/LONG_LAT**:
   도형 인코딩 방식을 설정합니다. DELIMITED 테이블 유형에서 AUTO로 설정하면, 입력 도형이 레이어의 지리 좌표계를 가진 포인트인 경우 포인트 좌표를 저장하기 위해 LONG과 LAT 열들을 생성할 것입니다. 입력 도형이 다른 유형이라면 WKT 열을 사용합니다. LONG과 LAT 열들을 사용할 수 있는 경우에도 이 옵션을 WKT 값으로 설정해서 강제로 WKT 열을 생성시킬 수도 있습니다. 고정 너비 테이블 유형의 경우, AUTO 및 LONG_LAT만 설정할 수 있습니다.

-  **CREATE_VRT=YES/NO**:
   DELIMITED 테이블 유형의 경우 기본값은 YES입니다. 이런 경우 .csv 파일과 함께 OGR VRT(XML 파일)을 생성할 것입니다.

-  **LAT=string**:
   위도값을 담고 있는 필드명입니다. 기본값은 'Latitude'입니다.
   도형이 지리 좌표계를 가진 포인트 레이어의 도형인 경우에만 사용합니다.

-  **LONG=string**:
   경도값을 담고 있는 필드명입니다. 기본값은 'Longitude'입니다.
   도형이 지리 좌표계를 가진 포인트 레이어의 도형인 경우에만 사용합니다.

-  **ALT=string**:
   고도값을 담고 있는 필드명입니다. 기본값은 'Altitude'입니다.
   도형이 지리 좌표계를 가진 포인트 레이어의 도형인 경우에만 사용합니다.

-  **WKT=string**:
   WKT 값을 담고 있는 필드명입니다.

-  **SAME_DIRECTORY=YES/NO**:
   테이블 파일을 동일한 디렉터리에 생성해야 할지 아니면 하위 디렉터리에 생성해야 할지 여부를 선택합니다. 기본값은 NO로, XML 파일의 기본명으로 명명된 하위 디렉터리에 테이블 파일을 생성할 것이라는 뜻입니다. 예를 들어 "foo.xml" PDS4 데이터셋을 생성한다고 할 때, 기본적으로 "foo" 하위 디렉터리에 테이블 파일을 생성할 것입니다. 이 옵션을 YES로 설정하는 경우, "foo.xml" 파일과 동일한 디렉터리에 테이블 파일을 생성할 것입니다.

하위 데이터셋 / 다중 이미지 지원
-----------------------------------

라벨에 배열 객체 여러 개가 존재하는 경우, 개별 하위 데이터셋들로 리포트될 것입니다. (일반적으로 주 데이터셋이 Array3D, 백플레인(backplane)들이 Array2D인 것으로 표현합니다.)

GDAL 3.0버전부터, (APPEND_SUBDATASET=YES 생성 옵션을 통해) 하위 데이터셋을 가진 새 데이터셋 생성을 지원합니다. 중요한 제약 조건이 하나 있는데, PDS4 XML 라벨 파일에 있는 지리참조 정보가 데이터셋 전체에 적용되는 전체 수준인 경우 모든 하위 데이터셋들도 반드시 동일한 지리참조 정보를 -- 좌표계, 지리 등록(georegistration), 해상도 정보를 -- 공유해야만 한다는 것입니다. RAW 및 GEOTIFF 래스터 둘 다에 이 정보를 추가할 수 있습니다. 추가(append) 모드에서는 ARRAY_TYPE 및 ARRAY_IDENTIFIER, 그리고 (산출 이미지가 GeoTIFF 포맷인 경우) INTERLEAVE를 제외한 생성 옵션 대부분을 무시합니다.

PDS4 래스터 예시
--------------------

밴드와 하위 데이터셋 목록:

::

   $ gdalinfo b0011_p237201_01_01v02.xml

   Driver: PDS4/NASA Planetary Data System 4
   Files: b0011_p237201_01_01v02.xml
          b0011_p237201_01_01v02.qub
   Size is 512, 512
   Coordinate System is `'
   Image Structure Metadata:
     INTERLEAVE=BAND
   Subdatasets:
     SUBDATASET_1_NAME=PDS4:b0011_p237201_01_01v02.xml:1:1
     SUBDATASET_1_DESC=Image file b0011_p237201_01_01v02.qub, array Spectral_Qube_Object
     SUBDATASET_2_NAME=PDS4:b0011_p237201_01_01v02.xml:1:2
     SUBDATASET_2_DESC=Image file b0011_p237201_01_01v02.qub, array iof_r2
     SUBDATASET_3_NAME=PDS4:b0011_p237201_01_01v02.xml:1:3
     SUBDATASET_3_DESC=Image file b0011_p237201_01_01v02.qub, array iof_r7
     SUBDATASET_4_NAME=PDS4:b0011_p237201_01_01v02.xml:1:4
   [...]
     SUBDATASET_16_DESC=Image file b0011_p237201_01_01v02.qub, array emission_angle
     SUBDATASET_17_NAME=PDS4:b0011_p237201_01_01v02.xml:1:17
     SUBDATASET_17_DESC=Image file b0011_p237201_01_01v02.qub, array phase_angle
     SUBDATASET_18_NAME=PDS4:b0011_p237201_01_01v02.xml:1:18
     SUBDATASET_18_DESC=Image file b0011_p237201_01_01v02.qub, array approx_incidence_angle
     SUBDATASET_19_NAME=PDS4:b0011_p237201_01_01v02.xml:1:19
     SUBDATASET_19_DESC=Image file b0011_p237201_01_01v02.qub, array approx_emission_angle
     SUBDATASET_20_NAME=PDS4:b0011_p237201_01_01v02.xml:1:20
     SUBDATASET_20_DESC=Image file b0011_p237201_01_01v02.qub, array approx_phase_angle
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)
   Band 1 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.146998785514825,   Scale:4.48823844390647e-06
   Band 2 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.146998785514825,   Scale:4.48823844390647e-06
   Band 3 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.146998785514825,   Scale:4.48823844390647e-06
   Band 4 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.146998785514825,   Scale:4.48823844390647e-06
   Band 5 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.146998785514825,   Scale:4.48823844390647e-06

기본적으로 출력되는 정보는 첫 번째 하위 데이터셋(SUBDATASET_1_NAME)의 정보입니다.

하위 데이터셋에 관한 정보 수집:

::

   $ gdalinfo PDS4:b0011_p237201_01_01v02.xml:1:2

   Driver: PDS4/NASA Planetary Data System 4
   Files: b0011_p237201_01_01v02.xml
          b0011_p237201_01_01v02.qub
   Size is 512, 512
   Coordinate System is `'
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)
   Band 1 Block=512x1 Type=Int16, ColorInterp=Undefined
     Offset: 0.04984971,   Scale:7.454028e-06

지정 하위 데이터셋을 GeoTIFF로 변환:

::

   $ gdal_translate PDS4:b0011_p237201_01_01v02.xml:1:2 iof_r2.tif

모든 하위 데이터셋을 GeoTIFF로 변환:

::

   $ gdal_translate -sds b0011_p237201_01_01v02.xml b0011_p237201_01_01v02.tif

이 명령어는 X=1,....,N인 b0011_p237201_01_01v02_X.tif 파일들을 생성할 것입니다.

기본 템플릿을 사용하고 기본 템플릿에 파라미터화된 변수들을 설정해서 새 PDS4 데이터셋을 생성:

::

   $ gdal_translate input.tif output.xml -of PDS4 \
               -co VAR_TARGET_TYPE=Satellite \
               -co VAR_Target=Moon \
               -co VAR_OBSERVING_SYSTEM_NAME=LOLA \
               -co VAR_LOGICAL_IDENTIFIER=Lunar_LRO_LOLA_DEM_Global_64ppd.tif \
               -co VAR_TITLE="LRO LOLA Digital Elevation Model (DEM) 64ppd" \
               -co VAR_INVESTIGATION_AREA_NAME="Lunar Reconnaissance Orbiter" \
               -co VAR_INVESTIGATION_AREA_LID_REFERENCE="urn:nasa:pds:context:instrument_host:spacecraft.lro"

기본 템플릿을 사용하지만 기본 템플릿에 텍스트 파일로부터 나온 파라미터화된 변수들을 설정해서 위와 동일한 PDS4 데이터셋을 생성합니다. 긴 명령어를 단순화할 수 있습니다:

다음 내용을 가진 "myOptions.txt" 텍스트 파일을 생성한 다음

::

   #This is a comment
   #Conversion parameters for the LRO LOLA dataset
   -co VAR_TARGET_TYPE=Satellite
   -co VAR_Target=Moon
   -co VAR_OBSERVING_SYSTEM_NAME=LOLA
   -co VAR_LOGICAL_IDENTIFIER=Lunar_LRO_LOLA_DEM_Global_64ppd.tif
   -co VAR_TITLE="LRO LOLA Digital Elevation Model (DEM) 64ppd"
   -co VAR_INVESTIGATION_AREA_NAME="Lunar Reconnaissance Orbiter"
   -co VAR_INVESTIGATION_AREA_LID_REFERENCE="urn:nasa:pds:context:instrument_host:spacecraft.lro"
   #end of file

::

   gdal_translate input.tif output.xml -of PDS4 --optfile myOptions.txt

--optfile 옵션에 관해 더 알고 싶다면, `GDAL 유틸리티 일반 문서 <gdal_utilities.html>`_ 를 읽어보십시오.

기본 템플릿이 아닌 템플릿을 사용해서 PDS4 데이터셋을 생성 (이 예시에서는 HTTP 서버에 있는 템플릿을 사용하지만, 로컬 파일명으로도 설정할 수 있습니다):

::

   $ gdal_translate input.tif output.xml -of PDS4 \
               -co TEMPLATE=http://example.com/mytemplate.xml

소스 PDS4 데이터셋의 (이 소스 PDS4 데이터셋의 XML 파일을 암묵적인 템플릿으로 사용해서) 부분 집합인 PDS4 데이터셋을 생성:

::

   $ gdal_translate input.xml output.xml -of PDS4 -projwin ullx ully lrx lry

파이썬 코드로 GeoTIFF의 요소 1개를 새 값으로 대체한 기본 템플릿을 사용해서 PDS4 데이터셋으로 생성:

.. code-block:: python

   from osgeo import gdal
   from lxml import etree

   # Customization of template
   template = open('template.xml','rb').read()
   root = etree.XML(template)
   ns = '{http://pds.nasa.gov/pds4/pds/v1}'
   identifier = root.find(".//{ns}Identification_Area/{ns}logical_identifier".format(ns = ns))
   identifier.text = 'new_identifier'

   # Serialize the modified template in a in-memory file
   in_memory_template = '/vsimem/template.xml'
   gdal.FileFromMemBuffer(in_memory_template, etree.tostring(root))

   # Create the output dataset
   gdal.Translate('out.xml', 'in.tif', format = 'PDS4',
                  creationOptions = ['TEMPLATE='+in_memory_template])

   # Cleanup
   gdal.Unlink(in_memory_template)

기존 PDS4 데이터셋에 새 이미지(하위 데이터셋)를 추가:

::

   $ gdal_translate new_image.tif existing_output.xml -of PDS4 \
                         -co APPEND_SUBDATASET=YES \
                         -co ARRAY_IDENTIFIER=my_new_image

기존 ISIS3 데이터셋에 PDS4 라벨을 추가 (GDAL 3.1 이상 버전):

::

   $ gdal_translate dataset.cub dataset.xml -of PDS4 -co CREATE_LABEL_ONLY=YES

PDS4 벡터 예시
--------------------

테이블을 가진 PDS4 데이터셋의 콘텐츠를 출력:

::

   $ ogrinfo -al my_pds4.xml

경도와 위도를 담고 있는 열을 지정해서 테이블을 가진 PDS4 데이터셋을 shapefile로 변환:

::

   $ ogr2ogr out.shp my_pds4.xml -oo LAT=my_lat_column -oo LONG=my_long_column

shapefile을 (도형을 저장하기 위한 WKT 열을 내포한) 쉼표로 구분된 CSV 테이블을 가진 PDS4 데이터셋으로 변환:

::

   $ ogr2ogr my_out_pds4.xml in.shp

제약
-----------

새로 도입된 드라이버와 포맷이기 때문에, 문제점을 발견했다면 `위키 <https://trac.osgeo.org/gdal/wiki>`_ 에 설명된 대로 버그 트래커에 리포트해주십시오.

참고
---------

-  ``gdal/frmts/pds/pds4dataset.cpp`` 로 구현되었습니다.

-  `공식 문서 <https://pds.nasa.gov/pds4/doc/index.shtml>`_

-  `지도 제작 확장 사양을 포함하는 스키마 <https://pds.nasa.gov/pds4/schema/released/>`_

-  :ref:`raster.pds` 드라이버

-  :ref:`raster.isis3` 드라이버

