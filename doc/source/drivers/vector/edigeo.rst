.. _vector.edigeo:

EDIGEO
======

.. shortname:: EDIGEO

.. built_in_by_default::

이 드라이버는 프랑스의 EDIGEO 정보 교환 포맷 -- 강력한 서술 케이퍼빌리티, 위상 모델링 등등을 이용해서 GIS 응용 프로그램들 사이에 지리 정보를 교환하려는 목적으로 개발된 텍스트 기반 파일 포맷 -- 으로 인코딩된 파일의 읽기를 지원합니다.

이 드라이버는 프랑스의 DGI((Direction Générale des Impots - 국세청)가 생산한 PCI(Plan Cadastral Informatisé - 수치지적도) 파일을 읽기 위해 개발되었습니다. 이 드라이버는 DGI의 다른 EDIGEO 기반 상품들도 열 수 있을 것입니다.

이 드라이버에 EDIGEO 정보 교환을 설명하는 .THF 파일을 반드시 지정해야만 하며, 그러면 이 드라이버는 관련 .DIC, .GEO, .SCD, .QAL 및 .VEC 파일들을 읽어올 것입니다.

레이어의 공간 좌표계를 정확하게 작성하려면, PROJ 리소스 파일이 있는 디렉터리에 IGN 공간 좌표계 정의를 담고 있는 IGNF 파일을 배치해야만 합니다.

파일 집합 전체를 메모리로 파싱할 것입니다. 대용량 EDIGEO 정보 교환 포맷을 처리하는 경우 제약이 될 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

라벨
------

EDIGEO PCI 파일의 경우, ID_S_OBJ_Z_1_2_2 레이어에 라벨을 담고 있습니다. OGR는 :ref:`ogr_feature_style` 에 따라 스타일을 내보낼 것입니다.

이때 다음과 같은 필드들을 추가할 것입니다:

-  OGR_OBJ_LNK: 이 라벨에 링크된 객체의 ID

-  OBJ_OBJ_LNK_LAYER: 링크된 객체가 있는 레이어의 이름

-  OGR_ATR_VAL: (OGR_OBJ_LNK 객체의 ATR 속성에 있는) 출력할 속성값

-  OGR_ANGLE: 도 단위 기울기 각도 (0 = 수평, 시계 반대 방향)

-  OGR_FONT_SIZE: 기본값이 2인 :decl_configoption:`OGR_EDIGEO_FONT_SIZE_FACTOR` 환경설정 옵션의 값으로 곱한 HEI 속성값

이 필드들을 FON (글꼴 패밀리) 속성과 결합하면, 예를 들어 QGIS에서 스타일을 정의할 수 있습니다.

OGR는 기본적으로 ID_S_OBJ_Z_1_2_2 레이어의 다양한 라벨들이 xxx=OBJ_OBJ_LNK_LAYER의 값에 따라 특정 레이어들(xxx_LABEL)에 할당되도록 레이어를 생성합니다. :decl_configoption:`OGR_EDIGEO_CREATE_LABEL_LAYERS` 환경설정 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

참고
--------

-  `EDIGEO 표준 소개 <http://georezo.net/wiki/main/donnees/edigeo>`_ (프랑스어)

-  `EDIGEO 표준 - AFNOR NF Z 52000 <http://georezo.net/wiki/_media/main/geomatique/norme_edigeo.zip>`_ (프랑스어)

-  `Standard d'échange des objets du PCI selon la norme EDIGEO <https://www.craig.fr/sites/www.craig.fr/files/contenu/60-2010-le-pci-en-auvergne/docs/edigeopci.pdf>`_ (프랑스어)

-  `프랑스 수치지적도 홈페이지 <http://www.cadastre.gouv.fr>`_ (프랑스어)

-  `Geotools EDIGEO 모듈 설명 <http://old.geotools.org/77692976.html>`_ (영어), `유지되지 않아 제거됨 <https://github.com/geotools/geotools/pull/2446/files>`_

-  `EDIGEO 데이터 샘플 <https://github.com/geotools/geotools/tree/affa340d16681f1bb78673d23fb38a6c1eb2b38a/modules/unsupported/edigeo/src/test/resources/org/geotools/data/edigeo/test-data>`_

