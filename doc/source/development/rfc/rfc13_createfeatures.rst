.. _rfc-13:

================================================================================
RFC 13: 배치 모드에서의 피처 삽입/업데이트/삭제 성능 향상
================================================================================

저자: 콘스탄틴 바우만(Konstantin Baumann)

연락처: konstantin.baumann@hpi.uni-potsdam.de

상태: 철회

철회
----

'gdal-dev' 메일링 리스트 상에서 `프랑크 바르메르담 <https://lists.osgeo.org/pipermail/gdal-dev/2007-May/013132.html>`_ 및 `세케레시 터마시 <https://lists.osgeo.org/pipermail/gdal-dev/2007-May/013130.html>`_ 가 보낸 몇몇 코멘트를 기반으로 이 RFC를 철회합니다.

요약
----

드라이버가 (하나씩 하는 대신) 한 번에 삽입, 업데이트, 또는 삭제해야 하거나 할 수 있는 온전한 피처 집합이 있다는 것을 알고 있는 경우, 일부 OGR 드라이버는 피처 집합의 삽입, 업데이트, 그리고 삭제 속도를 극적으로 높이고 최적화할 수 있습니다.

CreateFeatures()
----------------

:cpp:class:`GDALDataset` 클래스에 다음과 같은 새로운 가상 메소드를 유사한 C 함수와 함께 추가합니다:

::

   virtual OGRErr CreateFeatures( OGRFeature** papoFeatures, int iFeatureCount );

기본 구현은 다음과 같습니다:

::

   OGRErr OGRLayer::CreateFeatures(
       OGRFeature **papoFeatures,
       int iFeatureCount
   ) {
       for(int i = 0; i < iFeatureCount; ++i) {
           OGRErr error = CreateFeature( papoFeatures[i] );
           if( error != OGRERR_NONE ) return error;
       }
       return OGRERR_NONE;
   }

기본 구현은 최적화되지 않은 예전의 삽입 습성을 촉발합니다.

개별 드라이버는 기본 구현을 대체해서 피처 집합을 삽입하기 위한 최적화된 알고리즘을 구현할 수 있습니다.

SetFeatures()
-------------

:cpp:class:`GDALDataset` 클래스에 다음과 같은 새로운 가상 메소드를 유사한 C 함수와 함께 추가합니다:

::

   virtual OGRErr SetFeatures( OGRFeature** papoFeatures, int iFeatureCount );

기본 구현은 다음과 같습니다:

::

   OGRErr OGRLayer::SetFeatures(
       OGRFeature **papoFeatures,
       int iFeatureCount
   ) {
       for(int i = 0; i < iFeatureCount; ++i) {
           OGRErr error = SetFeature( papoFeatures[i] );
           if( error != OGRERR_NONE ) return error;
       }
       return OGRERR_NONE;
   }

기본 구현은 최적화되지 않은 예전의 업데이트 습성을 촉발합니다.

개별 드라이버는 기본 구현을 대체해서 피처 집합을 업데이트하기 위한 최적화된 알고리즘을 구현할 수 있습니다.

DeleteFeatures()
----------------

:cpp:class:`GDALDataset` 클래스에 다음과 같은 새로운 가상 메소드를 유사한 C 함수와 함께 추가합니다:

::

   virtual OGRErr DeleteFeatures( long *panFIDs, int iFIDCount );

기본 구현은 다음과 같습니다:

::

   OGRErr OGRLayer::DeleteFeatures(
       long *panFIDs,
       int iFIDCount
   ) {
       for(int i = 0; i < iFIDCount; ++i) {
           OGRErr error = DeleteFeature( panFIDs[i] );
           if( error != OGRERR_NONE ) return error;
       }
       return OGRERR_NONE;
   }

기본 구현은 최적화되지 않은 예전의 삭제 습성을 촉발합니다.

개별 드라이버는 기본 구현을 대체해서 피처 집합을 삭제하기 위한 최적화된 알고리즘을 구현할 수 있습니다.

C API 함수
----------

다음 C 함수를 추가합니다:

::

   OGRErr OGR_L_CreateFeatures( OGRFeature** papoFeatures, int iFeatureCount );
   OGRErr OGR_L_SetFeatures( OGRFeature** papoFeatures, int iFeatureCount );
   OGRErr OGR_L_DeleteFeatures( long* panFIDs, int iFIDCount );

하지만, SWIG 기반 래핑(wrapping) 때문에 공개 OGR 인터페이스에 평문 C 배열을 추가하는 데 조금 문제가 있습니다. 예를 들면 `세케레시 터마시가 보낸 'gdal-dev' 이메일 <https://lists.osgeo.org/pipermail/gdal-dev/2007-May/013092.html>`_ 을 읽어보십시오.

추가 메모
---------

이 새로운 인터페이스 함수를 기반으로, MySQL 드라이버에서 피처 삽입 속도를 초당 40개에서 초당 800~2,000개로 높일 수 있었습니다. 다른 드라이버들도 이 변경 사항으로 혜택을 볼 수 있을 거라 믿습니다.

#1633 티켓도 참조하십시오.

구현 계획
---------

추가 사항을 설명하기 위한 간단한 패치를 제공할 수 있습니다.

MySQL 드라이버 용 최적화 구현을 담고 있는 인터페이스를 기반으로 하는 또다른 패치를 제공할 수 있습니다.

이력
----

2007년 5월 14일: 초안 작성

2007년 5월 15일: SetFeatures() 추가

2007년 5월 16일: DeleteFeatures() 추가

2007년 5월 17일: C API 함수 추가; SWIG 래핑(wrapping) 문제점 언급

2007년 5월 23일: 'gdal-dev' 메일링 리스트 상에서의 몇몇 우려로 철회

