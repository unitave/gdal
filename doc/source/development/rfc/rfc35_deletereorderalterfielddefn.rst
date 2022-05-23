.. _rfc-35:

================================================================================
RFC 35: OGR 레이어 필드 정의 삭제, 재정렬 및 수정
================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인

요약
----

이 RFC는 OGR 레이어 정의에 있는 필드를 삭제하고, 필드를 재정렬하며, 필드 정의를 수정할 수 있는 케이퍼빌리티를 추가해서 OGR를 변경할 것을 제안합니다.

근거
----

현재 :cpp:func:`OGRLayer::CreateField` 메소드로 새 필드 정의를 추가해야만 OGR 레이어 정의를 수정할 수 있습니다.

기존 레이어의 필드 정의를 삭제, 재정렬 및 수정할 수 있도록 OGR 케이퍼빌리티를 확장하는 것이 바람직합니다. #2671 티켓에서 이런 바람을 표하고 있으며, QGIS 메일링 리스트에도 정기적으로 이런 요청이 (예: `http://lists.osgeo.org/pipermail/qgis-user/2011-May/011935.html <http://lists.osgeo.org/pipermail/qgis-user/2011-May/011935.html>`_) 들어오고 있습니다. QGIS는 현재 DeleteField() 메소드가 없는 문제를 "테이블 관리자" 확장 사양으로 메꾸고 있기 때문에, 제대로 된 해결책이 분명히 필요합니다.

계획된 변경 사항
----------------

:cpp:class:`OGRLayer` 클래스를 다음 메소드들로 확장할 것입니다:

.. code-block:: cpp

       virtual OGRErr      DeleteField( int iField );
       virtual OGRErr      ReorderFields( int* panMap );
       virtual OGRErr      AlterFieldDefn( int iField, OGRFieldDefn* poNewFieldDefn, int nFlags );

       /* 가상 아님: ReorderFields() 용 간이 래퍼(wrapper)  */
       OGRErr              ReorderField( int iOldFieldPos, int iNewFieldPos );

다음은 이 새 메소드들에 대한 문서입니다:

::


   /*
   \fn OGRErr OGRLayer::DeleteField( int iField );

   \brief 레이어 상에 있는 기존 필드를 삭제합니다.

   이 메소드는 실제 레이어 상에 있는 기존 필드를 삭제하기 위해 사용해야만 합니다.
   삭제된 필드를 반영하기 위해 레이어의 OGRFeatureDefn을 내부적으로 업데이트할
   것입니다. 응용 프로그램이 레이어가 사용하는 OGRFeatureDefn을 직접 수정해서는
   절대로 안 됩니다.

   이전 레이어 정의로 가져오거나 생성했던 피처 객체가 존재하는 동안 이 메소드를
   호출해서는 안 됩니다.

   모든 드라이버가 이 메소드를 지원하지는 않습니다. OLCDeleteField 케이퍼빌리티로
   레이어를 쿼리해서 드라이버가 이 메소드를 지원하는지 확인할 수 있습니다.
   몇몇 드라이버는 레이어에 아직 아무 피처도 없는 동안에만 이 메소드를 지원할 수도
   있습니다. 드라이버가 이 메소드를 지원하는 경우, 그에 따라 기저 파일/
   데이터베이스의 기존 피처들을 업데이트해야 합니다.

   이 함수는 OGR_L_DeleteField() C 함수와 동일합니다.

   @param iField 삭제할 필드의 색인입니다.

   @return 성공 시 OGRERR_NONE을 반환합니다.

   @since OGR 1.9.0
   */

   /*
   \fn OGRErr OGRLayer::ReorderFields( int* panMap );

   \brief 레이어의 모든 필드들을 재정렬합니다.

   이 메소드는 실제 레이어 상에 있는 기존 필드들을 재정렬하기 위해 사용해야만
   합니다. 필드들의 재정렬을 반영하기 위해 레이어의 OGRFeatureDefn을 내부적으로
   업데이트할 것입니다. 응용 프로그램이 레이어가 사용하는 OGRFeatureDefn을 직접
   수정해서는 절대로 안 됩니다.

   이전 레이어 정의로 가져오거나 생성했던 피처 객체가 존재하는 동안 이 메소드를
   호출해서는 안 됩니다.

   panMap 파라미터의 의미는, 각 필드 정의의 재정렬 전 위치가 panMap[i]인 경우
   재정렬 후 위치가 i입니다.

   예를 들어 필드들이 초기에 "0","1","2","3","4"이었다면
   ReorderFields([0,2,3,1,4])가 필드들을 "0","2","3","1","4"로 재정렬합니다.

   모든 드라이버가 이 메소드를 지원하지는 않습니다. OLCReorderFields 케이퍼빌리티로
   레이어를 쿼리해서 드라이버가 이 메소드를 지원하는지 확인할 수 있습니다.
   몇몇 드라이버는 레이어에 아직 아무 피처도 없는 동안에만 이 메소드를 지원할 수도
   있습니다. 드라이버가 이 메소드를 지원하는 경우, 그에 따라 기저 파일/
   데이터베이스의 기존 피처들을 업데이트해야 합니다.

   이 함수는 OGR_L_ReorderFields() C 함수와 동일합니다.

   @param panMap [0, GetLayerDefn()->GetFieldCount()-1] 순열인
                 GetLayerDefn()->GetFieldCount() 요소들의 배열입니다.

   @return 성공 시 OGRERR_NONE을 반환합니다.

   @since OGR 1.9.0
   */

   /*
   \fn OGRErr OGRLayer::ReorderField( int iOldFieldPos, int iNewFieldPos );

   \brief 레이어 상의 기존 필드를 재정렬합니다.

   이 메소드는 단일 필드를 이동시키는 데 특화된 ReorderFields()의 간이 래퍼입니다.
   가상 메소드가 아니기 때문에 드라이버에 ReorderFields()를 대신 구현해야 합니다.

   이 메소드는 실제 레이어 상에 있는 기존 필드를 재정렬하기 위해 사용해야만
   합니다. 필드의 재정렬을 반영하기 위해 레이어의 OGRFeatureDefn을 내부적으로
   업데이트할 것입니다. 응용 프로그램이 레이어가 사용하는 OGRFeatureDefn을 직접
   수정해서는 절대로 안 됩니다.

   이전 레이어 정의로 가져오거나 생성했던 피처 객체가 존재하는 동안 이 메소드를
   호출해서는 안 됩니다.

   초기 위치 iOldFieldPos에 있던 필드 정의를 iNewFieldPos 위치로 이동시킬 것이며,
   그에 맞춰 그 사이에 있는 요소들을 움직일 것입니다.

   예를 들어 필드들이 초기에 "0","1","2","3","4"이었다면
   ReorderField(1, 3)이 필드들을 "0","2","3","1","4"로 재정렬합니다.

   모든 드라이버가 이 메소드를 지원하지는 않습니다. OLCReorderFields 케이퍼빌리티로
   레이어를 쿼리해서 드라이버가 이 메소드를 지원하는지 확인할 수 있습니다.
   몇몇 드라이버는 레이어에 아직 아무 피처도 없는 동안에만 이 메소드를 지원할 수도
   있습니다. 드라이버가 이 메소드를 지원하는 경우, 그에 따라 기저 파일/
   데이터베이스의 기존 피처들을 업데이트해야 합니다.

   이 함수는 OGR_L_ReorderField() C 함수와 동일합니다.

   @param iOldFieldPos 이동시킬 필드의 이전 위치입니다.
                       [0,GetFieldCount()-1] 범위 안이어야만 합니다.
   @param iNewFieldPos 이동시킬 필드의 새 위치입니다.
                       [0,GetFieldCount()-1] 범위 안이어야만 합니다.
   @return 성공 시 OGRERR_NONE을 반환합니다.

   @since OGR 1.9.0
   */

   /*
   \fn OGRErr OGRLayer::AlterFieldDefn( int iField, OGRFieldDefn* poNewFieldDefn, int nFlags );

   \brief 레이어 상에 있는 기존 필드의 정의를 수정합니다.

   이 메소드는 실제 레이어 상에 있는 기존 필드의 정의를 수정하기 위해 사용해야만
   합니다. 수정된 필드를 반영하기 위해 레이어의 OGRFeatureDefn을 내부적으로
   업데이트할 것입니다. 응용 프로그램이 레이어가 사용하는 OGRFeatureDefn을 직접
   수정해서는 절대로 안 됩니다.

   이전 레이어 정의로 가져오거나 생성했던 피처 객체가 존재하는 동안 이 메소드를
   호출해서는 안 됩니다.

   모든 드라이버가 이 메소드를 지원하지는 않습니다. OLCAlterFieldDefn 케이퍼빌리티로
   레이어를 쿼리해서 드라이버가 이 메소드를 지원하는지 확인할 수 있습니다.
   몇몇 드라이버는 레이어에 아직 아무 피처도 없는 동안에만 이 메소드를 지원할 수도
   있습니다. 드라이버가 이 메소드를 지원하는 경우, 그에 따라 기저 파일/
   데이터베이스의 기존 피처들을 업데이트해야 합니다. 일부 드라이버는 모든 업데이트
   플래그를 지원하지 않을 수도 있습니다.

   이 함수는 OGR_L_AlterFieldDefn() C 함수와 동일합니다.

   @param iField 필드 정의를 수정해야만 하는 필드의 색인입니다.
   @param poNewFieldDefn 새 필드 정의입니다.
   @param nFlags ALTER_NAME_FLAG, ALTER_TYPE_FLAG 및 ALTER_WIDTH_PRECISION_FLAG 조합을
                 이용해서 새 필드 정의의 이름 그리고/또는 유형 그리고/또는 길이 및 정밀도
                 가운데 고려해야만 하는 사항을 나타냅니다.

   @return 성공 시 OGRERR_NONE을 반환합니다.

   @since OGR 1.9.0
   */

새로운 레이어 케이퍼빌리티 세 가지를 추가합니다:

-  OLCDeleteField / "DeleteField":
   이 레이어가 DeleteField() 메소드를 이용해서 현재 레이어 상에 있는 기존 필드를 삭제할 수 있는 경우 TRUE, 그렇지 않다면 FALSE입니다.

-  OLCReorderFields / "ReorderFields":
   이 레이어가 ReorderField() 또는 ReorderFields() 메소드를 이용해서 현재 레이어 상에 있는 기존 필드를 재정렬할 수 있는 경우 TRUE, 그렇지 않다면 FALSE입니다.

-  OLCAlterFieldDefn / "AlterFieldDefn":
   이 레이어가 AlterFieldDefn() 메소드를 이용해서 현재 레이어 상에 있는 기존 필드의 정의를 수정할 수 있는 경우 TRUE, 그렇지 않다면 FALSE입니다.

새 메소드들을 C API에 다음과 같이 매핑합니다:

.. code-block:: c

   OGRErr CPL_DLL OGR_L_DeleteField( OGRLayerH, int iField );
   OGRErr CPL_DLL OGR_L_ReorderFields( OGRLayerH, int* panMap );
   OGRErr CPL_DLL OGR_L_ReorderField( OGRLayerH, int iOldFieldPos, int iNewFieldPos );
   OGRErr CPL_DLL OGR_L_AlterFieldDefn( OGRLayerH, int iField, OGRFieldDefnH hNewFieldDefn, int nFlags );

구현 목적으로, :cpp:class:`OGRFeatureDefn` 클래스에도 새 메소드들을 추가합니다:

.. code-block:: cpp

       OGRErr      DeleteFieldDefn( int iField );
       OGRErr      ReorderFieldDefns( int* panMap );

배열이 [0,nSize-1] 범위의 순열인지 확인하기 위해 :file:`ogrutils.cpp` 에 ``OGRErr OGRCheckPermutation(int\* panPermutation, int nSize)`` 함수를 추가합니다. :cpp:func:`OGRFeatureDefn::ReorderFieldDefns` 메소드가 그리고 :cpp:func:`OGRLayer::ReorderFields` 메소드를 구현한 모든 드라이버가 이 함수를 사용해서 'panMap' 인자를 검증할 수 있습니다.

필드 유형 수정하기
------------------

이 RFC는 어떤 유형 변환이 가능할지 보장하려 시도하지 않습니다. 구현되는 드라이버의 케이퍼빌리티에 따라 달라질 것입니다. 예를 들어 데이터베이스 드라이버의 경우 (PG 드라이버의 경우 ``ALTER TABLE my_table ALTER COLUMN my_column TYPE new_type`` 명령어를 통해) 서버 쪽에서 직접 변환 작업을 수행할 것입니다. 따라서 몇몇 변환은 가능하고 다른 변환은 불가능할 수도 있습니다.

하지만 AlterFieldDefn() 메소드를 지원한다면, 대부분의 경우 모든 유형을 OFTString 유형으로 변환할 수 있을 것으로 예상합니다.

드라이버가 변환을 지원하지 않는데 변환을 수행해야 하는 경우 (ALTER_TYPE_FLAG가 설정되어 있는데 ``new_type != old_type`` 인 경우) 명시적인 오류를 발생시켜야 합니다.

호환성 문제점
-------------

없음

변경된 드라이버
---------------

Shapefile 드라이버가 DeleteField(), ReorderFields() 및 AlterFieldDefn()을 구현할 것입니다.
Shapelib은 DBFReorderFields() 및 DBFAlterFieldDefn()으로 확장될 것입니다.

주의: Shapefile 드라이버에 AlterFieldDefn()을 구현한다고 해서 -- OFTString 유형으로의 변환을 제외하고 -- 필드 유형 변환을 지원하지는 않습니다. 필드 길이 또는 정밀도를 변경하는 경우에도 기존 피처의 숫자값 서식을 변경하지 않을 것입니다. 하지만, 필드 길이를 수정하면 자르기(truncation) 또는 늘이기(expansion)를 적절하게 수행할 것입니다.

다른 드라이버들, 주로 (PG, MySQL, SQLite) 데이터베이스 드라이버들은 적절한 SQL 명령어(``ALTER TABLE foo DROP COLUMN bar``, ``ALTER TABLE foo ALTER COLUMN bar``, ...)를 전송함으로써 새 API를 구현하도록 쉽게 확장시킬 수 있습니다.
이 RFC가 승인된다면 실제로 PG 드라이버에 DeleteField() 및 AlterFieldDefn()을 구현할 계획입니다. 메모리 드라이버도 DeleteField(), ReorderFields() 및 AlterFieldDefn()을 지원하도록 업데이트할 것입니다.

SWIG 바인딩
-----------

DeleteField(), ReorderField(), ReorderFields() and AlterFieldDefn()를 SWIG에 매핑할 것입니다.

테스트 스위트
-------------

Shapefile 드라이버 용 새로운 API 구현을 테스트할 수 있도록 자동 테스트 스위트를 확장할 것입니다. 새 API의 사용 예시는 #2671 티켓에 첨부되어 있으며 (`rfc35_test.py <http://trac.osgeo.org/gdal/attachment/ticket/2671/rfc35_test.py>`_) 단위 테스트로 변환될 것입니다.

구현
----

이벤 루올이 GDAL/OGR 트렁크에 이 RFC를 구현할 것입니다. Shapelib 커밋 개발자가 Shapelib의 변경 사항을 업스트림 CVS로 푸시해야 할 것입니다. 제안된 구현은 #2671 티켓에 패치로 (`rfc35_v3.patch <http://trac.osgeo.org/gdal/attachment/ticket/2671/rfc35_v3.patch>`_) 첨부되어 있습니다.

투표 이력
---------

-  프랑크 바르메르담(Frank Warmerdam) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  하워드 버틀러(Howard Butler) +1
-  세케레시 터마시(Szekeres Tamás) +1
-  이벤 루올(Even Rouault) +1

