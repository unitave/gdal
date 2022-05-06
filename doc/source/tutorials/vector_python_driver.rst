.. _vector_python_driver_tut:

================================================================================
파이썬으로 벡터 드라이버 구현 예제
================================================================================

.. versionadded:: 3.1

.. highlight:: python

개요
----

GDAL 3.1버전부터, 파이썬 언어로 읽기 전용 벡터 드라이버를 작성할 수 있는 케이퍼빌리티가 추가되었습니다. 벡터 드라이버가 어떻게 작동하는지에 대한 일반적인 원칙을 알 수 있는 :ref:`vector_driver_tut` 를 먼저 읽어볼 것을 강력하게 권장합니다.

이 케이퍼빌리티는 GDAL/OGR SWIG 파이썬 바인딩을 사용할 필요가 없습니다. (그러나 파이썬 벡터 드라이버는 사용할 수도 있습니다.)

주의: 프로젝트 정책에 따라, 이 케이퍼빌리티는 "실험적인" 기능으로 간주되며 GDAL 프로젝트는 GDAL 저장소에 이런 파이썬 드라이버를 포함시키지 않을 것입니다. GDAL 마스터 브랜치에 포함시키려면 먼저 드라이버를 C++로 포팅해야 합니다. 그 이유는 다음과 같습니다:

-   파이썬 코드의 정확도는 대부분 런타임 시 확인할 수 있는 반면, C++는 (컴파일 시, 또는 다른 확인자로) 정적 분석을 할 수 있다는 장점이 있습니다.
-  파이썬 코드는 파이썬 GIL(Global Interpreter Lock) 아래 실행되기 때문에, 척도를 사용할 수 없습니다.
-  모든 GDAL 빌드가 파이썬을 사용할 수 있는 것이 아닙니다.

파이썬 해석기에 메커니즘 링크하기
---------------------------------

:ref:`linking_mechanism_to_python_interpreter` 참조

드라이버 위치
-------------

드라이버 파일명은 'gdal_' 또는 'ogr_'로 시작해야만 하고 확장자는 '.py'여야만 합니다. 다음 디렉터리에서 파이썬 드라이버 파일을 찾을 것입니다:

-  :decl_configoption:`GDAL_PYTHON_DRIVER_PATH` 환경설정 옵션이 가리키는 디렉터리 (유닉스 상에서 ':', 윈도우 상에서는 ';'으로 구분된 경로들이 여러 개 있을 수도 있습니다.)
-  이 환경설정 옵션이 지정되지 않은 경우, :decl_configoption:`GDAL_DRIVER_PATH` 환경설정 옵션이 가리키는 디렉터리
-  이 환경설정 옵션도 지정되지 않았다면 네이티브 플러그인들이 위치한 디렉터리 (유닉스 빌드의 경우 컴파일 시 하드코딩됩니다.)

GDAL은 드라이버 .py 스크립트가 가져오는 파이썬 의존성을 관리하려 시도하지 않습니다. 드라이버 스크립트의 현재 파이썬 환경에 모든 필수 의존성이 설치되어 있는지 확인하는 것은 사용자의 몫입니다.

가져오기 부분
-------------

드라이버 스크립트에 다음과 같이 기반 클래스들을 불러오는 'import' 부분이 있어야만 합니다.

.. code-block::

    from gdal_python_driver import BaseDriver, BaseDataset, BaseLayer

GADL이 ``gdal_python_driver`` 모듈을 동적으로 생성하기 때문에, 파일 시스템 상에는 존재하지 않습니다.

메타데이터 부분
---------------

.py 파일의 처음 1천 줄 안에서 수많은 필수 및 선택적 'KEY=VALUE' 드라이버 제어 옵션(directive)을 정의해야만 합니다. C++ 코드가 파이썬 해석기를 사용하지 않고 이 옵션들을 파싱하기 때문에, 다음 제약 조건을 만족시키는 것이 중요합니다:

-  한 줄에 하나의 옵션을 선언해야만 하고, 키는 ``# gdal: DRIVER_`` 로 시작해야 합니다. ('#' 문자와 'gdal', 그리고 쌍점과 'DRIVER\_' 사이에 공백을 넣어야 한다는 사실을 기억하십시오.)
-  값은 표현식, 함수 호출, 이스케이프 시퀀스 등등이 없는 유형 문자열의 문자 그대로의 값이어야만 합니다. (``# gdal: DRIVER_SUPPORTED_API_VERSION`` 은 예외로, 정수형 배열을 입력받을 수 있습니다.)
-  문자열을 작은따옴표 또는 큰따옴표로 감쌀 수도 있습니다.

다음 제어 옵션을 반드시 선언해야만 합니다:

-  ``# gdal: DRIVER_NAME`` = "some_name": 드라이버의 단축명입니다.
-  ``# gdal: DRIVER_SUPPORTED_API_VERSION`` = [1]: 드라이버가 지원하는 API 버전(들)입니다. GDAL 3.1버전에서 지원되는 유일한 버전인 1이 포함되어야만 합니다.
-  ``# gdal: DRIVER_DCAP_VECTOR`` = "YES": 벡터 드라이버로 선언합니다.
-  ``# gdal: DRIVER_DMD_LONGNAME`` = "a longer description of the driver": 드라이버의 설명입니다.

추가 제어 옵션:

-  ``# gdal: DRIVER_DMD_EXTENSIONS`` = "ext1 ext2": 드라이버가 인식하는 확장자(들)의 목록입니다. 점('.')은 없으며, 공백으로 구분합니다.
-  ``# gdal: DRIVER_DMD_HELPTOPIC`` = "url_to_help_page": 도움말 페이지의 URL입니다.
-  ``# gdal: DRIVER_DMD_OPENOPTIONLIST`` = "xml_value": 이때 'xml_value' 는 ``<OpenOptionList><Option name='OPT1' type='boolean' description='bla' default='NO'/></OpenOptionList>`` 같은 OptionOptionList 사양입니다.
-  그리고 "# gdal: DRIVER\_"로 시작하는 항목 이름과 "GDAL_DMD\_" (또는 "GDAL_DCAP") 메타데이터 항목의 값을 생성해서 gdal.h 파일에 있는 "GDAL_DMD\_"(또는 "GDAL_DCAP")로 시작하는 다른 모든 메타데이터 항목들.
   예를 들어 ``#define GDAL_DMD_CONNECTION_PREFIX "DMD_CONNECTION_PREFIX"`` 는 ``# gdal: DRIVER_DMD_CONNECTION_PREFIX`` 가 됩니다.

예시:

.. code-block:: 

    # gdal: DRIVER_NAME = "DUMMY"
    # gdal: DRIVER_SUPPORTED_API_VERSION = [1]
    # gdal: DRIVER_DCAP_VECTOR = "YES"
    # gdal: DRIVER_DMD_LONGNAME = "my super plugin"
    # gdal: DRIVER_DMD_EXTENSIONS = "foo bar"
    # gdal: DRIVER_DMD_HELPTOPIC = "http://example.com/my_help.html"

드라이버 클래스
---------------

엔트리 포인트(entry point) .py 스크립트는 ``gdal_python_driver.BaseDriver`` 로부터 상속받은 단일 클래스를 담고 있어야만 합니다.

해당 클래스는 다음과 같은 메소드들을 정의해야만 합니다:

.. py:function:: identify(self, filename, first_bytes, open_flags, open_options={})
    :noindex:

    :param str filename: 파일명, 또는 좀 더 일반적으로 연결 문자열입니다.
    :param binary first_bytes: (파일인 경우) 파일의 처음 바이트들입니다. (파일이 최소 1,024바이트인 경우) 최소값이 1024이고, 또는 드라이버 탐색 순서(probe sequence)에서 네이티브 드라이버가 이전에 더 많이 요청한 경우 그 보다 큰 값입니다.
    :param int open_flags: 열기 플래그입니다. 지금은 무시합니다.
    :param dict open_options: 열기 옵션입니다.
    :return: 드라이버가 파일을 인식하는 경우 참, 인식 못 하는 경우 거짓, 또는 처음 바이트들로 판단할 수 없는 경우 -1을 반환합니다.

.. py:function:: open(self, filename, first_bytes, open_flags, open_options={})
    :noindex:

    :param str filename: 파일명, 또는 좀 더 일반적으로 연결 문자열입니다.
    :param binary first_bytes: (파일인 경우) 파일의 처음 바이트들입니다. (파일이 최소 1,024바이트인 경우) 최소값이 1024이고, 또는 드라이버 탐색 순서(probe sequence)에서 네이티브 드라이버가 이전에 더 많이 요청한 경우 그 보다 큰 값입니다.
    :param int open_flags: 열기 플래그입니다. 지금은 무시합니다.
    :param dict open_options: 열기 옵션입니다.
    :return: gdal_python_driver.BaseDataset으로부터 파생된 객체를 반환하거나 또는 아무것도 반환하지 않습니다.

예시:

.. code-block::

    # 필수: BaseDriver로부터 파생되는 클래스
    class Driver(BaseDriver):

        def identify(self, filename, first_bytes, open_flags, open_options={}):
            return filename == 'DUMMY:'

        # 필수
        def open(self, filename, first_bytes, open_flags, open_options={}):
            if not self.identify(filename, first_bytes, open_flags):
                return None
            return Dataset(filename)


데이터셋 클래스
---------------

``Driver.open()`` 메소드가 성공하면 ``gdal_python_driver.BaseDataset`` 로부터 상속받은 클래스로부터 객체 하나를 반환해야 합니다.

레이어
++++++

이 객체는 벡터 레이어를 저장하는 역할입니다. 두 가지 구현 옵션이 있습니다. 레이어 개수가 적거나 구성 속도가 빠른 경우 ``__init__`` 메소드가 ``gdal_python_driver.BaseLayer`` 로부터 상속받은 클래스로부터 나온 객체 시퀀스인 ``layers`` 속성을 정의할 수 있습니다.

예시:

.. code-block::

    class Dataset(BaseDataset):

        def __init__(self, filename):
            self.layers = [Layer(filename)]

그렇지 않다면, 다음 메소드 2개를 정의해야 합니다:

.. py:function:: layer_count(self)
    :noindex:

    :return: 레이어의 개수를 반환합니다.

.. py:function:: layer(self, idx)
    :noindex:

    :param int idx: 반환할 레이어의 색인입니다. 일반적으로 0에서 'self.layer_count() - 1' 사이의 값이지만, 호출하는 코드가 어떤 값이든 전송할 수도 있습니다. 무결하지 않은 색인의 경우, 아무것도 반환하지 않을 것입니다.
    :return: gdal_python_driver.BaseLayer로부터 파생된 객체를 반환하거나 또는 아무것도 반환하지 않습니다. C++ 코드가 해당 객체를 캐시에 저장하고, 이 메소드는 지정한 idx 값에 대해 한 번 호출될 뿐입니다.

예시:

.. code-block::

    class Dataset(BaseDataset):

        def layer_count(self):
            return 1

        def layer(self, idx):
            return [Layer(self.filename)] if idx = 0 else None

메타데이터
++++++++++

데이터셋이 기본 메타데이터 도메인의 "key: value" 유형 문자열의 ``__init__`` 에 ``metadata`` 딕셔너리를 정의할 수도 있습니다. 아니면, 다음 메소드를 구현할 수도 있습니다.

.. py:function:: metadata(self, domain)
    :noindex:

    :param str domain: 메타데이터 도메인입니다. 기본 도메인인 경우 비어 있는 문자열을 사용합니다.
    :return: 아무것도 반환하지 않거나, "키:값" 쌍 유형 문자열의 딕셔너리를 반환합니다.

기타 메소드
+++++++++++

다음 메소드를 선택적으로 구현할 수도 있습니다:

.. py:function:: close(self)
    :noindex:

    C++ 피어(peer) GDALDataset 객체를 삭제할 때 호출됩니다. 예를 들면 데이터베이스 연결을 종료하는 데 유용합니다.

레이어 클래스
-------------

데이터셋 객체가 ``gdal_python_driver.BaseLayer`` 로부터 상속받는 클래스로부터 나온 하나 이상의 객체를 인스턴스화할 것입니다.

메타데이터 및 기타 정의
+++++++++++++++++++++++

``__init__`` 시 다음 속성들을 요구하며 반드시 정의해야만 합니다:

.. py:attribute:: name
    :noindex:

    레이어 이름 유형 문자열입니다. 설정하지 않는 경우 ``name`` 메소드를 정의해야만 합니다.

.. py:attribute:: fields

    필드 정의들의 순열입니다. (비어 있을 수도 있습니다.) 각 필드는 다음 속성(property)들을 가진 딕셔너리입니다:

    .. py:attribute:: name
        :noindex:

        필수

    .. py:attribute:: type
        :noindex:

        (SWIG 파이썬 바인딩의) ogr.OFT\_ 유형의 정수값, 또는 다음 ``String``, ``Integer``, ``Integer16``, ``Integer64``, ``Boolean``, ``Real``, ``Float``, ``Binary``, ``Date``, ``Time``, ``DateTime`` 문자열 값들 가운데 하나입니다.

    이 속성을 설정하지 않는 경우, ``fields`` 메소드를 정의해서 이런 순열을 반환해야만 합니다.

.. py:attribute:: geometry_fields
    :noindex:

    도형 정의들의 순열입니다. (비어 있을 수도 있습니다.) 각 필드는 다음 속성(property)들을 가진 딕셔너리입니다:

    .. py:attribute:: name
        :noindex:

        필수. 비어 있을 수도 있습니다.

    .. py:attribute:: type
        :noindex:

        필수. (SWIG 파이썬 바인딩의) ogr.wkb\_ 유형의 정수값, 또는 다음 ``Unknown``, ``Point``, ``LineString``, ``Polygon``, ``MultiPoint``, ``MultiLineString``, ``MultiPolygon``, ``GeometryCollections`` 또는 :cpp:func:`OGRGeometryTypeToName` 함수가 반환하는 다른 모든 값들 가운데 하나입니다.

    .. py:attribute:: srs
        :noindex:

        도형 필드에 :cpp:func:`OGRSpatialReference::SetFromUserInput` 함수가 받아들일 수 있는 PROJ 문자열, WKT 문자열, 또는 AUTHORITY:CODE 같은 문자열로 추가되는 공간 좌표계입니다.

    이 속성을 설정하지 않는 경우, ``geometry_fields`` 메소드를 정의해서 이런 순열을 반환해야만 합니다.

다음 속성들은 선택적입니다:

.. py:attribute:: fid_name
    :noindex:

    피처ID 열 이름 유형 문자열이빈다. 빈 문자열일 수도 있습니다. 설정하지 않는 경우 ``fid_name`` 메소드를 정의할 수도 있습니다.

.. py:attribute:: metadata
    :noindex:

    기본 메타데이터 도메인의 메타데이터에 대응하는 "key: value" 문자열들의 딕셔너리입니다. 아니면, 도메인 인자를 입력받는 ``metadata`` 메소드를 정의할 수도 있습니다.

.. py:attribute:: iterator_honour_attribute_filter
    :noindex:

    피처 반복자(iterator)가 레이어 상에 설정할 수 있는 ``attribute_filter`` 속성을 연산에 넣는 경우 참으로 설정할 수 있습니다.

.. py:attribute:: iterator_honour_spatial_filter
    :noindex:

    피처 반복자(iterator)가 레이어 상에 설정할 수 있는 ``spatial_filter`` 속성을 연산에 넣는 경우 참으로 설정할 수 있습니다.

.. py:attribute:: feature_count_honour_attribute_filter
    :noindex:

    feature_count 메소드가 레이어 상에 설정할 수 있는 ``attribute_filter`` 속성을 연산에 넣는 경우 참으로 설정할 수 있습니다.

.. py:attribute:: feature_count_honour_spatial_filter
    :noindex:

    feature_count 메소드가 레이어 상에 설정할 수 있는 ``spatial_filter`` 속성을 연산에 넣는 경우 참으로 설정할 수 있습니다.

피처 반복자
+++++++++++

레이어 클래스가 반복자(iterator) 인터페이스를 구현해야만 하기 때문에, 일반적으로 ``__iter__`` 메소드로 구현합니다.

반복자는 피처 내용을 가진 딕셔너리를 반환해야만 합니다.

반환되는 딕셔너리에 허용되는 키들은 다음과 같습니다:

.. py:attribute:: id
    :noindex:

    강력히 권장합니다. GDAL이 FID로 인식하려면 이 값이 정수형이어야만 합니다.

.. py:attribute:: type
    :noindex:

    필수. 이 값은 "OGRFeature" 문자열이어야만 합니다.

.. py:attribute:: fields
    :noindex:

    필수. 이 값은 키가 필드 이름인 딕셔너리여야만 합니다. 또는 비어 있을 수도 있습니다.

.. py:attribute:: geometry_fields
    :noindex:

    필수. 이 값은 키가 도형 필드 이름인 딕셔너리여야만 합니다. (명명되지 않은 도형 열인 경우 빈 문자열일 수도 있습니다.) 또는 비어 있을 수도 있습니다. 각 키의 값은 WKT로 인코딩된 도형이어야만 하며, 비어 있을 수도 있습니다.

.. py:attribute:: style
    :noindex:

    선택적. 이 값은 :ref:`ogr_feature_style` 을 준수하는 문자열이어야만 합니다.

필터링
++++++

기본적으로 드라이버의 일반 C++ 쪽이 OGR API 사용자가 설정한 모든 속성 또는 공간 필터를 레이어의 모든 피처에 반복해서 평가할 것입니다.

``iterator_honour_attribute_filter`` (또는 ``iterator_honour_spatial_filter``) 레이어 객체 속성을 ``True`` 로 설정하면, 피처 반복자 메소드가 속성 필터를 (또는 공간 필터를) 준수해야만 합니다.

속성 필터는 레이어 객체의 ``attribute_filter`` 속성에 설정됩니다. 그 값은 :ref:`OGR SQL <ogr_sql_dialect>` 을 준수하는 문자열입니다. OGR API가 속성 필터를 변경하는 경우, 선택적인 ``attribute_filter_changed`` 메소드를 호출합니다. (선택적인 메소드는 아래 단락을 참조하십시오.) ``attribute_filter_changed`` 구현이 ``SetAttributeFilter`` 메소드를 호출해서 드라이버의 일반 C++ 쪽이 평가하도록 결정할 수도 있습니다. (아래 전체 예시를 참조하십시오.)

도형 필터는 레이어 객체의 ``spatial_filter`` 에 설정됩니다. 그 값은 ISO WKT로 인코딩된 문자열입니다. 도형 필터를 레이어 좌표계로 표현하는 것은 OGR API 사용자의 몫입니다. OGR API가 공간 필터를 변경하는 경우, 선택적인 ``spatial_filter_changed`` 메소드를 호출합니다. (선택적인 메소드는 아래 단락을 참조하십시오.) ``spatial_filter_changed`` 구현이 ``SetSpatialFilter`` 메소드를 호출해서 드라이버의 일반 C++ 쪽이 평가하도록 결정할 수도 있습니다. (아래 전체 예시를 참조하십시오.)

기타 메소드
+++++++++++

다음 메소드들을 선택적으로 구현할 수도 있습니다:

.. py:function:: extent(self, force_computation)
    :noindex:

    :return: 레이어의 공간 범위를 가진 [xmin,ymin,xmax,ymax] 목록을 반환합니다.

.. py:function:: feature_count(self, force_computation)
    :noindex:

    :return: 레이어의 피처 개수를 반환합니다.

    self.feature_count_honour_attribute_filter 또는 self.feature_count_honour_spatial_filter 를 참으로 설정하면, 이 메소드가 속성 필터 그리고/또는 공간 필터를 준수해야만 합니다.

.. py:function:: feature_by_id(self, fid)
    :noindex:

    :param int fid: 피처ID
    :return: 앞에서 설명한 ``__next__`` 메소드의 포맷들 가운데 하나로 된 객체를 반환하거나, 피처ID와 일치하는 객체가 없는 경우 아무것도 반환하지 않습니다.

.. py:function:: attribute_filter_changed(self)
    :noindex:

    self.attribute_filter가 변경될 때마다 이 메소드를 호출합니다. 드라이버가 self.iterator_honour_attribute_filter 또는 feature_count_honour_attribute_filter 속성의 값을 변경할 수도 있는 기회입니다.

.. py:function:: spatial_filter_changed(self)
    :noindex:

    elf.spatial_filter가 변경될 때마다 이 메소드를 호출합니다. (그 값은 WKT로 인코딩된 도형입니다.) 드라이버가 self.iterator_honour_spatial_filter 또는 feature_count_honour_spatial_filter 속성의 값을 변경할 수도 있는 기회입니다.

.. py:function:: test_capability(self, cap)
    :noindex:

    :param cap string: BaseLayer.FastGetExtent, BaseLayer.FastSpatialFilter, BaseLayer.FastFeatureCount, BaseLayer.RandomRead, BaseLayer.StringsAsUTF8 또는 :cpp:func:`OGRLayer::TestCapability` 함수가 지원하는 다른 문자열 가운데 하나를 값으로 설정할 수 있습니다.
    :return: 이 케이퍼빌리티를 지원하는 경우 참, 지원하지 않으면 거짓을 반환합니다.

전체 예시
------------

다음은 호출을 SWIG 파이썬 GDAL API로 포워딩하는 통과(passthrough) 드라이버의 예시입니다. 실용적인 기능은 없으며, 그저 API의 가능한 사용례를 가능한 한 모두 보여주기 위한 것입니다. 실제 드라이버는 여기서 보여주는 API의 일부분만 사용할 것입니다. 예를 들어 통과 드라이버는 드라이버의 C++ 부분을 다시 불러오는 완전히 가짜 방식으로 속성 및 공간 필터를 구현합니다. 이 예시에서는 ``iterator_honour_attribute_filter`` 및 ``iterator_honour_spatial_filter`` 속성 구현, 그리고 ``attribute_filter_changed`` 및 ``spatial_filter_changed`` 메소드 구현이 동일한 결과물로 생략했을 수도 있습니다.

드라이버가 인식하는 연결 문자열은 "PASSHTROUGH:connection_string_supported_by_non_python_drivers"입니다. 드라이버 이름을 반드시 접두어로 사용해야 하는 것은 아니지만, 가짜인 이 특정 드라이버를 특정하기 위한 것입니다. (접두어가 없으면 연결 문자열이 네이티브 드라이버를 직접 가리킬 것입니다.) :ref:`기타 예시 <other_examples>` 에 소개된 CityJSON 드라이버는 이런 접두어가 필요없습니다.

.. code-block::

    #!/usr/bin/env python
    # -*- 인코딩: utf-8 -*-
    # 이 코드는 실제 플러그인 용 템플릿 역할을
    # 수행하도록 또는 사용 권한 소유자의 선택으로
    # 퍼블릭 도메인에 속합니다.
    # Copyright 2019 이벤 루올(Even Rouault)
    # SPDX-License-Identifier: MIT

    # gdal: DRIVER_NAME = "PASSTHROUGH"
    # API 버전(들)을 지원합니다. 현재 1을 포함해야만 합니다
    # gdal: DRIVER_SUPPORTED_API_VERSION = [1]
    # gdal: DRIVER_DCAP_VECTOR = "YES"
    # gdal: DRIVER_DMD_LONGNAME = "Passthrough driver"
    # gdal: DRIVER_DMD_CONNECTION_PREFIX = "PASSTHROUGH:"

    from osgeo import gdal, ogr

    from gdal_python_driver import BaseDriver, BaseDataset, BaseLayer

    class Layer(BaseLayer):

        def __init__(self, gdal_layer):
            self.gdal_layer = gdal_layer
            self.name = gdal_layer.GetName()
            self.fid_name = gdal_layer.GetFIDColumn()
            self.metadata = gdal_layer.GetMetadata_Dict()
            self.iterator_honour_attribute_filter = True
            self.iterator_honour_spatial_filter = True
            self.feature_count_honour_attribute_filter = True
            self.feature_count_honour_spatial_filter = True

        def fields(self):
            res = []
            layer_defn = self.gdal_layer.GetLayerDefn()
            for i in range(layer_defn.GetFieldCount()):
                ogr_field_def = layer_defn.GetFieldDefn(i)
                field_def = {"name": ogr_field_def.GetName(),
                             "type": ogr_field_def.GetType()}
                res.append(field_def)
            return res

        def geometry_fields(self):
            res = []
            layer_defn = self.gdal_layer.GetLayerDefn()
            for i in range(layer_defn.GetGeomFieldCount()):
                ogr_field_def = layer_defn.GetGeomFieldDefn(i)
                field_def = {"name": ogr_field_def.GetName(),
                             "type": ogr_field_def.GetType()}
                srs = ogr_field_def.GetSpatialRef()
                if srs:
                    field_def["srs"] = srs.ExportToWkt()
                res.append(field_def)
            return res

        def test_capability(self, cap):
            if cap in (BaseLayer.FastGetExtent, BaseLayer.StringsAsUTF8,
                    BaseLayer.RandomRead, BaseLayer.FastFeatureCount):
                return self.gdal_layer.TestCapability(cap)
            return False

        def extent(self, force_computation):
            # SWIG GetExtent()와 파이썬 드라이버 API 사이의 임피던스(impedance) 불일치
            minx, maxx, miny, maxy = self.gdal_layer.GetExtent(force_computation)
            return [minx, miny, maxx, maxy]

        def feature_count(self, force_computation):
            # 더미 구현: 일반 C++ 구현을 다시 호출합니다
            return self.gdal_layer.GetFeatureCount(True)

        def attribute_filter_changed(self):
            # 더미 구현: 일반 C++ 구현을 다시 호출합니다
            if self.attribute_filter:
                self.gdal_layer.SetAttributeFilter(str(self.attribute_filter))
            else:
                self.gdal_layer.SetAttributeFilter(None)

        def spatial_filter_changed(self):
            # 더미 구현: 일반 C++ 구현을 다시 호출합니다
            # 'inf' 테스트는 test_ogrsf 특이성만을 위한 것입니다
            if self.spatial_filter and 'inf' not in self.spatial_filter:
                self.gdal_layer.SetSpatialFilter(
                    ogr.CreateGeometryFromWkt(self.spatial_filter))
            else:
                self.gdal_layer.SetSpatialFilter(None)

        def _translate_feature(self, ogr_f):
            fields = {}
            layer_defn = ogr_f.GetDefnRef()
            for i in range(ogr_f.GetFieldCount()):
                if ogr_f.IsFieldSet(i):
                    fields[layer_defn.GetFieldDefn(i).GetName()] = ogr_f.GetField(i)
            geom_fields = {}
            for i in range(ogr_f.GetGeomFieldCount()):
                g = ogr_f.GetGeomFieldRef(i)
                if g:
                    geom_fields[layer_defn.GetGeomFieldDefn(
                        i).GetName()] = g.ExportToIsoWkt()
            return {'id': ogr_f.GetFID(),
                    'type': 'OGRFeature',
                    'style': ogr_f.GetStyleString(),
                    'fields': fields,
                    'geometry_fields': geom_fields}

        def __iter__(self):
            for f in self.gdal_layer:
                yield self._translate_feature(f)

        def feature_by_id(self, fid):
            ogr_f = self.gdal_layer.GetFeature(fid)
            if not ogr_f:
                return None
            return self._translate_feature(ogr_f)

    class Dataset(BaseDataset):

        def __init__(self, gdal_ds):
            self.gdal_ds = gdal_ds
            self.layers = [Layer(gdal_ds.GetLayer(idx))
                        for idx in range(gdal_ds.GetLayerCount())]
            self.metadata = gdal_ds.GetMetadata_Dict()

        def close(self):
            del self.gdal_ds
            self.gdal_ds = None


    class Driver(BaseDriver):

        def _identify(self, filename):
            prefix = 'PASSTHROUGH:'
            if not filename.startswith(prefix):
                return None
            return gdal.OpenEx(filename[len(prefix):], gdal.OF_VECTOR)

        def identify(self, filename, first_bytes, open_flags, open_options={}):
            return self._identify(filename) is not None

        def open(self, filename, first_bytes, open_flags, open_options={}):
            gdal_ds = self._identify(filename)
            if not gdal_ds:
                return None
            return Dataset(gdal_ds)

.. _other_examples:

기타 예시
--------------

https://github.com/OSGeo/gdal/tree/master/examples/pydrivers 에서 CityJSON 드라이버를 포함한 다른 예시들을 찾아볼 수 있습니다.

