.. _rfc-47:

=======================================================================================
RFC 47: 데이터셋별 캐시 작업 및 GDALRasterBand 멀티스레딩 (구현되지 않음)
=======================================================================================

저자: 블레이크 톰슨(Blake Thompson)

연락처: flippmoke@gmail.com

상태: 개발 중

요약
----

멀티스레드 코드에서 GDAL을 활용할 때, 코드 가운데 제한되는 부분이 GDAL 내부의 LRU(Least Recently Used) 블록 캐시였던 경우가 많았습니다. 이 RFC는 데이터셋별로 여러 LRU를 가질 수 있게 하고 잠금(locking) 발생 시 최적화해서 멀티스레드 상황에서 LRU 캐시를 보다 효율적으로 만들기 위한 시도입니다. 뿐만 아니라 이 변경 사항은 캐시 내부에서 데이터를 효율적으로 관리할 수 있는 방식을 찾으려는 시도를 간략하게 서술합니다.

*이 변경 사항은 다음을 시도합니다*:

-  래스터 데이터셋 내부의 캐시 작업 시스템을 만듭니다:

   -  스레드 안전(Thread Safety)
   -  증가하는 스레드 개수와 비례하는 보다 선형적인 성능 제공

-  현재 캐시 잠금의 범위를 축소합니다.
-  선택적으로, (전체 수준 캐시보다는) 데이터셋별 캐시를 활성화합니다.
-  Mem 데이터셋의 READ 스레드를 데이터셋별로 안전하게 만듭니다.
-  드라이버에서의 스레드 안전을 높이는 향후 개발을 위한 토대를 마련합니다.

*이 변경 사항은 다음을 시도하지 않습니다*:

-  모든 드라이버를 스레드 안전하게 만들기
-  데이터셋을 스레드 안전하게 만들기

두 가지 서로 다른 해결책
------------------------

이 문제를 해결하기 위한 두 가지 서로 다른 방법을 제안하고 둘 다 코드 작업을 완료했습니다. (각 해결책에 대한 테스트 코드를 작성해야 합니다.) 하지만, 두 해결책들은 몇몇 공통 해결책을 공유합니다. 먼저 이 두 가지 서로 다른 해결책의 공통 변경 사항들을 설명한 다음 이 두 해결책이 어떻게 다른지를 설명하겠습니다.

풀 요청
-------------

-  `풀(pull) 요청 #1 <https://github.com/OSGeo/gdal/pull/38>`_:
   첫 번째 해결책 (데이터셋 RW 잠금)

-  `풀(pull) 요청 #2 <https://github.com/OSGeo/gdal/pull/39>`_:
   두 번째 해결책 (블록 RW 잠금)

공통 해결책
-----------

데이터셋 캐시 작업
~~~~~~~~~~~~~~~~~~

성능을 제한하는 정적 전체 수준 뮤텍스(mutex)는 :file:`gcore/gdalrasterblock.cpp` 안에 있습니다. 이 뮤텍스가 해당 파일에 위치한 이유는 최대 캐시, LRU 캐시 자체 및 현재 캐시 용량의 설정을 보호하기 위해서입니다. 캐시가 가득 차면 이 뮤텍스의 현재 범위가 한동안 캐시를 잠그게 만들고, 그 동안 :cpp:func:`GDALRasterBlock::Internalize` 메소드가 새 메모리를 초기화합니다.

이 LRU 캐시를 더 자주 잠가야 할 필요가 없게 하기 위해 새로운 전체 수준 환경설정 옵션 "GDAL_DATASET_CACHING"을 도입했습니다. 이 옵션을 YES로 설정하면 LRU 캐시를 전체 수준 캐시가 아니라 데이터별 캐시로 만듭니다. (기본값은 NO입니다.) 이렇게 하면 스레드를 사용하는 응용 프로그램이 단일 데이터셋에 대한 캐시만 플러시할 수 있게 해주기 때문에, 어떤 상황에서는 두 가지 이유로 성능을 개선합니다.
첫째, 좀 더 자주 사용되는 데이터셋의 캐시는 다른 데이터셋의 캐시와는 별도로 설정될 수도 있습니다. 즉 캐시된 상태로 유지될 가능성이 더 크다는 뜻입니다.
둘째, 공통 전체 수준 뮤텍스가 없다는 것은 서로 다른 데이터셋들을 작업하는 경우 스레드 2개가 동일한 뮤텍스를 잠글 가능성이 낮아진다는 의미입니다.

서로 다른 캐시들을 관리하기 위해 :cpp:class:`GDALRasterBlockManager` 클래스를 도입했습니다. 이 클래스는 전체 수준 상황 또는 데이터셋별 상황에서 캐시를 관리하는 책임을 집니다.

GDALRasterBlockManager
^^^^^^^^^^^^^^^^^^^^^^

::


   class CPL_DLL GDALRasterBlockManager
   {
       friend class GDALRasterBlock;
       
       int             bCacheMaxInitialized;
       GIntBig         nCacheMax;
       volatile GIntBig nCacheUsed;
       volatile GDALRasterBlock *poOldest;    /* tail */
       volatile GDALRasterBlock *poNewest;    /* head */
       void            *hRBMMutex;

     public:
                   GDALRasterBlockManager();
       virtual     ~GDALRasterBlockManager();
       void        SetCacheMax( GIntBig nBytes );
       GIntBig     GetCacheMax(void);
       GIntBig     GetCacheUsed(void);
       int         FlushCacheBlock(void);
       void        FlushTillBelow();
       void        Verify();
       int         SafeLockBlock( GDALRasterBlock ** );
       void        DestroyRBMMutex();
   };

원래 :cpp:class:`GDALRasterBlock` 내부에서 ``statistics:*`` 가 수행했던 작업들 가운데 다수가 이제 :cpp:class:`GDALRasterBlockManager` 로 이동했습니다.

GDALDataset
^^^^^^^^^^^

이제 모든 :cpp:class:`GDALDataset` 이 다음을 가집니다:

::

   GDALRasterBlockManager *poRasterBlockManager;

데이터셋 초기화 시 다음을 통해 설정됩니다:

::

   bDatasetCache =  CSLTestBoolean( 
   CPLGetConfigOption( "GDAL_DATASET_CACHING", "NO") );

   if ( bDatasetCache ) 
   {    
       poRasterBlockManager = new GDALRasterBlockManager();
   }
   else
   {   
       poRasterBlockManager = GetGDALRasterBlockManager();
   }

GDALRasterBand
^^^^^^^^^^^^^^

캐시 작업을 더 안전하고 효율적으로 만들기 위해, :cpp:class:`GDALRasterBand` 에도 뮤텍스를 도입했습니다. 이 뮤텍스는 밴드별 RasterBlock 배열('papoBlocks')을 보호하는 역할입니다.

스레드 안전과 두 가지 해결책
----------------------------

GDAL의 멀티스레드 작업은 복잡하지만, 이 변경 사항들은 GDAL 내부의 스레드 작업을 '개선'하려는 것입니다. GDAL 내부의 스레드 작업 문제들을 '해결'하고 정말로 스레드 안전하게 만들려는 것이 아닙니다. 이 변경 사항들의 목적은 단순히 캐시 스레드를 안전하게 만드는 것입니다. 이를 위해 다음 3개의 뮤텍스를 사용합니다. 이 뮤텍스 3개의 위치는 제안 해결책이 무엇이냐에 따라 달라집니다.

.. _solution-1-rw-mutex-in-gdaldataset-:

첫 번째 해결책 (GDALDataset의 RW 뮤텍스)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

뮤텍스
^^^^^^

첫 번째 해결책을 위한 뮤텍스 3개는 다음과 같습니다:

-  데이터셋 RW 뮤텍스 (:cpp:class:`GDALDataset` 별)
-  밴드 뮤텍스 (:cpp:class:`GDALRasterBand` 별)
-  RBM 뮤텍스 (:cpp:class:`GDALRasterBlockManager` 별)

교착 상태(deadlock)를 피하기 위해, 이 뮤텍스들의 우선 순위는 목록화되는 순서를 확립하는 것입니다. 예를 들어 밴드 뮤텍스를 가지고 있다면, 밴드 뮤텍스를 가져오기 전에 가져오지 않는 이상 데이터셋 RW 뮤텍스를 가져오지 못 할 수도 있습니다. 하지만 한 번에 하나 이상의 뮤텍스를 가지고 있지 않는 것이 목표입니다!

데이터셋 RW 뮤텍스
''''''''''''''''''
데이터셋 RW 뮤텍스의 목적은 데이터셋과 연결된 :cpp:class:`GDALRasterBlock` 들 안에 저장된 데이터를 보호하고 대용량 읽기 또는 쓰기 작업 도중 잠그는 것입니다. 이렇게 하면 서로 다른 스레드 2개가 동일한 :cpp:class:`GDALRasterBlock` 에 대해 memcpy()를 동시에 사용하는 일을 방지합니다. 이 뮤텍스는 일반적으로 :cpp:class:`GDALDataset` 안에 있지만, 독립형 :cpp:class:`GDALRasterBand` 의 경우 밴드에 대해 새 뮤텍스를 사용합니다.

밴드 뮤텍스
'''''''''''

밴드 뮤텍스의 목적은 :cpp:class:`GDALRasterBand` 에 있는 블록들의 배열의 제어를 관리하고 :cpp:class:`GDALRasterBlock` 들의 잠금을 관리하는 것입니다. 이 뮤텍스는 :cpp:class:`GDALRasterBand` 별 뮤텍스입니다.

RBM 뮤텍스
''''''''''

RBM(Restricted Boltzmann Machine) 뮤텍스의 목적은 LRU 캐시의 제어를 관리하는 것입니다. 이 뮤텍스는 캐시의 링크된 목록의 관리 및 캐시에 저장된 데이터의 총용량을 제어하는 책임을 집니다.

장점
^^^^

이 해결책은 두 가지 서로 다른 해결책 가운데 훨씬 단순한 해결책입니다. 데이터셋 수준에서 블록 보호가 이루어지기 때문에 밴드 하나를 읽거나 쓰는 과정에서 하나 이상의 밴드에 접근할 수도 있는 GeoTIFF 드라이버 같은 일부 드라이버들의 문제를 방지합니다. 즉 블록 데이터별로 밴드 수준에서만 잠금이 일어나는 경우 이 해결책이 제안하는 블록 보호가 없다면 문제점이 발생할 수 있습니다.

단점
^^^^

이 해결책은 최적의 잠금 방법이 아닐 수도 있습니다. IReadBlock, IWriteBlock, 그리고 IRasterIO 루틴을 전체 데이터셋에 걸쳐 보호하기 때문입니다. 스레드를 사용하는 환경에서 동일한 데이터셋을 읽어오는 경우 이 해결책은 아주 제한적입니다. 한 번에 하나 이상의 블록을 읽을 수 없기 때문입니다.

.. _solution-2-rw-mutex-in-gdalrasterblock-:

두 번째 해결책 (GDALRasterBlock의 RW 뮤텍스)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _mutexes-1:

뮤텍스
^^^^^^

두 번째 해결책을 위한 뮤텍스 3개는 다음과 같습니다:

-  밴드 뮤텍스 (:cpp:class:`GDALRasterBand` 별)

   -  RBM 뮤텍스 (:cpp:class:`GDALRasterBlockManager` 별)
   -  블록 RW 뮤텍스 (:cpp:class:`GDALRasterBlock` 별)

교착 상태를 피하기 위해 밴드 뮤텍스가 우선합니다. 즉 RBM 또는 블록 RW 뮤텍스를 가지고 있는 경우, 이전에 이미 밴드 뮤텍스를 가지고 있지 않은 이상 밴드 뮤텍스를 가져올 수 없다는 뜻입니다. 블록 뮤텍스와 RBM 뮤텍스를 동시에 가져오지 못 할 수도 있습니다.

.. _band-mutex-1:

밴드 뮤텍스
'''''''''''

밴드 뮤텍스의 목적은 :cpp:class:`GDALRasterBand` 에 있는 블록들의 배열의 제어를 관리하고 :cpp:class:`GDALRasterBlock` 들의 잠금을 관리하는 것입니다. 이 뮤텍스는 :cpp:class:`GDALRasterBand` 별 뮤텍스입니다.

.. _rbm-mutex-1:

RBM 뮤텍스
''''''''''

RBM 뮤텍스의 목적은 LRU 캐시의 제어를 관리하는 것입니다. 이 뮤텍스는 캐시의 링크된 목록의 관리 및 캐시에 저장된 데이터의 총용량을 제어하는 책임을 집니다.

블록 RW 뮤텍스
''''''''''''''

블록 RW 뮤텍스의 목적은 데이터셋과 연결된 :cpp:class:`GDALRasterBlock` 들 안에 저장된 데이터를 보호하고 대용량 읽기 또는 쓰기 작업 도중 잠그는 것입니다. 이렇게 하면 서로 다른 스레드 2개가 동일한 :cpp:class:`GDALRasterBlock` 에 대해 memcpy()를 동시에 사용하는 일을 방지합니다. 이 뮤텍스는 블록별 기반으로 생성되었습니다.

.. _pros-1:

장점
^^^^

이 해결책이 아마도 블록 작업을 위한 집중적이고 빠른, 가장 완전한 해결책일 것입니다. 이렇게 하면 IReadWrite, IWriteBlock, 그리고 IRasterIO가 이제 자신의 호출을 통해 뮤텍스를 ``void **`` (void pointer pointer)로 전송할 수 있기 때문입니다. CPLMutexHolderD에 전송된 NULL인 ``void **`` 가 포인터를 생성하거나 잠금을 발생시키지 않도록 뮤텍스에도 변경 사항을 적용했습니다. 다시 말해 뮤텍스에 대해 NULL 값을 전송하는 것만으로도 기존 코드의 습성을 대부분 유지할 수 있다는 의미입니다. 이런 모든 변경 사항들은 드라이버가 블록 안에 있는 데이터를 보호할 때 잠금이 발생하는 방식을 더 광범위하게 제어할 수 있게 해줍니다.

.. _cons-1:

단점
^^^^

이 해결책이 더 복잡한 해결책이기 때문에 유지/관리도 더 어려울 것이 분명합니다. 드라이버 작성도 이전처럼 대수로운 작업이 아니라, 교착 상태를 방지하고 스레드 안전을 유지/관리하기 위해 드라이버 안에서 잠금이 어떻게 수행되는지에 대해 더 주의를 기울여야만 합니다.
이 해결책으로 인해 발생할 수도 있는 다른 문제점은 스레드를 사용하지 않는 코드에서 속도가 약간 줄어든다는 것입니다. 스레드를 사용하는 방식으로 접근하지 않을 데이터를 잠그는 데 추가 사이클이 소요되기 때문입니다. 뿐만 아니라, 뮤텍스가 너무 많이 생성되는 경우 윈도우에서 문제점이 발생할 수도 있습니다. (:cpp:class:`GDALRasterBlock` 별 뮤텍스이기 때문에 윈도우 상에서 더 많이 생성되기 때문입니다.)
(주의: 이 문제점을 어떻게 제대로 테스트할 수 있을지 확실하지 않습니다.)

