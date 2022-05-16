.. _rfc-23:

================================================================================
RFC 23.1: OGR에서의 유니코드 지원
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인, 구현

요약
----

이 RFC는 GDAL/OGR가 문자열을 내부적으로 UTF-8 인코딩으로 처리하고 서로 다른 인코딩들 사이의 변환을 지원하도록 하기 위한 예비 단계를 제안합니다.

주요 개념
---------

다음 세 가지 주요 아이디어를 지원하는 방향으로 GDAL을 수정해야 합니다:

1. 표현들 사이의 (예를 들면 UTF-8을 UCS-16/wchar_t로) 변환을 포함, 다양한 인코딩 변환을 지원하는 C 함수들을 제공할 것입니다.
2. iconv() 스타일 문자열이 문자 인코딩을 식별할 것입니다.
3. OGR의 OFTString/OFTStringList 피처 속성을 UTF-8 인코딩으로 취급할 것입니다.

이 RFC는 아스키가 아닌 파일명을 사용하는 문제점을 지적하려 시도하지 않습니다. GDAL/OGR에서 사용되는 (필드 이름, 메타데이터 등등 같은) 기타 문자열의 인코딩에 관해 정의하려 시도하지도 않습니다. 이런 문제점들은 아마 향후 이에 대한 RFC 작성 시 다루어질 것입니다.

CPLRecode API
-------------

문자열 재(再)코딩 및 wchar_t(확장 문자) 및 char(멀티바이트) 포맷들 간의 변환을 위한 다음 C 호출 가능 함수 3개를 도입할 것입니다:

::

   char *CPLRecode( const char *pszSource, 
                    const char *pszSrcEncoding, const char *pszDstEncoding );

   char *CPLRecodeFromWChar( const wchar_t *pwszSource, 
                             const char *pszSrcEncoding, 
                             const char *pszDstEncoding );
   wchar_t *CPLRecodeToWChar( const char *pszSource,
                              const char *pszSrcEncoding, 
                              const char *pszDstEncoding );

각 함수는 입력 문자열과 마찬가지로 0으로 종료되는 문자열을 반환하며 반환 문자열은 CPLFree() 함수로 할당 해제되어야 합니다. 오류가 발생하는 경우 반환 문자열은 NULL일 것이고, 해당 함수는 CPLError()를 발행할 것입니다. 이 함수들은 CPL_DLL로 표시되며, 내부 사용은 물론 응용 프로그램 사용에 대해서도 공개 GDAL/OGR API의 일부분으로 간주될 것입니다.

인코딩 이름
-----------

iconv() 함수가 사용하는 인코딩 이름과 동일한 종류의 인코딩 이름을 사용할 것을 제안합니다. 즉 "UTF-8", "LATIN5", "CP850" 및 "ISO_8859-1" 같은 이름들을 사용합니다. 이런 인코딩 이름들이 (예를 들면 "en_CA.utf8" 같은) C 라이브러리 로케일 이름과 1:1로 일치하지 않는 것으로 보이기 때문에 어떤 문제를 일으킬 수도 있습니다.

다음은 흥미있는 몇몇 특정 이름들입니다:

-  "":
   현재 로케일입니다. 사용자 로케일 간의 변환 시 이 비어 있는 문자열을 사용하십시오.
-  "UTF-8":
   멀티바이트 인코딩으로 된 유니코드입니다. 대부분의 경우 UTF-8이 내부 `링구아 프랑카 <https://ko.wikipedia.org/wiki/%EB%A7%81%EA%B5%AC%EC%95%84_%ED%94%84%EB%9E%91%EC%B9%B4>`_ 가 될 것입니다.
-  "POSIX":
   대략 (아마도 몇몇 확장 문자를 가진?) 아스키로 간주됩니다.
-  "UCS-2":
   2바이트 유니코드입니다. 확장 문자(wide character) 포맷으로 wchar_t 메소드를 사용하는 경우에만 적합합니다.

몇몇 시스템 상에서 ``iconv --list`` 명령을 사용하면 지원 인코딩 목록을 볼 수 있습니다.

iconv()
-------

사용할 수 있는 경우 iconv() 및 관련 함수들을 사용하는 CPLRecode() 메소드를 구현할 것을 제안합니다.

이 API는 리눅스 상에서 C 라이브러리가 사용하는 GNU libiconv()로 멋지게 구현되어 있습니다. 또한 몇몇 운영 체제는 (모두 유닉스 계열?) iconv() API를 C 라이브러리의 일부분으로 제공합니다. 하지만 시스템 iconv()는 지원하는 변환 종류가 제한되어 있기 때문에, 사용할 수 있는 경우 시스템 iconv()보다 libiconv()를 사용하는 편이 더 좋습니다.

iconv()를 사용할 수 없는 경우, 재(再)코딩 토막(stub) 구현을 제공할 것인데 이는:

-  mbtowc/wctomb, 또는 `유닉스/리눅스의 UTF-8 및 유니코드 FAQ <https://www.cl.cam.ac.uk/~mgk25/unicode.html>`_ 로부터 파생된 구현을 사용하는 UCS-2/UTF-8 상호 변환을 구현합니다.
-  아무것도 하지 않고 "" 와 "UTF-8" 간에 재(再)코딩을 하지만 현재 로케일이 "C" 로케일로 보이지 않는 경우 첫 번째 사용 시 경고를 발하도록 구현합니다.
-  "ASCII"로부터 "UTF-8"로의 재(再)코딩을 NULL 작업으로 구현합니다.
-  "UTF-8"로부터 "ASCII"로의 재(再)코딩을 아스키가 아닌 모든 멀티바이트 문자를 '?'로 바꿔서 구현합니다.

이렇게 구현하면 iconv() 없이 빌드하는 경우 불충분한 작업 상태를 가지게 되지만, iconv()를 사용할 수 있는 경우 완전한 작업을 할 수 있을 것입니다.

환경설정에 ``--with-iconv=`` 옵션을 추가할 것입니다. 이 옵션의 인자는 libiconv 설치본을 가리키는 경로 또는 시스템 라이브러리를 사용해야 한다는 사실을 나타내는 특수값 'system' 가운데 하나일 수 있습니다. 아니면 ``--without-iconv`` 를 이용해서 iconv()를 사용하지 않을 수도 있습니다.

OFTString/OFTStringList 필드
----------------------------

OGR 문자열 속성값은 UTF-8 인코딩일 것이라고 선언되었습니다. 즉 OGR 드라이버가 읽기 작업 시 포맷 특화 표현을 UTF-8로 변환하고 쓰기 작업 시 다시 포맷 특화 표현으로 변환해야 한다는 뜻입니다. 대부분의 경우 이 (대부분의 경우 단순 아스키 텍스트의) 작업에는 변환이 필요하지 않습니다.

다시 말해 ``OGRFeature::SetField(int i, const char \*)`` 같은 메소드의 인자들이 UTF-8이어야 하고, :cpp:func:`GetFieldAsString` 이 UTF-8 인코딩 문자열을 반환할 것이라는 의미입니다.

OFTStringList 문자열 목록도 동일한 문제점을 가지고 있습니다. 각 문자열을 UTF-8 인코딩으로 가정할 것입니다.

OLCStringsAsUTF8 케이퍼빌리티 플래그
------------------------------------

(CSV 드라이버 같은) 일부 드라이버는 입력물의 인코딩을 사실상 모를 수 있습니다. 따라서 보장된 방법으로 문자열을 UTF-8 인코딩으로 변환하는 것이 항상 실용적이지는 않습니다. 즉 "OLCStringsAsUTF8" 매크로를 가진 "StringsAsUTF8"이라는 새로운 레이어 수준 케이퍼빌리티를 레이어 수준에서 :cpp:func:`TestCapability` 로 테스트할 수 있을 것입니다. 문자열 속성을 UTF-8로 반환하는 것이 확실한 드라이버는 TRUE를 반환해야 하는 반면, 자신이 반환하는 인코딩을 모르는 드라이버는 FALSE를 반환해야 합니다. 자신의 인코딩을 알고 있는 모든 드라이버는 UTF-8로 변환해야 합니다.

OGR 드라이버 업데이트
---------------------

어떤 방식으로든 UTF-8 지원으로 재(再)코딩하면, 다음 OGR 드라이버들은 즉시 혜택을 볼 수 있습니다.

-  ODBC (wchar_t / NVARSHAR 필드에 대한 지원 추가)
-  Shapefile
-  GML (XML 인코딩 값 모두를 어떻게 이 RFC의 인코딩 개념과 매핑할지 확실하지 않습니다)
-  PostgreSQL

다른 여러 드라이버들도, 특히 RDBMS 드라이버를 업데이트하면 혜택을 볼 수 있을 것입니다.

구현
----

프랑크 바르메르담이 핵심 iconv() 케이퍼빌리티 및 CPLRecode() 추가 사항을 구현하고 ODBC 드라이버를 업데이트할 것입니다. 관심 있는 개발자들이 다른 OGR 드라이버들이 이 RFC의 정의를 준수하도록 요구할 때 다른 OGR 드라이버들을 업데이트할 것입니다.

GDAL/OGR 1.6.0버전 배포판에 맞춰 핵심 작업을 완료할 것입니다.

참조
----

-  `유니코드 표준 4.0버전 - 구현 지침 <http://unicode.org/versions/Unicode4.0.0/ch05.pdf>`_ 제5장 (PDF)
-  소프트웨어에서 유니코드를 사용하는 방법에 대한 FAQ:
   `http://www.cl.cam.ac.uk/~mgk25/unicode.html <http://www.cl.cam.ac.uk/~mgk25/unicode.html>`_
-  문자열 변환 함수의 FLTK 구현:
   `http://svn.easysw.com/public/fltk/fltk/trunk/src/utf.c <http://svn.easysw.com/public/fltk/fltk/trunk/src/utf.c>`_
-  `http://www.easysw.com/~mike/fltk/doc-2.0/html/utf_8h.html <http://www.easysw.com/~mike/fltk/doc-2.0/html/utf_8h.html>`_
-  #1494 티켓: GML 산출물에 대한 UTF-8 인코딩
-  Libiconv:
   `http://www.gnu.org/software/libiconv/ <http://www.gnu.org/software/libiconv/>`_
-  ICU (또다른 i18n 라이브러리):
   `http://www.icu-project.org/ <http://www.icu-project.org/>`_

