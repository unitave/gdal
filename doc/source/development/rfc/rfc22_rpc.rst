.. _rfc-22:

================================================================================
RFC 22: RPC 지리참조 작업
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인, 구현

요약
----

이 RFC는 GDAL이 메타데이터로 표현되는 유리 다항식 계수(Rational Polynomial Coefficient)를 기반으로 하는 영상의 지리위치(geolocation) 용 추가 메커니즘을 지원해야 한다고 제안합니다.

지오아이(GeoEye) 및 디지털글로브(DigitalGlobe)의 제품을 포함하는 많은 현대 원시(raw) 위성영상 제품들이 RPC와 함께 배포됩니다. RPC는 이미지 전체에 걸쳐 지리참조에 대한 보다 체계적인 설명을 제공하고, 이론적으로 (DEM을 지정하는 경우) 정사보정(orthocorrection) 및 건물 높이 계산 같은 몇몇 3차원 작업을 가능하게 해주는 도형 보기(viewing geometry)에 대한 정보도 담고 있습니다.

RPC 도메인 메타데이터
---------------------

RPC를 가진 데이터셋은 "RPC" 도메인에 유리 다항식을 식별하기 위한 다음 데이터셋 수준 메타데이터 항목들을 포함할 것입니다:

-  ERR_BIAS: 오류 - 사선(bias). 이미지에 있는 모든 포인트의 수평 축 당 미터 단위의 RMS(Root Mean Square) 사선 오류 (알 수 없는 경우 -1.0)

-  ERR_RAND: 오류 - 임의(random). 이미지에 있는 각 포인트의 수평 축 당 미터 단위의 RMS(Root Mean Square) 임의 오류 (알 수 없는 경우 -1.0)

-  LINE_OFF: 줄 오프셋

-  SAMP_OFF: 샘플 오프셋

-  LAT_OFF: 측지 위도 오프셋

-  LONG_OFF: 측지 경도 오프셋

-  HEIGHT_OFF: 측지 높이 오프셋

-  LINE_SCALE: 줄 척도

-  SAMP_SCALE: 샘플 척도

-  LAT_SCALE: 측지 위도 척도

-  LONG_SCALE: 측지 경도 척도

-  HEIGHT_SCALE: 측지 높이 척도

-  LINE_NUM_COEFF (1-20): 줄 분자 계수(Line Numerator Coefficient). Rn 방정식의 분자에 있는 다항식에 대한 계수 20개 (공백으로 구분)

-  LINE_DEN_COEFF (1-20): 줄 분모 계수(Line Denominator Coefficient). Rn 방정식의 분모에 있는 다항식에 대한 계수 20개 (공백으로 구분)

-  SAMP_NUM_COEFF (1-20): 샘플 분자 계수(Sample Numerator Coefficient). CN 방정식의 분자에 있는 다항식에 대한 계수 20개 (공백으로 구분)

-  SAMP_DEN_COEFF (1-20): 샘플 분모 계수(Sample Denominator Coefficient). CN 방정식의 분모에 있는 다항식에 대한 계수 20개 (공백으로 구분)

이 필드들은 다음 웹페이지에 있는 GeoTIFF RPC 제안 문서로부터 직접 파생되었습니다:

`http://geotiff.maptools.org/rpc_prop.html <http://geotiff.maptools.org/rpc_prop.html>`_

LINE_OFF 및 SAMP_OFF로 표현되는 줄 및 픽셀 오프셋은 픽셀의 중심을 기준으로 합니다. (#5993 티켓)

NITF 드라이버 업데이트
----------------------

-  이 모델은 이미 RPC를 지원하지만, 기본 메타데이터 도베인 대신 RPC 도메인에 RPC들을 넣도록 수정할 것입니다.
-  디지털글로브 .RPB 파일 읽기 지원을 추가할 것입니다.
-  현재 RPC 쓰기는 지원하지 않습니다.

GeoTIFF 드라이버 업데이트
-------------------------

-  디지털글로브 .RPB 파일 읽기를 지원하도록 업그레이드할 것입니다.
-  우주 이미징(지오아이?) :file:`rpc.txt` 파일 읽기를 지원할 수도 있습니다.
-  RPC TIFF 태그 (`GeoTIFF RPC 제안 문서 <http://geotiff.maptools.org/rpc_prop.html>`_ 에 따라) 읽기 지원
-  RPC TIFF 태그 쓰기 지원
-  .RPB 파일 쓰기 지원 (RPB 값이 GDALGeoTIFF가 아니라 YES 또는 PROFILE인 경우)

GenImgProj 변환기 변경
----------------------

현재 :cpp:func:`GDALGenImgProjTransformer` 함수를 이용해서 신뢰할 수 있는 RPC 기반 왜곡 변환기(warp transformer)를 생성하는 것은 어렵습니다. 이 함수는 지리변환(geotransform)을 사용할 수 있는 경우 RPC보다 지리변환을 사용하는 것을 선호할 것이기 때문입니다. 유용한 RPC 정보를 가진 이미지들 가운데 다수는 (근사치의 또는 정확한) 지리변환도 포함합니다. 따라서 :cpp:func:`GDALCreateGenImgProjTransformer` 함수가 변환기 생성에 더 많은 옵션을 지정할 수 있도록 실용적으로 수정할 것을 제안합니다. 이 새로운 제안 함수는 다음과 같습니다:

::

   void *
   GDALCreateGenImgProjTransformer2( GDALDatasetH hSrcDS, GDALDatasetH hDstDS, 
                                     char **papszOptions );

다음 옵션들을 지원합니다:

-  SRC_SRS: 'hSrcDS'를 대체해서 사용할 WKT 공간 좌표계입니다.

-  DST_SRS: 'hDstDS'를 대체해서 사용할 WKT 공간 좌표계입니다.

-  GCPS_OK: 이 옵션의 값이 거짓인 경우 GCP를 사용하지 않을 것입니다. 기본값은 TRUE입니다.

-  MAX_GCP_ORDER:
   가능한 경우 GCP 파생 다항식에 사용할 최대 차수(order)입니다. 기본값은 GCP 개수를 기반으로 자동 선택되는 값입니다. -1로 지정하는 경우 다항식 대신 박막 스플라인(Thin Plate Spline)을 사용합니다.

-  METHOD:
   GEOTRANSFORM, GCP_POLYNOMIAL, GCP_TPS, GEOLOC_ARRAY, RPC 가운데 하나로 지정할 수도 있습니다. 소스 데이터셋 상에서 오직 하나의 지리위치 메소드만 간주하도록 강제합니다.

-  RPC_HEIGHT: RPC 계산에 사용할 고정 높이입니다.

이 새 함수가 임의 옵션 전송을 지원하지 않기 때문에 쉽게 확장될 수 없었던 예전 함수를 대체합니다. 예전 함수가 새 함수를 호출하도록 다시 구현할 것입니다.

가장 중요한 제안 사항은 METHOD 옵션으로, 코드가 가장 적절하다고 판단하는 방법을 선택하는 대신 이미지 가운데 하나를 이용해서 지리참조 좌표계 메소드를 사용하도록 지정할 수 있습니다.

gdalwarp 및 gdaltransform 변경
------------------------------

업데이트된 :cpp:func:`GDALCreateGenImgProjTransformer2` 함수에 변환기 옵션들을 쉽게 전송하기 위해, (이 함수를 대상으로 빌드된) gdalwarp 및 gdaltransform 프로그램이 '-to'(transformer option) 스위치를 포함하고 새 함수를 사용하도록 업데이트할 것입니다.

변환 과정에서 지리위치 보전하기
-------------------------------

변환 과정에서 데이터의 공간 배열(spatial arrangement)을 변경하지 않도록 RPC 정보를 복사하고 보전해야 합니다. 이를 위해 다음 코드에 RPC 메타데이터 복사 작업을 추가할 것입니다:

-  VRT 드라이버의 :cpp:func:`CreateCopy`
-  :cpp:class:`GDALDriver` 의 기본 :cpp:func:`CreateCopy`
-  :cpp:func:`GDALPamDataset::CopyInfo`
-  어떤 크기 조정 또는 부분 집합 작업도 하지 않는 경우에만 중간(intermediate) 내부 VRT에 RPC 메타데이터를 복사하도록 gdal_translate 프로그램을 업데이트할 것입니다.

RPC 변환기 변경
---------------

-  단순 선형 근사기(approximator) 대신 픽셀/줄로부터 위도/경도/높이로 변환하는 반복 "하위 변환"을 구현합니다.
-  변환기로 전송되는 모든 Z 값이 (일반적으로 신(scene)의 실질적인 평균 표고인) 이 오프셋에 상대적이라고 가정하도록 해주는 RPC_HEIGHT 오프셋 지원을 추가합니다.
-  RPC 변환기가 (VRT 파일 등에서) 직렬화될 수 있게 만듭니다.

하위 호환성 문제점
------------------

예전에는 NITF 드라이버가 기본 도메인에 RPC 메타데이터를 반환했습니다. GDAL 1.6.0에 이 RFC를 구현하면 RPC 메타데이터를 이용하는 모든 응용 프로그램이 기본 도메인이 아니라 RPC 도메인을 사용하도록 해야 할 것입니다. 메타데이터 값에 붙던 ``RPC_`` 접두어도 제거합니다.

일반화된 새 함수를 추가했기 때문에 예상되는 호환성 문제가 없도록, :cpp:func:`GDALCreateGenImgProjTransformer` 함수를 보전합니다.

SWIG 바인딩 문제점
------------------

-  확립된 메타데이터 API가 원시(raw) 접근을 수행하기 때문에, 이를 변경할 필요는 없습니다.
-  왜곡 API는 높은 수준에만 바인딩되기 때문에, 이와 관련된 변경 사항이 없어야 합니다.
-  테스트를 위해 GDAL 변환기 API를 감싸는 바인딩을 제공하는 편이 좋습니다. 다음 계획된 바인딩은 :cpp:class:`OGRCoordinateTransformation` API 바인딩에 느슨하게 기반을 두고 있습니다. 지금까지 파이썬에서 ``TransformPoint( bDstToSrc, x, y, z )`` 진입점(entry point)이 유용하다는 사실을 발견했는데, 이조차도 다소 불편한 ``(bSuccess, (x, y, z))`` 결과값을 반환하게 되었습니다. 이를 더 훌륭하게 수행할 방법이 있을까요?

::

   /************************************************************************/
   /*                         변환기(Transformer)                          */
   /************************************************************************/

   %rename (Transformer) GDALTransformerInfoShadow;
   class GDALTransformerInfoShadow {
   private:
     GDALTransformerInfoShadow();
   public:
   %extend {

     GDALTransformerInfoShadow( GDALDatasetShadow *src, GDALDatasetShadow *dst,
                                char **options ) {
       GDALTransformerInfoShadow *obj = (GDALTransformerInfoShadow*) 
          GDALCreateGenImgProjTransformer2( (GDALDatasetH)src, (GDALDatasetH)dst, 
                                            options );
       return obj;
     }

     ~GDALTransformerInfoShadow() {
       GDALDestroyTransformer( self );
     }

   // argout의 numinputs=0 버전 대신 numinputs=1 버전이 적용되도록
   // argin typemap을 두 번째로 적용해야 합니다.
   %apply (double argout[ANY]) {(double inout[3])};
   %apply (double argin[ANY]) {(double inout[3])};
     int TransformPoint( int bDstToSrc, double inout[3] ) {
       int nRet, nSuccess = TRUE;

       nRet = GDALUseTransformer( self, bDstToSrc, 
                                  1, &inout[0], &inout[1], &inout[2], 
                                  &nSuccess );

       return nRet && nSuccess;
     }
   %clear (double inout[3]);

     int TransformPoint( double argout[3], int bDstToSrc, 
                         double x, double y, double z = 0.0 ) {
       int nRet, nSuccess = TRUE;
       
       argout[0] = x;
       argout[1] = y;
       argout[2] = z;
       nRet = GDALUseTransformer( self, bDstToSrc, 
                                  1, &argout[0], &argout[1], &argout[2], 
                                  &nSuccess );

       return nRet && nSuccess;
     }
     
   #ifdef SWIGCSHARP
     %apply (double *inout) {(double*)};
     %apply (double *inout) {(int*)};
   #endif
     int TransformPoints( int bDstToSrc, 
                          int nCount, double *x, double *y, double *z,
                          int *panSuccess ) {
       int nRet;

       nRet = GDALUseTransformer( self, bDstToSrc, nCount, x, y, z, panSuccess );

       return nRet;
     }
   #ifdef SWIGCSHARP
     %clear (double*);
     %clear (int*);
   #endif

   } /*확장됨*/
   };

문서화
------

표준 API 문서는 물론, "GDAL 데이터 모델" 문서에도 RPC 메타데이터 메커니즘을 작성할 것입니다.

구현
----

프랑크 바르메르담이 캐나다 원자력 안전 위원회의 후원으로 이 작업을 구현할 것입니다.

테스트
------

-  RPC, GCP_TPS, GCP_POLYNOMIAL, GEOLOC 및 GEOTRANSFORM을 커버하는 변환기 API에 대한 테스트 스크립트를 구현할 것입니다.
-  RPB 및 GeoTIFF RPC 태그들의 읽기 및 쓰기를 테스트하는 스크립트를 작성할 것입니다.

