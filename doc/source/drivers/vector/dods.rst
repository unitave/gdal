.. _vector.dods:

DODS/OPeNDAP
============

.. shortname:: DODS

.. build_dependencies:: libdap

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_OGR_DODS

이 드라이버는 OPeNDAP(DODS) 서버로부터 객체 데이터를 읽어오기 위한 읽기 전용 지원을 구현합니다. GDAL/OGR를 OPeNDAP 지원 라이브러리와 함께 빌드한 경우 OGR에 포함시킬 수도 있습니다.

데이터베이스를 열 때, 데이터베이스 이름을 "DODS:url" 형식으로 지정해줘야 합니다. 이 URL은 이 문서에도 있는 제약 표현식을 포함할 수도 있습니다. DODS URL이 물음표 또는 앤드('&') 문자를 포함하는 경우 이들이 명령줄 셸에서 특수한 의미를 가지는 경우가 많기 때문에, 명령줄에 DODS URL을 입력할 때 큰따옴표 또는 다른 방법으로 URL을 보호해야 할 수도 있습니다.

::

   DODS:http://dods.gso.uri.edu/dods-3.4/nph-dods/broad1999?&press=148

기본적으로 최상위 수준의 Sequence, Grid 및 Array 객체를 대응하는 레이어로 변환할 것입니다. 기본적으로 Sequence 객체를 -- 위도 및 경도 변수가 존재하는 경우 -- 위도 및 경도를 가진 포인트 도형들로 이루어진 포인트 레이어로 취급합니다. Sequence, Grid 및 Array 객체를 좀 더 정교하게 피처로 변환하려면, 원격 서버 또는 로컬 가운데 하나로부터 OGR에 AIS 메커니즘을 통해 추가 정보를 DAS로서 (데이터셋 보조 정보로서) 넘겨줘야 합니다.

OGR 레이어에 대한 DAS 정의는 다음과 비슷하게 보일 수도 있습니다:

::

   Attributes {
       ogr_layer_info {
       string layer_name WaterQuality;
       string spatial_ref WGS84;
       string target_container Water_Quality;
           layer_extents {
           Float64 x_min -180;
           Float64 y_min -90;
           Float64 x_max 180;
           Float64 y_max 90;
           }
           x_field {
               string name YR;
           string scope dds;
           }
           y_field {
               string name JD;
           string scope dds;
           }
       }
   }

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

주의할 점
--------

-  DODS로부터 속성 필드 용 필드 길이를 수집할 수 없습니다.

-  DODS 캐시 작업을 활성화하면 반복 요청 처리 속도가 훨씬 빨라집니다. 사용자의 ~/.dodsrc 에 있는 USE_CACHE 옵션을 1로 설정해보십시오.

참고
--------

-  `OPeNDAP <http://www.opendap.org/>`_

