.. _vector_data_model:

================================================================================
벡터 데이터 모델
================================================================================

이 문서에서는 OGR 클래스를 설명하려 합니다. OGR 클래스는 일반적이지만 (OLE DB 또는 COM 또는 윈도우에 특화되지 않았지만) OLE DB 제공자 지원은 물론 SFCOM 용 클라이언트 쪽 지원을 구현하기 위한 기반으로 사용됩니다. 예를 들어 SFCORBA 구현이, 또는 오픈GIS 단순 피처에서 영감을 받은 API를 사용하고자 하는 C++ 프로그램이 직접 이런 동일 OGR 클래스를 사용할 수 있게 하려는 목적입니다.

OGR 클래스가 오픈GIS 단순 피처 데이터 모델을 기반으로 하기 때문에, SFCOM 또는 OGC(Open Geospatial Consortium) 웹사이트로부터 가져올 수 있는 다른 단순 피처 인터페이스 사양들을 검토해보는 것이 매우 도움이 될 것입니다. 데이터 유형 및 메소드 이름도 인터페이스 사양의 데이터 유형 및 메소드 이름에 기반을 두고 있습니다.

클래스 개요
--------------

- 도형(:ref:`ogr_geometry.h <ogrgeometry_cpp>`):
  (:cpp:class:`OGRGeometry` 등의) 도형 클래스는 오픈GIS 모델 벡터 데이터를 요약하는 것은 물론, 몇몇 도형 작업을 제공하고 WKT 및 텍스트 포맷을 서로 변환합니다. 도형은 좌표계(투영법)를 포함합니다.

- 공간 좌표계(:ref:`ogr_spatialref.h <ogrspatialref>`):
  :cpp:class:`OGRSpatialReference` 클래스는 투영법 및 원점(datum)의 정의를 요약합니다.

- 피처(:ref:`ogr_feature.h <ogrfeature_cpp>`):
  :cpp:class:`OGRFeature` 클래스는 도형 및 속성 집합이라는 전체 피처의 정의를 요약합니다.

- 피처 클래스 정의(:ref:`ogr_feature.h <ogrfeature_cpp>`):
  :cpp:class:`OGRFeatureDefn` 클래스는 연결된 피처 그룹의 (일반적으로 전체 레이어의) 스키마(필드 정의 집합)를 수집합니다.

- 레이어(:ref:`ogrsf_frmts.h <ogrlayer_cpp>`):
  :cpp:class:`OGRLayer` 클래스는 GDALDataset에 있는 피처 레이어를 표현하는 추상 기반(base) 클래스입니다.

- 데이터셋(:ref:`gdal_priv.h <gdaldataset_cpp>`):
  :cpp:class:`GDALDataset` 클래스는 OGRLayer 객체(object)를 하나 이상 담고 있는 파일 또는 데이터베이스를 표현하는 추상 기반(base) 클래스입니다.

- 드라이버(:ref:`gdal_priv.h <gdaldriver_cpp>`):
  :cpp:class:`GDALDriver` 클래스는 GDALDataset 객체를 열기 위한 특정 포맷 변환기(translator)를 표현합니다. GDALDriverManager가 사용할 수 있는 모든 드라이버를 관리합니다.

도형
--------

도형 클래스는 여러 유형의 벡터 도형을 표현합니다. 모든 도형 클래스는 모든 도형의 공통 서비스를 정의하는 :cpp:class:`OGRGeometry` 로부터 파생됩니다. 도형 유형에는 :cpp:class:`OGRPoint`, :cpp:class:`OGRLineString`, :cpp:class:`OGRPolygon`, :cpp:class:`OGRGeometryCollection`, :cpp:class:`OGRMultiPolygon`, :cpp:class:`OGRMultiPoint`, 및 :cpp:class:`OGRMultiLineString` 이 포함됩니다.

이런 도형 유형들은 :cpp:class:`OGRCircularString`, :cpp:class:`OGRCompoundCurve`, :cpp:class:`OGRCurvePolygon`, :cpp:class:`OGRMultiCurve` 및 :cpp:class:`OGRMultiSurface` 클래스를 가지는 비선형 도형들로 확장됩니다.

추가적인 중간(intermediate) 추상 기반 클래스는 다른 도형 유형들이 결국 구현하게 될 기능을 담고 있습니다. 이 기능에는 (OGRLineString의 기반 클래스인) OGRCurve와 (OGRPolygon의 기반 클래스인) OGRSurface가 포함됩니다. 몇몇 중간 인터페이스들은 단순 피처 추상 모델을 기반으로 하며, 현재 OGR에서 SFCOM은 모델링되지 않았습니다. 대부분의 경우 메소드를 다른 클래스로 집계합니다.

:cpp:class:`OGRGeometryFactory` 클래스를 사용해서 WKT 및 WKB 포맷 데이터를 도형으로 변환합니다. WKT 및 WKB는 모든 단순 피처 도형 유형을 표현하기 위해 사전 정의된 아스키 및 바이너리 포맷입니다.

SFCOM의 도형 객체를 기반으로 하는 방식으로, OGRGeometry에는 해당 도형의 공간 좌표계를 정의하는 :cpp:class:`OGRSpatialReference` 객체를 가리키는 참조가 포함됩니다. 이 참조는 일반적으로 해당 공간 좌표계를 사용하는 각 OGRGeometry 객체에 대한 참조를 집계하는 공유 공간 좌표계 객체를 가리킵니다.

OGRGeometry에 대한 (중첩 등등을 계산하는) 많은 공간 분석 메소드는 아직 구현되지 않았습니다.

기존 OGRGeometry 클래스로부터 다른 많은 특정 도형 클래스를 파생시키는 것은 이론적으로 가능하지만, 제대로 숙고된 측면은 아닙니다. 특히 OGRGeometryFactory 클래스를 이용해서 OGRGeometryFactory를 수정하지 않고 특수 클래스를 생성할 수는 있을 것입니다.

비선형 도형의 호환성 문제점
++++++++++++++++++++++++++++++++++++++++++++++++

비선형 도형을 지원하지 않는 드라이버의 레이어에 있는 비선형 도형을 가진 피처를 생성하거나 수정할 수 있도록 도입된 일반 메커니즘은 해당 도형을 가장 근접하게 일치하는 선형 도형으로 변환할 것입니다.

다른 한편으로는 OGR C API로부터 데이터를 가져올 때, 필요한 경우 :cpp:func:`OGRSetNonLinearGeometriesEnabledFlag` 함수를 사용해서 반환되는 도형 및 레이어 도형 유형을 가장 근접하게 일치하는 선형 도형으로 변환할 수 있습니다.

공간 좌표계
-----------------

:cpp:class:`OGRSpatialReference` 클래스는 오픈GIS 공간 좌표계 정의를 저장합니다. 현재 로컬, 지리 및 투영 좌표계를 지원합니다. 최신 GDAL 버전들에서는 수직 좌표계, 측지 좌표계 및 복합(수평+수직) 좌표계도 지원합니다.

오픈GIS WKT 포맷으로부터 공간 좌표계 데이터 모델을 상속받습니다. 단순 피처 사양에 이에 대한 간단한 형식이 정의되어 있습니다. 좌표 변환(Coordinate Transformation) 사양에서 더 복잡한 형식을 찾아볼 수 있습니다. OGRSpatialReference는 좌표 변환 사양을 기반으로 작성되지만 이전 버전들의 단순 피처 형식과 호환되려는 의도를 가지고 있습니다.

다른 좌표계들을 서로 변환하기 위한 PROJ 사용을 요약하는 관련 :cpp:class:`OGRCoordinateTransformation` 클래스도 있습니다. OGRSpatialReference 클래스의 사용법을 설명하는 예제가 존재합니다.

객체 / 객체 정의
----------------------------

:cpp:class:`OGRGeometry` 클래스는 벡터 피처의 도형을, 피처의 공간 위치/영역을 수집합니다. :cpp:class:`OGRFeature` 클래스가 이 도형을 담고 있으며, 피처 속성, 피처ID, 그리고 피처 클래스 식별자를 추가합니다. OGRFeature 하나에 도형 여러 개를 연결할 수 있습니다.

:cpp:class:`OGRFeatureDefn` 클래스로 속성 집합(:cpp:class:`OGRFieldDefn`), 속성 유형, 이름 등등을 표현합니다. 일반적으로 피처 레이어 하나 당 OGRFeatureDefn 클래스 하나가 존재합니다. 해당 유형의 (또는 피처 클래스의) 피처를 가리키는 참조를 집계하는 방식으로 동일한 정의를 공유합니다.

피처의 피처ID(FID)는 피처가 속해 있는 레이어 안에서 해당 피처를 유일하게 식별하기 위한 것입니다. 독립형 피처, 또는 아직 레이어에 작성되지 않은 피처는 NULL(OGRNullFID) 피처ID를 가질 수도 있습니다. OGR에서 피처ID는 64비트 정수형 기반입니다. 하지만 64비트 정수형은 일부 포맷에서 네이티브한 피처ID를 제대로 표현하지 못 하는 경우도 있습니다. 예를 들면 GML의 피처ID는 문자열입니다.

피처 클래스는 해당 피처 클래스에 허용되는 도형 유형의 지시자(indicator)도 담고 있습니다. (이 표시자는 :cpp:func:`OGRFeatureDefn::GetGeomType` 함수로부터 OGRwkbGeometryType으로 반환됩니다.) 이 표시자가 wkbUnknown인 경우 모든 도형 유형을 사용할 수 있습니다. 어떤 레이어에 있는 피처들이 항상 공통 속성 스키마를 공유할 테지만, 서로 다른 도형 유형일 수도 있다는 사실을 의미합니다.

피처 클래스에 도형 필드 (:cpp:class:`OGRGeomFieldDefn`) 여러 개를 연결할 수 있습니다. 각 도형 필드는 :cpp:func:`OGRGeomFieldDefn::GetType` 함수가 반환하는 자신만의 허용 도형 유형 지시자와 :cpp:func:`OGRGeomFieldDefn::GetSpatialRef` 함수가 반환하는 공간 좌표계를 가집니다.

OGRFeatureDefn 클래스는 (일반적으로 레이어 이름으로 사용되는) 피처 클래스 이름도 담고 있습니다.

레이어
-----

:cpp:class:`OGRLayer` 클래스는 데이터소스 안에 있는 피처 레이어를 표현합니다. OGRLayer에 있는 모든 피처는 공통 스키마를 공유하며 동일한 :cpp:class:`OGRFeatureDefn` 클래스입니다. OGRLayer 클래스는 데이터소스로부터 피처를 읽어오기 위한 메소드도 담고 있습니다. OGRLayer를 일반적으로 파일 포맷인 기저 데이터소스로부터 피처를 읽고 쓰기 위한 게이트웨이로 생각해도 됩니다. SFCOM 및 다른 테이블 기반 단순 피처 구현에서 OGRLayer는 공간 테이블로 표현됩니다.

OGRLayer에는 순차 및 임의 읽기 및 쓰기를 위한 메소드가 포함됩니다. (:cpp:func:`OGRLayer::GetNextFeature` 메소드를 통한) 읽기 접근은 일반적으로 모든 피처를 한 번에 하나씩 순차적으로 읽어옵니다. 하지만 OGRLayer에 (:cpp:func:`OGRLayer::SetSpatialFilter` 메소드를 통해) 공간 필터를 설치하면 특정 지리 영역과 교차하는 피처만 반환하도록 제한할 수 있습니다. 속성에 대한 필터는 :cpp:func:`OGRLayer::SetAttributeFilter` 메소드로만 설정할 수 있습니다.

GDAL 3.6버전부터, ``GetNextFeature`` 를 통해 피처를 가져오는 대신 :cpp:func:`OGRLayer::GetArrowStream` 메소드를 사용해서 열 지향 메모리 레이아웃을 가진 배치(batch)로 가져올 수도 있습니다. (참고: :ref:`vector_api_tut_arrow_stream`)

현재 OGR 아키텍처에 존재하는 한 가지 결함은 공간 필터 및 속성 필터가 데이터소스에 있는 어떤 레이어를 유일하게 대표하기 위한 OGRLayer 상에 직접 설정된다는 점입니다. 즉 한 번에 서로 다른 공간 필터를 각각 가진 읽기 작업 여러 개를 수행할 수 없다는 뜻입니다.

.. note:: 향후 :cpp:class:`OGRLayerView` 또는 이와 유사한 클래스를 도입하기 위해 이런 측면을 수정할 수도 있습니다.

떠올릴 수도 있는 또다른 질문은 어째서 OGRLayer와 OGRFeatureDefn 클래스가 구별되느냐입니다. OGRLayer 클래스와 OGRFeatureDefn 클래스는 항상 일대일 관계이기 때문에, 어째서 두 클래스를 합치면 안 되느냐라는 질문 말입니다. 두 가지 이유가 있습니다:

- 이제 OGRFeature와 OGRFeatureDefn이 OGRLayer를 의존하지 않는다고 정의되었기 때문에, 이 두 클래스가 데이터소스에 있는 특정 레이어에 상관없이 메모리에 독립적으로 존재할 수 있습니다.

- SFCORBA 모델은 SFCOM 및 SFSQL 모델과는 다르게 단일 고정 스키마를 가진 레이어라는 개념을 가지고 있지 않습니다. 피처가 현재 피처 그룹에 직접 연결되지 않을 가능성이 있는 피처 집합에 속해 있다는 사실이 OGR를 이용해서 SFCORBA 지원을 구현하는 데 중요할 수도 있습니다.

OGRLayer 클래스는 추상 기반 클래스입니다. OGRLayer 클래스를 구현하는 각 파일 포맷 드라이버별로 하위 클래스로 구현될 것으로 예상됩니다. OGRLayer는 일반적으로 해당 OGRLayer의 :cpp:class:`GDALDataset` 클래스가 직접 소유하며, 직접 인스턴스화되거나 삭제되지 않습니다.

데이터셋
-------

:cpp:class:`GDALDataset` 클래스는 OGRLayer 객체 집합을 표현합니다. 이 클래스는 일반적으로 단일 파일, 파일 집합, 데이터베이스 또는 게이트웨이를 표현합니다. GDALDataset은 자신이 소유하고 있지만 그를 가리키는 참조를 반환할 수 있는 :cpp:class:`OGRLayer` 목록을 가집니다.

GDALDataset 클래스는 추상 기반 클래스입니다. GDALDataset 클래스를 구현하는 각 파일 포맷 드라이버별로 하위 클래스로 구현될 것으로 예상됩니다. 일반적으로 GDALDataset 객체를 직접 인스턴스화하지 않지만, :cpp:class:`GDALDriver` 를 이용해서 인스턴스화하는 경우가 많습니다. GDALDataset을 삭제하면 기저 영구 데이터소스에의 접근이 종료되지만, 일반적으로 해당 파일을 정말로 삭제하지는 않습니다.

GDALDataset은 GDALDriver로 데이터소스를 다시 여는 데 사용할 수 있는 (보통 파일명인) 이름을 가집니다.

GDALDataset은 일반적으로 SQL 형식의 데이터소스 특화 명령어를 실행할 수 있도록 지원합니다. :cpp:func:`GDALDataset::ExecuteSQL` 메소드를 통해 SQL 명령어를 실행합니다. (PostGIS 또는 오라클 같은) 일부 데이터소스가 기저 데이터베이스를 통해 SQL을 전송하는 반면, OGR는 어떤 데이터소스 대상으로도 SQL SELECT 문의 부분 집합을 평가할 수 있도록 지원합니다.

드라이버
-------

지원하는 각 파일 포맷에 대해 :cpp:class:`GDALDriver` 객체를 인스턴스화합니다. GDALDriver 객체는 일반적으로 새 데이터셋을 열기 위해 사용되는 단독(singleton) 클래스인 GDALDriverManager를 통해 등록됩니다.

이는 새 GDALDriver 객체를 인스턴스화하고 지원할 각 파일 포맷에 대해 (파일 포맷 특화 GDALDataset 및 OGRLayer 클래스와 함께) Identify(), Open() 같은 작업용 함수 포인터를 정의하기 위해서입니다.

응용 프로그램 구동 시 일반적으로 원하는 파일 포맷별로 등록 함수를 호출합니다. 이 함수가 적절한 GDALDriver 객체를 인스턴스화하고 GDALDriverManager를 통해 등록합니다. 데이터셋을 여는 경우, 드라이버 관리자는 일반적으로 GDALDataset 가운데 하나가 성공해서 GDALDataset 객체를 반환할 때까지 각 GDALDataset을 차례로 시도할 것입니다.

