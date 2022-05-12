.. _rfc-15:

================================================================================
RFC 15: 밴드 마스크
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인

요약
----

몇몇 파일 포맷들은 무결하지 않은 데이터인 픽셀을 식별하기 위한 비트마스크(bitmask)라는 개념을 지원합니다. 모든 픽셀값이 무결한 의미를 가지기 때문에 NODATA 픽셀값을 사용할 수 없는 바이트 이미지 포맷을 작업할 때 이 비트마스크가 특히 유용할 수 있습니다. 이 RFC는 다른 종류의 마스크 작업(NODATA 값 및 알파 밴드)을 표현하는 균일한 수단을 지향하면서 이런 NULL 마스크를 인식하고 접근하는 방법을 공식화하려 합니다.

기본 접근법은 이런 마스크를 래스터 밴드로 취급하는 것이지만, 데이터 소스 상에 있는 정규 래스터 밴드처럼 취급하는 것은 아닙니다. 그 대신 오버뷰 래스터 밴드 객체와 유사한 방식의 독립형 래스터 밴드로 취급합니다. 마스크는 0 값이 NODATA를 나타내고 0이 아닌 값이 무결한 데이터를 나타내는 GDT_Byte 밴드로 표현됩니다. 일반적으로 무결한 데이터 픽셀에 255 값을 사용할 것입니다.

API
---

:cpp:class:`GDALRasterBand` 클래스에 다음 메소드를 추가해서 확장합니다:

::

       virtual GDALRasterBand *GetMaskBand();
       virtual int             GetMaskFlags();
       virtual CPLErr          CreateMaskBand( int nFlags );

:cpp:class:`GDALDataset` 클래스에 다음 메소드를 추가해서 확장합니다:

::

       virtual CPLErr          CreateMaskBand( nFlags );

:cpp:class:`GDALRasterBand` 마스크가 GMF_ALL_VALID를 의미하는 플래그를 가진 모든 픽셀값이 255인 마스크인 경우에도 :cpp:func:`GetMaskBand` 메소드가 항상 :cpp:class:`GDALRasterBand` 마스크를 반환해야 한다는 사실을 기억하십시오.

:cpp:func:`GetMaskFlags` 메소드는 향후 확장될 수도 있는 다음과 같은 사용 가능한 정의를 가진, 비트 단위로 OR 처리된 상태 플래그 집합을 반환합니다:

-  GMF_ALL_VALID(0x01):
   무결하지 않은 픽셀이 없고, 모든 마스크 값이 255일 것입니다. 이 플래그를 사용하는 경우 일반적으로 이 플래그가 유일하게 설정된 플래그일 것입니다.

-  GMF_PER_DATASET(0x02):
   데이터셋 상에 있는 모든 밴드가 마스크 밴드를 공유합니다.

-  GMF_ALPHA(0x04):
   마스크 밴드가 실제로는 알파 밴드이고 0 및 255가 아닌 다른 값을 가질 수도 있습니다.

-  GMF_NODATA(0x08):
   실제로는 NODATA 값들로부터 마스크를 생성한다는 의미입니다. (GMF_ALPHA와 함께 사용할 수 없습니다.)

:cpp:func:`CreateMaskBand` 메소드는 자신이 호출된 밴드와 연결된 마스크 밴드를 생성하려 시도할 것입니다. 마스크 밴드를 지원하지 않는 경우 오류를 발생시킵니다. 현재 마스크 밴드를 생성할 때 전송하는 플래그 가운데 의미가 있는 플래그는 GMF_PER_DATASET뿐입니다. 나머지는 특수 시스템 제공 마스크 밴드를 나타내는 데 사용합니다. 데이터셋에 대해 :cpp:func:`CreateMaskBand` 를 호출하는 경우 GMF_PER_DATASET 플래그라고 가정합니다.

기본 GetMaskBand() / GetMaskFlags() 구현
----------------------------------------

:cpp:class:`GDALRasterBand` 클래스는 다음 3개의 기본 구현 가운데 하나를 반환하는 :cpp:func:`GetMaskBand` 메소드의 기본 구현을 포함할 것입니다.

-  대응하는 .msk 파일이 존재하는 경우 마스크 밴드 용으로 사용할 것입니다.

-  밴드가 NODATA 값 집합을 가지고 있는 경우, 새 :cpp:class:`GDALNodataMaskRasterBand` 클래스의 인스턴스를 반환할 것입니다. :cpp:func:`GetMaskFlags` 메소드는 GMF_NODATA를 반환할 것입니다.

-  NODATA 값이 존재하지 않지만 데이터셋이 해당 밴드에 적용되는 것처럼 보이는 (특정 규칙이 아직 결정되지 않았습니다) 알파 밴드를 가지고 있고 알파 밴드가 GDT_Byte 유형인 경우, 해당 알파 밴드를 반환하고 플래그에 GMF_PER_DATASET 및 GMF_ALPHA를 반환할 것입니다.

-  앞의 3개 가운데 하나도 적용되지 않는 경우, 모든 픽셀값이 255인 새 :cpp:class:`GDALAllValidRasterBand` 클래스의 인스턴스를 반환할 것입니다. NULL 플래그는 GMF_ALL_VALID를 반환할 것입니다.

:cpp:class:`GDALRasterBand` 클래스는 보호된 'poMask' 인스턴스 변수와 'bOwnMask' 플래그를 포함할 것입니다. 기본 :cpp:func:`GetMaskBand` 를 처음으로 호출하면 :cpp:class:`GDALNodataMaskRasterBand` 및 :cpp:class:`GDALAllValidMaskRasterBand` 를 생성하고, 이 둘이 할당된 'poMask'도 'bOwnMask' 플래그를 TRUE로 설정해서 생성할 것입니다. 알파 밴드를 사용한다고 식별하는 경우, 알파 밴드가 할당된 'poMask'를 'bOwnMask' 플래그를 FALSE로 설정해서 생성할 것입니다. 삭제자(destructor)에 'bOwnMask'가 TRUE로 설정된 경우 :cpp:class:`GDALRasterBand` 클래스가 'poMask' 삭제를 처리할 것입니다. 파생 밴드 클래스는 의미가 유지되는 한 'poMask'와 'bOwnMask' 플래그를 유사하게, 안전하게 사용할 수도 있습니다.

GDAL이 외부 .msk 파일을 인식하려면, 주 데이터셋과 동일한 이름에 접미어 .msk를 붙인 이름의 무결한 GDAL 데이터셋이어야만 하고, (GMF_PER_DATASET의 경우) 밴드 하나를 또는 주 데이터셋과 동일한 개수의 밴드를 가져야만 합니다. 외부 .msk 파일은 데이터셋 수준에서 설정된 INTERNAL_MASK_FLAGS_xx 메타데이터 항목을 가져야만 합니다. 이때 xx가 주 데이터셋 밴드의 밴드 번호와 일치해야만 합니다. 이 항목의 값은 GMF_ALL_VALID, GMF_PER_DATASET, GMF_ALPHA 및 GMF_NODATA 플래그들의 조합입니다. 어떤 밴드의 이 메타데이터 항목이 없는 경우, 실시간(on-the-fly)으로 마스크 밴드를 생성하기 위해 앞에서 설명한 3개의 규칙 가운데 하나를 사용할 것입니다.

기본 CreateMaskBand()
---------------------

:cpp:func:`CreateMaskBand` 메소드의 기본 구현은 :cpp:class:`GDALDefaultOverviews` 객체를 사용해서 구현된 .ovr 처리에 적용되는 규칙과 비슷한 규칙을 기반으로 구현될 것입니다. 원본 파일과 동일한 기본명을 가지고 확장자가 .msk인 TIFF 파일을 생성할 것이며, 생성된 파일은 원본 이미지와 동일한 개수의 밴드를 (또는 GMF_PER_DATASET의 경우 밴드 하나만) 가질 것입니다. 마스크 이미지는 가능한 경우 원본 이미지와 동일한 블록 크기인, DEFLATE 압축된, 타일화 이미지일 것입니다.

:cpp:func:`GetFileList` 의 기본 구현도 .msk 파일에 관해 알 수 있도록 수정될 것입니다.

CreateCopy()
------------

필요한 것으로 보이고 가능한 경우, :cpp:func:`GDALDriver::DefaultCreateCopy` 및 :cpp:func:`GDALPamDataset::CloneInfo` 메소드가 마스크 정보를 복사하도록 업데이트할 것입니다. NODATA, ALL_VALID 및 ALPHA 유형의 마스크는 그저 파생된 정보일 뿐이기 때문에 복사하지 않는다는 사실을 기억하십시오.

알파 밴드
---------

데이터셋에 일반 GDT_Byte 알파(투명도) 밴드가 존재하고 적용되는 경우, NULL 마스크를 반환해야 하지만 :cpp:func:`GetMaskFlags` 메소드는 GMF_ALPHA 플래그를 포함해야 합니다. 몇몇 알고리즘들이 1에서 254 사이의 값들을 부분적으로 투명하다고 취급할 것이긴 하지만, 처리 목적을 위해 0이 아닌 다른 모든 값을 무결한 데이터로 취급해야 합니다.

업데이트된 드라이버
-------------------

다음 드라이버들을 업데이트할 것입니다:

-  JPEG 드라이버:
   몇몇 데이터 제공자가 사용하는 "파일에 추가된 Zlib 압축 마스크" 접근법을 지원할 것입니다.

-  GRASS 드라이버:
   NULL 값들을 마스크로 처리할 수 있도록 업데이트할 것입니다.

다음 드라이버들을 업데이트할 수도 있습니다:

-  HDF4 드라이버: 
   방법을 알아낼 수 있다면 이 드라이버가 실제 마스크를 반환하도록 업데이트할 수도 있습니다.

-  SDE 드라이버:
   하워드 버틀러가 충분한 시간과 열정을 가지고 있다면 이 드라이버를 업데이트할 수도 있습니다.

유틸리티
--------

gdalwarp 유틸리티와 GDAL 왜곡기(warper) 알고리즘이 NULL 마스크를 입력받을 수 있도록 업데이트할 것입니다. 왜곡기 알고리즘은 이미 내부에서 이 모델을 실질적으로 사용하고 있습니다. 현재 gdalwarp 산출물은 (NODATA 또는 알파 밴드는) 변경되지 않은 채 유지될 것이지만, 향후 어느 시점에 명확하게 NULL 마스크를 생성하기 위한 지원이 추가될 수도 있습니다. 그러나 대부분의 사용례에서, 알파 밴드를 생성한다는 것은 곧 NULL 마스크를 생성한다는 것입니다.

구현 계획
---------

프랑크 바르메르담이 GDAL/OGR 1.5.0 배포판을 위해 '트렁크'에 이 변경 사항을 구현할 것입니다.

SWIG 구현
---------

드라이버에 대한 :cpp:func:`GetMaskBand`, :cpp:func:`GetMaskFlags` 및 :cpp:func:`CreateMaskBand` 메소드를 (그리고 대응하는 정의들을) 추가해야 할 것입니다. 마스크가 SWIG 목적을 위해 일반 래스터 밴드처럼 작동해야 하기 때문에 최소한의 특수 작업이 필요할 것입니다.

테스트
------

:file:`gdalautotest` 를 다음으로 확장할 것입니다:

-  :file:`gcore/mask.py`:
   NODATA, 알파 및 모든 무결한 사례에 대해 기본 마스크 구현을 테스트합니다.
   
-  :file:`gdriver/jpeg.py`:
   "추가 비트마스크(appended bitmask)" 사례에 대한 -- 생성 및 읽기 -- 테스트로 확장합니다.

gdalwarp에 대한 대화형 작업 테스트를 수행할 것입니다.

