.. _rfc-59.1:

=======================================================================================
RFC 59.1 : GDAL/OGR 유틸리티를 라이브러리로
=======================================================================================

저자: 파자 마하무드, 이벤 루올

연락처: fazamhd@gmail.com, even.rouault@spatialys.com

상태: 승인, GDAL 2.1버전에 구현

요약
----

이 RFC는 GDAL/OGR C/C++ 유틸리티를 C 호출 가능 함수로 노출시키는 방법을 정의합니다. 유틸리티 코드가 새 함수를 호출할 수 있도록 수정합니다. 이 RFC는 몇몇 유틸리티를 통해 시연되지만, 다른 유틸리티들로 확장되는 것을 목표로 하는 일반 프레임과 원칙을 제공합니다.

근거
----

인메모리 데이터셋에 대해 작업할 수 있고 진행 상황/취소 콜백 함수를 이용할 수 있도록, 시스템 호출 사용을 수반하지 않고 코드로부터 GDAL 유틸리티를 호출해야 할 필요가 있습니다.

변경 사항
---------

GDAL 유틸리티의 공개 선언을 담고 있는 :file:`gdal_utils.h` 공개 헤더 파일을 생성합니다. (아직 진행 중인) 현재 헤더는 `여기 <https://github.com/rouault/gdal2/blob/rfc59.1/gdal/apps/gdal_utils.h>`_ 에서 찾아볼 수 있습니다.

각 유틸리티는 문자열 배열로 지정되는 인자들로부터 옵션 구조를 생성하는 함수(XXXXOptionsNew)를 가지고 있습니다. 이 함수는 명령줄 유틸리티 자체의 코드와 협력하기 위해 사용되는 추가적인 반공개(semi-private) 구조도 인자로 받아들입니다.

GDALInfo()의 경우:

::

   /*! GDALInfo() 용 옵션. 불투명 유형입니다. */
   typedef struct GDALInfoOptions GDALInfoOptions;
   typedef struct GDALInfoOptionsForBinary GDALInfoOptionsForBinary;

   /**
    * GDALInfoOptions 구조를 할당합니다.
    *
    * @param papszArgv NULL로 종료되는 옵션 목록입니다. (파일명 및 열기 옵션도 포함할 수 있습니다.)
    *                  gdalinfo 유틸리티의 옵션을 받아들입니다.
    * @param psOptionsForBinary (산출물) NULL일 수 있으며 (일반적으로 NULL이어야 합니다)
    *                           그렇지 않은 경우 (gdalinfo_bin.cpp 사용례) 이 함수 이전에
    *                           GDALInfoOptionsForBinaryNew()로 할당해야만 합니다. 존재할 수 있는
    *                           파일명, 열기 옵션, 하위 데이터셋 번호 등등으로 채워질 것입니다.
    * @return 할당된 GDALInfoOptions 구조를 가리키는 포인터를 반환합니다.
    *
    * @since GDAL 2.1
    */
   GDALInfoOptions CPL_DLL *GDALInfoOptionsNew(char** papszArgv, GDALInfoOptionsForBinary* psOptionsForBinary);

   void CPL_DLL GDALInfoOptionsFree( GDALInfoOptions *psOptions );

   /**
    * GDAL 지원 래스터 데이터셋에 관한 다양한 정보를 목록화합니다.
    *
    * GDALInfoOptionsNew()로 GDALInfoOptions* 를 할당하고
    * GDALInfoOptionsFree()로 할당 해제해야만 합니다.
    *
    * @param hDataset 데이터셋 핸들입니다.
    * @param psOptions GDALInfoOptionsNew()가 반환하는 옵션 구조 또는 NULL입니다.
    * @return 래스터 데이터셋에 관한 정보에 해당하는 문자열을 반환합니다.
    * CPLFree()로 해제해야만 합니다.
    *
    * @since GDAL 2.1
    */
   char CPL_DLL *GDALInfo( GDALDatasetH hDataset, const GDALInfoOptions *psOptions );

GDALTranslate()의 경우도 마찬가지입니다:

::

   /*! GDALTranslate() 용 옵션. 불투명 유형입니다. */
   typedef struct GDALTranslateOptions GDALTranslateOptions;
   typedef struct GDALTranslateOptionsForBinary GDALTranslateOptionsForBinary;

   GDALTranslateOptions CPL_DLL *GDALTranslateOptionsNew(char** papszArgv,
                                                         GDALTranslateOptionsForBinary* psOptionsForBinary);

   void CPL_DLL GDALTranslateOptionsFree( GDALTranslateOptions *psOptions );

   void CPL_DLL GDALTranslateOptionsSetProgress( GDALTranslateOptions *psOptions,
                                                 GDALProgressFunc pfnProgress,
                                                 void *pProgressData );

   GDALDatasetH CPL_DLL GDALTranslate(const char *pszDestFilename,
                                      GDALDatasetH hSrcDataset,
                                      const GDALTranslateOptions *psOptions,
                                      int *pbUsageError);

GDALWarp()의 경우도 마찬가지입니다:

::

   /*! GDALWarp() 용 옵션. 불투명 유형입니다. */
   typedef struct GDALWarpAppOptions GDALWarpAppOptions;

   typedef struct GDALWarpAppOptionsForBinary GDALWarpAppOptionsForBinary;

   GDALWarpAppOptions CPL_DLL *GDALWarpAppOptionsNew(char** papszArgv,
                                                         GDALWarpAppOptionsForBinary* psOptionsForBinary);

   void CPL_DLL GDALWarpAppOptionsFree( GDALWarpAppOptions *psOptions );

   void CPL_DLL GDALWarpAppOptionsSetProgress( GDALWarpAppOptions *psOptions,
                                                 GDALProgressFunc pfnProgress,
                                                 void *pProgressData );
   void CPL_DLL GDALWarpAppOptionsSetWarpOption( GDALWarpAppOptions *psOptions,
                                                 const char* pszKey,
                                                 const char* pszValue );

   GDALDatasetH CPL_DLL GDALWarp( const char *pszDest, GDALDatasetH hDstDS, int nSrcCount,
                                  GDALDatasetH *pahSrcDS,
                                  const GDALWarpAppOptions *psOptions, int *pbUsageError );

GDALVectorTranslate()의 경우도 마찬가지입니다(ogr2ogr와 동등합니다):

::

   /*! GDALVectorTranslate() 용 옵션. 불투명 유형입니다. */
   typedef struct GDALVectorTranslateOptions GDALVectorTranslateOptions;

   typedef struct GDALVectorTranslateOptionsForBinary GDALVectorTranslateOptionsForBinary;

   GDALVectorTranslateOptions CPL_DLL *GDALVectorTranslateOptionsNew(char** papszArgv,
                                                         GDALVectorTranslateOptionsForBinary* psOptionsForBinary);

   void CPL_DLL GDALVectorTranslateOptionsFree( GDALVectorTranslateOptions *psOptions );

   void CPL_DLL GDALVectorTranslateOptionsSetProgress( GDALVectorTranslateOptions *psOptions,
                                                 GDALProgressFunc pfnProgress,
                                                 void *pProgressData );

   GDALDatasetH CPL_DLL GDALVectorTranslate( const char *pszDest, GDALDatasetH hDstDS, int nSrcCount,
                                  GDALDatasetH *pahSrcDS,
                                  const GDALVectorTranslateOptions *psOptions, int *pbUsageError );

다른 유틸리티에 대해서는 `gdal_utils.h <https://svn.osgeo.org/gdal/trunk/gdal/apps/gdal_utils.h>`_ 를 참조하십시오.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

모든 바인딩
~~~~~~~~~~~

모든 바인딩에 대해, SWIG에 앞의 함수들을 다음과 같이 매핑합니다:

::


   struct GDALInfoOptions {
   %extend {
       GDALInfoOptions(char** options) {
           return GDALInfoOptionsNew(options, NULL);
       }

       ~GDALInfoOptions() {
           GDALInfoOptionsFree( self );
       }
   }
   };

   %rename (InfoInternal) GDALInfo;
   char *GDALInfo( GDALDatasetShadow *hDataset, GDALInfoOptions *infoOptions );

::

   struct GDALTranslateOptions {
   %extend {
       GDALTranslateOptions(char** options) {
           return GDALTranslateOptionsNew(options, NULL);
       }

       ~GDALTranslateOptions() {
           GDALTranslateOptionsFree( self );
       }
   }
   };

   %rename (TranslateInternal) wrapper_GDALTranslate;
   %newobject wrapper_GDALTranslate;

   %inline %{
   GDALDatasetShadow* wrapper_GDALTranslate( const char* dest,
                                         GDALDatasetShadow* dataset,
                                         GDALTranslateOptions* translateOptions,
                                         GDALProgressFunc callback=NULL,
                                         void* callback_data=NULL);

::

   struct GDALWarpAppOptions {
   %extend {
       GDALWarpAppOptions(char** options) {
           return GDALWarpAppOptionsNew(options, NULL);
       }

       ~GDALWarpAppOptions() {
           GDALWarpAppOptionsFree( self );
       }
   }
   };

   /* 주의: SWIG에 "int object_list_count, GDALDatasetShadow** poObjects" 입력 유형 매핑과 잘 */
   /* 동작하지 않는 버그/기능이 있기 때문에 2개의 개별 이름을 사용해야만 합니다 */

   %inline %{
   int wrapper_GDALWarpDestDS( GDALDatasetShadow* dstDS,
                               int object_list_count, GDALDatasetShadow** poObjects,
                               GDALWarpAppOptions* warpAppOptions,
                               GDALProgressFunc callback=NULL,
                               void* callback_data=NULL),
   %}

   %newobject wrapper_GDALWarpDestName;

   %inline %{
   GDALDatasetShadow* wrapper_GDALWarpDestName( const char* dest,
                                                int object_list_count, GDALDatasetShadow** poObjects,
                                                GDALWarpAppOptions* warpAppOptions,
                                                GDALProgressFunc callback=NULL,
                                                void* callback_data=NULL),
   %}

::


   struct GDALVectorTranslateOptions {
   %extend {
       GDALVectorTranslateOptions(char** options) {
           return GDALVectorTranslateOptionsNew(options, NULL);
       }

       ~GDALVectorTranslateOptions() {
           GDALVectorTranslateOptionsFree( self );
       }
   }
   };

   /* 주의: SWIG에 "int object_list_count, GDALDatasetShadow** poObjects" 입력 유형 매핑과 잘 */
   /* 동작하지 않는 버그/기능이 있기 때문에 2개의 개별 이름을 사용해야만 합니다 */

   %inline %{
   int wrapper_GDALVectorTranslateDestDS( GDALDatasetShadow* dstDS,
                                          GDALDatasetShadow* srcDS,
                               GDALVectorTranslateOptions* options,
                               GDALProgressFunc callback=NULL,
                               void* callback_data=NULL);
   %}

   %newobject wrapper_GDALVectorTranslateDestName;

   %inline %{
   GDALDatasetShadow* wrapper_GDALVectorTranslateDestName( const char* dest,
                                                GDALDatasetShadow* srcDS,
                                                GDALVectorTranslateOptions* options,
                                                GDALProgressFunc callback=NULL,
                                                void* callback_data=NULL);
   %}

다른 유틸리티에 대해서는 `gdal.i <https://svn.osgeo.org/gdal/trunk/gdal/swig/python/gdal.i>`_ 를 참조하십시오.

파이썬 바인딩
~~~~~~~~~~~~~

파이썬 바인딩의 경우, 좀 더 사용자 친화적인 방법으로 옵션을 지정할 수 있게 해주는 편이 래퍼(convenience wrapper)를 생성합니다.

::

   def InfoOptions(options = [], format = 'text', deserialize = True,
            computeMinMax = False, reportHistograms = False, reportProj4 = False,
            stats = False, approxStats = False, computeChecksum = False,
            showGCPs = True, showMetadata = True, showRAT = True, showColorTable = True,
            listMDD = False, showFileList = True, allMetadata = False,
            extraMDDomains = None):
       """ gdal.Info() 옵션으로 전송할 수 있는 InfoOptions() 객체를 생성합니다. 이 객체는
           문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다."""


   def Info(ds, **kwargs):
       """ 데이터셋에 대한 정보를 반환합니다.
           인자:
             ds --- 데이터셋 객체 또는 파일명
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.InfoOptions()의 다른 키워드 인자들
           옵션을 gdal.InfoOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

gdal.InfoOptions()의 속성을 설정하는 데 또는 gdal.Info()의 그때 그때 즉석에서 처리되는(inline) 인자로 gdal.Info()를 사용할 수 있습니다. 인자를 문자열 배열, 명령줄 문법 또는 전용 키워드로 지정할 수 있기 때문에, 다양하게 조합할 수 있습니다:

::

       options = gdal.InfoOptions(format = 'json', computeChecksum = True)
       gdal.Info(ds, options)

::

       options = gdal.InfoOptions(options = ['-json', '-checksum'])
       gdal.Info(ds, options)

::

       options = gdal.InfoOptions(options = '-json -checksum')
       gdal.Info(ds, options)

::

       gdal.Info(ds, format = 'json', computeChecksum = True)

::

       gdal.Info(ds, options = ['-json', '-checksum'])

::

       gdal.Info(ds, options = '-json -checksum')

::

   def TranslateOptions(options = [], format = 'GTiff',
                 outputType = GDT_Unknown, bandList = None, maskBand = None,
                 width = 0, height = 0, widthPct = 0.0, heightPct = 0.0,
                 xRes = 0.0, yRes = 0.0,
                 creationOptions = None, srcWin = None, projWin = None, projWinSRS = None, strict = False,
                 unscale = False, scaleParams = None, exponents = None,
                 outputBounds = None, metadataOptions = None,
                 outputSRS = None, GCPs = None,
                 noData = None, rgbExpand = None,
                 stats = False, rat = True, resampleAlg = None,
                 callback = None, callback_data = None):
       """ gdal.Translate()로 전송할 수 있는 TranslateOptions() 객체를 생성합니다.
           키워드 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("GTiff" 등등)
             outputType --- 산출물 유형 (gdal.GDT_Byte 등등)
             bandList --- 밴드 번호 배열 (1에서 시작하는 색인)
             maskBand --- 생성하거나 생성하지 않을 마스크 밴드 ("none", "auto", "mask", 1, ...)
             width --- 산출 래스터의 픽셀 단위 너비
             height --- 산출 래스터의 픽셀 단위 높이
             widthPct --- 산출 래스터의 백분율 너비 (100 = 원래 너비)
             heightPct --- 산출 래스터의 백분율 높이 (100 = 원래 높이)
             xRes --- 산출물의 수평 해상도
             yRes --- 산출물의 수직 해상도
             creationOptions --- 생성 옵션 목록
             srcWin --- 추출할 픽셀 단위 하위 창: [left_x, top_y, width, height]
             projWin --- 추출할 투영 좌표 단위 하위 창: [ulx, uly, lrx, lry]
             projWinSRS --- projWin을 표현하는 공간 좌표계
             strict --- 엄격 모드
             unscale --- 척도 및 오프셋 메타데이터를 가진 비척도(unscale) 값
             scaleParams --- 각각 [src_min,src_max] 또는 [src_min,src_max,dst_min,dst_max] 형식의 척도 파라미터 목록
             exponents --- 지수(exponentiation) 파라미터 목록
             outputBounds ---할당된 산출물 경계: [ulx, uly, lrx, lry]
             metadataOptions --- 메타데이터 옵션 목록
             outputSRS --- 할당된 산출 공간 좌표계
             GCPs --- GCP 목록
             noData --- NODATA 값 (또는 설정 해제하려면 "none")
             rgbExpand --- 색상표 확장 모드: "gray", "rgb", "rgba"
             stats --- 통계 계산 여부
             rat --- 소스 RAT 작성 여부
             resampleAlg --- 리샘플링 모드
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def Translate(destName, srcDS, **kwargs):
       """ 데이터셋을 변환합니다.
           인자:
             destName --- 산출 데이터셋 이름
             srcDS --- 데이터셋 객체 또는 파일명
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.TranslateOptions()의 다른 키워드 인자들
           옵션을 gdal.TranslateOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::


   def WarpOptions(options = [], format = 'GTiff', 
            outputBounds = None,
            outputBoundsSRS = None,
            xRes = None, yRes = None, targetAlignedPixels = False,
            width = 0, height = 0,
            srcSRS = None, dstSRS = None,
            srcAlpha = False, dstAlpha = False, 
            warpOptions = None, errorThreshold = None,
            warpMemoryLimit = None, creationOptions = None, outputType = GDT_Unknown,
            workingType = GDT_Unknown, resampleAlg = None,
            srcNodata = None, dstNodata = None, multithread = False,
            tps = False, rpc = False, geoloc = False, polynomialOrder = None,
            transformerOptions = None, cutlineDSName = None,
            cutlineLayer = None, cutlineWhere = None, cutlineSQL = None, cutlineBlend = None, cropToCutline = False,
            copyMetadata = True, metadataConflictValue = None,
            setColorInterpretation = False,
            callback = None, callback_data = None):
       """ gdal.Warp()로 전송할 수 있는 WarpOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("GTiff" 등등)
             outputBounds --- 대상 공간 좌표계 단위 (minX, minY, maxX, maxY)의 산출물 경계
             outputBoundsSRS --- dstSRS에 표현되지 않은 경우 산출물 경계를 표현하는 공간 좌표계
             xRes, yRes --- 대상 공간 좌표계 단위 산출물 해상도
             targetAlignedPixels --- 산출물 경계를 산출물 해상도의 배수로 강제할지 여부
             width --- 산출 래스터의 픽셀 단위 너비
             height --- 산출 래스터의 픽셀 단위 높이
             srcSRS --- 소스 공간 좌표계
             dstSRS --- 산출 공간 좌표계
             srcAlpha --- 입력 데이터셋의 마지막 밴드를 강제로 알파 밴드로 간주할지 여부
             dstAlpha --- 산출물에 알파 밴드를 강제 생성할지 여부
             outputType --- 산출물 유형 (gdal.GDT_Byte 등등)
             workingType --- 작업 유형 (gdal.GDT_Byte 등등)
             warpOptions --- 왜곡 옵션 목록
             errorThreshold --- 근사치 변환기 용 오류 한계값 (픽셀 단위)
             warpMemoryLimit --- 작업 버퍼의 바이트 단위 용량
             resampleAlg --- 리샘플링 모드
             creationOptions --- 생성 옵션 목록
             srcNodata --- 소스 NODATA 값(들)
             dstNodata --- 산출 NODATA 값(들)
             multithread --- 멀티스레드 계산 및 I/O 작업 여부
             tps --- 박막 스플라인 GCP 변환 사용 여부
             rpc --- RPC 변환기 사용 여부
             geoloc --- 지리위치(GeoLocation) 배열 변환기 사용 여부
             polynomialOrder --- 다항 GCP 보간 순서
             transformerOptions --- 변환기 옵션 목록
             cutlineDSName --- 설명문(cutline) 데이터셋 이름
             cutlineLayer --- 설명문 레이어 이름
             cutlineWhere --- 설명문 WHERE 절
             cutlineSQL --- 설명문 SQL 선언문
             cutlineBlend --- 픽셀 단위 설명문 혼합(blend) 거리
             cropToCutline --- 산출 밴드에 설명문 범위를 사용할지 여부
             copyMetadata --- 소스 메타데이터를 복사할지 여부
             metadataConflictValue --- 메타데이터 데이터 충돌 값
             setColorInterpretation --- 입력 밴드의 색상 해석을 산출 밴드에 강제할지 여부
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def Warp(destNameOrDestDS, srcDSOrSrcDSTab, **kwargs):
       """ 하나 이상의 데이터셋을 왜곡합니다.
           인자:
             destNameOrDestDS --- 산출 데이터셋 이름 또는 객체
             srcDSOrSrcDSTab --- 데이터셋 객체 또는 파일명 배열, 또는 데이터셋 객체 또는 파일명
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.WarpOptions()의 다른 키워드 인자들
           옵션을 gdal.WarpOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::


   def VectorTranslateOptions(options = [], format = 'ESRI Shapefile', 
            accessMode = None,
            srcSRS = None, dstSRS = None, reproject = True,
            SQLStatement = None, SQLDialect = None, where = None, selectFields = None, spatFilter = None,
            datasetCreationOptions = None,
            layerCreationOptions = None,
            layers = None,
            layerName = None,
            geometryType = None,
            segmentizeMaxDist= None,
            callback = None, callback_data = None):
       """ gdal.VectorTranslate()로 전송할 수 있는 VectorTranslateOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("ESRI Shapefile" 등등)
             accessMode --- 생성 시 설정하지 않음, 'update', 'append', 'overwrite'
             srcSRS --- 소스 공간 좌표계
             dstSRS --- 산출 공간 좌표계 (reproject = True이면 재투영)
             reproject --- 재투영할지 여부
             SQLStatement --- 소스 데이터셋에 적용할 SQL 선언문
             SQLDialect --- SQL 방언 ('OGRSQL', 'SQLITE', ...)
             where --- 소스 레이어(들)에 적용할 WHERE 절
             selectFields --- 선택할 필드 목록
             spatFilter --- (minX, minY, maxX, maxY) 경계 상자 형식의 공간 필터
             datasetCreationOptions --- 데이터셋 생성 옵션 목록
             layerCreationOptions --- 레이어 생성 옵션 목록
             layers --- 변환할 레이어 목록
             layerName --- 산출 레이어 이름
             geometryType --- 산출 레이어 도형 유형 ('POINT', ....)
             segmentizeMaxDist --- 라인 도형의 연속하는 노드들 사이의 최대 거리
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def VectorTranslate(destNameOrDestDS, srcDS, **kwargs):
       """ 벡터 데이터셋 하나를 변환합니다.
           인자:
             destNameOrDestDS --- 산출 데이터셋 이름 또는 객체
             srcDS --- 데이터셋 객체 하나 또는 파일명 하나
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.VectorTranslateOptions()의 다른 키워드 인자들
           옵션을 gdal.VectorTranslateOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::


   def DEMProcessingOptions(options = [], colorFilename = None, format = 'GTiff',
                 creationOptions = None, computeEdges = False, alg = 'Horn', band = 1,
                 zFactor = None, scale = None, azimuth = None, altitude = None, combined = False,
                 slopeFormat = None, trigonometric = False, zeroForFlat = False,
                 callback = None, callback_data = None):
       """ gdal.DEMProcessing()으로 전송할 수 있는 DEMProcessingOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             colorFilename --- ("color-relief"의 경우 필수) "color-relief" 처리를 위한 색상표 정의를 담고 있는 파일의 이름
             format --- 산출물 포맷 ("GTiff" 등등)
             creationOptions --- 생성 옵션 목록
             computeEdges --- 래스터 경계에 있는 값을 계산할지 여부
             alg --- 'ZevenbergenThorne' 또는 'Horn'
             band --- 사용할 소스 밴드 번호
             zFactor --- (음영기복 전용) 표고를 사전에 곱하기 위해 사용하는 수직 과장
             scale --- 수직 단위와 수평 단위의 비율
             azimuth --- (음영기복 전용) 광원의 도 단위 방위각입니다. 래스터 위에서 수직으로 빛이 내리쬐는 경우 0, 동쪽인 경우 90, ... 기본값은 315로, 음영도 생성 시 일반적으로 쓰이는 값이기 때문에 변경할 필요가 거의 없습니다.
             altitude ---(음영기복 전용) 광원의 도 단위 고도입니다. DEM 위에서 수직으로 빛이 내리쬐는 경우 90, 지평선(수평선)인 경우 0입니다.
             combined --- (음영기복 전용) 경사와 비스듬한 음영을 조합하는 결합 음영을 계산할지 여부
             slopeformat --- (경사 전용) "degree" 또는 "percent"
             trigonometric --- (경사방향 전용) 방위각 대신 삼각법 각도(trigonometric angle)를 반환할지 여부를 설정합니다. 즉 0deg는 동쪽, 90deg는 북쪽, 180deg는 서쪽, 270deg는 남쪽입니다.
             zeroForFlat --- (경사방향 전용) 평지 지역에 대해 slope=-9999가 아니라 slope=0으로 반환할지 여부
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def DEMProcessing(destName, srcDS, processing, **kwargs):
       """ DEM 처리를 적용합니다.
           인자:
             destName --- 산출 데이터셋 이름
             srcDS --- 데이터셋 객체 하나 또는 파일명 하나
             processing --- "hillshade", "slope", "aspect", "color-relief", "TRI", "TPI", "Roughness" 가운데 하나
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.DEMProcessingOptions()의 다른 키워드 인자들
           옵션을 gdal.DEMProcessingOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::

   def NearblackOptions(options = [], format = 'GTiff', 
            creationOptions = None, white = False, colors = None,
            maxNonBlack = None, nearDist = None, setAlpha = False, setMask = False,
            callback = None, callback_data = None):
       """ gdal.Nearblack()으로 전송할 수 있는 NearblackOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("GTiff" 등등)
             creationOptions --- 생성 옵션 목록
             white --- 근사 검은색 픽셀 대신 근사 하얀색(255) 픽셀을 검색할지 여부
             colors --- 예를 들면 ((0,0,0),(255,255,255)) 같은 형식의 검색할 색상 목록입니다. 색상으로 간주하는 픽셀은 0으로 설정됩니다.
             maxNonBlack --- 안쪽으로의 검색을 포기하기 전에 발견할 수 있는 검은색이 아닌 (또는 white, colors로 지정한 다른 검색 색상이 아닌) 픽셀의 최대 개수입니다. 기본값은 2입니다.
             nearDist --- 픽셀값이 검은색/하얀색/사용자 지정 색상으로 간주되려면 검은색/하얀색/사용자 지정 색상과 얼마나 다를 수 있는지 선택합니다. 기본값은 15입니다.
             setAlpha --- 산출 파일이 지원하는 경우 알파 밴드를 추가합니다.
             setMask --- 산출 파일에 마스크 밴드를 추가합니다.
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def Nearblack(destNameOrDestDS, srcDS, **kwargs):
       """ 근사 검은색/하얀색 경계를 정확한 값으로 변환합니다.
           인자:
             destNameOrDestDS --- 산출 데이터셋 이름 또는 객체
             srcDS --- 데이터셋 객체 하나 또는 파일명 하나
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.NearblackOptions()의 다른 키워드 인자들
           옵션을 gdal.NearblackOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::

   def GridOptions(options = [], format = 'GTiff',
                 outputType = GDT_Unknown,
                 width = 0, height = 0,
                 creationOptions = None,
                 outputBounds = None,
                 outputSRS = None,
                 noData = None,
                 algorithm = None,
                 layers = None,
                 SQLStatement = None,
                 where = None,
                 spatFilter = None,
                 zfield = None,
                 z_increase = None,
                 z_multiply = None,
                 callback = None, callback_data = None):
       """ gdal.Grid()로 전송할 수 있는 GridOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("GTiff" 등등)
             outputType --- 산출물 유형 (gdal.GDT_Byte 등등)
             width --- 산출 래스터의 픽셀 단위 너비
             height --- 산출 래스터의 픽셀 단위 높이
             creationOptions --- 생성 옵션 목록
             outputBounds ---할당된 산출물 경계: [ulx, uly, lrx, lry]
             outputSRS --- 할당된 산출 공간 좌표계
             noData --- NODATA 값
             algorithm --- 예: "invdist:power=2.0:smoothing=0.0:radius1=0.0:radius2=0.0:angle=0.0:max_points=0:min_points=0:nodata=0.0"
             layers --- 변환할 레이어 목록
             SQLStatement --- 소스 데이터셋에 적용할 SQL 선언문
             where --- 소스 레이어(들)에 적용할 WHERE 절
             spatFilter --- (minX, minY, maxX, maxY) 경계 상자 형식의 공간 필터
             zfield --- Z 값을 가져오기 위해 사용할 피처에 있는 속성 필드를 식별합니다. 이 값은 피처 도형 레코드에서 읽어온 Z 값을 대체합니다.
             z_increase --- Z 값을 가져오기 위해 사용할 피처에 있는 속성 필드에 추가할 값입니다. 이 값의 단위는 Z 값의 단위와 동일해야 합니다. 결과값은 Z 값 + Z 증가 값입니다. 기본값은 0입니다.
             z_multiply --- Z 필드에 대한 곱셈 비율입니다. 예를 들어 피트 단위를 미터 단위로 또는 표고 값을 심도 값으로 변환하기 위해 사용할 수 있습니다. 결과값은 (Z 값 + Z 증가 값) * Z 곱셈 값이 됩니다. 기본값은 1입니다.
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def Grid(destName, srcDS, **kwargs):
       """ 분산 데이터로부터 래스터를 생성합니다.
           인자:
             destName --- 산출 데이터셋 이름
             srcDS --- 데이터셋 객체 하나 또는 파일명 하나
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.GridOptions()의 다른 키워드 인자들
           옵션을 gdal.GridOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::

   def RasterizeOptions(options = [], format = None, 
            creationOptions = None, noData = None, initValues = None,
            outputBounds = None, outputSRS = None,
            width = None, height = None,
            xRes = None, yRes = None, targetAlignedPixels = False,
            bands = None, inverse = False, allTouched = False,
            burnValues = None, attribute = None, useZ = False, layers = None,
            SQLStatement = None, SQLDialect = None, where = None,
            callback = None, callback_data = None):
       """ gdal.Rasterize()로 전송할 수 있는 RasterizeOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             format --- 산출물 포맷 ("GTiff" 등등)
             creationOptions --- 생성 옵션 목록
             outputBounds ---할당된 산출물 경계: [minx, miny, maxx, maxy]
             outputSRS --- 할당된 산출 공간 좌표계
             width --- 산출 래스터의 픽셀 단위 너비
             height --- 산출 래스터의 픽셀 단위 높이
             xRes, yRes --- 대상 공간 좌표계 단위 산출물 해상도
             targetAlignedPixels --- 산출물 경계를 산출물 해상도의 배수로 강제할지 여부
             noData --- NODATA 값
             initValues --- 산출 이미지 밴드를 사전 초기화하기 위해 사용할 값 또는 값 목록입니다. 하지만, 산출 파일에서 NODATA 값으로 표시되지는 않습니다. 값을 하나만 지정하는 경우, 모든 밴드에 동일한 값을 사용합니다.
             bands --- 값을 작성할 산출 밴드 목록입니다.
             inverse --- 역 래스터화할지 여부. 예를 들어 고정 작성값을 작성할지 또는 지정한 폴리곤의 내부가 아니라 이미지의 모든 부분에 첫 번째 피처와 연결된 값을 작성할지 여부를 설정합니다.
             allTouched --- ALL_TOUCHED 래스터화 옵션을 활성화해서, 라인을 렌더링한 경로 상에 있는 또는 중심 포인트가 폴리곤 내부에 떨어지는 픽셀만이 아니라 라인 또는 폴리곤에 접하는 모든 픽셀을 업데이트할지 여부
             burnValues --- 모든 객체의 각 밴드에 작성할 고정 값 목록입니다. attribute와 함께 사용할 수 없습니다.
             attribute --- 작성할 값을 위해 사용할 피처에 있는 속성 필드를 식별합니다. 모든 산출 밴드에 값을 작성할 것입니다. burnValues와 함께 사용할 수 없습니다.
             useZ --- 작성 값을 피처의 "Z" 값으로부터 추출해야 할지 여부를 나타냅니다. burnValues 또는 attribute를 지정한 경우 burnValues 또는 attribute로 설정한 작성 값에 이 값을 추가합니다. 현재로서는 포인트 및 라인만 3차원으로 그립니다.
             layers --- 입력 피처에 대해 사용할 데이터소스의 레이어 목록입니다.
             SQLStatement --- 소스 데이터셋에 적용할 SQL 선언문
             SQLDialect --- SQL 방언 ('OGRSQL', 'SQLITE', ...)
             where --- 소스 레이어(들)에 적용할 WHERE 절
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def Rasterize(destNameOrDestDS, srcDS, **kwargs):
       """ 래스터에 벡터 도형을 작성합니다.
           인자:
             destNameOrDestDS --- 산출 데이터셋 이름 또는 객체
             srcDS --- 데이터셋 객체 하나 또는 파일명 하나
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.RasterizeOptions()의 다른 키워드 인자들
           옵션을 gdal.RasterizeOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

::

   def BuildVRTOptions(options = [],
                       resolution = None,
                       outputBounds = None,
                       xRes = None, yRes = None,
                       targetAlignedPixels = None,
                       separate = None,
                       bandList = None,
                       addAlpha = None,
                       resampleAlg = None,
                       outputSRS = None,
                       allowProjectionDifference = None,
                       srcNodata = None,
                       VRTNodata = None,
                       hideNodata = None,
                       callback = None, callback_data = None):
       """ gdal.BuildVRT()로 전송할 수 있는 BuildVRTOptions() 객체를 생성합니다.
           Keyword 인자:
             options --- 문자열 배열, 문자열이 될 수 있고 또는 비워둔 채 다른 키워드들로 채울 수도 있습니다.
             resolution --- 'highest', 'lowest', 'average', 'user'
             outputBounds --- 대상 공간 좌표계 단위 (minX, minY, maxX, maxY)의 산출물 경계
             xRes, yRes --- 대상 공간 좌표계 단위 산출물 해상도
             targetAlignedPixels --- 산출물 경계를 산출물 해상도의 배수로 강제할지 여부
             separate --- 각 소스 파일을 VRT 밴드에 있는 개별 스택 밴드로 넣을지 여부
             bandList --- 밴드 번호 배열 (1에서 시작하는 색인)
             addAlpha --- 소스 래스터에 알파 마스크 밴드가 없는 경우 VRT에 추가할지 여부
             resampleAlg --- 리샘플링 모드
             outputSRS --- 할당된 산출 공간 좌표계
             allowProjectionDifference --- 동일한 투영법을 가지지 않은 입력 데이터셋들을 입력받을지 여부. 주의: 재투영하지 '않을' 것입니다.
             srcNodata --- 소스 NODATA 값(들)
             VRTNodata --- VRT 밴드 수준의 NODATA 값들
             hideNodata --- VRT 밴드가 NODATA 값을 리포트하지 않게 할지 여부
             callback --- 콜백 메소드
             callback_data --- 콜백 용 사용자 데이터
       """

   def BuildVRT(destName, srcDSOrSrcDSTab, **kwargs):
       """ 데이터셋 목록으로부터 VRT를 작성합니다.
           인자:
             destName --- 산출 데이터셋 이름
             srcDSOrSrcDSTab --- 데이터셋 객체 또는 파일명 목록, 또는 데이터셋 객체 또는 파일명
           키워드 인자:
             options --- gdal.InfoOptions()의 반환, 문자열 또는 문자열 배열,
             gdal.BuildVRTOptions()의 다른 키워드 인자들
           옵션을 gdal.BuildVRTOptions() 객체로 제공하는 경우, 다른 키워드를 무시합니다. """

유틸리티
--------

유틸리티들이 각각 대응하는 함수를 호출하도록 수정합니다.

문서화
------

새 메소드/함수를 모두 문서화합니다.

Test Suite
----------

`test_gdalinfo_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdalinfo_lib.py>`_ 에서 gdal.Info 메소드를 테스트합니다.

`test_gdal_translate_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdal_translate_lib.py>`_ 에서 gdal.Translate 메소드를 테스트합니다.

`test_gdalwarp_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdalwarp_lib.py>`_ 에서 gdal.Warp 메소드를 테스트합니다.

`test_ogr2ogr_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_ogr2ogr_lib.py>`_ 에서 gdal.VectorTranslate 메소드를 테스트합니다.

`test_gdaldem_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdaldem_lib.py>`_ 에서 gdal.DEMProcessing 메소드를 테스트합니다.

`test_nearblack_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_nearblack_lib.py>`_ 에서 gdal.Nearblack 메소드를 테스트합니다.

`test_gdal_grid_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdal_grid_lib.py>`_ 에서 gdal.Grid 메소드를 테스트합니다.

`test_gdal_rasterize_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdal_rasterize_lib.py>`_ 에서 gdal.Rasterize 메소드를 테스트합니다.

`test_gdalbuildvrt_lib.py <https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdalbuildvrt_lib.py>`_ 에서 gdal.BuildVRT 메소드를 테스트합니다.

호환성 문제점
-------------

예상되는 문제점은 없습니다. 명령줄 유틸리티들은 동일한 인터페이스를 유지할 것입니다. :file:`autotest/utilities` 에서의 유틸리티 테스트를 여전히 통과하는지 확인할 것입니다.

관련 티켓
---------

구현
----

파자 마하무드와 이벤 루올이 이 RFC를 구현할 것입니다.

gdalinfo 및 gdal_translate에 대해 제안한 구현은 `""rfc59.1"" 브랜치 <https://github.com/rouault/gdal2/tree/rfc59.1>`_ 에 있습니다.

투표 이력
---------

-  대니얼 모리셋 +1
-  이벤 루올 +1

