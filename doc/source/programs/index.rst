.. _programs:

================================================================================
프로그램
================================================================================

래스터 프로그
---------------

.. toctree::
   :maxdepth: 1
   :hidden:

   공통 옵션 <raster_common_options>
   gdalinfo
   gdal_translate
   gdaladdo
   gdalwarp
   gdaltindex
   gdalbuildvrt
   gdal_contour
   gdaldem
   rgb2pct
   pct2rgb
   gdalattachpct
   gdal_merge
   gdal2tiles
   gdal2xyz
   gdal_rasterize
   gdaltransform
   nearblack
   gdal_retile
   gdal_grid
   gdal_proximity
   gdal_polygonize
   gdal_sieve
   gdal_fillnodata
   gdallocationinfo
   gdalsrsinfo
   gdalmove
   gdal_edit
   gdal_calc
   gdal_pansharpen
   gdal-config
   gdalmanage
   gdalcompare
   gdal_viewshed
   gdal_create

.. only:: html

    - :ref:`공통 옵션 <raster_common_options>`
    - :ref:`gdalinfo`: 래스터 데이터셋에 대한 정보를 목록화합니다.
    - :ref:`gdal_translate`: 래스터 데이터를 서로 다른 포맷으로 변환합니다.
    - :ref:`gdaladdo`: 오버뷰 이미지를 작성 또는 재작성합니다.
    - :ref:`gdalwarp`: 이미지 재투영 및 왜곡 유틸리티입니다.
    - :ref:`gdaltindex`: OGR 지원 데이터셋을 래스터 타일인덱스로 작성합니다.
    - :ref:`gdalbuildvrt`: 데이터셋 목록으로부터 VRT를 작성합니다.
    - :ref:`gdal_contour`: 래스터 표고 모델로부터 벡터 등고선을 작성합니다.
    - :ref:`gdaldem`: DEM을 분석하고 가시화하는 도구입니다.
    - :ref:`rgb2pct`: 24비트 RGB 이미지를 8비트 색상표 이미지로 변환합니다.
    - :ref:`pct2rgb`: 8비트 색상표 이미지를 24비트 RGB 이미지로 변환합니다.
    - :ref:`gdalattachpct`: 래스터 파일에 입력 파일에서 나온 색상표를 첨부합니다.
    - :ref:`gdal_merge`: 이미지 집합을 모자이크처럼 맞춥니다.
    - :ref:`gdal2tiles`: TMS 타일, KML 및 단순 웹 뷰어를 가진 디렉터리를 생성합니다.
    - :ref:`gdal2xyz`: 래스터 파일을 xyz 포맷으로 변환합니다.
    - :ref:`gdal_rasterize`: 벡터 도형을 래스터로 굽습니다.
    - :ref:`gdaltransform`: 좌표를 변환합니다.
    - :ref:`nearblack`: 근사 검은색/하얀색 경계를 검은색으로 변환합니다.
    - :ref:`gdal_retile`: 타일 집합을 재배열 그리고/또는 타일화된 피라미드 수준을 작성합니다.
    - :ref:`gdal_grid`: 산포되어 있는 데이터로부터 정규 그리드를 생성합니다.
    - :ref:`gdal_proximity`: 래스터 근접성 맵을 생산합니다.
    - :ref:`gdal_polygonize`: 래스터로부터 폴리곤 피처 레이어를 생산합니다.
    - :ref:`gdal_sieve`: 래스터 폴리곤 조각을 제거합니다.
    - :ref:`gdal_fillnodata`: 래스터 영역을 경계로부터 보간해서 채웁니다.
    - :ref:`gdallocationinfo`: 래스터 쿼리 도구입니다.
    - :ref:`gdalsrsinfo`: 여러 포맷(WKT, PROJ.4 등등)으로 된 입력 SRS에 대한 정보를 목록화합니다.
    - :ref:`gdalmove`: 래스터 파일의 지리참조를 제자리 변환합니다.
    - :ref:`gdal_edit`: 기존 GDAL 데이터셋의 여러 가지 정보를 제자리 편집합니다.
    - :ref:`gdal_calc`: 넘파이 문법을 따르는 명령줄 래스터 계산기입니다.
    - :ref:`gdal_pansharpen`: 영상융합 작업을 수행합니다.
    - :ref:`gdal-config`: GDAL 설치에 대한 여러 가지 정보를 결정합니다.
    - :ref:`gdalmanage`: 래스터 데이터 파일을 식별, 삭제, 재명명, 복사합니다.
    - :ref:`gdalcompare`: 이미지 2개를 비교합니다.
    - :ref:`gdal_viewshed`: 래스터 용 가시성 마스크를 계산합니다.
    - :ref:`gdal_create`: 래스터 파일을 (소스 데이터셋 없이) 생성합니다.

다중차원 래스터 프로그램
--------------------------------

.. toctree::
   :maxdepth: 1
   :hidden:

   gdalmdiminfo
   gdalmdimtranslate

.. only:: html

    - :ref:`gdalmdiminfo`: 다중차원 데이터셋의 구조 및 내용을 리포트합니다.
    - :ref:`gdalmdimtranslate`: 다중차원 데이터를 서로 다른 포맷으로 변환하고, 하위 집합을 작성합니다.

벡터 프로그램
---------------

.. toctree::
   :maxdepth: 1
   :hidden:

   공통 옵션 <vector_common_options>
   ogrinfo
   ogr2ogr
   ogrtindex
   ogrlineref
   ogrmerge

.. only:: html

    - :ref:`공통 옵션 <vector_common_options>`
    - :ref:`ogrinfo`: OGR 지원 데이터소스에 대한 정보를 목록화합니다.
    - :ref:`ogr2ogr`: 단순 피처 데이터를 서로 다른 포맷으로 변환합니다.
    - :ref:`ogrtindex`: 타일인덱스를 생성합니다.
    - :ref:`ogrlineref`: 선형 참조를 생성하고 이를 이용한 몇몇 계산을 제공합니다.
    - :ref:`ogrmerge`: 벡터 데이터셋 몇 대를 단일 데이터셋으로 병합합니다.

지리 네트워크 프로그램
---------------------------

.. toctree::
   :maxdepth: 1
   :hidden:

   gnmmanage
   gnmanalyse

.. only:: html

    - :ref:`gnmmanage`: 네트워크를 관리합니다.
    - :ref:`gnmanalyse`: 네트워크를 분석합니다.
