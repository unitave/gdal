.. _rfc-59:

=======================================================================================
RFC 59 : GDAL/OGR 유틸리티를 라이브러리로
=======================================================================================

저자: 파자 마하무드(Faza Mahamood)

연락처: fazamhd@gmail.com

상태: :ref:`rfc-59.1` 로 발전하여 이 RFC는 철회

요약
----

이 RFC는 각 GDAL 유틸리티에 대해 새 함수를 정의합니다. 이 새로운 유틸리티 함수를 사용해서 인메모리 데이터셋에 대해 작업할 수 있습니다. 유틸리티 코드가 새 함수를 호출할 수 있도록 수정합니다. 이 RFC는 gdalinfo를 통해 시연되지만, 다른 유틸리티들로 확장되는 것을 목표로 하는 일반 프레임과 원칙을 제공합니다.

근거
----

코드로부터 GDAL 유틸리티를 호출해야 할 필요가 있습니다. 그러나 이는 시스템 호출 사용을 수반하며 인메모리 데이터셋에 대해 작업할 수 없습니다.

변경 사항
---------

새 libgdalutils 라이브러리를 생성합니다. 유닉스 및 윈도우 빌드 둘 다 새 라이브러리를 연산에 넣도록 수정했습니다. GDAL 유틸리티가 새 함수를 사용하도록 수정합니다. GDAL 유틸리티의 공개 선언을 담고 있는 새 :file:`gdal_utils.h` 헤더 파일을 생성합니다. (아직 진행 중인) 현재 헤더는 `여기 <https://github.com/fazam/gdal/blob/gdalinfo/gdal/apps/gdal_utils.h>`_ 에서 찾아볼 수 있습니다.

::


       char CPL_DLL *GDALInfo( GDALDatasetH hDataset, GDALInfoOptions *psOptions );

       GDALInfoOptions CPL_DLL *GDALInfoOptionsNew( void );

       void CPL_DLL GDALInfoOptionsAddExtraMDDomains( GDALInfoOptions *psOptions,
                                                      const char *pszDomain );

       void CPL_DLL GDALInfoOptionsSetExtraMDDomains( GDALInfoOptions *psOptions,
                                                      char **papszExtraMDDomains );

       void CPL_DLL GDALInfoOptionsFree( GDALInfoOptions *psOptions );

::

   GDALDatasetH CPL_DLL GDALTranslate(const char *pszDest, GDALDatasetH hSrcDataset, GDALTranslateOptions *psOptions, int *pbUsageError)

   GDALDatasetH CPL_DLL GDALWarp( const char *pszDest, GDALDatasetH hDstDS, int nSrcCount,
                          GDALDatasetH *pahSrcDS, GDALWarpAppOptions *psOptions, int *pbUsageError )

   GDALDatasetH CPL_DLL OGR2OGR( const char *pszDest, GDALDatasetH hDstDS, GDALDatasetH hSrcDS,
                                 OGR2OGROptions *psOptions, int *pbUsageError )

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

파이썬 바인딩에 대해서만, GDAL 모듈에 새로운 Info(), Translate() 및 Warp() 함수를 추가합니다. 이 함수들은 각각 새로운 GDALInfo(), GDALTranslate() 및 GDALWarp() 함수를 사용합니다. OGR 모듈에는 새 OGR2OGR() 함수를 사용하는 Translate()를 추가합니다.

gdal.InfoOptions()의 속성을 설정하는 데 또는 gdal.Info()의 그때 그때 즉석에서 처리되는(inline) 인자로 gdal.Info()를 사용할 수 있습니다.

::


       options = gdal.InfoOptions()
       
       options.format = gdal.INFO_FORMAT_TEXT
       options.deserialize = True
       options.computeMinMax = False
       options.reportHistograms = False
       options.reportProj4 = True
       options.stats = False
       options.approxStats = True
       options.sample = False
       options.computeChecksum = False
       options.showGCPs = True
       options.showMetadata = True
       options.showRAT = False
       options.showColorTable = True
       options.listMDD = False
       options.showFileList = True
       options.allMetadata = TRUE
       options.extraMDDomains = ['TRE']
       
       gdal.Info(ds, options, deserialize = True)

::


       gdal.Info(ds, options = None, format = _gdal.INFO_FORMAT_TEXT, deserialize = True,
                computeMinMax = False, reportHistograms = False, reportProj4 = False,
                stats = False, approxStats = True, sample = False, computeChecksum = False,
                showGCPs = True, showMetadata = True, showRAT = True, showColorTable = True,
                listMDD = False, showFileList = True, allMetadata = False,
                extraMDDomains = None)

       gdal.Translate(destName, srcDS, options = None, format = 'GTiff', quiet = True,
                outputType = GDT_Unknown, maskMode = _gdal.MASK_AUTO, bandList = None,
                oXSizePixel = 0, oYSizePixel = 0, oXSizePct = 0.0, oYSizePct = 0.0,
                createOptions = None, srcWin = [0,0,0,0],strict = False,
                unscale = False, scaleParams = None, exponent = None,
                uLX = 0.0, uLY = 0.0, lRX = 0.0, lRY = 0.0, metadataOptions = None,
                outputSRS = None, GCPs = None, ULLR = [0,0,0,0], setNoData = False,
                unsetNoData = False, noDataReal = 0.0, rgbExpand = 0, maskBand = 0,
                stats = False, approxStats = False, errorOnPartiallyOutside = False,
                errorOnCompletelyOutside = False, noRAT = False, resampling = None,
                xRes = 0.0, yRes = 0.0, projSRS = None)
       
       gdal.Warp(destNameOrDestDS, srcDSOrSrcDSTab, options = None, minX = 0.0, minY = 0.0, maxX = 0.0,
                maxY = 0.0, xRes = 0.0, yRes = 0.0, targetAlignedPixels = False, forcePixels = 0,
                forceLines = 0, quiet = True, enableDstAlpha = False, enableSrcAlpha = False,
                format = 'GTiff', createOutput = False, warpOptions = None, errorThreshold = -1,
                warpMemoryLimit = 0.0, createOptions = None, outputType = GDT_Unknown,
                workingType = GDT_Unknown, resampleAlg = GRA_NearestNeighbour,
                srcNodata = None, dstNodata = None, multi = False, TO = None, cutlineDSName = None,
                cLayer = None, cWHERE = None, cSQL = None, cropToCutline = False, overwrite = False,
                copyMetadata = True, copyBandInfo = True, MDConflictValue = '*',
                setColorInterpretation = False, destOpenOptions = None, OvLevel = -2)

       ogr.Translate(destNameOrDestDS, srcDS, options = None, accessMode = _ogr.ACCESS_CREATION,
                skipFailures = False, layerTransaction = -1, forceTransaction = False,
                groupTransactions = 20000, FIDToFetch = -1, quiet = False,
                format = 'ESRI Shapefile', layers = None, DSCO = None, LCO = None, transform = False,
                addMissingFields = False, outputSRSDef = None, sourceSRSDef = None,
                nullifyOutputSRS = False, exactFieldNameMatch = True, newLayerName = None,
                WHERE = None, geomField = None, selFields = None, SQLStatement = None,
                dialect = None, gType = -2, geomConversion = _ogr.GEOMTYPE_DEFAULT, geomOp = _ogr.GEOMOP_NONE,
                geomOpParam = 0, fieldTypesToString = None, mapFieldType = None, unsetFieldWidth = False,
                displayProgress = False, wrapDateline = False, dateLineOffset = 10, clipSrc = None, clipSrcDS = None,
                clipSrcSQL = None, clipSrcLayer = None, clipSrcWhere = None, clipDst = None,
                clipDstDS = None, clipDstSQL = None, clipDstLayer = None, clipDstWhere = None,
                splitListFields = False, maxSplitListSubFields = -1, explodeCollections = False,
                zField = None, fieldMap = None, coordDim = -1, destOpenOptions = None,
                forceNullable = False, unsetDefault = False, unsetFid = False, preserveFID = False,
                copyMD = True, metadataOptions = None, spatSRSDef = None, transformOrder = 0,
                spatialFilter = None)

유틸리티
--------

유틸리티들이 각각 대응하는 함수를 호출하도록 수정합니다.

문서화
------

새 메소드/함수를 모두 문서화합니다.

테스트 스위트
-------------

:file:`test_gdalinfo_lib.py` 에서 gdal.Info() 메소드를 테스트합니다.
:file:`test_gdal_translate_lib.py` 에서 gdal.Translate() 메소드를 테스트합니다.
:file:`test_gdalwarp_lib.py` 에서 gdal.Warp() 메소드를 테스트합니다.
:file:`test_ogr2ogr_lib.py` 에서 ogr.Translate() 메소드를 테스트합니다.

호환성 문제점
-------------

예상되는 문제점은 없습니다. 명령줄 유틸리티들은 동일한 인터페이스를 유지할 것입니다. :file:`autotest/utilities` 에서의 유틸리티 테스트를 여전히 통과하는지 확인할 것입니다.

공개 질문
---------

라이브러리화된 ogr2ogr에 어떤 이름을 붙여야 할까요? OGR2OGR() 또는 OGRTranslate()?

GDALTranslate(), GDALWarp() 및 OGR2OGR()에 있는 인자들의 순서는 현재 소스(들) 쪽이라기 보단 대상 쪽입니다.

::

   GDALDatasetH CPL_DLL GDALTranslate(const char *pszDest, GDALDatasetH hSrcDataset, GDALTranslateOptions *psOptions, int *pbUsageError)

   GDALDatasetH CPL_DLL GDALWarp( const char *pszDest, GDALDatasetH hDstDS, int nSrcCount,
                          GDALDatasetH *pahSrcDS, GDALWarpAppOptions *psOptions, int *pbUsageError )

   GDALDatasetH CPL_DLL OGR2OGR( const char *pszDest, GDALDatasetH hDstDS, GDALDatasetH hSrcDS,
                                 OGR2OGROptions *psOptions, int *pbUsageError )

``GDALCreateCopy(const char\* pszDestFilename, GDALDatasetH hSrcDS, ....)`` 의 인자 순서와 유사하기 때문에, 적어도 API 수준에서는 일관적인 형식이 존재합니다. 의견이 있으신 분?

관련 티켓
---------

구현
----

파자 마하무드가 이 RFC를 구현할 것입니다.

제안한 구현은 `"gdalinfo" 브랜치 <https://github.com/fazam/gdal/tree/gdalinfo>`_ 에 있습니다.

`변경 사항 목록 <https://github.com/fazam/gdal/compare/gdalinfo>`_

투표 이력
---------

