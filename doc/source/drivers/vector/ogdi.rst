.. _vector.ogdi:

OGDI 벡터
============

.. shortname:: OGDI

.. build_dependencies:: OGDI 라이브러리

OGR에서 OGDI 벡터 지원은 선택적이며, 일반적으로 OGDI가 빌드 시스템 상에 설치된 경우에만 환경설정됩니다. OGDI 벡터를 사용할 수 있는 경우 다음과 같은 동종(family) 유형에 읽기 접근을 지원합니다:

-  포인트(point)
-  라인(line)
-  면(area)
-  텍스트(text): 현재 "text" 속성에 텍스트를 가지고 있는 포인트로 반환됩니다.

OGDI는 (다른 포맷들 가운데) DCW 및 VMAP 같은 VPF 상품을 읽어올 수 있습니다.

OGDI GLTP URL을 직접 여는 경우, 드라이버/서버에 OGDI 3.1 케이퍼빌리티를 쿼리해서 레이어 목록을 가져옵니다. 데이터 저장소에 있는 각 레이어에서 사용할 수 있는 각 ODGI 동종 유형별로 OGR 레이어 하나를 생성합니다. VRF 같은 드라이버의 경우 수많은 레이어를 산출할 수 있습니다. 각 레이어는 OGDI 이름에 밑줄 문자('_')와 동종 유형 이름을 붙인 이름을 기반으로 하는 OGR 이름을 가집니다. 예를 들면 VRF 드라이버에서 나오는 레이어 이름이 ``watrcrsl@hydro(*)_line`` 일 수도 있습니다.

:decl_configoption:`OGR_OGDI_LAUNDER_LAYER_NAMES` 환경설정 옵션(또는 환경 변수)을 YES로 설정하면 레이어 이름을 단순화시킵니다. 예를 들면 ``watrcrsl@hydro(*)_line`` 을 ``watrcrsl_hydro`` 로 단순화시킵니다.

데이터 저장소에 있는 모든 레이어에 접근하는 대신, 정규 GLTP URL에 레이어 이름 및 동종 유형을 (쌍점으로 구분해서) 추가해서 이루어진 사용자 지정 파일명을 이용하면 특정 레이어를 열 수도 있습니다. OGDI 3.1 이전 버전의 드라이버가 생성한 레이어에 접근하려면 반드시 이 메커니즘을 이용해야만 합니다. OGDI 3.1 이전 버전들에서는 OGDI에서 사용할 수 있는 레이어를 찾을 수 있는 정식 방법이 없었기 때문입니다.

::

      gltp:[//<hostname>]/<driver_name>/<dataset_name>:<layer_name>:<family>

이때 <layer_name>이 OGDI 레이어 이름이고, <family>는 "point", "line", "area", 또는 "text" 가운데 하나입니다.

OGDI 좌표계 정보는 대부분의 좌표계를 지원합니다. 좌표계를 변환할 수 없는 경우 레이어를 열 때 경고를 출력할 것입니다.

OGDI 드라이버는 업데이트 또는 생성을 지원하지 않습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

오류 처리
--------------

GDAL 2.2버전 및 OGDI 3.2.0beta2 초과 버전부터, OGDI_STOP_ON_ERROR 환경 변수를 NO로 설정하면 ODGI가 (VPF 드라이버에서) 일부 오류를 정상적으로 복구할 수 있습니다. 그래도 GDAL이 이런 오류를 잡아내서 정식 GDAL 오류로 발생시킬 것입니다.

주의: 이 습성은 아직 개발중이기 때문에 조심해야 합니다. 복구할 수 있는 오류를 모두 복구할 수 없으며, 몇몇 오류는 어떤 리포트도 없이 복구될 수도 있습니다.

예시
--------

-  예시 'ogrinfo' 사용례:

::

      ogrinfo gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'watrcrsl@hydro(*)_line'

   'gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia' 데이터셋 이름에서 'gltp:/vrf' 부분은 파일 시스템 안에 실제로 있지는 않지만 추가해줘야 합니다. '/usr4/mpp1/v0eur/' 부분이 VPF 데이터입니다. 'eurnasia' 디렉터리는 .dht 및 .lat 파일과 같은 수준에 있어야 합니다. 'hydro' 참조는 watrcrsl.\* 가 발견된 'eurnasia/' 디렉터리의 하위 디렉터리입니다.

-  'ogr2ogr' 유틸리티로 VMAP0을 shapefile로 변환하는 사용례:

::

      ogr2ogr watrcrsl.shp gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'watrcrsl@hydro(*)_line'
      ogr2ogr polbnda.shp  gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'polbnda@bnd(*)_area'

-  VMAP 데이터셋을 대상으로 하는 OGR SQL 쿼리. 레이어 이름을 큰따옴표로 묶는다는 사실을 기억하십시오:

::

      ogrinfo -ro gltp:/vrf/usr4/mpp1/v0noa/vmaplv0/noamer \
              -sql 'select * from "polbndl@bnd(*)_line" where use=26'

See Also
--------

-  `OGDI.SourceForge.Net <http://ogdi.sourceforge.net/>`_
-  `VMap0 커버리지 <http://www.terragear.org/docs/vmap0/coverage.html>`_

