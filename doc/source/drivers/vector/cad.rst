.. _vector.cad:

================================================================================
CAD -- AutoCAD DWG
================================================================================

.. shortname:: CAD

.. build_dependencies:: (내부 libopencad 제공)

OGR DWG 지원은 libopencad에 기반하기 때문에, libopencad 문서에서 지원 DWG(DXF) 버전 목록을 볼 수 있습니다. 모든 도면(drawing) 요소들은 DXF 드라이버가 하는 것처럼 레이어 1개에 존재하는 것이 아니라 DWG 파일에서와 마찬가지로 개별 레이어들로 구분됩니다.

DWG 파일은 OGR를 통한 지리참조 정보를 가지고 있지 않다고 간주됩니다. 모든 객체는 다음과 같은 일반 속성들을 가질 것입니다:

-  CADGeometry: 표현되는 도형의 CAD 유형입니다.

-  Thickness: 객체 도면 단위의 굵기입니다. (해당 유형이 지원하지 않는 경우, 0.0으로 설정됩니다.)

-  Color (RGB): IntegerList가 색상의 R, G, B 구성요소를 담고 있습니다.

-  ExtendedEntity: 사용 가능한 경우, 단일 텍스트 속성을 형성하도록 모든 확장 요소 속성을 추가합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

지원 요소
------------------

다음과 같은 요소 유형들을 지원합니다:

-  POINT: 단순 포인트 도형 객체를 생성합니다.

-  LINE: LINESTRING으로 변환합니다. (꼭짓점의 벗지(budge) 속성이 설정된) 둥글림된(rounded) 폴리라인은 모자이크화(tessellated)합니다. 단일 꼭짓점 폴리라인은 POINT로 변환합니다.

-  CIRCLE, ARC: CIRCULARSTRING으로 변환합니다.

-  3DFACE: POLYGON으로 변환합니다.

이 드라이버는 읽기 전용입니다.

참고
--------

-  `ODA DWG 참조 <https://www.opendesign.com/files/guestdownloads/OpenDesign_Specification_for_.dwg_files.pdf>`_

-  `Libopencad 저장소 <https://github.com/nextgis-borsch/lib_opencad>`_

