.. _rfc-66:

=======================================================================================
RFC 66 : OGR 임의 레이어 읽기/쓰기 케이퍼빌리티
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.2버전에 구현

요약
----

이 RFC는 레이어 수준에서 벡터 피처를 반복할 수 있는 기존 케이퍼빌리티에 추가로 데이터 수준에서 동일한 작업을 할 수 있는 새로운 API를 도입할 것을 제안합니다. 산출 케이퍼빌리티 가진 대부분의 드라이버가 지원하는, 레이어에 피처를 임의의 순서로 작성하는 기존 케이퍼빌리티를 새로운 데이터셋 케이퍼빌리티 플래그로 공식화합니다.

근거
----

일부 벡터 포맷은 서로 다른 레이어에 속한 피처들을 교차삽입 방식으로 혼합하는데, 이는 현재의 레이어별 피처 반복을 조금 비효율적으로 만듭니다. (각 레이어를 반복하기 위해 전체 파일을 읽어와야 하기 때문입니다.) 이런 드라이버의 한 예가 OSM 드라이버입니다. 이 드라이버의 경우, :cpp:func:`OGRLayer::GetNextFeature` 메소드를 사용할 수 있도록 과거에 한 가지 꼼수를 개발했지만, 이 꼼수는 정말로 특별한 의미 체계를 수반합니다. 더 자세한 내용은 :ref:`vector.osm` 의 "교차삽입 읽기" 단락을 참조하십시오.
스트리밍 방식으로 작동하기 때문에 임의 요소를 내포하는 GML 파일을 읽어와서 명백한 임의의 순서로 반환할 수 있는 새로운 GMLAS(GML Application Schemas) 드라이버의 개발 과정에서도 비슷한 필요성이 발생합니다. 예를 들어 다음과 같이 단순화된 XML 콘텐츠가 있다고 할 때:

::

   <A>
       ...
       <B>
           ...
       </B>
       ...
   </A>

이 드라이버는 피처 A를 내보내기 전에 먼저 피처 B의 작성을 완료할 수 있을 것입니다. 따라서 이 패턴의 순열을 읽어오는 경우, 드라이버가 B, A, B, A, ...라는 순서로 피처들을 내보낼 것입니다.

변경 사항
---------

C++ API
~~~~~~~

:cpp:class:`GDALDataset` 수준에 새 메소드 2개를 추가합니다:

GetNextFeature():

::

   /**
    \brief 이 데이터셋으로부터 사용할 수 있는 다음 피처를 가져옵니다.

    호출자가 반환된 피처를 OGRFeature::DestroyFeature()를 이용해서
    삭제할 책임을 집니다.

    드라이버에 따라, 이 메소드는 레이어로부터 순차적이지 않은 방식으로
    피처를 반환할 수도 있습니다. (예를 들어 OSM 및 GMLAS 드라이버의 경우)
    ODsCRandomLayerRead 케이퍼빌리티를 선언하면 이런 일이 발생할 수도
    있습니다. 데이터셋이 이 케이퍼빌리티를 선언하는 경우,
    OGRLayer::GetNextFeature() 대신 GDALDataset::GetNextFeature()를
    사용할 것을 강력하게 권장합니다. 전자가 느리고 불완전하며 버벅거리는
    구현을 가질 수도 있기 때문입니다.

    하지만 대부분의 드라이버가 각 레이어를 반복한 다음 레이어의 각 피처를
    반복하는 기본 구현을 사용할 것입니다.

    이 메소드는 반복될 레이어 상에 설정된 공간 및 속성 필터를 연산에
    넣습니다.

    ResetReading() 메소드를 사용해서 처음부터 다시 시작할 수도 있습니다.

    드라이버에 따라, 이 메소드에는 이 데이터셋의 레이어에 대해
    OGRLayer::GetNextFeature()를 호출하는 부작용이 있을 수도 있습니다.

    이 메소드는 GDALDatasetGetNextFeature() C 함수와 동일합니다.

    @param ppoBelongingLayer 객체가 속해 있는 레이어를 받는 OGRLayer*
                             변수를 가리키는 포인터, 또는 NULL입니다.
                             피처가 NULL이 아닌 경우에도 *ppoBelongingLayer의
                             산출물이 NULL일 수 있습니다.
    @param pdfProgressPct    ([0,1] 범위의) 진행 상황 백분율을 받는
                             더블형 변수를 가리키는 포인터, 또는 NULL입니다.
                             진행 상황을 판단할 수 없는 경우 반환 시 포인터가
                             가리키는 값이 음수일 수도 있습니다.
    @param pfnProgress       진행 상황을 리포트하고 (GetNextFeature() 호출의
                             경우 시간이 오래 걸릴 수도 있습니다) 취소할 수 있는
                             가능성을 제공하는 진행 상황 콜백, 또는 NULL입니다.
    @param pProgressData     pfnProgress에 제공되는 사용자 데이터, 또는 NULL입니다.
    @return 피처 하나, 또는 사용할 수 있는 피처가 더 이상 없는 경우 NULL을 반환합니다.
    @since GDAL 2.2
   */

   OGRFeature* GDALDataset::GetNextFeature( OGRLayer** ppoBelongingLayer,
                                            double* pdfProgressPct,
                                            GDALProgressFunc pfnProgress,
                                            void* pProgressData )

그리고 ResetReading():

::

   /** 
    \brief 피처 읽기를 첫 번째 피처 상에서 시작하도록 리셋합니다.

    이 메소드는 GetNextFeature()에 영향을 미칩니다.

    드라이버에 따라, 이 메소드에도 이 데이터셋의 레이어에 대해
    OGRLayer::ResetReading()을 호출하는 부작용이 있을 수도 있습니다.

    이 메소드는 GDALDatasetResetReading() C 함수와 동일합니다.
    
    @since GDAL 2.2
   */
   void        GDALDataset::ResetReading();

새로운 케이퍼빌리티
~~~~~~~~~~~~~~~~~~~

다음 새로운 데이터셋 케이퍼빌리티 2개를 추가합니다:

::

   #define ODsCRandomLayerRead     "RandomLayerRead"   /**< 임의의 레이어로부터 피처를 반환하는 GetNextFeature()를 위한 데이터셋 케이퍼빌리티 */
   #define ODsCRandomLayerWrite    "RandomLayerWrite " /**< 레이어에 대한 CreateFeature()를 임의의 순서로 지원하기 위한 데이터셋 케이퍼빌리티 */

C API
~~~~~

C API에서 앞의 새 메소드 2개를 다음과 같이 사용할 수 있습니다:

::

   OGRFeatureH CPL_DLL GDALDatasetGetNextFeature( GDALDatasetH hDS,
                                                  OGRLayerH* phBelongingLayer,
                                                  double* pdfProgressPct,
                                                  GDALProgressFunc pfnProgress,
                                                  void* pProgressData )

   void CPL_DLL GDALDatasetResetReading( GDALDatasetH hDS );

새 API의 몇몇 설계 선택에 관한 논의
-----------------------------------

:cpp:func:`OGRLayer::GetNextFeature` 와 비교했을 때, :cpp:func:`GDALDataset::GetNextFeature` 에는 차이점이 몇 가지 존재합니다:

-  피처가 속해 있는 레이어를 반환합니다. 실제로 피처로부터 해당 피처가 속해 있는 레이어를 쉽게 알아낼 수 있는 방법은 없습니다. (데이터 모델에서, 피처는 어떤 레이어든 그 바깥에 존재할 수 있기 때문입니다.) 피처의 ``OGRFeatureDefn*`` 객체를 레이어의 ``OGRFeatureDefn*`` 객체와 상호연결하는 것도 한 가지 방법이지만, 그러기에는 조금 불편합니다. (그리고 아마도 어떤 인트리 드라이버에서도 절대 발생하지 않을 일이지만 이론적으로는 레이어 여러 개가 동일한 피처 정의 객체를 공유하는 것도 상상해볼 수 있습니다.)

-  반환된 피처가 NULL이 아닌 경우에도, 반환된 레이어가 NULL일 수도 있습니다. 이는 현재로서는 일어날 수 없는 일이기 때문에 단시 하나의 규정일 뿐입니다. 기본적으로 각 피처가 명확하게 식별된 레이어에 실제로 속하지 않은 채 서로 다른 스키마를 가질 수 있는 (예를 들면 GeoJSON 같은) 스키마가 없는 데이터소스를 처리하는 경우 흥미로울 수 있습니다.

-  진행 상황 백분율을 반환합니다. OGRLayer API를 사용하는 경우, 반환된 피처의 개수를 GetFeatureCount()가 반환한 총 개수로 나누어야 합니다. 사용례를 위해 데이터셋의 피처 총 개수를 빨리 알 수 있는 방법이 없다는 것을 강조하고 싶습니다. 그러나 총 용량이라는 측면에서 파일 포인터가 파일의 어느 위치에 있는지는 쉽게 알 수 있습니다. 따라서 GetNextFeature()가 진행 상황 백분율을 반환하도록 결정했습니다. [0,1] 범위를 선택한 이유는, GDAL 진행 상황 함수가 입력받는 범위와 일치하기 때문입니다.

-  진행 상황 및 취소 콜백을 받아들입니다. GetNextFeature()가 "기초적인" 메소드이고 이미 진행 상황 백분율을 반환할 수 있는데 어째서 이런 기능이 필요한지 궁금해 할 수도 있습니다. 하지만 어떤 상황에서는 GetNextFeature() 호출을 완료하는 데 긴 시간이 걸릴 수도 있습니다. 예를 들어 OSM 드라이버의 경우, 최적화로서 사용자가 드라이버에 레이어 부분 집합의 피처를, 예를 들면 노드를 제외한 모든 레이어 피처를 반환하도록 요청할 수 있습니다. 그러나 일반적으로 노드는 파일의 시작 위치에 존재하기 때문에 첫 번째 피처를 가져오기 전에 평균적으로 전체 파일의 70%를 처리하게 됩니다.
   GMLAS 드라이버에서, 첫 번째 GetNextFeature() 호출은 도형 열의 공간 좌표계를 판단하기 위해 파일을 빠르게 예비 스캔할 수 있는 기회이기도 합니다. 따라서 진행 상황 피드백을 받는 편이 좋습니다.

진행 상황 백분율 산출물은 진행 상황 콜백 메커니즘과 중복되며, 전자를 가져오기 위해 후자를 사용할 수 있지만 조금 난해할 수도 있습니다. 다음과 같은 작업을 수행해야 할 것이기 때문입니다:

::

   int MyProgress(double pct, const char* msg, void* user_data)
   {
       *(double*)user_data = pct;
       return TRUE;
   }

   myDS->GetNextFeature(&poLayer, MyProgress, &pct)

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

GDALDatasetGetNextFeature는 gdal::Dataset::GetNextFeature()로 매핑되고 GDALDatasetResetReading은 gdal::Dataset::ResetReading()로 매핑됩니다.

gdal::Dataset::GetNextFeature()와 관련해서, 현재 파이썬만 피처와 피처가 속해 있는 레이어를 둘 다 반환하도록 수정했습니다. 현재 다른 바인딩들은 피처만 반환합니다. (수정하려면 특화된 유형 매핑이 필요할 것입니다.)

드라이버
--------

OSM 및 GMLAS 드라이버가 이 새로운 API를 구현하도록 업데이트했습니다.

ODsCRandomLayerWrite를 지원하는 기존 드라이버가 이를 노출시키도록 업데이트했습니다.
(레이어 생성 케이퍼빌리티를 지원하는 드라이버 가운데 KML, JML 및 GeoJSON 드라이버를 제외한 대부분의 드라이버를 업데이트했습니다.)

유틸리티
--------

ogr2ogr / GDALVectorTranslate()로부터 ODsCRandomLayerRead가 노출된 경우 OSM 드라이버가 새 API를 사용하도록 사용되었던 꼼수를 제거했습니다. 새 API는 산출 드라이버가 ODsCRandomLayerWrite를 노출시키는지 확인하고 노출시키지 않는 경우 경고를 발하지만 임의 레이어 읽기/쓰기를 이용해서 변환을 계속 진행시킵니다.

ogrinfo가 :cpp:func:`GDALDataset::GetNextFeature` API를 사용하도록 지시하는 "-rl" (random layer) 플래그를 받아들이도록 확장합니다. ODsCRandomLayerRead가 노출되었을 때 자동적으로 해당 플래그를 사용한다고 간주되었지만, 산출물이 꽤나 무작위적이어서 사용자에게 실용적이진 않습니다.

문서화
------

새 메소드 및 함수를 모두 문서화합니다.

테스트 스위트
-------------

OSM 및 GMLAS 드라이버의 특수 GetNextFeature() 구현을 각각 대응하는 테스트로 테스트합니다.
:cpp:func:`GDALDataset::GetNextFeature` 의 기본 구현은 MEM 드라이버 테스트로 테스트합니다.

호환성 문제점
-------------

C/C++ API 기존 사용자의 경우 호환성 문제점은 없습니다.

기본 구현이 존재하기 때문에, 특수 구현이 없는 드라이버에 대해 새로운 함수/메소드를 안전하게 사용할 수 있습니다.

새로운 :cpp:func:`GDALDataset::ResetReading` 및 :cpp:func:`GDALDataset::GetNextFeature` 가상 메소드의 추가로 인해 동일한 이름이지만 다른 의미 체계 또는 서명을 가진 메소드 이름을 이미 내부적으로 사용하고 있는 트리 외부의 드라이버에 문제점이 발생할 수도 있습니다. 몇몇 인트리(in-tree) 드라이버에서 이런 문제점을 찾아내서 수정했습니다.

구현
----

이벤 루올이 이 RFC를 구현할 것입니다. 이 구현은 새 GMLAS 드라이버의 필요성에 의해 촉발되었습니다.
(GMLAS 드라이버의 초기 개발은 `코페르니쿠스 유럽 지구 관측 프로그램 <https://www.copernicus.eu/en>`_ 의 후원으로 이루어졌습니다.)

제안한 구현은 `"gmlas randomreadwrite" 브랜치 <https://github.com/rouault/gdal2/tree/gmlas_randomreadwrite>`_ 저장소에 있습니다. (`커밋 <https://github.com/rouault/gdal2/commit/8447606d68b9fac571aa4d381181ecfffed6d72c>`_)

투표 이력
---------

-  세케레시 터마시 +1
-  하워드 버틀러 +1
-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

