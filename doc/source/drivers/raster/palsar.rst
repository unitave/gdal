.. _raster.palsar:

================================================================================
JAXA PALSAR 처리 상품
================================================================================

.. shortname:: JAXAPALSAR

.. built_in_by_default::

이 드라이버는 JAXA PALSAR 처리기(processor)가 처리한 PALSAR 상품에 대한 강화된 지원을 제공합니다. 이 지원에는 다음 기관이 생산하는 상품이 포함됩니다:

-  JAXA(Japanese Aerospace eXploration Agency): 일본 우주항공연구개발기구
-  AADN(America's ALOS Data Node): 알래스카 위성 운영 시설
-  ESA(European Space Agency): 유럽 우주국

이 드라이버는 벡셀(Vexcel) 처리기를 이용해 생성된 상품은 지원하지 않습니다. (예: ERSDAC 및 연계 기관이 배포하는 상품)

PALSAR 상품의 다음 기능들을 지원합니다:

-  1.1 및 1.5수준 처리 상품 읽기
-  1.5수준 상품에 대한 지리참조 작업
-  기본 메타데이터(센서 정보, 지표 픽셀 간격 등등)
-  다중 채널 데이터 (예: 이중 편파(dual-polarization) 또는 완전한 편광 데이터셋)

이 드라이버는 읽기전용입니다.

PALSAR 상품을 열려면, 볼륨 디렉터리 파일을 (예를 들면 VOL-ALPSR000000000-P1.5_UA 또는 VOL-ALPSR000000000-P1.1__A 파일을) 선택하십시오. 그러면 드라이버가 볼륨 디렉터리 파일이 담고 있는 정보를 이용해서 다양한 이미지 파일(IMG-\* 파일들)은 물론 리더(leader) 파일을 찾을 것입니다. 이 드라이버가 정확하게 작동하려면 리더 파일이 필수적이라는 사실을 기억하십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `RESTEC 샘플 데이터 <http://www.alos-restec.jp/en/staticpages/index.php/service-sampledata>`_
