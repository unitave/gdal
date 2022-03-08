.. _raster.bag:

================================================================================
BAG -- 수심 측량 속성 그리드(Bathymetry Attributed Grid)
================================================================================

.. shortname:: BAG

.. build_dependencies:: libhdf5

이 드라이버는 BAG 포맷의 수심 측량 데이터를 읽기전용(read-only)으로 읽어올 수 있고, GDAL 2.4버전부터는 생성할 수 있습니다. BAG 파일은 실제로 HDF5 파일 형태의 특정 산출물 프로파일이지만, 일반 HDF5 드라이버를 통해 사용할 수 있는 방법보다 더 편리한 방식으로 데이터를 표현할 수 있는 사용자 작성 드라이버가 존재합니다.

BAG 파일은 래스터 그리드 영역에 있는 각 셀에 표고(밴드 1), 불확실성(밴드 2) 값을 표현하는 이미지 밴드 2개를 가지고 있습니다. 이름만 표고인 값들도 있을 수 있고, GDAL 3.2버전부터 BAG_root 아래 있는 표고와 동일한 차원을 가진 모든 숫자 데이터 유형의 2차원 배열을 GDAL 밴드로써 리포트할 것입니다.

데이터셋과 함께 제공되는 내부 XML 메타데이터로부터 지리변형(geotransform) 및 좌표계를 추출합니다. 하지만 공간 좌표계를 인코딩하는 데 WKT가 아닌 방식을 사용하는 경우, 일부 산출물이 지원되지 않는 좌표계 서식을 가질 수도 있습니다.

"xml:BAG" 메타데이터 도메인에서 전체 XML 메타데이터를 사용할 수 있습니다.

각 밴드의 NODATA 값, 최소값, 최대값도 리포트합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

    이 드라이버는 :cpp:func:`GDALDriver::Create` 작업을 지원합니다.

    .. versionadded:: 3.2

.. supports_georeferencing::

.. supports_virtualio::

열기 옵션
------------

변동 해상도에 특화된 열기 옵션의 경우, 다음 단락을 참조하십시오.

기타 열기 옵션:

- REPORT_VERTCRS=YES/NO : (GDAL 3.2버전부터) 기본값은 YES입니다. 이 옵션의 목적은 BAG XML 메타데이터로부터 수직 좌표계를 합성 좌표계의 수직 구성요소로써 리포트하는 것입니다. NO로 설정하면 수평 부분만 리포트할 것입니다.

변동 해상도(Variable Resolution) 그리드 지원
------------------------------------------

GDAL 2.4버전부터, GDAL은 `변동 해상도 그리드 <https://bitbucket.org/ccomjhc/openns/raw/master/docs/VariableResolution/2017-08-10_VariableResolution.docx>`_ 를 가진 BAG 파일을 처리할 수 있게 되었습니다. 변동 해상도 데이터셋은 드라이버가 기본적으로 출력하는 저해상도 그리드로 이루어져 있는데, 파일이 이런 저해상도 셀 각각에 대해 더 높은 해상도의 그리드를 가지고 있을 수 있습니다. GDAL에서는 이런 더 높은 해상도의 그리드를 "수퍼그리드(supergrid)"라고 합니다.

BAG 드라이버는 MODE 열기 옵션으로 제어할 수 있는 서로 다른 작업 모드들을 가지고 있습니다:

-  MODE=LOW_RES_GRID: 기본 모드입니다. 드라이버가 저해상도 그리드를 노출시키며, 데이터셋 메타데이터에 데이터셋이 수퍼그리드를 가지고 있는지(HAS_SUPERGRIDS=TRUE)는 물론 수퍼그리드의 최소 및 최대 해상도를 보여줍니다.
-  MODE=LIST_SUPERGRIDS: 드라이버는 이 모드에서 하위 데이터셋 목록에 있는 다양한 수퍼그리드들을 리포트할 것입니다. 이 모드에서는 검색을 제한하기 위해 추가적인 열기 옵션을 적용할 수도 있습니다.

   -  SUPERGRIDS_INDICES=(y1,x1),(y2,x2),...: 수퍼그리드의 y, x 인덱스가 설명하는 수퍼그리드의 투플(tuple) 또는 투플 목록입니다. (y, x 인덱스는 0에서 시작하며, y는 그리드의 남쪽에서 북쪽 방향이고 x는 그리드의 서쪽에서 동쪽 방향입니다.)
   -  MINX=value: 목록화할 수퍼그리드에 대한 필터로 사용할 최소 지리참조 X값입니다.
   -  MINY=value: 목록화할 수퍼그리드에 대한 필터로 사용할 최소 지리참조 Y값입니다.
   -  MAXX=value: 목록화할 수퍼그리드에 대한 필터로 사용할 최대 지리참조 X값입니다.
   -  MAXY=value: 목록화할 수퍼그리드에 대한 필터로 사용할 최대 지리참조 Y값입니다.
   -  RES_FILTER_MIN=value: 연산에 넣을 수퍼그리드의 최저 해상도 (경계 제외)
   -  RES_FILTER_MAX=value: 연산에 넣을 수퍼그리드의 최고 해상도 (경계 포함)

-  MODE=OPEN_SUPERGRIDS: 수퍼그리드를 엽니다. 이 모드는 앞에서 언급한 모드가 리포트한 SUBDATASET_x_NAME 메타데이터 항목의 값인 BAG:my.bag:supergrid:{y}:{x}와 같은 서식으로 된 문자열을 데이터셋 이름으로 사용하면 촉발됩니다. {y}는 열어볼 수퍼그리드의 (0에서 시작하며, 그리드의 남쪽에서 북쪽 방향인) 인덱스이며 {x}는 (0에서 시작하며, 그리드의 서쪽에서 동쪽 방향인) 인덱스입니다.
-  MODE=RESAMPLED_GRID: 이 모드에서는, 사용자가 대상 그리드의 범위 및 해상도를 지정하면, 드라이버가 대상 그리드의 각 셀 안에 들어오는 수퍼그리드의 노드를 검색할 것입니다. 드라이버는 기본적으로 최고 표고값을 가진 노드를 셀 값을 채우기 위해 선택할 것입니다. 또는 어떤 수퍼그리드의 노드도 검색되지 않는 경우, 셀 값을 NODATA 값으로 설정할 것입니다. 오버뷰를 리포트합니다. 리샘플링된 그리드에 대응하는 이런 오버뷰를 RESX 및 RESY 파라미터의 서로 다른 값들로 계산하지만, (전체 해상도의 리샘플링된 그리드의 최근접 이웃 리샘플링 메소드가 아니라) 동일한 값 채우기 규칙을 사용한다는 사실을 기억하십시오.

   이 모드에서는 다음 열기 옵션들을 사용할 수 있습니다:

   -  MINX=value: 리샘플링된 그리드를 위한 최소 지리참조 X값입니다. 기본적으로, 저해상도 그리드의 대응하는 값입니다.
   -  MINY=value: 리샘플링된 그리드를 위한 최소 지리참조 Y값입니다. 기본적으로, 저해상도 그리드의 대응하는 값입니다.
   -  MAXX=value: 리샘플링된 그리드를 위한 최대 지리참조 X값입니다. 기본적으로, 저해상도 그리드의 대응하는 값입니다.
   -  MAXY=value: 리샘플링된 그리드를 위한 최대 지리참조 Y값입니다. 기본적으로, 저해상도 그리드의 대응하는 값입니다.
   -  RESX=value: 수평 해상도 입니다. 기본적으로, 그리고 RES_STRATEGY를 AUTO로 설정한 경우, 이 해상도가 모든 수퍼그리드 가운데 최저 해상도가 될 것입니다.
   -  RESY=value: (양의 값인) 수직 해상도입니다. 기본적으로, 그리고 RES_STRATEGY를 AUTO로 설정한 경우, 이 해상도가 모든 수퍼그리드 가운데 최저 해상도가 될 것입니다.
   -  RES_STRATEGY=AUTO/MIN/MAX/MEAN: 리샘플링된 그리드의 해상도를 설정하기 위해 적용할 전략을 선택합니다. RESX, RESY, RES_FILTER_MIN 및 RES_FILTER_MAX 모두 지정하지 않는 경우, 기본적으로 AUTO 전략이 MIN 전략에 대응할 것입니다: 모든 수퍼그리드 가운데 최저 해상도를 사용하는 전략입니다. MAX로 지정하면 모든 수퍼그리드 가운데 최고 해상도를 사용합니다. MEAN을 지정하면 모든 수퍼그리드의 평균 해상도를 사용합니다. RESX 및 RESY를 지정한 경우에는 RES_STRATEGY가 결정한 해상도를 무시할 것입니다.
   -  RES_FILTER_MIN=value: 연산에 넣을 수퍼그리드의 최저 해상도입니다. (경계가 수퍼그리드의 최저 해상도인 경우가 아니라면 경계를 제외합니다.) 기본적으로, 사용할 수 있는 수퍼그리드들 가운데 최저 해상도입니다. 이 값을 지정하고 RES_STRATEGY, RES_FILTER_MAX, RESX 또는 RESY 모두를 지정하지 않았다면, 모든 수퍼그리드 가운데 최고 해상도를 리샘플링된 그리드의 해상도로 사용할 것입니다.
   -  RES_FILTER_MAX=value: 연산에 넣을 수퍼그리드의 최고 해상도입니다. (경계 포함) 기본적으로, 사용할 수 있는 수퍼그리드들 가운데 최고 해상도입니다. 이 값을 지정하고 RES_STRATEGY, RESX 또는 RESY 모두를 지정하지 않았다면, 이 값을 리샘플링된 그리드의 해상도로 사용할 것입니다.
   -  VALUE_POPULATION=MIN/MAX/MEAN/COUNT: 리샘플링된 셀 값을 계산하기 위해 적용할 값 채우기 전략을 선택합니다. 기본값은 MAX입니다: 대상 셀의 표고값을 해당 셀 안에 들어오는 (RES_FILTER_MIN 그리고/또는 RES_FILTER_MAX로 필터링되었을 수도 있는) 모든 수퍼그리드 노드들 가운데 최고 표고값으로 설정합니다. 대응하는 불확실성(uncertainty)은 이 최고 표고가 도달하는 위치의 소스 노드의 불확실성이 될 것입니다. 어떤 수퍼그리드 노드도 대상 셀 안에 들어가지 않는 경우, NODATA 값을 설정합니다. 대상 셀과 교차하는 노드들 가운데 최저 표고값을 선택한다는 점을 제외하면, MIN 전략도 비슷합니다. MEAN 전략은 대상 셀과 교차하는 노드들의 표고값의 평균값과 해당 노드들 가운데 최고 불확실성을 사용합니다. (GDAL 3.2버전부터 사용할 수 있는) COUNT 전략은 각 대상 셀이 해당 셀 안에 들어오는 수퍼그리드 노드의 개수를 담고 있는 단일 UInt32 밴드를 노출시킵니다.
   -  SUPERGRIDS_MASK=YES/NO: 기본값은 NO입니다. YES로 설정하면, 데이터셋이 표고와 불확실성 밴드 대신 불(boolean) 값을 가진 단일 1바이트 밴드를 담습니다. 대상 셀의 경우, 해당 셀에 (RES_FILTER_MIN 그리고/또는 RES_FILTER_MAX로 필터링되었을 수도 있는) 수퍼그리드 노드가 최소한 1개 들어온다면 해당 셀의 값을 255로 설정합니다. 그렇지 않다면 0으로 설정합니다. 셀의 표고값이 NODATA 값인 이유가 해당 셀에 어떤 소스 수퍼그리드 노드도 들어오지 않기 때문인지, 또는 수퍼그리드 노드 자체가 NODATA 값인지 구별하기 위해 사용할 수 있습니다.
   -  NODATA_VALUE=value: 일반적으로 1000000인 기본값을 무시합니다.

공간 메타데이터 지원
------------------------

GDAL 3.2버전부터, GDAL은 `공간 메타데이터
<https://github.com/OpenNavigationSurface/BAG/issues/2>`_ 를 가진 BAG 파일을 노출시킬 수 있게 되었습니다.

이런 공간 데이터가 존재하는 경우, 하위 데이터셋 목록이 'BAG:"{filename}":georef_metadata:{name_of_layer}' 형태의 이름을 포함할 것입니다. 이때 ``name_of_layer`` 는 ``/BAG_root/Georef_metadata`` 아래 있는 하위 그룹의 이름입니다.

각 메타데이터 레이어 밑에 있는 ``keys`` 데이터셋의 값을 GDAL 래스터 값으로 사용합니다. 그리고 이에 대응하는 ``values`` 데이터셋을 GDAL 래스터 밴드와 관련된 GDAL 래스터 속성 테이블로써 노출시킵니다. ``keys`` 가 없는 경우, ``values`` 의 1번 레코드가 표고 밴드에서 NODATA 값과 일치하지 않는 각 표고 포인트의 값이라고 가정합니다.

변동 해상도 그리드가 존재하는 경우, MODE=LIST_SUPERGRIDS 열기 옵션이 'BAG:"{filename}":georef_metadata:{name_of_layer}:{y}:{x}' 형태의 이름들의 하위 데이터셋을 리포트하도록 할 것입니다. 이런 데이터셋을 열 때, GDAL 래스터 값을 채우기 위해 ``varres_keys`` 데이터셋을 사용할 것입니다. ``varres_keys`` 가 없는 경우, ``values`` 의 1번 레코드가 변동 해상도 표고 밴드에서 NODATA 값과 일치하지 않는 각 표고 포인트의 값이라고 가정합니다.

추적(tracking) 목록 지원
-----------------------

데이터셋을 벡터 모드로 (ogrinfo, ogr2ogr 등등) 열었을 때, tracking_list를 OGR 벡터 레이어로 리포트할 것입니다.

생성 지원
----------------

GDAL 2.4버전부터, BAG 드라이버가 소스 데이터셋으로부터 나온 표고 및 불확실성 밴드를 가지고 (변동 해상도 확장하지 않은) BAG 데이터셋을 생성할 수 있습니다. 소스 데이터셋은 지리참조되어야만 하며, 밴드 1개 또는 2개를 가지고 있어야만 합니다. 첫 번째 밴드를 표고 밴드로, 두 번째 밴드를 불확실성 밴드로 가정합니다. 두 번째 밴드가 없는 경우, 불확실성을 NODATA로 설정할 것입니다.

이 드라이버는 BAG XML 메타데이터를 템플릿 파일이라는 예를 들어 나타내는데, 이 템플릿 파일은 기본적으로 GDAL 데이터 정의 파일에서 찾을 수 있는 `bag_template.xml <https://raw.githubusercontent.com/OSGeo/gdal/master/data/bag_template.xml>`_ 입니다. 이 템플릿은 XML 파일에서 ${KEYNAME} 또는 ${KEYNAME:default_value} 형태로 나타나는 변수들을 담고 있습니다. 키 이름 앞에 접두어 VAR\_ 문자열을 붙인 이름을 가진 생성 옵션을 지정하면 이런 변수 이름을 대체할 수 있습니다. 현재 다음 생성 옵션들을 사용할 수 있습니다:

-  VAR_INDIVIDUAL_NAME=string: contact/CI_ResponsibleParty/individualName을 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "unknown"입니다.
-  VAR_ORGANISATION_NAME=string: contact/CI_ResponsibleParty/organisationName을 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "unknown"입니다.
-  VAR_POSITION_NAME=string: contact/CI_ResponsibleParty/positionName을 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "unknown"입니다.
-  VAR_DATE=YYYY-MM-DD: dateStamp/Date를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 현재 날짜입니다.
-  VAR_VERT_WKT=wkt_string: 수직 좌표계 용 referenceSystemInfo/MD_ReferenceSystem/referenceSystemIdentifier/RS_Identifier/code를 채우기 위한 옵션입니다. 지정하지 않는다면 그리고 입력 좌표계가 합성 좌표계가 아니라면, 기본값은 VERT_CS["unknown",VERT_DATUM["unknown", 2000]]입니다.
-  VAR_ABSTRACT=string: identificationInfo/abstract를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 비어 있는 문자열입니다.
-  VAR_PROCESS_STEP_DESCRIPTION=string: dataQualityInfo/lineage/LI_Lineage/processStep/LI_ProcessStep/description을 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "Generated by GDAL x.y.z"입니다.
-  VAR_DATETIME=YYYY-MM-DDTHH:MM:SS : dataQualityInfo/lineage/LI_Lineage/processStep/LI_ProcessStep/dateTime/DateTime을 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 현재 날짜/시간입니다.
-  VAR_RESTRICTION_CODE=enumerated_value: metadataConstraints/MD_LegalConstraints/useConstraints/MD_RestrictionCode를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "otherRestrictions"입니다.
-  VAR_OTHER_CONSTRAINTS=string: metadataConstraints/MD_LegalConstraints/otherConstraints를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "unknown"입니다.
-  VAR_CLASSIFICATION=enumerated_value: metadataConstraints/MD_SecurityConstraints/classification/MD_ClassificationCode를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "unclassified"입니다.
-  VAR_SECURITY_USER_NOTE=string: metadataConstraints/MD_SecurityConstraints/userNote를 채우기 위한 옵션입니다. 지정하지 않는 경우 기본값은 "none"입니다.

입력 데이터셋 메타데이터로부터 템플릿에서 발견되는, RES, RESX, RESY, RES_UNIT, HEIGHT, WIDTH, CORNER_POINTS 및 HORIZ_WKT 같은 기타 필수 변수들을 자동적으로 채울 것입니다.

그 외에 다음 생성 옵션들을 사용할 수 있습니다:

-  TEMPLATE=filename: 템플릿 역할을 할 수 있는 XML 파일을 가리키는 경로입니다. 이 파일은 보통 기반 bag_template.xml 파일을 사용자가 수정한 버전일 것입니다. 앞에서 본 문법과 비슷한 문법을 사용하면 앞에서 언급된 변수와는 다른 대체 가능한 변수를 담을 수 있습니다.
-  VAR_xxxx=value: 템플릿 XML에 있는 변수 ${xxxx}의 값을 지정한 값으로 대체합니다.
-  BAG_VERSION=string: /BAG_root/BAG Version에 있는 속성에 작성할 값입니다. 기본값은 1.6.2입니다.
-  COMPRESS=NONE/DEFLATE: 표고 및 불확실성 그리드를 압축할지 여부를 선택합니다. 기본값은 DEFLATE 무손실 압축 알고리즘입니다.
-  ZLEVEL=[1-9]: DEFLATE 압축 수준을 지정합니다. 기본값은 6입니다.
-  BLOCK_SIZE=value_in_pixel: HDF5 배열의 크기를 나눕니다. 기본값은 100이며, 배열의 크기가 100 미만인 경우 래스터의 최대 차원으로 설정합니다.

사용 예시
--------------

-  저해상도 모드에서 열기:

   ::

      $ gdalinfo data/test_vr.bag

      [...]
      Size is 6, 4
      [...]
        HAS_SUPERGRIDS=TRUE
        MAX_RESOLUTION_X=29.900000
        MAX_RESOLUTION_Y=31.900000
        MIN_RESOLUTION_X=4.983333
        MIN_RESOLUTION_Y=5.316667
      [...]

-  사용할 수 있는 수퍼그리드 출력하기:

   ::

      $ gdalinfo data/test_vr.bag -oo MODE=LIST_SUPERGRIDS

      [...]
      Subdatasets:
        SUBDATASET_1_NAME=BAG:"data/test_vr.bag":supergrid:0:0
        SUBDATASET_1_DESC=Supergrid (y=0, x=0) from (x=70.100000,y=499968.100000) to (x=129.900000,y=500031.900000), resolution (x=29.900000,y=31.900000)
        SUBDATASET_2_NAME=BAG:"data/test_vr.bag":supergrid:0:1
        SUBDATASET_2_DESC=Supergrid (y=0, x=1) from (x=107.575000,y=499976.075000) to (x=152.424999,y=500023.924999), resolution (x=14.950000,y=15.950000)
      [...]
        SUBDATASET_24_NAME=BAG:"data/test_vr.bag":supergrid:3:5
        SUBDATASET_24_DESC=Supergrid (y=3, x=5) from (x=232.558335,y=500077.391667) to (x=267.441666,y=500114.608334), resolution (x=4.983333,y=5.316667)
      [...]

-  특정 수퍼그리드 열기:

   ::

      $ gdalinfo BAG:"data/test_vr.bag":supergrid:3:5

-  리샘플링 모드에서 BAG를 기본 파라미터를 사용해서 변환하기(수퍼그리드들 가운데 최저 해상도 사용, MAX값 채우기 규칙):

   ::

      $ gdal_translate data/test_vr.bag -oo MODE=RESAMPLED_GRID out.tif

-  리샘플링 모드에서 BAG를 특정 그리드의 원점(origin)과 해상도를 사용해서 변환하기:

   ::

      $ gdal_translate data/test_vr.bag -oo MODE=RESAMPLED_GRID -oo MINX=80 -oo MINY=500000 -oo RESX=16 -oo RESY=16 out.tif

-  리샘플링 모드에서 BAG를 수퍼그리드 노드와 리샘플링된 데이터셋의 셀이 교차하는 위치를 나타내는 마스크를 사용해서 변환하기:

   ::

      $ gdal_translate data/test_vr.bag -oo MODE=RESAMPLED_GRID -oo SUPERGRIDS_MASK=YES out.tif

-  리샘플링 모드에서 BAG를 수퍼그리드 해상도를 필터링해서 변환하기(리샘플링된 그리드는 기본적으로 4미터 해상도를 사용할 것입니다):

   ::

      $ gdal_translate data/test_vr.bag -oo MODE=RESAMPLED_GRID -oo RES_FILTER_MIN=4 -oo RES_FILTER_MAX=8 out.tif

-  GeoTIFF 파일을 BAG 데이터셋으로 변환하고, ABSTRACT 대체 가능 변수에 사용자 지정 값을 지정하기:

   ::

      $ gdal_translate in.tif out.bag -co "VAR_ABSTRACT=My abstract"

-  리샘플링 모드에서 (변동 해상도) BAG를 특정 그리드 해상도(5m)를 사용해서 (변동 해상도 확장하지 않은) BAG 데이터셋으로 변환하고, ABSTRACT 메타데이터에 사용자 지정 값을 지정하기:

   ::

      $ gdal_translate data/test_vr.bag -oo MODE=RESAMPLED_GRID -oo RESX=5 -oo RESY=5 out.bag -co "VAR_ABSTRACT=My abstract"

-  추적 목록을 출력하기:

   ::

      $ ogrinfo -al data/my.bal

참고
--------

-  ``gdal/frmts/hdf5/bagdataset.cpp`` 로 구현되었습니다.
-  `오픈 수면 항해 프로젝트(The Open Navigation Surface Project) <http://www.opennavsurf.org>`_
-  `수심 측량 속성 그리드(BAG) 객체 버전 1.6 설명서 <https://github.com/OpenNavigationSurface/BAG/raw/master/docs/BAG_FSD_Release_1.6.3.doc>`_
-  `BAG 파일 용 변동 해상도 그리드 확장 <https://github.com/OpenNavigationSurface/BAG/raw/master/docs/VariableResolution/2017-08-10_VariableResolution.docx>`_
