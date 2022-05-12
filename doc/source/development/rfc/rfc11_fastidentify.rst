.. _rfc-11:

================================================================================
RFC 11: 빠른 포맷 식별
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인 / 구현

요약
----

이 RFC의 목표는 응용 프로그램이 파일 시스템에 있는 파일들을 열어볼 필요없이 어떤 파일이 GDAL이 지원하는 파일 포맷인지 빠르게 식별할 수 있는 기능을 추가하는 것입니다. 주로 파일 유형 기반 GUI 파일 탐색기를 사용할 수 있게 하려는 목적입니다.

:cpp:class:`GDALOpenInfo` 클래스 구조를 더 많은 디렉터리 맥락을 담을 수 있도록 확장하고, :cpp:class:`GDALDriver` 클래스에 드라이버가 더 많은 리소스를 사용하는 :cpp:func:`Open` 작업을 하지 않고 어떤 파일이 지정한 포맷인지 빠르게 식별할 수 있도록 구현할 수 있는 :cpp:func:`Identify` 메소드를 추가해서 이를 달성합니다.

GDALOpenInfo
------------

많은 드라이버들의 :cpp:func:`Open` (또는 :cpp:func:`Identify`) 메소드는 어떤 파일을 특정 포맷으로 열거나 식별하려면 대상 파일 관련 파일들을 조사해야 합니다. 예를 들어, ESRI BIL 파일(EHdr 드라이버)을 열려면 드라이버가 대상 파일과 동일한 기본명을 가지지만 .hdr 확장자를 가진 파일을 조사해야 합니다. 현재 이 조사는 일반적으로 상당한 리소스를 사용할 수도 있는 :cpp:func:`VSIFStatL` 또는 이와 유사한 메소드를 호출해서 이루어집니다.

이렇게 운영 체제 파일 시스템 기작을 건드리는 검색을 해야 할 필요성을 줄이기 위해, 선택적인 파일 목록을 담을 수 있도록 :cpp:class:`GDALOpenInfo` 구조를 확장할 것입니다. 이 목록은 파일 시스템에서 대상 파일과 동일한 수준에 있는 모든 파일들의 목록으로, 대상 파일을 포함합니다. 어떤 경로 구성요소에도 파일명은 포함되지 '않을' 것이며, 파일명은 본질적으로 상위 디렉터리에 대한 :cpp:func:`CPLReadDir` 의 산출물일 뿐입니다. 대상 객체가 파일 시스템 의미(semantics)를 가지고 있지 않은 경우 파일 목록은 NULL이어야 합니다.

:cpp:class:`GDALOpenInfo` 에 다음을 추가합니다:

::

              GDALOpenInfo( const char * pszFile, GDALAccess eAccessIn, char **papszSiblings );
       char **papszSiblingFiles;

새 구성자가 파일 목록이 전송되어 'papszSiblingFiles' 멤버를 채우도록 해줍니다. (인자를 복사할 것입니다.) 기존 기본 구성자는 :cpp:func:`CPLGetDirname` 을 사용해서 전송된 'pszFile'의 디렉터리를 가져오고, :cpp:func:`CPLReadDir` 를 이용해서 대응하는 파일 목록을 읽어옵니다. 새 구성자는 각 파일을 테스트할 때마다 파일 목록을 다시 읽어오지 않아도 되는 최신 :cpp:func:`GDALIdentifyDriver` 함수의 효율적인 구현을 우선합니다.

Identify()
----------

:cpp:class:`GDALDriver` 를 다음 함수로 확장할 것입니다:

::

     int      (*pfnIdentify)( GDALOpenInfo * );

드라이버로 구현할 때, 이 함수의 목적은 드라이버가 :cpp:class:`GDALOpenInfo` 를 통해 전송된 파일이 해당 드라이버가 구현된 대상인 포맷으로 보인다고 판단하는 경우 TRUE(0이 아닌 값)를 반환하는 것입니다.
이 함수를 호출하려면 응용 프로그램이 새 함수를 호출해야 합니다:

::

     GDALDriverH *GDALIdentifyDriver( const char *pszDatasource, const char **papszDirFiles );

내부적으로 :cpp:func:`GDALIdentifyDriver` 함수는 다음을 수행할 것입니다:

1. :cpp:class:`GDALOpenInfo` 구조를 'pszDatasource' 및 'papszDirFiles'를 기반으로 초기화할 것입니다.
2. :cpp:func:`GDALOpen` 과 유사하게 모든 드라이버를 반복할 것입니다. 해당 드라이버가 해당 파일을 지원하는지 판단하기 위해, 사용할 수 있는 경우 각 드라이버에 :cpp:func:`pfnIdentify` 함수를 사용할 것이며 사용할 수 없다면 :cpp:func:`pfnOpen` 메소드를 사용할 것입니다.
3. 긍정적으로 응답하는 첫 번째 드라이버에 대해 드라이버 핸들을 반환할 것이고, 또는 해당 파일을 지원하는 드라이버가 없는 경우 NULL을 반환할 것입니다.

드라이버 변경
-------------

이론적으로는 어떤 드라이버도 수정할 필요가 없습니다. :cpp:func:`GDALIdentifyDriver` 가 다시 :cpp:func:`pfnOpen` 함수로 돌아가 테스트를 계속할 것이기 때문입니다. 그러나 실사용 시 최소한 몇몇 드라이버를 (바라건대 :cpp:func:`Open` 메소드가 아주 많은 리소스를 사용할 수도 있는 드라이버들을) 업데이트하지 않고서는 최적화를 달성할 수 없습니다. 이제 GDAL 드라이버에 식별 함수를 구현하는 노력을 계속해야 합니다.

일반적으로 :cpp:func:`Open` 함수에 있는 초기 테스트 로직으로부터 식별 함수를 구성하는 것은 쉬운 일입니다. 예를 들어 GeoTIFF 드라이버를 다음과 같이 변경할 수도 있습니다:

::

   int GTiffDataset::Identify( GDALOpenInfo * poOpenInfo )

   {
   /* -------------------------------------------------------------------- */
   /*      TIFF 파일의 특정 디렉터리 열기를 처리하기 위한                  */
   /*      특수 후크(hook)가 있습니다.                                     */
   /* -------------------------------------------------------------------- */
       if( EQUALN(poOpenInfo->pszFilename,"GTIFF_DIR:",10) )
           return TRUE;

   /* -------------------------------------------------------------------- */
   /*  먼저 이 파일이 예상 헤더 바이트를 가지는지 확인합니다               */
   /* -------------------------------------------------------------------- */
       if( poOpenInfo->nHeaderBytes < 2 )
           return FALSE;

       if( (poOpenInfo->pabyHeader[0] != 'I' || poOpenInfo->pabyHeader[1] != 'I')
           && (poOpenInfo->pabyHeader[0] != 'M' || poOpenInfo->pabyHeader[1] != 'M'))
           return FALSE;

       // 현재 BigTIFF 파일은 지원하지 못 합니다.
       if( poOpenInfo->pabyHeader[2] == 43 && poOpenInfo->pabyHeader[3] == 0 )
           return FALSE;
    

       if( (poOpenInfo->pabyHeader[2] != 0x2A || poOpenInfo->pabyHeader[3] != 0)
           && (poOpenInfo->pabyHeader[3] != 0x2A || poOpenInfo->pabyHeader[2] != 0) )
           return FALSE;

       return TRUE;
   }

그 다음 테스트 로직을 복제하는 일을 피하기 위해 :cpp:func:`Open` 함수가 식별 함수를 사용하도록 수정할 수도 있습니다:

::

   GDALDataset *GTiffDataset::Open( GDALOpenInfo * poOpenInfo )

   {
       TIFF    *hTIFF;

       if( !Identify( poOpenInfo ) )
           return NULL;

   /* -------------------------------------------------------------------- */
   /*      TIFF 파일의 특정 디렉터리 열기를 처리하기 위한                  */
   /*      특수 후크(hook)가 있습니다.                                     */
   /* -------------------------------------------------------------------- */
       if( EQUALN(poOpenInfo->pszFilename,"GTIFF_DIR:",10) )
           return OpenDir( poOpenInfo->pszFilename );

       GTiffOneTimeInit();
   ...

EHdr 드라이버처럼 헤더 파일을 요구하는 드라이버는 :cpp:func:`Identify` 함수를 다음과 같이 구현할 수도 있습니다:

::

   int EHdrDataset::Identify( GDALOpenInfo * poOpenInfo )

   {
       int     i, bSelectedHDR;
       const char  *pszHDRFilename;
       
   /* -------------------------------------------------------------------- */
   /*  사용자가 바이너리(예: .bil) 파일을 가리키고 있다고 가정합니다.      */
   /* -------------------------------------------------------------------- */
       if( poOpenInfo->nHeaderBytes < 2 )
           return FALSE;

   /* -------------------------------------------------------------------- */
   /*      이제 파일명을 분해해서 .HDR 파일명을 형성해야 합니다.           */
   /* -------------------------------------------------------------------- */
       CPLString osBasename = CPLGetBasename( poOpenInfo->pszFilename );
       pszHDRFilename = CPLFormCIFilename( "", osBasename, "hdr" );

       if( CSLFindString( poOpenInfo->papszSiblingFiles, pszHDRFilename) )
           return TRUE;
       else
           return FALSE;
   }

초기 구현을 하는 동안 다음 드라이버들을 포함, 다양한 드라이버를 업데이트할 것입니다. 뿐만 아니라 현재 리소스를 많이 사용하는 드라이버를 식별하기 위해 몇몇 성능 및 파일 시스템 활동 로그 작업도 업데이트할 것입니다.

-  HFA
-  GTiff
-  JPEG
-  PNG
-  GIF
-  HDF4
-  DTED
-  USGS DEM
-  MrSID
-  JP2KAK
-  ECW
-  EHdr
-  RST

CPLReadDir()
------------

현재 메모리에 있는 객체에 "파일 시스템과 비슷한" 접근을 제공하는 :file:`cpl_vsi_mem.cpp` 에 구현된 :cpp:class:`VSIMemFilesystemHandler` 클래스는 디렉터리 읽기 서비스를 구현하고 있지 않습니다. 디렉터리 목록을 제대로 채워넣으려면 디렉터리 읽기 서비스를 추가해야 할 것입니다.

이를 위해 :cpp:func:`CPLReadDir` 함수도 :file:`cpl_dir.cpp` 에 직접 구현된 디렉터리 읽기 서비스 대신 :cpp:func:`VSIFilesystemHandler::ReadDir` 메소드를 사용하도록 다시 구현해야 할 것입니다. 이미 Win32 및 유닉스/포직스(POSIX) 용으로 구현된 :cpp:func:`VSIFilesystemHandler::ReadDir` 함수가 존재합니다. 이 함수가 파일 시스템 접근 서비스 가상화를 실질적으로 완성할 것입니다.

:cpp:func:`CPLReadDir` 도 :cpp:func:`VSIReadDir` 로 재명명하지만, 하위 호환성을 위해 예전 이름 아래 스텁(stub)을 포함할 것입니다.

호환성
------

예상되는 하위 호환성 문제는 없습니다. 하지만 상위 호환성은 영향을 받을 것입니다. 트렁크에서 :cpp:func:`Identify` 함수를 가지도록 업데이트된 드라이버를 1.4버전 빌드로 포팅할 수 없으므로 1.4버전 :cpp:func:`Identify` 함수를 사용할 수 없을 것이기 때문입니다. 이 RFC 개발은 수정되지 않는 드라이버 및 외부에서 유지/관리되는 드라이버에 영향을 미치지 않을 것입니다.

SWIG 구현
---------

:cpp:func:`GDALIdentifyDriver` 및 :cpp:func:`VSIReadDir` 함수를 SWIG을 통해 노출시켜야 합니다.

회귀 테스트
-----------

:file:`autotest/gcore` 디렉터리에 :cpp:func:`Identify` 함수에 대한 테스트 스크립트를 추가할 것입니다. 이 스크립트는 :file:`/vsimem` 메모리 선택 집합에 있는 파일을 식별하는 테스트도 포함할 것입니다.

구현 계획
---------

프랑크 바르메르담이 GDAL/OGR 1.5.0 배포판을 위해 '트렁크'에 이 새 기능을 구현할 것입니다.

성능 테스트
-----------

실제로 파일을 열지 않는 :cpp:func:`Identify` 함수를 도입한 아주 간단한 테스트에서, (NFS 공유 상에서) TIFF 파일 70개를 가진 디렉터리에 있는 모든 파일을 식별하는 데 걸리는 시간이 2초에서 0.5초로 줄었습니다. 즉 GeoTIFF처럼 널리 사용되는 포맷을 포함하는 몇몇 포맷의 경우 실제로 파일을 여는 오버헤드를 상당히 절약할 수 있습니다.

