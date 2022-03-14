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
  - where  = 하나 이상의 지오래스터(들)를 식별하기 위한 단순 WHERE 문
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

    다음 명령어는 다음 테이블에 존재하는 모든 지오래스터를 WHERE 문에 따라 목록화할 것입니다:

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

-  **BLOCKXSIZE**: The number of pixel columns on raster block.
-  **BLOCKYSIZE**: The number of pixel rows on raster block.
-  **BLOCKBSIZE**: The number of bands on raster block.
-  **BLOCKING**: Decline the use of blocking (NO) or request an
   automatic blocking size (OPTIMUM).
-  SRID: Assign a specific EPSG projection/reference system
   identification to the GeoRaster.
-  **INTERLEAVE**: Band interleaving mode, BAND, LINE, PIXEL (or BSQ,
   BIL, BIP) for band sequential, Line or Pixel interleaving.
   Starting with GDAL 3.5, when copying from a source dataset with multiple bands
   which advertises a INTERLEAVE metadata item, if the INTERLEAVE creation option
   is not specified, the source dataset INTERLEAVE will be automatically taken
   into account, unless the COMPRESS creation option is specified.
-  **DESCRIPTION**: A simple description of a newly created table in SQL
   syntax. If the table already exist, this create option will be
   ignored, e.g.:

% gdal_translate -of georaster landsat_823.tif
geor:scott/tiger@orcl,landsat,raster \\
  -co DESCRIPTION="(ID NUMBER, NAME VARCHAR2(40), RASTER
MDSYS.SDO_GEORASTER)" \\
  -co INSERT="VALUES (1,'Scene 823',SDO_GEOR.INIT())"

-  **INSERT**: A simple SQL insert/values clause to inform the driver
   what values to fill up when inserting a new row on the table, e.g.:

| % gdal_translate -of georaster landsat_825.tif
  geor:scott/tiger@orcl,landsat,raster \\
    -co INSERT="(ID, RASTER) VALUES (2,SDO_GEOR.INIT())"

-  **COMPRESS**: Compression options, JPEG-F, JP2-F, DEFLATE or NONE.
   The JPEG-F options is lossy, meaning that the original pixel values
   are changed. The JP2-F compression is lossless if JP2_QUALITY=100.
-  **GENPYRAMID**: Generate pyramid after a GeoRaster object have been
   loaded to the database. The content of that parameter must be the
   resampling method of choice NN (nearest neighbor) , BILINEAR,
   BIQUADRATIC, CUBIC, AVERAGE4 or AVERAGE16. If GENPYRLEVELS is not
   informed the PL/SQL function sdo_geor.generatePyramid will calculate
   the number of levels to generate.
-  **GENPYRLEVELS**: Define the number of pyramid levels to be
   generated. If GENPYRAMID is not informed the resample method NN
   (nearest neighbor) will apply.
-  **QUALITY**: Quality compression option for JPEG ranging from 0 to
   100. The default is 75.
-  **JP2_QUALITY=float_value,float_value,...** Only if COMPRESS=JP2-f :
   Percentage between 0 and 100. A value of 50 means the file will be
   half-size in comparison to uncompressed data, 33 means 1/3, etc..
   Defaults to 25 (unless the dataset is made of a single band with
   color table, in which case the default quality is 100).

-  **JP2_REVERSIBLE=YES/NO** Only if COMPRESS=JP2-f : YES means use of
   reversible 5x3 integer-only filter, NO use of the irreversible DWT
   9-7. Defaults to NO (unless the dataset is made of a single band with
   color table, in which case reversible filter is used).

-  **JP2_RESOLUTIONS=int_value** Only if COMPRESS=JP2-f : Number of
   resolution levels. Default value is selected such the smallest
   overview of a tile is no bigger than 128x128.

-  **JP2_BLOCKXSIZE=int_value** Only if COMPRESS=JP2-f : Tile width.
   Defaults to 1024.

-  **JP2_BLOCKYSIZE=int_value** Only if COMPRESS=JP2-f : Tile height.
   Defaults to 1024.

-  **JP2_PROGRESSION=LRCP/RLCP/RPCL/PCRL/CPRL** Only if COMPRESS=JP2-f :
   Progession order. Defaults to LRCP.

-  **NBITS**: Sub byte data type, options: 1, 2 or 4.
-  **SPATIALEXTENT**: Generate Spatial Extents. The default for that
   options is TRUE, that means that this option only need to be informed
   to force the Spatial Extent to remain as NULL. If EXTENTSRID is not
   informed the Spatial Extent geometry will be generated with the same
   SRID as the GeoRaster object.
-  **EXTENTSRID**: SRID code to be used on the Spatial Extent geometry.
   If the table/column has already a spatial index, the value informed
   should be the same as the SRID on the Spatial Extents of the other
   existing GeoRaster objects, on which the spatial index is built.
-  **OBJECTTABLE**: To create RDT as SDO_RASTER object inform TRUE
   otherwise, the default is FALSE and the RDT will be created as
   regular relational tables. That does not apply for Oracle version
   older than 11.

Importing GeoRaster
-------------------

During the process of importing raster into a GeoRaster object it is
possible to give the driver a simple SQL table definition and also a SQL
insert/values clause to inform the driver about the table to be created
and the values to be added to the newly created row. The following
example does that:

| % gdal_translate -of georaster
  Newpor.tif georaster:scott/tiger,,landsat,scene \\
|   -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE
  MDSYS.SDO_GEORASTER)" \\
|   -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())" \\
|   -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" -co "BLOCKBSIZE=3" \\
|   -co "INTERLEAVE=PIXEL" -co "COMPRESS=JPEG-F"

Note that the create option DESCRIPTION requires to inform table name
(in bold). And column name (underlined) should match the description:

| % gdal_translate -of georaster
  landsat_1.tif georaster:scott/tiger,,landsat,scene \\
|   -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE
  MDSYS.SDO_GEORASTER)" \\
|   -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())"

If the table "landsat" exist, the option "DESCRIPTION" is ignored. The
driver can only update one GeoRaster column per run of
gdal_translate. Oracle create default names and values for RDT and RID
during the initialization of the SDO_GEORASTER object but user are also
able to specify a name and value of their choice.

| % gdal_translate -of georaster
  landsat_1.tif georaster:scott/tiger,,landsat,scene \\
|   -co "INSERT=VALUES(10,'Main building', SDO_GEOR.INIT('RDT', 10))"

If no information is given about where to store the raster the driver
will create (if doesn't exist already) a default table named GDAL_IMPORT
with just one GeoRaster column named RASTER and a table GDAL_RDT as the
RDT, the RID will be given automatically by the server, example:

| % gdal_translate -of georaster input.tif “geor:scott/tiger@dbdemo”

Exporting GeoRaster
-------------------

| A GeoRaster can be identified by a Where clause or by a pair of RDT &
  RID:
| % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54
  output.tif
  % gdal_translate -of gtiff geor:scott/tiger@dbdemo,st_rdt_1,130
  output.tif

Cross schema access
-------------------

| As long as the user was granted full access the GeoRaster table and
  the Raster Data Table, e.g.:
| % sqlplus scott/tiger
  SQL> grant select,insert,update,delete on gdal_import to spock;
  SQL> grant select,insert,update,delete on gdal_rdt to spock;
| It is possible to an user access to extract and load GeoRaster from
  another user/schema by informing the schema name as showed here:
| Browsing:
| % gdalinfo geor:spock/lion@orcl,scott.
  %gdalinfo
  geor:spock/lion@orcl,scott.gdal_import,raster,"t.raster.rasterid >
  100"
| %gdalinfo
  geor:spock/lion@orcl,scott.gdal_import,raster,t.raster.rasterid=101
  Extracting:
| %
  gdal_translate geor:spock/lion@orcl,scott.gdal_import,raster,t.raster.rasterid=101out.tif
  % gdal_translate geor:spock/lion@orcl,gdal_rdt,101 out.tif
  Note: On the above example that accessing by RDT/RID doesn't need
  schame name as long as the users is granted full access to both
  tables.
| Loading:
| % gdal_translate -of georaster input.tifgeor:spock/lion@orcl,scott.
  % gdal_translate -of georaster input.tif
  geor:spock/lion@orcl,scott.cities,image \\
    -co INSERT="(1,'Rio de Janeiro',sdo_geor.init('cities_rdt'))"

General use of GeoRaster
------------------------

| GeoRaster can be used in any GDAL command line tool with all the
  available options. Like a image subset extraction or re-project:
| % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54
  output.tif \\
    -srcwin 0 0 800 600
  % gdalwarp -of png geor:scott/tiger@dbdemo,st_rdt_1,130 output.png
  -t_srs EPSG:9000913
  Two different GeoRaster can be used as input and output on the same
  operation:
| % gdal_translate -of georaster
  geor:scott/tiger@dbdemo,landsat,scene,id=54
  geor:scott/tiger@proj1,projview,image -co INSERT="VALUES
  (102, SDO_GEOR.INIT())"
  Applications that use GDAL can theoretically read and write from
  GeoRaster just like any other format but most of then are more
  inclined to try to access files on the file system so one alternative
  is to create VRT to represent the GeoRaster description, e.g.:
| % gdal_translate -of VRT geor:scott/tiger@dbdemo,landsat,scene,id=54
  view_54.vrt
  % openenv view_54.vrt
