.. _mg4lidar_view_point_cloud:

================================================
MrSID/MG4 LiDAR View 문서의 사양
================================================

1.0버전

개요
------------

이 문서는 LiDAR 포인트 클라우드에서 "뷰"로 사용되는 XML 문서의 사양을 정의합니다. 이 문서의 목적은 포인트 클라우드 데이터의 래스터화에 관한 상세 사항을 지정하기 위한 XML 기반 서식을 엄격하게 정의하는 것입니다. "빨리 적용할 수 있는 무언가"를 찾고 있다면 다음 예시들을 살펴보십시오.

문서 구조 (유용한 정보)
--------------------------------

다음은 View 문서의 전체적인 요소 구조를 약식으로 표현한 것입니다. 상위-하위(parent-child) 내포 및 요소들의 사용 빈도를 직관적으로 나타내기 위해 들여쓰기 및 정규 표현식 문법을 사용했습니다.

::

      PointCloudView
            InputFile +
            Datatype ?
            Band *
                  Channel ?
                  ClassificationFilter ?
                  ReturnNumberFilter ?
                  AggregationMethod ?
                  InterpolationMethod ?
            ClassificationFilter ?
            ReturnNumberFilter ?
            AggregationMethod ?
            InterpolationMethod ?
            ClipBox ?
            CellSize ?
            GeoReference ?

요소
--------

각 요소의 사양은 다음과 같습니다:

::

    ElementName
        Cardinality: 허용되는 사용 빈도
        Parents: 이 요소를 담고 있을 수 있는 요소(들)
        Contents: 이 요소 안에 들어 올 수 있는 요소(들)
        Attributes: (존재하는 경우) 허용되는 속성
        메모: 추가적인 활용 정보 또는 제약

PointClouldView
+++++++++++++++

설명: 문서의 루트 요소입니다.

Cardinality: 1

Parents: 없음 (루트 요소여야만 합니다)

Contents: 다음과 같은 하위 요소들

- InputFile
- Datatype
- Band
- ClassificationFilter
- ReturnNumberFilter
- AggregationMethod
- InterpolationMethod
- ClipBox
- CellSize
- GeoReference

Attributes:

- version - 이 속성은 반드시 존재해야 하며 1.0 값으로 설정해야만 합니다.

메모: 없음

InputFile
+++++++++

설명: 포인트 클라우드 데이터를 담고 있는 입력 파일을 지정합니다.

Cardinality: 1..n

Parents: PointClouldView

Contents: (파일명에 대응하는) 문자열

Attributes: 없음

메모:
- 입력 파일은 일반적으로 MrSID/MG4 LiDAR 파일일 것이지만, LAS 파일일 수도 있습니다.
- 입력 파일명이 상대 또는 절대 경로를 가지고 있을 수도 있습니다. 상대 경로일 경우, 이 View 문서를 담고 있는 디렉터리를 기준으로 하는 경로입니다.

Datatype
++++++++

설명: 채널 데이터를 강제 변환해야 할 데이터 유형을 지정합니다.

Cardinality: 0 또는 1

Parents: PointClouldView

Contents: (데이터 유형 이름에 대응하는) 문자열

Attributes: 없음

메모:

- 이 요소가 존재하지 않는 경우, 채널의 네이티브 데이터 유형을 사용합니다.
- GDALGetDataTypeByName이 반환하는 이름으로부터 파생된 다음과 같은 값들로 설정할 수 있습니다:

    - Byte
    - UInt16
    - Int16
    - UInt32
    - Int32
    - Float32
    - Float64

- C 스타일 cast() 함수를 통해 필요한 경우 데이터를 절단(truncate)해서라도 채널 데이터를 강제 변환합니다.

Band
++++

설명: 밴드 데이터를 처리하기 위해 어떤 밴드(들)를 어떤 방식으로 노출시킬지를 지정하는 목록입니다.

Cardinality: 0, 1 또는 3

Parents: PointClouldView

Contents: 다음과 같은 하위 요소들

- Channel 요소 0 또는 1개
- ClassificationFilter 요소 0 또는 1개
- ReturnNumberFilter 요소 0 또는 1개
- InterpolationMethod 요소 0 또는 1개
- AggregationMethod 0 또는 1개

Attributes: 없음

메모:

- 어떤 밴드도 지정하지 않는 경우는 밴드 1개만 모든 기본값으로 지정하는 경우와 동일합니다.

Channel
+++++++

설명: 입력 파일에 있는 채널 이름입니다.

Cardinality: Band 요소 당 0 또는 1

Parents: Band

Contents: 다음과 같은 기본 채널 이름을 사용합니다.

- X
- Y
- Z
- Intensity
- ReturnNum
- NumReturns
- ScanDir
- EdgeFlightLine
- ClassId
- ScanAngle
- UserData
- SourceId
- GPSTime
- Red
- Green
- Blue

Attributes: 없음

메모:

- 기본 이름이 아닌 사용자 지정 채널도 지원하며, 지정할 수도 있습니다.
- 이 요소가 생략된 경우, 밴드 채널이 기본값 Z로 설정될 것입니다.
- 이 채널 이름들은 MG4 DSDK의 PointData.h 파일로부터 파생되었습니다.

ClassificationFilter
++++++++++++++++++++

설명: 범주 코드가 지정한 값 가운데 하나인 포인트에 대한 필터입니다.

Cardinality: Band 요소 당 0 또는 1

Parents: Band 또는 PointCloudView

Contents: LAS 1.3 사양의 ASPRS 표준 LIDAR 포인트 범주가 정의하는, 공백으로 구분된 "Classification Values" (0-31)

Attributes: 없음

메모:

- 이 요소가 생략된 경우, 밴드에 어떤 범주 필터도 적용되지 않을 것입니다.
- 이 요소가 PointCloudView 요소의 하위 요소인 경우, (특정 밴드에 대해 대체하지 않는 이상) 모든 밴드에 필터를 적용합니다.
- 이 요소가 Band 요소의 하위 요소인 경우, 해당 밴드에만 필터를 적용하고 다른 모든 설정을 무시합니다.
- 숫자는 문자열이 아니라 필터를 표현하기 위해 쓰인다는 사실을 기억하십시오. 필터를 위한 단순하고 기본적인 명명 규범이 없으며, 특정 기존 응용 프로그램에서 이미 쓰이고 있는 필터들과 호환해야 하기 때문입니다.

ReturnNumberFilter
++++++++++++++++++

설명: 반환 숫자가 지정한 값 가운데 하나인 포인트에 대한 필터입니다.

Cardinality: Band 요소 당 0 또는 1

Parents: Band 또는 PointCloudView

Contents: 공백으로 구분된 숫자(1, 2, ...) 또는 문자열 LAST

Attributes: 없음

메모:

- 이 요소가 생략된 경우, 밴드에 어떤 숫자 필터도 적용되지 않을 것입니다.
- 이 요소가 PointCloudView 요소의 하위 요소인 경우, (특정 밴드에 대해 대체하지 않는 이상) 모든 밴드에 필터를 적용합니다.
- 이 요소가 Band 요소의 하위 요소인 경우, 해당 밴드에만 필터를 적용하고 다른 모든 설정을 무시합니다.

AggregationMethod
+++++++++++++++++

설명: 각 셀(픽셀) 하나가 값 하나를 노출시킬 수 있습니다. 2개 이상의 포인트가 단일 셀에 들어오는 경우, 이 메소드가 어떤 값을 노출시킬지 결정합니다.

Cardinality: Band 요소 당 0 또는 1

Parents: Band 또는 PointCloudView

Contents: Min, Max, 또는 Mean 가운데 하나인 문자열

Attributes: 없음

메모:

- 이 요소가 생략된 경우, 밴드에 "Mean" 집계 메소드가 적용될 것입니다.
- 이 요소가 PointCloudView 요소의 하위 요소인 경우, (특정 밴드에 대해 대체하지 않는 이상) 모든 밴드에 메소드를 적용합니다.
- 이 요소가 Band 요소의 하위 요소인 경우, 해당 밴드에만 필터를 적용하고 다른 모든 설정을 무시합니다.

InterpolationMethod
+++++++++++++++++++

설명: NODATA를 보간하기 위한 메소드와 파라미터입니다. NODATA 값도 지정합니다.

Cardinality: Band 요소 당 0 또는 1

Parents: Band 또는 PointCloudView

Contents: 다음 요소들 가운데 하나만

- None

- InverseDistanceToAPower

- MovingAverage

- NearestNeighbor

- Minimum

- Maximum

- Range

Attributes: 없음

Notes

- 보간 메소드들 (MovingAverage 등등) 각각이 해당 메소드 용 파라미터(들)에 대응하는 텍스트 문자열을 하위 요소로 가지고 있는 요소입니다. :ref:`gdal_grid_tut` 에서 이 보간 메소드들과 파라미터 문자열에 관해 설명하고 있습니다.
- 파라미터 설명을 보면, libc가 정의하는 값이 산출 데이터 유형이 지원할 수 있는 값들 가운데 가장 큰 값이라는 사실을 나타내기 위해 MAX를 사용합니다. 이 기본 습성을 무시하려면 사용자가 지정한 숫자가 지정한 데이터 유형과 잘 맞을 것인지 확인하십시오.
- 이 요소가 생략된 경우, 밴드에 "None" 보간 메소드가 적용될 것입니다.
- 이 요소가 PointCloudView 요소의 하위 요소인 경우, (특정 밴드에 대해 대체하지 않는 이상) 모든 밴드에 이 메소드를 적용합니다.
- 이 요소가 Band 요소의 하위 요소인 경우, 해당 밴드에만 필터를 적용하고 다른 모든 설정을 무시합니다.

ClipBox
+++++++

설명: 뷰 영역의 지리 범위

Cardinality: 0 또는 1

Parents: PointClouldView

Contents: Double형 숫자 4개 또는 6개; Double형 값 자리에 문자열 NOFILTER를 지정할 수도 있습니다.

Attributes: 없음

메모:

- 값 6개 전체(순서대로): xmin, xmax, ymin, ymax, zmin, zmax.
- 문자열 NOFILTER는 입력 파일의 최소 경계 직사각형(Minimum Bounding Rectangle; MBR)의 대응하는 값을 사용하라는 뜻입니다. 문자열 NOFILTER 값으로 포인트를 필터링하지 않습니다.
- Double형 숫자 4개만 지정하는 경우, zmin 및 zmax를 NOFILTER라고 가정합니다.
- 이 요소가 존재하지 않는 경우, 입력 파일의 MBR을 자르기 상자(clip box)라고 가정합니다.

CellSize
++++++++

설명: (정사각형) 픽셀의 한 변의 지표 단위 길이

Cardinality: 0 또는 1

Parents: PointClouldView

Contents: Double형 숫자 1개

Attributes: 없음

메모:

- 이 요소를 사용해서 산출 래스터의 크기를 결정합니다.
- 이 요소가 생략된 경우, 셀 크기 기본값은 (포인트가 전체 범위에 걸쳐 균일하게 분포되어 있다는 가정 하에) 평균 (선형) 포인트 간격입니다.

GeoReference
++++++++++++

설명: 뷰의 좌표계입니다.

Cardinality: 0 또는 1

Parents: PointClouldView

Contents: (WKT에 대응하는) 문자열

Attributes: 없음

메모:

- 이 요소가 생략된 경우, 입력 파일의 WKT를 사용합니다. 2개 이상의 파일이 서로 다른 WKT를 가지고 있는 경우, 어떤 지리참조도 정의하지 않습니다.
- 일반적으로 MG4 파일이 적절한 지리참조 정보 없이 생성된 경우 이 요소를 사용합니다. 측정 단위, 수평 좌표계 및 수직 좌표계의 몇몇 조합이 누락되는 경우를 꽤 흔히 볼 수 있습니다.

추가 요구 사항
-----------------------

인식되지 않는 모든 요소를 오류로 취급할 것입니다.

인식되지 않는 모든 속성을 오류로 취급할 것입니다.

이 문서 사양은 어떤 상위 요소 안에 있는 하위 요소들의 사전적인 정렬을 요구하지 않습니다.

예시
--------

가능한 한 가장 단순한 .view 파일
++++++++++++++++++++++++++++++

MG4 파일을 볼 수 있는 가장 단순한 방법은 뷰 파일(.view) 안에 MG4 파일을 다음과 같이 참조시키는 것입니다. 이때 MG4 파일을 가리키는 상대 참조는 MG4 파일이 .view 파일과 같은 디렉터리에 존재해야만 한다는 의미입니다. 어떤 밴드도 명확하게 매핑하고 있지 않기 때문에, 표고뿐인 기본 이미지를 보게 됩니다. 기본적으로 평균을 기반으로 집계합니다. 다시 말해 포인트 2개(또는 그 이상)가 단일 셀 안에 들어오는 경우 포인트 2개의 평균값을 노출시킬 것입니다. 어떤 필터링도 하지 않기 때문에 범주 코드나 반환 숫자에 상관없이 모든 포인트를 수집하게 될 것입니다. 표고의 네이티브 데이터 유형이 "Float64"이기 때문에 밴드를 Float64 데이터 유형으로 노출시킬 것입니다.

.. code-block:: xml

    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
    </PointCloudView>

 
데이터 잘라내기
++++++++++++++

앞의 예시와 비슷하지만, 선택 옵션인 ClipBox 태그를 이용해서 클라우드를 관통하는 북-남 방향 300미터 길이의 견본(swatch)을 선택합니다. 동-서 방향으로 데이터를 잘라내려면, NOFITLER를 사용하는 대신 그 자리에 명확하게 지정해주면 됩니다. 마찬가지로 Z 방향으로도 잘라낼 수 있습니다.

.. code-block:: xml

    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
        <ClipBox>505500 505800 NOFILTER NOFILTER</ClipBox>
    </PointCloudView>

 
맨땅(bare earth) (최대) DEM으로 노출시키기
++++++++++++++++++++++++++++++++++++++++

이번엔 단일 밴드(표고)를 노출시켰지만 "Ground"로 분류된 포인트들만 원한다고 해봅시다. ClassificationFilter 태그로 2라는 값을 -- "Ground" 포인트를 규정하는 ASPRS 포인트 범주 코드를 -- 지정합니다. 또한, 기본 "Mean" 집계 대신 "Max"를 지정합니다. 이렇게 하면 포인트 2개(또는 그 이상)가 단일 셀 안에 들어오는 경우 포인트 2개 가운데 더 큰 표고값을 노출시킵니다.

.. code-block:: xml

    <PointCloudView>
        <InputFile>E:\ESRIDevSummit2010\Tetons.sid</InputFile>
        <Band> <!-- Max Bare Earth-->
            <Channel>Z</Channel>
            <AggregationMethod>Max</AggregationMethod>
            <ClassificationFilter>2</ClassificationFilter>
        </Band>
    </PointCloudView>

강도 이미지
+++++++++++++++

포인트 클라우드로부터 강도(intensity) 이미지를 노출시킵니다.

.. code-block:: xml

    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
        <Band>
            <!-- All intensities -->
            <Channel>Intensity</Channel>
        </Band>
    </PointCloudView>

RGB 이미지
+++++++++

일부 포인트 클라우드 이미지는 RGB 데이터를 포함하고 있습니다. 이런 경우, .view 파일에 다음과 같이 작성하면 RGB 데이터를 노출시킬 수 있습니다.

.. code-block:: xml

    <PointCloudView>
        <InputFile>Grass Lake Small.xyzRGB.sid</InputFile>
        <Band>
            <Channel>Red</Channel>
        </Band>
        <Band>
            <Channel>Green</Channel>
        </Band>
        <Band>
            <Channel>Blue</Channel>
        </Band>
    </PointCloudView>
