.. _rfc-45:

=======================================================================================
RFC 45: 가상 메모리 매핑으로서의 GDAL 데이터셋 및 래스터 밴드
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, 구현

요약
----

이 RFC는 GDAL에 -- 바라건대 보다 단순한 사용례를 위해 -- GDAL 데이터셋 및 래스터 밴드의 이미지 데이터를 가상 메모리 매핑으로 표시할 수 있도록 해주는 추가 사항들을 제안합니다.

근거
----

GDAL 데이터셋 또는 래스터 밴드에서 이미지 데이터를 읽거나 쓰려면 읽거나 쓰는 관심 영역에 대해 RasterIO() 인터페이스를 사용해야만 합니다. 소용량 이미지의 경우, 가장 간편한 해결책은 일반적으로 관심 영역이 전체 래스터 범위인 단일 요청으로 전체 이미지를 읽기/쓰기 하는 것입니다. 대용량 이미지의 경우, 특히 이미지 데이터의 용량이 RAM을 초과하는 경우 이런 접근법이 불가능하며, 전체 이미지를 작업하려면 메모리 문제를 피하기 위해 창 작업 전략을 이용해야만 합니다: 일반적으로 스캔라인별로 (또는 스캔라인 그룹별로) 또는 타일화 이미지의 경우 블록별로 처리합니다. 이는 각 관심 픽셀 주변의 이웃 픽셀에 접근해야 하는 경우 알고리즘 작성을 더 복잡하게 만들 수 있습니다. 이 추가 창의 크기를 고려해야만 하기 때문에 관심 영역들이 중첩하게 되기 때문입니다. 해결할 수 없는 문제는 아니지만, 추구하는 주요 목적으로부터 주의를 분산시키는 추가적인 사고가 필요합니다.

이 RFC가 제안하는 추가 사항은 (CPU 아키텍처 및 운영 체제가 부과하는 제한을 제외하고) 데이터셋 용량 대비 RAM 용량으로 제한받지 않고 포인터로 접근할 수 있는 단일 배열로 이미지 데이터를 표현하도록 합니다.

기술적 해결책
~~~~~~~~~~~~~

저수준 메커니즘: cpl_virtualmem.h
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

이 새로운 케이퍼빌리티를 지원하는 저수준 메커니즘은 가상 메모리 영역(리눅스 상에서는 mmap() 함수가 할당하는 가상 메모리 영역)을 표현하는 CPLVirtualMem 객체입니다. 이 가상 메모리 영역은 초기에 가상 메모리 공간이라는 측면에서만 예약되어 있는데, 실제 메모리에는 할당되어 있지 않습니다. 이 예약된 가상 메모리 공간은 POSIX 시스템 상에서 가상 메모리 공간에 접근하려는 모든 시도가 SIGSEGV 신호(분할 폴트)를 촉발하는 예외 -- 페이지 폴트 -- 를 발생시키는 접근 권한으로 보호됩니다. 다행히 소프트웨어에서 신호 처리기(signal handler)를 사용해서 분할 폴트를 포착할 수 있습니다. 이런 분할 폴트가 방생하는 경우 특수 신호 처리기가 자신의 책임 하에 있는 가상 메모리 영역에서 분할 폴트가 발생하는지 확인하고, 그렇다면 접근한 가상 메모리 영역의 일부분("페이지")을 (사용자가 제공한 콜백 덕분에) 합리적인 값으로 채우는 작업을 처리할 것입니다. 그 다음 분할 폴트를 촉발한 명령을 다시 시도하기 전에 페이지에 대한 적절한 권한(읽기 전용 또는 읽기-쓰기)을 설정할 것입니다. 메모리 매핑에 접근하는 사용자 코드의 관점에서 보면 이 과정은 완전히 투명하며, 처음부터 전체 가상 메모리 영역을 채우는 것과 동일합니다.

RAM 용량을 초과하는 대용량 매핑의 경우, 여전히 특정 시점에서 디스크 스왑 작업을 발생시킬 것입니다. 이를 피하기 위해, CPLVirtualMem 객체 생성 시 정의된 한계값에 도달하면 분할 폴트 처리기가 가장 최근에 사용된 페이지를 제거할 것입니다.

쓰기 지원의 경우 또다른 콜백을 전송하면 됩니다. 페이지를 제거하기 전에 콜백을 호출하기 때문에 사용자 코드가 자신의 콘텐츠를 보다 영구적인 저장소로 플러시할 수 있는 기회를 가지게 됩니다.

또한 메모리 파일 매핑 메커니즘을 사용해서 CPLVirtualMem 객체를 생성하는 다른 방법도 제공합니다. 디스크 상에 있는 데이터의 구성이 인메모리 배열의 구성과 완전히 일치하는 "원시(raw)" 데이터셋이 (예를 들면 EHdr 드라이버에서) 이 방법을 사용할 수도 있습니다.

고수준 사용례
^^^^^^^^^^^^^

새 API 4개를 도입합니다(다른 단락에서 자세히 설명합니다):

-  :cpp:func:`GDALDatasetGetVirtualMem`:
   주목할 만한 'pData' 버퍼를 제외하면, GDALDatasetRasterIO()와 거의 동일한 인자들을 입력받습니다. CPLVirtualMemGetAddr() 메소드를 사용해서 가상 메모리 매핑의 기반 주소를 가져올 수 있는 ``CPLVirtualMem*`` 객체를 반환합니다.

.. image:: ../../../images/rfc45/rfc_2d_array.png

-  :cpp:func:`GDALRasterBandGetVirtualMem`:
   데이터셋 객체보다는 래스터 밴드 객체 상에서 작업하는 GDALDatasetGetVirtualMem()과 동일합니다.

-  :cpp:func:`GDALDatasetGetTiledVirtualMem`:
   다소 독창적인 API입니다. 데이터셋 자체가 타일화되어 있는 경우, 매핑이 이미지 데이터의 (예를 들어 행별로 구성된) 2차원 뷰를 표현하는 대신 성능면에서 더 적합한 타일 배열로 노출시킵니다.

.. image:: ../../../images/rfc45/rfc_tiled.png

밴드가 여러 개인 경우, 밴드 구성 요소들을 서로 다른 세 가지로 구성할 수 있습니다. 알려진 한도 내에서 이런 구성들을 부르는 표준적인 방법은 없기 때문에 결과적으로 다음과 같은 스키마들로 가장 잘 설명할 수 있을 것입니다:

- TIP / 픽셀이 교차삽입된 타일(Tile Interleaved by Pixel)

.. image:: ../../../images/rfc45/rfc_TIP.png
   :alt: TIP / Tile Interleaved by Pixel

- BIT / 타일이 교차삽입된 밴드(Band Interleaved by Tile)

.. image:: ../../../images/rfc45/rfc_BIT.png
   :alt: BIT / Band Interleaved by Tile

- BSQ / 밴드 순차 구성(Band SeQuential organization)

.. image:: ../../../images/rfc45/rfc_BSQ.png
   :alt: BSQ / Band SeQuential organization

-  :cpp:func:`GDALRasterBandGetTiledVirtualMem`:
   데이터셋 객체보다는 래스터 밴드 객체 상에서 작업하는 GDALDatasetGetTiledVirtualMem()과 동일합니다.

-  :cpp:func:`GDALGetVirtualMemAuto`:
   사용자가 접근 모드만 지정하는 GDALRasterBandGetVirtualMem()를 단순화시킨 버전입니다. 이 함수는 픽셀 간격 및 줄 간격을 반환합니다. 이 함수는 :cpp:class:`GDALRasterBand` 클래스 수준에서 가상 메소드로 구현되기 때문에 드라이버가 GDALRasterBandGetVirtualMem()만 사용하는 기본 구현을 대체할 수 있는 기회를 가집니다. 대체 구현은 메모리 파일 매핑 메커니즘을 대신 사용할 수도 있습니다. RawRasterBand 객체 및 GeoTIFF 드라이버에서 이렇게 구현될 것입니다.

새 API의 상세 사항
------------------

.. _implemented-by-cpl_virtualmemcpp:

cpl_virtualmem.cpp로 구현
~~~~~~~~~~~~~~~~~~~~~~~~~

::

   /**
    * \file cpl_virtualmem.h
    *
    * 가상 메모리 관리.
    *
    * 이 파일은 그 내용을 투명하게 할당하고 실시간(on-the-fly)으로 채우는 가상 메모리
    * 매핑을 정의하는 메커니즘을 제공합니다. 이런 가상 메모리 매핑은 사용할 수 있는
    * RAM 용량을 훨씬 초과할 수 있지만, 허용된 캐시 용량 제한 내에서 가상 메모리 매핑의
    * 일부만 실제로 할당됩니다.
    *
    * 이 과정에서 운영 체제의 저수준 메커니즘(가상 메모리 할당, 페이지 보호 및
    * 가상 메모리 예외 처리기)을 이용합니다.
    *
    * 파일 또는 파일의 일부분으로부터 가상 메모리 매핑을 생성할 수도 있습니다.
    *
    * 현재 구현은 리눅스 전용입니다.
    */

   /** 가상 메모리 매핑을 표현하는 불투명(opaque) 데이터 유형입니다. */
   typedef struct CPLVirtualMem CPLVirtualMem;

   /** 가상 메모리의 아직 매핑되지 않은 페이지에 접근하는 경우 촉발되는 콜백입니다.
     * 이 콜백은 페이지를 관련 값으로 채울 책임을 집니다.
     *
     * @param ctxt 가상 메모리 핸들입니다.
     * @param nOffset 메모리 매핑에서의 페이지 오프셋입니다.
     * @param pPageToFill 채워야 할 페이지의 주소입니다. 이 주소가 CPLVirtualMemGetAddr()
                          + nOffset 위치가 아니라 임시 위치일 수도 있다는 사실을 기억하십시오.
     * @param nToFill 페이지의 바이트 개수입니다.
     * @param pUserData CPLVirtualMemNew()에 전송된 사용자 데이터입니다.
     */
   typedef void (*CPLVirtualMemCachePageCbk)(CPLVirtualMem* ctxt,
                                       size_t nOffset,
                                       void* pPageToFill,
                                       size_t nToFill,
                                       void* pUserData);

   /** 지저분하게 매핑된(dirty mapped) 페이지를 해제하려 하는 경우 (캐시의 포화 또는
     * 가상 메모리 매핑의 종료) 촉발되는 콜백입니다.
     *
     * @param ctxt 가상 메모리 핸들입니다.
     * @param nOffset 메모리 매핑에서의 페이지 오프셋입니다.
     * @param pPageToBeEvicted 플러시할 페이지의 주소입니다. 이 주소가 
     *                         CPLVirtualMemGetAddr() + nOffset 위치가 아니라
     *                         임시 위치일 수도 있다는 사실을 기억하십시오.
     * @param nToBeEvicted 페이지의 바이트 개수입니다.
     * @param pUserData CPLVirtualMemNew()에 전송된 사용자 데이터입니다.
     */
   typedef void (*CPLVirtualMemUnCachePageCbk)(CPLVirtualMem* ctxt,
                                         size_t nOffset,
                                         const void* pPageToBeEvicted,
                                         size_t nToBeEvicted,
                                         void* pUserData);

   /** 가상 메모리 매핑을 삭제(destroy)하는 경우 촉발되는 콜백입니다.
     * @param pUserData CPLVirtualMemNew()에 전송된 사용자 데이터입니다.
    */
   typedef void (*CPLVirtualMemFreeUserData)(void* pUserData);

   /** 가상 메모리 매핑의 접근 모드입니다. */
   typedef enum
   {
       /*! 매핑은 읽기 전용이지만 쓰기를 방지하지는 않을 것입니다.
           작성된 내용은 모두 손실될 것이라는 사실을 기억하십시오. */
       VIRTUALMEM_READONLY,
       /*! 매핑은 읽기 전용이며, 운영 체제 페이지 보호 메커니즘을 통해
           이를 강제합니다. */
       VIRTUALMEM_READONLY_ENFORCED,
       /*! 매핑은 읽기-쓰기이며, pfnUnCachePage 콜백 덕분에 수정한
           페이지를 저장할 수 있습니다. */
       VIRTUALMEM_READWRITE
   } CPLVirtualMemAccessMode;


   /** 가상 메모리 페이지 용량을 반환합니다.
    *
    * @return 페이지 용량을 반환합니다.
    *
    * @since GDAL 1.11
    */
   size_t CPL_DLL CPLGetPageSize(void);

   /** 새로운 가상 메모리 매핑을 생성합니다.
    *
    * nSize 용량의 가상 메모리 영역을 예약할 것인데, 그 용량이 사용할 수 있는
    * 실제 메모리를 훨씬 초과할 수도 있습니다. 초기에는 실제 메모리를 할당하지
    * 않을 것입니다. 메모리 페이지에 접근하는 즉시 실제 메모리를 투명하게 할당하고
    * pfnCachePage 콜백으로 채울 것입니다. 허용된 캐시 용량에 도달하면
    * 가장 최근에 사용한 페이지를 할당 해제할 것입니다.
    *
    * 리눅스 AMD64 플랫폼 상에서 nSize의 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 nSize의 최대값은 2GB입니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 리눅스 상에서 이 함수는 SIGSEGV 처리기를 설치할 것입니다.
    * CPLVirtualMemManagerTerminate()가 원본 처리기를 복원할 것입니다.
    *
    * @param nSize 가상 메모리 매핑의 바이트 단위 용량입니다.
    * @param nCacheSize 실제로 할당될 바이트 단위 최대 메모리 용량입니다.
    *                   (이상적으로는 RAM 용량 이하여야만 합니다.)
    * @param nPageSizeHint 페이지 용량에 대한 힌트입니다. CPLGetPageSize()가
    *                      반환한 시스템 페이지 용량의 배수여야만 합니다.
    *                      일반적으로 최소값은 4096입니다. 함수가 기본 페이지
    *                      용량을 결정하게 하려면 0으로 설정할 수도 있습니다.
    * @param bSingleThreadUsage 가상 메모리 매핑에 동시에 접근할 스레드들이
    *                           없는 경우 TRUE로 설정하십시오. 이렇게 하면
    *                           성능을 조금 최적화할 수 있습니다.
    * @param eAccessMode 가상 메모리 매핑에 사용할 권한입니다.
    * @param pfnCachePage 가상 메모리의 아직 매핑되지 않은 페이지에 접근하는
    *                     경우 촉발되는 콜백입니다.
    *                     이 콜백은 페이지를 관련 값으로 채울 책임을 집니다.
    * @param pfnUnCachePage 지저분하게 매핑된(dirty mapped) 페이지를 해제하려
    *                       하는 경우 (캐시의 포화 또는 가상 메모리 매핑의 종료)
    *                       촉발되는 콜백입니다. NULL일 수도 있습니다.
    * @param pfnFreeUserData pCbkUserData를 해제하기 위해 사용할 수 있는
    *                        콜백입니다. NULL일 수도 있습니다.
    * @param pCbkUserData pfnCachePage 및 pfnUnCachePageuser에 전송되는
    *                     사용자 데이터입니다.
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem CPL_DLL *CPLVirtualMemNew(size_t nSize,
                                           size_t nCacheSize,
                                           size_t nPageSizeHint,
                                           int bSingleThreadUsage,
                                           CPLVirtualMemAccessMode eAccessMode,
                                           CPLVirtualMemCachePageCbk pfnCachePage,
                                           CPLVirtualMemUnCachePageCbk pfnUnCachePage,
                                           CPLVirtualMemFreeUserData pfnFreeUserData,
                                           void *pCbkUserData);


   /** 파일의 가상 메모리 매핑을 사용할 수 있는지 여부를 반환합니다.
    *
    * @return 파일의 가상 메모리 매핑을 사용할 수 있는 경우 TRUE를 반환합니다.
    * @since GDAL 1.11
    */
   int CPL_DLL CPLIsVirtualMemFileMapAvailable(void);

   /** 파일로부터 새 가상 메모리 매핑을 생성합니다.
    *
    * 이 파일은 VSI 확장 가상 파일이 아니라 운영 체제가 인식하는
    * "진짜" 파일이어야만 합니다.
    *
    * VIRTUALMEM_READWRITE 모드에서는, 파일에 메모리 매핑에 대한
    * 업데이트를 작성할 것입니다.
    *
    * 리눅스 AMD64 플랫폼 상에서 nLength의 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 nLength의 최대값은 2GB입니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * @param  fp       가상 파일 핸들입니다.
    * @param  nOffset  파일에서 매핑을 시작할 오프셋입니다.
    * @param  nLength  파일에서 메모리로 매핑할 부분의 길이입니다.
    * @param eAccessMode 가상 메모리 매핑에 사용할 권한입니다.
    *                    파일을 연 권한과 일관되어야만 합니다.
    * @param pfnFreeUserData 객체를 삭제(destroy)할 때 호출하는 콜백입니다.
    * @param pCbkUserData pfnFreeUserData로 전송되는 사용자 데이터입니다.
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */
   CPLVirtualMem CPL_DLL *CPLVirtualMemFileMapNew( VSILFILE* fp,
                                                   vsi_l_offset nOffset,
                                                   vsi_l_offset nLength,
                                                   CPLVirtualMemAccessMode eAccessMode,
                                                   CPLVirtualMemFreeUserData pfnFreeUserData,
                                                   void *pCbkUserData );

   /** 다른 가상 메모리로부터 파생된 새 가상 메모리 매핑을 생성합니다.
    *
    * 픽셀 교차삽입 데이터에 대해 매핑을 생성하는 경우 유용할 수도 있습니다.
    *
    * 새 매핑은 기반 매핑을 참조합니다.
    *
    * @param pVMemBase 기반 가상 메모리 매핑입니다.
    * @param nOffset   기반 가상 메모리 매핑에서 새 매핑을 시작할 오프셋입니다.
    * @param nSize     새 매핑에 노출시킬 기반 가상 메모리 매핑의 용량입니다.
    * @param pfnFreeUserData 객체를 삭제(destroy)할 때 호출하는 콜백입니다.
    * @param pCbkUserData pfnFreeUserData로 전송되는 사용자 데이터입니다.
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */
   CPLVirtualMem CPL_DLL *CPLVirtualMemDerivedNew(CPLVirtualMem* pVMemBase,
                                                  vsi_l_offset nOffset,
                                                  vsi_l_offset nSize,
                                                  CPLVirtualMemFreeUserData pfnFreeUserData,
                                                  void *pCbkUserData);

   /** 가상 메모리 매핑을 해제합니다.
    *
    * CPLVirtualMemGetAddr()가 반환하는 포인터가 더 이상 무결하지 않을 것입니다.
    * 가상 메모리 매핑이 쓰기/읽기 권한으로 생성되었고 지저분한 (예를 들면 수정된)
    * 페이지인 경우 해제되기 전에 pfnUnCachePage 콜백을 통해 플러시될 것입니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL CPLVirtualMemFree(CPLVirtualMem* ctxt);

   /** 가상 메모리 매핑의 시작을 가리키는 포인터를 반환합니다.
    *
    * p가 이 함수가 반환한 포인터일 때, [p:p+CPLVirtualMemGetSize()-1] 범위 안에 있는
    * 바이트들은 CPLVirtualMemFree()를 호출할 때까지 무결할 것입니다.
    *
    * (read() 또는 write() 같은) 시스템 호출의 인자로 사용되는 바이트 범위가
    * "실체화되지 않은" 페이지를 담고 있는 경우 시스템 호출이 EFAULT와 함께
    * 실패할 것입니다. 이 문제점을 피하려면 CPLVirtualMemPin()을 사용하면 됩니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 가상 메모리 매핑의 시작을 가리키는 포인터를 반환합니다.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL *CPLVirtualMemGetAddr(CPLVirtualMem* ctxt);

   /** 가상 메모리 매핑의 용량을 반환합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 가상 메모리 매핑의 용량을 반환합니다.
    *
    * @since GDAL 1.11
    */
   size_t CPL_DLL CPLVirtualMemGetSize(CPLVirtualMem* ctxt);

   /** 가상 메모리 매핑이 직접 파일 매핑(direct file mapping)인지 여부를 반환합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 가상 메모리 매핑이 직접 파일 매핑인 경우 TRUE를 반환합니다.
    *
    * @since GDAL 1.11
    */
   int CPL_DLL CPLVirtualMemIsFileMapping(CPLVirtualMem* ctxt);

   /** 가상 메모리 매핑의 접근 모드를 반환합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 가상 메모리 매핑의 접근 모드를 반환합니다.
    *
    * @since GDAL 1.11
    */
   CPLVirtualMemAccessMode CPL_DLL CPLVirtualMemGetAccessMode(CPLVirtualMem* ctxt);

   /** 가상 메모리 매핑에 연결된 페이지 용량을 반환합니다.
    *
    * 반환 값이 최소한 CPLGetPageSize()일 것이며, 초과할 가능성도 있습니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 페이지 용량을 반환합니다.
    *
    * @since GDAL 1.11
    */
   size_t CPL_DLL CPLVirtualMemGetPageSize(CPLVirtualMem* ctxt);

   /** 동시(concurrent) 스레드들로부터 이 메모리 매핑에 안전하게 접근할 수
    * 있는 경우 TRUE를 반환합니다.
    *
    * 문제가 발생할 수 있는 상황은 스레드 여러 개가 아직 매핑되지 않은
    * 매핑 페이지에 접근하려 시도하는 경우입니다.
    *
    * 이 함수가 반환하는 값은 bSingleThreadUsage가 CPLVirtualMemNew()
    * 그리고/또는 구현에 설정되지 않았는지 여부에 따라 달라집니다.
    *
    * 리눅스 상에서 bSingleThreadUsage = FALSE인 경우
    * 이 함수는 항상 TRUE를 반환합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @return 동시 스레드들로부터 이 메모리 매핑에 안전하게 접근할 수
    * 있는 경우 TRUE를 반환합니다.
    *
    * @since GDAL 1.11
    */
   int CPL_DLL CPLVirtualMemIsAccessThreadSafe(CPLVirtualMem* ctxt);

   /** 스레드가 가상 메모리 매핑에 접근할 것이라고 선언합니다.
    *
    * 가상 메모리 매핑을 bSingleThreadUsage = TRUE로 생성한 경우를 제외하고,
    * 가상 메모리 매핑의 콘텐츠에 접근하려는 스레드가 이 함수를 호출해야만 합니다.
    *
    * 이 함수는 CPLVirtualMemUnDeclareThread()과 쌍으로 사용해야만 합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL CPLVirtualMemDeclareThread(CPLVirtualMem* ctxt);

   /** 스레드가 가상 메모리 매핑에 접근을 종료할 것이라고 선언합니다.
    *
    * 가상 메모리 매핑을 bSingleThreadUsage = TRUE로 생성한 경우를 제외하고,
    * 가상 메모리 매핑에 더 이상 접근하지 않을 스레드가 이 함수를 호출해야만 합니다.
    *
    * 이 함수는 CPLVirtualMemDeclareThread()과 쌍으로 사용해야만 합니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL CPLVirtualMemUnDeclareThread(CPLVirtualMem* ctxt);

   /** 가상 메모리 영역을 실체화할 것을 확인합니다.
    *
    * 이 함수를 반드시 호출할 필요는 없지만, 분할 폴트 신호를 네이티브하게
    * 받아들이지 못 하는 gdb 또는 valgrind 같은 도구를 사용해서 프로세스를
    * 디버깅하는 경우 유용할 수도 있습니다.
    *
    * read() 또는 write() 같은 시스템 호출에 가상 메모리 매핑의 일부분을
    * 제공하려는 경우에도 이 함수가 필요합니다. 아직 실체화되지 않은 메모리
    * 영역에 대해 read() 또는 write()를 호출하는 경우,
    * 호출이 EFAULT와 함께 실패할 것입니다.
    *
    * @param ctxt CPLVirtualMemNew()이 반환하는 맥락입니다.
    * @param pAddr 고정(pin)시킬 메모리 영역입니다.
    * @param nSize 메모리 영역의 용량입니다.
    * @param bWriteOp 메모리에 쓰기 모드로 접근할 경우 TRUE로 설정하십시오.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL CPLVirtualMemPin(CPLVirtualMem* ctxt,
                                 void* pAddr, size_t nSize, int bWriteOp);

   /** 가상 메모리와 연결된 모든 리소스와 처리기들을 정리(cleanup)합니다.
    *
    * 마지막 CPLVirtualMem 객체를 해제한 다음 이 함수를 호출해야만 합니다.
    *
    * @since GDAL 1.11
    */
   void CPL_DLL CPLVirtualMemManagerTerminate(void);

.. _implemented-by-gdalvirtualmemcpp:

gdalvirtualmem.cpp로 구현
~~~~~~~~~~~~~~~~~~~~~~~~~

::


   /** GDAL 데이터셋 객체로부터 CPLVirtualMem 객체를 생성합니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 이 메소드를 사용하면 이 데이터셋으로부터 하나 이상의 GDALRasterBands의
    * 한 영역에 대한 가상 메모리 객체를 생성할 수 있습니다. 가상 메모리 페이지에
    * 처음 접근할 때 데이터셋 콘텐츠로부터 가상 메모리 객체의 콘텐츠를
    * 자동으로 채우고, 캐시 용량 제한에 도달할 때 해제(또는 "지저분한"
    * 페이지인 경우 플러시)합니다.
    *
    * CPLVirtualMemGetAddr()를 사용해서 가상 메모리 객체에 접근하기 위한
    * 포인터를 가져옵니다. 이 포인터는 CPLVirtualMemFree()를 호출할 때까지
    * 무결합니다. 데이터셋 객체를 삭제(destroy)하기 전에 CPLVirtualMemFree()를
    * 호출해야만 합니다.
    *
    * 간격 파라미터의 기본값에서 p가 이런 포인터이고 base_type이 eBufType과
    * 일치하는 C 유형인 경우, ((base_type*)p)[x + y * nBufXSize +
    * (b-1)*nBufXSize*nBufYSize]로 밴드 b의 (xOff, yOff에 상대적인)
    * 이미지 좌표 (x, y) 요소에 접근할 수 있습니다.
    *
    * 메모리 페이지에 접근할 때 메모리 페이지를 투명하게 채우기 위해
    * 사용되는 메커니즘은 프로그램에서 메모리 오류가 발생할 때 일어나는 일과
    * 동일하지만 좀 더 제어된 방식이라는 점을 기억하십시오. 이런 일이 일어나는
    * 경우 디버깅 소프트웨어는 일반적으로 프로그램 실행을 중단할 것입니다.
    * 필요한 경우 CPLVirtualMemPin()을 사용해서 메모리 페이지에 접근하기 전에
    * 메모리 페이지를 할당하도록 보장하는 방식으로 이를 방지할 수 있습니다.
    *
    * 가상 메모리 객체로 매핑할 수 있는 영역의 용량은 하드웨어 및
    * 운영 체제의 제한 사항에 따라 달라질 수 있습니다.
    * 리눅스 AMD64 플랫폼 상에서 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 최대값은 2GB입니다.
    *
    * 버퍼의 데이터 유형(eBufType)이 GDALRasterBand의 버퍼 데이터 유형과
    * 다른 경우 자동으로 데이터 유형 변환을 수행합니다.
    *
    * 현재, 예를 들어 접근 중인 영역의 용량(nXSize x nYSize)이
    * 버퍼 용량(nBufXSize x nBufYSize)과 다를 경우
    * 이미지 제거(decimation)/복제는 지원하지 않습니다.
    *
    * nPixelSpace, nLineSpace 및 nBandSpace 파라미터는 다양한 버퍼 구성으로의
    * 읽기 및 다양한 버퍼 구성으로부터의 쓰기를 허용합니다. 간격 파라미터에
    * 임의의 값을 사용하는 것은 지원하지 않습니다. 간격 파라미터의 값은
    * 버퍼 데이터 유형의 용량의 배수여야만 하며, 밴드 순차 구성
    * (일반적으로 nPixelSpace = GDALGetDataTypeSize(eBufType) / 8, nLineSpace =
    * nPixelSpace * nBufXSize, nBandSpace = nLineSpace * nBufYSize) 또는
    * 픽셀 교차삽입 구성(typically nPixelSpace = nBandSpace * nBandCount,
    * nLineSpace = nPixelSpace * nBufXSize, nBandSpace =
    * GDALGetDataTypeSize(eBufType) / 8) 가운데 하나여야만 합니다.
    *
    * @param hDS 데이터셋 객체입니다.
    *
    * @param eRWFlag 데이터 영역을 읽기 위한 GF_Read 또는
    *                데이터 영역을 쓰기 위한 GF_Write 가운데 하나입니다.
    *
    * @param nXOff 접근할 밴드 영역의 좌상단 모서리에 대한 픽셀 오프셋입니다.
    *              좌측으로부터 시작하는 0일 것입니다.
    *
    * @param nYOff 접근할 밴드 영역의 좌상단 모서리에 대한 줄 오프셋입니다.
    *              상단으로부터 시작하는 0일 것입니다.
    *
    * @param nXSize 접근할 밴드 영역의 픽셀 단위 너비입니다.
    *
    * @param nYSize 접근할 밴드 영역의 줄 단위 높이입니다.
    *
    * @param nBufXSize 원하는 영역을 읽어들일, 또는 해당 버퍼로부터
    *                  원하는 영역을 작성할 버퍼 이미지의 너비입니다.
    *
    * @param nBufYSize 원하는 영역을 읽어들일, 또는 해당 버퍼로부터
    *                  원하는 영역을 작성할 버퍼 이미지의 높이입니다.
    *
    * @param eBufType 데이터 버퍼에 있는 픽셀값의 유형입니다.
    *                 GDALRasterBand 데이터 유형으로/부터 픽셀값을
    *                 필요한 대로 자동 변환할 것입니다.
    *
    * @param nBandCount 읽어올 또는 작성할 밴드의 번호입니다.
    *
    * @param panBandMap 읽어올 또는 작성할 nBandCount 밴드 번호 목록입니다.
    *                   밴드 번호는 1부터 시작한다는 사실을 기억하십시오.
    *                   첫 번째 nBandCount 밴드를 선택하기 위해 NULL일 수도 있습니다.
    *
    * @param nPixelSpace 버퍼에 있는 한 픽셀값의 시작으로부터 같은 스캔라인에 있는
    *                    다음 픽셀값의 시작까지의 바이트 오프셋입니다. 기본값 0으로
    *                    설정하는 경우 eBufType 데이터 유형의 용량을 사용합니다.
    *
    * @param nLineSpace 버퍼에 있는 한 스캔라인의 시작으로부터 다음 스캔라인의
    *                   시작까지의 바이트 오프셋입니다. 기본값 0으로 설정하는 경우
    *                   eBufType 데이터 유형의 용량을 nBufXSize로 곱한 값을 사용합니다.
    *
    * @param nBandSpace 한 밴드 데이터의 시작으로부터 다음 밴드 데이터의 시작까지의
    *                   바이트 오프셋입니다. 기본값 0으로 설정하는 경우 데이터 버퍼가
    *                   밴드 순차 구성이라는 사실을 암시하는 nLineSpace * nBufYSize
    *                   값을 사용할 것입니다.
    *
    * @param nCacheSize 실제로 할당될 바이트 단위 최대 메모리 용량입니다.
    *                   (이상적으로는 RAM 용량 이하여야만 합니다.)
    *
    * @param nPageSizeHint 페이지 용량에 대한 힌트입니다. CPLGetPageSize()가
    *                      반환한 시스템 페이지 용량의 배수여야만 합니다.
    *                      일반적으로 최소값은 4096입니다. 함수가 기본 페이지
    *                      용량을 결정하게 하려면 0으로 설정할 수도 있습니다.
    *
    * @param bSingleThreadUsage 가상 메모리 매핑에 동시에 접근할 스레드들이
    *                           없는 경우 TRUE로 설정하십시오. 이렇게 하면
    *                           성능을 조금 최적화할 수 있습니다. FALSE로 설정하는 경우 
    *                           CPLVirtualMemDeclareThread()를 반드시 호출해야만 합니다.
    *
    * @param papszOptions NULL로 종료되는 옵션 목록입니다. 현재 사용되지 않습니다.
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem CPL_DLL* GDALDatasetGetVirtualMem( GDALDatasetH hDS,
                                            GDALRWFlag eRWFlag,
                                            int nXOff, int nYOff,
                                            int nXSize, int nYSize,
                                            int nBufXSize, int nBufYSize,
                                            GDALDataType eBufType,
                                            int nBandCount, int* panBandMap,
                                            int nPixelSpace,
                                            GIntBig nLineSpace,
                                            GIntBig nBandSpace,
                                            size_t nCacheSize,
                                            size_t nPageSizeHint,
                                            int bSingleThreadUsage,
                                            char **papszOptions );

   /** GDAL 래스터 밴드 객체로부터 CPLVirtualMem 객체를 생성합니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 이 메소드를 사용하면 한 GDALRasterBand의 한 영역에 대한 가상 메모리 객체를
    * 생성할 수 있습니다. 가상 메모리 페이지에 처음 접근할 때 데이터셋
    * 콘텐츠로부터 가상 메모리 객체의 콘텐츠를 자동으로 채우고, 캐시 용량 제한에
    * 도달할 때 해제(또는 "지저분한" 페이지인 경우 플러시)합니다.
    *
    * CPLVirtualMemGetAddr()를 사용해서 가상 메모리 객체에 접근하기 위한
    * 포인터를 가져옵니다. 이 포인터는 CPLVirtualMemFree()를 호출할 때까지
    * 무결합니다. 데이터셋 객체를 삭제(destroy)하기 전에 CPLVirtualMemFree()를
    * 호출해야만 합니다.
    *
    * 간격 파라미터의 기본값에서 p가 이런 포인터이고 base_type이 eBufType과
    * 일치하는 C 유형인 경우, ((base_type*)p)[x + y * nBufXSize]로 밴드 b의
    * (xOff, yOff에 상대적인) 이미지 좌표 (x, y) 요소에 접근할 수 있습니다.
    *
    * 메모리 페이지에 접근할 때 메모리 페이지를 투명하게 채우기 위해
    * 사용되는 메커니즘은 프로그램에서 메모리 오류가 발생할 때 일어나는 일과
    * 동일하지만 좀 더 제어된 방식이라는 점을 기억하십시오. 이런 일이 일어나는
    * 경우 디버깅 소프트웨어는 일반적으로 프로그램 실행을 중단할 것입니다.
    * 필요한 경우 CPLVirtualMemPin()을 사용해서 메모리 페이지에 접근하기 전에
    * 메모리 페이지를 할당하도록 보장하는 방식으로 이를 방지할 수 있습니다.
    *
    * 가상 메모리 객체로 매핑할 수 있는 영역의 용량은 하드웨어 및
    * 운영 체제의 제한 사항에 따라 달라질 수 있습니다.
    * 리눅스 AMD64 플랫폼 상에서 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 최대값은 2GB입니다.
    *
    * 버퍼의 데이터 유형(eBufType)이 GDALRasterBand의 버퍼 데이터 유형과
    * 다른 경우 자동으로 데이터 유형 변환을 수행합니다.
    *
    * 현재, 예를 들어 접근 중인 영역의 용량(nXSize x nYSize)이
    * 버퍼 용량(nBufXSize x nBufYSize)과 다를 경우
    * 이미지 제거(decimation)/복제는 지원하지 않습니다.
    *
    * nPixelSpace 및 nLineSpace 파라미터는 다양한 버퍼 구성으로의
    * 읽기 및 다양한 버퍼 구성으로부터의 쓰기를 허용합니다. 간격 파라미터에
    * 임의의 값을 사용하는 것은 지원하지 않습니다. 간격 파라미터의 값은
    * 버퍼 데이터 유형의 용량의 배수여야만 하며, nLineSpace의 값이
    * nPixelSpace * nBufXSize 이상이어야만 합니다.
    *
    * @param hBand 래스터 밴드 객체입니다.
    *
    * @param eRWFlag 데이터 영역을 읽기 위한 GF_Read 또는
    *                데이터 영역을 쓰기 위한 GF_Write 가운데 하나입니다.
    *
    * @param nXOff 접근할 밴드 영역의 좌상단 모서리에 대한 픽셀 오프셋입니다.
    *              좌측으로부터 시작하는 0일 것입니다.
    *
    * @param nYOff 접근할 밴드 영역의 좌상단 모서리에 대한 줄 오프셋입니다
    *              상단으로부터 시작하는 0일 것입니다.
    *
    * @param nXSize 접근할 밴드 영역의 픽셀 단위 너비입니다.
    *
    * @param nYSize 접근할 밴드 영역의 줄 단위 높이입니다.
    *
    * @param nBufXSize 원하는 영역을 읽어들일, 또는 해당 버퍼로부터
    *                  원하는 영역을 작성할 버퍼 이미지의 너비입니다.
    *
    * @param nBufYSize 원하는 영역을 읽어들일, 또는 해당 버퍼로부터
    *                  원하는 영역을 작성할 버퍼 이미지의 높이입니다.
    *
    * @param eBufType 데이터 버퍼에 있는 픽셀값의 유형입니다.
    *                 GDALRasterBand 데이터 유형으로/부터 픽셀값을
    *                 필요한 대로 자동 변환할 것입니다.
    *
    * @param nPixelSpace 버퍼에 있는 한 픽셀값의 시작으로부터 같은 스캔라인에 있는
    *                    다음 픽셀값의 시작까지의 바이트 오프셋입니다. 기본값 0으로
    *                    설정하는 경우 eBufType 데이터 유형의 용량을 사용합니다.
    *
    * @param nLineSpace 버퍼에 있는 한 스캔라인의 시작으로부터 다음 스캔라인의
    *                   시작까지의 바이트 오프셋입니다. 기본값 0으로 설정하는 경우
    *                   eBufType 데이터 유형의 용량을 nBufXSize로 곱한 값을 사용합니다.
    *
    * @param nCacheSize 실제로 할당될 바이트 단위 최대 메모리 용량입니다.
    *                   (이상적으로는 RAM 용량 이하여야만 합니다.)
    *
    * @param nPageSizeHint 페이지 용량에 대한 힌트입니다. CPLGetPageSize()가
    *                      반환한 시스템 페이지 용량의 배수여야만 합니다.
    *                      일반적으로 최소값은 4096입니다. 함수가 기본 페이지
    *                      용량을 결정하게 하려면 0으로 설정할 수도 있습니다.
    *
    * @param bSingleThreadUsage 가상 메모리 매핑에 동시에 접근할 스레드들이
    *                           없는 경우 TRUE로 설정하십시오. 이렇게 하면
    *                           성능을 조금 최적화할 수 있습니다. FALSE로 설정하는 경우 
    *                           CPLVirtualMemDeclareThread()를 반드시 호출해야만 합니다.
    *
    * @param papszOptions NULL로 종료되는 옵션 목록입니다. 현재 사용되지 않습니다.
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem CPL_DLL* GDALRasterBandGetVirtualMem( GDALRasterBandH hBand,
                                            GDALRWFlag eRWFlag,
                                            int nXOff, int nYOff,
                                            int nXSize, int nYSize,
                                            int nBufXSize, int nBufYSize,
                                            GDALDataType eBufType,
                                            int nPixelSpace,
                                            GIntBig nLineSpace,
                                            size_t nCacheSize,
                                            size_t nPageSizeHint,
                                            int bSingleThreadUsage,
                                            char **papszOptions );

   typedef enum
   {
       /*! 픽셀이 교차삽입된 타일(Tile Interleaved by Pixel):
           픽셀 구성으로 교차삽입된 내부 밴드를 가진 타일 (0,0), 타일 (1,0), ... */
       GTO_TIP,
       /*! 타일이 교차삽입된 밴드(Band Interleaved by Tile):
           첫 번째 밴드의 타일 (0,0), 두 번째 밴드의 타일 (0,0), ...
           첫 번째 밴드의 타일 (1,0), 두 번째 밴드의 타일 (1,0), ... */
       GTO_BIT,
       /*! 밴드 순차(Band SeQuential):
           첫 번째 밴드의 모든 타일, 다음 밴드의 모든 타일, ... */
       GTO_BSQ
   } GDALTileOrganization;

   /** GDAL 데이터셋 객체로부터 타일 구성을 사용해서 CPLVirtualMem 객체를 생성합니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 이 메소드를 사용하면 이 데이터셋으로부터 하나 이상의 GDALRasterBands의
    * 한 영역에 대한 가상 메모리 객체를 생성할 수 있습니다. 가상 메모리 페이지에
    * 처음 접근할 때 데이터셋 콘텐츠로부터 가상 메모리 객체의 콘텐츠를
    * 자동으로 채우고, 캐시 용량 제한에 도달할 때 해제(또는 "지저분한"
    * 페이지인 경우 플러시)합니다.
    *
    * GDALDatasetGetVirtualMem()과는 반대로, 스캔라인 대신 타일이 픽셀을 구성합니다.
    * eTileOrganization 파라미터로 타일 내부 및 타일 전반의 서로 다른 픽셀 구성
    * 방식을 선택할 수 있습니다.
    *
    * nXSize가 nTileXSize의 배수가 아니거나 nYSize가 nTileYSize의 배수가 아닌 경우,
    * 관심 영역의 우측 그리고/또는 하단에 부분 타일들이 존재할 것입니다.
    * 이런 부분 타일들 또한 채워넣기(padding) 픽셀로 nTileXSize * nTileYSize
    * 크기를 가질 것입니다.
    *
    * CPLVirtualMemGetAddr()를 사용해서 가상 메모리 객체에 접근하기 위한
    * 포인터를 가져옵니다. 이 포인터는 CPLVirtualMemFree()를 호출할 때까지
    * 무결합니다. 데이터셋 객체를 삭제(destroy)하기 전에 CPLVirtualMemFree()를
    * 호출해야만 합니다.
    *
    * 간격 파라미터의 기본값에서 p가 이런 포인터이고 base_type이 eBufType과
    * 일치하는 C 유형인 경우, 다음으로 밴드 b의 (xOff, yOff에 상대적인)
    * 이미지 좌표 (x, y) 요소에 접근할 수 있습니다:
    *  - eTileOrganization = GTO_TIP인 경우, ((base_type*)p)[tile_number(x,y)*nBandCount*tile_size + offset_in_tile(x,y)*nBandCount + (b-1)].
    *  - eTileOrganization = GTO_BIT인 경우, ((base_type*)p)[(tile_number(x,y)*nBandCount + (b-1)) * tile_size + offset_in_tile(x,y)].
    *  - eTileOrganization = GTO_BSQ인 경우, ((base_type*)p)[(tile_number(x,y) + (b-1)*nTilesCount) * tile_size + offset_in_tile(x,y)].
    *
    * 이때 nTilesPerRow = ceil(nXSize / nTileXSize)
    *      nTilesPerCol = ceil(nYSize / nTileYSize)
    *      nTilesCount = nTilesPerRow * nTilesPerCol
    *      tile_number(x,y) = (y / nTileYSize) * nTilesPerRow + (x / nTileXSize)
    *      offset_in_tile(x,y) = (y % nTileYSize) * nTileXSize  + (x % nTileXSize)
    *      tile_size = nTileXSize * nTileYSize
    *
    * 단일 밴드 요청의 경우 모든 타일 구성이 동등하다는 사실을 기억하십시오.
    *
    * 메모리 페이지에 접근할 때 메모리 페이지를 투명하게 채우기 위해
    * 사용되는 메커니즘은 프로그램에서 메모리 오류가 발생할 때 일어나는 일과
    * 동일하지만 좀 더 제어된 방식이라는 점을 기억하십시오. 이런 일이 일어나는
    * 경우 디버깅 소프트웨어는 일반적으로 프로그램 실행을 중단할 것입니다.
    * 필요한 경우 CPLVirtualMemPin()을 사용해서 메모리 페이지에 접근하기 전에
    * 메모리 페이지를 할당하도록 보장하는 방식으로 이를 방지할 수 있습니다.
    *
    * 가상 메모리 객체로 매핑할 수 있는 영역의 용량은 하드웨어 및
    * 운영 체제의 제한 사항에 따라 달라질 수 있습니다.
    * 리눅스 AMD64 플랫폼 상에서 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 최대값은 2GB입니다.
    *
    * 버퍼의 데이터 유형(eBufType)이 GDALRasterBand의 버퍼 데이터 유형과
    * 다른 경우 자동으로 데이터 유형 변환을 수행합니다.
    *
    * @param hDS 데이터셋 객체입니다.
    *
    * @param eRWFlag 데이터 영역을 읽기 위한 GF_Read 또는
    *                데이터 영역을 쓰기 위한 GF_Write 가운데 하나입니다.
    *
    * @param nXOff 접근할 밴드 영역의 좌상단 모서리에 대한 픽셀 오프셋입니다.
    *              좌측으로부터 시작하는 0일 것입니다.
    *
    * @param nYOff 접근할 밴드 영역의 좌상단 모서리에 대한 줄 오프셋입니다
    *              상단으로부터 시작하는 0일 것입니다.
    *
    * @param nXSize 접근할 밴드 영역의 픽셀 단위 너비입니다.
    *
    * @param nYSize 접근할 밴드 영역의 줄 단위 높이입니다.
    *
    * @param nTileXSize 타일의 너비입니다.
    *
    * @param nTileYSize 타일의 높이입니다.
    *
    * @param eBufType 데이터 버퍼에 있는 픽셀값의 유형입니다.
    *                 GDALRasterBand 데이터 유형으로/부터 픽셀값을
    *                 필요한 대로 자동 변환할 것입니다.
    *
    * @param nBandCount 읽어올 또는 작성할 밴드의 번호입니다.
    *
    * @param panBandMap 읽어올 또는 작성할 nBandCount 밴드 번호 목록입니다.
    *                   밴드 번호는 1부터 시작한다는 사실을 기억하십시오.
    *                   첫 번째 nBandCount 밴드를 선택하기 위해 NULL일 수도 있습니다.
    *
    * @param eTileOrganization 타일 구성입니다.
    *
    * @param nCacheSize 실제로 할당될 바이트 단위 최대 메모리 용량입니다.
    *                   (이상적으로는 RAM 용량 이하여야만 합니다.)
    *
    * @param bSingleThreadUsage 가상 메모리 매핑에 동시에 접근할 스레드들이
    *                           없는 경우 TRUE로 설정하십시오. 이렇게 하면
    *                           성능을 조금 최적화할 수 있습니다. FALSE로 설정하는 경우 
    *                           CPLVirtualMemDeclareThread()를 반드시 호출해야만 합니다.
    *
    * @param papszOptions NULL로 종료되는 옵션 목록입니다. 현재 사용되지 않습니다.
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem CPL_DLL* GDALDatasetGetTiledVirtualMem( GDALDatasetH hDS,
                                                 GDALRWFlag eRWFlag,
                                                 int nXOff, int nYOff,
                                                 int nXSize, int nYSize,
                                                 int nTileXSize, int nTileYSize,
                                                 GDALDataType eBufType,
                                                 int nBandCount, int* panBandMap,
                                                 GDALTileOrganization eTileOrganization,
                                                 size_t nCacheSize,
                                                 int bSingleThreadUsage,
                                                 char **papszOptions );

   /** GDAL 데이터셋 객체로부터 타일 구성을 사용해서 CPLVirtualMem 객체를 생성합니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 이 메소드를 사용하면 한 GDALRasterBand의 한 영역에 대한 가상 메모리 객체를
    * 생성할 수 있습니다. 가상 메모리 페이지에 처음 접근할 때 데이터셋
    * 콘텐츠로부터 가상 메모리 객체의 콘텐츠를 자동으로 채우고, 캐시 용량 제한에
    * 도달할 때 해제(또는 "지저분한" 페이지인 경우 플러시)합니다.
    *
    * GDALDatasetGetVirtualMem()과는 반대로, 스캔라인 대신 타일이 픽셀을 구성합니다.
    *
    * nXSize가 nTileXSize의 배수가 아니거나 nYSize가 nTileYSize의 배수가 아닌 경우,
    * 관심 영역의 우측 그리고/또는 하단에 부분 타일들이 존재할 것입니다.
    * 이런 부분 타일들 또한 채워넣기(padding) 픽셀로 nTileXSize * nTileYSize
    * 크기를 가질 것입니다.
    *
    * CPLVirtualMemGetAddr()를 사용해서 가상 메모리 객체에 접근하기 위한
    * 포인터를 가져옵니다. 이 포인터는 CPLVirtualMemFree()를 호출할 때까지
    * 무결합니다. 데이터셋 객체를 삭제(destroy)하기 전에 CPLVirtualMemFree()를
    * 호출해야만 합니다.
    *
    * 간격 파라미터의 기본값에서 p가 이런 포인터이고 base_type이 eBufType과
    * 일치하는 C 유형인 경우, 다음으로 밴드 b의 (xOff, yOff에 상대적인)
    * 이미지 좌표 (x, y) 요소에 접근할 수 있습니다:
    * ((base_type*)p)[tile_number(x,y)*tile_size + offset_in_tile(x,y)].
    *
    * 이때 nTilesPerRow = ceil(nXSize / nTileXSize)
    *      nTilesCount = nTilesPerRow * nTilesPerCol
    *      tile_number(x,y) = (y / nTileYSize) * nTilesPerRow + (x / nTileXSize)
    *      offset_in_tile(x,y) = (y % nTileYSize) * nTileXSize  + (x % nTileXSize)
    *      tile_size = nTileXSize * nTileYSize
    *
    * 메모리 페이지에 접근할 때 메모리 페이지를 투명하게 채우기 위해
    * 사용되는 메커니즘은 프로그램에서 메모리 오류가 발생할 때 일어나는 일과
    * 동일하지만 좀 더 제어된 방식이라는 점을 기억하십시오. 이런 일이 일어나는
    * 경우 디버깅 소프트웨어는 일반적으로 프로그램 실행을 중단할 것입니다.
    * 필요한 경우 CPLVirtualMemPin()을 사용해서 메모리 페이지에 접근하기 전에
    * 메모리 페이지를 할당하도록 보장하는 방식으로 이를 방지할 수 있습니다.
    *
    * 가상 메모리 객체로 매핑할 수 있는 영역의 용량은 하드웨어 및
    * 운영 체제의 제한 사항에 따라 달라질 수 있습니다.
    * 리눅스 AMD64 플랫폼 상에서 최대값은 128TB입니다.
    * 리눅스 x86 플랫폼 상에서 최대값은 2GB입니다.
    *
    * 버퍼의 데이터 유형(eBufType)이 GDALRasterBand의 버퍼 데이터 유형과
    * 다른 경우 자동으로 데이터 유형 변환을 수행합니다.
    *
    * @param hBand 래스터 밴드 객체입니다.
    *
    * @param eRWFlag 데이터 영역을 읽기 위한 GF_Read 또는
    *                데이터 영역을 쓰기 위한 GF_Write 가운데 하나입니다.
    *
    * @param nXOff 접근할 밴드 영역의 좌상단 모서리에 대한 픽셀 오프셋입니다.
    *              좌측으로부터 시작하는 0일 것입니다.
    *
    * @param nYOff 접근할 밴드 영역의 좌상단 모서리에 대한 줄 오프셋입니다
    *              상단으로부터 시작하는 0일 것입니다.
    *
    * @param nXSize 접근할 밴드 영역의 픽셀 단위 너비입니다.
    *
    * @param nYSize 접근할 밴드 영역의 줄 단위 높이입니다.
    *
    * @param nTileXSize 타일의 너비입니다.
    *
    * @param nTileYSize 타일의 높이입니다.
    *
    * @param eBufType 데이터 버퍼에 있는 픽셀값의 유형입니다.
    *                 GDALRasterBand 데이터 유형으로/부터 픽셀값을
    *                 필요한 대로 자동 변환할 것입니다.
    *
    * @param nCacheSize 실제로 할당될 바이트 단위 최대 메모리 용량입니다.
    *                   (이상적으로는 RAM 용량 이하여야만 합니다.)
    *
    * @param bSingleThreadUsage 가상 메모리 매핑에 동시에 접근할 스레드들이
    *                           없는 경우 TRUE로 설정하십시오. 이렇게 하면
    *                           성능을 조금 최적화할 수 있습니다. FALSE로 설정하는 경우 
    *                           CPLVirtualMemDeclareThread()를 반드시 호출해야만 합니다.
    *
    * @param papszOptions NULL로 종료되는 옵션 목록입니다. 현재 사용되지 않습니다.
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem CPL_DLL* GDALRasterBandGetTiledVirtualMem( GDALRasterBandH hBand,
                                                 GDALRWFlag eRWFlag,
                                                 int nXOff, int nYOff,
                                                 int nXSize, int nYSize,
                                                 int nTileXSize, int nTileYSize,
                                                 GDALDataType eBufType,
                                                 size_t nCacheSize,
                                                 int bSingleThreadUsage,
                                                 char **papszOptions );

.. _implemented-by-gdalrasterbandcpp:

gdalrasterband.cpp로 구현
~~~~~~~~~~~~~~~~~~~~~~~~~

::


   /** \brief GDAL 래스터 밴드 객체로부터 CPLVirtualMem 객체를 생성합니다.
    *
    * 현재 리눅스 상에서만 지원됩니다.
    *
    * 이 메소드를 사용하면 GDALRasterBand로부터 전체 이미지 데이터를 가상 배열로
    * 노출시키는 가상 메모리 객체를 생성할 수 있습니다.
    *
    * 기본 구현은 GDALRasterBandGetVirtualMem()에 의존하지만, 원시 파일 용 같은
    * 특수 구현은 기저 파일의 뷰를 가상 메모리로 생성하는 운영 체제의 메커니즘을
    * ( CPLVirtualMemFileMapNew() ) 직접 이용할 수도 있습니다.
    *
    * At the time of writing, the GeoTIFF driver and "raw" drivers (EHdr, ...) offer
    * a specialized implementation with direct file mapping, provided that some
    * requirements are met :
    *   - for all drivers, the dataset must be backed by a "real" file in the file
    *     system, and the byte ordering of multi-byte datatypes (Int16, etc.)
    *     must match the native ordering of the CPU.
    *   - in addition, for the GeoTIFF driver, the GeoTIFF file must be uncompressed, scanline
    *     oriented (i.e. not tiled). Strips must be organized in the file in sequential
    *     order, and be equally spaced (which is generally the case). Only power-of-two
    *     bit depths are supported (8 for GDT_Bye, 16 for GDT_Int16/GDT_UInt16,
    *     32 for GDT_Float32 and 64 for GDT_Float64)
    *
    * The pointer returned remains valid until CPLVirtualMemFree() is called.
    * CPLVirtualMemFree() must be called before the raster band object is destroyed.
    *
    * p가 이런 포인터이고 base_type이 GDALGetRasterDataType()과 일치하는
    * 유형인 경우, 다음으로 이미지 좌표 (x, y) 요소에 접근할 수 있습니다:
    * *(base_type*) ((GByte*)p + x * *pnPixelSpace + y * *pnLineSpace)
    *
    * This method is the same as the C GDALGetVirtualMemAuto() function.
    *
    * @param eRWFlag Either GF_Read to read the band, or GF_Write to
    * read/write the band.
    *
    * @param pnPixelSpace 버퍼에 있는 한 픽셀값의 시작으로부터 같은 스캔라인에 있는
    *                     다음 픽셀값의 시작까지의 바이트 오프셋을 지정하는 
    *                     산출 파라미터입니다.
    *
    * @param pnLineSpace 버퍼에 있는 한 스캔라인의 시작으로부터 다음 스캔라인의
    *                    시작까지의 바이트 오프셋을 지정하는 산출 파라미터입니다.
    *
    * @param papszOptions NULL로 종료되는 옵션 목록입니다.
    *                     If a specialized implementation exists, defining USE_DEFAULT_IMPLEMENTATION=YES
    *                     will cause the default implementation to be used.
    *                     When requiring or falling back to the default implementation, the following
    *                     options are available : CACHE_SIZE (in bytes, defaults to 40 MB),
    *                     PAGE_SIZE_HINT (in bytes),
    *                     SINGLE_THREAD ("FALSE" / "TRUE", defaults to FALSE)
    *
    * @return CPLVirtualMemFree()로 해제해야만 하는 가상 메모리 객체를,
    *         또는 실패하는 경우 NULL을 반환합니다.
    *
    * @since GDAL 1.11
    */

   CPLVirtualMem  *GDALRasterBand::GetVirtualMemAuto( GDALRWFlag eRWFlag,
                                                      int *pnPixelSpace,
                                                      GIntBig *pnLineSpace,
                                                      char **papszOptions ):

   CPLVirtualMem CPL_DLL* GDALGetVirtualMemAuto( GDALRasterBandH hBand,
                                                 GDALRWFlag eRWFlag,
                                                 int *pnPixelSpace,
                                                 GIntBig *pnLineSpace,
                                                 char **papszOptions );

이식성
------

The CPLVirtualMem low-level machinery is only implemented for Linux now.
It assumes that returning from a SIGSEGV handler is possible, which is a
blatant violation of POSIX, but in practice it seems that most POSIX
(and non POSIX such as Windows) systems should be able to resume
execution after a segmentation fault.

Porting to other POSIX operating systems such as MacOSX should be doable
with moderate effort. Windows has API that offer similar capabilities as
POSIX API with VirtualAlloc(), VirtualProtect() and
SetUnhandledExceptionFilter(), although the porting would undoubtly
require more effort.

The existence of `libsigsegv <http://www.gnu.org/software/libsigsegv>`_
that run on various OS is an evidence on its capacity of being ported to
other platforms.

The trickiest part is ensuring that things will work reliably when two
concurrent threads that try to access the same initially unmapped page.
Without special care, one thread could manage to access the page that is
being filled by the other thread, before it is completely filled. On
Linux this can be easily avoided with the mremap() call. When a page is
filled, we don't actually pass the target page to the user callback, but
a temporary page. When the callback has finished its job, this temporary
page is mremap()'ed to its target location, which is an atomic
operation. An alternative implementation for POSIX systems that don't
have this mremap() call has been tested : any declared threads that can
access the memory mapping are paused before the temporary page is
memcpy'ed to its target location, and are resumed afterwards. This
requires threads to priorly declare their "interest" for a memory
mapping with CPLVirtualMemDeclareThread(). Pausing a thread is
interestingly non-obvious : the solution found to do so is to send it a
SIGUSR1 signal and make it wait in a signal handler for this SIGUSR1
signal... It has not been investigated if/how this could be done on
Windows. CPLVirtualMemIsAccessThreadSafe() has been introduced for that
purpose.

As far as CPLVirtualMemFileMapNew() is concerned, memory file mapping on
POSIX systems with mmap() should be portable. Windows has
CreateFileMapping() and MapViewOfFile() API that have similar
capabilities as mmap().

성능
----

No miraculous performance gain should be expected from this new
capability, when compared to code that carefully uses GDALRasterIO().
Handling segmentation faults has a cost ( the operating system catches a
hardware exception, then calls the user program segmentation fault
handler, which does the normal GDAL I/O operations, and plays with page
mappings and permissions which invalidate some CPU caches, etc... ).
However, when a page has been realized, access to it should be really
fast, so with appropriate access patterns and cache size, good
performance should be expected.

It should also be noted that in the current implementation, the
realization of pages is done in a serialized way, that is to say if 2
threads which use 2 different memory mappings cause a segmentation fault
at the same time, they will not be dealt by 2 different threads, but one
after the other one.

The overhead of virtual memory objects returned by GetVirtualMemAuto(),
when using the memory file mapping, should be lesser than the manual
management of page faults. However, GDAL has no control of the strategy
used by the operating system to cache pages.

제한 사항
---------

The maximum size of the virtual memory space (and thus a virtual memory
mapping) depends on the CPU architecture and OS limitations :

-  on Linux AMD64, 128 TB.
-  on Linux x86, 2 GB.
-  On Windows AMD64 (unsupported by the current implementation), 8 TB.
-  On Windows x86 (unsupported by the current implementation), 2 GB.

Clearly, the main interest of this new functionality is for AMD64
platforms.

On a Linux AMD64 machine with 4 GB RAM, the Python binding of
GDALDatasetGetTiledVirtualMem() has been successfully used to access
random points on the new `Europe 3'' DEM
dataset <http://www.eea.europa.eu/data-and-maps/data/eu-dem/#tab-original-data>`_,
which is a 20 GB compressed GeoTIFF ( and 288000 \* 180000 \* 4 = 193 GB
uncompressed )

관련 메모
---------

Some issues with system calls such as read() or write(), or easier
multi-threading could potentially be solved by making a FUSE (File
system in USEr space) driver that would expose a GDAL dataset as a file,
and the mmap()'ing the file itself. However FUSE drivers are only
available on POSIX OS, and need root privilege to be mounted (a FUSE
filesystem does not need root privilege to run, but the mounting
operation does).

질문
----

현재 리눅스 상에서만 작동한다는 사실로 인해 현재로서는 이 API를 실험적인 것으로 표시해야 하는지?

하위 호환성 문제점
------------------

-  C/C++ API --> 호환 가능 (새 API)
-  C ABI --> 호환 가능 (새 API)
-  C++ ABI --> :cpp:class:`GDALRasterBand` 클래스에 새 가상 메소드가 추가되었기 때문에 호환 불가능

업데이트된 드라이버들
---------------------

RawRasterBand 객체 및 GeoTIFF 드라이버가 GetVirtualMemAuto() 메소드를 구현하고, 가능한 경우 메모리 파일 매핑을 제공하도록 업데이트할 것입니다. (가능한 경우에 대해서는 앞에 작성한 제한 사항을 참조하십시오.)

향후 단계에서 (VRTRawRasterBand를 위한) VRT 드라이버 같은 다른 드라이버들도 GetVirtualMemAuto() 메소드의 특수 구현을 제공할 수 있을 것입니다.

SWIG 바인딩
-----------

The high level API (dataset and raster band) API is available in Python
bindings.

GDALDatasetGetVirtualMem() is mapped as Dataset.GetVirtualArray(), which
returns a NumPy array.

::

       def GetVirtualMemArray(self, eAccess = gdalconst.GF_Read, xoff=0, yoff=0,
                              xsize=None, ysize=None, bufxsize=None, bufysize=None,
                              datatype = None, band_list = None, band_sequential = True,
                              cache_size = 10 * 1024 * 1024, page_size_hint = 0, options = None):
           """Return a NumPy array for the dataset, seen as a virtual memory mapping.
              If there are several bands and band_sequential = True, an element is
              accessed with array[band][y][x].
              If there are several bands and band_sequential = False, an element is
              accessed with array[y][x][band].
              If there is only one band, an element is accessed with array[y][x].
              Any reference to the array must be dropped before the last reference to the
              related dataset is also dropped.
           """

Similarly for GDALDatasetGetTiledVirtualMem() :

::

       def GetTiledVirtualMemArray(self, eAccess = gdalconst.GF_Read, xoff=0, yoff=0,
                              xsize=None, ysize=None, tilexsize=256, tileysize=256,
                              datatype = None, band_list = None, tile_organization = gdalconst.GTO_BSQ,
                              cache_size = 10 * 1024 * 1024, options = None):
           """Return a NumPy array for the dataset, seen as a virtual memory mapping with
              a tile organization.
              If there are several bands and tile_organization = gdal.GTO_BIP, an element is
              accessed with array[tiley][tilex][y][x][band].
              If there are several bands and tile_organization = gdal.GTO_BTI, an element is
              accessed with array[tiley][tilex][band][y][x].
              If there are several bands and tile_organization = gdal.GTO_BSQ, an element is
              accessed with array[band][tiley][tilex][y][x].
              If there is only one band, an element is accessed with array[tiley][tilex][y][x].
              Any reference to the array must be dropped before the last reference to the
              related dataset is also dropped.
           """

And the Band object has the following 3 methods :

::

     def GetVirtualMemArray(self, eAccess = gdalconst.GF_Read, xoff=0, yoff=0,
                            xsize=None, ysize=None, bufxsize=None, bufysize=None,
                            datatype = None,
                            cache_size = 10 * 1024 * 1024, page_size_hint = 0, options = None):
           """Return a NumPy array for the band, seen as a virtual memory mapping.
              An element is accessed with array[y][x].
              Any reference to the array must be dropped before the last reference to the
              related dataset is also dropped.
           """

     def GetVirtualMemAutoArray(self, eAccess = gdalconst.GF_Read, options = None):
           """Return a NumPy array for the band, seen as a virtual memory mapping.
              An element is accessed with array[y][x].

     def GetTiledVirtualMemArray(self, eAccess = gdalconst.GF_Read, xoff=0, yoff=0,
                              xsize=None, ysize=None, tilexsize=256, tileysize=256,
                              datatype = None,
                              cache_size = 10 * 1024 * 1024, options = None):
           """Return a NumPy array for the band, seen as a virtual memory mapping with
              a tile organization.
              An element is accessed with array[tiley][tilex][y][x].
              Any reference to the array must be dropped before the last reference to the
              related dataset is also dropped.
           """

Note: dataset/Band.GetVirtualMem()/GetTiledVirtualMem() methods are also
available. They return a VirtualMem python object that has a GetAddr()
method that returns a Python memoryview object (Python 2.7 or later
required). However, using such object does not seem practical for
non-Byte data types.

테스트 스위트
-------------

The autotest suite will be extended to test the Python API of this RFC.
It will also test the specialized implementations of GetVirtualMemAuto()
in RawRasterBand and the GeoTIFF drivers. In autotest/cpp, a
test_virtualmem.cpp file tests concurrent access to the same pages by 2
threads.

구현
----

이벤 루올이 GDAL/OGR 트렁크에 이 RFC를 구현할 것입니다.
제안한 구현을 `패치 <https://trac.osgeo.org/gdal/attachment/wiki/rfc45_virtualmem/virtualmem.patch>`_ 로 첨부했습니다.

투표 이력
---------

-  이벤 루올 +1
-  프랑크 바르메르담 +1
-  대니얼 모리셋 +1
-  유카 라흐코넨 +1

