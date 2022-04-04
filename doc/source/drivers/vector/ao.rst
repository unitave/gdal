.. _vector.ao:

================================================================================
ESRI ArcObjects
================================================================================

.. shortname:: AO

.. build_dependencies:: ESRI ArcObjects

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_AO

개요
--------

OGR ArcObjects 드라이버는 ArcObjects 기반 데이터소스에 읽기 전용 접근을 지원합니다. 이 드라이버가 ESRI SDK를 이용하기 때문에, 이 드라이버를 실행하려면 ESRI 사용 허가가 필수입니다. 그래도 이 드라이버가 ESRI의 추상 개념(abstraction)을 완전히 알고 있다는 뜻이기도 합니다. 이런 추상 개념들 가운데:

* GeoDatabases:

    * 개인 GeoDatabase (.mdb)
    * 파일 GeoDatabase (.gdb)
    * 기업 GeoDatabase (.sde)

* ESRI Shapefiles

(필요가 없었기 때문에) 아직 다음과 같은 기능까지 확장되지는 않았지만, 다음과 같은 GeoDatabase 추상 개념을 지원할 가능성도 있습니다.:

* 주석(annotation) 및 차원 객체(dimension feature) 클래스
* 관계성(relationship) 클래스
* 네트워크 (GN 및 ND)
* 위상(topology)
* 지형(terrain)
* 표현(representation)
* 파셀 패브릭(parcel fabric)

이 추상 개념들을 시도해본다면 작동할 수도 있습니다. 그러나 테스트되지는 않았습니다. 오픈 FileGeoDatabase API가 이런 추상 개념들을 지원하지 못 한다는 사실을 기억하십시오.

요구 사항
------------

* ArcView 사용 허가 또는 ArcEngine 사용 허가 (또는 더 상위의 사용 허가) -- 실행하기 위해 필수입니다.

* ESRI 라이브러리가 설치되어 있어야 합니다. 사용자가 ArcEngine 또는 ArcGIS 데스크탑/서버를 설치하는 경우 -- 일반적으로 컴파일 작업에 ESRI 라이브러리가 필요합니다. 이 코드도 ArcEngine \*nix SDK를 이용해서 컴파일해야 하지만, 작성자가 이를 구할 수 없어서 실제로 시도해보지는 못 했다는 사실을 기억하십시오.

사용례
-----

데이터소스에 접두어 "AO:"를 붙이십시오.

FileGDB로부터 읽어와서 PostGIS로 불러오십시오:

.. code-block::

    ogr2ogr -overwrite -skipfailures -f "PostgreSQL" PG:"host=myhost user=myuser dbname=mydb password=mypass" AO:"C:\somefolder\BigFileGDB.gdb" "MyFeatureClass"

개인 GeoDatabase의 상세 정보를 가져오십시오:

.. code-block::

    ogrinfo -al AO:"C:\somefolder\PersonalGDB.mdb"

기업 GeoDatabase의 상세 정보를 가져오십시오(.sde 파일이 연결할 대상 GeoDatabase의 버전을 담고 있습니다):

.. code-block::

    ogrinfo -al AO:"C:\somefolder\MySDEConnection.sde"

빌드 메모
--------------

`플러그인 용 GDAL 윈도우 빌드 작업 예시 <http://trac.osgeo.org/gdal/wiki/BuildingOnWindows>`_ 를 읽어보십시오. ArcObjects 용 :file:`nmake.opt` 파일에 비슷한 단락이 있을 것입니다. 준비가 되었다면 :file:`$gdal_source_root/ogr/ogrsf_frmts/arcobjects*` 폴더로 가서 다음 명령어를 실행하십시오:

.. code-block::

    nmake /f makefile.vc plugin
    nmake /f makefile.vc plugin-install

알려진 문제점
------------

날짜 및 블랍(blob) 필드가 아직 구현되지 않았습니다. 아마도 코드 몇 줄이면 구현할 수 있겠지만, 작성자가 그렇게 할 시간(또는 필요)이 없었습니다.
