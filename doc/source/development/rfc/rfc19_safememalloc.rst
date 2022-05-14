.. _rfc-19:

================================================================================
RFC 19: GDAL에서 더 안전한 메모리 할당
================================================================================

저자: 이벤 루올(Even Rouault)

연락처: even.rouault@spatialys.com

상태: 승인, 구현

요약
----

이 문서는 메모리 할당 시 GDAL을 더 안전하게 (크래시를 방지하게) 만드는 방법을 제안합니다. 이 논의의 시발점은 #2075 티켓입니다.

상세 사항
---------

GDAL 소스 코드의 많은 곳에서 래스터 블록, 스캔라인, 전체 이미지 버퍼 등등을 할당하기 위한 메모리 버퍼 크기를 계산하는 곱셈을 수행합니다. 현재 어떤 오버플로 검사도 하지 않기 때문에 버퍼가 충분히 크게 할당되지 않을 가능성이 있습니다. 래스터 크기가 매우 큰 경우 (예를 들어 WMS 래스터 소스가 그 사례가 될 수 있습니다) 또는 데이터소스에 의도적이든 의도적이지 않든 오류가 발생하는 경우 오버플로가 발생할 수 있습니다. 이렇게 되면 크래시로 이어질 수 있습니다.

이 RFC는 할당할 메모리 버퍼 크기 계산이 곱셈을 기반으로 하는 경우 메모리를 할당하기 위한 새 API를 도입합니다. 이 새 API는 오버플로 발생 시 이를 리포트합니다. ``((a*b)/b) == a`` 를 확인해서 오버플로를 탐지합니다. 이때 변수 유형의 크기, 변수의 부호 등을 가정할 필요가 없습니다.

.. code-block:: cpp

   /*
    VSIMalloc2가 (nSize1 * nSize2) 바이트를 할당합니다.
    곱셈의 오버플로가 발생하는 경우, 또는 메모리 할당이 실패하는 경우
    NULL 포인터를 반환하고 CPLError()로 CE_Failure 오류를 발생시킵니다.
    'nSize1 == 0 || nSize2 == 0'인 경우에도 NULL 포인터를 반환할 것입니다.
    CPLFree() 또는 VSIFree()를 사용해서 이 함수가 할당한 메모리를 해제할 수 있습니다.
   */
   void CPL_DLL *VSIMalloc2( size_t nSize1, size_t nSize2 );

   /*
    VSIMalloc3이 (nSize1 * nSize2 * nSize3) 바이트를 할당합니다.
    곱셈의 오버플로가 발생하는 경우, 또는 메모리 할당이 실패하는 경우
    NULL 포인터를 반환하고 CPLError()로 CE_Failure 오류를 발생시킵니다.
    'nSize1 == 0 || nSize2 == 0 || nSize3 == 0'인 경우에도 NULL 포인터를 반환할 것입니다.
    CPLFree() 또는 VSIFree()를 사용해서 이 함수가 할당한 메모리를 해제할 수 있습니다.
   */
   void CPL_DLL *VSIMalloc3( size_t nSize1, size_t nSize2, size_t nSize3 );

:cpp:func:`VSIMalloc2` 및 :cpp:func:`VSIMalloc3` 의 습성은 :cpp:func:`VSIMalloc` 의 습성과 일치합니다. 기존 메모리 할당 API(:cpp:func:`CPLMalloc`, :cpp:func:`CPLCalloc`, :cpp:func:`CPLRealloc`, :cpp:func:`VSIMalloc`, :cpp:func:`VSICalloc`, :cpp:func:`VSIRealloc`)의 구현은 변경되지 않을 것입니다.

더 안전한 메모리 할당을 위한 새 API를 촉진하도록 :ref:`rfc-8` 을 업데이트할 것입니다. 예를 들면 ``CPLMalloc(x * y)`` 또는 ``VSIMalloc(x * y)`` 대신 ``VSIMalloc2(x, y)`` 를 사용하도록 업데이트할 것입니다.

구현 단계
---------

1. :file:`gdal/port` 에 새 API를 도입합니다.

2. GDAL 코어에서 관련이 있는 곳에 새 API를 사용합니다. 다음 파일들이 후보로 식별되었습니다:

   * :file:`gcore/gdalnodatamaskband.cpp`
   * :file:`gcore/overview.cpp`
   * :file:`gcore/gdaldriver.cpp`
   * :file:`gcore/gdalrasterblock.cpp`

3. GDAL 드라이버에 새 API를 사용합니다. 이 단계는 점진적으로 수행할 수 있습니다. 몇몇 드라이버의 경우 CPL 할당으로부터 VSI 할당으로 전이해야 할 수도 있습니다. 다음은 후보 드라이버 목록입니다:

   * Idrisi
   * PNG
   * GXF
   * BSB
   * VRT
   * MEM
   * JP2KAK
   * RPFTOC
   * AIRSAIR
   * AIGRIB
   * XPM
   * USGDEM
   * BMP
   * GSG
   * HFA
   * AAIGRID
   
   (#2075 티켓에 있는 :file:`gdal_svn_trunk_use_vsi_safe_mul_in_frmts.patch` 를 참조하십시오.)

이벤 루올이 GDAL/OGR 1.6.0버전 배포판을 위해 이 RFC에서 설명하는 변경 사항들을 구현할 것입니다.

투표 이력
---------

프로젝트 운영 위원회의 모든 멤버가 +1 투표

-  프랑크 바르메르담
-  대니얼 모리셋
-  하워드 버틀러
-  세케레시 터마시
-  안드레이 키셀레프

