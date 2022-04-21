.. _vector.selafin:

세라핀 파일
=============

.. shortname:: Selafin

.. built_in_by_default::

OGR는 2차원 세라핀(Selafin/Seraphin) 파일 읽기를 지원합니다. 세라핀은 오픈 소스 `텔레맥 수리 모델(Telemac hydraulic model) <http://www.opentelemac.org>`_ 에서 쓰이는 지리 파일의 일반 산출 및 입력 포맷입니다. 이 파일 포맷은 서로 다른 시계열 단계에 있는 포인트 객체 집합의 숫자형 속성을 설명하는 데 적합합니다. 이 포인트 객체는 보통 유한 요소 모델(finite-element model)에 있는 노드에 대응합니다. 이 파일은 이런 노드들이 형성하는 요소들을 설명하는 연결성(connectivity) 테이블도 가지고 있는데, 세라핀 드라이버는 이 테이블도 읽을 수 있습니다.

세라핀 드라이버는 VSI 가상 파일을 세라핀 데이터소스로 사용할 수 있습니다.

이 드라이버는 세라핀 파일에 대한 완전한 읽기 및 쓰기를 지원합니다. 하지만, 요소(폴리곤) 객체와 노드(포인트) 객체가 밀접하게 관련되어 있는 세라핀 파일의 특수한 성질 때문에 세라핀 레이어 상에 작성 작업을 하는 것이 직관에 반대되는 결과로 이어질 수 있습니다. 일반적으로, 세라핀 데이터소스의 어떤 한 레이어에 작성 작업을 하면 다른 모든 레이어에도 부작용을 일으킬 것입니다. 또한, **업데이트 모드에서 동일한 레이어를 한 번 이상 열지 말아야 합니다**. 단일 데이터소스에 쓰기 작업 2개를 동시에 처리하는 것이 복구 불가능한 데이터 오류로 이어질 수 있기 때문입니다. 이 드라이버는 데이터소스를 업데이트 모드로 열 때마다 경고를 발합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

매직 넘버
-----------

세라핀 파일은 일반 확장자를 가지고 있지 않습니다. 파일 시작 부분에 있는 12개의 매직 넘버(magic byte)로 세라핀 포맷이 맞는지 테스트합니다:

-  파일의 처음 4바이트가 00 00 00 50 (16진법) 값들을 담고 있어야 합니다. 이 값들은 실제로 파일에 있는 80바이트 길이의 문자열의 시작을 의미합니다.
-  파일의 84바이트 위치부터, 00 00 00 50 00 00 00 04 (16진법) 값들이 읽혀야 합니다.

이 드라이버는 이 두 가지 조건을 만족하는 파일을 세라핀 파일로 간주하고 성공적으로 열었다고 리포트할 것입니다.

포맷
------

세라핀 포맷은 포터블하고 컴팩트한 방식으로 데이터 구조를 담도록, 그리고 데이터에 효율적인 임의 접근이 가능하도록 설계되었습니다. 세라핀 파일은 이런 목적을 위한 일반 구조를 가진 바이너리 파일입니다.

요소
~~~~~~~~

세라핀 파일은 요소들의 병렬 배치(juxtaposition)로 이루어져 있습니다. 요소 유형은 다음 가운데 하나입니다:

-  정수형
-  문자열
-  부동소수점형
-  정수값 배열
-  부동소수점값 배열

.. list-table:: Selafin Element Types
   :header-rows: 1
   
   * - 요소
     - 내부 표현
     - 비고
   * - Integer
     - a b c d
     - 정수형은 빅 엔디언 (최상위 바이트 우선) 서식의 4바이트로 저장됩니다. 정수값은 '2\ :sup:`24`.a+2\ :sup:`16`.b+2\ :sup:`8`.c+d'입니다.
   * - Floating point
     - a b c d
     - 부동소수점형은 빅 엔디언 규범(최상위 바이트 우선) 아래 IEEE 754 서식의 4바이트로 저장됩니다. 런타임에서 첫 번째 부동소수점형 값을 읽을 때 엔디언 여부를 탐지합니다.
   * - String
     - Length 1 2 ... Length
     - 문자열은 세 부분으로 저장됩니다:

         -  문자열의 (문자 단위) 길이를 담고 있는 정수, 4바이트
         -  문자열에 있는 문자들의 순열, 문자 당 1바이트
         -  문자열의 길이를 담고 있는 정수의 반복

   * - Array of integers
     - Length 1 2 ... Length
     - 정수값 배열은 세 부분으로 저장됩니다:

         -  배열의 (바이트 단위, 즉 요소 개수의 4배) 길이를 담고 있는 정수, 4바이트
         -  배열에 있는 정수들의 순열, 앞에서 설명한 대로 정수 당 4바이트
         -  배열의 길이를 담고 있는 정수의 반복

   * - Array of floating point values
     - Length 1 2 ... Length
     - 부동소수점값 배열은 세 부분으로 저장됩니다:

         -  배열의 (바이트 단위, 즉 요소 개수의 4배) 길이를 담고 있는 정수, 4바이트
         -  배열에 있는 부동소수점형 숫자들의 순열, 앞에서 설명한 대로 부동소수점형 숫자 당 4바이트
         -  배열의 길이를 담고 있는 정수의 반복

전체 구조
~~~~~~~~~~~~~~

세라핀 파일의 헤더는 다음 요소들을 정확히 다음 순서대로 담고 있습니다:

-  연구 제목을 담은 문자 80개 길이의 *문자열*:
   마지막 문자 8개는 "SERAPHIN" 또는 "SERAFIN" 또는 "SERAFIND" 가운데 하나여야 합니다.

-  요소를 딱 2개 가진 *정수값 배열*:
   첫 번째 요소는 변수(속성) *nVar* 의 개수이고, 두 번째 요소는 무시합니다.

-  변수의 이름을 담은 *nVar 문자열*:
   각 문자열의 길이는 문자 32개입니다.

-  요소를 딱 10개 가진 *정수값 배열*:

   -  세 번째 요소가 모델 원점(origin)의 X 좌표입니다.
   -  네 번째 요소가 모델 원점의 Y 좌표입니다.
   -  열 번째 요소가 모델의 날짜를 읽어와야 하는지를 나타내는 *isDate* 입니다. (다음 항목 참조)
   -  덧붙여, 현재 수리 소프트웨어는 두 번째 요소를 사용하지 않지만, 이 드라이버가 데이터소스의 공간 좌표계를 투영법의 EPSG 번호를 의미하는 단일 정수 형식으로 저장하기 위해 사용합니다.

-  *isDate*\ =1인 경우, 요소를 딱 6개 가진 *정수값 배열*:
   모델의 시작일(연, 월, 일, 시, 분, 초)을 담고 있습니다.

-  요소를 딱 4개 가진 *정수값 배열*.:

   -  첫 번째 요소가 *nElements* 요소의 개수입니다.
   -  두 번째 요소가 *nPoints* 포인트의 개수입니다.
   -  세 번째 요소가 *nPointsPerElement* 요소 당 포인트의 개수입니다.
   -  네 번째 요소는 반드시 1이어야만 합니다.

-  요소를 딱 *nElements*nPointsPerElement* 개 가진 *정수값 배열*:
   연속하는 *nPointsPerElement* 집합은 각각 요소를 구성하는 포인트의 (1에서 시작하는) 개수 목록입니다.

-  요소를 딱 *nPoints* 개 가진 *정수값 배열*:
   드라이버가 무시합니다. (요소는 내부 포인트에 대해 0이어야 하고 제한 조건이 적용되는 경계 포인트에 대해서는 또다른 값이어야 합니다.)

-  요소를 딱 *nPoints* 개 가진 *부동소수점값 배열*:
   포인트의 X 좌표를 담고 있습니다.

-  요소를 딱 *nPoints* 개 가진 *부동소수점값 배열*:
   포인트의 Y 좌표를 담고 있습니다.

파일의 나머지 부분은 이어지는 각 시계열 단계의 실제 데이터를 담고 있습니다. 시계열 단계는 다음과 같은 요소들을 담고 있습니다:

-  요소를 딱 1개 가진 *부동소수점값 배열*:
   시뮬레이션의 시작일에 상대적인 시계열 단계의 날짜입니다. (보통 초 단위입니다.)

-  배열의 각 항목이 딱 *nPoints* 개의 요소를 가진 *부동소수점값 nVar 배열*:
   현재 시계열 단계에 있는 각 포인트의 각 속성값을 담고 있습니다.

파일과 레이어 사이의 매핑
-------------------------------

세라핀 데이터소스의 레이어
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Selafin driver accepts only Selafin files as data sources.

Each Selafin file can hold one or several time steps. All the time steps
are read by the driver and two layers are generated for each time step:

-  one layer with the nodes (points) and their attributes: its name is
   the base name of the data source, followed by "_p" (for Points);
-  one layer with the elements (polygons) and their attributes
   calculated as the averages of the values of the attributes of their
   vertices: its name is the base name of the data source, followed by
   "_e" (for Elements).

Finally, either the number of the time step, or the calculated date of
the time step (based on the starting date and the number of seconds
elapsed), is added to the name. A data source in a file called Results
may therefore be read as several layers:

-  ``Results_p2014_05_01_20_00_00``, meaning that the layers holds the
   attributes for the nodes and that the results hold for the time step
   at 8:00 PM, on May 1st, 2014;
-  ``Results_e2014_05_01_20_00_00``, meaning that the layers holds the
   attributes for the elements and that the results hold for the time
   step at 8:00 PM, on May 1st, 2014;
-  ``Results_p2014_05_01_20_15_00``, meaning that the layers holds the
   attributes for the elements and that the results hold for the time
   step at 8:15 PM, on May 1st, 2014;
-  ...

레이어에 대한 제약 사항
~~~~~~~~~~~~~~~~~~~~~

Because of the `format of the Selafin file <#format>`_, the layers in a
single Selafin datasource are not independent from each other. Changing
one layer will most certainly have side effects on all other layers. The
driver updates all the layers to match the constraints:

-  All the point layers have the same number of features. When a feature
   is added or removed in one layer, it is also added or removed in all
   other layers.
-  Features in different point layers share the same geometry. When the
   position of one point is changed, it is also changed in all other
   layers.
-  All the element layers have the same number of features. When a
   feature is added or removed in one layer, it is also added or removed
   in all other layers.
-  All the polygons in element layers have the same number of vertices.
   The number of vertices is fixed when the first feature is added to an
   element layer, and can not be changed afterwards without recreating
   the datasource from scratch.
-  Features in different element layers share the same geometry. When an
   element is added or removed in one layer, it is also added or removed
   in all other layers.
-  Every vertex of every feature in an element layer has a corresponding
   point feature in the point layers. When an element feature is added,
   if its vertices do not exist yet, they are created in the point
   layers.
-  Points and elements layers only support attributes of type "REAL".
   The format of real numbers (width and precision) can not be changed.

레이어 필터링 사양
-----------------------------

As a single Selafin files may hold millions of layers, and the user is
generally interested in only a few of them, the driver supports
syntactic sugar to filter the layers before they are read.

When the datasource is specified, it may be followed immediately by a
*layer filtering specification.*, as in ``Results[0:10]``. The effects
of the layer filtering specification is to indicate which time steps
shall be loaded from all Selafin files.

The layer filtering specification is a comma-separated sequence of range
specifications, delimited by square brackets and maybe preceded by the
character 'e' or 'p'. The effect of characters 'e' and 'p' is to select
respectively either only elements or only nodes. If no character is
added, both nodes and elements are selected. Each range specification
is:

-  either a single number, representing one single time step (whose
   numbers start with 0),
-  or a set of two numbers separated by a colon: in that case, all the
   time steps between and including those two numbers are selected; if
   the first number is missing, the range starts from the beginning of
   the file (first time step); if the second number is missing, the
   range goes to the end of the file (last time step);

Numbers can also be negative. In this case, they are counted from the
end of the file, -1 being the last time step.

Some examples of layer filtering specifications:

============ =================================================================================
[0]          First time step only, but return both points and elements
[e:9]        First 10 time steps only, and only layers with elements
[p-4:]       Last 4 time steps only, and only layers with nodes
[3,10,-2:-1] 4\ :sup:`th`, 11\ :sup:`th`, and last two time steps, for both nodes and elements
============ =================================================================================

데이터소스 생성 옵션
---------------------------

Datasource creation options can be specified with the "``-dsco``" flag
in ogr2ogr.

TITLE
   Title of the datasource, stored in the Selafin file. The title must
   not hold more than 72 characters. If it is longer, it will be
   truncated to fit in the file.
DATE
   Starting date of the simulation. Each layer in a Selafin file is
   characterized by a date, counted in seconds since a reference date.
   This option allows providing the reference date. The format of this
   field must be YYYY-MM-DD_hh:mm:ss. The format does not mention the
   time zone.

An example of datasource creation option is:
``-dsco TITLE="My simulation" -dsco DATE=2014-05-01_10:00:00``.

레이어 생성 옵션
----------------------

Layer creation options can be specified with the "``-lco``" flag in
ogr2ogr.

DATE
   Date of the time step relative to the starting date of the simulation
   (see `Datasource creation options <#DCO>`_). This is a single
   floating-point value giving the number of seconds since the starting
   date.

An example of datasource creation option is: ``-lco DATE=24000``.

세라핀 데이터소스의 생성 및 업데이트에 관한 메모
---------------------------------------------------------------

The driver supports creating and writing to Selafin datasources, but
there are some caveats when doing so.

When a new datasource is created, it does not contain any layer, feature
or attribute.

When a new layer is created, it automatically inherits the same number
of features and attributes as the other layers of the same type (points
or elements) already in the datasource. The features inherit the same
geometry as their corresponding ones in other layers. The attributes are
set to 0. If there was no layer in the datasource yet, the new layer is
created with no feature and attribute.In any case, when a new layer is
created, two layers are actually added: one for points and one for
elements.

New features and attributes can be added to the layers or removed. The
behavior depends on the type of layer (points or elements). The
following table explains the behavior of the driver in the different
cases.

================================== ========================================================================================================================================================================================= ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Operation                          Points layers                                                                                                                                                                             Element layers
================================== ========================================================================================================================================================================================= ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Change the geometry of a feature   The coordinates of the point are changed in the current layer and all other layers in the datasource.                                                                                     The coordinates of all the vertices of the element are changed in the current layer and all other layers in the datasource. It is not possible to change the number of vertices. The order of the vertices matters.
Change the attributes of a feature The attributes of the point are changed in the current layer only.                                                                                                                        No effect.
Add a new feature                  A new point is added at the end of the list of features, for this layer and all other layers. Its attributes are set to the values of the new feature.                                    The operation is only allowed if the new feature has the same number of vertices as the other features in the layer. The vertices are checked to see if they currently exist in the set of points. A vertex is considered equal to a point if its distance is less than some maximum distance, approximately equal to 1/1000\ :sup:`th` of the average distance between two points in the points layers. When a corresponding point is found, it is used as a vertex for the element. If no point is found, a new is created in all associated layers.
Delete a feature                   The point is removed from the current layer and all point layers in the datasource. All elements using this point as a vertex are also removed from all element layers in the datasource. The element is removed from the current layer and all element layers in the datasource.
================================== ========================================================================================================================================================================================= ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

Typically, this implementation of operations is exactly what you'll
expect. For example, ogr2ogr can be used to reproject the file without
changing the inner link between points and elements.

It should be noted that update operations on Selafin datasources are
very slow. This is because the format does no allow for quick insertions
or deletion of features and the file must be recreated for each
operation.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기 전용) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

기타 메모
-----------

There is no SRS specification in the Selafin standard. The
implementation of SRS is an addition of the driver and stores the SRS in
an unused data field in the file. Future software using the Selafin
standard may use this field and break the SRS specification. In this
case, Selafin files will still be readable by the driver, but their
writing will overwrite a value which may have another purpose.
