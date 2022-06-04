.. _rfc-57:

=======================================================================================
RFC 57: 히스토그램 용 64비트 버킷 개수
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 GDALRasterBand GetHistogram(), GetDefaultHistogram() 및 SetDefaultHistogram() 메소드가 `버킷(bucket) <https://datamod.tistory.com/129>`_ 개수에 대해 현재의 32비트 정수형 배열 대신 64비트 정수형 배열을 받아들이도록 수정할 것을 제안합니다. 이렇게 변경하면 픽셀 20억 개를 초과하는 대용량 래스터에 대해 작업하는 경우 발생하는 문제점을 해결할 것입니다.

핵심 변경 사항
--------------

:cpp:class:`GDALRasterBand` 클래스의 다음 메소드들을 수정해서 GetHistogram() 및 SetDefaultHistograph()의 경우 ``GUIntBig*`` 인자를, GetDefaultHistogram()의 경우 ``GUIntBig**`` 인자를, 그리고 GetRasterSampleOverview()의 경우 ``GUIntBig`` 인자를 입력받을 수 있게 합니다:

::

       virtual CPLErr  GetHistogram( double dfMin, double dfMax,
                             int nBuckets, GUIntBig * panHistogram,
                             int bIncludeOutOfRange, int bApproxOK,
                             GDALProgressFunc, void *pProgressData );

       virtual CPLErr GetDefaultHistogram( double *pdfMin, double *pdfMax,
                                           int *pnBuckets, GUIntBig ** ppanHistogram,
                                           int bForce,
                                           GDALProgressFunc, void *pProgressData);

       virtual CPLErr SetDefaultHistogram( double dfMin, double dfMax,
                                           int nBuckets, GUIntBig *panHistogram );

       virtual GDALRasterBand *GetRasterSampleOverview( GUIntBig );

PAM(Pluggable Authentication Module) 직렬화(serialization)/역직렬화(deserialization)도 업데이트합니다.

C API 변경 사항
~~~~~~~~~~~~~~~

다음 함수들만 추가합니다:

::

   CPLErr CPL_DLL CPL_STDCALL GDALGetRasterHistogramEx( GDALRasterBandH hBand,
                                          double dfMin, double dfMax,
                                          int nBuckets, GUIntBig *panHistogram,
                                          int bIncludeOutOfRange, int bApproxOK,
                                          GDALProgressFunc pfnProgress,
                                          void * pProgressData );

   CPLErr CPL_DLL CPL_STDCALL GDALGetDefaultHistogramEx( GDALRasterBandH hBand,
                                          double *pdfMin, double *pdfMax,
                                          int *pnBuckets, GUIntBig **ppanHistogram,
                                          int bForce,
                                          GDALProgressFunc pfnProgress,
                                          void * pProgressData );

   CPLErr CPL_DLL CPL_STDCALL GDALSetDefaultHistogramEx( GDALRasterBandH hBand,
                                          double dfMin, double dfMax,
                                          int nBuckets, GUIntBig *panHistogram );

   GDALRasterBandH CPL_DLL CPL_STDCALL
                              GDALGetRasterSampleOverviewEx( GDALRasterBandH, GUIntBig );

기존 GDALGetRasterHistogram(), GDALGetDefaultHistogram() 및 GDALSetDefaultHistogram() 메소드들을 퇴출되었다고 표시합니다.
이 함수들은 내부적으로 64비트 메소드를 호출하고, GDALGetRasterHistogram() 및 GDALGetDefaultHistogram()의 경우 32비트 오버플로(overflow)가 발생하면 경고를 발합니다. 이 경우 버킷 개수가 INT_MAX로 설정됩니다.

드라이버 변경 사항
------------------

C++ 히스토그램 메소드를 사용하거나 구현한 모든 인트리 드라이버를 수정합니다:

   -  ECW
   -  VRT
   -  MEM
   -  HFA

유틸리티 변경 사항
------------------

gdalinfo 및 gdalenhance가 수정된 메소드들을 사용하도록 수정합니다.

SWIG 바인딩 변경 사항
---------------------

파이썬 바인딩의 경우에만 RasterBand.GetHistogram(), GetDefaultHistogram() 및 SetDefaultHistogram()이 새 64비트 C 함수들을 사용합니다.

다른 바인딩들도 업데이트할 수 있지만, (int, GUIntBig*)에 대한 새로운 유형 매핑이 필요할 것입니다. 그 동안에는 32비트 C 함수들을 계속 사용합니다.

호환성
------

이 RFC는 C++ API 및 ABI를 수정합니다.

트리 외부에 있는 드라이버는 수정된 가상 메소드 4개 가운데 일부를 구현하는 경우 업데이트된 C++ API를 반드시 연산에 넣어야 합니다.

관련 티켓
---------

`#5159 티켓 <https://trac.osgeo.org/gdal/ticket/5159>`_

문서화
------

새로운/수정된 메소드/함수를 모두 문서화합니다.
:file:`MIGRATION_GUIDE.TXT` 에 이 RFC에 대한 단락을 새로 추가합니다.

테스트
------

:file:`gcore/pam.y` 및 :file:`gdrivers/mem.py` 에서 64비트 값 설정하기/가져오기를 테스트했습니다.

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 이 RFC를 구현할 것입니다.

제안한 구현은 `"histogram_64bit_count" 브랜치 <https://github.com/rouault/gdal2/tree/histogram_64bit_count>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/histogram_64bit_count>`_

투표 이력
---------

-  대니얼 모리셋 +1
-  유카 라흐코넨 +1
-  이벤 루올 +1

