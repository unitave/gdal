.. _rfc-40:

=======================================================================================
RFC 40: 대용량 테이블을 위한 래스터 속성 테이블 구현의 성능 개선
=======================================================================================

요약
----

일부 응용 프로그램의 (특히 분할(segmentation)의) 래스터 속성 테이블은 매우 대용량일 수 있으며, 한 번에 하나의 요소만 읽거나 쓸 수 있는 방식 때문에 현재 API로 접근하는 경우 매우 느립니다. 또한 응용 프로그램이 속성 테이블을 요청하는 경우 전체 테이블을 읽어와야만 합니다 -- 디스크로부터 요청한 부분 집합만 읽어올 수 있도록 이를 지연시킬 방법이 없습니다. 이 RFC가 제안하는 변경 사항들은 래스터 데이터에 접근하는 방식과 더 비슷한 방식으로 속성 테이블 지원을 개선할 것입니다.

구현
----

:cpp:class:`GDALRasterAttributeTable` 클래스를 가상 기본 클래스로 재작성할 것을 제안합니다. 이렇게 하면 드라이버가 요청받는 경우에만 읽고 쓰도록 하는 드라이버 각자의 구현을 가질 수 있게 될 것입니다. GDAL 1.x 버전 :cpp:class:`GDALRasterAttributeTable` 의 (예를 들어 메모리에 모든 데이터를 담을 수 있는) 기능을 제공하는 새 파생 클래스 :cpp:class:`GDALDefaultRasterAttributeTable` 을 제공할 것입니다.

:cpp:class:`GDALRasterAttributeTable` 클래스에 호출 한번으로 열의 데이터 '덩어리(chunk)'를 읽거나 작성할 수 있도록 해주는 추가 메소드들을 제공할 것입니다. :cpp:func:`GetValueAs` 함수와 마찬가지로, 적절한 변환이 수행되는 경우 서로 다른 유형의 열들을 서로 다른 유형의 값으로 (예를 들면 정수형 열을 더블형으로) 읽을 수 있습니다. 다음과 같은 오버로드(overloaded) 메소드들을 사용할 수 있을 것입니다:

::

   CPLErr ValuesIO(GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, double *pdfData);
   CPLErr ValuesIO(GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, int *pnData);
   CPLErr ValuesIO(GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, char **papszStrList);

응용 프로그램이 읽기에 필요한 공간을 RasterIO() 호출과 동일한 방식으로 할당할 것으로 예상됩니다.

문자열 읽기 및 쓰기에 ``char**`` 유형을 사용할 것입니다. 스트링을 읽어오는 경우, 배열을 올바른 크기로 생성하고 ``ValuesIO`` 가 각 행에 대한 개별 문자열을 생성할 것으로 예상됩니다. 응용 프로그램은 배열을 할당 해제하기 전에 각 문자열에 대해 ``CPLFree`` 를 호출해야 합니다.

C에서는 이 메소드들을 ``GDALRATValuesIOAsDouble``, ``GDALRATValuesIOAsInteger`` 및 ``GDALRATValuesIOAsString`` 으로 사용할 수 있을 것입니다.

속성 테이블에서 사용되지 않는 GetRowMin(), GetRowMax() 및 GetColorOfValue() 같은 함수들을 제거할 수 있는 기회이기도 합니다.

언어 바인딩
-----------

유형을 적절하게 캐스트한 데이터에 대해 NumPy 배열을 사용해서 ``ValuesIO`` 를 지원하도록 파이썬 바인딩을 수정할 것입니다. 문자열 배열에 대해 NumPy 지원을 사용해서 문자열을 지원할 것입니다.

하위 호환성
-----------

C API에 제안하는 추가 사항들을 추가할 것입니다. 하지만 C++ 바이너리 인터페이스가 망가질 것이기 때문에, GDAL 2.0버전이 이 변경 사항들을 도입하기에 적당한 시기라고 제안합니다.

기존 코드가 Clone() 및 Serialize() 함수들을 호출하기 때문에 :cpp:class:`GDALRasterAttributeTable` 클래스의 파생 구현에 있는 Clone() 및 Serialize() 함수들을 계속 지원할 수 있도록 주의를 기울여야 할 것입니다. 테이블이 메모리에 담기지 않는 구현에서는 테이블이 적합한 제한 용량(예를 들면 ``GetRowCount() * GetColCount() < 1,000,000``)보다 클 경우 실패할 수도 있습니다. 객체들 간의 메모리 공유 문제를 방지하기 위해, Clone()은  :cpp:class:`GDALDefaultRasterAttributeTable` 의 인스턴스를 반환해야 합니다.

메모리 구현이 여전히 필요한 경우, 기존 코드가 :cpp:class:`GDALRasterAttributeTable` 대신 :cpp:class:`GDALDefaultRasterAttributeTable` 의 인스턴스를 사용/생성하도록 수정해야 할 수도 있습니다.

드라이버에 미치는 영향
----------------------

HFA 드라이버가 새 함수 및 요청 시 읽기/쓰기 같은 새 인터페이스의 모든 측면을 지원하도록 업데이트할 것입니다.
다른 드라이버들은 인메모리(in-memory) 구현(:cpp:class:`GDALDefaultRasterAttributeTable`)을 계속 사용하도록 수정할 것입니다.

테스트
------

파이썬 자동 테스트 스위트에 새 API에 대한 -- 기본 구현과 HFA 드라이버에 특화된 구현 둘 다에 대한 -- 테스트를 추가할 것입니다.

타임라인
--------

샘 길링엄(Sam Gillingham)과 피트 번팅(Pete Bunting)이 필요한 작업을 수행하고 이를 GDAL 1.11버전에 포함시킬 준비가 되어 있습니다.
이 메소드들의 이름과 내부 로직에 대한 논의가 필요합니다.

티켓
----

이 RFC의 진행 상황을 추적하기 위한 #5129 티켓을 열었습니다.

