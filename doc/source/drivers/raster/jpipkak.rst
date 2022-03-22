.. _raster.jpipkak:

================================================================================
JPIPKAK - JPIP 스트리밍
================================================================================

.. shortname:: JPIPKAK

.. build_dependencies:: 카카두 라이브러리

JPEG2000 대화형 프로토콜(JPEG2000 Interactive Protocol; JPIP)은 네트워크 환경에서 임의 접근, 코드스트림 재배열 및 점증 디코딩에 대한 유연성이 뛰어나기 때문에 제한된 대역폭 연결 또는 고경합(high contention) 네트워크를 통해 원격 대용량 파일에 접근하는 데 유용합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

JPIPKAK - JPIP 오버뷰
-----------------------

이 단락에서는 JPIP 이벤트 시퀀스의 오버뷰를 간단히 소개합니다. 더 자세한 내용은 `JPEG2000 대화형 프로토콜 (Part 9 – JPIP) <http://www.jpeg.org/jpeg2000/j2kpart9.html>`_ 에 있고, `ISO <http://www.iso.org>`_ 에서 사양을 구매할 수 - 구매해야 합니다.

`여기 <http://www.jpeg.org/public/fcd15444-9v2.pdf>`_ 에서 JPEG2000 Part 9 초기 버전에 대한 설명을 볼 수 있습니다. ISO 저작권을 존중해서 이 문서에 도표를 복제하지는 않았습니다.

이 포맷 드라이버에 JPIP 프로토콜을 추상화했으며, 1:1 해상도 수준에서 요청을 생성합니다.

.. _initJPIP:

|JPIP Sequence Diagram|

#. 대상 이미지, 대상 ID, HTTP 상의 세션, JPP 스트림으로 반환할 데이터 그리고 응답이 사용할 수 있는 최대 길이에 대한 초기 JPIP 요청을 전송합니다. 이 경우 초기 윈도우를 요청하지 않았지만, 할 수도 있습니다. 서버는 서버 상에 있는 이미지를 식별하기 위해 사용할 수 있는 대상 식별자, 모든 향후 요청을 처리할 JPIP 서버를 가리키는 경로를 포함하는 JPIP-cnew 응답 헤더, 그리고 CID 세션 식별자를 응답합니다. 서버가 요청받은 데이터만 전송하기 위해 클라이언트 연결의 상태를 모델링할 수 있도록 요청하는 세션입니다.
#. 클라이언트가 최대 응답 길이를 가지고 있고 이전 통신에서 확정된 세션 식별자를 포함하는 대상 이미지에 대한 특정 뷰 윈도우를 요청합니다. 요청한 뷰 윈도우와 관련된 해상도를 식별하기 위해 'fsiz'를 사용합니다. 'fx'와 'fy'가 원하는 이미지 해상도의 차원을 지정합니다. 요청한 뷰 윈도우와 관련된 공간 영역이 좌상단 모서리로부터 얼마나 떨어져 있는지를 식별하기 위해 'roff'를 사용합니다. 요청한 뷰 윈도우와 관련된 공간 영역의 수평 및 수직 범위를 식별하기 위해 'rsiz'를 사용합니다.

JPIPKAK - 접근법
-----------------

JPIPKAK 드라이버는 `J2KViewer <http://www.drc-dev.ohiolink.edu/browser/J2KViewer>`_ 가 처음 보여준 접근법을 이용합니다. 이 뷰어는 후안 파블로 가르시아 오르티스(Juan Pablo Garcia Ortiz)가 카카두 kdu_cache 객체로부터 통신 레이어(소켓/HTTP)를 분리해서 개발한 것입니다. 데이터 객체로부터 통신 레이어를 분리하면 libcurl, 아파치 HttpClient (후안 파블로 오르티스가 평문 JAVA 소켓을 사용했다는 사실을 기억하십시오) 같은 최적화된 HTTP 클라이언트 라이브러리를 사용할 수 있고, 클라이언트와 서버 사이에 SSL 통신을 할 수 있기 때문입니다.

카카두는 소켓을 이용해서 JPIP 서버와 클라이언트의 통신을 구현했고, 이 소켓 연결이 이 클라이언트 세션의 상태를 가지고 있습니다. 클라이언트와 서버 사이의 JPIP 캐시 작업을 이용하면 카카두와의 클라이언트 세션을 재현할 수 있지만, JPIP은 전송 레이어에 중립적이기 때문에 전통적인 HTTP 쿠키 이용은 지원하지 않습니다.

JPIPKAK 드라이버는 카카두 캐시 객체를 가진 HTTP 클라이언트 라이브러리를 이용해서 작성되었고, (HTTP 세션을 지원할 수도 있고 지원하지 않을 수도 있는) JPIP 서버와의 최적화된 통신을 지원하며, 카카두 kdu_region_decompressor의 성능을 향상시킵니다.

|Component Diagram|

JPIPKAK - 구현
------------------------

JPIPKAK 드라이버는 GDAL C++ 및 C API를 지원하도록 구현되었으며, JAVA ImageIO 예시를 이용해서 이 드라이버를 위한 초기 SWIG 래퍼(wrapper)를 제공합니다. (**할 일** - QGIS 예시)

이 드라이버는 데이터 읽기 요청 및 원격 가져오기를 지원하기 위해 단순 스레딩 모델을 사용합니다.이 스레딩 모델은 서버와의 연결 하나만으로 개별 클라이언트 윈도우 2개를 지원합니다. 사용 가능한 대역폭을 효율적으로 활용하기 위해 서버로의 요청을 다중 송신합니다. 클라이언트는 "PRIORITY" 메타데이터 요청 옵션에 "0"(low) 또는 "1"(high) 값을 설정해서 클라이언트 윈도우를 식별합니다.

.. note:: SSL 지원
   
   클라이언트가 SSL을 지원하도록 빌드하는 경우, 요청이 jpips:// 프로토콜인지 아니면 jpip:// 프로토콜인지에 따라 드라이버가 SSL을 사용할지 여부를 결정합니다. 드라이버가 Curl 인증서를 사용해서 서버 인증서를 검증하지 않으며, 현재 모든 SSL 서버 인증서를 받아들이도록 설정되어 있다는 사실을 기억하십시오.

.. note:: libCurl
   
   JPIP은 HTTP 헤더를 이용해서 클라이언트/서버 값들을 설정합니다. 이를 지원하기 위해 GDAL HTTP 이식성(portability) 라이브러리를 수정했습니다.

|GDAL Sequence Diagram|

#. GDALGetDatasetDriver

   이 데이터셋과 관련된 드라이버를 가져옵니다.

#. Open

   ``GDALOpenInfo`` 객체에 담겨 있는 파일명이 JPIP 또는 JPIPS의 대소문자를 구분하는 URI 스키마인 경우 ``JPIPKAKDataset`` 을 생성한 다음 초기화하고, 그렇지 않다면 NULL을 반환합니다.

#. Initialize

   초기화는 세션을 확정하고 이미지에 관한 초기 메타데이터를 가져오기 위해 JPIP 서버로의 초기 연결을 생성하는 작업을 포함합니다. (`JPIP 시퀀스 다이어그램 <#initJPIP>`_ 참조)

   이 연결이 실패할 경우, 함수가 거짓을 반환하고 ``Open`` 함수는 NULL을 반환합니다. 이 드라이버로 데이터셋을 여는 데 실패했다는 뜻입니다.

   이 연결이 성공한 경우, 이미지에 관해 사용할 수 있는 모든 메타데이터를 가져오기 위한 JPIP 서버로의 그 다음 요청을 전송합니다. "JPIP" 메타데이터 도메인에 있는 ``GDALMajorObject->SetMetadataItem`` 을 이용해서 메타데이터 항목들을 설정합니다.

   서버로부터 반환된 메타데이터에 GeoJP2 UUID 경계 상자 또는 GMLJP2 XML 경계 상자가 포함되어 있는 경우, 해당 메타데이터를 파싱해서 이 데이터셋의 지리 메타데이터를 설정합니다.

#. GDALGetMetadata

   ``JPIPKAKDataset->GetMetadata`` 를 호출하는 C API입니다.

#. GetMetadata

   "JPIP" 메타데이터 도메인의 메타데이터를 반환합니다. 키는 "JPIP_NQUALITYLAYERS", "JPIP_NRESOLUTIONLEVELS", "JPIP_NCOMPS" 및 "JPIP_SPRECISION"입니다.

#. GDALEndAsyncRasterIO

   비동기(asynchronous) 래스터 I/O가 활성화된 상태인데 이를 요청하지 않은 경우, C API가 ``JPIPKAKDataset->EndAsyncRasterIO`` 를 호출합니다.

#. EndAsyncRasterIO

   JPIPKAKAsyncRasterIO 객체를 삭제합니다.

#. delete

#. GDALBeginAsyncRasterIO

   ``JPIPKAKDataset->BeginAsyncRasterIO`` 를 호출하는 C API입니다.

#. BeginAsyncRasterIO

   클라이언트가 1:1 해상도 수준에서 요청한 뷰 윈도우를 설정하고, 폐기 수준(discard level), 품질 레이어 및 스레드 우선순위 메타데이터 항목을 선택적으로 설정합니다.

#. Create

   JPIPKAKAsyncRasterIO 객체를 생성합니다.

#. Start

   카카두 메커니즘을 환경설정하고 서버와 현재 뷰 윈도우 요청을 통신하기 위한 배경 스레드를 (이미 실행 중이 아니라면) 시작합니다. 이 배경 스레드는 JPIP 서버가 현재 뷰 윈도우 요청에 대한 "EOR(End Of Response)" 메시지를 보낼 때까지 ``kdu_cache`` 객체를 계속 업데이트합니다.

#. GDALLockBuffer

   LockBuffer를 호출하는 C API입니다.

#. LockBuffer

   ``JPIPKAKAsyncRasterIO`` 에는 구현되지 않았습니다. ``JPIPKAKAsyncRasterIO->GetNextUpdatedRegion`` 에서 버퍼를 잠글 수 있습니다.

#. GDALGetNextUpdatedRegion

   GetNextUpdatedRegion을 호출하는 C API입니다.

#. GetNextUpdatedRegion

   이 함수는 사용할 수 있는 데이터를 압축 해제해서 (``JPIPKAKDataset->BeginAsyncRasterIO`` 에 설정된 데이터셋 버퍼 유형에 따라) 이미지를 생성하고, 영역 포인터에 (요청한 폐기 수준에서) 압축 해제된 윈도우 너비 및 높이를 반환합니다. 클라이언트는 이를 이용해서 윈도우를 렌더링할 수 있습니다. 렌더링 작업의 상태는 ``GDALAsyncStatusType`` 의 ``GARIO_PENDING, GARIO_UPDATE, GARIO_ERROR, GARIO_COMPLETE`` 가운데 하나입니다. ``GARIO_UPDATE, GARIO_PENDING`` 은 전체 이미지 데이터를 얻기 위해 GetNextUpdatedRegion을 더 읽어와야 하는데, 이것이 JPIP의 진행형 렌더링입니다. ``GARIO_COMPLETE`` 은 윈도우가 완성되었다는 뜻입니다.

   ``GDALAsyncStatusType`` 이란 카카두가 자체 캐시에 압축 해제할 데이터를 더 가지고 있지 않거나 또는 서버가 요청 윈도우가 완료되었다는 의미의 EOR 메시지를 보내지 않는다는 사실을 나타내기 위해 ``GetNextUpdatedRegion`` 이 사용하는 구조입니다.

   이 함수로 전송되는 영역은 참조로 전송되고, 압축 해제된 영역을 찾았다는 결과가 반환되는 경우 호출자가 이 영역을 읽을 수 있습니다. 이미지 데이터는 - 예를 들어 요청한 영역이 구성요소 3개를 가지고 있는 경우의 RGB처럼 - 버퍼 안에 빽빽히 채워져 있습니다.

#. GDALUnlockBuffer

   UnlockBuffer를 호출하는 C API입니다.

#. UnlockBuffer

   ``JPIPKAKAsyncRasterIO`` 에는 구현되지 않았습니다. ``JPIPKAKAsyncRasterIO->GetNextUpdatedRegion`` 에서 버퍼 잠금을 해제할 수 있습니다.

#. Draw

   클라이언트가 이미지 데이터를 렌더링합니다.

#. `GDALLockBuffer <#GDALLockBuffer>`_

#. `LockBuffer <#LockBuffer>`_

#. `GDALGetNextUpdatedRegion <#GDALGetNextUpdatedRegion>`_

#. `GetNextUpdatedRegion <#GetNextUpdatedRegion>`_

#. `GDALUnlockBuffer <#GDALUnlockBuffer>`_

#. `UnlockBuffer <#UnlockBuffer>`_

#. `Draw <#Draw>`_

JPIPKAK - 설치 요구사항
-----------------------------------

-  `Libcurl 7.9.4 <http://curl.haxx.se/>`_
-  `OpenSSL 0.9.8K <http://www.openssl.org/>`_ (SSL이 필수인 경우, JPIPS 연결)
-  `카카두 <http://www.kakadusoftware.com>`_ (v5.2.6 및 v6과 테스트)

현재 윈도우 용 makefile만 제공하지만, 윈도우 의존성이 없기 때문에 리눅스 상에서도 컴파일될 것입니다.

참고
--------

-  `JPEG2000 대화형 프로토콜 (Part 9 – JPIP) <http://www.jpeg.org/jpeg2000/j2kpart9.html>`_
-  http://www.opengeospatial.org/standards/gmljp2
-  `카카두 소프트웨어 <http://www.kakadusoftware.com>`_
-  `IAS 데모 (예시 JPIP(S) 스트림) <http://iasdemo.ittvis.com/>`_

메모
-----

원래 `ITT VIS <http://www.ittvis.com>`_ 사가 이 드라이버를 개발했으며, SSL이 원격 JPEG2000 데이터셋의 JPIP 클라이언트 스트리밍을 할 수 있도록 하기 위해 GDAL에 기부했습니다.

.. |JPIP Sequence Diagram| image:: ../../../images/jpipsequence.PNG
.. |Component Diagram| image:: ../../../images/components.PNG
.. |GDAL Sequence Diagram| image:: ../../../images/gdalsequence.PNG

