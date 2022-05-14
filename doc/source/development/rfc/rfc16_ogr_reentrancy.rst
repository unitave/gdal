.. _rfc-16:

================================================================================
RFC 16: OGR 스레드 보안
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 개발 중

요약
----

OGR에서 스레드 보안을 더 잘 지원하기 위해 내부 인프라스트럭처를 업데이트하면서 메소드 몇 개를 추가합니다.

정의
----

-  **Reentrant**:
   함수의 호출이 각각 유일 데이터를 참조하는 경우 스레드 여러 개가 재진입(reentrant) 함수를 동시에 호출할 수 있습니다.

-  **Thread-safe**:
   함수의 호출이 각각 공유 데이터를 참조하는 경우 스레드 여러 개가 스레드 안전(thread-safe) 함수를 동시에 호출할 수 있습니다.

목표
----

모든 OGR 코어와 선택된 드라이버들이 재진입할 수 있도록 만들고, 드라이버 등록자(registrar), 드라이버 및 데이터소스가 적어도 잠재적으로 스레드 안전하도록 만듭니다.

TestCapability()
----------------

드라이버 및 데이터소스에 대한 :cpp:func:`TestCapability` 메소드가 특정 인스턴스에 대해 재진입성 및 스레드 보안을 테스트하는 방법을 포함하도록 확장할 것입니다. 다음 매크로들을 추가할 것입니다:

::

   #define OLCReentrant    "Reentrant"
   #define ODsCLayerClones "LayerClones"
   #define ODsCReentrant   "Reentrant"
   #define ODsCThreadSafe  "Threadsafe"

이때:

-  OLCReentrant:
   이 레이어 클래스가 재진입할 수 있습니다. 스레드 여러 개가 이 클래스의 -- 단일 데이터소스에 있는 서로 다른 레이어를 포함하는 -- 개별 인스턴스들을 작업할 수 있습니다.

-  ODsCReentrant:
   이 데이터소스 클래스가 재진입할 수 있습니다. 스레드 여러 개가 이 클래스의 개별 인스턴스들을 작업할 수 있습니다.

-  ODsCThreadSafe:
   이 데이터소스 클래스는 스레드 안전합니다. 스레드 여러 개가 이 클래스의 단일 인스턴스를 작업할 수 있습니다.

-  ODsCLayerClones:
   :cpp:func:`OGRDataSource::GetLayerClone` 메소드를 지원하며, :cpp:func:`GetLayer` 가 반환하는 기본 레이어로부터 나온 개별 상태(distinct state)를 가진 레이어 인스턴스를 반환합니다.

레이어 피처 읽기 상태가 레이어 객체에 내재되어 있는 한 단일 레이어 인스턴스가 스레드 안전할 수 없다는 사실을 기억하십시오.
모든 테스트 값에 대한 기본 반환값은 FALSE입니다. 이는 :cpp:func:`TestCapability` 메소드의 경우 일반적인 습성이지만, 드라이버 데이터소스 또는 레이어가 사실상 재진입 가능하고 그리고/또는 스레드 안전하다고 결정한 특정 드라이버들은 TRUE를 반환할 수 있습니다.

OGRSFDriverRegistrar
--------------------

주로 드라이버 등록자에 대한 작업을 뮤텍스(mutex)로 보호함으로써 드라이버 등록자를 스레드 안전하게 만들기 위한 여러 가지 변경 사항들이 이미 적용되어 있습니다.

OGRSFDriver
-----------

스레드 안전을 위해 :cpp:class:`OGRSFDriver` 기반 클래스를 변경할 필요는 없습니다. 이 클래스가 거의 아무 일도 하지 않기 때문입니다.

OGRDataSource
-------------

:cpp:class:`OGRDataSource` 클래스가 'm_hMutex' 클래스 데이터 멤버를 포함하도록 수정되었습니다. 'm_hMutex' 멤버는 레이어 목록 같은 내부 데이터 구조에 스레드 안전하게 접근하기 위해 사용되는 뮤텍스입니다. :cpp:class:`OGRDataSource` 로부터 파생된, 스레드 안전 작업을 구현하려는 클래스들은 배타성(exclusivity)이 요구되는 경우 이 뮤텍스를 사용해야 합니다.

이 클래스에 새 메소드를 추가합니다:

::

     OGRLayer *GetLayerClone( int i );

이 메소드의 기본 구현은 NULL을 반환합니다. 데이터소스에 대해 :cpp:class:`ODsCLayerClones` 케이퍼빌리티가 참인 경우, 이 메소드는 개별 피처 읽기 상태를 가지고 있는 요청 레이어의 복제본을 반환해야만 합니다.
즉 이 복제본이 자신만의 공간 및 속성 필터 설정을 가질 수 있으며, (:cpp:func:`GetNextFeature` 및 :cpp:func:`ResetReading` 메소드를 위한) 내부 피처 반복자(iterator)가 동일한 기저 데이터소스 레이어를 참조하는 다른 :cpp:class:`OGRLayer` 인스턴스와 구분된다는 의미입니다.

멀티스레딩 맥락에서 이 메소드의 목적은 서로 다른 스레드들이 개별 읽기 상태를 가진 레이어의 복제본을 가질 수 있게 하는 것입니다. 실제로는 재진입성에 불과하지만, 일종의 빈약한 스레드 안전성입니다.

:cpp:func:`ExecuteSQL` 이 반환한 레이어와 마찬가지로, :cpp:func:`GetLayerClone` 이 반환한 레이어를 :cpp:func:`OGRDataSource::ReleaseResultSet` 메소드로 해제해야 합니다.

ExecuteSQL()
------------

:cpp:func:`OGRDataSource::ExecuteSQL` 의 기본 OGR 구현은 내부적으로 레이어 상태(피처 반복자 및 필터)를 사용하고 수정합니다. 따라서 자신의 개별 레이어가 스레드 안전하지 않다는 것을 알고 있더라도 스레드 안전하도록 시도하는 데이터소스에 이 구현을 사용하는 것은 적절하지 않습니다.

데이터소스가 :cpp:func:`GetLayerClone` 을 지원하는 경우 이 코드가 :cpp:func:`GetLayerClone` 을 사용하도록 수정할 것을 제안합니다.

테스트
------

재진입성 및 스레드 안전을 지원한다고 주장하는 데이터소스의 읽기 전용 스트레스 테스트를 위해 멀티스레딩 C++ 테스트 코드를 구현할 것입니다.

회귀 테스트 스위트(gdalautotest)에는 어떤 재진입성 및 스레드 안전 테스트도 통합하지 않을 것입니다. 실용성이 없는 것으로 보이기 때문입니다.

구현
----

프랑크 바르메르담이 GDAL/OGR 1.5.0버전 배포판을 위해 이 RFC의 모든 핵심 기능을 구현할 것입니다. 또한 Shapefile, 개인 지리 데이터베이스(Personal Geodatabase), ODBC 및 Oracle 드라이버에도 :cpp:class:`OLCReentrant`, :cpp:class:`ODsCLayerClones`, :cpp:class:`ODsCReentrant` 및 :cpp:class:`ODsThreadSafe` 를 구현할 것입니다.

