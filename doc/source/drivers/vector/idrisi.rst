.. _vector.idrisi:

Idrisi 벡터 (.VCT)
====================

.. shortname:: IDRISI

.. built_in_by_default::

VCT 드라이버는 .vct 확장자를 가진 Idrisi 벡터 포맷 읽기를 지원합니다. 이 드라이버는 포인트, 라인 및 폴리곤 도형을 인식합니다.

지리참조 식별 정보의 경우, .vdc 파일이 지리참조 상세 정보를 가지고 있는 파일을 가리키는 정보를 담고 있습니다. 이 파일의 확장자는 .ref이며 RST 이미지와 같은 폴더에 있거나, 없다면 Idrisi 설치 폴더에 있는 경우가 많습니다.

따라서 실행 중인 운영 체제에 Idrisi 소프트웨어가 있느냐 없느냐에 따라 이 드라이버가 작동하는 방식이 달라질 것입니다. IDRISIDIR 환경 변수를 Idrisi 주 설치 폴더를 가리키도록 설정하면 GDAL이 REF 파일에 있는 지리참조 및 투영법에 관한 더 상세한 정보를 찾을 수 있습니다.

이 드라이버는 Idrisi에서 UTM 및 미국 주(州) 평면 좌표계(State Plane Coordinate System; SPCS)의 지리참조 용 명명 규범을 인식하기 때문에 REF 파일에 접근할 필요가 없다는 사실을 기억해두십시오. RDC 파일의 "ref. system" 필드에 "utm-30n" 또는 "spc87ma1"을 지정한 데이터셋이 바로 이런 경우입니다. 이와 다른 지리 좌표계를 사용하는 RST 파일을 내보내는 경우 RDC 파일의 주석 부분에 REF 제안 내용을 생성할 것입니다.

이 드라이버는 .ADC / .AVL 아스키 파일로부터 속성을 가져올 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
