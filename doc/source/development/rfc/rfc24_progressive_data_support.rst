.. _rfc-24:

================================================================================
RFC 24: GDAL 점진적 데이터 지원
================================================================================

.. highlight:: cpp

저자: 노먼 바커(Norman Barker), 프랑크 바르메르담(Frank Warmerdam)

연락처: nbarker@ittvis.com, warmerdam@pobox.com

상태: 승인

요약
----

GDAL에 비동기/스트리밍 데이터 접근을 위한 인터페이스를 추가할 것을 제안합니다. 초기 구현은 JPIP(JPEG 2000 Interactive Protocol) 용이지만, 다른 스트리밍/점진적 접근법에 적용할 수 있을 만큼 일반적이어야 합니다. `이 페이지 <https://trac.osgeo.org/gdal/wiki/rfc24_jpipkak>`_ 에서 JPIP (카카두) 구현에 대한 배경을 찾아볼 수 있습니다.

인터페이스
----------

GDALAsyncReader
~~~~~~~~~~~~~~~

이 새 클래스의 목적은 활성 비동기 래스터 영상 요청을 표현하는 것입니다. 이 요청에는 요청하는 데이터셋 상의 소스 윈도우, (제거(decimation) 또는 복제 수준을 암시하는) 대상 버퍼 크기, 버퍼 유형, 버퍼 교차삽입, 데이터 버퍼 그리고 밴드에 대한 정보가 포함됩니다. 본질적으로 :cpp:func:`GDALDataset::!RasterIO` 요청에 전송되는 정보와 동일합니다.

:cpp:func:`GetNextUpdatedRegion` 메소드를 사용해서 영상 버퍼의 업데이트를 대기하고 어떤 영역이 업데이트되었는지 찾아낼 수 있습니다. :cpp:func:`LockBuffer` 및 :cpp:func:`UnlockBuffer` 메소드를 사용하면 응용 프로그램 코드가 버퍼에 접근하는 동안 버퍼 업데이트를 임시로 비활성화시킬 수 있습니다.

이 단순 접근자 구현을 :cpp:class:`GDALAsyncReader` 클래스의 일부로 제공하긴 하지만, 그 목적은 이 클래스를 특정 드라이버의 구현 그리고 지정한 :cpp:func:`GetNextUpdatedRegion`, :cpp:func:`LockBuffer` 및 :cpp:func:`UnlockBuffer` 의 사용자 지정 구현의 일부로서 하위 클래스화시키는 것입니다.

.. code-block:: c

   {{{ class CPL_DLL GDALAsyncReader { protected: GDALDataset\* poDS; int nXOff; int nYOff; int nXSize; int nYSize; void \* pBuf; int nBufXSize; int nBufYSize; GDALDataType eBufType; int nBandCount; int\* panBandMap; int nPixelSpace; int nLineSpace; int nBandSpace; long nDataRead;

   public: GDALAsyncReader(GDALDataset\* poDS = NULL); virtual ~GDALAsyncReader();

      GDALDataset* GetGDALDataset() {return poDS;}
      int GetXOffset() {return nXOff;}
      int GetYOffset() {return nYOff;}
      int GetXSize() {return nXSize;}
      int GetYSize() {return nYSize;}
      void * GetBuffer() {return pBuf;}
      int GetBufferXSize() {return nBufXSize;}
      int GetBufferYSize() {return nBufYSize;}
      GDALDataType GetBufferType() {return eBufType;}
      int GetBandCount() {return nBandCount;}
      int* GetBandMap() {return panBandMap;}
      int GetPixelSpace() {return nPixelSpace;}
      int GetLineSpace() {return nLineSpace;}
      int GetBandSpace() {return nBandSpace;}

      virtual GDALAsyncStatusType GetNextUpdatedRegion(double dfTimeout,
                                                       int* pnBufXOff,
                                                       int* pnBufYOff,
                                                       int* pnBufXSize,
                                                       int* pnBufXSize) = 0;

      virtual int LockBuffer( double dfTimeout );
      virtual void UnlockBuffer(); 

      friend class GDALDataset;

   }; }}}

GetNextUpdatedRegion()
~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   GDALAsyncStatusType 
   GDALAsyncRasterio::GetNextUpdatedRegion(int dfTimeout,
                                           int* pnBufXOff, int* pnBufYOff,
                                           int* pnBufXSize, int* pnBufXSize);

   int dfTimeout;
     // 결과물 대기 시간을 초 단위로 측정한 값입니다.
     // 이 값이 0인 경우 사용할 수 있는 작업을 처리할 수도 있지만
     // 더 많은 영상이 도착할 때까지 대기해서는 안 됩니다.
     // 이 값이 -1.0이면 새 데이터를 시간 제한 없이 대기한다는 의미입니다.
     // 그래도 사용할 수 있는 영상을 처리하는 데 임의의 시간이 걸릴 수도 있습니다.

   int *pnBufXOff, *pnBufYOff, *pnBufXSize, *pnBufYSize;
     // 이 변수들이 비동기 I/O 영상 버퍼 내에서 업데이트된 데이터의 윈도우를 반환합니다.
     // 이 정보를 사용해서 변경되었을 수도 있는 영상의 일부분에 대한
     // 스크린 다시 그리기 또는 기타 처리를 제한할 수 있습니다.

비동기 반환 상태 목록은 다음과 같으며, :file:`gdal.h` 에 선언될 것입니다.

.. code-block::

   typedef enum 
   {   
       GARIO_PENDING = 0,
       GARIO_UPDATE = 1,
       GARIO_ERROR = 2,
       GARIO_COMPLETE = 3,
       GARIO_TypeCount = 4
   } GDALAsyncStatusType;

반환값의 의미는 다음과 같습니다:

-  GARIO_PENDING:
   버퍼에서 어떤 영상도 변경되지 않았지만 대기 중인 활동이 있으며 시간이 허용되는 한 응용 프로그램이 :cpp:func:`GetNextUpdatedRegion` 을 호출해야 합니다.
-  GARIO_UPDATE:
   일부 영상이 업데이트되었지만 대기 중인 활동이 있습니다.
-  GARIO_ERROR:
   무언가 잘못되었습니다. 비동기 요청을 종료해야 합니다.
-  GARIO_COMPLETE:
   업데이트가 발생했으며 이 요청에 대한 대기 작업이 더 이상 없습니다. 요청을 종료하고 사용한 버퍼를 해제해야 합니다.

GDALDataset
~~~~~~~~~~~

비동기 판독기를 생성하고 정리하는 메소드들을 추가해서 :cpp:class:`GDALDataset` 클래스를 확장합니다. 그 목적은 이 메소드들을 비동기 데이터 접근을 구현하는 드라이버의 하위 클래스로 만드는 것입니다.

.. code-block::

       virtual GDALAsyncReader* 
           BeginAsyncReader(int nXOff, int nYOff, int nXSize, int nYSize,
                              void *pBuf, int nBufXSize, int nBufYSize,
                              GDALDataType eBufType,
                              int nBandCount, int* panBandMap,
                              int nPixelSpace, int nLineSpace, int nBandSpace,
                              char **papszOptions);
       virtual void EndAsyncReader(GDALAsyncReader *);

:cpp:func:`GDALDataset::!RasterIO` 만 사용해서 요청을 단일 블록 작업 요청으로 수행하는 기본 :cpp:class:`!GDALAsyncReader` 구현을 :file:`gdal/gcore` 의 일부분으로서 제공할 것으로 예상됩니다. 하지만, 이 기본 구현은 특정 포맷이 실제로 비동기적으로 작동하느냐와 상관없이 응용 프로그램이 비동기 인터페이스를 사용할 수 있도록 보장할 것입니다.

GDALDriver
~~~~~~~~~~

응용 프로그램에 특정 포맷이 비동기 I/O를 지원하는지 여부에 관한 힌트를 제공하기 위해, 구현되는 포맷의 :cpp:class:`GDALDriver` 클래스에 새로운 메타데이터 항목을 추가할 것입니다. 이 메타데이터 항목이 "DCAP_ASYNCIO"(GDAL_DCAP_ASYNCIO 매크로)이며 비동기 I/O를 사용할 수 있는 경우 YES 값을 가질 것입니다.

구현되는 드라이버는 드라이버 설정 코드 안에 다음과 같은 코드를 실행하게 될 것입니다:

.. code-block::

      poDriver->SetMetadataItem( GDAL_DCAP_ASYNCIO, "YES" );

GDALRasterBand
~~~~~~~~~~~~~~

비동기 I/O 용 :cpp:class:`GDALRasterBand` 인터페이스는 변경되지 않습니다. 밴드 수준이 아니라 데이터셋 수준에서만 비동기 I/O 요청이 발생하기 때문입니다.

C API
-----

C++ 클래스 및 메소드를 위한 다음 C API 래퍼(wrapper)를 추가할 것입니다. 이때 모든 :cpp:class:`GDALAsyncReader` 접근자에 대해 C 래퍼를 제공하려는 의도는 아니라는 사실을 기억하십시오. 응용 프로그램에서 이미 비동기 I/O를 구동시키는 호출로부터 제공 정보를 사용할 수 있기 때문입니다.

.. code-block:: c

   typedef void *GDALAsyncReaderH;

   GDALAsyncStatusType CPL_DLL CPL_STDCALL 
   GDALGetNextUpdatedRegion(GDALAsyncReaderH hARIO, double dfTimeout,
                            int* pnXBufOff, int* pnYBufOff, 
                            int* pnXBufSize, int* pnYBufSize );
   int CPL_DLL CPL_STDCALL GDALLockBuffer(GDALAsyncReaderH hARIO,double dfTimeout);
   void CPL_DLL CPL_STDCALL GDALUnlockBuffer(GDALAsyncReaderH hARIO); 

   GDALAsyncReaderH CPL_DLL CPL_STDCALL 
   GDALBeginAsyncReader(GDALDatasetH hDS, int nXOff, int nYOff,
                          int nXSize, int nYSize,
                          void *pBuf, int nBufXSize, int nBufYSize,
                          GDALDataType eBufType,
                          int nBandCount, int* panBandMap,
                          int nPixelSpace, int nLineSpace, int nBandSpace,
                          char **papszOptions);
   void  CPL_DLL CPL_STDCALL 
   GDALEndAsyncReader(GDALDatasetH hDS, GDALAsyncReaderH hAsynchRasterIOH);

SWIG
----

C API에서, 앞의 모든 함수들을 SWIG 용으로 래핑할 것입니다.

드라이버 구현
-------------

비동기 API를 JPIPKAK 드라이버로서 완전하게 구현할 것입니다. JPIPKAK 드라이버는 카카두 라이브러리를 이용해서 JPIP 프로토콜을 구현합니다.

현재로서는 다른 어떤 구현도 계획되어 있지 않습니다.

테스트
------

테스트 스위트에 비동기 및 일반적인 데이터 접근 모드의 JPIPKAK 드라이버 테스트는 물론 일반 드라이버를 대상으로 하는 비동기 API 테스트도 추가할 것입니다.

또한 새로운 명령줄 프로그램 gdalasyncread도 구현합니다. 이 gdalasyncread 유틸리티는 명령줄에서 비동기 API를 테스트할 수 있는 메커니즘을 제공합니다. 이 유틸리티는 gdal_translate 명령줄 옵션의 부분 집합을 입력받습니다.

::

   용례:  gdalasyncread [--help-general]
          [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
                CInt16/CInt32/CFloat32/CFloat64}]
          [-of format] [-b band]
          [-outsize xsize[%] ysize[%]]
          [-srcwin xoff yoff xsize ysize]
          [-co "NAME=VALUE"]* [-ao "NAME=VALUE"]
          src_dataset dst_dataset

