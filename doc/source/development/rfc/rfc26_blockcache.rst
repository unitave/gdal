.. _rfc-26:

================================================================================
RFC 26: GDAL 블록 캐시 개선
================================================================================

저자: 세케레시 터마시, 이벤 루올

연락처: szekerest@gmail.com, even.rouault@spatialys.com

상태: 승인, 구현

구현 버전: GDAL 2.1버전

요약 및 근거
------------

GDAL은 드라이버로부터 가져온 래스터 블록을 위한 인메모리 캐시를 유지/관리하고 동일한 블록에 두 번째로 접근하는 경우 드라이버가 아니라 캐시로부터 서비스되도록 보장합니다. 이 캐시는 밴드별로 유지/관리되며 각 블록을 (또는 하위 블록을) 가리키는 포인터를 위한 배열을 할당합니다. 이 접근법은 대용량 래스터 크기에 (또는 예를 들어 WMS/TMS 드라이버로 서비스되는 대용량 가상 래스터에) 충분하지 않기 때문에, #3224 티켓에서 제기된 :cpp:func:`GDALRasterBand::InitBlockInfo` 에서의 메모리 부족 오류를 일으킬 수도 있습니다.

예를 들면, 21수준에서 데이터셋의 밴드 하나를 구글 지도 타일 작업하면 256x256 픽셀 크기의 타일이 2,097,152 x 2,097,152 개 필요합니다. 다시 말해 GDAL이 32,768 x 32,768 (32,768 = 2,097,152 / 64) 즉 약 10억 개의 요소를 가진 배열을 할당하려 시도할 것이라는 뜻입니다. 32비트 빌드 상에서 이 배열의 용량은 4GB이기 때문에 전혀 할당할 수 없습니다. 또 64비트 빌드 상에서는 (운영 체제의 오버커밋(over-commit) 메커니즘 때문에 실제 메모리의 물리적 페이지를 할당하는 것이 아니라 일반적으로 가상 메모리를 예약할 뿐인 경우에도) 8GB입니다. 데이터셋 종료 시, 캐시에 남아 있는 블록들을 찾기 위해 이 10억 개의 셀을 탐색해야 할 것이라는 뜻입니다. 실제 상황이라면 RGB 데이터셋의 경우 앞에서 말한 모든 숫자를 3으로 (RGBA인 경우 4로) 곱해야만 합니다.

해시 집합(hash set) 구현의 경우, 메모리 할당은 캐시된 블록 개수에 직접적으로 의존합니다. 일반적으로 GDAL_CACHEMAX 용량 기본값이 40MB인데, 이때 (모든 데이터셋에 대해) 256x256 픽셀 크기의 타일 640개만 동시에 캐시할 수 있습니다.

주요 개념
---------

블록 캐시 작업을 설계할 때 스레드 안전성(thread-safety) 문제점에 대해 인식하는 것이 매우 중요합니다. :file:`gdalrasterblock.cpp` 에서는 정적 링크된 목록을 유지/관리해서 블록들의 접근 순서를 추적하고, 목록에서 가장 오래된 블록을 삭제해서 원하는 한도 내에서 캐시 용량을 유지합니다.
GDAL에서 ('hRBMutex'로 보호받는) 모든 데이터셋 및 밴드가 이 링크된 목록을 공유합니다. 새 블록을 읽어오는 경우 각 밴드에 대한 스레드가 이 뮤텍스(mutex)의 범위 안에 있는 또다른 밴드에 대한 :cpp:func:`GDALRasterBand::UnreferenceBlock` 호출을 촉발할 수도 있습니다. :cpp:func:`GDALRasterBand::FlushBlock` 또한 배열 또는 해시 테이블로부터 대응하는 타일을 제거해서 밴드 수준 캐시의 데이터 구조에 접근할 것입니다.

GDAL 2.0버전에서 스레드 안전성 관련 일부 문제점들(#3225, #3226)이 수정되었으며 이 RFC는 그런 시나리오를 계속 안전한 것으로 보전합니다.

이 RFC의 변경 사항은 캐시된 블록에 접근하거나 캐시된 블록을 추가 또는 제거하는 로직을 :cpp:class:`GDALRasterBand` 클래스로부터 새로운 :cpp:class:`GDALAbstractBandBlockCache` 클래스로 이동시키는 것입니다. 현재 배열 기반 로직을 새로운 :cpp:class:`GDALArrayBandBlockCache` 클래스로 이동시키고, 새 해시 집합 기반 로직은 :cpp:class:`GDALHashsetBandBlockCache` 클래스로 이동시킵니다.

배열 기반 구현의 경우, 호스팅 구조(배열)의 "정적" 특성 때문에 동시 스레드에서 셀을 읽어오거나 작성하는 경우 특별한 주의가 필요하지 않습니다. 특별한 주의를 기울여야만 하는 지점은 지정한 셀(블록)을 동시에 접근하지 않도록 하는 것뿐입니다. 예를 들어 또다른 스레드가 :cpp:func:`GDALRasterBlock::FlushCacheBlock` 또는 :cpp:func:`Internalize` 로부터 해제 중인 블록을 :cpp:func:`TryGetLockedBlockRef` 가 반환하는 일을 막아야 합니다. 이를 위해 이제 :cpp:class:`GDALRasterBlock` 의 'nRefCount' 멤버의 값을 증가시키거나, 감소시키거나, 또는 비교해서 바꿀 수 있는(`compare-and-swap <https://en.wikipedia.org/wiki/Compare-and-swap>`_) `원자 함수 <https://ko.wikipedia.org/wiki/%EC%9B%90%EC%9E%90_%EC%A1%B0%EC%9E%91>`_ 를 통해서만 :cpp:class:`GDALRasterBlock` 의 'nRefCount' 멤버에 접근해서 수정합니다.

해시 집합 기반 구현의 경우, :file:`cpl_hash_set.h` / :file:`cpl_hash_set.cpp` 에 구현된 해시 집합의 기반 데이터 구조가 기본적으로 스레드 안전하지 않습니다. 따라서 :cpp:class:`GDALHashsetBandBlockCache` 클래스가 해시 집합에서의 모든 읽기, 추가 및 제거를 보호하기 위한 전용 뮤텍스를 가집니다. 해시 집합 뮤텍스 아래 수행되는 어떤 작업도 :cpp:class:`GDALRasterBlock` 으로부터 어떤 메소드도 호출하지 않기 때문에, 'hRBMutex' 관련 교착 상태(deadlock)는 발생할 수 없습니다.

'hRBMutex'를 재사용해서 해시 집합을 보호할 수도 있겠지만, 그렇게 하면 'hRBMutex'의 경합(contention; 복수의 단말이 공유하는 회선에서 동시에 송신할 때 생기는 상태)이 불필요하게 증가했을 것입니다.

기본적으로, 다음 규칙을 기반으로 배열 기반 접근법과 해시 테이블 기반 접근법 가운데 하나를 선택합니다:

-  데이터셋이 가진 블록이 100만 개를 초과하는 경우 해시 집합 기반 구현을 사용하고, 그렇지 않다면 배열 기반 구현을 사용합니다.

이 선택을 대체하려면 :cpp:func:`GDALOpenEx` 에 새로운 GDAL_OF_ARRAY_BLOCK_ACCESS 및 GDAL_OF_HASHSET_BLOCK_ACCESS 열기 옵션 플래그를 전송하거나 또는 GDAL_BAND_BLOCK_CACHE 환경설정 옵션을 ARRAY 또는 HASHSET으로 설정하면 됩니다.

해시 집합 기반 구현은 모든 경우에 대해 기본 구현이 될 수 있는 잠재력을 가지고 있지만 (CPU 코어가 4개 또는 8개인 환경에서 :file:`autotest/cpp/testblockcache` 유틸리티로 수행된 성능 비교는 측정할 수 없는 차이를 보여줍니다) 이론적으로 배열 기반 구현에서 'hRBMutex'의 경합이 더 적기 때문에 코어를 많이 사용하는 경우 확장성(scalability)이 더 좋을 것입니다. GDAL 2.0버전에서 확장성을 향상시키기 위한 작업이 이루어졌기 때문에, 현재로서는 적당한 크기의 래스터에 대해 배열 기반 구현을 사용하도록 유지하는 것이 신중한 결정일 수도 있습니다.

이 RFC와 완전히 연결된 것은 아니지만, 메모리 할당 루틴이 스레드 간의 동기화를 수반하기 때문에 확장성에 영향을 미치는 (:cpp:class:`CPLHashSet` 의 내부 요소는 물론 :cpp:class:`GDALRasterBlock` 인스턴스) 객체 할당/할당 해제 횟수를 제한하기 위한 몇 가지 변경 사항이 적용되었습니다.

구현
----

이 RFC의 추가 사항을 구현하기 위해 GDAL 코드베이스에 다음과 같은 변경 사항을 적용합니다:

-  :file:`port/cpl_hash_set.cpp`/ :file:`port/cpl_hash_set.h`:
   작업 한 번으로 모든 요소를 제거하기 위한 CPLHashSetClear() 함수를 추가했습니다.

-  :file:`port/cpl_hash_set.cpp`/ :file:`port/cpl_hash_set.h`:
   요소 하나를 빨리 제거하기 위한 CPLHashSetRemoveDeferRehash() 함수를 추가했습니다.
   다시 말해 내부적으로 사용되는 배열의 크기 조정 가능성은 이후 작업으로 연기됩니다.

-  :file:`port/cpl_hash_set.cpp`/ :file:`port/cpl_hash_set.h`:
   링크된 목록으로부터 링크를 "재활용"하고 쓸모없는 malloc()/free()를 사용하지 않도록 개선합니다.

-  :file:`port/cpl_atomic_ops.cpp`:
   CPLAtomicCompareAndExchange() 함수를 추가합니다.

-  :file:`gcore/gdal.h`:
   GDAL_OF_DEFAULT_BLOCK_ACCESS, GDAL_OF_ARRAY_BLOCK_ACCESS 및 GDAL_OF_HASHSET_BLOCK_ACCESS 값들을 추가합니다.

-  :file:`gcore/gdal_priv.h`:
   GDALAbstractBandBlockCache 클래스와 GDALArrayBandBlockCacheCreate() 및 GDALHashSetBandBlockCacheCreate() 함수의 정의를 추가합니다. GDALRasterBand, GDALDataset 및 GDALRasterBlock 클래스 정의를 수정합니다.

-  :file:`gcore/gdalrasterband.cpp`:
   InitBlockInfo() 함수가 알맞은 밴드 블록 캐시 구현을 인스턴스화하도록 수정합니다.

-  :file:`gcore/gdalrasterband.cpp`:
   AdoptBlock(), UnreferenceBlock(), FlushBlock() 및 TryGetLockedBlockRef() 메소드의 기능을 실제 밴드 블록 캐시 구현에 위임합니다.

-  :file:`gcore/gdalrasterband.cpp`:
   AddBlockToFreeList() 함수를 추가하고 GDALAbstractBandBlockCache 클래스에 위임합니다.

-  :file:`gcore/gdalrasterblock.cpp`:
   SafeLockBlock() 함수를 TakeLock() 함수로 대체합니다.

-  :file:`gcore/gdalrasterblock.cpp`:
   (GDALAbstractBandBlockCache::CreateBlock() 함수가 사용하는) new/delete 호출을 몇 번 줄이기 위해 기존 블록 객체를 재활용하는 RecycleFor() 메소드를 추가합니다.

-  :file:`gcore/gdalrasterblock.cpp`:
   Internalize() 또는 FlushCacheBlock() 메소드가 더 이상 블록을 직접 해제하지 않지만 (이 메소드들은 여전히 블록의 'pData' 멤버를 해체하거나 재활용합니다) 레이어를 재사용하기 위해 GDALRasterBand::AddBlockToFreeList() 함수에 해당 블록을 넘깁니다.

-  :file:`gcore/gdalrasterblock.cpp`:
   GDALRasterBand::FlushCache() 또는 FlushBlock() 메소드와 GDALRasterBlock::Internalize() 또는 FlushCacheBlock() 메소드 사이의 블록 삭제 경합을 막기 위해 DropLockForRemovalFromStorage() 함수를 추가합니다.

-  :file:`gcore/gdalabstractbandblockcache.cpp`:
   이 파일을 추가합니다. 이 파일은 전체 수준 블록 관리자가 폐기했던 인스턴스화된 GDALRasterBlock 클래스를 나중에 재사용하기 위해 유지하는 로직을 담고 있습니다. new/delete 호출을 몇 번 줄여줍니다.

-  :file:`gcore/gdalarraybandblockcache.cpp`:
   대부분 기존 코드를 사용해서 GDALArrayBandBlockCache 클래스를 구현합니다.

-  :file:`gcore/gdalhashsetbandblockcache.cpp`:
   새로운 GDALHashsetBandBlockCache 클래스를 구현합니다.

하위 호환성
-----------

이 구현은 기존 API와의 하위 호환성을 유지합니다. :cpp:class:`GDALRasterBand`, :cpp:class:`GDALDataset` 및 :cpp:class:`GDALRasterBlock` 의 C++ API를 수정합니다.

성능에 미치는 영향
------------------

이 RFC를 구현한 이후, 배열 기반 구현이 계속 현재 구현과 동일한 성능을 보여야 합니다. (블록 재활용으로 성능이 아주 약간 향상될 가능성이 있습니다.)
:file:`autotest/cpp/testblockcache` 테스트로 확인되었습니다.

문서화
------

이 변경 사항은 기존 사용자 문서에 영향을 미치지 않습니다.

테스트
------

배열 기반 구현뿐만 아니라 GDAL_BAND_BLOCK_CACHE를 HASHSET으로 설정한 :file:`autotest/cpp/Makefile` 의 "quick_test" 대상이 :file:`autotest/cpp/testblockcache` 유틸리티를 실행합니다.

몇 가지 경합 상황을 테스트하기 위해 새로운 :file:`autotest/cpp/testblockcachelimits` 유틸리티를 개발했습니다. 경합을 촉발하기가 어렵기 때문에, :cpp:class:`GDALRasterBlock` 의 코드가 특정 위치에서 휴지(sleep)되도록 편집해서 경합을 안정적으로 시뮬레이션할 수 있게 했습니다.

구현 인력
---------

세케레시 터마시가 이 RFC의 초기 버전을 제공했습니다. 이벤 루올이 (`LINZ(Land Information New Zealand) <https://www.linz.govt.nz/>`_ 의 후원으로) 이를 재구성하고 GDAL 2.0버전 상에 포팅했습니다.

참조
----

-  제안된 구현은 깃허브 저장소의 `rfc26_bandblockcache <https://github.com/rouault/gdal2/tree/rfc26_bandblockcache>`_ 브랜치에 있습니다.

-  변경 사항 목록:
   `https://github.com/rouault/gdal2/compare/rfc26_bandblockcache <https://github.com/rouault/gdal2/compare/rfc26_bandblockcache>`_

관련 버그: #3264, #3224 티켓

투표 이력
---------

-  이벤 루올(Even Rouault) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  세케레시 터마시(Szekeres Tamás) +1
-  유카 라흐코넨(Jukka Rahkonen) +0

