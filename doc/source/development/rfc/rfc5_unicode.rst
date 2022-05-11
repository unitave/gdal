.. _rfc-5:

=======================================================================================
RFC 5: GDAL에서의 유니코드 지원
=======================================================================================

저자: 안드레이 키셀레프(Andrey Kiselev)

연락처: dron@ak4719.spb.edu

상태: 개발 중

요약
----

이 문서는 GDAL 코어 로케일을 네이티브 문자 집합에 대한 독립형 보전 지원(independent preserving support)으로 만드는 방법에 대한 제안을 담고 있습니다.

주요 개념
---------

GDAL을 다음 3개의 주요 아이디어를 지원할 수 있는 방식으로 수정해야 합니다:

1. 사용자는 사용자의 모어를 사용하는 현지화된 환경에서 작업합니다. 다시 말해 GDAL에 전송된 문자열 데이터로 작업할 때 아스키 문자 집합을 확정할 수 없습니다.
2. GDAL은 문자열 작업 시 내부적으로 UTF-8 인코딩을 사용합니다.
3. GDAL은 가능한 경우 제3자 API의 유니코드 버전을 사용합니다.

따라서 GDAL에서 사용되는 모든 문자열은 평문 아스키가 아니라 UTF-8 인코딩으로 되어 있습니다. 즉 대화형 작업 세션 도중 사용자의 입력을 로컬 인코딩으로부터 UTF-8 인코딩으로 변환해야 한다는 의미입니다. GDAL 산출물에 대해서는 그 역을 수행해야 합니다. 예를 들면 사용자가 GDAL 유틸리티에 파일명을 명령줄 파라미터로 전송하는 경우 해당 파일명을 즉시 UTF-8 인코딩으로 변환한 다음에야 GDALOpen() 또는 OGROpen() 같은 함수에 전송해야 합니다. 문자열을 파라미터로 입력받는 모든 함수는 입력 문자열을 UTF-8 인코딩으로 가정합니다. (서로 다른 인코딩들 사이에 변환을 수행하는 몇몇 예외적인 함수도 있습니다. 구현 단락을 참조하십시오.) 산출 함수도 마찬가지입니다. GDAL에 내장된 산출 함수(CPLError/CPLDebug)는 출력 직전에 모든 문자열을 UTF-8 인코딩으로부터 로컬 인코딩으로 변환해야 합니다. 사용자 지정 오류 처리자(error handler)는 UTF-8 문제점을 인식하고 자신에게 전송되는 문자열을 적절하게 변환해야 합니다.

GDAL이 제3자 API를 호출해야 하는 경우 문자열 인코딩 문제가 다시 나타납니다. UTF-8 인코딩을 해당 API에 적합한 인코딩으로 변환해야 합니다. 특히, VSIFOpenL() 함수의 윈도우 구현에서 CreateFile() 함수를 호출하기 전에 UTF-8 을 UTF-16으로 변환해야 한다는 뜻입니다. 또다른 예를 들자면 PostgreSQL API가 있습니다. PostgreSQL은 내부적으로 문자열을 UTF-8 인코딩으로 저장하기 때문에, 서버에 전송 문자열이 이미 UTF-8 인코딩이므로 어떤 변환 및 손실도 없이 그대로 저장될 것이라는 사실을 알려야 합니다.

파일 포맷 드라이버의 경우 문자열 표현은 드라이버별로 작업해야 할 것입니다. 모든 파일 포맷이 비(非) 아스키 문자를 지원하지는 않습니다. 예를 들면, .HDR 명찰(labelled) 래스터는 평문 7비트 아스키 텍스트 파일로 이런 파일에 8비트 문자 문자열을 작성하는 것은 좋은 생각이 아닙니다. 문자열을 전송해야 하는 경우, 드라이버 외부에서 (예를 들어 SetMetadata() 호출로) 파일로부터 문자열을 추출한 다음 UTF-8 인코딩으로 변환해야 합니다. 추출한 문자열을 드라이버 내부적으로 사용하고자 한다면, 변환할 필요는 없습니다.

파일 인코딩이 로컬 시스템 인코딩과 다른 경우도 있는데, 이런 경우 사용자에게 물어보는 것 외에는 파일 인코딩을 알 수 있는 방법이 없습니다. (예를 들면 누군가가 앞에서 말한 평문 텍스트 .HDR 파일에 8비트 비(非) 아스키 문자열 필드를 추가한 경우를 상상해보십시오.) 다시 말해 파일 인코딩을 UTF-8 인코딩으로 변환할 수 없지만 로컬 인코딩을 UTF-8 인코딩으로 변환할 수는 있다는 뜻입니다. 따라서 데이터소스별로 어떤 방식으로든 파일 인코딩을 알아낼 수 있는 방법이 필요합니다. 이 문제의 자연스러운 해결 방법은 GDALOpen/OGROpen 함수에 선택적인 "ENCODING" 열기 옵션을 도입하는 것이지만, 안타깝게도 이 함수들은 파라미터를 입력받지 않습니다. 이 함수들에 열기 옵션을 도입하려면 또다른 RFC로 제안해야 합니다.

다행스러운 것은 당장 인코딩 파라미터를 추가해야 할 필요는 없다는 사실입니다. 일반 i18n 프로세스로부터 독립적이기 때문입니다. 이 RFC에 정의된 대로 UTF-8 인코딩 지원을 추가하고, 나중에 열기 옵션이 도입될 때 데이터소스별 인코딩을 강제하는 지원을 추가하면 됩니다.

구현
----

-  CPLString 클래스에 새로운 문자 변환 함수를 도입할 것입니다. 이 클래스는 UTF-8 문자열을 항상 내부적으로 담고 있는 것이 목적입니다.

::


   // 내부 UTF-8 인코딩 문자열로부터 로컬 인코딩으로 된 문자열을 가져옵니다.
   // 범위를 넘어서는 문자는 산출 문자열에 '?'로 대체합니다.
   // nEncoding은 인코딩의 코드명입니다.
   // 0인 경우 로컬 시스템 인코딩을 사용할 것입니다.
   char* CPLString::recode( int nEncoding = 0 );

   // 다른 인코딩으로 된 문자열로부터 UTF-8 문자열 객체를 구성합니다.
   // nEncoding은 인코딩의 코드명입니다.
   // 0인 경우 로컬 시스템 인코딩을 사용할 것입니다.
   CPLString::CPLString( const char*, int nEncoding );

   // wchar_t 요소들의 배열로부터 UTF-8 문자열 객체를 구성합니다.
   // 소스 인코딩은 시스템별로 다릅니다.
   CPLString::CPLString( wchar_t* );

   // UTF-8 인코딩으로부터 wchar_t 요소들의 배열로 문자열을 가져옵니다.
   // 대상 인코딩은 시스템별로 다릅니다.
   operator wchar_t* (void) const;

-  사용자 입력에 비(非) 아스키 문자를 사용하려면, 모든 응용 프로그램이 입구점(entry point) 직후 setlocale(LC_ALL, "") 함수를 호출해야 합니다.

-  다음은 코드 예시입니다. 유니코드 측면에서 GDAL 유틸리티 및 핵심 코드를 어떻게 변경해야 하는지 살펴봅시다.

입력물의 경우 다음 코드 대신

::

   pszFilename = argv[i];
   if( pszFilename )
       hDataset = GDALOpen( pszFilename, GA_ReadOnly );

다음 코드를 사용해야 합니다:

::

   CPLString oFilename(argv[i], 0); // <-- 로컬 인코딩을 UTF-8로 변환
   hDataset = GDALOpen( oFilename.c_str(), GA_ReadOnly );

출력물의 경우 다음 코드 대신

::

   printf( "Description = %s\n", GDALGetDescription(hBand) );

다음 코드를 사용해야 합니다:

::


   CPLString oDescription( GDALGetDescription(hBand) );
   printf( "Description = %s\n", oDescription.recode( 0 ) ); // <-- UTF-8을 로컬 인코딩으로 변환

앞의 코드 조각에서 GDALOpen() 함수에 UTF-8 인코딩으로 전송된 파일명은 GDAL 코어에서 추가 처리될 것입니다. 윈도우 상에서는 다음 코드 대신

::

   hFile = CreateFile( pszFilename, dwDesiredAccess,
       FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, dwCreationDisposition,
       dwFlagsAndAttributes, NULL );

다음 코드를 사용합니다:

::

   CPLString oFilename( pszFilename );
   // _UNICODE 스위치를 지정하기보다 확장 문자(wide character) 버전을
   // 명확하게 호출하는 것을 선호합니다.
   hFile = CreateFileW( (wchar_t *)oFilename, dwDesiredAccess,
           FILE_SHARE_READ | FILE_SHARE_WRITE, NULL,
           dwCreationDisposition,  dwFlagsAndAttributes, NULL );

-  이 문서에서는 아직 문자 변환 함수의 실제 구현을 명시하고 있지 않습니다. 추가적인 논의가 필요합니다.
   제일 큰 문제는 '로컬 인코딩 <-> UTF-8 인코딩' 변환뿐만이 아니라 '*임의의 인코딩* <-> UTF-8 인코딩' 변환이 필요하다는 것입니다. 이를 구현하려면 소프트웨어 부분에서 상당한 지원을 해줘야 합니다.

하위 호환성
-----------

이 새 기능은 8비트 문자 처리 방법이라는 면에서 GDAL/OGR 하위 호환성을 무너뜨릴 것입니다. 지금까지는 사용자가 모든 8비트 문자 문자열이 아무 변경 없이 GDAL/OGR를 통해 전송되고 끝까지 정확히 동일한 데이터를 담고 있을 것이라는 사실에 의존할 수도 있습니다. 이 새 기능이 도입되면 7비트 아스키 및 8비트 UTF-8 인코딩 문자열만 아무 변경 없이 GDAL/OGR를 통해 전송될 것입니다. GDAL 작업 시 아스키 부분 집합만 사용하는 경우 이 새 기능의 영향을 받지 않는다는 사실을 기억하십시오.

유니코드 표준의 제 5장에서 발췌:

"'wchar_t'의 길이는 컴파일러에 따라 다르며 8비트까지 짧아질 수 있습니다. 결과적으로 모든 C 또는 C++ 컴파일러에 걸쳐 이식성을 가져야 하는 프로그램은 'wchar_t'에 유니코드 텍스트를 저장해서는 안 됩니다."

참조
----

-  `유니코드 표준 4.0버전 - 구현 지침 <http://unicode.org/versions/Unicode4.0.0/ch05.pdf>`_ - 제 5장 (PDF)
-  소프트웨어에서 유니코드 사용법에 대한 FAQ:
   `http://www.cl.cam.ac.uk/~mgk25/unicode.html <http://www.cl.cam.ac.uk/~mgk25/unicode.html>`_
-  문자열 변환 함수의 FLTK 구현:
   `http://svn.easysw.com/public/fltk/fltk/trunk/src/utf.c <http://svn.easysw.com/public/fltk/fltk/trunk/src/utf.c>`_
-  `http://www.easysw.com/~mike/fltk/doc-2.0/html/utf_8h.html <http://www.easysw.com/~mike/fltk/doc-2.0/html/utf_8h.html>`_
-  #1494 티켓: GML 산출물 용 UTF-8 인코딩
-  :ref:`rfc30_utf8_filenames` 에서도 파일명에 대해 논의합니다.

