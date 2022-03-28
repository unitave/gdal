.. _raster.rasterlite:

================================================================================
Rasterlite - SQLite 데이터베이스 래스터
================================================================================

.. shortname:: Rasterlite

.. build_dependencies:: libsqlite3

Rasterlite 드라이버는 Rasterlite 데이터베이스 읽기 및 생성을 지원합니다.

-  rasterlite_load, rasterlite_pyramids 등과 같은 `Rasterlite <http://www.gaia-gis.it/spatialite>`_ 유틸리티를 사용하면 이런 데이터베이스를 생성할 수 있습니다.

-  이 드라이버는 GIF, PNG, TIFF 또는 JPEG 타일로 저장된 회색조, 색상표 및 RGB 이미지의 읽기를 지원합니다. 오버뷰/피라미드, 공간 좌표계 및 공간 범위도 읽어올 수 있습니다.

GDAL/OGR를 OGR SQLite 드라이버 지원과 함께 컴파일해야만 합니다. 읽기 지원의 경우 SpatiaLite 라이브러리에 대한 링크 작업은 필요없지만, Rasterlite 데이터베이스를 읽기 위해서는 충분히 최신인 SQLite3 라이브러리가 필요합니다. Rasterlite 라이브러리에 대한 링크 작업도 필요없습니다.

새 테이블 작성 지원의 경우, SpatiaLite 라이브러리에 대한 링크 작업이 **필요합니다**.

Rasterlite 문서가 타일 용 압축 포맷으로 GIF, PNG, TIFF, JPEG만 언급하고 있기는 하지만, 이 드라이버는 GDAL이 처리할 수 있는 모든 포맷으로 된 내부 타일을 읽고 쓸 수 있습니다. 거기에 더해, Rasterlite 드라이버는 내부 타일에 드라이버가 지원하는 만큼 많은 밴드와 밴드 유형도 읽고 쓸 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

읽기 모드에서의 연결 문자열 문법
-------------------------------------

문법:

::

   'rasterlitedb_name'
   
   또는
   
   'RASTERLITE:rasterlitedb_name[,table=raster_table_prefix][,minx=minx_val,miny=miny_val,maxx=maxx_val,maxy=maxy_val][,level=level_number]'

이때:

-  *rasterlitedb_name*:
   RasterLite DB의 파일명입니다.

-  *raster_table_prefix*:
   열어야 할 래스터 테이블의 접두어입니다. 각 래스터에는 해당 래스터에 대응하는, \_rasters 및 \_metadata 접미어가 붙은 SQLite 테이블 2개가 존재합니다.

-  *minx_val,miny_val,maxx_val,maxy_val*:
   기본 범위와 다를 수도 있는 래스터의 사용자 정의 범위를 (좌표계 단위로) 설정합니다.

-  *level_number*:
   열어야 할 오버뷰/피라미드의 수준입니다. 0이 기반 피라미드입니다.

생성 문제점
---------------

이 드라이버는 필요한 경우 새 데이터베이스와 새 래스터 테이블을 생성하고, 지정한 래스터 테이블에 소스 데이터셋을 복사할 수 있습니다.

래스터 테이블에 기존 데이터가 존재하는 경우, 새 데이터를 추가할 것입니다. WIPE 생성 옵션을 YES로 설정하면 기존 데이터를 삭제할 수 있습니다.

이 드라이버는 기존 래스터 테이블에 있는 블록의 업데이트를 지원하지 않습니다. 새 데이터를 추가할 수 있을 뿐입니다.

산출 데이터셋의 명명 문법은 다음과 같습니다:

::

   'RASTERLITE:rasterlitedb_name,table=raster_table_prefix'

   또는

   'rasterlitedb_name'

그 이름을 가진 기존 데이터베이스가 존재하지 않는 경우에만 데이터베이스 이름만 후자 형태로 지정할 수 있습니다. 해당 이름을 가진 기존 데이터베이스가 존재한다면, 데이터베이스 이름 자체를 기반으로 래스터 테이블 이름을 결정할 것입니다.

생성 옵션
~~~~~~~~~~~~~~~~

-  **WIPE=YES/NO**:
   이 옵션을 YES로 설정하면 지정한 테이블에 있는 기존 데이터를 모두 삭제합니다. 기본값은 NO입니다.

-  **TILED=YES/NO**:
   래스터 테이블에 소스 데이터셋을 단일 타일로 작성해야만 하는 경우 이 옵션을 NO로 설정하십시오. 기본값은 YES입니다.

-  **BLOCKXSIZE=n**:
   타일 너비를 설정합니다. 기본값은 256입니다.

-  **BLOCKYSIZE=n**:
   타일 높이를 설정합니다. 기본값은 256입니다.

-  **DRIVER=[GTiff/GIF/PNG/JPEG/...]**:
   타일을 저장하기 위해 사용할 GDAL 드라이버의 이름입니다. 기본값은 GTiff입니다.

-  **COMPRESS=[LZW/JPEG/DEFLATE/...]**:
   (GTiff 드라이버를 설정한 경우) 압축 방식의 이름입니다.

-  **PHOTOMETRIC=[RGB/YCbCr/...]**:
   (GTiff 드라이버를 설정한 경우) 측광 해석 형식을 설정합니다.

-  **QUALITY**:
   (JPEG 압축 GTiff, JPEG 및 WEBP 드라이버를 설정한 경우) JPEG/WEBP 압축 품질을 1에서 100 사이의 값으로 설정합니다. 기본값은 75입니다.

오버뷰
---------

(데이터셋을 업데이트 모드로 연 경우) 이 드라이버는 내부 오버뷰 작성 및 읽기를 지원합니다.

내부 오버뷰를 하나도 탐지하지 못 했다면, 이 드라이버는 외부 오버뷰(.ovr 파일)을 사용하려 시도할 것입니다.

내부 오버뷰 작성을 위해 옵션을 사용할 수 있습니다. RASTERLITE_OVR_OPTIONS 환경설정 옵션을 앞에서 설명한 생성 옵션들을 쉼표로 구분한 목록으로 지정하면 됩니다. 아래 예시를 참조하십시오.

GDAL 오버뷰가 지원하는 모든 리샘플링 메소드를 사용할 수 있습니다.

성능 힌트
-----------------

OGR SQLite 드라이버를 활용하기 위한 몇몇 성능 힌트를 서술합니다. 특히 데이터셋 생성 또는 오버뷰 추가 시 OGR_SQLITE_SYNCHRONOUS 환경설정 옵션을 OFF로 설정하면 일부 파일 시스템 상에서 성능을 향상시킬 수도 있습니다.

래스터 테이블을 모두 추가하고 필요한 오버뷰 수준들을 모두 작성한 다음, 다음 명령어를 실행할 것을 권장합니다:

::

   ogrinfo rasterlitedb.sqlite -sql "VACUUM"

이 명령어는 데이터베이스를 최적화하고 읽기 성능을 향상시킵니다. 특히 대용량 RasterLite 데이터셋의 경우 상당한 성능 향상을 보입니다. 이 명령어를 실행하면 시간이 꽤 걸릴 수도 있다는 사실을 기억하십시오.

예시
--------

-  단일 래스터 테이블을 가지고 있는 RasterLite 데이터베이스에 접근하기:

   ::

      $ gdalinfo rasterlitedb.sqlite -noct

   산출물:

   ::

      Driver: Rasterlite/Rasterlite
      Files: rasterlitedb.sqlite
      Size is 7200, 7200
      Coordinate System is:
      GEOGCS["WGS 84",
          DATUM["WGS_1984",
              SPHEROID["WGS 84",6378137,298.257223563,
                  AUTHORITY["EPSG","7030"]],
              AUTHORITY["EPSG","6326"]],
          PRIMEM["Greenwich",0,
              AUTHORITY["EPSG","8901"]],
          UNIT["degree",0.01745329251994328,
              AUTHORITY["EPSG","9122"]],
          AUTHORITY["EPSG","4326"]]
      Origin = (-5.000000000000000,55.000000000000000)
      Pixel Size = (0.002083333333333,-0.002083333333333)
      Metadata:
        TILE_FORMAT=GIF
      Image Structure Metadata:
        INTERLEAVE=PIXEL
      Corner Coordinates:
      Upper Left  (  -5.0000000,  55.0000000) (  5d 0'0.00"W, 55d 0'0.00"N)
      Lower Left  (  -5.0000000,  40.0000000) (  5d 0'0.00"W, 40d 0'0.00"N)
      Upper Right (  10.0000000,  55.0000000) ( 10d 0'0.00"E, 55d 0'0.00"N)
      Lower Right (  10.0000000,  40.0000000) ( 10d 0'0.00"E, 40d 0'0.00"N)
      Center      (   2.5000000,  47.5000000) (  2d30'0.00"E, 47d30'0.00"N)
      Band 1 Block=480x480 Type=Byte, ColorInterp=Palette
        Color Table (RGB with 256 entries)

-  다중 래스터 테이블을 가지고 있는 RasterLite 데이터베이스에 접근하기:

   ::

      $ gdalinfo multirasterdb.sqlite

   산출물:

   ::

      Driver: Rasterlite/Rasterlite
      Files:
      Size is 512, 512
      Coordinate System is `'
      Subdatasets:
        SUBDATASET_1_NAME=RASTERLITE:multirasterdb.sqlite,table=raster1
        SUBDATASET_1_DESC=RASTERLITE:multirasterdb.sqlite,table=raster1
        SUBDATASET_2_NAME=RASTERLITE:multirasterdb.sqlite,table=raster2
        SUBDATASET_2_DESC=RASTERLITE:multirasterdb.sqlite,table=raster2
      Corner Coordinates:
      Upper Left  (    0.0,    0.0)
      Lower Left  (    0.0,  512.0)
      Upper Right (  512.0,    0.0)
      Lower Right (  512.0,  512.0)
      Center      (  256.0,  256.0)

-  다중 래스터 테이블을 가지고 있는 데이터베이스 안에 있는 래스터 테이블 하나에 접근하기:

   ::

      $ gdalinfo RASTERLITE:multirasterdb.sqlite,table=raster1

-  JPEG 타일로 인코딩된 데이터로 새 RasterLite 데이터베이스를 생성하기:

   ::

      $ gdal_translate -of Rasterlite source.tif RASTERLITE:my_db.sqlite,table=source -co DRIVER=JPEG

-  내부 오버뷰 생성하기:

   ::

      $ gdaladdo RASTERLITE:my_db.sqlite,table=source 2 4 8 16

-  내부 오버뷰 제거하기:

   ::

      $ gdaladdo -clean RASTERLITE:my_db.sqlite,table=source

-  외부 오버뷰를 .ovr 파일로 생성하기:

   ::

      $ gdaladdo -ro RASTERLITE:my_db.sqlite,table=source 2 4 8 16

-  내부 오버뷰를 옵션을 사용해서 생성하기(GDAL 1.10 이상 버전):

   ::

      $ gdaladdo RASTERLITE:my_db.sqlite,table=source 2 4 8 16 --config RASTERLITE_OVR_OPTIONS DRIVER=GTiff,COMPRESS=JPEG,PHOTOMETRIC=YCbCr


참고
--------

-  `Spatialite 및 Rasterlite 홈페이지 <https://www.gaia-gis.it/fossil/libspatialite/index>`_

-  `Rasterlite 지침서 <http://www.gaia-gis.it/gaia-sins/rasterlite-docs/rasterlite-man.pdf>`_

-  `Rasterlite 입문서 <http://www.gaia-gis.it/gaia-sins/rasterlite-docs/rasterlite-how-to.pdf>`_

-  `샘플 데이터베이스 <http://www.gaia-gis.it/spatialite-2.3.1/resources.html>`_

-  :ref:`OGR SQLite <vector.sqlite>` 드라이버

