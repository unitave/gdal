.. _rfc-58:

=======================================================================================
RFC 58: 데이터셋 NODATA 값 제거
=======================================================================================

저자: 션 길리스(Sean Gillies)

연락처: sean@mapbox.com

상태: 승인, GDAL 2.1버전에 구현

요약
----

이 RFC는 C++ :cpp:class:`GDALRasterBand` API에 ``DeleteNoDataValue()`` 함수를 추가할 것을 제안합니다. 이 함수는 래스터 밴드의 NODATA 값을 제거합니다. 이 함수가 성공할 경우 래스터 밴드에 NODATA 값이 존재하지 않을 것입니다. 실패한다면 NODATA 값이 그대로 유지될 것입니다.

근거
----

NODATA 값은 ``GetNoDataValue()`` 및 ``SetNoDataValue()`` 접근자(accessor)를 가지고 있습니다. GeoTIFF의 경우 TIFFTAG_GDAL_NODATA TIFF 태그에 NODATA 값을 저장합니다. 새로 생성된 GeoTIFF 파일은 (태그가 없기 때문에) NODATA 값을 가질 수 없지만, NODATA 값을 설정하고 저장하고 나면 새로운 값만 지정할 수 있을 뿐 제거할 수 없습니다. 또한 데이터 유형의 범위를 벗어나는 값으로 설정할 수도 없습니다. 8비트 데이터의 경우 ``GDALSetNoDataValue()`` 에 ``nan``, ``-inf``, 또는 ``256`` 을 전송하는 것은 0을 전송하는 것과 마찬가지입니다.

제거할 수 없는 NODATA 값의 문제는 다음과 같습니다:

-  NODATA 마스크가 NODATA 값을 완전히 가릴 수 있지만 (GDAL RFC 15 참조) .msk 파일이 사라질 경우 (사이드카 파일의 고질적인 문제입니다) 숨겼던 NODATA 값이 다시 노출됩니다.

-  GDAL의 모든 부분에서 NODATA 마스크를 사용할 수 있는 것은 아닙니다. GDAL의 어떤 부분에서는 NODATA 값이란 그저 무결한 데이터의 정의일 뿐이기 때문입니다.

NODATA 값을 제거하기 위해 현재 권장되는 방법은 gdal_translate를 사용해서 GeoTIFF를 복사할 때 NODATA 태그를 데이터와 함께 복사하지 않도록 지정하는 것입니다. NODATA 값을 완벽하게 편집 가능하고 제거 가능하도록 만들면 불필요하게 복사하지 않을 수 있습니다.

변경 사항
---------

:file:`gdal_priv.h` (C++ API)에 있는 :cpp:class:`GDALRasterBand` 에 ``virtual CPLErr DeleteNoDataValue()`` 메소드를 추가하고, :file:`gdal.h` (C API)에 ``CPLErr GDALDeleteRasterNoDataValue()`` 를 추가할 것입니다.

업데이트된 드라이버
~~~~~~~~~~~~~~~~~~~

다음 드라이버들을 업데이트할 것입니다:

   -  GTiff
   -  MEM
   -  VRT
   -  KEA

GTiff 드라이버의 경우, GDAL이 libtiff 4.x버전을 대상으로 빌드되었다면 TIFFTAG_GDAL_NODATA TIFF 태그를 설정하지 않습니다. 이는 적절한 습성입니다.
TIFFUnsetField()가 존재하지 않는 libtiff 3.x버전의 경우, 태그를 비어 있는 문자열로 설정합니다 -- GDAL 2.0버전은 이를 NODATA가 없는 것으로 탐지하고, 그 이전 버전들은 0으로 파싱할 것입니다.

(내장된 NODATA 메커니즘이 없기 때문에 .aux.xml 사이드카 파일에 의존하는 드라이버의 경우) :cpp:class:`GDALPamRasterBand` 클래스도 업데이트할 것입니다. .aux.xml 파일로부터 태그만 제거하기 때문에 드라이버가 내부적으로 NODATA를 저장할 수 있지만 읽기 전용 모드로 NODATA를 여는 (따라서 기본값이 PAM(Pluggable Authentication Modules)이 되는) 상황에서는 DeleteNoData()가 아무 영향도 미치지 못 할 것입니다.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

RasterBand 객체에 DeleteNoDataValue() 메소드를 추가합니다.

유틸리티
--------

:file:`gdal_edit.py` 스크립트를 "-unsetnodata" 옵션으로 개선합니다.

문서화
------

새 메소드 및 함수를 모두 문서화합니다.

테스트 스위트
-------------

업데이트된 드라이버들의 테스트가 새 메소드의 영향을 테스트합니다.

호환성 문제점
-------------

C API의 경우 호환성에 문제가 없습니다.
C++ API의 경우 새 가상 메소드 도입 때문에 ABI를 변경합니다.

관련 티켓
---------

`#2020 티켓 <https://trac.osgeo.org/gdal/ticket/2020>`_

구현
----

이벤 루올이 `Mapbox <https://www.mapbox.com/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc58_removing_nodata_value" 브랜치 <https://github.com/rouault/gdal/tree/rfc58_removing_nodata_value>`_ 에 있습니다.

투표 이력
---------

-  이벤 루올 +1
-  하워드 버틀러 +1
-  대니얼 모리셋 +1
-  유카 라흐코넨 +1

