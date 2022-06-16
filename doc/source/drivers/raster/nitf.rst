.. _raster.nitf:

================================================================================
NITF -- 국립 영상 전송 포맷
================================================================================

.. shortname:: NITF

.. built_in_by_default::

.. toctree::
   :maxdepth: 1
   :hidden:

   nitf_advanced

GDAL은 NITF(National Imagery Transmission Format) 이미지 파일의 몇몇 하위 유형 읽기를 지원하며, 단순한 NITF 2.1 파일 쓰기도 지원합니다. 비압축, ARIDPCM 및 JPEG 압축, (카카두, ECW SDK 또는 다른 JPEG2000 호환 드라이버로 생성된) JPEG2000 또는 VQ 압축 NITF 1.1, NITF 2.0, NITF 2.1 및 NSIF 1.0 이미지를 읽을 수 있을 것입니다.

RPF 상품의 CIB 및 CADRG 프레임, ECRG 프레임, HRE 상품을 포함한 다양한 상품에 대해 읽기 지원을 테스트했습니다.

의사색상 용 색상표를 가진 이미지를 읽을 수 있습니다. 몇몇 경우 NODATA 값을 식별할 수도 있습니다.

이미지 헤더에 IGEOLO 정보가 있는 경우 위도/경도 범위를 읽어옵니다. RPF 보조 데이터에 고정밀도 위도/경도 지리참조 정보가 있다면 저정밀도 IGEOLO 정보 정보 대신 사용할 것입니다. BLOCKA 인스턴스가 있는 경우, 블록 데이터가 이미지 전체를 커버하면 -- 블록의 행 개수를 가진 L_LINES 필드의 값이 이미지의 행 개수와 동일하다면 -- BLOCKA의 고정밀도 좌표를 사용합니다. 또한 모든 BLOCKA 인스턴스를 메타데이터로 반환합니다. GeoSDE TRE를 사용할 수 있다면, 더 정밀한 좌표를 제공하기 위해 사용할 것입니다. RPC00B (또는 RPC00A) TRE를 사용할 수 있다면, RPC 메타데이터를 리포트하기 위해 사용합니다.
GDAL 2.2버전부터, \_rpc.txt 파일로부터 RPC 정보를 가져올 수 있으며, 내부 RPC00B 값보다 RPC 정보를 우선해서 사용할 것입니다. 외부 \_rpc.txt 파일에 저장된 좌표가 내부 RPC00B 값보다 더 정밀하기 때문입니다.

파일 헤더와 이미지 헤더 필드 대부분은 데이터셋 수준 메타데이터로 반환됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

내보내기 작업 시 NITF 파일을 언제나 다른 보조 레이어 없이 이미지 1개만 가진 NITF 2.1로 작성합니다. 기본적으로 이미지는 비압축이지만, JPEG 및 JPEG2000 압축을 사용할 수 있습니다. 지리참조 정보는 지리 좌표계 또는 UTM WGS84 투영법을 사용하는 이미지에만 작성할 수 있습니다. 좌표계가 다른 지리 좌표계이더라도 암암리에 WGS84 좌표로 취급합니다. 8비트 이미지의 경우 의사색상표를 작성할 수도 있습니다.

내보내기 지향 CreateCopy() API에 더해, Create()를 이용해서 비어 있는 NITF 파일을 생성한 다음 원하는 영상을 작성할 수도 있습니다. 하지만, 알맞은 IREP 및 ICORDS 생성 옵션을 정의하지 않는다면 이 방법으로는 의사색상표와 지리참조 정보를 작성할 수 없습니다.

생성 옵션
~~~~~~~~

알맞은 **생성 옵션** 으로 파일 헤더, 영상 헤더 메타데이터 및 보안 필드 대부분을 설정할 수 있습니다. (이런 필드들이 메타데이터로 리포트되긴 하지만, 절대 메타데이터로 설정해서는 안 됩니다.) 예를 들어 생성 옵션 목록에 ``"FTITLE=카르스크 남서쪽에 있는 미사일 발사대 폐허의 이미지"`` 라고 설정하면, NITF 파일 헤더에 있는 FTITLE 필드를 설정하게 될 것입니다. NITF 사양 문서에 있는 공식 필드명을 사용하십시오. 메타데이터 목록 요청 시 리포트되는 접두어 "NITF\_"를 붙여서는 안 됩니다.

-  **IC=NC/C3/M3/C8**:
   압축 방식을 설정합니다.

   -  NC가 기본값이며, 비압축이라는 뜻입니다.
   -  C3는 JPEG 압축이라는 뜻이며, CreateCopy() 메소드를 사용하는 경우에만 설정할 수 있습니다. 이때 JPEG 특화 생성 옵션인 QUALITY와 PROGRESSIVE도 사용할 수 있습니다. :ref:`raster.jpeg` 드라이버를 참조하십시오. 다중 블록 이미지를 작성할 수 있습니다.
   -  M3는 C3의 변이형입니다. 단 한 가지 차이점은 어떤 블록으로든 빠른 검색을 할 수 있게 해주는 블록 맵을 작성한다는 것입니다.
   -  C8는 (블록 1개의) JPEG2000 압축이라는 뜻이며, CreateCopy() 그리고/또는 Create() 메소드를 사용하는 경우 설정할 수 있습니다. 자세한 내용은 다음 단락을 읽어보십시오.

-  **NUMI=n**:
   이미지 개수를 설정합니다. 기본값은 1입니다.
   :ref:`고급 GDAL NITF 드라이버 정보 <raster.nitf_advanced>` 에서 NITF 파일에 이미지 여러 개를 작성하려면 준수해야 하는 과정을 설명하고 있습니다.

-  **WRITE_ALL_IMAGES=YES/NO**: (GDAL 3.4 이상 버전)
   (이 옵션은 NUMI 옵션을 1보다 큰 숫자로 설정하고 새 NITF 파일을 작성하는 경우에만 연산에 넣습니다.)
   기본값 NO로 설정하면, 드라이버가 첫 번째 이미지 부분만 작성하고 파일 헤더에 추가 이미지 NUMI-1개를 위한 공간을 남겨둡니다.
   YES로 설정하는 경우 모든 이미지를 위한 공간을 할당하는데, 이 공간은 IC=NC인 경우에만 (비압축 이미지인 경우에만) 호환됩니다. (GDAL 3.4 이전 버전의 습성은 YES로 설정한 경우와 비슷합니다.)

-  **ICORDS=G/D/N/S**:

   -  "G": 나중에 SetGeoTransform()을 통해 설정할 (도분초 단위) 모서리 지리 좌표를 위한 공간을 남겨둘 것입니다.
   -  "D": 십진수도(decimal degree) 단위 지리 좌표를 위한 공간을 남겨둘 것입니다.
   -  "N": 북반구 UTM WGS84 투영법을 위한 공간을 남겨둘 것입니다.
   -  "S": 남반구 UTM WGS84 투영법을 위한 공간을 남겨둘 것입니다.
   
   (이 옵션은 Create() 메소드 사용 시에만 필요합니다. CreateCopy() 사용 시 필요없습니다.)

   Create() 메소드로 새 NITF 파일을 생성할 때 ICORDS 생성 옵션을 "N" 또는 "S"로 설정한 경우, 나중에 SetGeoTransform() 메소드를 일관적인 UTM 공간 좌표계로 호출해서 UTM 구역 번호를 설정해야 합니다. (그렇지 않으면 기본값인 구역 0으로 설정될 것입니다.)

   GDAL 3.5.1버전부터, 소스 공간 좌표계가 UTM WGS84 투영법인 이미지에 ICORDS를 G 또는 D로 지정해서 CreateCopy() 인터페이스를 사용하는 경우 NITF 드라이버가 이미지 모서리 좌표를 경도-위도로 재투영할 것입니다. IGEOLO 필드에서 UTM 북반구 투영법으로 표현된 편북 가운데 하나가 -1e6 미만인 적도 지역에 있는 이미지 좌표를 인코딩할 수 없는 경우 유용할 수 있습니다.

-  **IGEOLO=string**: (GDAL 3.5.1 이상 버전)
   문자 60개 길이의 문자열로 지정된 이미지 모서리 좌표입니다. (예상 포맷은 `MIL-STD-2500C <https://nsgreg.nga.mil/doc/view?i=2063>`_ 참조) CreateCopy() 인터페이스를 사용하는 경우 일반적으로 소스 지리변환 및 공간 좌표계로부터 자동 설정됩니다. 이 옵션을 지정하는 경우 반드시 ICORDS 옵션도 지정해야만 합니다.

-  **FHDR**:
   파일 버전을 선택할 수 있지만, 현재 지원하는 변이형은 "NITF02.10"(기본값) 그리고 "NSIF01.00" 2개뿐입니다.

-  **IREP**:
   각 산출 밴드 용 색상표를 위한 공간을 남겨두려면 "RGB/LUT"으로 설정하십시오.
   (이 옵션은 Create() 메소드 사용 시에만 필요합니다. CreateCopy() 사용 시 필요없습니다.)

-  **IREPBAND**:
   IREPBAND들을 밴드 순서대로 쉼표로 구분한 목록입니다.

-  **ISUBCAT**:
   ISUBCAT들을 밴드 순서대로 쉼표로 구분한 목록입니다.

-  **LUT_SIZE**:
   RGB/LUT 밴드 용 의사색상표의 크기를 제어합니다. 이 옵션을 설정하지 않는 경우 256값을 사용합니다.
   (이 옵션은 Create() 메소드 사용 시에만 필요합니다. CreateCopy() 사용 시 필요없습니다.)

-  **BLOCKXSIZE=n**:
   블록 너비를 설정합니다.

-  **BLOCKYSIZE=n**:
   블록 높이를 설정합니다.

-  **BLOCKA_*=**:
   NITF 파일을 BLOCKA TRE로 읽어올 때 리포트된 NITF_BLOCKA 메타데이터와 정확히 동일한 구조로 되어 있는 완전한 BLOCKA 옵션 집합을 설정하는 경우, 파일을 BLOCKA TRE로 생성할 것입니다.

-  **TRE=tre-name=tre-contents**:
   이미지 헤더에 임의의 사용자가 정의한 TRE를 작성하려면 TRE 생성 옵션을 하나 이상 사용해야 할 수도 있습니다.
   tre-name은 최대 문자 6개여야 하고, tre-contents가 역슬래시 또는 0으로 채워진 바이트를 담고 있는 경우 tre-contents는 "역슬래시 이스케이프(backslash escaped)" 상태여야 합니다.
   인자들은 읽기 작업 시 TRE 메타데이터 도메인에 반환되는 것과 동일한 서식을 사용합니다.

-  **FILE_TRE=tre-name=tre-contents**:
   TRE 생성 옵션과 비슷하지만, 이미지 헤더 대신 파일 헤더에 TRE를 작성한다는 점이 다릅니다.

-  **DES=des-name=des-contents**:
   NITF 파일에 임의의 사용자가 정의한 DES를 작성하려면 DES 생성 옵션을 하나 이상 사용해야 할 수도 있습니다.
   des-name은 최대 문자 25개여야 하고, des-contents가 역슬래시 또는 0으로 채워진 바이트를 담고 있는 경우 des-contents는 CPLEscapeString(str, -1, CPLES_BackslashQuotable)로 처리한 문자열처럼 "역슬래시 이스케이프(backslash escaped)" 상태여야 합니다.
   des-contents는 DESVER로 시작하는 표준 DES 필드를 담고 있어야만 합니다. (MIL-STD-2500C를 참조하십시오.) 현재 CreateCopy() 메소드에서는 DES를 복사하지 않지만, Create() 메소드로 명확하게 설정하는 경우 추가할 수도 있습니다.

-  **NUMDES=n**: (GDAL 3.4 이상 버전)
   DES 부분들의 개수입니다. 첫 번째 이미지 부분에만 쓰입니다.

-  **SDE_TRE=YES/NO**:
   더 정밀한 지리참조를 위해 GEOLOB 및 GEOPSB TRE를 작성합니다.
   현재 지리 공간 좌표계와 CreateCopy()를 사용하는 경우에만 설정할 수 있습니다.

-  **RPC00B=YES/NO**: (GDAL 2.2.0 이상 버전)
   소스 RPC00B TRE가 존재하는 경우 소스 RPC00B TRE로부터, 또는 RPC 메타데이터 도메인에서 찾은 값들로부터 RPC00B TRE를 작성합니다. 현재 CreateCopy()를 사용하는 경우에만 연산에 넣습니다. NITF RPC00B 포맷이 제한된 정밀도의 ASCII 인코딩 숫자를 사용한다는 사실을 기억하십시오. 기본값은 YES입니다.

-  **RPCTXT=YES/NO**: (GDAL 2.2.0 이상 버전)
   외부 \_rpc.txt 파일에 RPC 메타데이터를 작성할지 여부를 선택합니다.
   내부 RPC00B TRE의 정밀도가 제한되어 있기 때문에 이 옵션이 유용할 수도 있습니다.
   현재 CreateCopy()를 사용하는 경우에만 연산에 넣습니다. 기본값은 NO입니다.

-  **USE_SRC_NITF_METADATA=YES/NO**: (GDAL 2.3.0 이상 버전)
   입력 데이터셋의 NITF_xxx 메타데이터 항목과 TRE 부분들을 사용할지 여부를 선택합니다.
   입력 파일의 지리참조 정보를 변경하는 경우 이 옵션을 NO로 설정해야 할 수도 있습니다.
   기본값은 YES입니다.

JPEG2000 압축 (쓰기 지원)
------------------------------------

JP2ECW(사용자가 JPEG2000 쓰기를 활성화할 수 있는 키를 가지고 있다고 가정할 때 SDK 3.3 이상 버전), JP2KAK, JP2OpenJPEG 또는 재스퍼(Jasper) 드라이버를 사용할 수 있는 경우, IC=C8 옵션을 사용하면 JPEG2000 압축 방식을 이용할 수 있습니다.

이 드라이버들을 사용할 수 있는 경우, (GDAL 3.4버전에서 추가된) JPEG2000_DRIVER 생성 옵션으로 사용할 JPEG2000 호환 드라이버를 명확하게 설정하지 않는 한 드라이버를 앞에서 언급한 순서대로 시도할 것입니다.

- :ref:`JP2ECW <raster.jp2ecw>`:
  JP2ECW 특화 생성 옵션 TARGET(원본 용량의 백분율로 대상 용량을 설정) 및 PROFILE=BASELINE_0/BASELINE_1/BASELINE_2/NPJE/EPJE를 사용할 수 있습니다. CreateCopy() 그리고/또는 Create() 메소드를 사용하는 경우 사용할 수 있습니다. 기본적으로 NPJE PROFILE을 사용할 것입니다. (즉 BLOCKXSIZE=BLOCKYSIZE=1024라는 의미입니다.)

- :ref:`JP2KAK <raster.jp2kak>`:
  JP2KAK 특화 생성 옵션 QUALITY, BLOCKXSIZE, BLOCKYSIZE, LAYERS, ROI를 사용할 수 있습니다.
  CreateCopy() 메소드를 사용하는 경우에만 사용할 수 있습니다.

- :ref:`JP2OpenJPEG <raster.jp2openjpeg>`:
  (CreateCopy() 메소드를 사용하는 경우에만 사용할 수 있습니다.)
  JP2OpenJPEG 특화 생성 옵션 QUALITY, BLOCKXSIZE 및 BLOCKYSIZE를 사용할 수 있습니다.
  기본적으로 BLOCKXSIZE=BLOCKYSIZE=1024를 사용할 것입니다.

  GDAL 3.4.0 및 OpenJPEG 2.5버전부터, `NCDRD(STDI-0006 NITF 2.1버전 상용 데이터셋 요구 사항 문서) <https://gwg.nga.mil/ntb/baseline/docs/stdi0006/STDI-0006-NCDRD-16Feb06.doc>`_ 를 준수하는 파일을 생성하기 위해 PROFILE=NPJE_VISUALLY_LOSSLESS/NPJE_NUMERICALLY_LOSSLESS 생성 옵션을 사용할 수 있습니다.
  NPJE_VISUALLY_LOSSLESS의 경우, 마지막 품질 레이어의 기본값이 픽셀 당 그리고 밴드 당 3.9비트입니다. QUALITY 생성 옵션으로 이를 조정할 수 있습니다. 프로파일을 지정하면, J2KLRA=NO 생성 옵션을 지정하지 않는 한 J2KLRA TRE도 작성할 것입니다.

-  재스퍼 JPEG2000 드라이버: CreateCopy() 메소드를 사용하는 경우에만 사용할 수 있습니다.

링크
-----

-  :ref:`고급 GDAL NITF 드라이버 정보 <raster.nitf_advanced>`


-  `NITFS 기술 위원회 공공 페이지 <http://www.gwg.nga.mil/ntb/>`_

-  `DIGEST Part 2 Annex D (NITF 공간 데이터 확장 사양의 인코딩 설명) <http://www.gwg.nga.mil/ntb/baseline/docs/digest/part2_annex_d.pdf>`_

-  :ref:`raster.rpftoc`: CIB 및 CADRG 상품 목차를 읽어보십시오.

-  `MIL-PRF-89038 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28080000+-+99999%29/MIL-PRF-89038_25371/>`_
   : RPF, CADRG, CIB 상품 사양

-  :ref:`raster.ecrgtoc`: ECRG 상품 목차를 읽어보십시오.

-  `MIL-PRF-32283 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28030000+-+79999%29/MIL-PRF-32283_26022/>`_
   : ECRG 상품 사양

감사의 말
--------

저자는 이 드라이버 개발을 지원해준 `AUG Signals <http://www.augsignals.com/>`_ 와 `GeoConnections <http://geoconnections.org/>`_ 프로그램에 감사드리며, JPEG 기능 추가를 도와준 스티브 롤린슨(Steve Rawlinson)과 BLOCKA 기능 추가를 도와준 라이너 벡(Reiner Beck)에게 감사의 말을 전합니다.
