.. _gdalmdiminfo:

================================================================================
gdalmdiminfo
================================================================================

.. only:: html

    .. versionadded:: 3.1

    다중차원 데이터셋의 구조 및 내용을 리포트합니다.

.. Index:: gdalmdiminfo

개요
--------

.. code-block::

    gdalmdiminfo [--help-general] [-oo NAME=VALUE]* [-arrayoption NAME=VALUE]*
                 [-detailed] [-nopretty] [-array {array_name}] [-limit {number}]
                 [-stats] <datasetname>

내용
-----------

:program:`gdalmdiminfo` 프로그램은 GDAL이 지원하는 다중차원 래스터 데이터셋에 대한 다양한 정보의 목록을 JSON으로 산출합니다. 이 목록은 `JSON 스키마 <https://github.com/OSGeo/gdal/blob/master/data/gdalmdiminfo_output.schema.json>`_ 를 따릅니다.

다음 명령줄 파라미터들은 어떤 순서로도 사용할 수 있습니다:

.. program:: gdalmdiminfo

.. option:: -detailed

    가장 상세한 산출물을 반환합니다. 속성 데이터 유형 및 배열 값들을 리포트합니다.

.. option:: -nopretty

    어떤 들여쓰기도 없이 한 줄짜리 산출물을 반환합니다.

.. option:: -array {array_name}

    산출물을 지정한 배열로 제한하기 위해 쓰이는 배열의 이름입니다.

.. option:: -limit {number}

    배열 값들의 출력을 제한하기 위해 쓰이는 각 차원에 있는 값들의 개수입니다. 기본값은 제한하지 않는 것입니다. -detailed 옵션과 함께 쓰일 때만 효과가 있습니다.

.. option:: -oo <NAME=VALUE>

    데이터셋 열기 옵션(특정 포맷 지원). 이 옵션을 여러 번 사용할 수도 있습니다.

.. option:: -arrayoption <NAME=VALUE>

    리포트된 배열을 필터링하기 위해 :cpp:func:`GDALGroup::GetMDArrayNames` 에 전송(pass)하는 옵션입니다. 이런 옵션은 특화된 서식을 사용합니다. 드라이버 문서를 자세히 읽어보십시오. 이 옵션을 여러 번 사용할 수도 있습니다.

.. option:: -stats

    이미지 통계를 읽어와서 출력합니다. 이미지에 어떤 통계도 저장돼 있지 않은 경우 강제로 계산합니다.

    .. versionadded:: 3.2

C API
-----

C에서 :cpp:func:`GDALMultiDimInfo` 로도 이 유틸리티를 호출할 수 있습니다.

예시
--------

- 일반 structure1을 출력합니다:

.. code-block::

    $ gdalmdiminfo netcdf-4d.nc 


.. code-block:: json

  {
    "type": "group",
    "name": "/",
    "attributes": {
      "Conventions": "CF-1.5"
    },
    "dimensions": [
      {
        "name": "levelist",
        "full_name": "/levelist",
        "size": 2,
        "type": "VERTICAL",
        "indexing_variable": "/levelist"
      },
      {
        "name": "longitude",
        "full_name": "/longitude",
        "size": 10,
        "type": "HORIZONTAL_X",
        "direction": "EAST",
        "indexing_variable": "/longitude"
      },
      {
        "name": "latitude",
        "full_name": "/latitude",
        "size": 10,
        "type": "HORIZONTAL_Y",
        "direction": "NORTH",
        "indexing_variable": "/latitude"
      },
      {
        "name": "time",
        "full_name": "/time",
          "size": 4,
        "type": "TEMPORAL",
        "indexing_variable": "/time"
        }
    ],
    "arrays": {
      "levelist": {
        "datatype": "Int32",
        "dimensions": [
            "/levelist"
          ],
        "attributes": {
          "long_name": "pressure_level"
        },
        "unit": "millibars"
      },
      "longitude": {
        "datatype": "Float32",
        "dimensions": [
          "/longitude"
        ],
        "attributes": {
          "standard_name": "longitude",
          "long_name": "longitude",
          "axis": "X"
        },
        "unit": "degrees_east"
      },
      "latitude": {
        "datatype": "Float32",
        "dimensions": [
          "/latitude"
        ],
        "attributes": {
          "standard_name": "latitude",
          "long_name": "latitude",
          "axis": "Y"
        },
        "unit": "degrees_north"
      },
      "time": {
        "datatype": "Float64",
        "dimensions": [
          "/time"
        ],
        "attributes": {
          "standard_name": "time",
          "calendar": "standard"
        },
        "unit": "hours since 1900-01-01 00:00:00"
      },
      "t": {
        "datatype": "Int32",
        "dimensions": [
          "/time",
          "/levelist",
          "/latitude",
          "/longitude"
        ],
        "nodata_value": -32767
      }
    },
    "structural_info": {
      "NC_FORMAT": "CLASSIC"
    }
  }

- 입력 배열에 대한 상세 정보를 출력합니다:

.. code-block::

    $ gdalmdiminfo netcdf-4d.nc -array t -detailed -limit 3
