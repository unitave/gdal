.. _rfc-44:

=======================================================================================
RFC 44: ogrinfo 및 gdalinfo에 파싱 가능한 산출 서식 추가
=======================================================================================

저자: 댄 리틀(Dan "Ducky" Little), 파자 마하무드(Faza Mahamood)

연락처: danlittle@yahoo.com, fazamhd@live.com

상태: 개발 중, GDAL 2.0버전에 "gdalinfo -json" 구현

요약
----

ogrinfo 및 gdalinfo 유틸리티에 XML과 JSON 산출물을 추가할 것을 제안합니다.

배경
----

ogrinfo 및 gdalinfo는 너무나도 유용한 메타데이터 수집 도구들입니다. 하지만 이 유틸리티들의 네이티브한 텍스트 기반 서식은 흔히 사용되는 외부 도구들로 쉽게 파싱할 수 없습니다. XML과 JSON은 둘 다 쉽게 파싱할 수 있는 서식으로, 이 산출 서식들을 추가하면 ogrinfo 및 gdalinfo 유틸리티를 스크립트 작업 스택에 추가하려는 사람들을 위한 활용성이 크게 증가할 것입니다.

구현
----

`이 깃허브 포크 <https://github.com/theduckylittle/gdal/blob/trunk/gdal/apps/ogrinfo.cpp>`_ 에서 이 RFC의 구현 예시를 찾아볼 수 있습니다.

각 유틸리티에 XML 산출물을 추가하려면 주 루프(main loop)를 조건부 덩어리(contingent chunk)들로 "분할"해야 할 것입니다. STDOUT 상에서의 산출물을 항상 파싱할 수 있다는 사실을 보장하기 위해 모든 진단 메시지도 STDERR로 이동시켜야 할 것입니다. GDAL 안에 빌드된 MiniXML 라이브러리를 사용해서 XML 표현을 구성할 것입니다.

gdalinfo에 대해 제안하는 JSON 서식
----------------------------------

::

   {
       "description": "...",
       "driverShortName": "GTiff",
       "driverLongName": "GeoTIFF",
       "files": [ (if -nofl not specified)
           "../gcore/data/byte.tif",
           "../gcore/data/byte.tif.aux.xml"
       ],
       "size": [
           20,
           20
       ],
       "coordinateSystem": {
           "proj": "+proj=.......", (if -proj4 specified)
           "wkt": "PROJCS[....]"
       },
       "gcps": { (if -nogcp not specified)
           "coordinateSystem": {
               "proj": "+proj=.......", (if -proj4 specified)
               "wkt": "PROJCS[....]"
           },
           "gcpList": [
               {
                   "id": "1",
                   "info": "a",
                   "pixel": 0.5,
                   "line": 0.5,
                   "X": 0.0,
                   "Y": 0.0,
                   "Z": 0.0
               },
               {
                   "id": "2",
                   "info": "b",
                   .
                   .
                   .
               }
           ]
       },
       "geoTransform": [
           440720.000000000000000,
           60.000000000000000,
           0.0,
           3751320.000000000000000,
           0.0,
           -60.000000000000000
       ],
       "cornerCoordinates":{
         "upperLeft":[
           440720.0,
           3751320.0
         ],
         "lowerLeft":[
           440720.0,
           3750120.0
         ],
         "upperRight":[
           441920.0,
           3751320.0
         ],
         "lowerRight":[
           441920.0,
           3750120.0
         ],
         "center":[
           441320.0,
           3750720.0
         ]
       },
       "wgs84Extent":{
         "type":"Polygon",
         "coordinates":[
         [
           [
             -117.642054,
             33.9023677
           ],
           [
             -117.6419729,
             33.8915454
           ],
           [
             -117.6290752,
             33.9024346
           ],
           [
             -117.6289957,
             33.8916123
           ],
           [
             -117.642054,
             33.9023677
           ]
          ]
         ]
       },
       "rat": { (if -norat not specified)
           "row0Min": 40918,
           "binSize": 1,
           "fieldDefn": [
               {
                   "index": 0,
                   "name": "Histogram",
                   "type": "integer",
                   "usage": "PixelCount"
               },
               {
                   "index": 1,
                   "name": "fieldName2",
                   "type": 2,
                   "usage": 2
               },
           ],
           "rows": [
               {
                   "index": 0,
                   "f": [
                       1,
                       4
                   ]
               },
               {
                   "index": 1,
                   "f": [
                       5,
                       4
                   ]
               },
               .
               .
               .
           ]
       },
       "metadata": { (if -nomd not specified)
           "": {
               "key1": "value1"
           },
           "IMAGE_STRUCTURE": {
               "key1": "value1"
           },
           "OTHER_DOMAIN": {
               "key1": "value1"
           },
       },
       "cornerCoordinates": {
           "upperLeft": [
               440720.000,
               3751320.000
           ],
           "lowerLeft": [
               440720.000,
               3750120.000
           ],
           "upperRight": [
               441920.000,
               3751320.000
           ],
           "lowerRight": [
               441920.000,
               3750120.000
           ],
           "center": [
               441320.000,
               3750720.000
           ]
       },
       "bands": [
           {
               "description": "...",
               "band": 1,
               "block": [
                   20,
                   20
               ],
               "type": "Byte",
               "colorInterp": "Gray",
               "min": 74.000,
               "max": 255.000,
               
               "computedMin": 74.000, (if -mm specified)
               "computedMax": 255.000,
               
               "minimum": 74.000, (if -stats specified)
               "maximum": 255.000,
               "mean": 126.765,
               "stdDev": 22.928,
               
               "unit": "....",
               "offset": X,
               "scale": X,
               "noDataValue": X,
               "overviews": [
                   {
                       "size": [
                           400,
                           400 ],
                       "checksum": X (if -checksum specified)
                   }, 
                   {
                       "size": [
                           200,
                           200 ],
                       "checksum": X (if -checksum specified)
                   }
               ],
               "mask": {
                   "flags": [
                       "PER_DATASET",
                       "ALPHA"
                   ],
                   "overviews": [
                       {
                           "size": [
                               400,
                               400 ]
                       }, 
                       { 
                           "size": [
                               200,
                               200 ],
                       }
                   ]
               },
               "metadata": { (if -nomd not specified)
                   "__default__": {
                       "key1": "value1"
                   },
                   "IMAGE_STRUCTURE": {
                       "key1": "value1"
                   },
                   "OTHER_DOMAIN": {
                       "key1": "value1"
                   },
               },
               "histogram": { (if -hist specified)
                   "count": 25,
                   "min": -0.5,
                   "max": 255.5,
                   "buckets": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
               },
               "checksum": 4672, (if -checksum specified)
               "colorTable": { (if -noct not specified)
                   "palette": "RGB",
                   "count": 6,
                   "entries": [
                       [255,255,255,255],
                       [255,255,208,255],
                       [255,255,204,255],
                       [153,204,255,255],
                       [0,153,255,255],
                       [102,102,102,255]
                   ]
               }
           },
           {
               "band": 2,
               "block": [
                   20,
                   20
               ],
               .
               .
               .
           }
       ]
   }

영향을 받는 드라이버
--------------------

없음.

영향을 받는 유틸리티
--------------------

-  gdalinfo

   -  "-xml" 산출 옵션을 추가합니다.
   -  "-json" 산출 옵션을 추가합니다.

-  ogrinfo

   -  "-xml" 산출 옵션을 추가합니다.
   -  "-json" 산출 옵션을 추가합니다.

하위 호환성
-----------

이 변경 사항은 C API/ABI 및 C++ API/ABI 수준에서 하위 호환성에 어떤 영향도 미치지 않습니다. 기본 산출물은 그대로 유지될 것입니다. 새로운 XML 산출물은 명령줄에 "-xml" 또는 "-json"을 지정한 사용자들에게만 영향을 미칠 것입니다.

테스트
------

파이썬 자동 테스트 스위트가 새 XML/JSON 산출물을 테스트하도록 확장하고, 기존 테스트들이 진단(diagnostic) 메시지를 위해 STDERR를 확인하도록 수정할 것입니다.

티켓
----

없음.

투표 이력
---------

