.. _raster.intergraphraster:

================================================================================
INGR -- 인터그래프 래스터 포맷
================================================================================

.. shortname:: INGR

.. built_in_by_default::

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_INGR

이 포맷의 읽기 및 쓰기 접근을 지원합니다.

인터그래프(Intergraph) 래스터 파일 포맷은 인터그래프 소프트웨어 응용 프로그램이 래스터 데이터를 저장하기 위해 사용하는 기본(native) 파일 포맷이었습니다. 이 포맷은 여러 개의 내부 데이터 포맷으로 나타납니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

INGR 파일 읽기
------------------

다음은 INGR 드라이버가 읽기를 지원하는 데이터 포맷입니다:

-  2 - 바이트 정수형(Byte Integer)
-  3 - 워드 정수형(Word Integer)
-  4 - 32비트 정수형(Integers 32bit)
-  5 - 32비트 부동소수점형(Floating Point 32bit)
-  6 - 64비트 부동소수점형(Floating Point 64bit)
-  9 - 런 렝스 부호화(Run Length Encoded)
-  10 - 런 렝스 부호화 색상
-  24 - CCITT Group 4
-  27 - 적응형 RGB(Adaptive RGB)
-  28 - 비압축 24비트(Uncompressed 24bit)
-  29 - 적응형 회색조(Adaptive Gray Scale)
-  30 - JPEG 회색조(JPEG GRAY)
-  31 - JPEG RGB
-  32 - JPEG CMYK
-  65 - 타일화(Tiled)
-  67 - 연속 색조(Continuous Tone)

"65 - 타일화(Tiled)" 포맷은 포맷이 아닙니다. 그저 파일이 타일화되었다는 사실을 알려줄 뿐입니다. 이 경우 타일 헤더가 이 목록의 어떤 포맷도 될 수 있는 실제 데이터 포맷 코드를 담고 있습니다. INGR 드라이버는 타일화되었든 되지 않았든 지원하는 모든 데이터 포맷의 인스턴스를 읽어올 수 있습니다.

INGR 파일 쓰기
------------------

다음은 INGR 드라이버가 쓰기를 지원하는 데이터 포맷입니다:

-  2 - 바이트 정수형(Byte Integer)
-  3 - 워드 정수형(Word Integer)
-  4 - 32비트 정수형(Integers 32bit)
-  5 - 32비트 부동소수점형(Floating Point 32bit)
-  6 - 64비트 부동소수점형(Floating Point 64bit)

".rle" 파일을 산출할 때, 9번 유형 RLE 흑백(bitonal) 압축을 사용합니다. 다른 파일 유형은 비압축입니다.

하지만 9번 유형 포맷으로 작성하는 일은 권장되지 않는다는 사실을 기억하십시오.

파일 확장자
--------------

다음은 INGR 파일 확장자 목록의 일부입니다:

.. list-table:: INGR File Extensions
   :header-rows: 0

   * - .cot
     - 8비트 회색조 또는 색상표 데이터
   * - .ctc
     - PackBits 유형 압축을 사용하는 8비트 회색조 (희귀)
   * - .rgb
     - 24비트 색상(비압축) 및 회색조(PackBits 유형 압축)
   * - .ctb
     - 8비트 색상표 데이터(비압축 또는 RLE)
   * - .grd
     - 8비트, 16비트 및 32비트 표고 데이터
   * - .crl
     - 런 렝스 압축된 8비트 또는 16비트 회색조 또는 색상표 데이터
   * - .tpe
     - 런 렝스 압축된 8비트 또는 16비트 회색조 또는 색상표 데이터
   * - .lsr
     - 런 렝스 압축된 8비트 또는 16비트 회색조 또는 색상표 데이터
   * - .rle
     - 런 렝스 압축된 1비트 데이터 (런: 16비트)
   * - .cit
     - CCITT G3 또는 G4 1비트 데이터
   * - .g3
     - CCITT G3 1비트 데이터
   * - .g4
     - CCITT G4 1비트 데이터
   * - .tg4
     - CCITT G4 1비트 데이터 (타일화)
   * - .cmp
     - JPEG 회색조, RGB, 또는 CMYK
   * - .jpg
     - JPEG 회색조, RGB, 또는 CMYK

소스: \ http://www.oreilly.com/www/centers/gff/formats/ingr/index.htm

INGR 드라이버는 INGR 파일을 식별하거나 생성하는 데 어떤 특별한 확장자도 필요로 하지 않습니다.

지리참조
------------

INGR 드라이버는 지리참조 정보 읽기 또는 쓰기를 지원하지 않습니다. 그 이유는 INGR 파일에 지리참조 정보를 저장하는 보편적인 방법이 없기 때문입니다. 관련 .dgn 파일에 또는 파일 자체에 내장된 응용 프로그램 특화 데이터 저장소에 지리참조 정보를 저장할 수는 있습니다.

메타데이터
---------

다음 생성 옵션을 설정하면 밴드 집합(bandset) 메타데이터를 사용할 수 있습니다.

-  **RESOLUTION**:
   DPI(인치 당 픽셀) 해상도입니다. 미크론(micron) 해상도는 지원하지 않습니다.

참고
--------

더 많은 정보를 원한다면:

-  ``gdal/frmts/ingr/intergraphraster.cpp`` 로 구현되었습니다.
-  `www.intergraph.com <http://www.intergraph.com>`_
-  http://www.oreilly.com/www/centers/gff/formats/ingr/index.htm
-  파일 사양: ftp://ftp.intergraph.com/pub/bbs/scan/note/rffrgps.zip/
