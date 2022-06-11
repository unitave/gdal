.. _rfc-76:

================================================================================
RFC 76: OGR 파이썬 드라이버
================================================================================

============ ==========================
저자:        이벤 루올
연락처:      even.rouault@spatialys.com
제안일:      2019년 11월 5일
최신 수정일: 2019년 11월 15일
상태:        승인, GDAL 3.1버전에 구현
============ ==========================

요약
----

이 RFC는 OGR/벡터 드라이버를 파이썬으로 작성할 수 있는 케이퍼빌리티를 추가할 것을 제안합니다.

동기
----

빠른 속도를 요구하지 않는 일부 사용례의 경우 또는 거의 사용되지 않는 (자체 내부 포맷일 가능성이 높은) 포맷을 처리하려는 경우 현재 요구되는 대로 GDAL C++ 드라이버 또는 즉석(ad hoc) 변환기를 사용하기보다 파이썬으로 벡터 드라이버를 작성하는 편이 더 빠르고 효율적일 수도 있습니다.

.. note::

   QGIS는 현재 https://github.com/qgis/QGIS/blob/master/tests/src/python/provider_python.py 에서와 같이 파이썬 기반 제공자를 생성할 수 있는 방법을 가지고 있습니다.
   GDAL 자체에서도 이런 방법을 가지게 된다면 나머지 GDAL/OGR 기반 도구들도 OGR 파이썬 드라이버를 사용할 수 있게 될 것입니다.

작동 방식은?
------------

드라이버 등록
+++++++++++++

드라이버 등록 메커니즘이 전용 디렉터리에서 :file:`.py` 스크립트를 검색하도록 확장합니다:

-  ``GDAL_PYTHON_DRIVER_PATH`` 환경설정 옵션이 가리키는 디렉터리
   (경로가 여러 개일 수도 있습니다. 유닉스 상에서는 ``:`` 그리고 윈도우 상에서는 ``;`` 문자로 구분합니다.)

-  앞에서 정의하지 않은 경우, ``GDAL_DRIVER_PATH`` 환경설정 옵션이 가리키는 디렉터리

-  앞에서 정의하지 않은 경우, (유닉스 빌드의 경우 컴파일 시 하드코딩된) 네이티브 플러그인들이 위치해 있는 디렉터리

이 파이썬 스크립트의 처음 줄들에 다음 가운데 적어도 2개의 지시문을 설정해야만 합니다:

-  ``# gdal: DRIVER_NAME = "short_name"``

-  ``# gdal: DRIVER_SUPPORTED_API_VERSION = 1``:
   현재 1만 지원합니다. 하위 호환성 방식으로 인터페이스를 변경한 경우, 지원하는 API 버전 번호를 내부적으로 증가시킬 것입니다. 이 항목은 파이썬 드라이버를 "안전하게" 불러올 수 있는지를 확인할 수 있게 해줍니다.
   파이썬 드라이버가 여러 API 버전을 지원할 경우 (이 시점에서는 정말로 가능한지 명확하지 않습니다) ``[1,2]`` 처럼 여러 버전들을 나타내는 배열 문법을 사용할 수도 있습니다.

-  ``# gdal: DRIVER_DCAP_VECTOR = "YES"``

-  ``# gdal: DRIVER_DMD_LONGNAME = "my super plugin"``

``# gdal: DRIVER_DMD_EXTENSIONS`` 또는 ``# gdal: DRIVER_DMD_HELPTOPIC`` 같은 선택적인 메타데이터를 (근본적으로, 접두어 ``# gdal: DRIVER_`` 가 붙은 모든 드라이버 메타데이터 키 문자열을) 정의할 수 있습니다.

효율성을 고려해서는 물론 가능한 한 파이썬 해석기(interpreter)를 재탐색 또는 실행하지 않으려는 이유로, 파이썬 해석기를 호출하지 않고 순수 텍스트 방식으로 이런 지시문을 파싱할 것입니다. (이것은 QGIS가 GDAL을 사용하는 경우 일반적인 사용례입니다: 파이썬 해석기를 재사용하기 위해 QGIS 자체가 파이썬을 시작하는 것을 확실히 하고자 합니다.)

단축 메타데이터로부터 나온 드라이버 등록 코드가 :cpp:class:`GDALDriver` C++ 객체를 인스턴스화할 수 있습니다. 해당 객체에 대해 Identify() 또는 Open() 메소드를 호출하면, C++ 코드가:

-  아직 수행하지 않은 경우, 파이썬 심볼을 찾거나 또는 파이썬을 시작할 것입니다. (자세한 내용은 다음 단락을 참조하십시오.)

-  아직 수행하지 않은 경우, :file:`.py` 파일을 파이썬 모듈로서 불러올 것입니다.

-  아직 수행하지 않은 경우, ``gdal_python_driver.BaseDriver`` 로부터 파생시킨 모듈의 파이썬 클래스 인스턴스를 인스턴스화할 것입니다.

-  시작된(originated) API 호출에 따라 ``identify`` 및 ``open`` 메소드를 호출할 것입니다.

``open`` 메소드는 파이썬 ``BaseDataset`` 객체를 대응하는 GDAL API 호출이 호출할 필수 및 선택적 메소들과 함께 반환할 것입니다. ``BaseLayer`` 객체에 대해서도 마찬가지입니다. :ref:`드라이버 예시 <example_>` 를 참조하십시오.

Python 해석기와 연결
++++++++++++++++++++

파이썬 기능으로 작성된 VRT 픽셀 함수들과 이 로직을 공유할 것입니다. 이 로직은 런타임 시 처리 과정에서 이미 사용할 수 있는 파이썬 심볼(예를 들어 QGIS처럼 파이썬 실행 파일 또는 GDAL을 이용하는 파이썬을 내장한 바이너리)에 링크하기  또는 어떤 파이썬 심볼도 찾을 수 없는 경우 컴파일 시 링크하기보다 파이썬 라이브러리 불러오기에 의존합니다.
그 이유는 GDAL이 링크될 가능성이 있는 파이썬 버전을 미리 알지 못 하며, :file:`gdal.so`/:file:`gdal.dll` 이 특정 파이썬 라이브러리와 명확하게 링크되지 않기를 바라기 때문입니다.

이 작업은 파이썬 내장 및 파이썬 확장을 둘 다 수행합니다.

다음 단계를 거칩니다:

1. 파이썬 심볼 검색을 위해 유닉스 상에서는 dlopen() + dlsym()을, 윈도우 상에서는 EnumProcessModules() + GetProcAddress()를 철저히 수행합니다. 파이썬 심볼을 찾은 경우, 해당 심볼을 사용합니다. 예를 들면 파이썬 모듈(GDAL 파이썬 바인딩, rasterio 등등) 또는 파이썬 해석기를 시작하는 QGIS 같은 응용 프로그램으로부터 GDAL을 사용하는 경우입니다.

2. 그렇지 않다면, :file:`pythonX.Y[...].so/.dll` 을 가리키고 있을 PYTHONSO 환경 변수를 검색합니다.

3. 그렇지 않다면, 경로에서 파이썬 바이너리를 검색해서 대응하는 파이썬 :file:`.so/.dll` 을 식별하려 시도합니다.

4. 그렇지 않다면, dlopen()/LoadLibrary()를 이용해서 파이썬 :file:`.so/.dll` 의 잘 알려진 이름들을 불러오려 시도합니다.

GDAL 코어에 미치는 영향
-----------------------

미미합니다. GDALAllRegister()에 앞에서 언급한 로직을 구현하는 :cpp:func:`GDALDriverManager::AutoLoadPythonDrivers` 호출을 추가합니다. :cpp:class:`GDALDriver` 클래스가 새 IdentifyEx() 함수 포인터를 지원하도록 확장합니다. 파이썬 코드를 불러오는 C++ `심(shim) <https://en.wikipedia.org/wiki/Shim_(computing)>`_ 이 이 포인터를 사용합니다.

.. code-block:: c++

    int                 (*pfnIdentifyEx)( GDALDriver*, GDALOpenInfo * );

GDALIdentify() 및 GDALOpen() 메소드들이 ``GDALDriver*`` 인자를 추가하도록 확장된 IdentifyEx() 함수 포인터를 우선 사용합니다. 이 포인터가 필요한 이유는 별 게 아닙니다. 일반 C++ 드라이버의 경우 드라이버와 드라이버를 구현하는 함수 사이에 1대1 대응성이 존재하기 때문에, 드라이버를 전송해야 할 필요가 없습니다. 그러나 파이썬 드라이버의 경우, 여러 파이썬 드라이버의 파이썬 Identify() 메소드와 작업하기 위한 인터페이스 역할을 하는 C++ 메소드가 하나뿐입니다. 따라서 알맞은 드라이버에 호출을 포워딩할 수 있는 ``GDALDriver*`` 인자가 필요합니다.

.. _example:

이런 드라이버의 예시
--------------------

연결 문자열 앞에 드라이버 이름을 접두어로 붙이는 일이 절대 필수는 아니지만, 해당 특정 드라이버에 특화된 요구 사항으로 약간 인위적입니다. 다음에 언급하는 CityJSON 드라이버는 연결 문자열 앞에 드라이버 이름을 접두어로 붙이지 않아도 됩니다:

.. code-block:: python

    #!/usr/bin/env python
    # -*- 인코딩: utf-8 -*-
    # 이 코드는 퍼블릭 도메인으로, 실제 플러그인 용
    # 템플릿 역할입니다.
    # 또는 사용 허가를 받은 쪽이 선택할 수 있습니다.
    # Copyright 2019 Even Rouault
    # SPDX-License-Identifier: MIT

    # 불러오기 전 드라이버에서 GDAL C++ 코드가 파싱한,
    # '# gdal: '로 시작하는 메타데이터. 필수이며,
    # 파이썬을 인식하지 못 하는 코드가 파싱했기 때문에
    # 정확한 문법을 사용해야 합니다.
    # 따라서 리터럴 값뿐이고 표현식 등등은 없습니다.
    # gdal: DRIVER_NAME = "DUMMY"
    # API 버전(들)을 지원합니다. 현재 1이 포함되어야만 합니다.
    # gdal: DRIVER_SUPPORTED_API_VERSION = [1]
    # gdal: DRIVER_DCAP_VECTOR = "YES"
    # gdal: DRIVER_DMD_LONGNAME = "my super plugin"

    # 선택적인 드라이버 메타데이터 항목들입니다.
    # # gdal: DRIVER_DMD_EXTENSIONS = "ext1 est2"
    # # gdal: DRIVER_DMD_HELPTOPIC = "http://example.com/my_help.html"

    # 런타임 시 GDAL 라이브러리가 gdal_python_driver 모듈을 정의합니다.
    from gdal_python_driver import BaseDriver, BaseDataset, BaseLayer

    class Layer(BaseLayer):
        def __init__(self):

            # 예약 속성명들입니다. 이 이름들 또는 대응하는 메소드
            # 가운데 하나를 반드시 정의해야만 합니다.
            self.name = 'my_layer'  # 필수, 또는 name() 메소드

            self.fid_name = 'my_fid'  # Optional

            self.fields = [{'name': 'boolField', 'type': 'Boolean'},
                        {'name': 'int16Field', 'type': 'Integer16'},
                        {'name': 'int32Field', 'type': 'Integer'},
                        {'name': 'int64Field', 'type': 'Integer64'},
                        {'name': 'realField', 'type': 'Real'},
                        {'name': 'floatField', 'type': 'Float'},
                        {'name': 'strField', 'type': 'String'},
                        {'name': 'strNullField', 'type': 'String'},
                        {'name': 'strUnsetField', 'type': 'String'},
                        {'name': 'binaryField', 'type': 'Binary'},
                        {'name': 'timeField', 'type': 'Time'},
                        {'name': 'dateField', 'type': 'Date'},
                        {'name': 'datetimeField', 'type': 'DateTime'}]  # 필수, 또는 fields() 메소드

            self.geometry_fields = [{'name': 'geomField',
                                    'type': 'Point',  # optional
                                    'srs': 'EPSG:4326'  # optional
                                    }]  # 필수, 또는 geometry_fields() 메소드

            self.metadata = {'foo': 'bar'}  # 선택적

            # __iter__()가 self.attribute_filter를 준수하는 경우 주석 해제
            #self.iterator_honour_attribute_filter = True

            # __iter__()가 self.spatial_filter를 준수하는 경우 주석 해제
            #self.iterator_honour_spatial_filter = True

            # feature_count()가 self.attribute_filter를 준수하는 경우 주석 해제
            #self.feature_count_honour_attribute_filter = True

            # feature_count()가 self.spatial_filter를 준수하는 경우 주석 해제
            #self.feature_count_honour_spatial_filter = True

            # 예약 속성명 끝

            self.count = 5

        # self.name 속성을 정의하지 않는 한 필수
        # def name(self):
        #    return 'my_layer'

        # 선택적. 정의하지 않는 경우, fid 이름은 'fid'입니다.
        # def fid_name(self):
        #    return 'my_fid'

        # self.geometry_fields 속성을 정의하지 않는 한 필수
        # def geometry_fields(self):
        #    return [...]

        # self.required 속성을 정의하지 않는 한 필수
        # def fields(self):
        #    return [...]

        # 선택적. self.metadata 필드를 정의하지 않는 경우에만 사용합니다.
        # def metadata(self, domain):
        #    if domain is None:
        #        return {'foo': 'bar'}
        #    return None

        # 선택적. GDAL이 self.attribute_filter를 변경한 경우 호출합니다.
        # def attribute_filter_changed(self):
        #     # self.iterator_honour_attribute_filter 또는
        #     # feature_count_honour_attribute_filter를 변경할 수도 있습니다.
        #     pass

        # 선택적. GDAL이 self.spatial_filter를 변경한 경우 호출합니다.
        # def spatial_filter_changed(self):
        #     # self.iterator_honour_spatial_filter 또는
        #     # feature_count_honour_spatial_filter를 변경할 수도 있습니다.
        #     pass

        # 선택적.
        def test_capability(self, cap):
            if cap == BaseLayer.FastGetExtent:
                return True
            if cap == BaseLayer.StringsAsUTF8:
                return True
            # if cap == BaseLayer.FastSpatialFilter:
            #    return False
            # if cap == BaseLayer.RandomRead:
            #    return False
            if cap == BaseLayer.FastFeatureCount:
                return self.attribute_filter is None and self.spatial_filter is None
            return False

        # 선택적.
        def extent(self, force_computation):
            return [2.1, 49, 3, 50]  # minx, miny, maxx, maxy

        # 선택적.
        def feature_count(self, force_computation):
            # feature_count_honour_attribute_filter 및 feature_count_honour_spatial_filter를
            # 선언하지 않았기 때문에, 다음 상황은 일어날 수 없습니다.
            # 그러나 이 코드는 기본 구현을 콜백할 수 있다는 사실을 설명하기 위한 것입니다.
            # if needed
            # if self.attribute_filter is not None or \
            #   self.spatial_filter is not None:
            #    return super(Layer, self).feature_count(force_computation)

            return self.count

        # 필수. 동일한 Layer 객체 상에 동시 반복자들을 사용하는 경우를
        # 사용자가 처리할 필요가 없습니다.
        def __iter__(self):
            for i in range(self.count):
                properties = {
                    'boolField': True,
                    'int16Field': 32767,
                    'int32Field': i + 2,
                    'int64Field': 1234567890123,
                    'realField': 1.23,
                    'floatField': 1.2,
                    'strField': 'foo',
                    'strNullField': None,
                    'binaryField': b'\x01\x00\x02',
                    'timeField': '12:34:56.789',
                    'dateField': '2017-04-26',
                    'datetimeField': '2017-04-26T12:34:56.789Z'}

                yield {"type": "OGRFeature",
                    "id": i + 1,
                    "fields": properties,
                    "geometry_fields": {"geomField": "POINT(2 49)"},
                    "style": "SYMBOL(a:0)" if i % 2 == 0 else None,
                    }

        # 선택적.
        # def feature_by_id(self, fid):
        #    return {}


    class Dataset(BaseDataset):

        # 선택적이지만 일반적으로 구현이 필요로 할 것입니다.
        def __init__(self, filename):
            # 레이어 멤버를 설정하면 layer_count() 및 layer()를 사용하지 않을 것입니다.
            self.layers = [Layer()]
            self.metadata = {'foo': 'bar'}

        # 선택적. 네이티브 객체 삭제 시 호출합니다.
        def __del__(self):
            pass

        # 선택적. self.metadata 필드를 정의하지 않은 경우에만 사용합니다.
        # def metadata(self, domain):
        #    if domain is None:
        #        return {'foo': 'bar'}
        #    return None

        # __init__에 레이어 속성을 설정하지 않는 이상 필수
        # def layer_count(self):
        #    return len(self.layers)

        # __init__에 레이어 속성을 설정하지 않는 이상 필수
        # def layer(self, idx):
        #    return self.layers[idx]


    # 필수: BaseDriver로부터 파생시킨 클래스
    class Driver(BaseDriver):

        # 선택적. 드라이버를 처음 불러왔을 때 호출합니다.
        def __init__(self):
            pass

        # 필수.
        def identify(self, filename, first_bytes, open_flags, open_options={}):
            return filename == 'DUMMY:'

        # 필수.
        def open(self, filename, first_bytes, open_flags, open_options={}):
            if not self.identify(filename, first_bytes, open_flags):
                return None
            return Dataset(filename)


다른 예시들:

-  호출을 GDAL SWIG 파이썬 API로 포워딩하는 PASSTHROUGH 드라이버:
   https://github.com/OSGeo/gdal/blob/master/examples/pydrivers/ogr_PASSTHROUGH.py

-  `CityJSON <https://www.cityjson.org/>`_ 의 단순 파싱을 구현한 드라이버:
   https://github.com/OSGeo/gdal/blob/master/examples/pydrivers/ogr_CityJSON.py

제한 사항 및 범위
-----------------

-  현재 파이썬 드라이버는 벡터 용 그리고 읽기 전용입니다. 물론 향후 확장될 수 있습니다.

-  플러그인의 파이썬 코드와 SWIG을 기반으로 빌드된 OGR 파이썬 API 사이에는 아무 관련도 없어야 합니다. 이렇게 할 수 있는 타당한 방법은 없는 것으로 보입니다. 사람들이 GDAL/OGR/OSR 파이썬 API를 사용하는 것을 막을 방법은 없지만, OGR 코어와 파이썬 코드 사이에 교환되는 객체는 OGR 파이썬 SWIG 객체가 아닐 것입니다.
   플러그인이 좌표계를 ``osgeo.osr.SpatialReference`` 객체가 아니라 문자열(WKT, PROJSON, 또는 퇴출된 PROJ.4 문자열)로 반환할 것이라는 것이 전형적인 예시입니다. 그러나 ``osgeo.osr.SpatialReference`` API를 사용해서 이 WKT 문자열을 생성할 수는 있습니다.

-  이 RFC는 파이썬 의존성을 관리하려 시도하지 않습니다. 필요한 ``pip install`` 또는 ``pip install`` 이 사용하는 어떤 파이썬 패키지 관리 솔루션이든 수행하는 것은 사용자의 책임입니다.

-  파이썬의 안전한 사용을 위한 요구 사항대로, 파이썬 드라이버에 파이썬 "전체 수준 해석기 잠금(Global Interpreter Lock)"을 담습니다. 결과적으로 이런 드라이버들의 축소 또는 확장이 제한됩니다.

-  이런 제약 사항들을 생각할 때, 파이썬 드라이버는 "실험적인" 기능으로 남을 것이며 GDAL 프로젝트는 GDAL 저장소에 이런 파이썬 드라이버들을 포함시키도록 허용하지 않을 것입니다. QGIS 주 저장소 외부에 파이썬 플러그인을 허용하는 QGIS 프로젝트의 상황과 유사합니다. QGIS 플러그인을 주 저장소로 옮기고자 하는 경우, C++로 변환해야만 합니다. 그 근거는 파이썬 코드의 정확성은 대부분 런타임 시 확인할 수 있는 반면 C++은 (컴파일 시 및 다른 점검자를 통해) 정적 분석의 이점을 취할 수 있다는 사실입니다.
   GDAL 맥락에서도 이 근거가 적용됩니다. `OSS-Fuzz <https://google.github.io/oss-fuzz/>`_ 가 GDAL 드라이버의 스트레스 테스트도 수행하는데, 이를 위해서는 드라이버가 C++로 작성되어 있어야 합니다.

-  GDAL이 새로운 기능을 배포하는 사이에 C++와 파이썬 코드 간 인터페이스가 망가질 수도 있습니다. 이런 경우 호환되지 않는 파이썬 드라이버를 불러오는 일을 피하기 위해 예상되는 API 버전 번호를 늘릴 것입니다. 호환되지 않는 (예전) API 버전의 플러그인과 작동할 수 있도록 하는 어떤 노력도 기울이지 않을 가능성이 큽니다.


SWIG 바인딩 변경 사항
---------------------

없음.

보안에 미치는 영향
------------------

GDAL의 기존 네이티브 코드 플러그인 메커니즘과 유사합니다. 사용자가 GDAL_PYTHON_DRIVER_PATH 또는 GDAL_DRIVER_PATH 환경 변수를 정의하고 그 안에 (또는 대비책으로서 ``{prefix}/lib/gdalplugins/python`` 에) :file:`.py` 스크립트를 넣는 경우, 스크립트를 실행할 것입니다.

하지만 GDALOpen() 또는 비슷한 메커니즘을 이용해서 :file:`.py` 파일을 열면 실행으로 이어지지 않을 것이기 때문에, 일반적인 GDAL 사용례에서는 이렇게 하는 것이 안전합니다.

네이티브 플러그인 불러오기를 비활성화시키기 위해 이미 사용되고 있는 컴파일 시의 ``#define GDAL_NO_AUTOLOAD`` 도 파이썬 플러그인 불러오기를 비활성화시킬 것입니다.

성능에 미치는 영향
------------------

검색 위치에 :file:`.py` 스크립트가 없는 경우, GDALAllRegister() 성능에 미치는 영향은 노이즈 범위 안일 것입니다.

하위 호환성
-----------

하위 호환성 문제점은 없습니다. 기능만 추가했습니다.

문서화
------

이런 파이썬 드라이버를 작성하는 방법을 설명하는 예제를 추가했습니다:
`vector_python_driver.rst <https://github.com/rouault/gdal/blob/pythondrivers/gdal/doc/source/tutorials/vector_python_driver.rst>`_

Testing
-------

앞의 파이썬 드라이버 및 몇몇 오류 사례를 테스트하기 위해 GDAL 자동 테스트 스위트를 확장할 것입니다:
`ogr_pythondrivers.py <https://github.com/rouault/gdal/blob/pythondrivers/autotest/ogr/ogr_pythondrivers.py>`_

예전 논의
---------

과거에 이 주제에 대한 논의가 있었습니다:

-  https://lists.osgeo.org/pipermail/gdal-dev/2017-April/thread.html#46526
-  https://lists.osgeo.org/pipermail/gdal-dev/2018-November/thread.html#49294

구현
----

https://github.com/rouault/gdal/tree/pythondrivers 에 구현 후보가 있습니다.

https://github.com/OSGeo/gdal/compare/master...rouault:pythondrivers

투표 이력
---------

-  이벤 루올 +1
-  유카 라흐코넨 +1
-  마테우시 워스코트(Mateusz Łoskot) +1
-  대니얼 모리셋 +1

-  션 길리스 -0

-  하워드 버틀러 +0

감사의 말
---------

`OpenGeoGroep <https://www.opengeogroep.nl/>`_ 이 이 RFC의 구현을 후원해주셨습니다.

