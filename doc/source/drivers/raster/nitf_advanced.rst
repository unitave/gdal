.. _raster.nitf_advanced:

================================================================================
NITF -- 고급 드라이버 정보
================================================================================

GDAL의 NITF(National Imagery Transmission Format) 드라이버는 난해하다고도 할 수 있는 고급 옵션 여러 개를 포함하고 있습니다. 이 옵션들은 이 드라이버의 :ref:`일반 종단 사용자 문서 <raster.nitf>` 에는 어울리지 않습니다. 이 페이지에는 개발자와 고급 사용자를 위한 고급 드라이버 정보를 모아놓았습니다.

CGM 부분(segment)
-----------------

CGM 데이터(GR 부분 유형 - 그래픽, 또는 STYPE 값이 'C'인 SY)를 가진 NITF 파일은 CGM을 가지고 있다는 사실을 CGM 도메인에 있는 메타데이터로 알릴 것입니다. 반환되는 메타데이터는 다음처럼 보일 것입니다:

::

     SEGMENT_COUNT=1
     SEGMENT_0_SLOC_ROW=25
     SEGMENT_0_SLOC_COL=25
     SEGMENT_0_SDLVL=2
     SEGMENT_0_SALVL=1
     SEGMENT_0_CCS_ROW=00025
     SEGMENT_0_CCS_COL=00025
     SEGMENT_0_DATA=\0!\0...

SLOC_ROW 및 SLOC_COL 값은 기반 (SALVL) 이미지에 상대적인 CGM 객체의 배치입니다. CCS_ROW 및 CCS_COL은 공통 좌표계에 상대적인 값입니다. \_SDLVL은 출력 수준입니다. DATA는 "인용 가능한 역슬래시(backslash quotable)" 이스케이프 작업을 거친 원본(raw) CGM 데이터입니다. 모든 아스키 0은 '\0'으로 변환되고, 모든 역슬래시와 큰따옴표도 역슬래시로 이스케이프될 것입니다. CPLUnescapeString() 함수를 통해 CPLES_BackslashQuotable 스키마를 이용하면 데이터를 바이너리 포맷으로 역 이스케이프시킬 수 있습니다.

NITF 이미지에 CGM 데이터를 추가하려면 생성 옵션을 다음과 같은 서식으로 전송해주면 됩니다:

::

     CGM=SEGMENT_COUNT=1
     CGM=SEGMENT_0_SLOC_ROW=25
     CGM=SEGMENT_0_SLOC_COL=25
     CGM=SEGMENT_0_SDLVL=2
     CGM=SEGMENT_0_SALVL=1
     CGM=SEGMENT_0_DATA=\0!\0...

CGM을 생성 옵션으로 전송하면 CGM 메타데이터 도메인에서 읽어온 CGM 부분을 덮어쓸 것이라는 사실을 기억하십시오.

GDAL은 CGM 데이터 파싱 또는 렌더링을 지원하지 않지만, 적어도 한 명의 사용자가 CGM 데이터 파싱 또는 렌더링에 `UniConverter <http://sk1project.org/modules.php?name=Products&product=uniconvertor>`_ 라이브러리가 유용하다는 사실을 알아냈습니다.

다중 이미지 NITF 파일
----------------------

하나 이상의 이미지 부분(IM)을 가진 NITF 파일은 이미지 부분들을 하위 데이터셋으로 노출시킵니다. 다중 NITF 파일을 파일명으로 열면 첫 번째 이미지 부분에 접근할 수 있습니다. 이미지 3개를 가진 NITF 파일의 하위 데이터셋 메타데이터는 다음처럼 보일 것입니다:

::

   Subdatasets:
     SUBDATASET_1_NAME=NITF_IM:0:multi_image_jpeg_2.0.ntf
     SUBDATASET_1_DESC=Image 1 of multi_image_jpeg_2.0.ntf
     SUBDATASET_2_NAME=NITF_IM:1:multi_image_jpeg_2.0.ntf
     SUBDATASET_2_DESC=Image 2 of multi_image_jpeg_2.0.ntf
     SUBDATASET_3_NAME=NITF_IM:2:multi_image_jpeg_2.0.ntf
     SUBDATASET_3_DESC=Image 3 of multi_image_jpeg_2.0.ntf

이 경우 "multi_image_jpeg_2.0.ntf"를 직접 열면 "NITF_IM:0:multi_image_jpeg_2.0.ntf"에 접근합니다. 다른 이미지를 열려면 해당 하위 데이터셋 이름을 이용하십시오. 이 하위 데이터셋 메커니즘은 :ref:`raster_data_model` 문서에서 논의하는 일반 GDAL 개념입니다.

텍스트 부분
-------------

텍스트 부분을 가진 NITF 파일은 텍스트를 가지고 있다는 사실을 TEXT 도메인에 있는 메타데이터로 알릴 것입니다. 반환되는 메타데이터는 다음처럼 보일 것입니다:

::

     HEADER_0=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     DATA_0=This is test text file 01.

     HEADER_1=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     DATA_1=This is test text file 02.

     HEADER_2=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     DATA_2=This is test text file 03.

     HEADER_3=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     DATA_3=This is test text file 04.

     HEADER_4=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     DATA_4=This is test text file 05.

DATA_n의 인자는 (0에서 시작하는) n번째 텍스트 부분의 어떤 유형의 이스케이프도 적용되지 않은 원본(raw) 텍스트입니다.

TEXT 부분 헤더 데이터는 HEADER_n 메타데이터 항목에 보전됩니다. NITF 드라이버를 사용하는 CreateCopy() 메소드는 입력 파일이 TEXT 도메인에 메타데이터를 앞에 정의된 대로 가지고 있는 한 산출 파일에 텍스트 부분을 생성하는 옵션을 지원합니다.

NITF 이미지에 TEXT 데이터를 추가하려면 생성 옵션을 다음과 같은 서식으로 전송해주면 됩니다:

::

     TEXT=HEADER_0=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     TEXT=DATA_0=This is test text file 01.
     TEXT=HEADER_1=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
     TEXT=DATA_1=This is test text file 02.

TEXT를 생성 옵션으로 전송하면 TEXT 메타데이터 도메인에서 읽어온 텍스트 부분을 덮어쓸 것이라는 사실을 주의하십시오.

TRE
----

파일 헤더, 또는 언급했던 이미지 헤더에 등록 (또는 미등록?) 확장 사양을 가지고 있는 NITF 파일은 태그된 레코드 확장 사양(Tagged Record Extension)을 가지고 있다는 사실을 TRE 도메인을 통해 원본 메타데이터라는 형태로 알릴 것입니다. TRE 도메인은 각 TRE 당 해당 TRE의 이름을 이름으로 삼고 TRE의 데이터를 내용으로 가질 메타데이터 항목을 가지게 될 것입니다. 이 데이터 내용은 앞의 CGM 데이터처럼 "역슬래시 이스케이프"될 것입니다.

동일한 TRE가 여러 번 나오는 경우, 두 번째 나오는 TRE의 이름이 "TRENAME_2", 세 번째 이름은 "TRENAME_3", ... 이 될 것입니다. 이때 TRENAME은 TRE의 이름입니다.

::

   Metadata (TRE):
     GEOPSB=MAPM  World Geodetic System 1984
                  WGE World Geodetic System 1984
                      WE Geodetic
                         GEODMean Sea
                             MSL 000000000000000
                                                   0000
     PRJPSB=Polar Stereographic
            PG2-00090.00000250000039.99999884000000000000000000000000000000
     MAPLOB=M  0598005958-000003067885.8-000002163353.8

TREs as xml:TRE
---------------

파일에서 검색되었고 GDAL data 디렉터리에 있는 `nitf_spec.xml <http://trac.osgeo.org/gdal/browser/trunk/gdal/data/nitf_spec.xml>`_ 의 TRE 설명 가운데 하나와 일치하는 모든 TRE를 xml:TRE 메타데이터 도메인의 XML 콘텐츠로 리포트할 것입니다.

::

   Metadata (xml:TRE):
   <tres>
     <tre name="RSMDCA" location="des TRE_OVERFLOW">
       <field name="IID" value="2_8" />
       <field name="EDITION" value="1101222272-2" />
       <field name="TID" value="1101222272-1" />
       <field name="NPAR" value="06" />
       <field name="NIMGE" value="001" />
       <field name="NPART" value="00006" />
       <repeated name="IMAGE" number="1">
         <group index="0">
           <field name="IID" value="2_8" />
           <field name="NPARI" value="06" />
         </group>
       </repeated>
       <field name="XUOL" value="-2.42965895449297E+06" />
       <field name="YUOL" value="-4.76049894293300E+06" />
       <field name="ZUOL" value="+3.46898407315533E+06" />
       <field name="XUXL" value="+8.90698769551156E-01" />
       <field name="XUYL" value="+2.48664813021570E-01" />
       <field name="XUZL" value="-3.80554217799520E-01" />
       <field name="YUXL" value="-4.54593996792805E-01" />
       <field name="YUYL" value="+4.87215943350720E-01" />
       <field name="YUZL" value="-7.45630553709282E-01" />
       <field name="ZUXL" value="+0.00000000000000E+00" />
       <field name="ZUYL" value="+8.37129879594448E-01" />
       <field name="ZUZL" value="+5.47004172461403E-01" />
   [...]
       <repeated name="DERCOV" number="21">
         <group index="0">
           <field name="DERCOV" value="+5.77388827727787E+04" />
         </group>
   [...]
         <group index="20">
           <field name="DERCOV" value="+1.14369570920252E-02" />
         </group>
       </repeated>
     </tre>
     <tre name="RSMECA" location="des TRE_OVERFLOW">
   [...]
     </tre>
     <tre name="RSMIDA" location="des TRE_OVERFLOW">
   [...]
     </tre>
     <tre name="RSMPCA" location="des TRE_OVERFLOW">
   [...]
     </tre>
   </tres>

16진법 데이터로부터 TRE 생성
----------------------------------

새로 생성하는 NITF 파일에 TRE 데이터를 부호 없는 정수형 또는 부동소수점형 같은 바이너리 데이터를 인코딩하기 위한 16진법 형식으로 추가할 수 있습니다. 16진법 TRE 생성 옵션의 서식은 "TRE=HEX/<tre_name>=<hex_tre_data>" 또는 "FILE_TRE=HEX/<tre_name>=<hex_tre_data> 입니다.

.. code-block:: python

    # Encode "ABC" as 3 bytes of hex data, "414243"
    ds = gdal.GetDriverByName('NITF').Create('/vsimem/file.ntf', 1, 1, options=["TRE=HEX/TSTTRE=414243"])

데이터 확장 사양 부분 (xml:DES)
---------------------------------

DES(Data Extension Segment)란 NITF 포맷의 사용자 정의 메타데이터 확장 사양입니다. xml\:DES 메타데이터 도메인을 통해 DES 메타데이터를 사용할 수 있습니다. xml\:DES 도메인은 표준 및 사용자 정의 DES 필드를 가진 XML 문자열을 평문으로, 그리고 사용자 정의 DES 데이터를 Base64 인코딩 텍스트로 반환합니다. 다음은 XML 구조의 예시입니다:

::

    <des_list>
      <des name="TEST">
        <field name="NITF_DESVER" value="02" />
        <field name="NITF_DECLAS" value="U" />
        <field name="NITF_DESCLSY" value="" />
        [...]
        <field name="NITF_DESCTLN" value="" />
        <field name="NITF_DESSHL" value="0004" />
        <field name="NITF_DESSHF" value="ABCD" />
        <field name="NITF_DESDATA" value="MTIzNDU2Nzg5MA==" />
      </des>
    </des_list>

RAW 파일 / 이미지 헤더
------------------------

응용 프로그램이 이미지 헤더 또는 파일 헤더로부터 일반적으로 메타데이터로 사용할 수 없는 매우 특정한 정보를 복구해야 하는 경우가 있을 수도 있습니다. 이런 경우 "NITF_METADATA" 메타데이터 도메인을 쿼리하면 됩니다. 완전한 파일 헤더 및 이미지 헤더를 Base64 인코딩 형식으로 반환할 것입니다. 다음은 그 예시입니다:

::

   Metadata (NITF_METADATA):
     NITFFileHeader=002213 TklURjAyLjAwMDEgICAgVTIxN0cwSjA...
     NITFImageSubheader=439 SU1NaXNzaW5nIElEMjUxNTI1NTlaTU...

Base64 인코딩 헤더 앞에 있는 아스키 인코딩 숫자값은 뒤에 공백 문자 하나가 붙은 바이트 단위 (디코딩된) 길이라는 사실을 기억하십시오.

다중 이미지 부분 작성
-------------------------------

(GDAL 3.4 이상 버전)

``APPEND_SUBDATASET=YES`` 생성 옵션으로 여러 개의 이미지 부분을 가진 NITF 파일을 작성할 수 있지만, 주의가 필요합니다.

이미지 부분의 총 개수를 지정하는 ``NUMI`` 생성 옵션과 DE 부분의 개수를 지정하는 ``NUMDES`` 선택 옵션으로 첫 번째 이미지 부분의 내용을 가진 파일을 생성해야만 합니다. 파일 전체에 적용되는 TRE도 이 단계에서 지정해야 합니다. 이 단계에서 절대로 ``APPEND_SUBDATASET`` 생성 옵션을 지정해서는 안 됩니다.

첫 파일을 생성한 다음, ``APPEND_SUBDATASET=YES`` 생성 옵션으로 그 다음 이미지들을 추가합니다. ``IDLVL``, ``IALVL``, ``ILOCROW`` 및 ``ILOCCOL`` 생성 옵션도 지정할 수 있습니다.

마지막 이미지 부분을 추가할 때, DES 콘텐츠가 하나라도 있다면 반드시 ``DES`` 생성 옵션으로 지정해야만 합니다.

.. note:: NUMI 개수의 이미지 모두를 실제로 작성해야만 파일이 무결할 것입니다.

예시:

::

    gdal_translate first_image.tif  dest.tif -co NUMI=3 -co NUMDES=1
    gdal_translate second_image.tif dest.tif -co APPEND_SUBDATASET=YES -co IC=C3 -co IDLVL=2
    gdal_translate third_image.tif  dest.tif -co APPEND_SUBDATASET=YES -co IC=C8 -co IDLVL=3 -co "DES=DES1={des_content}"
