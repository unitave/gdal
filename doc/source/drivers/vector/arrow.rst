.. _vector.arrow:

(지오)애로우 IPC 파일 포맷 / 스트림
===================================

.. versionadded:: 3.5

.. shortname:: Arrow

.. build_dependencies:: 아파치 애로우 C++ 라이브러리

애로우(Arrow) IPC 파일 포맷(Feather 포맷)은 애로우 IPC 포맷을 내부적으로 활용하는 (파이썬 또는 R 같은 언어로 작성된) 애로우 테이블 또는 데이터 프레임을 저장하기 위한 포터블 파일 포맷입니다.

애로우 드라이버는 이 포맷의 두 가지 변이형을 지원합니다:

-  Feather 포맷으로도 알려진 파일 또는 임의 접근(Random Access) 포맷:
   고정 개수의 레코드 배치(batch)를 직렬화하기 위한 포맷입니다.
   이런 파일을 읽으려면 임의 접근이 필요하지만, 스트리밍 전용 파일을 사용해서 이런 파일을 생성할 수 있습니다. 이런 파일에 권장되는 확장자는 ``.arrow`` 입니다.

-  스트리밍 IPC 포맷:
   레코드 배치(batch)의 임의 길이의 순열(sequence)을 전송하기 위한 포맷입니다.
   이 포맷은 일반적으로 처음부터 끝까지 처리되어야만 하기 때문에, 임의 접근이 필요하지 않습니다. 이 포맷은 일반적으로 실제 파일로 생성되지 않습니다. 실제 파일로 생성되는 경우, 권장되는 확장자는 (뒤에 s가 붙는) ``.arrows`` 입니다. 그러나 이 드라이버는 /vsistdin/ 및 /vsistdout/ 스트리밍 파일은 물론 정규 파일도 지원할 수 있습니다.
   열기 작업 시, 특히 확장자가 ``.arrows`` 가 아니고 메타데이터 부분이 대용량인 경우 드라이버가 파일 내용이 명확하게 Arrow IPC 스트림인지 탐지하는 데 어려움이 있을 수도 있습니다.
   파일명 앞에 ``ARROW_IPC_STREAM:`` 접두어를 붙이면 (예: "ARROW_IPC_STREAM:/vsistdin/") 이 드라이버가 파일을 무조건 스트리밍 IPC 포맷으로 열게 될 것입니다.

이 드라이버는 지오애로우(GeoArrow) 사양을 사용하는 도형 열도 지원합니다.

.. note::

   지오애로우 사양이 아직 확정되지 않았기 때문에 이 드라이버를 실험적인 것으로 간주해야 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

이 드라이버는 데이터셋 하나에 단일 레이어 하나만 생성할 수 있습니다.

레이어 생성 옵션
----------------------

-  **COMPRESSION=string**:
   압축 메소드를 지정합니다. ``NONE``, ``ZSTD`` 또는 ``LZ4`` 가운데 하나로 지정할 수 있습니다. 애로우 라이브러리가 어떻게 컴파일되었는지에 따라 지정할 수 있는 값이 달라집니다.
   LZ4를 사용할 수 있는 경우 기본값은 LZ4이고, 사용할 수 없다면 기본값은 NONE입니다.

-  **FORMAT=FILE/STREAM**:
   파일 포맷의 변이형을 지정합니다. 두 변이형의 차이점에 대해서는 소개 문단을 읽어보십시오. 파일명이 "/vsistdout/"이거나 확장자가 ".arrows"가 아닌 이상 기본값은 FILE입니다. 파일명이 "/vsistdout/"이거나 확장자가 ".arrows"인 경우 STREAM을 기본값으로 사용합니다.

-  **GEOMETRY_ENCODING=GEOARROW/WKB/WKT**:
   도형 인코딩을 지정합니다. 기본값은 GEOARROW입니다.

-  **BATCH_SIZE=integer**:
   레코드 배치 당 행의 최대 개수를 지정합니다. 기본값은 65536입니다.

-  **GEOMETRY_NAME=string**:
   도형 열의 이름을 지정합니다. 기본값은 ``geometry`` 입니다.

-  **FID=string**:
   생성할 FID(Feature ID) 열의 이름을 지정합니다. 아무것도 지정하지 않으면 FID 열을 생성하지 않습니다.
   소스 레이어가 명명된 FID 열을 가지고 있는데 애로우 드라이버를 대상 드라이버로 ogr2ogr 유틸리티를 사용하는 경우, (비어 있는 이름을 설정하기 위해 ``-lco FID=`` ogr2ogr 옵션을 사용하지 않는 이상) 애로우 드라이버의 FID 레이어 생성 옵션을 이 FID 열의 이름으로 자동 설정할 것이라는 사실을 기억하십시오.

링크
-----

-  `Feather 파일 포맷 <https://arrow.apache.org/docs/python/feather.html>`_

-  `지오애로우 사양 <https://github.com/geopandas/geo-arrow-spec>`_

-  관련 드라이버: :ref:`파켓 <vector.parquet>` 드라이버

