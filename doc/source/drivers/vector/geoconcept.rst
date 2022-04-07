.. _vector.geoconcept:

GeoConcept 텍스트 내보내기
==========================

.. shortname:: Geoconcept

.. built_in_by_default::

OGR GeoConcept 드라이버는 GeoConcept 텍스트 내보내기(GeoConcept Text Export) 파일 읽기 및 쓰기를 지원할 것입니다.

이 드라이버는 디렉터리에 있는 단일 GeoConcept 파일을 레이어들을 담고 있는 데이터셋으로 취급합니다. GeoConcept 파일의 확장자는 ``.txt`` 또는 ``.gxt`` 입니다.

현재 GeoConcept 드라이버는 멀티폴리곤, 라인 및 포인트만 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
    
GeoConcept 텍스트 파일 포맷 (GXT)
---------------------------------

GeoConcept는 GeoConcept 그룹이 개발한 GIS입니다.

GeoConcept는 객체 지향 GIS로, 객체를 "object"라고 하고 객체 유형을 "type/subtype"(상속을 허용하는 클래스)이라고 부릅니다.

GeoConcept는 자신의 가져오기/내보내기 포맷들 가운데, GXT라는 단순 텍스트 포맷을 제안합니다. .gxt 파일은 여러 type/subtype 유형의 object를 담을 수도 있습니다.

OGR GeoConcept 드라이버가 GeoConcept 텍스트 내보내기 파일을 읽고 쓸 수 있을 것입니다.

이 드라이버는 디렉터리에 있는 단일 GeoConcept 파일을 레이어들을 담고 있는 데이터셋으로 취급합니다. GeoConcept 파일의 확장자는 ``.txt`` 또는 ``.gxt`` 입니다.

현재 GeoConcept 드라이버는 멀티폴리곤, 라인 및 포인트만 지원합니다.

생성 문제점
---------------

GeoConcept 드라이버는 GeoConcept 파일(``.txt`` 또는 ``.gxt``)을 데이터셋으로 취급합니다.

GeoConcept 레이어 하나는 단일 유형의 도형만 담을 수 있지만, GeoConcept 파일은 여러 유형의 도형을 (레이어 당 유형 하나로) 저장할 수 있습니다.

이런 이유 때문에 ogr2ogr 유틸리티를 이용해서 또다른 포맷의 혼합 도형 레이어를 GeoConcept 포맷으로 변환하는 작업이 매우 어려워집니다. ogr2ogr 유틸리티는 소스 레이어로부터 도형들을 분리하는 기능을 지원하지 않기 때문입니다.

GeoConcept 하위 유형은 OGR 객체로 취급됩니다. 따라서 레이어 이름은 GeoConcept 유형 이름, ``'.'``, 그리고 GeoConcept 하위 유형 이름을 연결한 것입니다.

생성 작업 시에만 GeoConcept 유형 정의(``.gct`` 파일)을 이용할 수 있습니다.

관련 ``.gct`` 파일에 GeoConcept 객체 필드 정의를 저장하기 때문에, 필드에 여러 제한 사항이 적용됩니다(수정 요망):

-  속성 이름 길이는 무제한입니다.

-  정수, 실수 및 문자열 필드 유형만 지원합니다. 현재 다양한 목록 및 다른 필드 유형을 생성할 수 없습니다. (GeoConcept 모델에는 이런 유형들이 존재하지만, GeoConcept 드라이버가 아직 지원하지 않습니다.)

OGR GeoConcept 드라이버는 객체 삭제를 지원하지 않습니다.

데이터셋 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~

-  **EXTENSION=TXT|GXT**:
   GeoConcept 내보내기 파일 확장자를 설정합니다. GeoConcept 예전 배포판들은 ``TXT`` 를 사용했습니다. 현재 배포판은 ``GXT`` 를 사용합니다.

-  **CONFIG=path to the GCT**:
   GCT 파일은 GeoConcept 유형 정의를 서술합니다. 이 파일의 모든 줄은 반드시 ``//#`` 로 시작해야만 하며, 바로 뒤에 키워드가 와야만 합니다. ``//`` 로 시작하는 줄은 주석입니다.

   GeoConcept 내보내기 파일이 서로 다른 유형 및 관련된 하위 유형을 담을 수 있다는 사실을 기억하는 것이 중요합니다.

   -  환경설정 부분: GCT 파일의 첫 줄은 ``//#SECTION CONFIG`` 이며 마지막 줄은 ``//#ENDSECTION CONFIG`` 입니다. 모든 환경설정이 이 표시들 내부에 있습니다.

   -  맵 부분: 오직 이 문서 작성 시의 문서화를 위한 부분입니다. 이 부분은 ``//#SECTION MAP`` 으로 시작해서 ``//#ENDSECTION MAP`` 으로 끝납니다.

   -  유형 부분: 이 부분은 객체의 클래스를 정의합니다. 유형은 이름(키워드 ``Name``)과 ID(키워드 ``ID``)를 가지고 있습니다. 유형 하나는 하위 유형과 필드를 담고 있습니다. 이 부분은 ``//#SECTION TYPE`` 으로 시작해서 ``//#ENDSECTION TYPE`` 으로 끝납니다.

      -  하위 유형 부분: 이 하위 부분은 클래스 내부에 있는 객체의 유형을 정의합니다. 하위 유형은 이름(키워드 ``Name``), ID(키워드 ``ID``), 도형 유형(키워드 ``Kind``) 그리고 차원을 가지고 있습니다. POINT, LINE, POLYGON 도형 유형을 지원합니다. 이 드라이버의 현재 배포판은 TEXT 도형을 지원하지 않습니다. 차원은 2D, 3DM 또는 3D일 수 있습니다. 하위 유형은 필드를 담고 있습니다. 이 부분은 ``//#SECTION SUBTYPE`` 으로 시작해서 ``//#ENDSECTION SUBTYPE`` 으로 끝납니다.

         -  필드 부분: 사용자 필드를 정의합니다. 필드는 이름(키워드 ``Name``), ID(키워드 ``ID``) 그리고 유형(키워드 ``Kind``)을 가지고 있습니다. INT, REAL, MEMO, CHOICE, DATE, TIME, LENGTH, AREA 필드 유형을 지원합니다. 이 부분은 ``//#SECTION FIELD`` 로 시작해서 ``//#ENDSECTION FIELD`` 로 끝납니다.

      -  필드 부분: 유형 필드를 정의합니다. 앞을 참조하십시오.

   -  필드 부분: 일반 필드를 정의합니다. 그 중에서도 다음과 같은 규칙이 적용됩니다:

      -  프라이빗 필드 이름은 '@'으로 시작하며, ``Identifier``, ``Class``, ``Subclass``, ``Name``, ``NbFields``, ``X``, ``Y``, ``XP``, ``YP``, ``Graphics``, ``Angle`` 이 프라이빗 필드입니다.

      -  ``Identifier``, ``Class``, ``Subclass``, ``Name``, ``X``, ``Y`` 프라이빗 필드는 필수적입니다(환경설정에 존재해야만 합니다).

      -  하위 유형이 선형 (LINE) 유형인 경우, ``XP``, ``YP`` 필드를 반드시 선언해야만 합니다.

      -  하위 유형이 선형 또는 폴리곤 (LINE, POLY) 유형인 경우, ``Graphics`` 필드를 반드시 선언해야만 합니다.

      -  하위 유형이 점형 또는 텍스트 (POINT, TEXT) 유형인 경우, ``Angle`` 필드를 반드시 선언해야만 합니다.

   이 옵션을 사용하지 않으면, 드라이버가 레이어 이름을 기반으로 또는 ``-nln`` 옵션 사용 여부를 기준으로 유형 및 하위 유형 이름을 관리합니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **FEATURETYPE=TYPE.SUBTYPE**:
   생성할 객체를 정의합니다. ``TYPE`` 은 GCT 파일의 유형 부분에 있는 ``Name`` 가운데 하나에 대응합니다.
   ``SUBTYPE`` 은 GCT 파일의 앞의 유형 부분 내부의 하위 유형 부분에 있는 ``Name`` 가운데 하나에 대응합니다.

현재 데카르트 공간 좌표계의 경우 (표고 포함) 좌표를 소수점 이하 자릿수 2개로 작성하고, 지리 공간 좌표계의 경우 소수점 이하 자릿수 9개로 작성합니다.

예시
~~~~~~~~

.gct 파일 예시:
^^^^^^^^^^^^^^^^^^^^^^^^

::

   //#SECTION CONFIG
   //#SECTION MAP
   //# Name=SCAN1000-TILES-LAMB93
   //# Unit=m
   //# Precision=1000
   //#ENDSECTION MAP
   //#SECTION TYPE
   //# Name=TILE
   //# ID=10
   //#SECTION SUBTYPE
   //# Name=TILE
   //# ID=100
   //# Kind=POLYGON
   //# 3D=2D
   //#SECTION FIELD
   //# Name=IDSEL
   //# ID=101
   //# Kind=TEXT
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=NOM
   //# ID=102
   //# Kind=TEXT
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=WITHDATA
   //# ID=103
   //# Kind=INT
   //#ENDSECTION FIELD
   //#ENDSECTION SUBTYPE
   //#ENDSECTION TYPE
   //#SECTION FIELD
   //# Name=@Identifier
   //# ID=-1
   //# Kind=INT
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@Class
   //# ID=-2
   //# Kind=CHOICE
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@Subclass
   //# ID=-3
   //# Kind=CHOICE
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@Name
   //# ID=-4
   //# Kind=TEXT
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@X
   //# ID=-5
   //# Kind=REAL
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@Y
   //# ID=-6
   //# Kind=REAL
   //#ENDSECTION FIELD
   //#SECTION FIELD
   //# Name=@Graphics
   //# ID=-7
   //# Kind=REAL
   //#ENDSECTION FIELD
   //#ENDSECTION CONFIG

GeoConcept 텍스트 내보내기:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   //$DELIMITER "    "
   //$QUOTED-TEXT "no"
   //$CHARSET ANSI
   //$UNIT Distance=m
   //$FORMAT 2
   //$SYSCOORD {Type: 2001}
   //$FIELDS Class=TILE;Subclass=TILE;Kind=4;Fields=Private#Identifier    Private#Class    Private#Subclass    Private#Name    Private#NbFields    IDSEL    NOM    WITHDATA    Private#X    Private#Y    Private#Graphics
   -1    TILE    TILE    TILE    3    000-2007-0050-7130-LAMB93    0    50000.00     7130000.00    4    600000.00     7130000.00    600000.00     6580000.00    50000.00     6580000.00    50000.00     7130000.00
   -1    TILE    TILE    TILE    3    000-2007-0595-7130-LAMB93    0    595000.00    7130000.00    4    1145000.00    7130000.00    1145000.00    6580000.00    595000.00    6580000.00    595000.00    7130000.00
   -1    TILE    TILE    TILE    3    000-2007-0595-6585-LAMB93    0    595000.00    6585000.00    4    1145000.00    6585000.00    1145000.00    6035000.00    595000.00    6035000.00    595000.00    6585000.00
   -1    TILE    TILE    TILE    3    000-2007-1145-6250-LAMB93    0    1145000.00   6250000.00    4    1265000.00    6250000.00    1265000.00    6030000.00    1145000.00   6030000.00    1145000.00   6250000.00
   -1    TILE    TILE    TILE    3    000-2007-0050-6585-LAMB93    0    50000.00     6585000.00    4    600000.00     6585000.00    600000.00     6035000.00    50000.00     6035000.00    50000.00     6585000.00

사용례:
^^^^^^^^^^^^^^^^

-  GeoConcept 텍스트 내보내기 파일 생성하기:

::

   ogr2ogr -f "Geoconcept" -a_srs "+init=IGNF:LAMB93" -dsco EXTENSION=txt -dsco CONFIG=tile_schema.gct tile.gxt tile.shp -lco FEATURETYPE=TILE.TILE

-  기존 GeoConcept 텍스트 내보내기 파일에 새 객체를 추가하기:

::

   ogr2ogr -f "Geoconcept" -update -append tile.gxt tile.shp -nln TILE.TILE

-  GeoConcept 텍스트 내보내기 파일 레이어를 MapInfo 파일로 변환하기:

::

   ogr2ogr -f "MapInfo File" -dsco FORMAT=MIF tile.mif tile.gxt TILE.TILE

참고
~~~~~~~~

-  `GeoConcept 웹사이트 <http://www.geoconcept.com/>`_

