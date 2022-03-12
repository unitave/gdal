.. _raster.dods:

================================================================================
DODS -- OPeNDAP 그리드 클라이언트
================================================================================

.. shortname:: DODS

.. build_dependencies:: libdap

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_DODS

GDAL은 OPeNDAP(DODS) 프로토콜을 통해 2차원 그리드 및 배열을 읽을 수 있도록 선택할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 명명
--------------

전체 데이터셋 이름 사양은 OPeNDAP 데이터셋 URL, 원하는 배열 또는 그리드 변수를 가리키는 전체 경로, 그리고 접근할 배열 색인의 표시자(indicator)로 구성되어 있습니다.

예를 들어 URL http://maps.gdal.org/daac-bin/nph-hdf/3B42.HDF.dds 가 다음과 같은 DDS 정의를 반환하는 경우:

::

   Dataset {
     Structure {
       Structure {
         Float64 precipitate[scan = 5][longitude = 360][latitude = 80];
         Float64 relError[scan = 5][longitude = 360][latitude = 80];
       } PlanetaryGrid;
     } DATA_GRANULE;
   } 3B42.HDF;

다음 GDAL 데이터셋 이름을 이용해서 침전물(precipitate) 격자에 접근할 수 있습니다:

http://maps.gdal.org/daac-bin/nph-hdf/3B42.HDF?DATA_GRANULE.PlanetaryGrid.precipitate[0][x][y]

접근할 그리드 또는 배열을 가리키는 전체 경로를 지정해야 합니다. (상위(outer) 데이터셋 이름은 넣지 않습니다.) GDAL은 배열의 어떤 색인을 x(경도 또는 편동)로 그리고 y(위도 또는 편북)로 취급할지 알아야 할 필요가 있습니다. 다른 모든 차원은 단일값으로 제한해야 합니다.

2차원 배열 및 그리드만 데이터셋의 직계 자손(immediate children)으로 가지고 있는 데이터 서버의 경우, 그리드 또는 배열 변수의 이름을 지정할 필요가 없을 수도 있습니다.

데이터셋 수준에서 2차원 배열 또는 그리드가 여러 개 있는 경우, 각각 자동적으로 개별 밴드로 취급될 수도 있습니다.

특화된 AIS/DAS 메타데이터
----------------------------

데이터셋을 설명하는 다양한 정보가 DAS를 통해 전송될 것입니다. 일부 (GDAL 기반 같은!) 드라이버는 이미 다음 DAS 정보를 반환하지만, AIX 메커니즘을 이용해서 로컬에서 DAS 정보를 제공하는 경우도 있을 수 있습니다. AIX 메커니즘의 작동 방식을 자세히 알고 싶다면 DODS 문서를 읽어보십시오.

::

   Attributes {

       GLOBAL {
           Float64 Northernmost_Northing 71.1722;
       Float64 Southernmost_Northing  4.8278;
       Float64 Easternmost_Easting  -27.8897;
       Float64 Westernmost_Easting -112.11;
           Float64 GeoTransform "71.1722 0.001 0.0 -112.11 0.0 -0.001";
       String spatial_ref "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433]]";
           Metadata {
             String TIFFTAG_XRESOLUTION "400";
             String TIFFTAG_YRESOLUTION "400";
             String TIFFTAG_RESOLUTIONUNIT "2 (pixels/inch)";
           }
       }

       band_1 {
           String Description "...";
           String
       }
   }

데이터셋
~~~~~~~

DAS에는 데이터셋 속성 전체를 담고 있는 GLOBAL이라는 객체가 있을 것입니다.

이 객체는 다음 하위 항목들을 가지고 있을 것입니다:

-  **Northernmost_Northing**: 이미지 북쪽 경계의 위도 또는 편북
-  **Southernmost_Northing**: 이미지 남쪽 경계의 위도 또는 편북
-  **Easternmost_Easting**: 이미지 동쪽 경계의 경도 또는 편동
-  **Westernmost_Easting**: 이미지 서쪽 경계의 경도 또는 편동
-  **GeoTransform**: 픽셀/라인 공간 및 적용할 수 있는 경우 지리참조 공간 사이에서 아핀 변환(affine transformation)을 정의하는 파라미터 6개입니다. 공백으로 구분된 값들을 가진 단일 문자열로 저장됩니다. 기울인 또는 전단(shear) 이미지에 이 항목을 사용할 수 있다는 사실을 기억하십시오. (선택 옵션)
-  **SpatialRef**: 좌표계의 OpenGIS WKT 서술입니다. 지정하지 않는 경우 좌표계가 WGS84라고 가정할 것입니다. (선택 옵션)
-  **Metadata**:  사용할 수 있는 각 메타데이터 항목에 대한 문자열 속성들의 목록을 가진 컨테이너입니다. 메타데이터 항목 키워드 이름을 속성명으로 사용할 것입니다. 메타데이터 값은 항상 문자열 유형입니다. (선택 옵션)
-  *address GCPs*

그리드 크기와 지리변형을 기반으로 경계의 편북 및 편동 값들을 계산할 수 있다는 사실을 기억하십시오. 이 값들은 사용자가 지리변형보다 쉽게 해석할 수 있기 때문에 추가적인 문서로 우선 포함되었습니다. 편북 및 편동 가운데 한 쪽만 제공된 경우 내부에서 지리변형을 계산하는 데 사용될 것입니다. 그러나 두 쪽 다 제공된 경우 지리변형을 우선할 것입니다.

밴드
~~~~

DAS에는 각 밴드마다 밴드의 이름을 딴 객체가 해당 밴드의 속성을 담고 있을 것입니다.

이 객체는 다음 하위 항목들을 가지고 있을 것입니다:

-  **Metadata**: 사용할 수 있는 각 메타데이터 항목에 대한 문자열 속성들의 목록을 가진 컨테이너입니다. 메타데이터 항목 키워드 이름을 속성명으로 사용할 것입니다. 메타데이터 값은 항상 문자열 유형입니다. (선택 옵션)
-  **PhotometricInterpretation**: "Undefined", "GrayIndex", "PaletteIndex", "Red", "Green", "Blue", "Alpha", "Hue", "Saturation", "Lightness", "Cyan", "Magenta", "Yellow" 또는 "Black" 가운데 하나를 문자열 값으로 가지고 있을 것입니다. (선택 옵션)
-  **units**: 단위 이름입니다. (표고 데이터의 경우 "ft" 또는 "m" 가운데 하나입니다.) (선택 옵션)
-  **add_offset**: "실수" 픽셀값을 계산하기 위해 (scale_factor 후에) 픽셀값에 적용할 오프셋입니다. 기본값은 0.0입니다. (선택 옵션)
-  **scale_factor**: "실수" 픽셀값을 계산하기 위해 (add_offset 전에) 픽셀값에 적용할 척도입니다. 기본값은 1.0입니다. (선택 옵션)
-  **Description**: 밴드에 관한 설명 텍스트입니다. (선택 옵션)
-  **missing_value**: The nodata value for the raster. (선택 옵션)
-  **Colormap**: 색상표의 각 색상을 위한 하위 컨테이너를 가지고 있는 컨테이너입니다. 다음과 같이 생겼습니다. 알파 구성요소는 선택 옵션이며, 지정하지 않는 경우 255(불투명)로 가정합니다.

   ::

          Colormap {
            Color_0 {
              Byte red 0;
              Byte green 0;
              Byte blue 0;
              Byte alpha 255;
            }
            Color_1 {
              Byte red 255;
              Byte green 255;
              Byte blue 255;
              Byte alpha 255;
            }
            ...
          }

참고
--------

-  `OPeNDAP 웹사이트 <http://www.opendap.org/>`_
