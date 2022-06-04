.. _rfc-54:

=======================================================================================
RFC 54: 데이터셋 트랜잭션
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 데이터셋 수준에서 트랜잭션 메커니즘을 제공하는 API를 도입해서 PostgreSQL, SQLite 및 GPKG 드라이버에 사용합니다. 또 PostgreSQL 드라이버가 트랜잭션을 처리하는 방법을 상당 부분 재작업합니다. 네이티브하게 트랜잭션을 지원하지 않는 데이터소스에 대해 트랜잭션의 에뮬레이션을 구현하는 일반 메커니즘도 도입해서 FileGDB 드라이버에 사용합니다.

근거
----

현재 추상화(abstraction)는 레이어 수준에서 트랜잭션 API를 제공합니다. 하지만 BEGIN/COMMIT/ROLLBACK SQL 선언문을 이용해서 (PostgreSQL, SQLite, GPKG, PGDump, MSSQLSpatial) DBMS에 트랜잭션 API를 구현할 때, 의미 체계(semantics)가 실제로는 모든 레이어/테이블에 걸쳐 있는 데이터베이스 수준에서의 트랜잭션이기 때문에 일반적으로 오해의 소지가 있습니다. 따라서 한 레이어 상에서 StartTransaction()을 호출하더라도 다른 레이어 상에서 수행된 변경 사항까지도 확장됩니다. 극소수의 드라이버에서 StartTransaction()/CommitTransaction()를 대량 삽입(bulk insertion)을 수행하는 메커니즘으로 사용하는 경우가 있습니다. 예를 들면 WFS, CartoDB, GFT, GME 드라이버가 그런 경우입니다. 이 드라이버들 가운데 몇몇의 경우, 잠재적으로 여러 레이어의 수정 사항들이 함께 쌓일(stack) 수 있기 때문에 데이터셋 수준에서 트랜잭션을 수행할 수도 있습니다.

뿐만 아니라 일부 사용례에서는 레이어 여러 개를 일관되게 업데이트해야 하기 때문에 실제 데이터베이스 수준 트랜잭션 추상화가 필요합니다.

다양한 드라이버들의 현재 상황은 다음과 같습니다:

(분석으로부터 얻은 다음 관찰 내용 가운데 일부는 주로 드라이버에서 작업해야 할 개발자들의 이익을 위해 남겨두었습니다.)

PostgreSQL
~~~~~~~~~~

GetNextFeature() 요청을 실행하는 데 사용되는 커서(cursor)에 관한 몇 가지 사실:

-  메모리에 얽매이지 않고 대용량 데이터를 가져오려면 커서가 필요합니다.

-  커서를 실행하려면 트랜잭션이 필요합니다.

-  커서를 생성한 트랜잭션의 외부에서 (HOLD가 없는) 기본 커서를 사용할 수 없습니다.

-  트랜잭션(예, 커서가 아니라 트랜잭션입니다)이 아직 활성화되어 있는 동안에는 테이블의 구조를 수정할 수 없으며, 또다른 연결에서 테이블 구조를 수정하는 경우 다른 연결이 커밋 또는 롤백할 때까지 대기하게 됩니다.

-  트랜잭션 내에서, 삭제/수정된 행은 커서를 선언하기 전에 삭제/수정된 경우에만 표시됩니다.

-  HOLD를 가진 커서: 트랜잭션 외부에서 사용할 수도 있지만 테이블을 복사해야 할 수도 있습니다 --> 성능을 저하시킵니다.

현재 결함은 다음과 같습니다:

-  레이어 B 읽기가 시작될 때 레이어 A 읽기를 위해 생성된 암묵적인 기저 트랜잭션이 종료되기 때문에, (처음 가져온 피처 500개를 넘어서서) 교차삽입 레이어를 읽어올 수 없습니다. (처음 가져온 피처 500개는 OGR_PG_CURSOR_PAGE=1으로 쉽게 볼 수 있습니다.)

-  GetFeature()는 현재 트랜잭션을 플러시하고 커서 SELECT를 수행하기 위해 새 트랜잭션을 시작하는데, 레코드 하나만 가져오기 때문에 이럴 필요가 없습니다.

-  SetAttributeFilter()는 현재 진행 중인 트랜잭션을 FlushSoftTransaction()하는 ResetReading()을 발행합니다. 트랜잭션을 보장해야 하는, 시간이 오래 걸리는 업데이트 시나리오의 경우 성가실 수 있습니다.

작동하는 기능:

-  레이어 수준의 트랜잭션 지원을 데이터소스로 포워딩했습니다.
-  교차삽입 쓰기 작업이 (복사 모드에서도) 작동합니다.

SQLite/GPKG
~~~~~~~~~~~

-  테이블 내용을 읽어오는 데 사용되는 메커니즘(sqlite3_prepare() / sqlite3_step())은 트랜잭션을 필요로 하지 않습니다.

-  준비된 선언문 뒤에 하지만 첫 번째 단계 전에 트랜잭션을 실행하는 경우 단계(step)가 구조 수정 사항(예: 열 추가)을 확인합니다.

-  단계는 행 수정/추가가 일어나는 즉시 확인합니다.

-  레이어 수준의 트랜잭션 지원을 데이터소스로 포워딩했습니다.

MySQL
~~~~~

-  한 번에 요청 하나만 작업할 수 있는 mysql_use_result()를 사용하기 때문에 교차삽입 레이어를 읽어오지 못 합니다. (한 레이어를 읽으면 다른 읽기를 리셋합니다.) mysql_store_result()가 해결책이 될 수 있지만 전체 결과물 집합을 메모리로 불러와야 하기 때문에 대용량 레이어의 경우 실용적이지 못 합니다.

-  쿼리를 시작하고 나면 단계가 행 변경 사항을 설정하지 않습니다. (또다른 연결을 통해 쿼리하는 경우입니다. ExecuteSQL()을 통해 쿼리하는 경우 시간이 오래 걸리는 트랜잭션이 중단되기 때문입니다.)

-  트랜잭션을 지원하지 않습니다.

OCI
~~~

-  교차삽입 레이어 읽기가 작동합니다.
-  SELECT 이후 적용된 변경 사항을 표시하지 않는 것으로 보입니다.
-  트랜잭션을 지원하지 않습니다.

FileGDB
~~~~~~~

-  교차삽입 레이어 읽기가 작동합니다.
-  SELECT 이후 적용된 변경 사항을 표시하지 않는 것으로 보입니다.
-  트랜잭션을 지원하지 않습니다.

제안 변경 사항
--------------

GDALDataset 변경 사항
~~~~~~~~~~~~~~~~~~~~~

:cpp:class:`GDALDataset` 에 (:cpp:class:`GDALDataset` 으로부터 상속받는 :cpp:class:`OGRDataSource` 가 사용할 수 있는) 다음 메소드들을 추가합니다:

::

   /************************************************************************/
   /*                           StartTransaction()                         */
   /************************************************************************/

   /**
    \brief 트랜잭션을 지원하는 데이터소스의 경우, StartTransaction()이 트랜잭션을 생성합니다.

    트랜잭션 시작이 실패하는 경우, OGRERR_FAILURE를 반환합니다.
    트랜잭션을 지원하지 않는 데이터소스는 언제나
    OGRERR_UNSUPPORTED_OPERATION을 반환할 것입니다.

    내포(nested) 트랜잭션은 지원하지 않습니다.

    트랜잭션 시작 이후의 모든 변경 사항은 CommitTransaction()을 호출하면
    데이터소스에 확실하게 적용됩니다. 그 대신 RollbackTransaction()을
    호출하면 변경 사항을 취소할 수도 있습니다.

    이 문서 작성 당시, 트랜잭션은 벡터 레이어에 대해서만 적용됩니다.

    트랜잭션을 지원하는 데이터셋은 ODsCTransactions 케이퍼빌리티를
    노출시킬 것입니다. 일반적으로 그 범위가 트랜잭션이 시작된 레이어로
    제한되는 일이 거의 없는 레이어 수준에서의 트랜잭션보다
    데이터셋 수준에서의 트랜잭션 사용을 선호합니다.

    StartTransaction()이 실패하는 경우, CommitTransaction() 및 RollbackTransaction()을
    호출해서는 안 됩니다.

    StartTransaction()이 성공한 이후 오류가 발생하는 경우, 드라이버에 따라
    전체 트랜잭션이 암묵적으로 취소될 수도 있고 아닐 수도 있습니다.
    (예를 들면 PG 드라이버는 취소할 것이고, SQLite/GPKG 드라이버는 취소하지
    않을 것입니다.) 어떤 경우에도 오류가 발생한다면 균형을 유지하기 위해
    RollbackTransaction()을 명확하게 호출해야 합니다.

    기본적으로 bForce를 FALSE로 설정하는 경우 "효율적인" 트랜잭션만 시도할 것입니다.
    일부 드라이버가 트랜잭션의 에뮬레이션을 제공할 수도 있는데, 가끔 상당한
    오버헤드(overhead)가 발생하기 때문에 이런 경우 사용자가 bForce를 TRUE로
    설정해서 이런 에뮬레이션을 명확하게 허용해야만 합니다. 트랜잭션 에뮬레이션을
    제공하는 드라이버는 (ODsCTransactions가 아니라) ODsCEmulatedTransactions
    케이퍼빌리티를 노출시켜야 합니다.
    
    이 메소드는 GDALDatasetStartTransaction() C 함수와 동일합니다.

    @param bForce 느릴 수도 있는 트랜잭션 에뮬레이션 메커니즘을 받아들일 수
                  있는 경우 TRUE로 설정할 수 있습니다.

    @return 성공 시 OGRERR_NONE을 반환합니다.
    @since GDAL 2.0
   */
   OGRErr GDALDataset::StartTransaction(CPL_UNUSED int bForce);


   /************************************************************************/
   /*                           CommitTransaction()                        */
   /************************************************************************/

   /**
    \brief 트랜잭션을 지원하는 데이터소스의 경우, CommitTransaction()이 트랜잭션을 커밋합니다.

    활성화된 트랜잭션이 없거나 커밋이 실패하는 경우, OGRERR_FAILURE를 반환할 것입니다.
    트랜잭션을 지원하지 않는 데이터소스는 언제나
    OGRERR_UNSUPPORTED_OPERATION을 반환할 것입니다.

    이 메소드는 드라이버에 따라 활성화된 레이어 순차 읽기를
    중단하거나 중단하지 않을 수도 있습니다.

    이 메소드는 GDALDatasetCommitTransaction() C 함수와 동일합니다.

    @return 성공 시 OGRERR_NONE을 반환합니다.
    @since GDAL 2.0
   */
   OGRErr GDALDataset::CommitTransaction();

   /************************************************************************/
   /*                           RollbackTransaction()                      */
   /************************************************************************/

   /**
    \brief 트랜잭션을 지원하는 데이터소스의 경우, RollbackTransaction()이
    데이터소스를 현재 트랜잭션이 시작되기 이전의 상태로 롤백시킬 것입니다.

    활성화된 트랜잭션이 없거나 롤백이 실패하는 경우, OGRERR_FAILURE를 반환할 것입니다.
    트랜잭션을 지원하지 않는 데이터소스는 언제나
    OGRERR_UNSUPPORTED_OPERATION을 반환할 것입니다.

    이 메소드는 GDALDatasetRollbackTransaction() C 함수와 동일합니다.

    @return 성공 시 OGRERR_NONE을 반환합니다.
    @since GDAL 2.0
   */
   OGRErr GDALDataset::RollbackTransaction();

주의: :cpp:class:`GDALDataset` 클래스 자체에서, 이 메소드들은 OGRERR_UNSUPPORTED_OPERATION을 반환하는 비어 있는 구현을 가집니다.

C 수준에서 이 메소드 3개를 다음과 같이 매핑합니다:

::

   OGRErr CPL_DLL GDALDatasetStartTransaction(GDALDatasetH hDS, int bForce);
   OGRErr CPL_DLL GDALDatasetCommitTransaction(GDALDatasetH hDS);
   OGRErr CPL_DLL GDALDatasetRollbackTransaction(GDALDatasetH hDS);

새로운 데이터셋 케이퍼빌리티 2개를 추가합니다:

-  ODsCTransactions:
   이 데이터소스가 (효율적인) 트랜잭션을 지원하는 경우 TRUE입니다.

-  ODsCEmulatedTransactions:
   이 데이터소스가 에뮬레이션을 통해 트랜잭션을 지원하는 경우 TRUE입니다.

트랜잭션 에뮬레이션
~~~~~~~~~~~~~~~~~~~

트랜잭션을 네이티브하게 지원하지는 않지만 트랜잭션의 에뮬레이션을 원하는 드라이버가 사용하기 위한 새로운 OGRCreateEmulatedTransactionDataSourceWrapper() 함수를 추가합니다. 파일/디렉터리로 데이터를 지원하는 모든 데이터소스가 이 함수를 도입할 수도 있습니다.

::

   /** 기존 데이터소스에 트랜잭션 습성을 추가하는 새 데이터소스 객체를 반환합니다.
    * 
    * 제공된 poTransactionBehaviour 객체는 트랜잭션을 위한 드라이버 특화
    * 습성을 구현해야 합니다.
    *
    * 래퍼(wrapper) 클래스가 제공하는 일반 메커닙즘은 동일한 데이터소스 파일에
    * (서로 다른 데이터소스 연결을 통한) 동시 업데이트를 지원하지 않습니다.
    *
    * 이 메소드로 달성할 수 있는 일에는 제한이 있습니다. 예를 들어 StartTransaction(),
    * CommitTransaction() 또는 RollbackTransaction()을 호출하기 전에
    * ExecuteSQL()이 반환하는 배포되지 않은 레이어를 가질 수 없습니다.
    *
    * GetLayerDefn()을 이용해서 이전에 레이어 정의 객체를 반환받은 경우
    * StartTransaction() 이후 레이어 구조를 변경할 수 없습니다.
    *
    * @param poBaseDataSource 트랜잭션 습성을 추가할 데이터소스입니다.
    * @param poTransactionBehaviour IOGRTransactionBehaviour 인터페이스의 구현입니다.
    * @param bTakeOwnershipDataSource 반환된 객체가 전송된 poBaseDataSource를
    *                                 소유해야 할 것인지 여부를 (따라서 자체 삭제하는
    *                                 경우 삭제해야 할 것인지를) 나타냅니다.
    * @param bTakeOwnershipTransactionBehavior 반환된 객체가 전송된 poTransactionBehaviour를
    *                                          소유해야 할 것인지 여부를 (따라서 자체 삭제하는
    *                                          경우 삭제해야 할 것인지를) 나타냅니다.
    * @return 새로운 데이터소스 핸들을 반환합니다.
    * @since GDAL 2.0
    */
   OGRDataSource CPL_DLL* OGRCreateEmulatedTransactionDataSourceWrapper(
                                   OGRDataSource* poBaseDataSource,
                                   IOGRTransactionBehaviour* poTransactionBehaviour,
                                   int bTakeOwnershipDataSource,
                                   int bTakeOwnershipTransactionBehavior);

IOGRTransactionBehaviour 인터페이스의 정의는 다음과 같습니다:

::

   /** IOGRTransactionBehaviour는 드라이버가 트랜잭션 에뮬레이션을 제공하려면
    *  반드시 구현해야 하는 인터페이스입니다.
    *
    * @since GDAL 2.0
    */
   class CPL_DLL IOGRTransactionBehaviour
   {
       public:

           /** 트랜잭션을 시작합니다.
           *
           * 이 구현은 데이터소스를 종료하고 다시 열어서 (또는 오류가 발생하는 경우
           * NULL로 할당해서) poDSInOut 참조를 업데이트할 수도 있습니다.
           * 이런 경우 bOutHasReopenedDS를 TRUE로 설정해야만 합니다.
           *
           * 이 구현은 예를 들어 현재 데이터소스를 구성하는 기존 파일/디렉터리를
           * 백업할 수 있습니다.
           *
           * @param poDSInOut 수정될 수도 있는 데이터소스 핸들입니다.
           * @param bOutHasReopenedDS 데이터소스가 종료되었는지를 나타내는
           *                          산출 불(boolean) 값입니다.
           * @return 성공 시 OGRERR_NONE을 반환합니다.
           */
          virtual OGRErr StartTransaction(OGRDataSource*& poDSInOut,
                                          int& bOutHasReopenedDS) = 0;

           /** 트랜잭션을 커밋합니다.
           *
           * 이 구현은 데이터소스를 종료하고 다시 열어서 (또는 오류가 발생하는 경우
           * NULL로 할당해서) poDSInOut 참조를 업데이트할 수도 있습니다.
           * 이런 경우 bOutHasReopenedDS를 TRUE로 설정해야만 합니다.
           *
           * 이 구현은 예를 들어 StartTransaction() 당시 수행했을 수도 있는
           * 백업을 제거할 수 있습니다.
           *
           * @param poDSInOut 수정될 수도 있는 데이터소스 핸들입니다.
           * @param bOutHasReopenedDS 데이터소스가 종료되었는지를 나타내는
           *                          산출 불(boolean) 값입니다.
           * @return 성공 시 OGRERR_NONE을 반환합니다.
           */
          virtual OGRErr CommitTransaction(OGRDataSource*& poDSInOut,
                                           int& bOutHasReopenedDS) = 0;

           /** Rollback a transaction.
           *
           * 이 구현은 데이터소스를 종료하고 다시 열어서 (또는 오류가 발생하는 경우
           * NULL로 할당해서) poDSInOut 참조를 업데이트할 수도 있습니다.
           * 이런 경우 bOutHasReopenedDS를 TRUE로 설정해야만 합니다.
           *
           * 이 구현은 예를 들어 StartTransaction() 당시 수행했을 수도 있는
           * 백업을 복원할 수 있습니다.
           *
           * @param poDSInOut 수정될 수도 있는 데이터소스 핸들입니다.
           * @param bOutHasReopenedDS 데이터소스가 종료되었는지를 나타내는
           *                          산출 불(boolean) 값입니다.
           * @return 성공 시 OGRERR_NONE을 반환합니다.
           */
          virtual OGRErr RollbackTransaction(OGRDataSource*& poDSInOut,
                                             int& bOutHasReopenedDS) = 0;
   };

OPGRLayer 변경 사항
~~~~~~~~~~~~~~~~~~~

:cpp:class:`OGRLayer` 수준에서, GetNextFeature() 문서에 그 의미 체계를 분명히 하는 다음 추가적인 정보를 추가합니다:

::

   드라이버에 따라 GetNextFeature()가 반환하는 피처가 동시(concurrent) 수정 사항의
   영향을 받을 수도 받지 않을 수도 있습니다. 수정 사항을 실제로 확인하는 확실한 방법은
   GetNextFeature()가 호출된 레이어를 다시 읽기 전에 해당 레이어 상에 ResetReading()을
   호출하는 것입니다. 드라이버에 따라 읽기가 진행 중일 때 레이어의 구조 변경(필드 추가,
   삭제 등등)이 가능할 수도 가능하지 않을 수도 있습니다. 트랜잭션이 커밋 또는 중단된
   경우, 해당 작업 이후 현재 순차 읽기가 무결할 수도 무결하지 않을 수도 있기 때문에
   ResetReading()을 호출해야 할 수도 있습니다.

PG 드라이버 변경 사항
~~~~~~~~~~~~~~~~~~~~~

데이터셋 수준 트랜잭션을 구현했고, 암묵적으로 생성된 트랜잭션 사용을 재작업했습니다.

이제 교차삽입 레이어를 읽을 수 있습니다.

GetFeature()가 커서 또는 트랜잭션 없이도 실행될 수 있도록 수정했고, 트랜잭션에 대한 다른 모든 호출이 사용자가 시작한 트랜잭션을 우연히라도 리셋하지 않도록 확인/수정했습니다.

다음은 업데이트된 :file:`drv_pg_advanced.html` 도움말 페이지에서 설명하는 새로운 습성입니다:

::

   PostgreSQL에서 순차 읽기를 효율적으로 하려면 트랜잭션 안에서 해야 합니다.
   (기술적으로 따지면 "CURSOR WITHOUT HOLD"입니다.) 즉 객체를 가져왔을 때
   열려 있는 트랜잭션이 없는 경우 PostgreSQL 드라이버가 암묵적으로 순차 읽기를
   위한 트랜잭션을 열 것입니다. (다른 레이어를 계속 읽어오는 중이 아니라는
   가정 하에) 이 트랜잭션은 ResetReading() 메소드를 호출하면 해제될 것입니다.

   이런 암묵적인 트랜잭션 안에서 데이터셋 수준 StartTransaction() 메소드가
   명확하게 호출되는 경우, PostgreSQL 드라이버는 읽어오는 레이어 상에
   활성 커서를 계속 열어놓은 채 트랜잭션 습성을 제대로 모방하기 위해
   "SAVEPOINT"를 사용할 것입니다.

   레이어를 읽어오기 전에 데이터셋 수준 StartTransaction()으로 트랜잭션을
   명확하게 열었다면, 이 트랜잭션을 이용해서 레이어에 커서를 반복할 것입니다.
   트랜잭션을 명확하게 커밋하거나 롤백하는 경우, 커서가 무결하지 않게 될 것입니다.
   이때 ResetReading()을 다시 호출해서 처음부터 읽기를 다시 시작해야 합니다.

   SetAttributeFilter() 또는 SetSpatialFilter() 메소드를 호출한다는 것은
   암묵적으로 ResetReading()을 호출한다는 의미이기 때문에, 이 메소드들도
   ResetReading()과 동일한 영향을 미칩니다. 다시 말해서 암묵적인 트랜잭션이
   진행 중일 때 SetAttributeFilter() 또는 SetSpatialFilter() 메소드를 호출하면
   (다른 레이어를 읽어오는 중이 아닌 경우) 트랜잭션을 커밋하고
   다음 GetNextFeature() 호출 시 새 트랜잭션을 다시 시작할 것입니다.
   그 반대로 명확한 트랜잭션 안에서 SetAttributeFilter() 또는 SetSpatialFilter()
   메소드를 호출하는 경우 트랜잭션을 유지합니다.

   앞의 이런 규칙을 따라, 다음 예시들은 서로 다른 시나리오 상에서 OGR API를
   사용할 때 실행되는 SQL 지침을 보여줍니다:

   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr2->GetNextFeature()             DECLARE cur2 CURSOR  FOR SELECT * FROM lyr2
                                      FETCH 1 IN cur2

   lyr1->GetNextFeature()             FETCH 1 IN cur1

   lyr2->GetNextFeature()             FETCH 1 IN cur2

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr1->ResetReading()               CLOSE cur1

   lyr2->ResetReading()               CLOSE cur2
                                      COMMIT (implicit)

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ds->StartTransaction()             BEGIN

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr2->GetNextFeature()             DECLARE cur2 CURSOR FOR SELECT * FROM lyr2
                                      FETCH 1 IN cur2

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr1->ResetReading()               CLOSE cur1

   lyr2->ResetReading()               CLOSE cur2

   ds->CommitTransaction()            COMMIT

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ds->StartTransaction()             BEGIN

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   ds->CommitTransaction()            CLOSE cur1 (implicit)
                                      COMMIT

   lyr1->GetNextFeature()             FETCH 1 IN cur1      ==> 커밋으로 커서를 종료했기 때문에 오류가 발생합니다. 종료하기 전에 명확하게 ResetReading()을 호출해야 합니다.

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   ds->StartTransaction()             SAVEPOINT savepoint

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   ds->CommitTransaction()            RELEASE SAVEPOINT savepoint

   lyr1->ResetReading()               CLOSE cur1
                                      COMMIT (implicit)


   주의: 실제로는 PostgreSQL 드라이버가 객체 500개를 한 번에 가져옵니다.
         'FETCH 1'은 설명을 분명하게 하기 위한 것입니다.

마음의 안정을 위해 명확한 트랜잭션 안에서 작업을 수행할 것을 권장합니다. (:file:`ogr_pg.py` 를 수정하는 데 문제가 조금 있는데, '암묵적' 트랜잭션과는 제대로 작동하지 않는 연결 다시 열기 같은 이상한 일들이 분명히 발생합니다.)

GPKG 및 SQLite 드라이버 변경 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

데이터셋 수준 트랜잭션을 구현했습니다. 사용자가 시작한 트랜잭션을 우연히라도 리셋하지 않도록 이곳 저곳 조금씩 수정했습니다.

FileGDB 드라이버 변경 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~

FileGDB 드라이버는 앞에서 설명한 에뮬레이션을 사용해서 트랜잭션 메커니즘을 제공합니다. 이 메커니즘은 ``StartTransaction(force=TRUE)`` 을 호출할 때 지리 데이터베이스의 현재 상태를 백업하는 방식으로 작동합니다.
트랜잭션을 커밋하는 경우, 백업 복사본을 삭제합니다.
트랜잭션을 롤백하는 경우, 백업 복사본을 복원합니다.
따라서 대용량 지리 데이터베이스에 대해 작업하는 경우 리소스를 많이 소비할 수도 있습니다.
(동일한 또는 또다른 프로세스에서 서로 다른 연결을 사용해서) 동시 업데이트하는 경우 이 에뮬레이션이 알 수 없는 습성을 보인다는 사실을 기억하십시오.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

다음을 추가했습니다:

-  Dataset.StartTransaction(int force=FALSE)
-  Dataset.CommitTransaction()
-  Dataset.RollbackTransaction()
-  ogr.ODsCTransactions 상수
-  ogr.ODsCEmulatedTransactions 상수

유틸리티
--------

ODsCTransactions 케이퍼빌리티를 노출시키는 경우 ogr2ogr가 이제 (레이어 수준 트랜잭션 대신) 데이터셋 수준 트랜잭션을 사용합니다.

문서화
------

새로운/수정된 API를 문서화합니다.
:file:`MIGRATION_GUIDE.TXT` 에 다음 호환성 문제점 단락에 대한 언급을 추가합니다.

테스트 스위트
-------------

다음을 테스트하도록 테스트 스위트를 확장합니다:

-  업데이트된 드라이버:

   -  PG
   -  GPKG
   -  SQLite
   -  FileGDB

-  ogr2ogr의 데이터셋 수준 트랜잭션 사용

호환성 문제점
-------------

앞에서 설명한 대로, 이전에 플러시되어 더 이상 존재하지 않는 암묵적 트랜잭션과 관련해서 PG 드라이버의 미묘한 습성 변경을 관찰할 수 있지만, 전형적이지 않은 사용례로 제한되기를 바랍니다. 따라서 이전에 "작동했던" 몇몇 사례가 더 이상 작동하지 않을 수도 있지만, 새 습성은 더 이해하기 쉬울 것으로 기대합니다.

PG 및 SQLite 드라이버는 (레이어 수준에서) 내포된 StartTransaction() 호출을 분명히 받아들일 수 있었습니다. 그러나 이제 내포된 StartTransaction() 호출을 명확하게 지원하지 않는 데이터셋 수준 트랜잭션으로 해당 호출을 리디렉션하기 때문에 더 이상 받아들일 수 없습니다.

이 RFC의 범위를 벗어나는 관련 주제
----------------------------------

BEGIN/COMMIT/ROLLBACK을 구현하는 OCI, MySQL, MSSQLSpatial 드라이버가 데이터셋 수준 트랜잭션을 지원하도록 향후 개선할 수 있습니다.

GFT, CartoDB, WFS 드라이버도 데이터셋 수준 트랜잭션으로 혜택을 받을 수 있을 것입니다.

VRT 드라이버는 레이어 수준 트랜잭션을 지원합니다. (기저 데이터셋이 지원하는 경우, 그리고 통합(union) 레이어에 대해서는 지원하지 않습니다.) 데이터셋 수준 트랜잭션을 구현하려면 소스 데이터셋(들)로 데이터셋 수준 트랜잭션을 포워딩하는 방식으로 구현해야 할까요?
여러 소스들이 동일한 데이터셋을 사용하는 경우 구현이 복잡해질 수도 있지만, 더 근본적으로는 여러 데이터셋들에 대해 `ACID <https://ko.wikipedia.org/wiki/ACID>`_ 를 보장할 수 없습니다.

관련 티켓
---------

앞에서 설명한 문제점들을 해결하기 위해, PG 드라이버에서 트랜잭션이 구현되는 방식에 대한 `개정안 <https://trac.osgeo.org/gdal/ticket/1265>`_ 은 오래 전에 제안되었습니다.
이 제안 패치는 더 이상 적용되지 않지만, 이 RFC의 변경 사항들이 이 #1265 티켓이 말하고자 하는 문제점을 해결할 것으로 기대합니다.

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 `LINZ(Land Information New Zealand) <https://www.linz.govt.nz/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc54_dataset_transactions" 브랜치 <https://github.com/rouault/gdal2/tree/rfc54_dataset_transactions>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/rfc54_dataset_transactions>`_

투표 이력
---------

-  유카 라흐코넨 +1
-  하워드 버틀러 +1
-  이벤 루올 +1

