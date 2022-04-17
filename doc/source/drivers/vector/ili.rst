.. _vector.ili:

"INTERLIS 1" 및 "INTERLIS 2" 드라이버
=====================================

.. shortname:: INTERLIS 1

.. shortname:: INTERLIS 2

.. build_dependencies:: Xerces

OGR는 INTERLIS 포맷의 읽기 및 쓰기를 지원합니다.
`INTERLIS <http://www.interlis.ch/>`_ 는 특히 지리 데이터를 모델링하고 현재 그리고 미래의 GIS로 통합하기 위한 요구 사항들을 달성하기 위해 구성된 표준입니다. 통일된, 문서화된 지리 데이터 사용 및 유연한 정보 교환 가능성은 다음과 같은 장점을 선보일 수도 있습니다:

-  표준화된 문서화
-  호환되는 데이터 교환
-  예를 들어 서로 다른 데이터 소유자들로부터 나온 지리 데이터의 포괄적 집적화(comprehensive integration)
-  품질 보증
-  장기(long term) 데이터 저장소
-  계약으로 보장된 보안 및 소프트웨어의 가용성

OGR는 다음과 같이 제한적으로 (GDAL 2.2버전에서) INTERLIS 1 및 (GDAL 2.3버전에서) INTERLIS 2를 지원합니다:

-  Interlis 1의 면(area) 폴리곤에 있는 곡선을 라인 선분으로 변환합니다.
-  Interlis 1의 숫자가 아닌 IDENT 필드를 가진 Surface 도형을 속성 레이어에 포함시키지 않습니다.
-  내장 INTERLIS 2 구조와 라인 속성을 지원하지 않습니다.
-  증분 전송(incremental transfer)을 지원하지 않습니다.
-  전송ID(Transfer ID; TID)를 객체ID(Feature ID; FID)로 사용합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

모델 지원
-------------

INTERLIS 1(.itf) 및 INTERLIS 2(.xtf)에서 데이터를 서로 다른 포맷을 가진 전송 파일에 읽고 씁니다. "a_filename.xtf,models.imd"를 연결 문자열로 사용해서 모델을 IlisMeta 포맷으로 전송합니다.

IlisMeta 파일은 ili2c 컴파일러로 생성할 수 있습니다. 다음은 명령줄 예시입니다:

::

   java -jar ili2c.jar --ilidirs '%ILI_DIR;http://models.interlis.ch/;%JAR_DIR' -oIMD --out models.imd model1.ili [model2.ili ...]

다음은 :ref:`ogr2ogr` 유틸리티를 이용해서 변환할 수 있는 몇몇 예시입니다.

-  Interlis 1 -> shapefile:

   ::

      ogr2ogr -f "ESRI Shapefile" shpdir ili-bsp.itf,Beispiel.imd

-  Interlis 2 -> shapefile:

   ::

      ogr2ogr -f "ESRI Shapefile" shpdir RoadsExdm2ien.xml,RoadsExdm2ien.imd

   또는 모델이 없는 경우:

   ::

      ogr2ogr -f "ESRI Shapefile" shpdir RoadsExdm2ien.xml

   다음은 곡선 및 다중 도형의 예시입니다:

   ::

      ogr2ogr --config OGR_STROKE_CURVE TRUE -SQL 'SELECT Rechtsstatus,publiziertAb,MetadatenGeobasisdaten,Eigentumsbeschraenkung,ZustaendigeStelle,Flaeche FROM "OeREBKRM09trsfr.Transferstruktur.Geometrie"' shpdir ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,OeREBKRM09vs.imd OeREBKRM09trsfr.Transferstruktur.Geometrie

-  shapefile -> Interlis 2:

   ::

      ogr2ogr -f "Interlis 2" LandCover.xml,RoadsExdm2ien.imd RoadsExdm2ben.Roads.LandCover.shp

-  Interlis 1 파일 여러 개를 PostGIS로 가져오기:

   ::

      ogr2ogr -f PostgreSQL PG:dbname=warmerda av_fixpunkte_ohne_LFPNachfuehrung.itf,av.imd -lco OVERWRITE=yes
      ogr2ogr -f PostgreSQL PG:dbname=warmerda av_fixpunkte_mit_LFPNachfuehrung.itf,av.imd -append

원호 보간
~~~~~~~~~~~~~~~~~

:decl_configoption:`OGR_STROKE_CURVE` 환경설정 옵션을 TRUE로 설정하면 INTERLIS 원호(arc) 도형을 라인 선분으로 강제 변환할 수 있습니다.
원호를 가장 근사치의 라인스트링으로 변환하는 작업은 원호를 한계 각도를 넘지 않는 하위 원호들로 분할해서 이루어집니다. :decl_configoption:`OGR_ARC_STEPSIZE` 환경설정 옵션으로 한계 각도를 설정합니다. 이 옵션의 기본값은 1도이지만, :decl_configoption:`OGR_ARC_STEPSIZE` 환경설정 옵션을 다른 값으로 설정해서 대체할 수도 있습니다.

기타 메모
-----------

-  `ogrtools <https://github.com/sourcepole/ogrtools>`_ 라이브러리는 OGR Interlis 드라이버 용 확장 사양을 포함합니다.

-  `스위스 연방 행정부 <http://www.kogis.ch/>`_, `졸로투른(Solothurn) 주 <http://www.sogis.ch/>`_ 그리고 `투르가우(Thurgau) 주 <http://www.geoinformation.tg.ch/>`_ 가 OGR INTERLIS 드라이버의 개발을 지원했습니다.

