.. _raster.fits:

================================================================================
FITS -- 유연한 이미지 전송 시스템(Flexible Image Transport System)
================================================================================

.. shortname:: FITS

.. build_dependencies:: libcfitsio

FITS는 주로 우주비행사들이 사용하는 포맷이지만, 임의의 이미지 유형들 및 다중 스펙트럼 이미지를 지원하는 상대적으로 단순한 포맷이기 때문에 GDAL이 지원합니다. 표준 `CFITSIO 라이브러리 <http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html>`_ 로 FITS 지원을 구현했기 때문에, 사용자 시스템에서 FITS 지원을 활성화하려면 사용자 시스템에 이 라이브러리가 설치되어 있어야만 합니다. (:ref:`CFITSIO 링크 작업에 대한 메모 <notes-on-cfitsio-linking>` 를 참조하십시오.) FITS 파일 읽기 및 쓰기 둘 다 지원합니다.

표준 3.0버전부터, WCS(World Coordinate System) 키워드 변환을 통해 지리참조 좌표계를 구현했습니다. 원격 탐사 처리 과정에서 흔히 쓰이는 위도-경도 좌표계들만 (`FITS 표준 문서 <https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf#subsection.8.3>`_ 참조) 구현되었습니다. FITS/WCS 표준에 3차원 원점(datum)이 누락되었기 때문에, `여기 <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018EA000388>`_ 에서 제안하는 행성 확장 프로그램을 이용해서 반경 및 대상 천체를 변환합니다.

파일을 열 때 GDAL 메소드를 통한 접근을 위해 데이터셋의 메타데이터에 FITS 파일에 존재하는 비표준 헤더 키워드를 복사할 것입니다. 마찬가지로, GDAL 처리를 종료할 때 FITS 파일에 사용자가 데이터셋의 메타데이터에 정의한 비표준 헤더 키워드를 작성할 것입니다.

CFITSIO 라이브러리에 친숙한 사용자에게: GDAL 3.0 미만 버전에서는 FITS 파일에 BSCALE 및 BZERO 헤더 키워드가 존재하는 경우 촉발되는 데이터 값의 자동 크기 조정이 비활성화됩니다. 다른 모든 헤더 키워드와 마찬가지로 이 헤더 키워드들도 데이터셋 메타데이터를 통해 접근 및 업데이트할 수 있지만, 이 키워드들이 파일로부터 데이터 값 읽기 또는 파일에 데이터 값을 쓰기에 영향을 미치지는 않습니다. GDAL 3.0버전부터, BZERO 및 BSCALE 키워드를 더 이상 메타데이터로 참조하지 않고서도 표준 :cpp:func:`GDALRasterBand::GetOffset` / :cpp:func:`GDALRasterBand::SetOffset` 및 :cpp:func:`GDALRasterBand::GetScale` / :cpp:func:`GDALRasterBand::SetScale` GDAL 함수를 통해 관리할 수 있습니다.

다중 이미지 지원
----------------------

GDAL 3.2버전부터, 제1 HDU 뒤에 하나 이상의 확장자를 담고 있는 MEF(Multi-Extension FITS) 파일을 지원합니다. 2개 이상의 이미지 HDU가 검색된 경우, 이 이미지들을 하위 데이터셋으로 리포트합니다.

입력 데이터셋/HDU를 위한 연결 문자열은 ``FITS:"filename.fits":hdu_number`` 입니다.

바이너리 테이블 지원
--------------------

GDAL 3.2버전부터, 바이너리 테이블을 벡터 레이어로 노출시킬 것입니다. (업데이트 및 생성은 GDAL 3.2.1부터 지원합니다.)

FITS 데이터 유형은 OGR 데이터 유형에 다음과 같이 매핑됩니다:

.. list-table:: Data types
   :header-rows: 0

   * - TFORM 값
     - TSCAL, TOFFSET 값
     - 발생 횟수
     - OGR 필드 유형
     - OGR 필드 하위 유형
   * - 'L' (진릿값)
     - 무시됨
     - 1
     - OFTInteger
     - OFSTBoolean
   * - 'L' (진릿값)
     - 무시됨
     - 1 초과
     - OFTIntegerList
     - OFSTBoolean
   * - 'X' (비트)
     - 무시됨
     - each bit mapped to a OGR field
     - OFTInteger
     - OFSTNone
   * - 'B' (부호 없는 바이트)
     - 1, 0 (부호 없는 바이트) or 1, -128 (부호 있는 바이트)
     - 1
     - OFTInteger
     - OFSTNone
   * - 'B' (부호 없는 바이트)
     - 1, 0 (부호 없는 바이트) or 1, -128 (부호 있는 바이트)
     - 1 초과
     - OFTIntegerList
     - OFSTNone
   * - 'I' (16비트 부호 있는 정수)
     - 1, 0
     - 1
     - OFTInteger
     - OFSTInt16
   * - 'I' (16비트 정수, 부호 없는 것으로 해석)
     - 1, 32768
     - 1
     - OFTInteger
     - OFSTNone
   * - 'I' (16비트 부호 있는 정수)
     - other than (1,0) and (1,32768)
     - 1
     - OFTReal
     - OFSTNone
   * - 'I' (16비트 정수)
     - 1, 0
     - 1 초과
     - OFTIntegerList
     - OFSTInt16
   * - 'I' (16비트 정수, 부호 없는 것으로 해석)
     - 1, 32768
     - 1 초과
     - OFTIntegerList
     - OFSTNone
   * - 'I' (16비트 부호 있는 정수)
     - other than (1, 0) and (1, 32768)
     - 1 초과
     - OFTRealList
     - OFSTNone
   * - 'J' (32비트 부호 있는 정수)
     - 1, 0
     - 1
     - OFTInteger
     - OFSTNone
   * - 'J' (32비트 정수, 부호 없는 것으로 해석)
     - 1, 2147483648
     - 1
     - OFTInteger
     - OFSTNone
   * - 'J' (32비트 부호 있는 정수)
     - other than (1, 0) and (1, 2147483648)
     - 1
     - OFTReal
     - OFSTNone
   * - 'J' (32비트 정수)
     - 1, 0
     - 1 초과
     - OFTIntegerList
     - OFSTNone
   * - 'J' (32비트 정수, 부호 없는 것으로 해석)
     - 1, 2147483648
     - 1 초과
     - OFTIntegerList
     - OFSTNone
   * - 'J' (32비트 부호 있는 정수)
     - other than (1, 0) and (1, 2147483648)
     - 1 초과
     - OFTRealList
     - OFSTNone
   * - 'K' (64비트 부호 있는 정수)
     - 1, 0
     - 1
     - OFTInteger64
     - OFSTNone
   * - 'K' (64비트 부호 있는 정수)
     - other than (1, 0)
     - 1
     - OFTReal
     - OFSTNone
   * - 'K' (64비트 부호 있는 정수)
     - 1, 0
     - 1 초과
     - OFTInteger64
     - OFSTNone
   * - 'K' (64비트 부호 있는 정수)
     - other than (1, 0)
     - 1 초과
     - OFTRealList
     - OFSTNone
   * - 'A' (문자)
     - 무시됨
     - if TFORM='Axxx' and no TDIM header
     - OFTString
     - OFSTNone
   * - 'A' (문자)
     - 무시됨
     - TDIM for 2D field, or variable length ('PA')
     - OFTStringList
     - OFSTNone
   * - 'E' (단정밀도 부동소수점)
     - 1, 0
     - 1
     - OFTReal
     - OFSTFloat32
   * - 'E' (단정밀도 부동소수점)
     - other than (1, 0)
     - 1
     - OFTReal
     - OFSTNone
   * - 'E' (단정밀도 부동소수점)
     - 1, 0
     - 1 초과
     - OFTRealList
     - OFSTFloat32
   * - 'E' (단정밀도 부동소수점)
     - other than (1, 0)
     - 1 초과
     - OFTRealList
     - OFSTNone
   * - 'D' (배정밀도 부동소수점)
     - any
     - 1
     - OFTReal
     - OFSTNone
   * - 'D' (배정밀도 부동소수점)
     - any
     - 1 초과
     - OFTRealList
     - OFSTNone
   * - 'C' (단정밀도 복소수)
     - any
     - 1
     - OFTString whose value is of the form "x + yj"
     - OFSTNone
   * - 'C' (단정밀도 복소수)
     - any
     - 1 초과
     - OFTStringList whose values are of the form "x + yj"
     - OFSTNone
   * - 'M' (배정밀도 복소수)
     - any
     - 1
     - OFTString whose value is of the form "x + yj"
     - OFSTNone
   * - 'M' (배정밀도 복소수)
     - any
     - 1 초과
     - OFTStringList whose values are of the form "x + yj"
     - OFSTNone

Fields with a repeat count 1 초과 expressing fixed size arrays, or fields using
array descriptors 'P' and 'Q' for variable length arrays are mapped to OGR OFTxxxxxList
data types. The potential 2D structure of such field has no direct equivalence in
OGR, so OGR will expose a linear structure. For fixed size arrays, the user can retrieve
the value of the TDIMxx header in the layer metadata to recover the dimensionality
of the field.

Fields that have TSCAL and/or TZERO headers are automatically scaled and offset
to the physical value (only applies to numeric data types)

TNULL headers are used for integer numeric data types and for a single-occurence
field to set a OGR field to NULL.

레이어 생성 옵션
----------------------

The following layer creation options are available:

- **REPEAT_{fieldname}=number**. For a given field (substitute {fieldname} by its
  name) of type IntegerList, Integer64List
  or RealList, specify a fixed number of elements. Otherwise those fields will be
  created as variable-length FITS columns, which can have performance impact on
  creation.

- **COMPUTE_REPEAT=AT_FIELD_CREATION/AT_FIRST_FEATURE_CREATION**. For fields of
  type IntegerList, Integer64List or RealList, specifies when they are mapped to
  a FITS column type. The default is AT_FIELD_CREATION, and implies that they
  will be created as variable-length FITS columns, unless a REPEAT_{fieldname}
  option is specified. When AT_FIRST_FEATURE_CREATION is specified, the number of
  elements in the first feature will be taken into account to create fixed-size
  FITS columns.

When using ogr2ogr or :cpp:func:`GDALVectorTranslate` with a FITS source, the
FITS header will be taken into account, in particular to help to determine the
FITS data type of target columns.

예시
--------

* Listing subdatasets in a MEF .fits:

    ::

        $ gdalinfo ../autotest/gdrivers/data/fits/image_in_first_and_second_hdu.fits

        Driver: FITS/Flexible Image Transport System
        Files: ../autotest/gdrivers/data/fits/image_in_first_and_second_hdu.fits
        Size is 512, 512
        Metadata:
        EXTNAME=FIRST_IMAGE
        Subdatasets:
        SUBDATASET_1_NAME=FITS:"../autotest/gdrivers/data/fits/image_in_first_and_second_hdu.fits":1
        SUBDATASET_1_DESC=HDU 1 (1x2, 1 band), FIRST_IMAGE
        SUBDATASET_2_NAME=FITS:"../autotest/gdrivers/data/fits/image_in_first_and_second_hdu.fits":2
        SUBDATASET_2_DESC=HDU 2 (1x3, 1 band)
        Corner Coordinates:
        Upper Left  (    0.0,    0.0)
        Lower Left  (    0.0,  512.0)
        Upper Right (  512.0,    0.0)
        Lower Right (  512.0,  512.0)
        Center      (  256.0,  256.0)

* Opening a given raster HDU:

    ::

        $ gdalinfo FITS:"../autotest/gdrivers/data/fits/image_in_first_and_second_hdu.fits":1

        Driver: FITS/Flexible Image Transport System
        Files: none associated
        Size is 1, 2
        Metadata:
        EXTNAME=FIRST_IMAGE
        Corner Coordinates:
        Upper Left  (    0.0,    0.0)
        Lower Left  (    0.0,    2.0)
        Upper Right (    1.0,    0.0)
        Lower Right (    1.0,    2.0)
        Center      (    0.5,    1.0)
        Band 1 Block=1x1 Type=Byte, ColorInterp=Undefined

* Listing potential binary tables in a FITS file:

    ::

        $ ogrinfo my.fits


* Converting a GeoPackage layer into a FITS binary table:


    ::

        $ ogr2ogr out.fits my.gpkg my_table


기타
-----

주의: ``gdal/frmts/fits/fitsdataset.cpp`` 로 구현되었습니다.

.. _notes-on-cfitsio-linking:

GDAL에서의 CFITSIO 링크 작업에 대한 메모
--------------------------------------
리눅스
^^^^^
소스로부터
"""""""""""
Install CFITSIO headers from your distro (eg, cfitsio-devel on Fedora; libcfitsio-dev on Debian-Ubuntu), then compile GDAL as usual. CFITSIO will be automatically detected and linked.

배포판으로부터
"""""""""""""
On Fedora/CentOS install CFITSIO then GDAL with dnf (yum): cfitsio is automatically linked.

맥OS
^^^^^^
The last versions of the MacOSX packages are not linked against CFITSIO.
Install CFITSIO as described in the `official documentation <https://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio_macosx.html>`__.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
