.. _rfc-43:

=======================================================================================
RFC 43: GDALMajorObject::GetMetadataDomainList
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

요약
----

이 (소규모) RFC는 :cpp:class:`GDALMajorObject` 클래스(및 C API)에 사용할 수 있는 모든 메타데이터 도메인을 반환하는 새로운 :cpp:func:`GetMetadataDomainList` 가상 메소드를 추가할 것을 제안합니다.

배경
----

:cpp:class:`GDALMajorObject` 클래스는 현재 메타데이터 도메인 인자를 입력받는 :cpp:func:`GetMetadata` 및 :cpp:func:`GetMetadataItem` 2개의 메소드를 제공합니다. 그러나 지정한 :cpp:class:`GDALMajorObject` 에서 (예를 들면 데이터셋 또는 래스터 밴드에서) 어떤 메타데이터 도메인들이 무결한지 자동으로 발견할 수 있는 방법이 없습니다. 때문에 데이터셋/래스터 밴드에 있는 모든 메타데이터를 철저하게 발견할 수 있는 일반 코드를 가질 수가 없게 됩니다.

구현
----

:cpp:class:`GDALMajorObject` 의 기반 구현은 내부 'oMDMD' 멤버에 대해 :cpp:func:`GetDomainList` 를 호출할 뿐입니다.

::

   /************************************************************************/
   /*                      GetMetadataDomainList()                         */
   /************************************************************************/

   /*
    * \brief 메타데이터 도메인 목록을 가져옵니다.
    *
    * (비어 있지 않은) 메타데이터 도메인들의 목록인 문자열 목록을 반환합니다.
    *
    * 이 메소드는 GDALGetMetadataDomainList() C 함수와 동일한 작업을 수행합니다.
    * 
    * @return NULL 또는 문자열 목록을 반환합니다. CSLDestroy()로 목록을 해제해야만 합니다.
    *
    * @since GDAL 1.11
    */

   char **GDALMajorObject::GetMetadataDomainList()
   {
       return CSLDuplicate(oMDMD.GetDomainList());
   }

C API(``char ** CPL_STDCALL GDALGetMetadataDomainList( GDALMajorObjectH hObject)``)와 SWIG 바인딩에서도 이 메소드를 사용할 수 있습니다.

영향을 받는 드라이버
--------------------

GetMetadata() 그리고/또는 GetMetadataItem()을 사용자 지정 구현한 드라이버들은 일반적으로 'oMDMD' 멤버를 수정하지 않는 경우 GetMetadataDomainList()도 구현해야 할 것입니다.

특화된 GetMetadataDomainList() 메소드를 쉽게 구현하기 위해, :cpp:class:`GDALMajorObject` 클래스가 다음과 같이 사용할 수 있는 보호된(protected) BuildMetadataDomainList() 메소드를 제공할 것입니다:

::

   /************************************************************************/
   /*                      GetMetadataDomainList()                         */
   /************************************************************************/

   char **NITFDataset::GetMetadataDomainList()
   {
       return BuildMetadataDomainList(GDALPamDataset::GetMetadataDomainList(),
                                      TRUE,
                                      "NITF_METADATA", "NITF_DES", "NITF_DES_METADATA",
                                      "NITF_FILE_HEADER_TRES", "NITF_IMAGE_SEGMENT_TRES",
                                      "CGM", "TEXT", "TRE", "xml:TRE", "OVERVIEWS", NULL);
   }

``TRUE`` 파라미터는 그 뒤에 오는 도메인 목록이 잠재적 도메인들임을 의미하기 때문에, BuildMetadataDomainList()가 GetMetadata()가 반환하는 각 도메인이 NULL이 아닌 값인지 확인할 것입니다.

GDAL 드라이버들에 대해 철저하게 검색해서 GetMetadataDomainList() 메소드를 구현하도록 업데이트해야 할 드라이버들을 모두 업데이트했습니다:

-  ADRG
-  BAG
-  CEOS2
-  DIMAP
-  ECW ENVISAT
-  ERS
-  GeoRaster (컴파일되는지 확인하지 못 했습니다)
-  GIF
-  GTiff
-  HDF4
-  JPEG
-  MBTILES
-  netCDF
-  NITF
-  OGDI
-  PCIDSK
-  PDF
-  PNG
-  PostgisRaster
-  RasterLite
-  RS2
-  VRT
-  WCS
-  WebP
-  WMS

몇 가지 주의할 점:

-  MBTiles, WMS 및 VRT 드라이버의 경우 ``GetMetadata("LocationInfo")`` 자체가 메타데이터를 반환하지 않더라도, 밴드 수준에서 GetMetadataDomainList()가 "LocationInfo"를 (gdallocationinfo 유틸리티가 사용하는) 무결한 메타데이터 도메인으로 반환할 것입니다:
   ``GetMetadataItem("Pixel_someX_someY", "LocationInfo")`` 또는 ``GetMetadataItem("GeoPixel_someX_someY", "LocationInfo")`` 를 호출해야 합니다.

-  CEOS2 및 ENVISAT 드라이버의 경우, 메타데이터 도메인 목록을 쉽게 확정할 수 없습니다. GetMetadataDomainList() 메소드는 받아들일 수 있는 도메인 이름들의 패턴을 반환할 것입니다.

영향을 받는 유틸리티
--------------------

gdalinfo 유틸리티가 다음을 입력받을 수 있도록 확장합니다:

-  사용할 수 있는 메타데이터 도메인들을 출력할 "-listmdd" 옵션:

::

   $ gdalinfo ../autotest/gdrivers/data/byte_with_xmp.jpg -listmdd

   Driver: JPEG/JPEG JFIF
   Files: ../autotest/gdrivers/data/byte_with_xmp.jpg
   Size is 20, 20
   Coordinate System is `'
   Metadata domains:
     xml:XMP
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,   20.0)
   Upper Right (   20.0,    0.0)
   Lower Right (   20.0,   20.0)
   Center      (   10.0,   10.0)
   Band 1 Block=20x1 Type=Byte, ColorInterp=Gray
     Metadata domains:
       IMAGE_STRUCTURE
     Image Structure Metadata:
       COMPRESSION=JPEG

-  모든 메타데이터 도메인의 내용을 출력할 "-mdd all" 옵션:

::

   $ gdalinfo ../autotest/gdrivers/data/byte_with_xmp.jpg -mdd all

   Driver: JPEG/JPEG JFIF
   Files: ../autotest/gdrivers/data/byte_with_xmp.jpg
   Size is 20, 20
   Coordinate System is `'
   Metadata (xml:XMP):
   <?xpacket begin='' id='W5M0MpCehiHzreSzNTczkc9d'?>
   <x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='Image::ExifTool 7.89'>
   <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>

    <rdf:Description rdf:about=''
     xmlns:dc='http://purl.org/dc/elements/1.1/'>
     <dc:description>
      <rdf:Alt>
       <rdf:li xml:lang='x-default'>Description</rdf:li>
      </rdf:Alt>
     </dc:description>
     <dc:subject>
      <rdf:Bag>
       <rdf:li>XMP</rdf:li>
       <rdf:li>Test</rdf:li>
      </rdf:Bag>
     </dc:subject>
     <dc:title>
      </rdf:Alt>
     </dc:title>
    </rdf:Description>

    <rdf:Description rdf:about=''
     xmlns:tiff='http://ns.adobe.com/tiff/1.0/'>
     <tiff:BitsPerSample>
      <rdf:Seq>
       <rdf:li>8</rdf:li>
      </rdf:Seq>
     </tiff:BitsPerSample>
     <tiff:Compression>1</tiff:Compression>
     <tiff:ImageLength>20</tiff:ImageLength>
     <tiff:ImageWidth>20</tiff:ImageWidth>
     <tiff:PhotometricInterpretation>1</tiff:PhotometricInterpretation>
     <tiff:PlanarConfiguration>1</tiff:PlanarConfiguration>
     <tiff:SamplesPerPixel>1</tiff:SamplesPerPixel>
    </rdf:Description>
   </rdf:RDF>
   </x:xmpmeta>
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
                                                                                                       
   <?xpacket end='w'?>
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,   20.0)
   Upper Right (   20.0,    0.0)
   Lower Right (   20.0,   20.0)
   Center      (   10.0,   10.0)
   Band 1 Block=20x1 Type=Byte, ColorInterp=Gray
     Image Structure Metadata:
       COMPRESSION=JPEG

하위 호환성
-----------

이 변경 사항은 C API/ABI 및 C++ API 수준에서 하위 호환성에 어떤 영향도 미치지 않습니다. 그러나 C++ ABI 수준에서는 영향을 미치기 때문에, 모든 GDAL 드라이버를 완전히 다시 빌드해야 합니다.

테스트
------

파이썬 자동 테스트 스위트가 몇몇 드라이버에서 새 API를 테스트하도록 확장시킬 것입니다.

티켓
----

이 RFC의 진행 상황을 추적하는 #5275 티켓을 열었습니다.

`#5275 티켓 첨부 파일 <http://trac.osgeo.org/gdal/attachment/ticket/5275/getmetadatadomainlist.patch>`_ 로 이 RFC의 구현을 사용할 수 있습니다.

투표 이력
---------

-  이벤 루올 +1
-  대니얼 모리셋 +1
-  유카 라흐코넨 +1

