.. _ogrmerge:

================================================================================
ogrmerge.py
================================================================================

.. only:: html

    벡터 데이터셋 여러 개를 단일 데이터셋으로 병합합니다.

.. Index:: ogrmerge

개요
--------

.. code-block::

    ogrmerge.py -o out_dsname src_dsname [src_dsname]*
                [-f format] [-single] [-nln layer_name_template]
                [-update | -overwrite_ds] [-append | -overwrite_layer]
                [-src_geom_type geom_type_name[,geom_type_name]*]
                [-dsco NAME=VALUE]* [-lco NAME=VALUE]*
                [-s_srs srs_def] [-t_srs srs_def | -a_srs srs_def]
                [-progress] [-skipfailures] [--help-general]

:ref:`-single <ogrmerge_single_option>` 옵션에 특화된 옵션들:

.. code-block::

                [-field_strategy FirstLayer|Union|Intersection]
                [-src_layer_field_name name]
                [-src_layer_field_content layer_name_template]

설명
-----------

.. versionadded:: 2.2

:program:`ogrmerge.py` 스크립트는 각각 벡터 레이어 여러 개를 가지고 있는 벡터 데이터셋 여러 개를 입력받아 하나의 대상 데이터셋으로 복사합니다.

핵심적인 모드 2개가 있습니다:

*  기본 모드: 대상 데이터셋으로 각 입력 벡터 레이어를 개별 레이어로 복사합니다.

*  -single 스위치로 활성화되는 다른 모드: 단일 대상 레이어에 모든 입력 벡터 레이어의 내용들을 추가합니다. 입력 벡터 레이어들의 스키마가 거의 동일하다고 가정합니다.

이 스크립트는 내부적으로 :ref:`vector.vrt` 파일을 생성하는데, 산출물 포맷이 VRT가 아닌 경우 :program:`ogr2ogr` 또는 :py:func:`gdal.VectorTranslate` 로 최종 변환합니다. 따라서 고급 사용자의 경우 VRT로 산출하면 직접 편집할 수도 있고 :program:`ogr2ogr` 를 사용할 수도 있습니다.

.. program:: ogrmerge.py

.. option:: -o <out_dsname

    산출 데이터셋의 이름을 설정합니다. 필수 옵션입니다.

.. option:: <src_dsname>

    하나 이상의 입력 벡터 데이터셋을 설정합니다. 필수 옵션입니다.

.. option:: -f <format>

    산출물 포맷을 선택합니다. GDAL 2.3버전부터, 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지는 ESRI Shapefile을 생성했습니다.) 단축 포맷명을 사용하십시오.

.. _ogrmerge_single_option:
.. option:: -single

    이 옵션을 지정하면, 모든 입력 벡터 레이어를 단일 레이어로 병합할 것입니다.

.. option:: -nln <layer_name_template>

    단일 모드에서 산출 벡터 레이어의 이름(기본값은 "merged"), 또는 기본 모드에서 산출 벡터 레이어들을 명명하기 위한 (기본값은 ``{AUTO_NAME}``) 템플릿입니다. 이 템플릿은 처리되고 있는 입력 레이어로부터 계산한 값으로 대체할 수 있는 다음 변수들을 가진 문자열일 수 있습니다:

    -  ``{AUTO_NAME}``: 기반(base) 이름과 레이어 이름이 서로 다른 경우 ``{DS_BASENAME}_{LAYER_NAME}`` 과 동일하고, 두 이름이 동일한 (shapefile의) 경우 ``{LAYER_NAME}`` 과 동일합니다.
    -  ``{DS_NAME}``: 소스 데이터셋의 이름
    -  ``{DS_BASENAME}``: 소스 데이터셋의 기반 이름
    -  ``{DS_INDEX}``: 소스 데이터셋의 색인
    -  ``{LAYER_NAME}``: 소스 레이어의 이름
    -  ``{LAYER_INDEX}``: 소스 레이어의 색인

.. option:: -update

    기존 데이터셋을 업데이트 모드로 엽니다.

.. option:: -overwrite_ds

    (파일 기반 데이터셋인 경우) 대상 데이터셋이 이미 존재하면 덮어씁니다.

.. option:: -append

    기존 데이터셋을 업데이트 모드로 열고, 산출 레이어가 이미 존재하는 경우 입력 레이어의 내용을 추가합니다.

.. option:: -overwrite_layer

    기존 데이터셋을 업데이트 모드로 열고, 산출 레이어가 이미 존재하는 경우 산출 레이어의 내용을 입력 레이어의 내용으로 대체합니다.

.. option:: -src_geom_type <geom_type_name[,geom_type_name]\*]>

    도형 유형이 지정한 유형(들)과 일치하는 입력 레이어들만 병합합니다. <geom_type_name>에는 GEOMETRY, POINT, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, GEOMETRYCOLLECTION, CIRCULARSTRING, CURVEPOLYGON, MULTICURVE, MULTISURFACE, CURVE, SURFACE, TRIANGLE, POLYHEDRALSURFACE 및 TIN을 지정할 수 있습니다.

.. option:: -dsco <NAME=VALUE>

    데이터셋 생성 옵션 (특정 포맷 지원)

.. option:: -lco <NAME=VALUE>

    레이어 생성 옵션 (특정 포맷 지원)

.. option:: -a_srs <srs_def>

    산출물 공간 좌표계를 할당합니다.

.. option:: -t_srs <srs_def>

    산출물을 지정한 공간좌표계로 재투영/변환합니다.

.. option:: -s_srs <srs_def>

    소스 공간 좌표계를 지정한 좌표계로 무시합니다.

.. option:: -progress

    터미널에 진행 상황을 출력합니다. 입력 레이어들이 "fast feature count" 능력을 갖추고 있는 경우에만 작동합니다.

.. option:: -skipfailures

    실패한 객체를 건너뛰고, 실패한 후에도 계속합니다.

.. option:: -field_strategy FirstLayer|Union|Intersection

    :option:`-single` 옵션과 함께 사용해야 합니다. 입력 레이어의 스키마로부터 대상 레이어의 스키마를 작성하는 방법을 결정합니다. 첫 번째로 검색된 레이어의 필드를 사용하려면 FirstLayer를, 모든 소스 레이어의 모든 필드의 확대 집합(superset)을 사용하려면 Union을, 또는 모든 소스 레이어의 모든 공통 필드의 하위 집합(subset)을 사용하려면 Intersection을 설정하면 됩니다. 기본값은 Union입니다.

.. option:: -src_layer_field_name <name>

    :option:`-single` 옵션과 함께 사용해야 합니다. 이 옵션을 지정하는 경우, 대상 레이어의 스키마가 :option:`-src_layer_field_content` 옵션이 그 내용을 결정하는 새 'name' 필드를 갖도록 확장할 것입니다.

.. option:: -src_layer_field_content <layer_name_template>

    :option:`-single` 옵션과 함께 사용해야 합니다. 이 옵션을 지정하는 경우, 대상 레이어의 스키마가 ``layer_name_template`` 이 그 내용을 결정하는 (:option:`-src_layer_field_name` 또는 'source_ds_lyr' 가 그 이름을 지정하는) 새 필드를 갖도록 확장할 것입니다. ``layer_name_template`` 의 문법은 :option:`-nln` 의 문법과 동일합니다.

예시
--------

각 입력 shapefile에 대한 레이어 하나를 가진 VRT를 하나씩 생성:

.. code-block::

    ogrmerge.py -f VRT -o merged.vrt *.shp

동일한 작업이지만, GeoPackage 파일을 생성:

.. code-block::

    ogrmerge.py -f GPKG -o merged.gpkg *.shp

france.shp와 germany.shp의 내용을 merged.shp로 연결(concatenate)하고, 각 객체에 소스 파일에 따라 'france' 또는 'germany' 값을 가지는 'country' 필드를 추가:

.. code-block::

    ogrmerge.py -single -o merged.shp france.shp germany.shp -src_layer_field_name country
