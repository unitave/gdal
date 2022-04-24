.. _vector.xls:

XLS - 마이크로소프트 엑셀 포맷
==============================

.. shortname:: XLS

.. build_dependencies:: libfreexl

XLS 드라이버는 마이크로소프트 엑셀(Excel) 포맷으로 된 스프레드시트를 읽어옵니다. GDAL/OGR가 (GPL/LPL/MPL 사용 허가가 있어야 하는) FreeXL 라이브러리를 대상으로 빌드되어 있어야만 하며, 이 드라이버가 어떤 엑셀 파일을 어디까지 지원하느냐에 대해서는 FreeXL 라이브러리 자체와 동일한 제약 조건을 가집니다. (다시 말해 이 문서 작성 당시 특히 -- FreeXL 1.0.0a 버전 -- 공식(formula)을 지원하지 않는다는 뜻입니다.)

각 시트를 OGR 레이어로 표현합니다. 도형을 직접 지원하지 않습니다. (그러나 도형 지원을 위해 OGR VRT 케이퍼빌리티를 이용할 수도 있습니다.)

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`OGR_XLS_HEADERS` = FORCE/DISABLE/AUTO:
   이 드라이버는 기본적으로 첫 줄이 열 이름일 수도 있는지 탐지하기 위해 각 시트의 첫 줄을 읽어올 것입니다.
   이 옵션을 FORCE로 설정하면, 드라이버가 첫 줄을 헤더 줄로 간주할 것입니다.
   DISABLE로 설정하면, 첫 줄을 첫 번째 객체로 간주할 것입니다.
   기본값인 AUTO로 설정하면, 자동으로 탐지할 것입니다.

-  :decl_configoption:`OGR_XLS_FIELD_TYPES` = STRING/AUTO:
   이 드라이버는 기본적으로 필드의 데이터 유형을 탐지하려 시도할 것입니다.
   이 옵션을 STRING으로 설정하면, 모든 필드가 문자열 유형이 될 것입니다.

참고
----

-  `FreeXL 라이브러리 홈페이지 <https://www.gaia-gis.it/fossil/freexl/index>`_

