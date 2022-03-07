.. _ogr2ogr:

================================================================================
ogr2ogr
================================================================================

.. only:: html

    단순 객체 데이터를 서로 다른 파일 포맷으로 변환합니다.

.. Index:: ogr2ogr

개요
--------

.. code-block::

    ogr2ogr [--help-general] [-skipfailures] [-append] [-update]
            [-select field_list] [-where restricted_where|@filename]
            [-progress] [-sql <sql statement>|@filename] [-dialect dialect]
            [-preserve_fid] [-fid FID] [-limit nb_features]
            [-spat xmin ymin xmax ymax] [-spat_srs srs_def] [-geomfield field]
            [-a_srs srs_def] [-t_srs srs_def] [-s_srs srs_def] [-ct string]
            [-f format_name] [-overwrite] [[-dsco NAME=VALUE] ...]
            dst_datasource_name src_datasource_name
            [-lco NAME=VALUE] [-nln name]
            [-nlt type|PROMOTE_TO_MULTI|CONVERT_TO_LINEAR|CONVERT_TO_CURVE]
            [-dim XY|XYZ|XYM|XYZM|2|3|layer_dim] [layer [layer ...]]

            # Advanced options
            [-gt n]
            [[-oo NAME=VALUE] ...] [[-doo NAME=VALUE] ...]
            [-clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent]
            [-clipsrcsql sql_statement] [-clipsrclayer layer]
            [-clipsrcwhere expression]
            [-clipdst [xmin ymin xmax ymax]|WKT|datasource]
            [-clipdstsql sql_statement] [-clipdstlayer layer]
            [-clipdstwhere expression]
            [-wrapdateline] [-datelineoffset val]
            [[-simplify tolerance] | [-segmentize max_dist]]
            [-makevalid]
            [-addfields] [-unsetFid] [-emptyStrAsNull]
            [-relaxedFieldNameMatch] [-forceNullable] [-unsetDefault]
            [-fieldTypeToString All|(type1[,type2]*)] [-unsetFieldWidth]
            [-mapFieldType type1|All=type2[,type3=type4]*]
            [-fieldmap identity | index1[,index2]*]
            [-splitlistfields] [-maxsubfields val]
            [-resolveDomains]
            [-explodecollections] [-zfield field_name]
            [-gcp ungeoref_x ungeoref_y georef_x georef_y [elevation]]* [-order n | -tps]
            [[-s_coord_epoch epoch] | [-t_coord_epoch epoch] | [-a_coord_epoch epoch]]
            [-nomd] [-mo "META-TAG=VALUE"]* [-noNativeData]

설명
-----------

:program:`ogr2ogr` 프로그램을 사용하면 단순 객체 데이터를 서로 다른 파일 포맷으로 변환할 수 있습니다. 변환 과정에서 공간 선택 또는 속성 선택, 속성 집합 축소, 산출물 좌표계 설정, 또는 변환 도중 객체 재투영까지, 다양한 작업도 수행할 수 있습니다.

.. program:: ogr2ogr

.. option:: -f <format_name>

    예를 들어 ``ESRI Shapefile``, ``MapInfo File``, ``PostgreSQL`` 같은 산출물 파일 포맷의 이름입니다. GDAL 2.3버전부터, 이 옵션을 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지의 기본값은 ESRI Shapefile이었습니다.)

.. option:: -append

    새 레이어를 생성하는 대신 기존 레이어에 추가합니다.

.. option:: -overwrite

    산출 레이어를 삭제하고 비어 있는 레이어를 재생성합니다.

.. option:: -update

    산출 데이터소스를 새로 생성하기보다 기존 산출 데이터소스를 업데이트 모드로 엽니다.

.. option:: -select <field_list>

    새 레이어에 복사할, 쉼표로 구분된 입력 레이어의 필드 목록입니다. 입력 레이어에 동일한 필드 이름이 있더라도 이전에 목록에서 언급되었다면 해당 필드를 건너뛸 것입니다. (기본값은 ``all`` 입니다. 동일한 이름을 가진 그 다음(subsequent) 필드를 발견한 경우 동일한 이름의 모든 필드를 건너뜁니다.) 이 목록에 도형 필드도 지정할 수 있습니다.

    이 설정을 ``-append`` 와 함께 사용할 수 없다는 사실을 기억하십시오. 레이어에 추가하는 작업 도중 필드 선택 작업을 제어하고 싶다면, ``-fieldmap`` 또는 ``-sql`` 을 사용하십시오.

.. option:: -progress

    터미널에 진생 상황을 출력합니다. 입력 레이어가 "fast feature count" 능력을 가지고 있는 경우에만 동작합니다.

.. option:: -sql <sql_statement>

    실행할 SQL 선언문입니다. 산출물에 생성되는 테이블/레이어를 저장할 것입니다. GDAL 2.1버전부터, 지정한 파일명에 내용이 있다는 사실을 나타내기 위한 ``@filename`` 문법을 사용할 수 있습니다.

.. option:: -dialect <dialect>

    SQL 방언(dialect)입니다. 어떤 경우 ``OGRSQL`` 을 전송해서 RDBMS의 네이티브 SQL 대신 (최적화되지 않은) :ref:`ogr_sql_dialect` 을 사용하기 위해 쓰일 수도 있습니다. 모든 데이터소스에서 ``SQLITE`` 및 ``INDIRECT_SQLITE`` 방언 값으로 :ref:`sql_sqlite_dialect` 도 사용할 수 있습니다.

.. option:: -where restricted_where

    (SQL WHERE 같은) 속성 쿼리입니다. GDAL 2.1버전부터, 지정한 파일명에 내용이 있다는 사실을 나타내기 위한 ``@filename`` 문법을 사용할 수 있습니다.

.. option:: -skipfailures

    실패한 객체를 건너뛰고, 실패가 발생한 후에도 계속합니다.

.. option:: -spat <xmin> <ymin> <xmax> <ymax>

    소스 레이어(들)의 (또는 ``-spat_srs`` 로 지정한) 공간 좌표계 단위로 범위를 공간 쿼리합니다. 이 범위와 교차하는 도형을 가진 객체만 선택할 것입니다. ``-clipsrc`` 옵션을 지정하지 않는 경우 도형을 자르지 않을 것입니다.

.. option:: -spat_srs <srs_def>

    공간 필터 공간 좌표계를 무시합니다.

.. option:: -geomfield <field>

    공간 필터가 작동하는 도형 필드의 이름입니다.

.. option:: -dsco NAME=VALUE

    데이터셋 생성 옵션 (특정 포맷 지원)

.. option:: -lco NAME=VALUE

    레이어 생성 옵션 (특정 포맷 지원)

.. option:: -nln <name>

    새 레이어에 대체 이름을 할당합니다.

.. option:: -nlt <type>

    생성된 레이어에 도형 유형을 정의합니다. ``NONE``, ``GEOMETRY``, ``POINT``, ``LINESTRING``, ``POLYGON``, ``GEOMETRYCOLLECTION``, ``MULTIPOINT``, ``MULTIPOLYGON``, ``MULTILINESTRING``, ``CIRCULARSTRING``, ``COMPOUNDCURVE``, ``CURVEPOLYGON``, ``MULTICURVE``, 그리고 ``MULTISURFACE`` 라는 비선형 도형 유형을 지정할 수 있습니다. 유형 이름에 표고 또는 측정값(measure)을 가진 좌표를 지정하려면 ``Z`` 또는 ``M`` 을, 또는 표고와 측정값을 지정하려면 ``ZM`` 을 추가하십시오. 폴리곤 또는 다중 폴리곤을 멀티폴리곤으로 혼합하도록, 그리고 라인스트링 또는 멀티라인스트링을 멀티라인스트링으로 혼합하도록 레이어를 자동으로 승격(promote)시키려면 ``PROMOTE_TO_MULTI`` 를 사용하면 됩니다. shapefile을 PostGIS 및 도형 유형을 엄격히 검증하도록 구현된 기타 대상 드라이버로 변환할 때 유용할 수 있습니다. 비선형 도형 유형의 근사치를 계산해서 선형 도형으로 변환하려면 ``CONVERT_TO_LINEAR`` 를 쓰면 되고, 비선형 유형을 해당 유형을 일반화시킨 만곡(curve) 유형으로 (``POLYGON`` 을 ``CURVEPOLYGON`` 으로, ``MULTIPOLYGON`` 을 ``MULTISURFACE`` 로, ``LINESTRING`` 을 ``COMPOUNDCURVE`` 로, ``MULTILINESTRING`` 을 ``MULTICURVE`` 로) 승격시키려면 ``CONVERT_TO_CURVE`` 를 사용하면 됩니다. GDAL 2.1버전부터, 유형을 측정값대로 정의할 수 있습니다. ("2.5D"는 단일 "Z"를 위한 별명으로 남았습니다.) 도형 변환을 강제하는 경우, 가끔 무결하지 않은 도형을 산출할 수도 있습니다. 예를 들어 다중부분(multi-part) 멀티폴리곤을 ``-nlt POLYGON`` 으로 강제로 변환하면 단순 객체 규칙을 어기는 폴리곤을 산출하게 됩니다.

    GDAL 3.0.5부터, ``-nlt CONVERT_TO_LINEAR`` 와 ``-nlt PROMOTE_TO_MULTI`` 를 동시에 사용할 수 있습니다.

.. option:: -dim <val>

    좌표 차원을 강제로 <val>로 변환시킵니다. (<val>에는 ``XY``, ``XYZ``, ``XYM``, 그리고 ``XYZM`` 을 지정할 수 있습니다 - 예전 버전과의 호환성을 위해 ``XY`` 의 별명인 ``2`` 와 ``XYZ`` 의 별명인 ``3`` 도 사용할 수 있습니다.) 이 옵션을 설정하면 레이어 도형 유형과 객체 도형 둘 다 영향을 받습니다. 객체 도형을 레이어가 선언한 좌표 차원으로 승격시키려면 <val>을 ``layer_dim`` 으로 설정하면 됩니다. GDAL 2.1버전부터 M을 지원하기 시작했습니다.

.. option:: -a_srs <srs_def>

    산출물에 공간 좌표계를 할당하지만, 재투영하지는 않습니다. (재투영하려면 :option:`-t_srs` 옵션을 사용하십시오.)

    .. include:: options/srs_def.rst

.. option:: -a_coord_epoch <epoch>

    .. versionadded:: 3.4

    산출물 공간 좌표계와 링크되는 시대(epoch) 좌표를 할당합니다. 산출물 공간 좌표계가 동적 좌표계인 경우 유용합니다. :option:`-a_srs` 옵션을 설정한 경우에만 동작합니다.

.. option:: -t_srs <srs_def>

    산출물을 지정한 공간 좌표계로 재투영/변형하고, 산출물 공간 좌표계로 할당합니다.

    재투영이 일어나려면 소스 공간 좌표계를 사용할 수 있어야만 합니다. 기본적으로 소스 레이어에서 발견된 공간 좌표계를 사용할 수 있는 경우 해당 공간 좌표계를 소스 공간 좌표계로 사용할 것입니다. 또는 사용자가 :option:`-s_srs` 옵션으로 무시할 수도 있습니다.

    .. include:: options/srs_def.rst

.. option:: -t_coord_epoch <epoch>

    .. versionadded:: 3.4

    산출물 공간 좌표계와 링크되는 시대(epoch) 좌표를 할당합니다. 산출물 공간 좌표계가 동적 좌표계인 경우 유용합니다. :option:`-t_srs` 옵션을 설정한 경우에만 동작합니다. 또한 :option:`-a_coord_epoch` 옵션과 서로 함께 사용할 수 없습니다.

    현재 :option:`-s_coord_epoch` 와 :option:`-t_coord_epoch` 는 서로 함께 사용할 수 없습니다. 두 동적 좌표계 사이의 변환에 대한 지원이 부족하기 때문입니다.

.. option:: -s_srs <srs_def>

    소스 공간 좌표계를 무시합니다. 지정하지 않는 경우 입력 레이어에서 발견된 공간 좌표계를 사용할 것입니다. 이 옵션은 재투영하기 위한 :option:`-t_srs` 옵션과 함께 사용하는 경우에만 효과가 있습니다.

    .. include:: options/srs_def.rst

.. option:: -s_coord_epoch <epoch>

    .. versionadded:: 3.4

    소스 공간 좌표계와 링크되는 시대(epoch) 좌표를 할당합니다. 소스 공간 좌표계가 동적 좌표계인 경우 유용합니다. :option:`-s_srs` 옵션을 설정한 경우에만 동작합니다.

    현재 :option:`-s_coord_epoch` 와 :option:`-t_coord_epoch` 는 서로 함께 사용할 수 없습니다. 두 동적 좌표계 사이의 변환에 대한 지원이 부족하기 때문입니다.

.. option:: -ct <string>

    PROJ 문자열(한 단계 작업 또는 +proj=pipeline으로 시작하는 여러 단계 작업 문자열)로, CoordinateOperation을 설명하는 WKT2 문자열, 또는 소스로부터 대상 좌표계로의 기본 변환을 무시하는 urn:ogc:def:coordinateOperation:EPSG::XXXX URN입니다. 소스 및 대상 좌표계의 축 순서를 고려해야만 합니다.

    .. versionadded:: 3.0

.. option:: -preserve_fid

    (FID가 필수적인 포맷의 경우) 산출물 드라이버가 새 FID를 자동으로 할당하도록 하는 대신 소스 객체의 FID를 사용합니다. 추가(append) 모드가 아니고 산출물 드라이버가 FID 레이어 생성 옵션을 가지고 있는 경우 이 습성이 기본값입니다. 이런 경우 소스 FID 열의 이름을 사용하고 소스 객체 ID를 보전하려 할 것입니다. ``-unsetFid`` 옵션을 설정하면 이 습성을 비활성화할 수 있습니다.

.. option:: -fid fid

    이 옵션을 지정하는 경우, 이 객체 ID를 가진 객체만 처리할 것입니다. 공간 또는 속성 쿼리를 제외하고 작동합니다. 주의: 객체 ID를 기반으로 객체 여러 개를 선택하려는 경우, 'fid'가 OGR SQL이 인식하는 특수 필드라는 사실도 이용할 수 있습니다. 즉 `-where "fid in (1,3,5)"` 는 객체 1, 3, 5를 선택할 것입니다.

.. option:: -limit nb_features

    레이어 당 객체 개수를 제한합니다.

.. option:: -oo NAME=VALUE

    입력 데이터셋 열기 옵션 (특정 포맷 지원).

.. option:: -doo NAME=VALUE

    대상 데이터셋 열기 옵션 (특정 포맷 지원), ``-update`` 모드에서만 작동합니다.

.. option:: -gt n

    트랜잭션(transaction) 당 객체 n개를 그룹화합니다. (기본값은 100,000개입니다.) 트랜잭션을 지원하는 DBMS 드라이버에 작성하는 경우 값을 증가시키면 더 나은 성능을 보여줍니다. 데이터를 단일 트랜잭션으로 불러오려면 ``n`` 을 "unlimited"로 설정하면 됩니다.

.. option:: -ds_transaction

    (해당 메커니즘을 지원하는 드라이버의 경우) 데이터셋 수준 트랜잭션을 강제로 사용합니다. 특히 에뮬레이션 모드에서 데이터셋 수준 트랜잭션만 지원하는 FileGDB 같은 드라이버들이 이에 해당합니다.

.. option:: -clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent

    도형을 (소스 공간 좌표계 단위로) 지정한 경계 상자(bounding box), WKT 도형(폴리곤 또는 멀티폴리곤), 데이터소스의 범위, 또는 spat_extent 키워드를 사용하는 경우 spat_extent 옵션의 공간 범위로 잘라냅니다. 데이터소스를 지정하는 경우, 일반적으로 -clipsrcsql, -clipsrclayer, 또는 -clipsrcwhere 옵션과 함께 사용하는 편이 좋습니다.

.. option:: -clipsrcsql <sql_statement>

    SQL 쿼리를 대신 사용해서 원하는 도형을 선택합니다.

.. option:: -clipsrclayer <layername>

    소스 클립 데이터소스로부터 지정한 레이어를 선택합니다.

.. option:: -clipsrcwhere <expression>

    속성 쿼리를 기반으로 원하는 도형을 제한합니다.

.. option:: -clipdst <xmin> <ymin> <xmax> <ymax>

    재투영 작업 후 도형을 (대상 공간 좌표계 단위로) 지정한 경계 상자(bounding box), WKT 도형(폴리곤 또는 멀티폴리곤), 데이터소스의 범위로 잘라냅니다. 데이터소스를 지정하는 경우, 일반적으로 -clipdstsql, -clipdstlayer, 또는 -clipdstwhere 옵션과 함께 사용하는 편이 좋습니다.

.. option:: -clipdstsql <sql_statement>

    SQL 쿼리를 대신 사용해서 원하는 도형을 선택합니다.

.. option:: -clipdstlayer <layername>

    대상 클립 데이터소스로부터 지정한 레이어를 선택합니다.

.. option:: -clipdstwhere <expression>

    속성 쿼리를 기반으로 원하는 도형을 제한합니다.

.. option:: -wrapdateline

    날짜 변경 자오선(dateline meridian)을 공간교차(cross)하는 도형을 분할합니다. (경도는 +/- 180도)

.. option:: -datelineoffset

    날짜 변경선(dateline)으로부터 도 단위로 오프셋합니다. (기본 경도는 +/- 10도, 170도에서 -170도 안에 있는 도형을 분할할 것입니다.)

.. option:: -simplify <tolerance>

    단순화(simplification) 작업 용 거리 허용 오차입니다. 주의: 이 옵션에 사용되는 알고리즘은 특히 폴리곤 도형의 경우 객체 별로 위상을 보전하지만, 레이어 전체에 대해서는 아닙니다.)

.. option:: -segmentize <max_dist>

    노드 2개 사이의 최장 거리입니다. 중간(intermediate) 포인트를 생성하기 위해 사용됩니다.

.. option:: -makevalid

    도형이 단순 객체 사양의 규칙을 따라 무결한지 확인하기 위해, :cpp:func:`OGRGeometryFactory::removeLowerDimensionSubGeoms` 작업 후에 도형을 대상으로 :cpp:func:`OGRGeometry::MakeValid` 작업을 실행합니다.

    .. versionadded: 3.1 (requires GEOS 3.8 or later)

.. option:: -fieldTypeToString type1,...

    지정한 유형의 모든 필드를 대상 레이어에 있는 문자열 유형 필드로 변환합니다. Integer, Integer64, Real, String, Date, Time, DateTime, Binary, IntegerList, Integer64List, RealList, StringList 유형을 지정할 수 있습니다. 모든 필드를 문자열로 변환하려면 특수값 All을 사용하면 됩니다. OGR SQL의 CAST 연산자 대신 사용할 수 있는 방법입니다. OGR SQL의 CAST 연산자를 사용하면 아주 긴 SQL 쿼리를 입력해야 할 수도 있습니다. 이 옵션은 소스 드라이버가 사용하는 필드 유형에 영향을 미치지 않으며, 나중에 변환할 뿐이라는 사실을 기억하십시오.

.. option:: -mapFieldType srctype|All=dsttype,...

    지정한 유형의 모든 필드를 다른 유형으로 변환합니다. Integer, Integer64, Real, String, Date, Time, DateTime, Binary, IntegerList, Integer64List, RealList, StringList 유형을 지정할 수 있습니다. 이 유형들은 Integer(Boolean), Real(Float32) 등과 같이 괄호 안에 하위 유형도 포함할 수 있습니다. 모든 필드를 다른 유형으로 변환하려면 특수값 All을 사용하면 됩니다. OGR SQL의 CAST 연산자 대신 사용할 수 있는 방법입니다. OGR SQL의 CAST 연산자를 사용하면 아주 긴 SQL 쿼리를 입력해야 할 수도 있습니다. 이 옵션은 -fieldTypeToString을 일반화 버전입니다. 이 옵션은 소스 드라이버가 사용하는 필드 유형에 영향을 미치지 않으며, 나중에 변환할 뿐이라는 사실을 기억하십시오.

.. option:: -unsetFieldWidth

    필드 길이(field width)와 정확도를 0으로 설정합니다.

.. option:: -splitlistfields

    StringList, RealList 또는 IntegerList 유형 필드를 필요한 만큼 많은 String, Real 또는 Integer 유형 필드로 분할합니다.

.. option:: -maxsubfields <val>

    ``-splitlistfields`` 옵션과 결합하면 분할된 각 필드별로 생성된 하위 필드의 개수를 제한할 수 있습니다.

.. option:: -explodecollections

    모든 ``-sql`` 옵션 뒤에 이 옵션을 설정하면 소스 파일에 있는 모든 유형의 도형 집합의 각 도형마다 객체 하나를 생성합니다.

.. option:: -zfield <field_name>

    지정한 필드를 사용해서 도형의 Z좌표를 채웁니다.

.. option:: -gcp <ungeoref_x> <ungeoref_y> <georef_x> <georef_y> <elevation>

    지정한 지상기준점(ground control point)을 추가합니다. GCP 집합을 지정하기 위해 이 옵션을 여러 번 설정할 수도 있습니다.

.. option:: -order <n>

    왜곡(warp) 작업에 쓰이는 다항식(polynomial)의 순서(1에서 3까지)입니다. 기본값은 GCP의 개수를 기반으로 다항식 순서를 선택하는 것입니다.

.. option:: -tps

    사용할 수 있는 GCP를 기반으로 하는 박막 스플라인 변형(thin plate spline transformer)을 강제로 사용합니다.

.. option:: -fieldmap

    소스로부터 대상으로 복사할 필드 색인 목록을 지정합니다. 이 목록에서 지정한 n번째 값이 소스 레이어의 n번째 필드를 복사해야만 하는 대상 레이어 정의에 있는 필드 색인이 됩니다. 색인 개수는 0부터 셉니다. 어떤 필드를 누락시키려면, -1값을 지정하십시오. 이 목록에는 소스 레이어에 있는 필드 개수와 정확히 일치하는 개수의 값들을 지정해야만 합니다. 복사해야 할 필드들을 동일한 순서로 지정하려면 'identity' 설정을 사용하면 됩니다. 이 설정을 사용하는 경우 ``-append`` 옵션도 함께 사용해야 합니다.

.. option:: -addfields

    이 옵션은 ``-append`` 의 특별 버전입니다. ``-append`` 와는 반대로, ``-addfields`` 옵션은 기존 대상 레이어에 소스 레이어에서 검색된 새 필드를 추가합니다. 엄밀히 동일하지 않은 구조를 가진 파일들을 병합할 때 유용합니다. 비어 있지 않은 기존 레이어에 필드를 추가하는 기능을 지원하지 않는 산출물 포맷의 경우 이 옵션이 작동하지 않을 수도 있습니다. -addfields를 사용할 계획이라면, 초기 가져오기를 위해 포함되는 -forceNullable과 함께 사용해야 할 수도 있습니다.

.. option:: -relaxedFieldNameMatch

    대상 드라이버가 이름 일치 확인 작업(name matching)을 구현하고 있는 경우, 소스 레이어와 기존 대상 레이어 간에 이름 일치 확인 작업을 더 여유 있는 방식으로 수행합니다.

.. option:: -forceNullable

    소스 레이어가 NULL값 변환 제약조건을 가지고 있는 경우, 대상 레이어에 NULL값 변환 제약조건을 적용하지 않습니다.

.. option:: -unsetDefault

    소스 레이어가 기본 필드값을 가지고 있는 경우, 대상 레이어에 기본 필드값을 적용하지 않습니다.

.. option:: -unsetFid

    소스 FID 열의 이름과 소스 객체 ID를 대상 레이어에 재사용하지 않으려면 이 옵션을 설정하면 됩니다. 예를 들면 소스 객체를 ORDER BY 문으로 선택하는 경우 이 옵션이 유용할 수 있습니다.

.. option:: -emptyStrAsNull

    .. versionadded:: 3.3

    비어 있는 문자열 값을 NULL값으로 취급합니다.

.. option:: -resolveDomains

    .. versionadded:: 3.3

    이 옵션을 지정하면, 코딩된 필드 도메인과 링크된 모든 선택 필드에 코딩된 값에 대한 설명을 담게 될 추가 필드(``{dstfield}_resolved``)를 덧붙일 것입니다.

.. option:: -nomd

   산출물 드라이버가 메타데이터 복사를 지원하는 경우, 소스 데이터셋과 레이어로부터 대상 데이터셋과 레이어로 메타데이터를 복사하지 않습니다.

.. option:: -mo META-TAG=VALUE

    산출물 드라이버가 지원하는 경우, 산출 데이터셋에 설정할 메타데이터 키와 값을 전송(pass)합니다.

.. option:: -noNativeData

    네이티브 데이터를 복사하지 않습니다. 예를 들면 이 옵션을 설정하지 않는 경우 동일한 포맷으로 변환할 때 (GeoJSON 같은) 일부 드라이버가 보전하는, OGR 추상화(OGR abstraction)가 캡처하지 못 한 소스 포맷의 상세 정보 같은 네이티브 데이터를 복사하지 않습니다.

    .. versionadded:: 2.1

성능 힌트
-----------------

트랜잭션을 지원하는 (SQLite/PostgreSQL, MySQL 등등) DBMS에 데이터를 작성하는 경우, BEGIN TRANSACTION과 COMMIT TRANSACTION 선언문 사이에 실행되는 INSERT 선언문의 개수를 늘리는 것이 이로울 수도 있습니다. 이 개수는 -gt 옵션으로 지정됩니다. 예를 들어, SQLite의 경우 -gt를 명확하게 65536으로 정의하면 수십만 수백반 개의 행을 담고 있는 일부 테이블을 채우는(populate) 과정에서 최적화된 성능을 보장합니다. 하지만, -skipfailures 옵션이 -gt 옵션을 무시하고 트랜잭션의 크기를 1로 설정한다는 사실을 기억하십시오.

PostgreSQL의 경우, 삽입 작업의 성능을 현저하게 증가시키려면 PG_USE_COPY 환경설정 옵션을 YES로 설정하면 됩니다. PG 드라이버 문서 페이지를 읽어보십시오.

좀 더 일반적인 정보를 원한다면, 입력 및 산출 드라이버들의 문서 페이지에서 성능 힌트에 대해 알아보십시오.

C API
-----

C에서 :cpp:func:`GDALVectorTranslate` 로도 이 유틸리티를 호출할 수 있습니다.

.. versionadded::2.1

예시
--------

Shapefile을 GeoPackage로 기본 변환:

.. code-block::

  ogr2ogr \
    -f GPKG output.gpkg \
    input.shp

``EPSG:4326`` 에서 ``EPSG:3857`` 로 좌표계를 변경:

.. code-block::

  ogr2ogr \
    -s_srs EPSG:4326 \
    -t_srs EPSG:3857 \
    -f GPKG output.gpkg \
    input.gpkg

기존 레이어에 추가(append)하는 예시(``-update`` 및 ``-append`` 플래그 둘 다 사용해야 합니다):

.. code-block::

    ogr2ogr -update -append -f PostgreSQL PG:dbname=warmerda abc.tab

입력 레이어를 경계 상자(<xmin> <ymin> <xmax> <ymax>)로 잘라내기:

.. code-block::

  ogr2ogr \
    -spat -13.931 34.886 46.23 74.12 \
    -f GPKG output.gpkg \
    natural_earth_vector.gpkg

객체를 ``-where`` 문으로 필터링:

.. code-block::

  ogr2ogr \
    -where "\"POP_EST\" < 1000000" \
    -f GPKG output.gpkg \
    natural_earth_vector.gpkg \
    ne_10m_admin_0_countries


ETRS_1989_LAEA_52N_10E에서 EPSG:4326으로 재투영하고 경계 상자로 잘라내는 예시:

.. code-block::

    ogr2ogr -wrapdateline -t_srs EPSG:4326 -clipdst -5 40 15 55 france_4326.shp europe_laea.shp

``-fieldmap`` 설정을 사용하는 예시입니다. 소스 레이어의 첫 번째 필드를 사용해서 대상 레이어의 세 번째 필드를 (index 2가 세 번째 필드) 채웁니다. 소스 레이어의 두 번째 필드를 무시하고, 소스 레이어의 세 번째 필드를 사용해서 대상 레이어의 다섯 번째 필드를 채웁니다.

.. code-block::

    ogr2ogr -append -fieldmap 2,-1,4 dst.shp src.shp

개별 포맷 페이지에 더 많은 예시들이 있습니다.
