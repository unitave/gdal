.. _gdalwarp:

================================================================================
gdalwarp
================================================================================

.. only:: html

    이미지 재투영 및 왜곡 유틸리티

.. Index:: gdalwarp

개요
--------

.. code-block::

    gdalwarp [--help-general] [--formats]
        [-s_srs srs_def] [-t_srs srs_def] [-ct string] [-to "NAME=VALUE"]* [-vshift | -novshift]
        [[-s_coord_epoch epoch] | [-t_coord_epoch epoch]]
        [-order n | -tps | -rpc | -geoloc] [-et err_threshold]
        [-refine_gcps tolerance [minimum_gcps]]
        [-te xmin ymin xmax ymax] [-te_srs srs_def]
        [-tr xres yres] [-tap] [-ts width height]
        [-ovr level|AUTO|AUTO-n|NONE] [-wo "NAME=VALUE"] [-ot Byte/Int16/...] [-wt Byte/Int16]
        [-srcnodata "value [value...]"] [-dstnodata "value [value...]"]
        [-srcalpha|-nosrcalpha] [-dstalpha]
        [-r resampling_method] [-wm memory_in_mb] [-multi] [-q]
        [-cutline datasource] [-cl layer] [-cwhere expression]
        [-csql statement] [-cblend dist_in_pixels] [-crop_to_cutline]
        [-if format]* [-of format] [-co "NAME=VALUE"]* [-overwrite]
        [-nomd] [-cvmd meta_conflict_value] [-setci] [-oo NAME=VALUE]*
        [-doo NAME=VALUE]*
        srcfile* dstfile

설명
-----------

:program:`gdalwarp` 유틸리티는 이미지를 모자이크(타일 분할), 재투영, 왜곡(warp)하는 유틸리티입니다. 이 프로그램은 이미지를 지원하는 어떤 투영법으로든 재투영할 수 있고, 이미지가 기준 정보를 가진 "원본(raw)"일 경우 이미지에 저장된 GCP도 적용할 수 있습니다.

.. program:: gdalwarp

.. option:: -s_srs <srs def>

    소스 공간 좌표계를 설정합니다. 지정하지 않으면 입력 데이터셋에서 검색된 공간 좌표계를 사용할 것입니다.

    .. include:: options/srs_def_gdalwarp.rst

.. option:: -s_coord_epoch <epoch>

    .. versionadded:: 3.4

    소스 공간 좌표계와 링크된 시대 좌표(coordinate epoch)를 할당합니다. 소스 공간 좌표계가 동적 좌표계(dynamic CRS)인 경우 유용합니다. :option:`-s_srs` 와 함께 사용할 경우에만 작동합니다.

    현재 :option:`-s_coord_epoch` 와 :option:`-t_coord_epoch` 는 함께 사용할 수 없습니다. 두 동적 좌표계 사이의 변환을 충분히 지원하지 않기 때문입니다.

.. option:: -t_srs <srs_def>

    대상(target) 공간 좌표계를 설정합니다.

    재투영이 일어나려면 소스 공간 좌표계를 사용할 수 있어야만 합니다. 소스 공간 좌표계를 사용할 수 있는 경우 입력 데이터셋에서 기본적으로 검색되는 좌표계일 것이고, 또는 사용자가 :option:`-s_srs` 옵션으로 우선시키는 좌표계가 될 것입니다.

    .. include:: options/srs_def_gdalwarp.rst

.. option:: -t_coord_epoch <epoch>

    .. versionadded:: 3.4

    대상(target) 공간 좌표계와 링크된 시대 좌표(coordinate epoch)를 할당합니다. 대상 공간 좌표계가 동적 좌표계(dynamic CRS)인 경우 유용합니다. :option:`-t_srs` 와 함께 사용할 경우에만 작동합니다.

    현재 :option:`-s_coord_epoch` 와 :option:`-t_coord_epoch` 는 함께 사용할 수 없습니다. 두 동적 좌표계 사이의 변환을 충분히 지원하지 않기 때문입니다.

.. option:: -ct <string>

    PROJ 문자열(한 단계 작업 또는 +proj=pipeline으로 시작하는 여러 단계 작업 문자열)로, CoordinateOperation을 설명하는 WKT2 문자열, 또는 소스로부터 대상 좌표계로의 기본 변환을 무시하는 urn:ogc:def:coordinateOperation:EPSG::XXXX URN입니다. 소스 및 대상 좌표계의 축 순서를 고려해야만 합니다.
    
    .. versionadded:: 3.0

.. option:: -to <NAME=VALUE>

    :cpp:func:`GDALCreateGenImgProjTransformer2` 에 전송하기에 적합한 변환기(transformer) 옵션을 설정합니다. RPC 특화 옵션을 알고 싶다면 :cpp:func:`GDALCreateRPCTransformerV2()` 를 읽어보십시오.

.. option:: -vshift

    수직 이동을 강제로 사용시킵니다. 일반적으로 이 옵션이 필요하지는 않지만, 명확한 좌표 변환(:option:`-ct`)을 사용하면서 명확한 소스 및 대상 공간 좌표계를 지정하지 않는 경우 필요합니다.

    .. versionadded:: 3.4

.. option:: -novshift

    소스 또는 대상 공간 좌표계 가운데 하나가 명확한 수직 데이터를 가지고 있고 입력 데이터셋이 단일 밴드 데이터셋인 경우 수직 이동 사용을 비활성화합니다.

    .. note:: GDAL 2.2에서 3.3까지는 이 옵션을 ``-novshiftgrid`` 라고 했습니다.

    .. versionadded:: 3.4

.. option:: -order <n>

    왜곡 작업에 쓰이는 다항(polynomial)의 순서(1에서 3까지)입니다. 기본값은 GCP 개수를 기반으로 하는 다항 순서를 선택하는 것입니다.

.. option:: -tps

    사용할 수 있는 GCP를 기반으로 박막 스플라인(thin plate spline) 변환기를 강제로 사용시킵니다.

.. option:: -rpc

    RPC를 강제로 사용시킵니다.

.. option:: -geoloc

    지리위치 배열(Geolocation Array)를 강제로 사용시킵니다.

.. option:: -et <err_threshold>

    변환 근사치의 오류 한계값입니다. (픽셀 단위로 기본값은 0.125입니다. 다만 GDAL 2.1버전부터 RPC_DEM 변환기 옵션을 지정한 경우, 예를 들어 err_threshold=0처럼 정확한 변환기를 사용할 것입니다.)

.. option:: -refine_gcps <tolerance minimum_gcps>

    자동적으로 이상값(outlier)을 제거해서 GCP를 개선합니다. minimum_gcps가 남을 때까지 또는 어떤 이상값도 탐지되지 않을 때까지 이상값을 제거할 것입니다. GCP를 제거할 경우 조정하기 위해 허용 오차를 전송합니다. GCP 개선이 다항 보간으로만 작동한다는 의미는 아닙니다. 어떤 투영법도 사용할 수 없는 경우 허용 오차는 픽셀 단위이며, 그렇지 않은 경우 공간 좌표계 단위입니다. minimum_gcps를 지정하지 않는 경우, 다항 모델에 따른 최소 GCP 개수를 사용합니다.

.. option:: -te <xmin ymin xmax ymax>

    산출물 파일의 지리참조 범위를 생성하도록 설정합니다. (기본적으로 대상 공간 좌표계 단위이지만, :option:`-te_srs` 로 공간 좌표계를 지정할 수도 있습니다.)

.. option:: -te_srs <srs_def>

    -te로 입력한 좌표를 해석할 공간 좌표계를 지정합니다. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다. 이 옵션을 산출 데이터셋의 대상 공간 좌표계인 -t_srs와 절대 혼동해서는 안 됩니다. 산출물의 좌표계가 측지(geodetic) 경도/위도 공간 좌표계라는 것을 알고 있지만, 그래도 투영 좌표계로 된 결과물을 원하는 경우 이 :option:`-te_srs` 가 편리합니다.

.. option:: -tr <xres> <yres>

    산출물 파일의 해상도를 (대상의 지리참조 단위로) 설정합니다.

    지정하지 않는 경우 (또는 -te 및 -ts로부터 추정되지 않는 경우) gdalwarp는 재투영을 사용하지 않는 상황이더라도 xres=yres인 산출 래스터를 생성할 것입니다.

.. option:: -tap

    (대상 정렬 픽셀(target aligned pixels)) 정렬된 범위가 최소 범위를 포함하도록, 산출물 파일의 범위 좌표를 :option:`-tr` 의 값들에 정렬시킵니다.

.. option:: -ts <width> <height>

    산출물 파일의 크기를 픽셀과 행 단위로 설정합니다. width 또는 height를 0으로 설정하면, 계산된 해상도에서 나머지 차원을 추정할 것입니다. :option:`-ts` 와 :option:`-tr` 을 함께 사용할 수 없다는 사실을 기억하십시오.

.. option:: -ovr <level|AUTO|AUTO-n|NONE>

    소스 파일의 어느 오버뷰 수준을 사용해야만 하는지를 지정합니다. 기본값인 AUTO는 대상 해상도에 가장 가까운 해상도를 가진 오버뷰 수준을 선택할 것입니다. 특정 수준을 선택하려면 정수값을 (0에서 시작합니다. 예를 들어 0이 첫 번째 오버뷰 수준입니다) 지정하십시오. 수준이 AUTO가 선택한 수준보다 아래인 오버뷰를 선택하려면 정수 n이 1 이상인 AUTO-n을 지정하십시오. 또는 NONE을 지정하는 경우 기반(base) 해상도를 강제로 사용합니다. (저품질 리샘플링 메소드로 오버뷰를 생성했고, 더 높은 품질의 리샘플링 메소드로 왜곡 작업을 한 경우 유용할 수 있습니다.)

.. option:: -wo `"NAME=VALUE"`

    왜곡(warp) 옵션을 설정합니다. :cpp:member:`GDALWarpOptions::papszWarpOptions` 문서에서 모든 옵션을 설명하고 있습니다. :option:`-wo` 옵션 여러 개를 목록화할 수도 있습니다.

.. include:: options/ot.rst

.. option:: -wt <type>

    픽셀 데이터 유형을 작업합니다. 소스 이미지와 대상 이미지 버퍼의 픽셀 데이터 유형을 설정합니다.

.. option:: -r <resampling_method>

    사용할 리샘플링 메소드를 선택합니다. 다음 메소드를 이용할 수 있습니다:

    ``near``: 최근접 이웃 리샘플링 (기본값, 최속(fastest) 알고리즘, 최저 보간 품질)

    ``bilinear``: 이중선형 리샘플링

    ``cubic``: 3차 리샘플링

    ``cubicspline``: 3차 스플라인 리샘플링

    ``lanczos``: 란초시 창함수 싱크 리샘플링

    ``average``: 평균 리샘플링, NODATA가 아닌 모든 기여 픽셀(contributing pixel)의 가중치 평균을 계산합니다.

    ``rms`` NODATA가 아닌 모든 기여 픽셀의 제곱평균제곱근(root mean squared)/이차평균(quadratic mean)을 계산합니다. (GDAL 3.3버전 이상)

    ``mode``: 모드 리샘플링, 샘플링된 모든 포인트들에서 가장 출현 빈도가 높은 값을 선택합니다. 가장 출현 빈도가 높은 값들이 동수인 경우, 모드로 식별된 첫 번째 값을 선택할 것입니다.

    ``max``: 최대값 리샘플링, NODATA가 아닌 모든 기여 픽셀 가운데 최대값을 선택합니다.

    ``min``: 최소값 리샘플링, NODATA가 아닌 모든 기여 픽셀 가운데 최소값을 선택합니다.

    ``med``: 중간값 리샘플링, NODATA가 아닌 모든 기여 픽셀 가운데 중간값(median)을 선택합니다.

    ``q1``: 제1 사분위수 리샘플링, NODATA가 아닌 모든 기여 픽셀 가운데 제1 사분위수(first quartile) 값을 선택합니다.

    ``q3``: 제3 사분위수 리샘플링, NODATA가 아닌 모든 기여 픽셀 가운데 제3 사분위수(third quartile) 값을 선택합니다.

    ``sum``: NODATA가 아닌 모든 기여 픽셀의 가중치 합을 계산합니다. (GDAL 3.1버전부터)

.. option:: -srcnodata <value [value...]>

    입력 밴드에 대한 NODATA 마스크 값을 설정합니다. (각 밴드 별로 서로 다른 값을 지정할 수 있습니다.) 값을 하나 이상 지정하는 경우 모든 값들을 단일 운영체제 인수로써 따옴표로 묶어주어야 합니다. 마스크 처리된 값은 보간에 쓰이지 않을 것입니다. 소스 데이터셋 상의 고유한 NODATA 설정을 무시하려면 ``None`` 이라는 값을 사용하십시오.

    이 옵션을 ``None`` 이 아닌 값으로 설정하면, ``UNIFIED_SRC_NODATA`` 왜곡 옵션을 명확하게 설정하지 않는 경우 ``YES`` 로 설정됩니다. (:cpp:member:`GDALWarpOptions::papszWarpOptions` 참조)

    ``-srcnodata`` 를 명확하게 설정하지 않았지만 소스 데이터셋이 NODATA 값을 가지고 있다면, ``UNIFIED_SRC_NODATA`` 가 기본적으로 ``PARTIAL`` 로 설정된 채 소스 데이터셋의 NODATA 값을 사용하게 될 것입니다.

.. option:: -dstnodata <value [value...]>

    산출 밴드에 대한 NODATA 값을 설정합니다. (각 밴드 별로 서로 다른 값을 지정할 수 있습니다.) 값을 하나 이상 지정하는 경우 모든 값들을 단일 운영체제 인수로써 따옴표로 묶어주어야 합니다. 새 파일은 이 값으로 초기화되고, 가능하다면 산출물 파일에 NODATA 값을 기록할 것입니다. NODATA가 정의되지 않도록 하려면 ``None`` 이라는 값을 사용하십시오. 이 인수를 사용하지 않는 경우 소스 데이터셋에서 NODATA 값을 복사할 것입니다.

.. option:: -srcalpha

    소스 이미지의 마지막 밴드를 소스 알파 밴드로 간주하도록 강제합니다.

.. option:: -nosrcalpha

    소스 이미지의 알파 밴드를 알파 밴드로 간주하지 않도록 방지합니다. (정규 밴드로 왜곡될 것입니다.)

    .. versionadded:: 2.2

.. option:: -dstalpha

    NODATA (미설정/투명) 픽셀을 식별하기 위한 산출 알파 밴드를 생성합니다.

.. option:: -wm <memory_in_mb>

    왜곡 API가 캐시 작업에 사용할 수 있는 메모리 용량을 설정합니다. 값이 10,000 미만인 경우 설정 값을 메가바이트로 해석합니다. 설정 값이 10,000 이상이면 바이트로 해석합니다.

.. option:: -multi

    멀티스레드 왜곡 작업 구현을 사용합니다. 이미지 덩어리를 처리하고 입력/산출 작업을 동시에 수행하기 위해 스레드 2개를 사용할 것입니다. 계산은 멀티스레드 자체가 아니라는 점을 기억하십시오. 계산을 멀티스레드로 수행하려면, :option:`-wo` NUM_THREADS=val/ALL_CPUS 옵션을 사용하면 됩니다. 이 옵션은 :option:`-multi` 와 함께 결합할 수 있습니다.

.. option:: -q

    효과음을 내지 않습니다.

.. include:: options/if.rst

.. include:: options/of.rst

.. include:: options/co.rst

.. option:: -cutline <datasource>

    지정한 OGR 지원 데이터소스에서 혼합 커트라인(blend cutline)을 사용할 수 있게 활성화합니다.

.. option:: -cl <layername>

    커트라인 데이터소스에서 지정한 레이어를 선택합니다.

.. option:: -cwhere <expression>

    속성 쿼리를 기반으로 원하는 커트라인 객체를 제한합니다.

.. option:: -csql <query>

    커트라인 객체를 :option:`-cl` 로 레이어에서 선택하는 대신 SQL 쿼리를 이용해서 선택합니다.

.. option:: -cblend <distance>

    커트라인들을 혼합하기 위해 사용할 혼합 거리를 (픽셀 단위로) 설정합니다.

.. option:: -crop_to_cutline

    대상 데이터셋의 범위를 커트라인의 범위로 잘라냅니다.

.. option:: -overwrite

    대상 데이터셋이 이미 존재하는 경우 대상 데이터셋을 덮어씁니다. 이때 덮어쓰기란 파일을 삭제한 다음 처음부터 다시 생성한다는 의미라는 것을 이해해야만 합니다. 이 옵션을 지정하지 *않았는데* 산출물 파일이 이미 존재한다면, 제자리(in place) 업데이트될 것입니다.

.. option:: -nomd

    메타데이터를 복사하지 않습니다. 이 옵션을 사용하지 않는다면, 첫 번째 소스 데이터셋으로부터 데이터셋과 밴드 메타데이터(는 물론 밴드 정보 일부)를 복사할 것입니다. 소스 데이터셋들 사이에 차이가 나는 항목들은 *로 설정될 것입니다. (:option:`-cvmd` 참조)

.. option:: -cvmd <meta_conflict_value>

    소스 데이터셋들 사이에서 충돌하는 메타데이터 항목들을 설정하기 위한 값입니다. (기본값은 "*"입니다.) 충돌하는 항목들을 제거하려면 ""을 사용하십시오.

.. option:: -setci

    대상 데이터셋 밴드의 색상 해석을 소스 데이터셋으로부터 설정합니다.

.. option:: -oo <NAME=VALUE>

    데이터셋 열기 옵션 (특정 포맷 지원)

.. option:: -doo <NAME=VALUE>

    산출 데이터셋 열기 옵션 (특정 포맷 지원)

    .. versionadded:: 2.1

.. option:: <srcfile>

    소스 파일명(들).

.. option:: <dstfile>

    대상 파일명.

산출 파일이 이미 존재하는 경우 기존 산출 파일로 모자이크(타일 분할) 작업을 수행할 수 있습니다. 새 데이터를 수용하기 위해 기존 파일의 공간 범위를 수정하지는 않을 것입니다. 따라서 이런 경우 기존 파일을 제거하거나, -overwrite 옵션을 사용해야 할 수도 있습니다.

혼합 작업을 포함, 업데이트될 수도 있는 대상 파일의 영역을 제한하기 위해 폴리곤 커트라인을 마스크로 사용할 수도 있습니다. 커트라인 객체를 담고 있는 OGR 레이어가 명확한 공간 좌표계를 가지고 있지 않다면, 커트라인 객체는 대상 파일의 공간 좌표계를 사용해야만 합니다. 아직 존재하지 않는 대상 데이터셋을 작성하는 경우, -te 또는 -crop_to_cutline을 지정하지 않는 이상 대상 파일의 범위는 원본 래스터의 범위가 될 것입니다.

GDAL 3.1버전부터, CreateCopy 작업만 지원하는 드라이버를 산출물 포맷으로 사용할 수 있습니다. 임시 파일을 내부적으로 생성할 수도 있다는 뜻입니다.

예시
--------

- 기본 변환:

::

  gdalwarp -t_srs EPSG:4326 input.tif output.tif


- 예를 들어 GeoTIFF로 저장된, GCP가 모서리를 위도/경도로 매핑하는 8비트 SPOT 영상을 다음과 같은 명령어로 UTM 투영으로 왜곡할 수 있습니다:

::

    gdalwarp -t_srs '+proj=utm +zone=11 +datum=WGS84' -overwrite raw_spot.tif utm11.tif

- 예를 들어 HDF로 저장된, GCP가 모서리를 위도/경도로 매핑하는 ASTER 이미지를 다음과 같은 명령어로 UTM 투영으로 왜곡할 수 있습니다:

    .. versionadded:: 2.2

::

    gdalwarp -overwrite HDF4_SDS:ASTER_L1B:"pg-PR1B0000-2002031402_100_001":2 pg-PR1B0000-2002031402_100_001_2.tif

- 지리참조되지 않은 이미지에 커트라인을 적용하고 픽셀(220,60)에서 픽셀(1160,690)까지 잘라내려면:

::

    gdalwarp -overwrite -to SRC_METHOD=NO_GEOTRANSFORM -to DST_METHOD=NO_GEOTRANSFORM -te 220 60 1160 690 -cutline cutline.csv in.png out.tif

이때 cutline.csv 내용은 다음과 비슷합니다:

::

    id,WKT
    1,"POLYGON((....))"

- (EGM96을 사용하는) 지오이드 표고에서 WGS84 타원체 고도로 DEM을 변환하려면:

    .. versionadded:: 2.2

::

    gdalwarp -overwrite in_dem.tif out_dem.tif -s_srs EPSG:4326+5773 -t_srs EPSG:4979


참고
--------

`gdalwarp의 옵션 및 습성을 토의하는 위키 페이지 <http://trac.osgeo.org/gdal/wiki/UserDocs/GdalWarp>`_
