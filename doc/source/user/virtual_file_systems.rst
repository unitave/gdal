.. _virtual_file_systems:

===========================================================================================================
GDAL 가상 파일 시스템 (압축, 네트워크 호스팅 등등): /vsimem, /vsizip, /vsitar, /vsicurl, ...
===========================================================================================================

개요
------------

GDAL은 예를 들어 유닉스 계열 시스템 상의 "/" 계층, 또는 윈도우 상의 "C:\", "D:\" 등등의 "표준" 파일 시스템에 위치한 파일에 접근할 수 있습니다. 그러나 GDAL 래스터 및 벡터 드라이버 대부분은 파일에 접근하기 위해 GDAL에 특화된 추상 개념을 사용합니다. 이로 인해 인메모리 파일, (.zip, .gz, .tar, .tar.gz) 압축 파일, 암호화 파일, (공개적으로 접근 가능한, 또는 상용 클라우드 저장소 서비스의 개인 버켓) 네트워크 상에 저장된 파일 등등 같은 비표준 유형의 파일에 접근할 수 있습니다.

각 특수 파일 시스템은 접두어를 가지며, 파일을 명명하는 일반 문법은 :file:`/vsiPREFIX/...` 입니다. 다음은 그 예시입니다:

::

    gdalinfo /vsizip/my.zip/my.tif

체인 작업
--------

여러 개의 파일 시스템 핸들러를 묶을 수 있습니다:

::

    # 인터넷 상에 있는 ZIP 압축 파일 안의 shapefile에 대한 ogrinfo:

    ogrinfo -ro -al -so /vsizip//vsicurl/https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/ogr/data/shp/poly.zip

    # FTP상에 있는 ZIP 압축 파일 안의 shapefile에 대한 ogrinfo:

    ogrinfo -ro -al -so /vsizip//vsicurl/ftp://user:password@example.com/foldername/file.zip/example.shp

(:file:`/vsizip/vsicurl/...` 처럼 슬래시를 하나만 써도 괜찮다는 사실을 기억하십시오. (그러나 문서 작성 시에는 슬래시를 2개 쓰시기 바랍니다.))

가상 파일 시스템을 지원하는 드라이버
---------------------------------------

"대용량 파일 API"를 지원하는 GDAL 또는 OGR 드라이버만 가상 파일 시스템을 사용할 수 있습니다. 현재 파일 기반 드라이버 거의 대부분이 이 API를 지원합니다. ``gdalinfo --formats`` 또는 ``ogrinfo --formats`` 가운데 하나를 실행한 다음 'v'로 표시된 드라이버를 찾으면 이런 포맷들의 완전한 목록을 얻을 수 있습니다.

대용량 파일 API를 지원하지 않으면서도 가상 파일 시스템을 사용할 수 있는 드라이버 가운데 기억해둘 만한 것은 netCDF, HDF4 및 HDF5 드라이버입니다.

.. _vsizip:

/vsizip/ (ZIP 압축 파일)
------------------------

/vsizip/ 은 ZIP 압축 파일을 사전에 압축 해제하지 않고 실시간(on-the-fly)으로 읽을 수 있게 해주는 파일 핸들러입니다.

ZIP 파일 안에 있는 파일을 가리키려면, 파일명이 반드시 :file:`/vsizip/path/to/the/file.zip/path/inside/the/zip/file` 형식이어야만 합니다. 이때 :file:`path/to/the/file.zip` 은 상대 경로 또는 절대 경로이며 :file:`path/inside/the/zip/file` 은 압축 파일 안에 있는 파일을 가리키는 상대 경로입니다.

ZIP 파일을 디렉터리로 사용하려면 :file:`/vsizip/path/to/the/file.zip` 또는 :file:`/vsizip/path/to/the/file.zip/subdir` 형식을 쓰면 됩니다. :cpp:func:`VSIReadDir` 함수로 디렉터리 목록을 볼 수 있습니다. :cpp:func:`VSIStatL` ("/vsizip/...") 함수를 호출하면 파일의 압축 해제 용량을 반환할 것입니다. ZIP 파일 안에 있는 디렉터리를 정규 파일과 구분하려면 정규 파일 시스템과 마찬가지로 VSI_ISDIR(stat.st_mode) 매크로를 이용하면 됩니다. 디렉터리 목록 및 파일 통계 작업의 속도는 빠릅니다.

주의: ZIP 파일이 루트 위치에 파일 하나만 담고 있는 경우, 그냥 :file:`/vsizip/path/to/the/file.zip` 형식을 쓰면 작동할 것입니다. 다음은 예시입니다:

::

    /vsizip/my.zip/my.tif  (ZIP 파일을 가리키는 상대 경로)
    /vsizip//home/even/my.zip/subdir/my.tif  (ZIP 파일을 가리키는 절대 경로)
    /vsizip/c:\users\even\my.zip\subdir\my.tif

'.kmz', '.ods' 및 '.xlsx' 확장자도 ZIP 호환 압축 파일의 무결한 확장자로 탐지합니다.

GDAL 2.2버전부터, '.zip' 확장자에 의존하지 않고 체인 작업을 활성화할 수 있는 대체 문법을 사용할 수 있습니다:

::

    /vsizip/{/path/to/the/archive}/path/inside/the/zip/file

이때 :file:`/path/to/the/archive` 자체도 이 대체 문법을 사용할 수 있다는 사실을 기억하십시오.

쓰기 케이퍼빌리티도 사용할 수 있습니다. 새 ZIP 파일을 생성하고 기존 (또는 방금 생성한) ZIP 파일에 새 파일을 추가할 수 있습니다.

새 ZIP 파일 생성하기:

::

    fmain = VSIFOpenL("/vsizip/my.zip", "wb");
    subfile = VSIFOpenL("/vsizip/my.zip/subfile", "wb");
    VSIFWriteL("Hello World", 1, strlen("Hello world"), subfile);
    VSIFCloseL(subfile);
    VSIFCloseL(fmain);

기존 ZIP 파일에 새 파일 추가하기:

::

    newfile = VSIFOpenL("/vsizip/my.zip/newfile", "wb");
    VSIFWriteL("Hello World", 1, strlen("Hello world"), newfile);
    VSIFCloseL(newfile);

GDAL 2.4버전부터, :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 정수 또는 ``ALL_CPUS`` 로 설정하면 단일 파일의 멀티스레딩 압축을 활성화할 수 있습니다. 이는 독립 모드의 pigz(parallel implementation of gzip) 유틸리티와 유사합니다. 기본적으로 입력 스트림을 1MB 덩어리로 분할한 다음 (이 덩어리 용량은 :decl_configoption:`CPL_VSIL_DEFLATE_CHUNK_SIZE` 환경설정 옵션을 "x K" 또는 "x M" 같은 값으로 설정해서 조정할 수 있습니다) 각 덩어리를 독립적으로 압축합니다. (이 각 압축 파일은 0x00 0x00 0xFF 0xFF 0x00 0x00 0x00 0xFF 0xFF 9바이트 마커로 종료됩니다. 이 마커는 스트림 및 딕셔너리 전체를 플러시했다는 신호로, 각 덩어리를 독립적으로 디코딩할 수 있게 해줍니다.) 이 습성은 압축률을 살짝 저하시키기 때문에, 덩어리 용량을 너무 작게 설정하지는 말아야 합니다.

교차삽입 읽기 및 쓰기는 지원하지 않습니다. 새로 생성된 ZIP 파일을 읽기 모드로 열려면 먼저 닫은 다음 다시 열어야만 합니다.

.. _vsigzip:

/vsigzip/ (GZip 압축 파일)
------------------------

/vsigzip/ 은 GZip(.gz) 압축 파일을 사전에 압축 해제하지 않고 실시간(on-the-fly)으로 읽을 수 있게 해주는 파일 핸들러입니다.

GDAL이 압축 해제한 것처럼 GZip 파일을 보려면, :file:`/vsigzip/path/to/the/file.gz` 문법을 사용해야만 합니다. 이때 :file:`path/to/the/file.gz` 은 상대 경로 또는 절대 경로입니다. 다음은 그 예시입니다:

::

    /vsigzip/my.gz # (relative path to the .gz)
    /vsigzip//home/even/my.gz # (absolute path to the .gz)
    /vsigzip/c:\users\even\my.gz

:cpp:func:`VSIStatL` 함수를 호출하면 파일의 압축 해제 용량을 반환할 것입니다. 그러나 전체 파일을 압축 해제해야 하기 때문에 대용량 파일의 경우 작업 속도가 느려질 수도 있습니다. 파일의 끝 부분 또는 임의의 위치를 찾는 것도 비슷하게 느립니다. 이 처리 속도를 높이려면 메모리에 "스냅샷(snapshot)"들을 내부적으로 생성해서 이미 압축 해제된 파일의 일부분을 더 빠른 방식으로 찾을 수 있게 해줘야 합니다. 이 스냅샷 메커니즘은 /vsizip/ 파일에도 적용됩니다.

파일이 쓰기 가능한 위치에 있는 경우, 압축 해제된 파일의 용량을 나타내는 .gz.properties 확장자를 가진 파일을 생성합니다. (:decl_configoption:`CPL_VSIL_GZIP_WRITE_PROPERTIES` 환경설정 옵션을 NO로 설정하면 이 파일을 생성하지 않게 할 수 있습니다.)

쓰기 케이퍼빌리티도 사용할 수 있지만, 교차삽입 읽기 및 쓰기는 지원하지 않습니다.

GDAL 2.4버전부터, :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 정수 또는 ``ALL_CPUS`` 로 설정하면 단일 파일의 멀티스레딩 압축을 활성화할 수 있습니다. 이는 독립 모드의 pigz(parallel implementation of gzip) 유틸리티와 유사합니다. 기본적으로 입력 스트림을 1MB 덩어리로 분할한 다음 (이 덩어리 용량은 :decl_configoption:`CPL_VSIL_DEFLATE_CHUNK_SIZE` 환경설정 옵션을 "x K" 또는 "x M" 같은 값으로 설정해서 조정할 수 있습니다) 각 덩어리를 독립적으로 압축합니다. (이 각 압축 파일은 0x00 0x00 0xFF 0xFF 0x00 0x00 0x00 0xFF 0xFF 9바이트 마커로 종료됩니다. 이 마커는 스트림 및 딕셔너리 전체를 플러시했다는 신호로, 각 덩어리를 독립적으로 디코딩할 수 있게 해줍니다.) 이 습성은 압축률을 살짝 저하시키기 때문에, 덩어리 용량을 너무 작게 설정하지는 말아야 합니다.

.. _vsitar:

/vsitar/ (.tar, .tgz 압축 파일)
------------------------------

/vsitar/ 는 정규 비압축 .tar 또는 압축 .tgz 또는 .tar.gz 파일을 사전에 압축 해제하지 않고 실시간(on-the-fly)으로 읽을 수 있게 해주는 파일 핸들러입니다.

'.tar', '.tgz' 또는 '.tar.gz' 파일 안에 있는 파일을 가리키려면, 파일명이 반드시 :file:`/vsitar/path/to/the/file.tar/path/inside/the/tar/file` 형식이어야만 합니다. 이때 :file:`path/to/the/file.tar` 는 상대 경로 또는 절대 경로이며 :file:`path/inside/the/tar/file` 은 압축 파일 안에 있는 파일을 가리키는 상대 경로입니다.

TAR 파일을 디렉터리로 사용하려면 :file:`/vsitar/path/to/the/file.tar` 또는 :file:`/vsitar/path/to/the/file.tar/subdir` 형식을 쓰면 됩니다. :cpp:func:`VSIReadDir` 함수로 디렉터리 목록을 볼 수 있습니다. :cpp:func:`VSIStatL` ("/vsitar/...") 함수를 호출하면 파일의 압축 해제 용량을 반환할 것입니다. TAR 파일 안에 있는 디렉터리를 정규 파일과 구분하려면 정규 파일 시스템과 마찬가지로 VSI_ISDIR(stat.st_mode) 매크로를 이용하면 됩니다. 디렉터리 목록 및 파일 통계 작업의 속도는 빠릅니다.

주의: TAR 파일이 루트 위치에 파일 하나만 담고 있는 경우, 그냥 :file:`/vsitar/path/to/the/file.tar` 형식을 쓰면 작동할 것입니다. 다음은 예시입니다:

::

    /vsitar/my.tar/my.tif # (relative path to the .tar)
    /vsitar//home/even/my.tar/subdir/my.tif # (absolute path to the .tar)
    /vsitar/c:\users\even\my.tar\subdir\my.tif

GDAL 2.2버전부터, '.tar' 확장자에 의존하지 않고 체인 작업을 활성화할 수 있는 대체 문법을 사용할 수 있습니다:

::

    :file:`/vsitar/{/path/to/the/archive}/path/inside/the/tar/file

이때 :file:`/path/to/the/archive` 자체도 이 대체 문법을 사용할 수 있다는 사실을 기억하십시오.

네트워크 기반 파일 시스템
--------------------------

특정 서명 인증 정보 스키마를 요구하지 않는 온라인 리소스를 위한 일반 :ref:`/vsicurl/ <vsicurl>` 파일 시스템 핸들러가 존재합니다. /vsicurl/ 은 :ref:`/vsis3/ <vsis3>`,  :ref:`/vsigs/ <vsigs>`, :ref:`/vsiaz/ <vsiaz>`, :ref:`/vsioss/ <vsioss>` 또는 :ref:`/vsiswift/ <vsiswift>` 같은 상용 클라우드 저장소 서비스 용 하위 파일 시스템으로 특화되어 있습니다.

전체 파일을 스트리밍 방식으로 읽어올 수 있는 경우, 앞의 클라우드 저장소 서비스에 :ref:`/vsicurl_streaming/ <vsicurl_streaming>` 및 그 변이형들을 이용하는 편이 좋습니다. 더 효율적이기 때문입니다.

자격인증서 설정법
++++++++++++++++++++++++

클라우드 저장소 서비스는 자격인증서(credentials) 설정을 요구합니다. 일부 서비스의 경우 환경설정 파일(~/.aws/config, ~/.boto 등등)을 통해 또는 환경 변수/환경설정 옵션을 통해 자격인증서를 제공할 수 있습니다.

GDAL 3.5버전부터, :cpp:func:`VSISetCredential` 메소드를 사용해서 파일 경로 수준에서 단위 설정(granularity)을 가진 환경설정 옵션을 설정할 수 있습니다. 동일한 가상 파일 시스템이지만 서로 다른 자격인증서를 사용하는 경우 (예: "/vsis3/foo"와 "/vsis3/bar" 버켓에 각각 다른 자격인증서를 사용하는 경우) 이 메커니즘이 더 쉽습니다.

GDAL 3.5버전부터, :cpp:func:`CPLLoadConfigOptionsFromFile` 메소드로 특정 자격인증서를 명확하게 불러오는 방법 또는 :cpp:func:`CPLLoadConfigOptionsFromPredefinedFiles` 메소드로 기본 자격인증서를 자동적으로 불러오는 방법 가운데 하나를 이용해서 :ref:`GDAL 환경설정 파일 <gdal_configuration_file>` 에 자격인증서를 지정할 수 있습니다.

``[credentials]`` 단락에 이 자격인증서들을 저장해야 하며, ``[.`` 로 시작하는 이름을 (예: ``[.some_arbitrary_name]``) 가진 상대 하위 단락에 각 경로 접두어를 넣어야 합니다. 각 하위 단락의 첫 번째 키는 ``path`` 입니다:
`
.. code-block::

    [credentials]

    [.private_bucket]
    path=/vsis3/my_private_bucket
    AWS_SECRET_ACCESS_KEY=...
    AWS_ACCESS_KEY_ID=...

    [.sentinel_s2_l1c]
    path=/vsis3/sentinel-s2-l1c
    AWS_REQUEST_PAYER=requester


.. _vsicurl:

/vsicurl/ (http/https/ftp 파일: 임의 접근)
+++++++++++++++++++++++++++++++++++++++++++++++

/vsicurl/ 은 HTTP/FTP 웹 프로토콜을 통해 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsicurl/http[s]://path/to/remote/resource` 또는 :file:`/vsicurl/ftp://path/to/remote/resource` 형식의 파일명을 인식합니다. 이때 :file:`path/to/remote/resource` 가 원격 리소스의 URL입니다.

다음은 :program:`ogrinfo` 유틸리티를 사용해서 인터넷 상에 있는 shapefile을 읽어오는 예시입니다:

::

    ogrinfo -ro -al -so /vsicurl/https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/ogr/data/poly.shp

GDAL 2.3버전부터, ``/vsicurl?[option_i=val_i&]*url=http://...`` 문법을 이용해서 파일명 안에 옵션을 전송할 수 있습니다. 이때 각 옵션 이름과 ("url" 값을 포함하는) 값은 URL 인코딩이어야 합니다. 현재 다음 옵션들을 지원합니다:

- use_head=yes/no:
  HTTP HEAD 요청을 생략할 수 있는지 여부를 선택합니다. 기본값은 YES입니다. 이 옵션을 설정하면 :decl_configoption:`CPL_VSIL_CURL_USE_HEAD` 환경설정 옵션의 습성을 대체합니다.

- max_retry=number:
  기본값은 0입니다. 이 옵션을 설정하면 :decl_configoption:`GDAL_HTTP_MAX_RETRY` 환경설정 옵션의 습성을 대체합니다.

- retry_delay=number_in_seconds:
  기본값은 30입니다. 이 옵션을 설정하면 :decl_configoption:`GDAL_HTTP_RETRY_DELAY` 환경설정 옵션의 습성을 대체합니다.

- list_dir=yes/no:
  파일이 위치해 있는 디렉터리의 파일 목록을 읽어오려 시도해야 할지 여부를 선택합니다. 기본값은 YES입니다.

(HTTP 서버가 임의 읽기를 지원해야 하는) 부분 다운로드는 기본적으로 16KB 단위로 수행됩니다. GDAL 2.3버전부터, :decl_configoption:`CPL_VSIL_CURL_CHUNK_SIZE` 환경설정 옵션을 바이트 단위 값으로 설정해서 덩어리 용량을 환경설정할 수 있습니다. 드라이버가 순차 읽기를 탐지한 경우, 다운로드 성능을 향상시키기 위해 덩어리 용량을 점진적으로 2MB까지 증가시킬 것입니다. GDAL 2.3버전부터, :decl_configoption:`GDAL_INGESTED_BYTES_AT_OPEN` 환경설정 옵션을 설정해서 파일 열기 시 GET 호출 한 번에 읽어올 바이트 수를 강제할 수 있습니다. (대용량 헤더를 가진 클라우드 최적화 GeoTIFF의 읽기 성능을 향상시킬 수 있습니다.)

(HTTP 및 HTTPS 프로토콜 용) :decl_configoption:`GDAL_HTTP_PROXY`, (HTTPS 프로토콜 전용) :decl_configoption:`GDAL_HTTPS_PROXY`, :decl_configoption:`GDAL_HTTP_PROXYUSERPWD` 그리고 :decl_configoption:`GDAL_PROXY_AUTH` 환경설정 옵션을 사용해서 프록시 서버를 정의할 수 있습니다.
이때 사용되는 문법은 ``CURLOPT_PROXY``, ``CURLOPT_PROXYUSERPWD`` 및 ``CURLOPT_PROXYAUTH`` 옵션을 사용하는 cURL 문법입니다.

GDAL 2.1.3버전부터, :decl_configoption:`CURL_CA_BUNDLE` 또는 :decl_configoption:`SSL_CERT_FILE` 환경설정 옵션을 사용해서 인증 기관(Certification Authority; CA) 번들 파일을 가리키는 경로를 설정할 수 있습니다. (이 두 옵션을 지정하지 않는 경우, cURL이 시스템 위치에 있는 파일을 사용할 것입니다.)

GDAL 2.3버전부터, :decl_configoption:`GDAL_HTTP_HEADER_FILE` 환경설정 옵션을 "key: value" HTTP 헤더를 가진 텍스트 파일명을 가리키도록 설정해서 추가 HTTP 헤더를 전송할 수 있습니다. :decl_configoption:`CPL_CURL_VERBOSE` 환경설정 옵션을 ``--debug`` 스위치와 함께 YES로 설정하면 추가 HTTP 헤더들을 전부 그리고 그 이상의 정보를 볼 수 있습니다.

GDAL 2.3버전부터, :decl_configoption:`GDAL_HTTP_MAX_RETRY` (시도 횟수) 및 (초 단위) :decl_configoption:`GDAL_HTTP_RETRY_DELAY` 환경설정 옵션을 설정해서 HTTP 429, 502, 503 또는 504 오류가 발생한 경우 요청을 몇 초 간격으로 몇 번 재시도할 것인지 제어할 수 있습니다.

환경설정 옵션을 통해 :cpp:func:`CPLHTTPFetch` 함수의 좀 더 일반적인 옵션을 사용할 수 있습니다.

:decl_configoption:`VSI_CACHE` 환경설정 옵션을 TRUE로 설정하면 RAM에 파일을 캐시할 수 있습니다. 캐시 크기의 기본값은 25MB이지만, 환경설정 옵션 :decl_configoption:`VSI_CACHE_SIZE` 를 바이트 단위로 설정해서 수정할 수 있습니다. 파일 핸들을 종료할 때 해당 캐시에 있는 내용을 폐기합니다.

뿐만 아니라, 다운로드된 모든 콘텐츠 사이에 공유되는 16MB 크기의 전체 수준 최소 최근 사용(least-recently-used) 캐시는 기본적으로 활성화되며 해당 캐시에 있는 내용은 프로세스 수명 동안 또는 :cpp:func:`VSICurlClearCache` 메소드를 호출할 때까지 파일 핸들을 종료하고 다시 열어도 재사용할 수도 있습니다. GDAL 2.3버전부터, :decl_configoption:`CPL_VSIL_CURL_CACHE_SIZE` 환경설정 옵션을 바이트 단위로 설정해서 전체 수준 최소 최근 사용 캐시의 크기를 수정할 수 있습니다.

GDAL 2.3버전부터, :decl_configoption:`CPL_VSIL_CURL_NON_CACHED` 환경설정 옵션을 :file:`/vsicurl/http://example.com/foo.tif:/vsicurl/http://example.com/some_directory` 같은 값으로 설정하면 파일 핸들 종료 시 해당 파일(들)과 연결되어 캐시된 모든 콘텐츠를 더 이상 캐시하지 않습니다. GDAL 관련 코드를 실행하는 동안 수정될 수 있는 리소스를 작업하는 경우 이 메커니즘이 도움이 될 수 있습니다. 또는 :cpp:func:`VSICurlClearCache` 함수를 사용할 수도 있습니다.

GDAL 2.1버전부터, 라운드트립(무결성을 잃지 않은 채 데이터를 내보내고 다시 가져오기, 또는 그 반대)을 최소화하기 위해 ``/vsicurl/`` 이 자신의 유효 기간 동안 아마존 S3 서명 URL로 리다이렉트된 URL에 직접 쿼리하려 시도할 것입니다. :decl_configoption:`CPL_VSIL_CURL_USE_S3_REDIRECT` 환경설정 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

:cpp:func:`VSIStatL` 함수를 호출하면 'st_size' 멤버에 파일 용량을 반환하고 st_mode 멤버에 파일 특성 -- 파일 또는 디렉터리 -- 을 반환할 것입니다. (현재 후자는 FTP 리소스를 작업하는 경우에만 신뢰할 수 있습니다.)

:cpp:func:`VSIReadDir` 함수는 아파치 및 마이크로소프트 IIS 같은 가장 유명한 웹 서버가 반환하는 HTML 디렉터리 목록을 파싱할 수 있을 것입니다.

.. _vsicurl_streaming:

/vsicurl_streaming/ (http/https/ftp 파일: 스트리밍)
+++++++++++++++++++++++++++++++++++++++++++++++++++++

/vsicurl_streaming/ 은 HTTP/FTP 웹 프로토콜을 통해 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

이 파일 핸들러가 파일에서 임의의 오프셋을 찾을 수 있긴 하지만, 효율적이지는 않습니다. 효율적인 임의 접근이 필요한데 서버가 범위 다운로드를 지원하는 경우, :ref:`/vsicurl/ <vsicurl>` 파일 시스템 핸들러를 대신 사용해야 합니다.

:file:`/vsicurl_streaming/http[s]://path/to/remote/resource` 또는 :file:`/vsicurl_streaming/ftp://path/to/remote/resource` 형식의 파일명을 인식합니다. 이때 :file:`path/to/remote/resource` 가 원격 리소스의 URL입니다.

(HTTP 및 HTTPS 프로토콜 용) :decl_configoption:`GDAL_HTTP_PROXY`, (HTTPS 프로토콜 전용) :decl_configoption:`GDAL_HTTPS_PROXY`, :decl_configoption:`GDAL_HTTP_PROXYUSERPWD` 그리고 :decl_configoption:`GDAL_PROXY_AUTH` 환경설정 옵션을 사용해서 프록시 서버를 정의할 수 있습니다.
이때 사용되는 문법은 ``CURLOPT_PROXY``, ``CURLOPT_PROXYUSERPWD`` 및 ``CURLOPT_PROXYAUTH`` 옵션을 사용하는 cURL 문법입니다.

GDAL 2.1.3버전부터, :decl_configoption:`CURL_CA_BUNDLE` 또는 :decl_configoption:`SSL_CERT_FILE` 환경설정 옵션을 사용해서 인증 기관(Certification Authority; CA) 번들 파일을 가리키는 경로를 설정할 수 있습니다. (이 두 옵션을 지정하지 않는 경우, cURL이 시스템 위치에 있는 파일을 사용할 것입니다.)

:decl_configoption:`VSI_CACHE` 환경설정 옵션을 TRUE로 설정하면 RAM에 파일을 캐시할 수 있습니다. 캐시 크기의 기본값은 25MB이지만, :decl_configoption:`VSI_CACHE_SIZE` 환경설정 옵션의 값을 바이트 단위로 설정해서 수정할 수 있습니다.

:cpp:func:`VSIStatL` 함수를 호출하면 'st_size' 멤버에 파일 용량을 반환하고 st_mode 멤버에 파일 특성 -- 파일 또는 디렉터리 -- 을 반환할 것입니다. (현재 후자는 FTP 리소스를 작업하는 경우에만 신뢰할 수 있습니다.)

.. _vsis3:

/vsis3/ (AWS S3 파일)
++++++++++++++++++++++

/vsis3/ 은 AWS S3 버켓에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

/vsis3/ 은 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) :cpp:func:`VSIUnlink` 메소드로 파일을 삭제할 수도 있습니다. GDAL 2.3버전부터 :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고 :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.

:file:`/vsis3/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 S3 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) S3 객체의 "key"입니다.


:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

몇 개의 인증 메소드를 사용할 수 있으며, 다음 순서대로 시도합니다:

1. :decl_configoption:`AWS_NO_SIGN_REQUEST=YES` 환경설정 옵션을 설정한 경우, 서명 요청을 비활성화합니다. 공개 접근 권한을 가진 버켓에 이 옵션을 사용할 수도 있습니다. GDAL 2.3버전부터 사용할 수 있습니다.

2. :decl_configoption:`AWS_SECRET_ACCESS_KEY` 및 :decl_configoption:`AWS_ACCESS_KEY_ID` 환경설정 옵션을 설정할 수 있습니다. 임시 자격인증서를 사용하는 경우 :decl_configoption:`AWS_SESSION_TOKEN` 환경설정 옵션도 설정해야만 합니다.

3. GDAL 2.3버전부터, "aws" 명령줄 유틸리티 또는 Boto3 지원을 사용하는 방법과 비슷한 방법을 대신 사용해서 자격인증서를 제공할 수 있습니다. 앞에서 말한 환경 변수를 지정하지 않는 경우, ``~/.aws/credentials`` 또는 ``%UserProfile%/.aws/credentials`` 파일을 (또는 :decl_configoption:`CPL_AWS_CREDENTIALS_FILE` 환경설정 옵션이 가리키는 파일을) 읽어올 것입니다. :decl_configoption:`AWS_DEFAULT_PROFILE` 환경 변수로 또는 GDAL 3.2버전부터 :decl_configoption:`AWS_PROFILE` 환경 변수로 프로파일을 지정할 수도 있습니다. (기본 프로파일은 "default"입니다.)

4. 자격인증서 및 AWS 영역(region)을 가져오기 위해 ``~/.aws/config`` 또는 ``%UserProfile%/.aws/config`` 파일을 (또는 :decl_configoption:`AWS_CONFIG_FILE` 환경설정 옵션이 가리키는 파일을) 사용할 수도 있습니다.

5. 앞의 방법들이 모두 실패하면, EC2 인스턴스 상에 GDAL을 사용하는 경우 인스턴스 프로파일 자격인증서를 가져올 것입니다.

:decl_configoption:`AWS_REGION` (또는 GDAL 2.3버전부터 :decl_configoption:`AWS_DEFAULT_REGION`) 환경설정 옵션을 지원하는 S3 영역 가운데 하나로 설정할 수 있습니다. 기본값은 ``us-east-1`` 입니다.

GDAL 2.2버전부터, :decl_configoption:`AWS_REQUEST_PAYER` 환경설정 옵션을 "requester"로 설정해서 'Requester Pays' 버켓을 사용 가능하게 할 수도 있습니다.

:decl_configoption:`AWS_S3_ENDPOINT` 환경설정 옵션의 기본값은 "s3.amazonaws.com"입니다.

:decl_configoption:`AWS_HTTPS` 환경설정 옵션옵션의 기본값은 YES입니다.

:decl_configoption:`AWS_VIRTUAL_HOSTING` 환경설정 옵션옵션의 기본값은 TRUE입니다. 이 옵션으로 버켓에 접근하는 두 가지 방식을 환경설정할 수 있습니다. 자세한 내용은 버켓(Bucket)과 호스트명(Host Name)을 참조하십시오.

- ``TRUE``:
  "mybucket.cname.domain.com" 같은 가상 버켓 호스트명을 통해 버켓을 식별합니다.

- ``FALSE``:
  버켓을 "cname.domain.com/mybucket" 같은 URI에 있는 최상위 디렉터리로 식별합니다.

작성 시, S3 다중부분 업로드 API를 이용해서 파일을 업로드합니다. 덩어리 크기의 기본값은 50MB로 (50MB 부분들 10,000개를 업로드해서) 500GB까지의 파일을 생성할 수 있습니다. 이보다 큰 파일이 필요한 경우, :decl_configoption:`VSIS3_CHUNK_SIZE` 환경설정 옵션을 더 큰 (MB 단위) 값으로 증가시키십시오. 프로세스가 죽어서 파일을 제대로 종료하지 못 했다면, 다중부분 업로드가 열려진 채일 것이기 때문에 아마존이 부분들의 저장소에 대해 과금할 것입니다. 사용자 스스로 (예를 들어 s3cmd 유틸리티를 통해) "ghost" 업로드 같은 수단을 이용해서 다중부분 업로드를 중단시켜야 할 것입니다. 덩어리 크기보다 작은 파일의 경우, 다중부분 업로드 API 대신 단순한 PUT 요청을 사용하십시오.

GDAL 2.4버전부터, 디렉터리 목록을 가져올 때 :decl_configoption:`CPL_VSIL_CURL_IGNORE_GLACIER_STORAGE` 환경설정 옵션을 NO로 설정하지 않는 이상 GLACIER 저장소 클래스 파일을 무시합니다. 이 옵션은 GDAL 3.5버전에서 저장소 클래스 이름을 쉼표로 구분한 목록을 입력받고 기본값이 ``GLACIER,DEEP_ARCHIVE`` 인 :decl_configoption:`CPL_VSIL_CURL_IGNORE_STORAGE_CLASSES` 환경설정 옵션으로 대체되었습니다. (이 옵션을 빈 문자열로 설정하는 경우 모든 저장소 클래스의 객체를 가져옵니다.)

GDAL 3.1버전부터, :cpp:func:`VSIRename` 작업을 지원합니다. (먼저 원본 파일을 새 이름으로 복사한 다음 원본 파일을 삭제합니다.)

GDAL 3.1버전부터, :cpp:func:`VSIRmdirRecursive` 작업을 (배치(batch) 삭제 메소드를 이용해서) 지원합니다. 배치 삭제를 지원하지 않는 S3 같은 API를 사용하는 경우 (GDAL 3.2 이상 버전) :decl_configoption:`CPL_VSIS3_USE_BASE_RMDIR_RECURSIVE` 환경설정 옵션을 YES로 설정하면 됩니다.

GDAL 3.5버전부터, IAM 역할(role) 가정을 사용하는 프로파일을 처리합니다. (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html 페이지를 참조하십시오.) 이런 프로파일에는 ``role_arn`` 및 ``source_profile`` 키워드가 필요합니다. ``external_id``, ``mfa_serial`` 및 ``role_session_name`` 키워드도 선택적으로 지정할 수 있습니다. 현재 ``credential_source`` 키워드는 지원하지 않습니다.

.. versionadded:: 2.1

.. _vsis3_streaming:

/vsis3_streaming/ (AWS S3 파일: 스트리밍)
+++++++++++++++++++++++++++++++++++++++++++

/vsis3_streaming/ 은 AWS S3 버켓에서 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsis3_streaming/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 S3 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) S3 객체의 "key"입니다.

인증 옵션 및 읽기 전용 기능은 :ref:`/vsis3/ <vsis3>` 와 동일합니다.

.. versionadded:: 2.1

.. _vsigs:

/vsigs/ (구글 클라우드 저장소 파일)
++++++++++++++++++++++++++++++++++++

/vsigs/ 는 구글 클라우드 저장소 버켓에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

GDAL 2.3버전부터, /vsigs/ 는 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) :cpp:func:`VSIUnlink` 메소드로 파일을 삭제하고, :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고, :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.

:file:`/vsigs/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 객체의 "key"입니다.

:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

몇 개의 인증 메소드를 사용할 수 있으며, 다음 순서대로 시도합니다:

1. :decl_configoption:`GS_NO_SIGN_REQUEST=YES` 환경설정 옵션을 설정한 경우, 서명 요청을 비활성화합니다. 공개 접근 권한을 가진 버켓에 이 옵션을 사용할 수도 있습니다. GDAL 3.4버전부터 사용할 수 있습니다.

2. AWS 스타일 인증에 :decl_configoption:`GS_SECRET_ACCESS_KEY` 및 :decl_configoption:`GS_ACCESS_KEY_ID` 환경설정 옵션을 설정할 수 있습니다.

3. :decl_configoption:`GDAL_HTTP_HEADER_FILE` 환경설정 옵션을 "key: value" HTTP 헤더를 가진 텍스트 파일명을 가리키도록 설정할 수 있습니다. 일반적으로, 이 파일은 "Authorization: Bearer XXXXXXXXX" 줄을 담고 있어야만 합니다.

4. GDAL 2.3버전부터, :decl_configoption:`GS_OAUTH2_REFRESH_TOKEN` 환경설정 옵션을 설정해서 OAuth2 클라이언트 인증 정보를 설정할 수 있습니다. https://developers.google.com/identity/protocols/oauth2?csw=1 페이지를 참조하십시오. ``gdal_auth.py -s storage`` 또는 ``gdal_auth.py -s storage-rw`` 스크립트로 이 새로고침 토큰을 얻어올 수 있습니다.
   주의: 기본 GDAL 응용 프로그램 자격인증서를 사용하는 대신, :decl_configoption:`GS_OAUTH2_CLIENT_ID` 및 :decl_configoption:`GS_OAUTH2_CLIENT_SECRET` 환경설정 옵션을 정의할 수도 있습니다. (/vsigs/ 를 실행하기 전에 gdal_auth.py 스크립트에 대해 두 옵션을 정의해야 합니다.)

5. GDAL 2.3버전부터, :decl_configoption:`GOOGLE_APPLICATION_CREDENTIALS` 환경설정 옵션을 OAuth2 서비스 계정 자격인증서(``type: service_account``)를, 특히 개인 키와 클라이언트 이메일 주소를 담고 있는 JSON 파일을 가리키도록 설정할 수 있습니다. 이 인증 메소드에 관해 자세히 알고 싶다면 https://developers.google.com/identity/protocols/oauth2/service-account 페이지를 참조하십시오. 버켓이 서비스 계정에 "Storage Legacy Bucket Owner" 또는 "Storage Legacy Bucket Reader" 권한을 허용해야만 합니다. 필요한 경우 :decl_configoption:`GS_OAUTH2_SCOPE` 환경설정 옵션을 설정해서 기본 권한 스코프를 "https://www.googleapis.com/auth/devstorage.read_write"로부터 "https://www.googleapis.com/auth/devstorage.read_only"로 변경할 수 있습니다.

6. GDAL 3.4.2버전부터, :decl_configoption:`GOOGLE_APPLICATION_CREDENTIALS` 환경설정 옵션을 설정해서 OAuth2 사용자 자격인증서(``type: authorized_user``)를 담고 있는 JSON 파일을 가리키도록 설정할 수 있습니다.

7. GDAL 2.3버전부터, 앞 메소드의 변이형을 사용할 수 있습니다. :decl_configoption:`GS_OAUTH2_PRIVATE_KEY` (또는 :decl_configoption:`GS_OAUTH2_PRIVATE_KEY_FILE)` 및 :decl_configoption:`GS_OAUTH2_CLIENT_EMAIL` 환경설정 옵션을 OAuth2 서비스 계정 인증을 사용하도록 설정할 수 있습니다. 이 인증 메소드에 관해 자세히 알고 싶다면 https://developers.google.com/identity/protocols/oauth2/service-account 페이지를 참조하십시오. :decl_configoption:`GS_OAUTH2_PRIVATE_KEY` 환경설정 옵션이 개인 키를 ``-----BEGIN PRIVATE KEY-----`` 로 시작하는 그때 그때 즉시 처리하는 문자열로 담고 있어야만 합니다. 또는 그 대신 :decl_configoption:`GS_OAUTH2_PRIVATE_KEY_FILE` 환경설정 옵션을 이런 개인 키를 담고 있는 파일명을 나타내도록 설정할 수도 있습니다. 버켓이 서비스 계정에 "Storage Legacy Bucket Owner" 또는 "Storage Legacy Bucket Reader" 권한을 허용해야만 합니다. 필요한 경우 :decl_configoption:`GS_OAUTH2_SCOPE` 환경설정 옵션을 설정해서 기본 권한 스코프를 "https://www.googleapis.com/auth/devstorage.read_write"로부터 "https://www.googleapis.com/auth/devstorage.read_only"로 변경할 수 있습니다.

8. GDAL 2.3버전부터, "gsutil" 명령줄 유틸리티 또는 Boto3 지원을 사용하는 방법과 비슷한 방법을 대신 사용해서 자격인증서를 제공할 수 있습니다. 앞에서 말한 환경 변수를 지정하지 않는 경우, AWS 스타일 인증에 대해 'gs_secret_access_key' 및 'gs_access_key_id' 항목을 찾기 위해 :file:`~/.boto` 또는 :file:`UserProfile%/.boto` 파일을 (또는 :decl_configoption:`CPL_GS_CREDENTIALS_FILE` 환경설정 옵션이 가리키는 파일을) 읽어올 것입니다. 찾지 못 하는 경우, OAuth2 클라이언트 인증 용 'gs_oauth2_refresh_token' (그리고 선택적인 'client_id' 및 'client_secret') 항목을 검색할 것입니다.

9. (GDAL 2.3버전부터) 마지막으로 앞의 방법들이 모두 실패하면 코드가 현재 머신이 구글 컴퓨트 엔진 인스턴스인지 확인하고, 그렇다면 (가상 머신과 관련된 기본 서비스 계정을 이용해서) 그에 관련된 권한을 사용할 것입니다. 머신을 강제로 구글 컴퓨트 엔진 인스턴스로 탐지되게 하려면 (예를 들어 부트 로그에 접근할 수 없는 컨테이너에서 실행되는 코드의 경우) :decl_configoption:`CPL_MACHINE_IS_GCE` 환경설정 옵션을 YES로 설정하면 됩니다.

GDAL 3.1버전부터, Rename() 작업을 지원합니다. (먼저 원본 파일을 새 이름으로 복사한 다음 원본 파일을 삭제합니다.)

GDAL 3.4버전부터, :decl_configoption:`GS_USER_PROJECT` 환경설정 옵션을 구글 프로젝트 ID로 설정해서 'Requester Pays' 버켓을 대상으로 하는 요청에 대해 과금할 수 있습니다. (https://cloud.google.com/storage/docs/xml-api/reference-headers#xgooguserproject 페이지를 참조하십시오.)

.. versionadded:: 2.2

.. _vsigs_streaming:

/vsigs_streaming/ (구글 클라우드 저장소 파일: 스트리밍)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

/vsigs_streaming/ 은 구글 클라우드 저장소 버켓에서 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsigs_streaming/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 객체의 "key"입니다.

인증 옵션 및 읽기 전용 기능은 :ref:`/vsigs/ <vsigs>` 와 동일합니다.

.. versionadded:: 2.2

.. _vsiaz:

/vsiaz/ (마이크로소프트 애저 블랍 파일)
++++++++++++++++++++++++++++++++++++

/vsiaz/ 는 마이크로소프트 애저 블랍(Microsoft Azure Blob) 컨테이너에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

애저 데이터 레이크 저장소 2세대 용 관련 파일 시스템에 대해서는 :ref:`/vsiadls/ <vsiadls>` 를 읽어보십시오.

/vsiaz/ 는 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) 파일 용량이 4MB 이하인 경우 블록 블랍을 생성할 것입니다. 4MB를 초과하는 경우 추가 블랍을 생성할 것입니다. (최대 파일 용량은 195GB입니다.)

:cpp:func:`VSIUnlink` 메소드로 파일을 삭제하고, :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고, :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.
주의: :cpp:func:`VSIMkdir` 메소드를 이용하는 경우 비어 있는 숨겨진 파일 :file:`.gdal_marker_for_dir` 를 생성합니다. 애저 블랍이 빈 디렉터리를 네이티브하게 지원하지 못 하기 때문입니다. 해당 디렉터리에 남아 있는 마지막 파일이 이 숨겨진 파일인 경우, :cpp:func:`VSIRmdir` 메소드가 해당 디렉터리를 자동으로 삭제할 것입니다. :cpp:func:`VSIReadDir` 메소드는 이 숨겨진 파일을 보지 못할 것입니다.
:cpp:func:`VSIMkdir` 메소드로 생성되지 않은 디렉터리에서 파일을 삭제하는 경우, 마지막 파일을 삭제했을 때 애저가 해당 디렉터리도 자동으로 제거합니다. 따라서 :cpp:func:`VSIRmdir` 호출 시 ``VSIUnlink("/vsiaz/container/subdir/lastfile")`` 뒤에 ``VSIRmdir("/vsiaz/container/subdir")`` 가 오는 경우 실패할 것입니다.

:file:`/vsiaz/container/key` 형식의 파일명을 인식합니다. 이때, ``container`` 가 컨테이너의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 객체의 "key"입니다.

:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

몇 개의 인증 메소드를 사용할 수 있으며, 다음 순서대로 시도합니다:

1. 관리자(administration) 인터페이스의 접근 키 부분에 :decl_configoption:`AZURE_STORAGE_CONNECTION_STRING` 환경설정 옵션을 지정합니다. 이 옵션은 계정명 및 보안 키 둘 다 담고 있습니다.

2. :decl_configoption:`AZURE_STORAGE_ACCOUNT` 환경설정 옵션을 설정해서 계정명 및 다음을 지정합니다:

    a) (GDAL 3.5 이상 버전) :decl_configoption:`AZURE_STORAGE_ACCESS_TOKEN` 환경설정 옵션을 설정해서 접근 토큰을 지정합니다. 이 접근 토큰이 "Authorization: Bearer ${AZURE_STORAGE_ACCESS_TOKEN}" 헤더에 포함될 것입니다. 일반적으로 마이크로소프트 인증 라이브버리(Microsoft Authentication Library; MSAL)를 이용해서 이 접근 토큰을 얻습니다.
    b) :decl_configoption:`AZURE_STORAGE_ACCESS_KEY` 환경설정 옵션을 설정해서 보안 키를 지정합니다.
    c) :decl_configoption:`AZURE_NO_SIGN_REQUEST=YES` 환경설정 옵션을 모든 서명 요청을 비활성화하도록 설정합니다. 공개 접근 권한을 가진 계정에 이 옵션을 사용할 수도 있습니다. GDAL 3.2버전부터 사용할 수 있습니다.
    d) :decl_configoption:`AZURE_STORAGE_SAS_TOKEN` (GDAL 3.5 미만 버전의 경우 :decl_configoption:`AZURE_SAS`) 환경설정 옵션을 설정해서 공유 접근 서명(Shared Access Signature)을 지정합니다. /vsiaz/ 파일 시스템 헤더가 작성한 URL 뒤에 이 공유 접근 서명을 붙입니다. 공유 접근 서명의 값은 이미 URL 인코딩되어 있어야 하며, '?' 또는 '&' 문자로 시작해서는 안 됩니다. (예: 무결한 공유 접근 서명은 ``st=2019-07-18T03%3A53%3A22Z&se=2035-07-19T03%3A53%3A00Z&sp=rl&sv=2018-03-28&sr=c&sig=2RIXmLbLbiagYnUd49rgx2kOXKyILrJOgafmkODhRAQ%3D`` 처럼 보일 것입니다.) GDAL 3.2버전부터 사용할 수 있습니다.
    e) 현재 머신은 애저 활성 디렉터리(Azure Active Directory) 권한이 할당된 애저 가상 머신입니다. (https://docs.microsoft.com/ko-kr/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm 페이지를 참조하십시오.) GDAL 3.3버전부터 사용할 수 있습니다.

3. GDAL 3.5버전부터, "az" 명령줄 유틸리티의 `환경설정 파일 <https://github.com/MicrosoftDocs/azure-docs-cli/blob/main/docs-ref-conceptual/azure-cli-configuration.md>`_ 을 사용할 수 있습니다. ``[storage]`` 단락의 ``connection_string``, ``account`` + ``key`` 또는 ``account`` + ``sas_token`` 키워드를 이 순서대로 우선해서 사용할 것입니다.

GDAL 3.1버전부터, :cpp:func:`VSIRename` 작업을 지원합니다. (먼저 원본 파일을 새 이름으로 복사한 다음 원본 파일을 삭제합니다.)

GDAL 3.3버전부터, :cpp:func:`VSIGetFileMetadata` 및 :cpp:func:`VSISetFileMetadata` 작업도 지원합니다.

.. versionadded:: 2.3

.. _vsiaz_streaming:

/vsiaz_streaming/ (마이크로소프트 애저 블랍 파일: 스트리밍)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

/vsiaz_streaming/ 은 마이크로소프트 애저 블랍(Microsoft Azure Blob) 컨테이너에서 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsiaz_streaming/container/key` 형식의 파일명을 인식합니다. 이때, ``container`` 가 컨테이너의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 객체의 "key"입니다.

인증 옵션 및 읽기 전용 기능은 :ref:`/vsiaz/ <vsiaz>` 와 동일합니다.

.. versionadded:: 2.3

.. _vsiadls:

/vsiadls/ (마이크로소프트 애저 데이터 레이크 저장소 2세대)
++++++++++++++++++++++++++++++++++++++++++++++++++

/vsiadls/ 는 마이크로소프트 애저 데이터 레이크 저장소 파일 시스템에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:ref:`/vsiaz/ <vsiaz>` 와 유사한 케이퍼빌리트를 가지고 있으며, 그 중에서도 인증에 동일한 환경설정 옵션들을 사용합니다. /vsiadls/ 가 /vsiaz/ 보다 뛰어난 점은 실제 디렉터리 관리 및 유닉스 스타일 ACL 지원입니다. 몇몇 기능은 애저 저장소의 계층(hierarchy) 지원이 활성화되어 있어야 합니다. 이 `문서 <https://docs.microsoft.com/ko-kr/azure/storage/blobs/data-lake-storage-introduction>`_ 를 참조하십시오.

/vsiaz/ 보다 향상된 주요 사항은 다음과 같습니다:

  - 진정한 디렉터리 관리 (/vsiaz/ 가 비어 있는 디렉터리를 가지기 위해 사용하는 빈 파일 :file:`.gdal_marker_for_dir` 가 필요없습니다.)

  - :cpp:func:`VSIRmdirRecursive` 를 한 번 호출해서 디렉터리를 재귀적으로 삭제할 수 있습니다.

  - :cpp:func:`VSIRename` 메소드로 강력한 재명명 기능

  - "STATUS" 및 "ACL" 메타데이터 도메인을 위한 :cpp:func:`VSIGetFileMetadata` 지원

  - "PROPERTIES" 및 "ACL" 메타데이터 도메인을 위한 :cpp:func:`VSISetFileMetadata` 지원

.. versionadded:: 3.3

.. _vsioss:

/vsioss/ (알리바바 클라우드 OSS 파일)
++++++++++++++++++++++++++++++++++

/vsioss/ 는 알리바바 클라우드 오브젝트 저장소 서비스(Alibaba Cloud Object Storage Service; OSS) 버켓에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

/vsioss/ 는 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) :cpp:func:`VSIUnlink` 메소드로 파일을 삭제할 수도 있습니다. :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고 :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.

:file:`/vsioss/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 OSS 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) OSS 객체의 "key"입니다.

:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

:decl_configoption:`OSS_SECRET_ACCESS_KEY` 및 :decl_configoption:`OSS_ACCESS_KEY_ID` 환경설정 옵션을 설정해야만 합니다. 일반적으로 :decl_configoption:`OSS_ENDPOINT` 환경설정 옵션을 버켓에 추가된 영역을 반영하는 알맞은 값으로 설정해야 합니다. 기본값은 ``oss-us-east-1.aliyuncs.com`` 입니다. 버켓이 'oss-us-east-1'이 아닌 다른 영역에 저장돼 있는 경우, 코드 로직이 적절한 종단점(endpoint)으로 리다이렉트할 것입니다.

작성 시, OSS 다중부분 업로드 API를 이용해서 파일을 업로드합니다. 덩어리 크기의 기본값은 50MB로 (50MB 부분들 10,000개를 업로드해서) 500GB까지의 파일을 생성할 수 있습니다. 이보다 큰 파일이 필요한 경우, :decl_configoption:`VSIOSS_CHUNK_SIZE` 환경설정 옵션을 더 큰 (MB 단위) 값으로 증가시키십시오. 프로세스가 죽어서 파일을 제대로 종료하지 못 했다면, 다중부분 업로드가 열려진 채일 것이기 때문에 알리바바가 부분들의 저장소에 대해 과금할 것입니다. 사용자 스스로 다른 수단을 이용해서 다중부분 업로드를 중단시켜야 할 것입니다. 덩어리 크기보다 작은 파일의 경우, 다중부분 업로드 API 대신 단순한 PUT 요청을 사용하십시오.

.. versionadded:: 2.3

.. _vsioss_streaming:

/vsioss_streaming/ (알리바바 클라우드 OSS 파일: 스트리밍)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

/vsioss_streaming/ 은 알리바바 OSS 버켓에서 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsioss_streaming/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 OSS 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) OSS 객체의 "key"입니다.

인증 옵션 및 읽기 전용 기능은 :ref:`/vsioss/ <vsioss>` 와 동일합니다.

.. versionadded:: 2.3

.. _vsiswift:

/vsiswift/ (오픈스택 스위프트 오브젝트 저장소)
+++++++++++++++++++++++++++++++++++++++++++

/vsiswift/ 는 오픈스택 스위프트 오브젝트 저장소(OpenStack Swift Object Storage; 스위프트) 버켓에서 사용할 수 있는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 임의로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

/vsiswift/ 는 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) :cpp:func:`VSIUnlink` 메소드로 파일을 삭제할 수도 있습니다. :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고 :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.

:file:`/vsiswift/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 스위프트 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 스위프트 객체의 "key"입니다.

:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

3개의 인증 메소드를 사용할 수 있으며, 다음 순서대로 시도합니다:

1. :decl_configoption:`SWIFT_STORAGE_URL` 및 :decl_configoption:`SWIFT_AUTH_TOKEN` 환경설정 옵션들을 각각 저장소 URL(예: http://127.0.0.1:12345/v1/AUTH_something) 및 'x-auth-token' 인증 토큰의 값으로 설정합니다.

2. :decl_configoption:`SWIFT_AUTH_V1_URL`, :decl_configoption:`SWIFT_USER` 및 :decl_configoption:`SWIFT_KEY` 환경설정 옵션들을 각각 Auth V1 인증의 종단점(예: http://127.0.0.1:12345/auth/v1.0), 사용자명 및 키/비밀번호로 설정합니다. 이 인증 종단점을 사용해서 1번 인증 메소드에서 언급한 저장소 URL과 인증 토큰을 가져올 것입니다.

3. Keystone v3 인증은 'python-swiftclient'와 동일한 옵션들을 사용합니다. 자세한 내용을 알고 싶다면 https://docs.openstack.org/python-swiftclient/latest/cli/index.html#authentication 페이지를 참조하십시오. GDAL 3.1 이상 버전에서는 다음 옵션을 지원합니다:

   - `OS_IDENTITY_API_VERSION=3`
   - `OS_AUTH_URL`
   - `OS_USERNAME`
   - `OS_PASSWORD`
   - `OS_USER_DOMAIN_NAME`
   - `OS_PROJECT_NAME`
   - `OS_PROJECT_DOMAIN_NAME`
   - `OS_REGION_NAME`

4. Keystone v3을 통한 응용 프로그램 자격인증서 인증의 경우, GDAL 3.3.1 이상 버전에서는 다음 옵션들로 'application-credential' 인증을 지원합니다:

   - `OS_IDENTITY_API_VERSION=3`
   - `OS_AUTH_TYPE=v3applicationcredential`
   - `OS_AUTH_URL`
   - `OS_APPLICATION_CREDENTIAL_ID`
   - `OS_APPLICATION_CREDENTIAL_SECRET`
   - `OS_REGION_NAME`

이 파일 시스템 핸들러는 파일을 순차적으로 작성할 수도 있습니다. (이때 찾기 또는 읽기 작업이 비활성화됩니다.)

오픈스택 스위프트의 몇몇 버전에서는, 기본값인 동적 대용량 객체가 아니라 정적 대용량 객체라고 명확하게 표시하지 않는 이상 대용량 (세그먼트화) 파일에의 접근이 실패합니다. 'python-swiftclient'에 ``--use-slo`` 플래그를 설정해서 파일을 업로드하는 경우 대용량 파일에 접근할 수 있습니다. (모든 옵션을 보고 싶다면 https://docs.openstack.org/python-swiftclient/latest/cli/index.html#swift-upload 페이지를 참조하십시오.) 대용량 객체에 관한 더 자세한 정보는 https://docs.openstack.org/swift/latest/api/large_objects.html 페이지를 참조하십시오.

.. versionadded:: 2.3

.. _vsiswift_streaming:

/vsiswift_streaming/ (오픈스택 스위프트 오브젝트 저장소: 스트리밍)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

/vsiswift_streaming/ 은 스위프트 버켓에서 스트리밍되는 파일을 사전에 전체 파일을 다운로드하지 않고 (비공개 파일 우선으로) 실시간(on-the-fly)으로 순차적으로 읽을 수 있게 해주는 파일 시스템 핸들러입니다. GDAL이 libcurl 라이브러리를 대상으로 빌드되어 있어야 합니다.

:file:`/vsiswift_streaming/bucket/key` 형식의 파일명을 인식합니다. 이때, ``bucket`` 이 스위프트 버켓의 이름이고 ``key`` 가 (예를 들어 하위 디렉터리를 담고 있을 수도 있는 파일명 같은) 스위프트 객체의 "key"입니다.

인증 옵션 및 읽기 전용 기능은 :ref:`/vsiswift/ <vsiswift>` 와 동일합니다.

.. versionadded:: 2.3

.. _vsihdfs:

/vsihdfs/ (하둡 파일 시스템)
++++++++++++++++++++++++++++++

/vsihdfs/ 는 HDFS(Hadoop File System)에 읽기 접근을 지원하는 파일 시스템 핸들러입니다. GDAL이 자바 지원(``--with-java``) 및 HDFS 지원(``--with-hdfs``)과 함께 빌드되어 있어야 합니다. 현재 유닉스 계열 시스템 상에서만 이 핸들러를 사용할 수 있습니다.
주의: :ref:`vsiwebhdfs` 를 이용해서 HTTP REST API(webHdfs)도 지원합니다.

:file:`/vsihdfs/hdfsUri` 형식의 파일명을 인식합니다. 이때, ``hdfsUri`` 가 무결한 HDFS URI입니다. 다음은 그 예시입니다:

::

    /vsihdfs/file:/tmp/my.tif  (HDFS를 통해 접근하는 로컬 파일)
    /vsihdfs/hdfs:/hadoop/my.tif  (HDFS에 저장된 파일)

.. versionadded:: 2.4

.. _vsiwebhdfs:

/vsiwebhdfs/ (웹 하둡 파일 시스템 REST API)
++++++++++++++++++++++++++++++++++++++++++++++

/vsiwebhdfs/ 는 자체 HTTP REST API를 통해 HDFS에 읽기 및 쓰기 접근을 지원하는 파일 시스템 핸들러입니다.

:file:`/vsiwebhdfs/http://hostname:port/webhdfs/v1/path/to/filename` 형식의 파일명을 인식합니다. 다음은 그 예시입니다:

::

    /vsiwebhdfs/http://localhost:50070/webhdfs/v1/mydir/byte.tif

/vsiwebhdfs/ 는 파일을 순차적으로 작성할 수도 있습니다. 이때 찾기 또는 읽기 작업이 비활성화되기 때문에, GDAL 3.2 이상 버전인 경우 :decl_configoption:`CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE` 환경설정 옵션을 YES로 설정하지 않는 이상 특히 GTiff 드라이버로 GeoTIFF 파일을 직접 작성할 수 없습니다. 이 환경설정 옵션을 YES로 설정하면 임의 쓰기 접근을 할 수 있습니다. (이때 :decl_configoption:`CPL_TMPDIR` 환경설정 옵션으로 제어되는 위치에 임시 로컬 파일을 생성합니다.) :cpp:func:`VSIUnlink` 메소드로 파일을 삭제할 수도 있습니다. :cpp:func:`VSIMkdir` 메소드로 디렉터리를 생성하고 :cpp:func:`VSIRmdir` 메소드로 (비어 있는) 디렉터리를 삭제할 수도 있습니다.

:ref:`/vsicurl/ <vsicurl>` 의 일반 메커니즘이 적용됩니다.

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

- :decl_configoption:`WEBHDFS_USERNAME` = value:
  (보안이 꺼져 있을 때) 사용자명입니다.

- :decl_configoption:`WEBHDFS_DELEGATION` = value:
  (보안이 켜져 있을 때) 하둡 대표(delegation) 토큰입니다.

- :decl_configoption:`WEBHDFS_DATANODE_HOST` = value:
  리다이렉트를 이용하는 API의 경우, 리다이렉트 호스트명을 이 옵션이 지정하는 호스트명으로 대체합니다. (일반적으로 프록시가 분해(resolve) 가능한 호스트명을 재작성해야 합니다.)

- :decl_configoption:`WEBHDFS_REPLICATION` = int_value:
  파일 생성 시 사용하는 복제 값입니다.

- :decl_configoption:`WEBHDFS_PERMISSION` = int_value:
  파일 또는 디렉터리 생성 시 (십진수로 지정하는) 권한 마스크입니다.

이 파일 시스템 핸들러는 파일을 순차적으로 작성할 수도 있습니다. (이때 찾기 또는 읽기 작업이 비활성화됩니다.)

.. versionadded:: 2.4

.. _vsistdin:

/vsistdin/ (표준 입력 스트리밍)
-------------------------------------

/vsistdin/ 은 표준 입력 스트림으로부터 읽어올 수 있는 파일 시스템 핸들러입니다.

파일명 문법이 반드시 :file:`/vsistdin/` 뿐이어야 합니다.

사용할 수 있는 파일 작업은 당연히 Read()와 Seek() 포워딩으로 제한되어 있습니다. 파일의 처음 1MB 전체에 Seek() 작업을 할 수 있으며, 동일한 프로세스에서 :file:`/vsistdin/` 을 몇 번이고 종료하고, 다시 열고, 처음 1MB를 읽을 수 있도록 해당 부분을 캐시합니다.

.. _vsistdout:

/vsistdout/ (표준 출력 스트리밍)
---------------------------------------

/vsistdout/ 은 표준 출력 스트림에 작성할 수 있는 파일 시스템 핸들러입니다.

파일명 문법이 반드시 :file:`/vsistdout/` 뿐이어야 합니다.

사용할 수 있는 파일 작업은 당연히 Write()로 제한되어 있습니다.

이 파일 시스템의 변이형인 :file:`/vsistdout_redirect/` 파일 시스템 핸들러가 존재합니다. 이 핸들러는 :cpp:func:`VSIStdoutSetRedirection` 함수로 출력 함수를 정의할 수 있습니다.

.. _vsimem:

/vsimem/ (인메모리 파일)
--------------------------

/vsimem/ 은 메모리 블록을 파일로 취급할 수 있게 해주는 파일 시스템 핸들러입니다. 이 드라이버는 기본 경로 :file:`/vsimem/` 아래 있는 파일 시스템의 모든 부분을 처리할 것입니다.

일반적인 VSI*L 함수를 사용해서 메모리 배열이 마치 실제 파일 시스템 객체인 것처럼 취급해서 메모리 배열을 자유롭게 생성하고 삭제할 수 있습니다. 데이터의 원본 복사본을 복제하지 않고 메모리 파일 시스템 객체를 효율적으로 생성하거나 메모리 파일과 관련된 메모리 블록을 "훔치기" 위한 몇몇 추가 메소드가 존재합니다. :cpp:func:`VSIFileFromMemBuffer` 및 :cpp:func:`VSIGetMemFileBuffer` 함수를 참조하십시오.

함수 관련 디렉터리를 지원합니다.

동일 프로세스 내에서 /vsimem/ 파일은 가시화됩니다. 스레드 여러 개가 서로 다른 핸들을 사용한다는 가정 하에, 읽기 모드에서 스레드 여러 개가 동일한 기저 파일에 접근할 수 있습니다. 그러나 동일한 기저 파일에 대해 쓰기 및 읽기 작업을 동시에 할 수는 없습니다. (잠금(lock)은 호출 코드의 책임으로 남겨져 있습니다.)

.. _vsisubfile:

/vsisubfile/ (파일의 일부분)
--------------------------------

/vsisubfile/ 가상 파일 시스템 핸들러는 (VSIFOpenL() 등등 같은) 가상 파일 시스템 함수에 파일의 하위 영역(subregion)을 자신의 파일로 취급해서 파일의 하위 영역에 접근할 수 있습니다.

다른 파일의 하위 부분(subportion)을 나타내기 위해 특수 형식의 파일명을 사용합니다:

::

    /vsisubfile/<offset>[_<size>],<filename>

<size> 파라미터는 선택적입니다. 이 파라미터를 설정하지 않으면 시작 오프셋으로부터 시작하는 파일의 나머지 부분을 하위 파일의 부분으로 취급합니다. 설정하는 경우 <offset>으로부터 <size> 바이트까지를 하위 파일의 부분으로 취급합니다. <filename>은 일반 규칙을 사용하는 상대 경로 또는 절대 경로일 수도 있습니다. <offset> 및 <size> 값은 바이트 단위입니다. 다음은 그 예시입니다:

::

    /vsisubfile/1000_3000,/data/abc.ntf
    /vsisubfile/5000,../xyz/raw.dat

/vsimem/ 또는 일반적인 파일 시스템 핸들러와는 달리, 새 파일 생성, 디렉터리 탐색, 그리고 /vsisubfile/ 영역 안에 있는 파일 삭제를 위한 파일 시스템 작업을 제대로 지원하지 않습니다. :cpp:func:`VSIFOpenL` 함수가 반환하는 파일 핸들을 기반으로 하는 :cpp:func:`VSIStatL`, :cpp:func:`VSIFOpenL` 작업만 제대로 작동합니다.

.. _vsisparse:

/vsisparse/ (희소 파일)
--------------------------

/vsisparse/ 가상 파일 핸들러는 다른 파일에 있는 데이터 덩어리로부터 가상 파일 내부의 큰 공간이 상수값으로 설정되어 있을 수도 있는 가상 파일을 구성할 수 있습니다. 이렇게 하면 이미지 데이터가 상수값으로 설정된 대용량 파일로 보이는 가상 파일에 어떤 종류의 작업을 테스트할 수 있게 됩니다. 테스트 스위트(test suite)에 너무 대용량이지만 대부분의 데이터를 무시할 수 있는 테스트 파일을 추가하려 하는 경우에도 도움이 됩니다. 이론상 서로 다른 파일 시스템 상에 있는 파일 여러 개를 대용량 가상 파일 하나로 취급하기 위해서 사용할 수도 있습니다.

/vsisparse/ 가 참조하는 파일은 다음과 같은 서식으로 작성된 XML 제어 파일이어야 합니다:

::

    <VSISparseFile>
        <Length>87629264</Length>
        <SubfileRegion>  <!-- 파일의 시작 -->
            <Filename relative="1">251_head.dat</Filename>
            <DestinationOffset>0</DestinationOffset>
            <SourceOffset>0</SourceOffset>
            <RegionLength>2768</RegionLength>
        </SubfileRegion>

        <SubfileRegion>  <!-- RasterDMS 노드 -->
            <Filename relative="1">251_rasterdms.dat</Filename>
            <DestinationOffset>87313104</DestinationOffset>
            <SourceOffset>0</SourceOffset>
            <RegionLength>160</RegionLength>
        </SubfileRegion>

        <SubfileRegion>  <!-- 파일의 끝 -->
            <Filename relative="1">251_tail.dat</Filename>
            <DestinationOffset>87611924</DestinationOffset>
            <SourceOffset>0</SourceOffset>
            <RegionLength>17340</RegionLength>
        </SubfileRegion>

        <ConstantRegion>  <!-- 파일의 나머지 부분의 기본값 -->
            <DestinationOffset>0</DestinationOffset>
            <RegionLength>87629264</RegionLength>
            <Value>0</Value>
        </ConstantRegion>
    </VSISparseFile>

이 예시의 값들과 그 의미를 쉽게 이해할 수 있을 것이라 믿습니다.

.. _target_user_virtual_file_systems_file_caching:

파일 캐시 작업
------------

파일 캐시 작업은 제대로 된 가상 파일 시스템 핸들러는 아니지만, 가상 파일 핸들을 입력 받아 입력 파일 핸들에 대한 읽기 작업을 캐시하는 새 핸들을 반환합니다. 캐시는 RAM 기반으로 파일 핸들이 종료될 때 캐시의 내용을 폐기합니다. 이 캐시는 각각 32KB 용량의 블록의 최소 최근 사용(Least Recently Used) 목록입니다.

현재 :cpp:class:`VSICachedFile` 클래스만 읽기 작업을 처리합니다. 쓰기 작업 시 오류를 발생시킬 것입니다.

:cpp:func:`VSICreateCachedFile` 함수로 읽기 작업을 수행하는데, :decl_configoption:`VSI_CACHE` 환경설정 옵션이 YES로 설정된 경우 (표준 파일 시스템 작업과 /vsicurl/ 및 기타 관련 네트워크 파일 시스템 작업을 위한 기본 파일 시스템 같은) 앞에서 설명한 파일 시스템들 여러 개가 이 함수를 암묵적으로 사용합니다.

각 파일에 대한 캐시 작업의 기본 크기는 (캐시되는 각 파일 당) 25MB지만, :decl_configoption:`VSI_CACHE_SIZE` 환경설정 옵션의 값을 바이트 단위로 설정해서 수정할 수 있습니다.

.. _vsicrypt:

/vsicrypt/ (암호화 파일)
----------------------------

/vsicrypt/ 는 특수 파일 핸들러로 임의 접근 케이퍼빌리티로 암호화 파일을 실시간(on-the-fly)으로 읽고, 생성하고, 업데이트할 수 있습니다.

자세한 내용은 :cpp:func:`VSIInstallCryptFileHandler` 함수를 참조하십시오.

