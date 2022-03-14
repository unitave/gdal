.. _raster.gif:

================================================================================
GIF -- 그래픽 교환 포맷(Graphics Interchange Format)
================================================================================

.. shortname:: GIF

.. build_dependencies:: (내부 GIF 라이브러리 제공)

GDAL은 정규 및 교차삽입 GIF 파일 읽기 및 쓰기를 지원합니다. GIF 파일은 항상 색상표를 가진 8비트 밴드 1개를 가진 것으로 보입니다. GIF 파일은 지리참조를 지원하지 않습니다.

투명도를 가진 GIF 이미지는 0.0(투명) 알파값을 가진 것으로 표시된 해당 항목을 가질 것입니다. 또한, 이 투명값은 밴드에 NODATA 값으로 반환될 것입니다.

.gfw, .gifw 또는 .wld 확장자를 가진 ESRI 월드 파일이 존재하는 경우, 이미지의 지리변형을 확정하기 위해 해당 파일을 읽어와서 사용할 것입니다.

GIF 파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 XML 원본(raw) 내용으로 저장할 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_virtualio::

생성 문제점
---------------

GIF 파일은 "CreateCopy" 메커니즘을 이용해서 8비트 밴드 1개로만 생성할 수 있습니다. 색상표가 없는 파일로부터 작성하는 경우, 기본 회색조 색상표를 생성합니다. 투명 GIF 생성은 현재 지원하지 않습니다.

**WORLDFILE=ON**: 관련 ESRI 월드 파일(.wld)을 강제로 생성합니다.

**INTERLACING=ON**: 파일 생성 시 이 옵션을 설정하면 교차삽입 (점진적) GIF 파일을 생성할 수 있습니다.

GDAL의 내부 GIF 지원은 (제르종 일보르(Gershon Elbor), 에릭 레이먼드(Eric Raymond), 토시오 쿠라토미(Toshio Kuratomi)가 작성한) giflib 4.1.6 라이브러리의 소스를 기반으로 구현되었기 때문에, LZW 압축 GIF를 생성합니다.

이 드라이버는 `DM 솔루션즈 그룹 <http://www.dmsolutions.ca/>`_ 과 `CIET 인터내셔널 <http://www.ciet.org/>`_ 의 재정 지원으로 작성되었습니다.

참고
--------

-  `giflib 홈페이지 <http://sourceforge.net/projects/giflib/>`_
