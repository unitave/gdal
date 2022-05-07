.. _wktproblems:

================================================================================
OGC WKT 좌표계 문제점
================================================================================

이 문서에서는 오픈GIS WKT(Well Known Text) 좌표계 설명을 사용하려 시도하는 과정에서 발생하는 문제점들을 논의하려 합니다. 원본 `"단순 피처" 사양 (예: SF-SQL 99-049) <http://portal.opengeospatial.org/files/?artifact_id=829>`_ 과 WKT 확장 형식을 정의하는 신규 `좌표 변환 서비스 (CT) 사양 (01-009) <http://portal.opengeospatial.org/files/?artifact_id=999>`_ 사이의 다양한 제품 구현 및 문제점을 논의합니다.

WKT 구현
--------

문서 작성 당시 다음 소프트웨어 패키지들이 내부적으로 또는 좌표계 설명 교환을 위해 어떤 WKT 형식을 사용한다고 알려져 있습니다:

-  오라클 Spatial (MDSYS.WKT에서 내부적으로 WKT 사용, 느슨하게 SFSQL 기반)

-  ESRI:
   Arc8 시스템의 투영 엔진이 단순 피처와 대충 호환되는 투영법 설명을 사용합니다. ESRI가 단순 피처 사양을 위한 WKT 정의를 제공하는 것으로 알려져 있습니다.

-  Cadcorp:
   CT 1.0 스타일 WKT를 읽고 쓸 수 있습니다. Cadcorp가 CT 사양을 작성했습니다.

-  OGR/GDAL:
   자신의 내부 좌표계 설명 서식으로 WKT를 읽고 씁니다. 예전, 최신 형식들은 물론 ESRI 형식도 지원하려 시도합니다.

-  FME:
   OGR 상에 빌드된 WKT 읽기/쓰기 케이퍼빌리티를 포함합니다.

-  MapGuide:
   SDP 데이터 접근 API에서 WKT를 사용합니다. 단순 피처와 대충 호환됩니다.

-  PostGIS:
   'spatial_ref_sys' 테이블에 WKT를 유지하지만, 실제 사용을 위해 PROJ.4 서식으로 변환하는 것은 클라이언트의 몫입니다. 'spatial_ref_sys' 테이블은 OGR가 생성한 변환을 사용해서 채워지는 것으로 보입니다.

투영법 파라미터
---------------

다양한 사양들이 투영법 집합 및 관련 파라미터들을 목록화하고 있지 않습니다. 즉 서로 다른 제품들이 서로 다른 파라미터 이름을 (그리고 가끔 서로 다른 투영법 이름을) 사용하게 됩니다. 저자는 `GeoTIFF 투영법 목록 <https://web.archive.org/web/20130728081442/http://www.remotesensing.org/geotiff/proj_list/>`_ 레지스트리의 일환으로 서로 다른 투영법들에 대한 WKT 바인딩 목록을 유지/보수하려 시도했습니다. 이 목록의 투영법 및 파라미터 이름을 사용해주십시오. 이 목록은 가능한 경우 투영법과 GeoTIFF, EPSG 및 PROJ.4 공식 서술(formulation)도 연결시키려 시도합니다.

저자가 알고 있는, 제품이 이 목록을 따르지 않는 사례 하나는 ESRI의 람베르트 정각원추도법 정의입니다. EPSG에는 이 투영법의 1SP 및 2SP 형식이 존재합니다. ESRI는 이 둘을 병합하고, 그냥 유형에 따라 서로 다른 파라미터를 사용하도록 했습니다.

다른 문제점 하나는 CT 사양이 횡축 메르카토르 도법, 람베르트 정각원추도법 1SP 및 2SP 투영법에 대한 파라미터들을 명확하게 목록화하지 않는다는 점입니다. 하지만 CT 사양은 'standard_parallel1' 및 'standard_parallel2'를 람베르트 정각원추도법 2SP의 파라미터로 목록화하는데, 이것은 'standard_parallel_1' 및 'standard_parallel_2'의 기존 사용례와 충돌하고 또 동일한 CT 사양에 있는 예시와도 충돌합니다.
저자는 CT 사양의 10.x 단락에 있는 표에 오류가 있고 널리 쓰이는 형식이 정확하다는 입장입니다. CT 사양에 있는 표가 동일 사양에 있는 다른 예시들과 충돌한다는 사실을 기억하십시오.

세 번째 문제점은 알베르스 도법의 공식 서술입니다. 저자가 'longitude_of_center' 및 'latitude_of_center'를 사용하는 반면, ESRI는 'Central_meridian' 및 'latitude_of_origin'을 사용합니다.

ESRI:

::

   PROJECTION["Albers"],
   PARAMETER["False_Easting",1000000.0],
   PARAMETER["False_Northing",0.0],
   PARAMETER["Central_Meridian",-126.0],
   PARAMETER["Standard_Parallel_1",50.0],
   PARAMETER["Standard_Parallel_2",58.5],
   PARAMETER["Latitude_Of_Origin",45.0],

OGR:

::

   PROJECTION["Albers"],
   PARAMETER["standard_parallel_1",50],
   PARAMETER["standard_parallel_2",58.5],
   PARAMETER["longitude_of_center",-126],
   PARAMETER["latitude_of_center",45],
   PARAMETER["false_easting",1000000],
   PARAMETER["false_northing",0],

원점 이름
---------

단순 피처 스타일 WKT에서 원점을 식별할 수 있는 유일한 방법은 원점(datum)과 관련된 이름입니다. CT WKT에서는 원점도 WGS84와의 관계를 나타내는 TOWGS84 파라미터와 원점을 ESPG 또는 다른 기관 공간에 연결시키는 AUTHORITY 파라미터를 가질 수 있습니다. 하지만 단순 피처 WKT에서는 이름 자체만 키입니다.

규범에 따라 OGR 및 Cadcorp는 비슷한 이름을 생성하기 위해 특정한 방법으로 ESPG 데이터베이스로부터 원점 이름을 변환합니다. 알파벳 또는 숫자가 아닌 모든 문자를 언더바로 변환한 다음, 맨 앞/맨 뒤 그리고 반복되는 언더바를 제거하는 규칙입니다. 이렇게 하면 "Nouvelle_Triangulation_Francaise"처럼 양호한 원점 이름을 생성합니다.

하지만 다른 제품들은 다르게 변환합니다. ESRI는 비슷한 규범을 따르는 것으로 보이지만 모든 원점 이름 앞에 접두어 "D\_"를 붙이기 때문에 "D_WGS_1972" 같은 이름을 생성합니다. 또 이유는 명확하지 않지만 다른 차이점들도 많이 있습니다. 예를 들어 OGR 및 Cadcorp가 "Nouvelle_Triangulation_Francaise"라고 하는 이름을 ESRI는 "D_NTF"라고 합니다. 오라클은 정리하지 않은 원시(raw) 이름을 사용하는 것으로 보입니다. 즉 "Nouvelle_Triangulation_Francaise"에 대해 오라클은 "NTF (Paris meridian)"을 사용합니다.

즉 빠른 결론을 내리자면, 서로 다른 단순 피처 구현 사이에 원점을 인식하고 비교하는 것이 거의 불가능합니다. 다만 저자는 몇몇 특수 대소문자 변환을 통해 ESRI 원점 이름을 OGR/Cadcorp 규범을 따르도록 변환하는 데 성공하기도 했습니다.

파라미터 순서
-------------

단순 피처 사양 및 CT 사양에서 WKT 용 BNF(Backus–Naur Form) 문법이 대부분의 항목에 대해 특정 순서를 의미한다는 사실을 기억해두는 편이 좋습니다. 예를 들어 CT 사양에서 PROJCS 항목에 대한 BNF는 다음과 같습니다:

::

   <projected cs> =
     PROJCS["<name>", <geographic cs>, <projection>, {<parameter>,}* <linear unit> {,<twin axes>}{,<authority>}]

이 문법은 GEOGCS 뒤에 PROJECTION 키워드가 오고 그 뒤를 UNIT, AXIS 및 AUTHORITY 항목이 따른다는 사실을 명확하게 서술하고 있습니다. 이 순서를 무시하고 파라미터를 지정하는 것은 사양을 위반하는 것과 같습니다. 다른 한편으로, WKT 소비자는 순서에 유연하도록 권장받습니다.

PARAMETER 단위
--------------

PROJCS에 있는 선형 PARAMETER 값들은 해당 PROJCS 용 선형 단위를 사용해야만 합니다. 저자의 생각에는 가짜 편동 및 편북 유형 값들이 유일하게 선형 단위를 사용합니다. 따라서 피트 단위의 주(州) 평면 구역 같은 흔한 사례에서, 가짜 편동 및 편북도 피트 단위일 것입니다.

PROJCS에 있는 각도 PARAMETER 값들은 GEOGCS의 각도 단위를 사용해야만 합니다. GEOGCS가 그라디안 단위인 경우, 모든 투영 각도들도 반드시 그라디안 단위여야 합니다!

PRIMEM 단위
-----------

본초자오선(PRIME Meridian)이 나타나야 할 단위는?

-  CT 1.0 사양 (7.3.14 PRIMEM):
   "단위는 맥락으로부터 유추해야만 합니다. GEOGCS 안에서 PRIMEM 절이 나온다면 경도 단위가 지리 좌표계의 단위와 일치할 것입니다."
   주의: 지구 중심(geocentric) 좌표계의 경우, "GEOCCS 안에서 PRIMEM 절이 나온다면, 그 단위는 도 단위일 것입니다."

-  SF-SQL 사양(99-049)은 본초자오선의 단위 문제점을 적시하려 하지 않습니다.

-  EPSG 4807 변환에서 볼 수 있듯이 GEOGCS가 그라디안 단위인 경우에도 기존 ESRI EPSG의 WKT로의 변환은 본초자오선에 도 단위를 사용합니다:

   ::

      GEOGCS["GCS_NTF_Paris",
        DATUM["D_NTF",
          SPHEROID["Clarke_1880_IGN",6378249.2,293.46602]],
        PRIMEM["Paris",2.337229166666667],
        UNIT["Grad",0.015707963267948967]]

-  OGR는 :cpp:class:`OGRSpatialReference` 클래스에 대해 ESRI와 동일한 해석을 구현합니다 -- PRIMEM 경도가 항상 도 단위입니다. `GDAL 티켓 #4524 <https://trac.osgeo.org/gdal/ticket/4524>`_ 를 참조하십시오:

   ::

      GEOGCS["NTF (Paris)",
          DATUM["Nouvelle_Triangulation_Francaise_Paris",
              SPHEROID["Clarke 1880 (IGN)",6378249.2,293.4660212936269,
                  AUTHORITY["EPSG","7011"]],
              TOWGS84[-168,-60,320,0,0,0,0],
              AUTHORITY["EPSG","6807"]],
          PRIMEM["Paris",2.33722917,
              AUTHORITY["EPSG","8903"]],
          UNIT["grad",0.01570796326794897,
              AUTHORITY["EPSG","9105"]],
          AUTHORITY["EPSG","4807"]]

-  Cadcorp의 EPSG 4807 변환에서 볼 수 있듯이 Cadcorp는 CT 1.0 사양에 따라 PRIMEM을 구현합니다:

   ::

      GEOGCS["NTF (Paris)",
        DATUM["Nouvelle_Triangulation_Francaise",
          SPHEROID["Clarke 1880 (IGN)",6378249.2,293.466021293627,
            AUTHORITY["EPSG",7011]],
          TOWGS84[-168,-60,320,0,0,0,0],
          AUTHORITY["EPSG",6275]],
        PRIMEM["Paris",2.5969213,
          AUTHORITY["EPSG",8903]],
        UNIT["grad",0.015707963267949,
          AUTHORITY["EPSG",9105]],
        AXIS["Lat",NORTH],
        AXIS["Long",EAST],
        AUTHORITY["EPSG",4807]]

-  오라클 Spatial 8.1.7버전은 EPSG 4807로 여겨지는 다음과 같은 정의를 사용합니다. 흥미롭게도 이 정의는 그라디안 단위를 사용하지 않고, 본초자오선을 매우 낮은 정밀도의 라디안 단위로 표현하는 것으로 보입니다:

   ::

      GEOGCS [ "Longitude / Latitude (NTF with Paris prime meridian)",
        DATUM ["NTF (Paris meridian)",
          SPHEROID ["Clarke 1880 (IGN)", 6378249.200000, 293.466021]],
        PRIMEM [ "", 0.000649 ],
        UNIT ["Decimal Degree", 0.01745329251994330]]

TOWGS84 기울기의 부호
---------------------

논의
~~~~

EPSG는 9606(파라미터 7개를 사용하는 위치 벡터)와 9607(좌표 프레임 기울기) 두 가지 메소드 가운데 하나를 사용해서 파라미터 7개를 사용하는 부르사-울프(Bursa-Wolf) 파라미터를 정의합니다. 이 두 메소드의 유일한 차이점은 기울기 계수의 부호가 역전된다는 점입니다.

프랑크 바르메르담(Frank Warmerdam)은 WKT에서 TOWGS84 값은 9606(파라미터 7개를 사용하는 위치 벡터)으로 정의해야 할 것이라고 어떻게든 확신했습니다.그리고 9607 메소드를 보면 WKT에 TOWGS84 덩어리를 넣기 전에 기울기 부호를 뒤바꿔야 할 것입니다.

하지만 Cadcorp 사가 보내준 WKT 덤프에서는 9607 의미로 사용했습니다. 예를 들면 다음 항목은 부호를 바꾸지 않고 9607 값을 직접 사용한 것으로 보입니다.

::

    GEOGCS["DHDN",
       DATUM["Deutsche_Hauptdreiecksnetz",
         SPHEROID["Bessel 1841",6377397.155,299.1528128,AUTHORITY["EPSG","7004"]],
         TOWGS84[582,105,414,-1.04,-0.35,3.08,8.3],
         AUTHORITY["EPSG","6314"]],
       PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],
       UNIT["DMSH",0.0174532925199433,AUTHORITY["EPSG","9108"]],
       AXIS["Lat",NORTH],AXIS["Long",EAST],AUTHORITY["EPSG","4314"]]

CT 1.0 사양의 (22페이지의 7.3.18) TOWGS84[] 절을 읽어보아도, 9606과 9607을 그냥 부르사-울프 변환 파라미터로만 언급하고 있습니다. 12.3.15.2에서 12.3.27까지 훑어보아도 TOWGS84 기울기의 방향에 대해서는 특정하지 않고 있습니다.

현재 TOWGS84가 EPSG 9606 또는 EPSG 9607 어느쪽과 명확하게 일치하는지 탐구하고 있습니다. 향후 CT 사양이 EPSG 메소드 정의를 참조해서 이 문제를 명확하게 정리할지도 기대하고 있습니다.

Cadcorp 사는 정확한 부호 체계에 대해서는 확신할 수 없으며 사용할 수 있는 테스트 데이터에 가장 잘 작동하는 것으로 보이는 방향으로 프로그램을 작성했다고 답신했습니다.

CT 사양이 Cadorp 사의 (EPSG 9607을 따르는) 부호 사용례를 분명히 하는 경우 이를 받아들일 준비가 되어 있습니다.

OGR 구현의 현재 상태
~~~~~~~~~~~~~~~~~~~~

OGR의 WKT 가져오기/내보내기는 `proj.4와 마찬가지로 <http://proj4.org/parameters.html#towgs84-datum-transformation-to-wgs84>`_ EPSG 9606 규범(파라미터 7개를 사용하는 위치 벡터)을 가정합니다.

EPSG 9607로 표현된 EPSG 파라미터로부터 가져오는 경우, (기울기 파라미터의 부호를 무시하고) 제대로 된 변환을 수행합니다.

PRIMEM 상대 경도?
-----------------

또다른 관련 질문은 경도 투영 파라미터(예: 중앙 경선(central meridian))가 GEOGCS 본초자오선에 상대적인지 또는 그리니치 본초자오선에 상대적인지에 대한 것입니다. 가장 단순한 접근법은 모든 경도를 그리니치 본초자오선에 상대적인 것으로 취급하는 것이지만, 저자는 어느 순간 경도는 GEOGCS 본초자오선에 상대적이어야 한다고 확신했습니다. 하지만 CT 1.0 사양의 (PARAMETER를 설명하는) 7.3.11 단락을 살펴보니 이런 의견에 대한 어떤 지지도 찾아볼 수 없었으며, Cadcorp 사의 EPSG 25700 규범에 대한 조사 내용도 중앙 경선이 GEOGCS이 아니라 그리니치 본초자오선에 상대적이라고 시사합니다.

::

   PROJCS["Makassar (Jakarta) / NEIEZ",
       GEOGCS["Makassar (Jakarta)",
           DATUM["Makassar",
               SPHEROID["Bessel 1841",6377397.155,299.1528128,
                   AUTHORITY["EPSG","7004"]],
               TOWGS84[0,0,0,0,0,0,0],
               AUTHORITY["EPSG","6257"]],
           PRIMEM["Jakarta",106.807719444444,
               AUTHORITY["EPSG","8908"]],
           UNIT["DMSH",0.0174532925199433,
               AUTHORITY["EPSG","9108"]],
           AXIS["Lat","NORTH"],
           AXIS["Long","EAST"],
           AUTHORITY["EPSG","4804"]],
       PROJECTION["Mercator_1SP",
           AUTHORITY["EPSG","9804"]],
       PARAMETER["latitude_of_origin",0],
       PARAMETER["central_meridian",110],
       PARAMETER["scale_factor",0.997],
       PARAMETER["false_easting",3900000],
       PARAMETER["false_northing",900000],
       UNIT["metre",1,
           AUTHORITY["EPSG","9001"]],
       AXIS["X","EAST"],
       AXIS["Y","NORTH"],
       AUTHORITY["EPSG","25700"]]

이런 내용을 기반으로, 파라미터가 GEOGCS 단위를 사용하지만 파라미터가 GEOGCS 본초자오선에 상대적이지는 않다고 가정합니다.

WKT의 숫자 정밀도
-----------------

CT 사양은 WKT에 어떤 정밀도의 값을 저장해야 하는지 지정하지 않습니다. 오라클 같은 일부 구현들은 크기 조정 인자(Scale Factor) 같은 파라미터에 다소 제한된 정밀도를 사용하기 때문에 좌표계 설명을 비교하거나 비교할 수 있는 수치 결과를 얻기조차 어려워집니다.

가장 좋은 방법은 가능한 경우 EPSG 같은 소스 데이터베이스에 지정된 원본 정밀도를 보전하는 것입니다. 다수의 시스템이 정밀도를 추적하지 않는다는 점을 감안할 때, 적어도 C 언어의 "%.16g" 형식과 동등한 값을 생성하고 16자리 정밀도를 유지하면서 배정밀도 IEEE 부동소수점형 값의 정밀도 대부분을 캡처하는 것을 추천합니다.

기타 메모
---------

#. ESRI는 "등장방형(Equirectangular)"으로 알려진 도법에 대해 'Equidistant_Cylindrical'을 사용하는 것으로 보입니다.

문서 이력
---------

-  2018년: 이벤 루올(Even Rouault): OGR가 TOWGS84에 대해 EPSG 9606 규범을 구현한다는 사실을 분명히 밝혔습니다.

-  2018년: 이벤 루올(Even Rouault): CT 1.0 사양(7.3.14 PRIMEM)이 오류를 담고 있다는 언급을 삭제하고 OGR가 PRIMEM 경도에 도 단위를 사용한다는 사실을 명확하게 언급

-  2018년: 이벤 루올(Even Rouault): 하이퍼링크들 추가

-  2007년 이전: `프랑크 바르메르담(Frank Warmerdam) <https://web.archive.org/web/20130728081442/http://pobox.com/~warmerdam>`_ 이 초안을 작성했습니다.

