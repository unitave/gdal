.. _raster.georaster:

================================================================================
오라클 공간 지오래스터
================================================================================

.. shortname:: GeoRaster

.. build_dependencies:: 오라클 클라이언트 라이브러리들

이 드라이버는 (10g버전 이상의) 오라클 공간 지오래스터(Oracle Spatial GeoRaster) 포맷 래스터 데이터 읽기 및 쓰기를 지원합니다. GDAL 플러그인으로 오라클 공간 지오래스터 드라이버를 빌드할 수 있는 옵션이 있지만, 오라클 클라이언트 라이브러리가 반드시 필요합니다.

지오래스터를 열 때, 지오래스터의 이름을 다음 양식으로 지정해야 합니다:

::

    georaster:<user>{,/}<pwd>{,@}[db],[schema.][table],[column],[where]
    georaster:<user>{,/}<pwd>{,@}[db],<rdt>,<rid>

이때:

- user   = 오라클 서버 로그인을 위한 사용자 이름
- pwd    = 사용자 비밀번호
- db     = 오라클 서버 식별 정보(데이터베이스 이름)
- schema = 스키마 이름
- table  = 지오래스터 테이블 이름 (지오래스터 열을 담고 있는 테이블)
- column = MDSYS.SDO_GEORASTER 데이터 유형의 열 이름
- where  = 하나 이상의 지오래스터(들)를 식별하기 위한 단순 WHERE 구문
- rdt    = 래스터 데이터 테이블 이름
- rid    = 지오래스터 1개의 숫자형 식별 정보

예시:

::

    geor:scott,tiger,demodb,table,column,id=1
    geor:scott,tiger,demodb,table,column,"id = 1"
    "georaster:scott/tiger@demodb,table,column,gain>10"
    "georaster:scott/tiger@demodb,table,column,city='Brasilia'"
    georaster:scott,tiger,,rdt_10$,10
    geor:scott/tiger,,rdt_10$,10

주의: 필드값을 둘러싸는 공백과 쉼표를 사용해야 합니다.

주의: 마지막 두 예시처럼, 데이터베이스 이름 항목을 비워둘 수 있으며 (",,") 이 경우 TNSNAME을 사용할 것입니다.

주의: 쿼리 결과 하나 이상의 지오래스터를 반환하는 경우 GDAL 메타데이터의 하위 데이터셋 목록으로 취급할 것입니다. (아래 내용 참조)

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

지오래스터 데이터베이스 탐색
------------------------------------

몇몇 기본 정보를 지정해주면, 지오래스터 드라이버가 서버에 저장된 기존 래스터들을 목록화할 수 있습니다:

    다음 사용자 이름과 데이터베이스에 속해 있는 서버의 모든 지오래스터 테이블을 목록화하려면:
    
        ::
        
            % gdalinfo georaster:scott/tiger@db1

    다음 테이블에 존재하는 모든 지오래스터 유형 열을 목록화하려면:

        ::
        
            % gdalinfo georaster:scott/tiger@db1,table_name

    다음 명령어는 다음 테이블에 저장된 모든 지오래스터 객체를 목록화할 것입니다:

        ::
        
            % gdalinfo georaster:scott/tiger@db1,table_name,georaster_column

    다음 명령어는 다음 테이블에 존재하는 모든 지오래스터를 WHERE 구문에 따라 목록화할 것입니다:

        ::
        
            % gdalinfo
            georaster:scott/tiger@db1,table_name,georaster_column,city='Brasilia'

이 쿼리들의 결과가 다음 예시와 같은 GDAL 메타데이터 하위 데이터셋으로 반환된다는 사실을 기억하십시오:

    ::
    
        % gdalinfo georaster:scott/tiger
        Driver: GeoRaster/Oracle Spatial GeoRaster
        Subdatasets:
        SUBDATASET_1_NAME=georaster:scott,tiger,,LANDSAT
        SUBDATASET_1_DESC=Table:LANDSAT
        SUBDATASET_2_NAME=georaster:scott,tiger,,GDAL_IMPORT
        SUBDATASET_2_DESC=Table:GDAL_IMPORT

생성 옵션
----------------

-  **BLOCKXSIZE**: 래스터 블록의 픽셀 열 개수
-  **BLOCKYSIZE**: 래스터 블록의 픽셀 행 개수
-  **BLOCKBSIZE**: 래스터 블록의 밴드 개수
-  **BLOCKING**: 블록화(blocking)를 사용하지 않거나(NO) 또는 자동 블록화 크기를 요청합니다(OPTIMUM).
-  **SRID**: 지오래스터에 특정 EPSG 투영법/좌표계 식별 정보를 할당합니다.
-  **INTERLEAVE**: 밴드 교차삽입(interleaving) 모드입니다. 밴드 순차, 라인 교차삽입, 픽셀 교차삽입에 대해 각각 BAND, LINE, PIXEL로 (또는 BSQ, BIL, BIP로) 설정할 수 있습니다. GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 가지고 있는 다중 밴드 소스 데이터셋으로부터 복사해올 때 INTERLEAVE 생성 옵션이 지정돼 있지 않은 경우, COMPRESS 생성 옵션이 지정돼 있지 않은 한 소스 데이터셋의 INTERLEAVE를 자동적으로 연산에 넣을 것입니다.
-  **DESCRIPTION**: 새로 생성된 테이블을 SQL 문법으로 간단하게 서술합니다. 테이블이 이미 존재한다면, 이 생성 옵션을 다음처럼 무시할 것입니다:

::

    % gdal_translate -of georaster landsat_823.tif
    geor:scott/tiger@orcl,landsat,raster \\
      -co DESCRIPTION="(ID NUMBER, NAME VARCHAR2(40), RASTER
    MDSYS.SDO_GEORASTER)" \\
      -co INSERT="VALUES (1,'Scene 823',SDO_GEOR.INIT())"

-  **INSERT**: 테이블에 새 행을 삽입할 때 어떤 값을 채울 것인지 드라이버에게 알려주기 위한, 예를 들면 다음과 같은 단순 SQL INSERT/VALUE 구문입니다:

::

    % gdal_translate -of georaster landsat_825.tif
    geor:scott/tiger@orcl,landsat,raster \\
      -co INSERT="(ID, RASTER) VALUES (2,SDO_GEOR.INIT())"

-  **COMPRESS**: 압축 옵션으로, JPEG-F, JP2-F, DEFLATE 또는 NONE으로 설정할 수 있습니다. JPEG-F 옵션은 손실 압축으로, 원본 픽셀값이 변경된다는 의미입니다. JP2_QUALITY를 100으로 설정하는 경우 JP2-F 옵션이 비손실 압축이 됩니다.
-  **GENPYRAMID**: 데이터베이스에 지오래스터 객체를 불러온 후 피라미드를 생성합니다. 이 파라미터의 내용은 NN(최근접 이웃), BILINEAR, BIQUADRATIC, CUBIC, AVERAGE4 또는 AVERAGE16 가운데 하나인 리샘플링 메소드여야만 합니다. GENPYRLEVELS 옵션을 설정하지 않는 경우, PL/SQL 함수 sdo_geor.generatePyramid가 생성할 수준의 개수를 계산할 것입니다.
-  **GENPYRLEVELS**: 생성할 피라미드 수준의 개수를 정의합니다. GENPYRAMID 옵션을 설정하지 않는 경우, NN(최근접 이웃) 리샘플링 메소드를 적용할 것입니다.
-  **QUALITY**: 0에서 100 범위의 JPEG 압축 품질 옵션입니다. 기본값은 75입니다.
-  **JP2_QUALITY=float_value,float_value,...** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. 0에서 100 사이의 백분율입니다. 50으로 설정하면 비압축 데이터 대비 용량이 절반으로 줄어들고, 33으로 설정하면 1/3으로... 기본값은 25입니다. (다만 데이터셋이 색상표를 가진 단일 밴드로 이루어진 경우에는 기본 품질이 100입니다.)
-  **JP2_REVERSIBLE=YES/NO** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. YES로 설정하면 5x3 정수 전용 가역(可逆) 필터를 사용하고, NO로 설정하면 비가역 DWT 9-7 필터를 사용합니다. 기본값은 NO입니다. (다만 데이터셋이 색상표를 가진 단일 밴드로 이루어진 경우에는 가역 필터를 사용합니다.)

-  **JP2_RESOLUTIONS=int_value** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. 해상도 수준의 개수입니다. 타일이 128x128 크기 미만인 가장 작은 오버뷰를 기본값으로 선택합니다.
-  **JP2_BLOCKXSIZE=int_value** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. 타일 너비입니다. 기본값은 1024입니다.
-  **JP2_BLOCKYSIZE=int_value** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. 타일 높이입니다. 기본값은 1024입니다.
-  **JP2_PROGRESSION=LRCP/RLCP/RPCL/PCRL/CPRL** COMPRESS 옵션을 JP2-F로 설정한 경우에만 사용할 수 있습니다. 수열(progression) 순서입니다. 기본값은 LRCP입니다.
-  **NBITS**: 하위 바이트 데이터 유형으로, 1, 2 또는 4 가운데 하나로 설정할 수 있습니다.
-  **SPATIALEXTENT**: 공간 범위를 생성합니다. 이 옵션의 기본값은 TRUE로, 강제로 공간 범위를 NULL로 유지하려면 이 옵션만 지정해주면 된다는 의미입니다. EXTENTSRID를 설정하지 않은 경우, 공간 범위 도형을 지오래스터 객체와 동일한 SRID로 생성할 것입니다.
-  **EXTENTSRID**: 공간 범위 도형에 사용할 SRID 코드입니다. 테이블/열이 이미 공간 색인을 가지고 있다면, 이 옵션의 값을 다른 기존 지오래스터 객체의 공간 범위에 쓰인 것과 동일한 SRID로 설정해야 합니다. 해당 SRID 상에서 공간 색인을 빌드했기 때문입니다.
-  **OBJECTTABLE**: 래스터 데이터 테이블을 SDO_RASTER 객체로 생성하려면 TRUE로 설정하십시오. 그렇지 않다면, 기본값은 FALSE이며 래스터 데이터 테이블을 정규 관계형 테이블로 생성할 것입니다. 오라클 11 이전 버전까지는 적용되지 않습니다.

지오래스터 가져오기
-------------------

래스터를 지오래스터 객체 안으로 가져오는 과정에서, 드라이버에게 생성할 테이블과 새로 생성될 행에 추가할 값들에 대해 알려주는 SQL INSERT/VALUE 구문은 물론 단순 SQL 테이블 정의를 지정할 수 있습니다. 다음이 그 예시입니다:

::

    % gdal_translate -of georaster
    Newpor.tif georaster:scott/tiger,,landsat,scene \\
      -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE
    MDSYS.SDO_GEORASTER)" \\
      -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())" \\
      -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" -co "BLOCKBSIZE=3" \\
      -co "INTERLEAVE=PIXEL" -co "COMPRESS=JPEG-F"

DESCRIPTION 생성 옵션에 반드시 테이블 이름(landsat)을 지정해야 한다는 사실을 기억하십시오. 그리고 열 이름(scene)도 설명과 일치해야 합니다:

::

    % gdal_translate -of georaster
    landsat_1.tif georaster:scott/tiger,,landsat,scene \\
      -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE
    MDSYS.SDO_GEORASTER)" \\
      -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())"

"landsat" 테이블이 존재하는 경우, "DESCRIPTION" 옵션을 무시합니다. 이 드라이버는 gdal_translate를 한번 실행할 때마다 지오래스터 열 하나만 업데이트할 수 있습니다. 오라클이 SDO_GEORASTER 객체 초기화 도중 래스터 데이터 테이블과 래스터 ID를 위한 기본 이름과 값을 생성하지만, 사용자도 직접 이름과 값을 지정할 수 있습니다.

::

    % gdal_translate -of georaster
    landsat_1.tif georaster:scott/tiger,,landsat,scene \\
      -co "INSERT=VALUES(10,'Main building', SDO_GEOR.INIT('RDT', 10))"

래스터 저장 위치에 대한 정보를 지정하지 않는 경우, 이 드라이버는 RASTER라는 지오래스터 열 하나만 가지고 있는 GDAL_IMPORT라는 기본 테이블을 (이미 존재하지 않는 경우) 생성하고, GDAL_RDT라는 테이블을 래스터 데이터 테이블(RDT)로서 생성할 것입니다. 래스터 ID(RID)는 서버가 자동으로 지정할 것입니다:

::

    % gdal_translate -of georaster input.tif "geor:scott/tiger@dbdemo"

지오래스터 내보내기
-------------------

WHERE 구문 또는 RDT와 RID 쌍을 사용하면 지오래스터를 식별할 수 있습니다:

::

    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54
    output.tif
    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,st_rdt_1,130
    output.tif

교차 스키마 접근
-------------------

사용자가 지오래스터 테이블 및 지오래스터 데이터 테이블에 대한 완전한 접근 권한을 가지고 있는 한, 다음과 같이 교차 접근할 수 있습니다:

::

    % sqlplus scott/tiger
    SQL> grant select,insert,update,delete on gdal_import to spock;
    SQL> grant select,insert,update,delete on gdal_rdt to spock;

다음과 같이 스키마 이름을 지정해주면 또다른 사용자/스키마로부터 GeoRaster를 추출하고 불러오기 위해 접근할 수 있습니다:

탐색:

::

    % gdalinfo geor:spock/lion@orcl,scott.
    %gdalinfo
    geor:spock/lion@orcl,scott.gdal_import,raster,"t.raster.rasterid > 100"

::
    %gdalinfo
    geor:spock/lion@orcl,scott.gdal_import,raster,t.raster.rasterid=101

추출하기:

::

    % gdal_translate geor:spock/lion@orcl,scott.gdal_import,raster,t.raster.rasterid=101out.tif
    % gdal_translate geor:spock/lion@orcl,gdal_rdt,101 out.tif

주의: 사용자가 두 테이블에 대한 완전한 접근 권한을 가지고 있는 한, RDT/RID로 접근하는 앞의 예시에서는 스키마 이름이 필요하지 않습니다.

불러오기:

::

    % gdal_translate -of georaster input.tifgeor:spock/lion@orcl,scott.
    % gdal_translate -of georaster input.tif
    geor:spock/lion@orcl,scott.cities,image \\
      -co INSERT="(1,'Rio de Janeiro',sdo_geor.init('cities_rdt'))"

지오래스터의 일반적인 사용
------------------------

모든 GDAL 명령줄 도구에서 지오래스터를 사용할 수 있는 모든 옵션과 함께 사용할 수 있습니다. 다음과 같이 이미지 하위 집합을 추출하거나 재투영할 수도 있습니다:

::

    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54
    output.tif \\
      -srcwin 0 0 800 600
    % gdalwarp -of png geor:scott/tiger@dbdemo,st_rdt_1,130 output.png -t_srs EPSG:9000913

동일한 작업에서 서로 다른 지오래스터 2개를 입력물 및 출력물로 사용할 수 있습니다:

::

    % gdal_translate -of georaster
    geor:scott/tiger@dbdemo,landsat,scene,id=54
    geor:scott/tiger@proj1,projview,image -co INSERT="VALUES(102, SDO_GEOR.INIT())"

GDAL을 이용하는 응용 프로그램은 이론적으로 다른 모든 포맷과 마찬가지로 지오래스터를 읽고 쓸 수 있지만, 대부분의 경우 파일 시스템 상에 있는 파일에 우선 접근하려는 경향이 있습니다. 이때 한 가지 대안은 지오래스터 설명을 표현하는 VRT를 다음과 같이 생성하는 것입니다:

::
    % gdal_translate -of VRT geor:scott/tiger@dbdemo,landsat,scene,id=54
    view_54.vrt
    % openenv view_54.vrt
