.. _multidimensional_api_tut:

================================================================================
다중차원 래스터 API 예제
================================================================================

배열 내용 읽어오기
------------------

C++ 코드
++++++++

.. code-block:: c++

    #include "gdal_priv.h"
    int main()
    {
        GDALAllRegister();
        auto poDataset = std::unique_ptr<GDALDataset>(
            GDALDataset::Open( "in.nc", GDAL_OF_MULTIDIM_RASTER ));
        if( !poDataset )
        {
            exit(1);
        }
        auto poRootGroup = poDataset->GetRootGroup();
        if( !poRootGroup )
        {
            exit(1);
        }
        auto poVar = poRootGroup->OpenMDArray("temperature");
        if( !poVar )
        {
            exit(1);
        }
        size_t nValues = 1;
        std::vector<size_t> anCount;
        for( const auto poDim: poVar->GetDimensions() )
        {
            anCount.push_back(static_cast<size_t>(poDim->GetSize()));
            nValues *= anCount.back();
        }
        std::vector<double> values(nValues);
        poVar->Read(std::vector<GUInt64>{0,0,0}.data(),
                    anCount.data(),
                    nullptr, /* step: 기본값은 1,1,1 */
                    nullptr, /* stride: 기본값은 행 중심 규범 */
                    GDALExtendedDataType::Create(GDT_Float64),
                    &values[0]);
        return 0;
    }

C 코드
++++++

.. code-block:: c

    #include "gdal.h"
    #include "cpl_conv.h"
    int main()
    {
        GDALDatasetH hDS;
        GDALGroupH hGroup;
        GDALMDArrayH hVar;
        size_t nDimCount;
        GDALDimensionH* dims;
        size_t nValues;
        size_t i;
        size_t* panCount;
        GUInt64* panOffset;
        double* padfValues;
        GDALExtendedDataTypeH hDT;

        GDALAllRegister();
        hDS = GDALOpenEx( "in.nc", GDAL_OF_MULTIDIM_RASTER, NULL, NULL, NULL);
        if( !hDS )
        {
            exit(1);
        }
        hGroup = GDALDatasetGetRootGroup(hDS);
        GDALReleaseDataset(hDS);
        if( !hGroup )
        {
            exit(1);
        }
        hVar = GDALGroupOpenMDArray(hGroup, "temperature", NULL);
        GDALGroupRelease(hGroup);
        if( !hVar )
        {
            exit(1);
        }

        dims = GDALMDArrayGetDimensions(hVar, &nDimCount);
        panCount = (size_t*)CPLMalloc(nDimCount * sizeof(size_t));
        nValues = 1;
        for( i = 0; i < nDimCount; i++ )
        {
            panCount[i] = GDALDimensionGetSize(dims[i]);
            nValues *= panCount[i];
        }
        GDALReleaseDimensions(dims, nDimCount);
        panOffset = (GUInt64*)CPLCalloc(nDimCount, sizeof(GUInt64));

        padfValues = (double*)VSIMalloc2(nValues, sizeof(double));
        if( !padfValues )
        {
            GDALMDArrayRelease(hVar);
            CPLFree(panOffset);
            CPLFree(panCount);
            exit(1);
        }
        hDT = GDALExtendedDataTypeCreate(GDT_Float64);
        GDALMDArrayRead(hVar,
                        panOffset,
                        panCount,
                        NULL, /* step: 기본값은 1,1,1 */
                        NULL, /* stride: 기본값은 행 중심 규범 */
                        hDT,
                        padfValues,
                        NULL, /* 배열 시작. 생략됨 */
                        0 /* 바이트 단위 배열 크기. 생략됨 */);
        GDALExtendedDataTypeRelease(hDT);
        GDALMDArrayRelease(hVar);
        CPLFree(panOffset);
        CPLFree(panCount);
        VSIFree(padfValues);

        return 0;
    }

파이썬 코드
+++++++++++

.. code-block:: python

    from osgeo import gdal
    ds = gdal.OpenEx("in.nc", gdal.OF_MULTIDIM_RASTER)
    rootGroup = ds.GetRootGroup()
    var = rootGroup.OpenMDArray("temperature")
    data = var.Read(buffer_datatype = gdal.ExtendedDataType.Create(gdal.GDT_Float64))

NumPy를 사용할 수 있는 경우:

.. code-block:: python

    from osgeo import gdal
    ds = gdal.OpenEx("in.nc", gdal.OF_MULTIDIM_RASTER)
    rootGroup = ds.GetRootGroup()
    var = rootGroup.OpenMDArray("temperature")
    data = var.ReadAsArray(buffer_datatype = gdal.ExtendedDataType.Create(gdal.GDT_Float64))

기타 예시
---------

GDAL 자동 테스트 스위트의 테스트 스크립트들:

  -  https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/gdrivers/memmultidim.py
  -  https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/gdrivers/netcdf_multidim.py
  -  https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/gdrivers/vrtmultidim.py
  -  https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/utilities/test_gdalmdiminfo_lib.py
  -  https://raw.githubusercontent.com/OSGeo/gdal/master/autotest/utilities/test_gdalmdimtranslate_lib.py

