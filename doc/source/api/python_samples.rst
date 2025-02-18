.. _python_samples:

================================================================================
파이썬 샘플 스크립트
================================================================================

다음은 GDAL의 파이썬 인터페이스를 사용하는 방법을 알려주기 위한 샘플 스크립트들입니다. 사용자의 응용 프로그램에서 마음대로 사용해주십시오.

GDAL 3.2버전부터, 'osgeo_utils' 모듈 안에 :ref:`programs` 파이썬 유틸리티 스크립트를 포함시켰습니다.
GDAL 3.3버전부터, 'osgeo_utils.samples' 하위 모듈 안에 파이썬 샘플 스크립트를 포함시켰습니다.

파이썬 래스터 샘플 스크립트
---------------------------

.. only:: html

    - assemblepoly: 원호들로부터 폴리곤을 조립하는 방법을 보여주는 스크립트입니다. OGR 파이썬 API의 다양한 측면을 보여줍니다.
    - fft: 2차원 고속 푸리에 변환 및 역변환을 수행하는 스크립트입니다.
    - gdal2grd: GDAL이 지원하는 모든 소스로부터 (골든소프트웨어 Surfer에서 사용되는) 아스키 GRD 래스터를 작성하는 스크립트입니다.
    - gdal_vrtmerge: gdal_merge와 유사하지만, VRT 파일을 생성합니다.
    - gdalcopyproj: 한 래스터 데이터셋으로부터 다른 데이터셋으로 지리변형(geotransform), 투영법 그리고/또는 GCP를 복제합니다. 지리참조 정보 메타데이터를 무시하거나 폐기하는 다른 소프트웨어로 이미지를 수정한 경우 유용한 스크립트입니다.
    - gdalfilter: GDAL을 이용해서 이미지에 커널 기반 필터를 적용하는 예시 스크립트입니다. 가상 파일을 중간(intermediate) 표현으로 사용하는 방법을 보여줍니다.
    - get_soundg: S-57 파일로부터 shapefile로 SOUNDG 레이어를 -- MULTIPOINT 도형을 가진 피처를 수많은 POINT 피처로 분할하고 포인트 표고를 속성으로 추가해서 -- 복사하는 스크립트입니다.
    - histrep: 래스터 여러 개로부터 산출물 하나로 데이터를 추출하는 모듈입니다.
    - load2odbc: ODBC 데이터 저장소에 ODBC 테이블을 불러옵니다. OGR의 경우 ODBC 드라이버가 읽기 전용이기 때문에 직접 SQL(Direct SQL)을 사용합니다.
    - rel: 표고 데이터로부터 음영기복도를 생성하는 스크립트입니다. (현재 gdaldem에 비슷한 기능이 있습니다.)
    - tigerpoly: TIGER/Line 데이터소스에서 원호들로부터 폴리곤을 조립해서 결과물을 새로 생성되는 shapefile로 작성하는 방법을 보여주는 스크립트입니다.
    - tolatlong: 입력 파일로부터 좌표계와 지리변형 행렬을 읽어와서 지정한 픽셀의 위도/경도 좌표를 리포트하는 스크립트입니다.
    - val_repl: 입력 래스터 파일에서 지정한 값을 새 값으로 대체하는 스크립트입니다. NODATA를 표시하기 위해 쓰인 값이 마음에 들지 않아 다른 값으로 대체하려는 경우 유용할 수 있습니다. 입력 파일을 건드리지 않고 결과물을 다른 파일로 저장합니다.
    - vec_tr: 파일에 있는 모든 도형에 고정 오프셋 같은 알고리즘을 적용하는 예시입니다.
    - vec_tr_spat: 지정한 직사각형과 정말로 교차하는 피처만을 기반으로 필터링하는 Intersect() 메소드를 사용하는 예시입니다. 일반 폴리곤으로 쉽게 확장할 수 있습니다!
    - classify: NumPy를 사용해서 이미지의 범주 기반 단순 범위를 생성하는 방법을 보여주는 스크립트입니다. 내용이 하드코딩된 유일한 예시입니다.
    - gdal_lut: 텍스트 파일로부터 LUT(Look-Up-Table)를 읽어와서 이미지에 적용하는 스크립트입니다. 일종의 '밴드 1개' pct2rgb 버전입니다.
    - magphase: 복잡 이미지로부터 이미지 규모(magnitude) 및 단계(phase) 이미지를 계산하는 예시 스크립트입니다.
    - hsv_merge: 회색조 이미지를 HSV 공간의 강도(intensity)로서 RGB 이미지로 병합하는 스크립트입니다.
    - gdal_ls: /vsicurl 또는 /vsizip 같은 가상 디렉터리에 있는 파일들의 목록을 출력하는 스크립트입니다.
    - gdal_cp: 가상 파일을 복사하는 스크립트입니다.

파이썬 벡터 샘플 스크립트
-------------------------

.. only:: html

    - ogrupdate: 대상 데이터소스를 소스 데이터소스의 피처로 업데이트합니다. ogr2ogr와는 반대로, 이 스크립트는 새 피처를 생성해야 할지 또는 기존 피처를 업데이트해야 할지 결정하기 위해 데이터소스 간의 피처들을 일치시키려 시도합니다.
    - ogr_layer_algebra: OGR 레이어 대수(algebra) 연산을 실행하기 위한 응용 프로그램입니다.
    - ogr_dispatch: 어떤 필드의 값 또는 도형 유형에 따라 레이어에 피처를 넣습니다.
    - wcs_virtds_params: 혼합 공간 좌표계를 가진 타일 색인(tileindex)으로부터 MapServer WCS 레이어 정의를 생성합니다.
    - ogr_build_junction_table: _href 헤더에서 다른 객체를 참조하는 GML 데이터소스로부터 나오는 레이어를 위한 연결 테이블을 생성합니다.
    - gcps2ogr: GDAL GCP를 OGR 포인트로 산출합니다.


파이썬 좌표계 샘플 스크립트
---------------------------

.. only:: html

    - crs2crs2grid: HTDP 프로그램으로부터 PROJ.4 그리드 이동(grid shift) 파일을 생성하는 스크립트입니다.

C++ 프로그램의 파이썬 직접 포트
-------------------------------

.. only:: html

    - :ref:`gdalinfo`: 'apps/gdalinfo.c'의 직접 포트입니다.
    - :ref:`ogrinfo`: 'apps/ogrinfo.cpp'의 직접 포트입니다.
    - :ref:`ogr2ogr`: 'apps/ogr2ogr.cpp'의 직접 포트입니다.
    - :ref:`gdallocationinfo`: 'apps/gdallocationinfo.cpp'의 직접 포트입니다.

현재 프로그램이 된 파이썬 샘플 스크립트
---------------------------------------

다음 GDAL 버전에서 샘플 스크립트가 추가 기능 및 문서를 가진 공식 GDAL 유틸리티(프로그램)로 업그레이드될 수도 있습니다. 이전 버전의 다음 샘플 스크립트들이 현재 프로그램으로 업그레이드되었습니다:

.. only:: html

    - :ref:`gdal2xyz`: 래스터 파일을 XYZ 포맷으로 변환합니다.
    - :ref:`gdal_retile`: 정규 타일 트리에서 데이터를 재구성하는 스크립트입니다.
    - val_at_coord: :ref:`gdallocationinfo` 를 참조하십시오.

