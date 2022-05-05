.. _vector_api_tut:

================================================================================
벡터 API 예제
================================================================================

이 문서에서는 OGR C++ 클래스를 사용해서 파일의 데이터를 읽고 쓰는 방법을 문서화하려 합니다. 먼저 OGR에서 주요 클래스 및 그 역할을 설명하고 있는 :ref:`vector_data_model` 문서를 살펴볼 것을 강력히 권장합니다.

이 문서는 C 및 파이썬 언어로 된 대응하는 함수들의 코드 조각도 포함하고 있습니다.

OGR로부터 읽어오기
------------------

OGR로 읽어오기를 보여주기 위해, OGR 데이터소스로부터 표준 출력(stdout)에 포인트 레이어를 쉼표 구분 형식으로 덤프하는 간단한 유틸리티를 구성할 것입니다.

가장 먼저 원하는 포맷 드라이버를 모두 등록해야 합니다. 일반적으로 GDAL/OGR에 빌드된 모든 포맷 드라이버를 등록하는 :cpp:func:`GDALAllRegister` 함수를 호출하면 됩니다.

C++ 코드:

.. code-block:: c++

    #include "ogrsf_frmts.h"

    int main()

    {
        GDALAllRegister();

C 코드:

.. code-block:: c

    #include "gdal.h"

    int main()

    {
        GDALAllRegister();

그 다음 입력 OGR 데이터셋을 열어야 합니다. 파일, RDBMS(Relational DataBase Management System), 파일로 가득 찬 디렉터리, 또는 사용하는 드라이버에 따라 원격 웹 서비스조차 데이터소스가 될 수 있습니다. 하지만, 데이터소스 이름은 언제나 단일 문자열입니다. 다음 예시에서는 특정 shapefile을 열기 위해 하드코딩했습니다. 두 번째 인자(GDAL_OF_VECTOR)는 :cpp:func:`OGROpen` 메소드에 벡터 드라이버를 사용하려 하고 업데이트 접근은 필요없다는 사실을 알려줍니다. 열기 실패 시 NULL을 반환하고 오류를 리포트합니다.

C++ 코드:

.. code-block:: c++

    GDALDataset       *poDS;

    poDS = (GDALDataset*) GDALOpenEx( "point.shp", GDAL_OF_VECTOR, NULL, NULL, NULL );
    if( poDS == NULL )
    {
        printf( "Open failed.\n" );
        exit( 1 );
    }

C 코드:

.. code-block:: c

    GDALDatasetH hDS;

    hDS = GDALOpenEx( "point.shp", GDAL_OF_VECTOR, NULL, NULL, NULL );
    if( hDS == NULL )
    {
        printf( "Open failed.\n" );
        exit( 1 );
    }

:cpp:class:`GDALDataset` 클래스는 수많은 관련 레이어를 가질 수 있습니다. :cpp:func:`GDALDataset::GetLayerCount` 함수로 사용할 수 있는 레이어 개수를 쿼리할 수 있습니다. 또 :cpp:func:`GDALDataset::GetLayer` 함수로 색인을 사용해서 개별 레이어를 가져올 수 있습니다. 하지만 여기에서는 이름만으로 레이어를 가져올 것입니다.

C++ 코드:

.. code-block:: c++

    OGRLayer  *poLayer;

    poLayer = poDS->GetLayerByName( "point" );

C 코드:

.. code-block:: c

    OGRLayerH hLayer;

    hLayer = GDALDatasetGetLayerByName( hDS, "point" );

이제 레이어로부터 피처를 읽어오기 시작해야 합니다. 피처를 읽어오기 전에, 반환되는 피처 집합을 제한하기 위해 레이어에 속성 또는 공간 필터를 적용할 수 있습니다. 그러나 지금은 모든 피처를 읽어오도록 합시다.

GDAL 2.3버전에서 C++ 11버전 코드:

.. code-block:: c++

    for( auto& poFeature: poLayer )
    {

GDAL 2.3버전에서 C코드:

.. code-block:: c

    OGR_FOR_EACH_FEATURE_BEGIN(hFeature, hLayer)
    {

예전 GDAL 버전들을 사용하는 경우, 이 예시에서는 레이어를 처음부터 읽어오기 때문에 엄격히 필요하지 않지만, 일반적으로 레이어를 시작부터 읽어오도록 보장하기 위해 :cpp:func:`OGRLayer::ResetReading` 함수를 호출하는 편이 좋습니다. :cpp:func:`OGRLayer::GetNextFeature` 함수를 이용해서 레이어에 있는 모든 피처를 반복합니다. 다음 피처가 없으면 NULL을 반환할 것입니다.

GDAL 2.3 미만 버전에서 C++ 코드:

.. code-block:: c++

    OGRFeature *poFeature;

    poLayer->ResetReading();
    while( (poFeature = poLayer->GetNextFeature()) != NULL )
    {

GDAL 2.3 미만 버전에서 C 코드:

.. code-block:: c

    OGRFeatureH hFeature;

    OGR_L_ResetReading(hLayer);
    while( (hFeature = OGR_L_GetNextFeature(hLayer)) != NULL )
    {

피처의 모든 속성 필드를 덤프하려면, :cpp:class:`OGRFeatureDefn` 클래스를 가져오는 것이 좋습니다. 이 클래스는 레이어와 연결된 객체로, 모든 필드의 정의를 담고 있습니다. 모든 필드를 반복해서 필드 유형을 기반으로 속성을 가져와 리포트합니다.

GDAL 2.3버전에서 C++ 11버전 코드:

.. code-block:: c++

    for( auto&& oField: *poFeature )
    {
        switch( oField.GetType() )
        {
            case OFTInteger:
                printf( "%d,", oField.GetInteger() );
                break;
            case OFTInteger64:
                printf( CPL_FRMT_GIB ",", oField.GetInteger64() );
                break;
            case OFTReal:
                printf( "%.3f,", oField.GetDouble() );
                break;
            case OFTString:
                printf( "%s,", oField.GetString() );
                break;
            default:
                printf( "%s,", oField.GetAsString() );
                break;
        }
    }

GDAL 2.3 미만 버전에서 C++ 코드:

.. code-block:: c

    OGRFeatureDefn *poFDefn = poLayer->GetLayerDefn();
    for( int iField = 0; iField < poFDefn->GetFieldCount(); iField++ )
    {
        OGRFieldDefn *poFieldDefn = poFDefn->GetFieldDefn( iField );

        switch( poFieldDefn->GetType() )
        {
            case OFTInteger:
                printf( "%d,", poFeature->GetFieldAsInteger( iField ) );
                break;
            case OFTInteger64:
                printf( CPL_FRMT_GIB ",", poFeature->GetFieldAsInteger64( iField ) );
                break;
            case OFTReal:
                printf( "%.3f,", poFeature->GetFieldAsDouble(iField) );
                break;
            case OFTString:
                printf( "%s,", poFeature->GetFieldAsString(iField) );
                break;
            default:
                printf( "%s,", poFeature->GetFieldAsString(iField) );
                break;
        }
    }

C 코드:

.. code-block:: c

    OGRFeatureDefnH hFDefn = OGR_L_GetLayerDefn(hLayer);
    int iField;

    for( iField = 0; iField < OGR_FD_GetFieldCount(hFDefn); iField++ )
    {
        OGRFieldDefnH hFieldDefn = OGR_FD_GetFieldDefn( hFDefn, iField );

        switch( OGR_Fld_GetType(hFieldDefn) )
        {
            case OFTInteger:
                printf( "%d,", OGR_F_GetFieldAsInteger( hFeature, iField ) );
                break;
            case OFTInteger64:
                printf( CPL_FRMT_GIB ",", OGR_F_GetFieldAsInteger64( hFeature, iField ) );
                break;
            case OFTReal:
                printf( "%.3f,", OGR_F_GetFieldAsDouble( hFeature, iField) );
                break;
            case OFTString:
                printf( "%s,", OGR_F_GetFieldAsString( hFeature, iField) );
                break;
            default:
                printf( "%s,", OGR_F_GetFieldAsString( hFeature, iField) );
                break;
        }
    }

앞의 예시에서 명확하게 다룬 필드 유형들보다 더 많은 필드 유형이 있지만, :cpp:func:`OGRFeature::GetFieldAsString` 메소드로 필드 유형들의 합당한 표현을 가져올 수 있습니다. 사실 모든 유형에 :cpp:func:`GetFieldAsString` 을 사용하면 앞의 예시를 짧게 줄일 수 있습니다.

다음으로 피처로부터 도형을 추출해서 포인트 도형 x 및 y를 작성할 것입니다. 도형은 일반 :cpp:class:`OGRGeometry` 포인터로 반환됩니다. 그러면 특정 도형 유형을 판단해서 포인트인 경우 포인트로 캐스트하고 작업합니다. 다른 유형이라면 플레이스홀더(placeholder)를 작성합니다.

C++ 코드:

.. code-block:: c++

    OGRGeometry *poGeometry;

    poGeometry = poFeature->GetGeometryRef();
    if( poGeometry != NULL
            && wkbFlatten(poGeometry->getGeometryType()) == wkbPoint )
    {
    #if GDAL_VERSION_NUM >= GDAL_COMPUTE_VERSION(2,3,0)
        OGRPoint *poPoint = poGeometry->toPoint();
    #else
        OGRPoint *poPoint = (OGRPoint *) poGeometry;
    #endif

        printf( "%.3f,%3.f\n", poPoint->getX(), poPoint->getY() );
    }
    else
    {
        printf( "no point geometry\n" );
    }

C 코드:

.. code-block:: c

    OGRGeometryH hGeometry;

    hGeometry = OGR_F_GetGeometryRef(hFeature);
    if( hGeometry != NULL
            && wkbFlatten(OGR_G_GetGeometryType(hGeometry)) == wkbPoint )
    {
        printf( "%.3f,%3.f\n", OGR_G_GetX(hGeometry, 0), OGR_G_GetY(hGeometry, 0) );
    }
    else
    {
        printf( "no point geometry\n" );
    }

이 예시에서 :cpp:func:`wkbFlatten` 매크로 함수를 사용해서 'wkbPoint25D'(z 좌표를 가진 포인트) 유형을 기본 2차원 도형 유형 코드(wkbPoint)로 변환합니다. 각 2차원 도형 유형별로 대응하는 2.5차원 유형 코드가 존재합니다. 동일한 C++ 클래스가 2차원 및 2.5차원 도형을 처리하기 때문에, 이 코드는 2차원 또는 3차원 도형을 제대로 처리할 것입니다.

피처 하나에 도형 필드 여러 개가 연결될 수 있습니다.

C++ 코드:

.. code-block:: c++

    OGRGeometry *poGeometry;
    int iGeomField;
    int nGeomFieldCount;

    nGeomFieldCount = poFeature->GetGeomFieldCount();
    for(iGeomField = 0; iGeomField < nGeomFieldCount; iGeomField ++ )
    {
        poGeometry = poFeature->GetGeomFieldRef(iGeomField);
        if( poGeometry != NULL
                && wkbFlatten(poGeometry->getGeometryType()) == wkbPoint )
        {
    #if GDAL_VERSION_NUM >= GDAL_COMPUTE_VERSION(2,3,0)
            OGRPoint *poPoint = poGeometry->toPoint();
    #else
            OGRPoint *poPoint = (OGRPoint *) poGeometry;
    #endif

            printf( "%.3f,%3.f\n", poPoint->getX(), poPoint->getY() );
        }
        else
        {
            printf( "no point geometry\n" );
        }
    }

C 코드:

.. code-block:: c

    OGRGeometryH hGeometry;
    int iGeomField;
    int nGeomFieldCount;

    nGeomFieldCount = OGR_F_GetGeomFieldCount(hFeature);
    for(iGeomField = 0; iGeomField < nGeomFieldCount; iGeomField ++ )
    {
        hGeometry = OGR_F_GetGeomFieldRef(hFeature, iGeomField);
        if( hGeometry != NULL
                && wkbFlatten(OGR_G_GetGeometryType(hGeometry)) == wkbPoint )
        {
            printf( "%.3f,%3.f\n", OGR_G_GetX(hGeometry, 0),
                    OGR_G_GetY(hGeometry, 0) );
        }
        else
        {
            printf( "no point geometry\n" );
        }
    }

파이썬 코드:

.. code-block:: python

    nGeomFieldCount = feat.GetGeomFieldCount()
    for iGeomField in range(nGeomFieldCount):
        geom = feat.GetGeomFieldRef(iGeomField)
        if geom is not None and geom.GetGeometryType() == ogr.wkbPoint:
            print "%.3f, %.3f" % ( geom.GetX(), geom.GetY() )
        else:
            print "no point geometry\n"

:cpp:func:`OGRFeature::GetGeometryRef` 및 :cpp:func:`OGRFeature::GetGeomFieldRef` 함수가 :cpp:class:`OGRFeature` 가 소유한 내부 도형을 가리키는 포인터를 반환한다는 사실을 기억하십시오. 반환 도형을 실제로 삭제하는 것이 아닙니다.

GDAL 2.3버전에서 C++ 11버전 코드를 쓰면, 중괄호('{}')를 닫는 것만으로 피처 반복을 종료할 수 있습니다.

.. code-block:: c++

    }

GDAL 2.3버전에서 C 코드를 쓰면, 다음과 같이 피처 반복을 종료할 수 있습니다.

.. code-block:: c

    }
    OGR_FOR_EACH_FEATURE_END(hFeature)

GDAL 2.3 미만 버전의 경우, :cpp:func:`OGRLayer::GetNextFeature` 메소드가 이제 사용자가 소유한 피처의 복사본을 반환합니다. 따라서 사용이 끝나면 피처를 해제해줘야만 합니다. 그냥 피처를 "삭제"해도 되지만, GDAL DLL이 주요 프로그램과 다른 "`힙(heap) <https://ko.wikipedia.org/wiki/%ED%9E%99_(%EC%9E%90%EB%A3%8C_%EA%B5%AC%EC%A1%B0)>`_" 을 가지는 윈도우 빌드에서는 문제를 일으킬 수 있습니다. 안전을 위해 GDAL 함수를 이용해서 피처를 삭제할 것입니다.

C++ 코드:

.. code-block:: c++

        OGRFeature::DestroyFeature( poFeature );
    }

C 코드:

.. code-block:: c

        OGR_F_Destroy( hFeature );
    }

:cpp:func:`GDALDataset::GetLayerByName` 함수가 반환하는 :cpp:class:`OGRLayer` 도 :cpp:class:`GDALDataset` 이 소유한 내부 레이어를 가리키는 참조이기 때문에 삭제할 필요가 없습니다. 그러나 입력 파일을 종료하려면 데이터소스를 삭제해야 합니다. 마찬가지로 Win32 힙(heap) 문제점을 피하기 위해 사용자 지정 삭제 메소드를 사용할 것입니다.

C/C++ 코드:

.. code-block:: c++

        GDALClose( poDS );
    }

이 코드들을 모두 합친 프로그램은 다음과 같이 보일 것입니다.

GDAL 2.3버전에서 C++ 11버전 코드:

.. code-block:: c++

    #include "ogrsf_frmts.h"

    int main()

    {
        GDALAllRegister();

        GDALDatasetUniquePtr poDS(GDALDataset::Open( "point.shp", GDAL_OF_VECTOR));
        if( poDS == nullptr )
        {
            printf( "Open failed.\n" );
            exit( 1 );
        }

        for( const OGRLayer* poLayer: poDS->GetLayers() )
        {
            for( const auto& poFeature: *poLayer )
            {
                for( const auto& oField: *poFeature )
                {
                    switch( oField.GetType() )
                    {
                        case OFTInteger:
                            printf( "%d,", oField.GetInteger() );
                            break;
                        case OFTInteger64:
                            printf( CPL_FRMT_GIB ",", oField.GetInteger64() );
                            break;
                        case OFTReal:
                            printf( "%.3f,", oField.GetDouble() );
                            break;
                        case OFTString:
                            printf( "%s,", oField.GetString() );
                            break;
                        default:
                            printf( "%s,", oField.GetAsString() );
                            break;
                    }
                }

                const OGRGeometry *poGeometry = poFeature->GetGeometryRef();
                if( poGeometry != nullptr
                        && wkbFlatten(poGeometry->getGeometryType()) == wkbPoint )
                {
                    const OGRPoint *poPoint = poGeometry->toPoint();

                    printf( "%.3f,%3.f\n", poPoint->getX(), poPoint->getY() );
                }
                else
                {
                    printf( "no point geometry\n" );
                }
            }
        }
        return 0;
    }

C++ 코드:

.. code-block:: c++

    #include "ogrsf_frmts.h"

    int main()

    {
        GDALAllRegister();

        GDALDataset *poDS = static_cast<GDALDataset*>(
            GDALOpenEx( "point.shp", GDAL_OF_VECTOR, NULL, NULL, NULL ));
        if( poDS == NULL )
        {
            printf( "Open failed.\n" );
            exit( 1 );
        }

        OGRLayer  *poLayer = poDS->GetLayerByName( "point" );
        OGRFeatureDefn *poFDefn = poLayer->GetLayerDefn();

        poLayer->ResetReading();
        OGRFeature *poFeature;
        while( (poFeature = poLayer->GetNextFeature()) != NULL )
        {
            for( int iField = 0; iField < poFDefn->GetFieldCount(); iField++ )
            {
                OGRFieldDefn *poFieldDefn = poFDefn->GetFieldDefn( iField );

                switch( poFieldDefn->GetType() )
                {
                    case OFTInteger:
                        printf( "%d,", poFeature->GetFieldAsInteger( iField ) );
                        break;
                    case OFTInteger64:
                        printf( CPL_FRMT_GIB ",", poFeature->GetFieldAsInteger64( iField ) );
                        break;
                    case OFTReal:
                        printf( "%.3f,", poFeature->GetFieldAsDouble(iField) );
                        break;
                    case OFTString:
                        printf( "%s,", poFeature->GetFieldAsString(iField) );
                        break;
                    default:
                        printf( "%s,", poFeature->GetFieldAsString(iField) );
                        break;
                }
            }

            OGRGeometry *poGeometry = poFeature->GetGeometryRef();
            if( poGeometry != NULL
                    && wkbFlatten(poGeometry->getGeometryType()) == wkbPoint )
            {
                OGRPoint *poPoint = (OGRPoint *) poGeometry;

                printf( "%.3f,%3.f\n", poPoint->getX(), poPoint->getY() );
            }
            else
            {
                printf( "no point geometry\n" );
            }
            OGRFeature::DestroyFeature( poFeature );
        }

        GDALClose( poDS );
    }

C 코드:

.. code-block:: c

    #include "gdal.h"

    int main()

    {
        GDALAllRegister();

        GDALDatasetH hDS;
        OGRLayerH hLayer;
        OGRFeatureH hFeature;
        OGRFeatureDefnH hFDefn;

        hDS = GDALOpenEx( "point.shp", GDAL_OF_VECTOR, NULL, NULL, NULL );
        if( hDS == NULL )
        {
            printf( "Open failed.\n" );
            exit( 1 );
        }

        hLayer = GDALDatasetGetLayerByName( hDS, "point" );
        hFDefn = OGR_L_GetLayerDefn(hLayer);

        OGR_L_ResetReading(hLayer);
        while( (hFeature = OGR_L_GetNextFeature(hLayer)) != NULL )
        {
            int iField;
            OGRGeometryH hGeometry;

            for( iField = 0; iField < OGR_FD_GetFieldCount(hFDefn); iField++ )
            {
                OGRFieldDefnH hFieldDefn = OGR_FD_GetFieldDefn( hFDefn, iField );

                switch( OGR_Fld_GetType(hFieldDefn) )
                {
                    case OFTInteger:
                        printf( "%d,", OGR_F_GetFieldAsInteger( hFeature, iField ) );
                        break;
                    case OFTInteger64:
                        printf( CPL_FRMT_GIB ",", OGR_F_GetFieldAsInteger64( hFeature, iField ) );
                        break;
                    case OFTReal:
                        printf( "%.3f,", OGR_F_GetFieldAsDouble( hFeature, iField) );
                        break;
                    case OFTString:
                        printf( "%s,", OGR_F_GetFieldAsString( hFeature, iField) );
                        break;
                    default:
                        printf( "%s,", OGR_F_GetFieldAsString( hFeature, iField) );
                        break;
                }
            }

            hGeometry = OGR_F_GetGeometryRef(hFeature);
            if( hGeometry != NULL
                && wkbFlatten(OGR_G_GetGeometryType(hGeometry)) == wkbPoint )
            {
                printf( "%.3f,%3.f\n", OGR_G_GetX(hGeometry, 0), OGR_G_GetY(hGeometry, 0) );
            }
            else
            {
                printf( "no point geometry\n" );
            }

            OGR_F_Destroy( hFeature );
        }

        GDALClose( hDS );
    }

파이썬 코드:

.. code-block:: python

    import sys
    from osgeo import gdal

    ds = gdal.OpenEx( "point.shp", gdal.OF_VECTOR )
    if ds is None:
        print "Open failed.\n"
        sys.exit( 1 )

    lyr = ds.GetLayerByName( "point" )

    lyr.ResetReading()

    for feat in lyr:

        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            field_defn = feat_defn.GetFieldDefn(i)

            # 다음 테스트는 'print feat.GetField(i)'로 단순화시킬 수 있습니다
            if field_defn.GetType() == ogr.OFTInteger or field_defn.GetType() == ogr.OFTInteger64:
                print "%d" % feat.GetFieldAsInteger64(i)
            elif field_defn.GetType() == ogr.OFTReal:
                print "%.3f" % feat.GetFieldAsDouble(i)
            elif field_defn.GetType() == ogr.OFTString:
                print "%s" % feat.GetFieldAsString(i)
            else:
                print "%s" % feat.GetFieldAsString(i)

        geom = feat.GetGeometryRef()
        if geom is not None and geom.GetGeometryType() == ogr.wkbPoint:
            print "%.3f, %.3f" % ( geom.GetX(), geom.GetY() )
        else:
            print "no point geometry\n"

    ds = None

OGR에 쓰기
----------

OGR를 통한 쓰기의 예시로서, 앞과 대략적으로 반대되는 작업을 할 것입니다. 입력 텍스트로부터 쉼표로 구분된 값들을 읽어와서 OGR를 통해 포인트 shapefile로 작성하는 짧은 프로그램을 구성할 것입니다.

읽기와 마찬가지로, 모든 드라이버를 등록한 다음 Shapefile 드라이버를 가져옵니다. 산출 파일을 생성하기 위해 필요할 것이기 때문입니다.

C++ 코드:

.. code-block:: c++

    #include "ogrsf_frmts.h"

    int main()
    {
        const char *pszDriverName = "ESRI Shapefile";
        GDALDriver *poDriver;

        GDALAllRegister();

        poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName );
        if( poDriver == NULL )
        {
            printf( "%s driver not available.\n", pszDriverName );
            exit( 1 );
        }

C 코드:

.. code-block:: c

    #include "ogr_api.h"

    int main()
    {
        const char *pszDriverName = "ESRI Shapefile";
        GDALDriver *poDriver;

        GDALAllRegister();

        poDriver = (GDALDriver*) GDALGetDriverByName(pszDriverName );
        if( poDriver == NULL )
        {
            printf( "%s driver not available.\n", pszDriverName );
            exit( 1 );
        }

다음으로 데이터소스를 생성합니다. ESRI Shapefile 드라이버는 shapefile로 가득 찬 디렉터리 또는 단일 shapefile을 데이터소스로 생성할 수 있습니다. 이 예시에서는 파일명에 확장자를 포함시켜 명확하게 단일 파일을 생성할 것입니다. 다른 드라이버들은 다르게 작동합니다.
두 번째, 세 번째, 네 번째 그리고 다섯 번째 인자는 (드라이버가 래스터 케이퍼빌리티를 가지고 있는 경우) 래스터 차원에 관련되어 있습니다. 호출의 마지막 인자는 옵션 값들의 목록이지만, 이 예시에서는 기본값만 사용할 것입니다. 지원되는 옵션들의 상세 사항 역시 포맷에 따라 달라집니다.

C++ 코드:

.. code-block:: c++

    GDALDataset *poDS;

    poDS = poDriver->Create( "point_out.shp", 0, 0, 0, GDT_Unknown, NULL );
    if( poDS == NULL )
    {
        printf( "Creation of output file failed.\n" );
        exit( 1 );
    }


C 코드:

.. code-block:: c

    GDALDatasetH hDS;

    hDS = GDALCreate( hDriver, "point_out.shp", 0, 0, 0, GDT_Unknown, NULL );
    if( hDS == NULL )
    {
        printf( "Creation of output file failed.\n" );
        exit( 1 );
    }

이제 산출 레이어를 생성했습니다. 이 경우 데이터소스가 단일 파일이기 때문에 레이어 하나만 가질 수 있습니다. 이 레이어가 지원하는 도형 유형을 지정하기 위해 'wkbPoint'를 전송합니다. 이 예시에서는 좌표계 정보 또는 다른 특수 레이어 생성 옵션을 하나도 전송하지 않습니다.

C++ 코드:

.. code-block:: c++

    OGRLayer *poLayer;

    poLayer = poDS->CreateLayer( "point_out", NULL, wkbPoint, NULL );
    if( poLayer == NULL )
    {
        printf( "Layer creation failed.\n" );
        exit( 1 );
    }


C 코드:

.. code-block:: c

    OGRLayerH hLayer;

    hLayer = GDALDatasetCreateLayer( hDS, "point_out", NULL, wkbPoint, NULL );
    if( hLayer == NULL )
    {
        printf( "Layer creation failed.\n" );
        exit( 1 );
    }

이제 레이어가 존재하므로, 레이어 상에 나타나야 할 모든 속성 필드를 생성해야 합니다. 레이어에 피처를 작성하기 전에 속성 필드를 추가해야만 합니다. 필드를 생성하기 위해 필드 관련 정보를 가진 :cpp:union:`OGRField` 객체를 초기화합니다. shapefile의 경우 필드 길이 및 정밀도가 산출 .dbf 파일 생성에 중요하기 때문에 이들을 특별히 설정하지만, 일반적으로 기본값을 사용해도 됩니다. 이 예시의 경우 'x,y' 포인트와 연결된 'name' 문자열 속성 필드 하나만 생성할 것입니다.

:cpp:func:`OGRLayer::CreateField` 함수에 전송하는 템플릿 :cpp:union:`OGRField` 객체를 내부적으로 복사한다는 사실을 기억하십시오. 이 객체의 소유권은 변경되지 않습니다.

C++ 코드:

.. code-block:: c++

    OGRFieldDefn oField( "Name", OFTString );

    oField.SetWidth(32);

    if( poLayer->CreateField( &oField ) != OGRERR_NONE )
    {
        printf( "Creating Name field failed.\n" );
        exit( 1 );
    }

C 코드:

.. code-block:: c

    OGRFieldDefnH hFieldDefn;

    hFieldDefn = OGR_Fld_Create( "Name", OFTString );

    OGR_Fld_SetWidth( hFieldDefn, 32);

    if( OGR_L_CreateField( hLayer, hFieldDefn, TRUE ) != OGRERR_NONE )
    {
        printf( "Creating Name field failed.\n" );
        exit( 1 );
    }

    OGR_Fld_Destroy(hFieldDefn);

다음 코드 조각은 표준 입력(stdin)으로부터 "x,y,name" 형식의 줄들을 반복해서 읽어와서 파싱합니다.

C/C++ 코드:

.. code-block:: c

    double x, y;
    char szName[33];

    while( !feof(stdin)
           && fscanf( stdin, "%lf,%lf,%32s", &x, &y, szName ) == 3 )
    {

디스크에 피처를 작성하려면 레이어에 작성하기 전에 로컬 :cpp:class:`OGRFeature` 를 생성하고 속성을 설정한 다음 도형을 추가해야만 합니다. 이 피처가 작성될 레이어와 연결되어 있는 :cpp:class:`OGRFeatureDefn` 으로부터 이 피처를 인스턴스화해야만 합니다.

C++ 코드:

.. code-block:: c++

        OGRFeature *poFeature;

        poFeature = OGRFeature::CreateFeature( poLayer->GetLayerDefn() );
        poFeature->SetField( "Name", szName );

C 코드:

.. code-block:: c

        OGRFeatureH hFeature;

        hFeature = OGR_F_Create( OGR_L_GetLayerDefn( hLayer ) );
        OGR_F_SetFieldString( hFeature, OGR_F_GetFieldIndex(hFeature, "Name"), szName );

로컬 도형 객체를 생성하고 피처에 그 복사본을 (간접적으로) 할당했습니다. :cpp:func:`OGRFeature::SetGeometryDirectly` 함수는 직접 할당 방법이 피처에게 도형의 소유권을 넘겨준다는 점에서 :cpp:func:`OGRFeature::SetGeometry` 함수와 다릅니다. 후자가 매우 심도 있는 도형 복사를 방지하기 때문에 일반적으로 더 효율적입니다.

C++ 코드:

.. code-block:: c++

        OGRPoint pt;
        pt.setX( x );
        pt.setY( y );

        poFeature->SetGeometry( &pt );

C 코드:

.. code-block:: c

        OGRGeometryH hPt;
        hPt = OGR_G_CreateGeometry(wkbPoint);
        OGR_G_SetPoint_2D(hPt, 0, x, y);

        OGR_F_SetGeometry( hFeature, hPt );
        OGR_G_DestroyGeometry(hPt);

이제 파일에 피처를 생성합니다. :cpp:func:`OGRLayer::CreateFeature` 함수는 피처의 소유권을 가져가지 않기 때문에 피처 생성 후 피처를 정리해줘야 합니다.

C++ 코드:

.. code-block:: c++

        if( poLayer->CreateFeature( poFeature ) != OGRERR_NONE )
        {
            printf( "Failed to create feature in shapefile.\n" );
           exit( 1 );
        }

        OGRFeature::DestroyFeature( poFeature );
   }

C 코드:

.. code-block:: c

        if( OGR_L_CreateFeature( hLayer, hFeature ) != OGRERR_NONE )
        {
            printf( "Failed to create feature in shapefile.\n" );
           exit( 1 );
        }

        OGR_F_Destroy( hFeature );
   }

마지막으로 헤더가 순서대로 작성되도록 그리고 모든 리소스를 복구하도록 데이터소스를 종료해야 합니다.

C/C++ 코드:

.. code-block:: c

        GDALClose( poDS );
    }

이 코드들을 모두 합친 프로그램은 다음과 같이 보일 것입니다.

C++ 코드:

.. code-block:: c++

    #include "ogrsf_frmts.h"

    int main()
    {
        const char *pszDriverName = "ESRI Shapefile";
        GDALDriver *poDriver;

        GDALAllRegister();

        poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName );
        if( poDriver == NULL )
        {
            printf( "%s driver not available.\n", pszDriverName );
            exit( 1 );
        }

        GDALDataset *poDS;

        poDS = poDriver->Create( "point_out.shp", 0, 0, 0, GDT_Unknown, NULL );
        if( poDS == NULL )
        {
            printf( "Creation of output file failed.\n" );
            exit( 1 );
        }

        OGRLayer *poLayer;

        poLayer = poDS->CreateLayer( "point_out", NULL, wkbPoint, NULL );
        if( poLayer == NULL )
        {
            printf( "Layer creation failed.\n" );
            exit( 1 );
        }

        OGRFieldDefn oField( "Name", OFTString );

        oField.SetWidth(32);

        if( poLayer->CreateField( &oField ) != OGRERR_NONE )
        {
            printf( "Creating Name field failed.\n" );
            exit( 1 );
        }

        double x, y;
        char szName[33];

        while( !feof(stdin)
            && fscanf( stdin, "%lf,%lf,%32s", &x, &y, szName ) == 3 )
        {
            OGRFeature *poFeature;

            poFeature = OGRFeature::CreateFeature( poLayer->GetLayerDefn() );
            poFeature->SetField( "Name", szName );

            OGRPoint pt;

            pt.setX( x );
            pt.setY( y );

            poFeature->SetGeometry( &pt );

            if( poLayer->CreateFeature( poFeature ) != OGRERR_NONE )
            {
                printf( "Failed to create feature in shapefile.\n" );
                exit( 1 );
            }

            OGRFeature::DestroyFeature( poFeature );
        }

        GDALClose( poDS );
    }

C 코드:

.. code-block:: c

    #include "gdal.h"

    int main()
    {
        const char *pszDriverName = "ESRI Shapefile";
        GDALDriverH hDriver;
        GDALDatasetH hDS;
        OGRLayerH hLayer;
        OGRFieldDefnH hFieldDefn;
        double x, y;
        char szName[33];

        GDALAllRegister();

        hDriver = GDALGetDriverByName( pszDriverName );
        if( hDriver == NULL )
        {
            printf( "%s driver not available.\n", pszDriverName );
            exit( 1 );
        }

        hDS = GDALCreate( hDriver, "point_out.shp", 0, 0, 0, GDT_Unknown, NULL );
        if( hDS == NULL )
        {
            printf( "Creation of output file failed.\n" );
            exit( 1 );
        }

        hLayer = GDALDatasetCreateLayer( hDS, "point_out", NULL, wkbPoint, NULL );
        if( hLayer == NULL )
        {
            printf( "Layer creation failed.\n" );
            exit( 1 );
        }

        hFieldDefn = OGR_Fld_Create( "Name", OFTString );

        OGR_Fld_SetWidth( hFieldDefn, 32);

        if( OGR_L_CreateField( hLayer, hFieldDefn, TRUE ) != OGRERR_NONE )
        {
            printf( "Creating Name field failed.\n" );
            exit( 1 );
        }

        OGR_Fld_Destroy(hFieldDefn);

        while( !feof(stdin)
            && fscanf( stdin, "%lf,%lf,%32s", &x, &y, szName ) == 3 )
        {
            OGRFeatureH hFeature;
            OGRGeometryH hPt;

            hFeature = OGR_F_Create( OGR_L_GetLayerDefn( hLayer ) );
            OGR_F_SetFieldString( hFeature, OGR_F_GetFieldIndex(hFeature, "Name"), szName );

            hPt = OGR_G_CreateGeometry(wkbPoint);
            OGR_G_SetPoint_2D(hPt, 0, x, y);

            OGR_F_SetGeometry( hFeature, hPt );
            OGR_G_DestroyGeometry(hPt);

            if( OGR_L_CreateFeature( hLayer, hFeature ) != OGRERR_NONE )
            {
            printf( "Failed to create feature in shapefile.\n" );
            exit( 1 );
            }

            OGR_F_Destroy( hFeature );
        }

        GDALClose( hDS );
    }

파이썬 코드:

.. code-block:: python

    import sys
    from osgeo import gdal
    from osgeo import ogr
    import string

    driverName = "ESRI Shapefile"
    drv = gdal.GetDriverByName( driverName )
    if drv is None:
        print "%s driver not available.\n" % driverName
        sys.exit( 1 )

    ds = drv.Create( "point_out.shp", 0, 0, 0, gdal.GDT_Unknown )
    if ds is None:
        print "Creation of output file failed.\n"
        sys.exit( 1 )

    lyr = ds.CreateLayer( "point_out", None, ogr.wkbPoint )
    if lyr is None:
        print "Layer creation failed.\n"
        sys.exit( 1 )

    field_defn = ogr.FieldDefn( "Name", ogr.OFTString )
    field_defn.SetWidth( 32 )

    if lyr.CreateField ( field_defn ) != 0:
        print "Creating Name field failed.\n"
        sys.exit( 1 )

    # 사용자 입력물의 예상 서식: x y name
    linestring = raw_input()
    linelist = string.split(linestring)

    while len(linelist) == 3:
        x = float(linelist[0])
        y = float(linelist[1])
        name = linelist[2]

        feat = ogr.Feature( lyr.GetLayerDefn())
        feat.SetField( "Name", name )

        pt = ogr.Geometry(ogr.wkbPoint)
        pt.SetPoint_2D(0, x, y)

        feat.SetGeometry(pt)

        if lyr.CreateFeature(feat) != 0:
            print "Failed to create feature in shapefile.\n"
            sys.exit( 1 )

        feat.Destroy()

        linestring = raw_input()
        linelist = string.split(linestring)

    ds = None

피처 하나에 도형 필드 여러 개를 연결시킬 수 있습니다. 이 케이퍼빌리티는 PostGIS 같은 몇몇 파일 포맷에 대해서만 사용할 수 있습니다.

이런 데이터소스를 생성하려면, 먼저 도형 필드들을 생성해야만 합니다. 각 도형 필드에 공간 좌표계 객체를 연결시킬 수 있습니다.

C++ 코드:

.. code-block:: c++

    OGRGeomFieldDefn oPointField( "PointField", wkbPoint );
    OGRSpatialReference* poSRS = new OGRSpatialReference();
    poSRS->importFromEPSG(4326);
    oPointField.SetSpatialRef(poSRS);
    poSRS->Release();

    if( poLayer->CreateGeomField( &oPointField ) != OGRERR_NONE )
    {
        printf( "Creating field PointField failed.\n" );
        exit( 1 );
    }

    OGRGeomFieldDefn oFieldPoint2( "PointField2", wkbPoint );
    poSRS = new OGRSpatialReference();
    poSRS->importFromEPSG(32631);
    oPointField2.SetSpatialRef(poSRS);
    poSRS->Release();

    if( poLayer->CreateGeomField( &oPointField2 ) != OGRERR_NONE )
    {
        printf( "Creating field PointField2 failed.\n" );
        exit( 1 );
    }

C 코드:

.. code-block:: c

    OGRGeomFieldDefnH hPointField;
    OGRGeomFieldDefnH hPointField2;
    OGRSpatialReferenceH hSRS;

    hPointField = OGR_GFld_Create( "PointField", wkbPoint );
    hSRS = OSRNewSpatialReference( NULL );
    OSRImportFromEPSG(hSRS, 4326);
    OGR_GFld_SetSpatialRef(hPointField, hSRS);
    OSRRelease(hSRS);

    if( OGR_L_CreateGeomField( hLayer, hPointField ) != OGRERR_NONE )
    {
        printf( "Creating field PointField failed.\n" );
        exit( 1 );
    }

    OGR_GFld_Destroy( hPointField );

    hPointField2 = OGR_GFld_Create( "PointField2", wkbPoint );
    OSRImportFromEPSG(hSRS, 32631);
    OGR_GFld_SetSpatialRef(hPointField2, hSRS);
    OSRRelease(hSRS);

    if( OGR_L_CreateGeomField( hLayer, hPointField2 ) != OGRERR_NONE )
    {
        printf( "Creating field PointField2 failed.\n" );
        exit( 1 );
    }

    OGR_GFld_Destroy( hPointField2 );

디스크에 피처를 작성하려면 레이어에 작성하기 전에 로컬 :cpp:class:`OGRFeature` 를 생성하고 속성을 설정한 다음 도형을 추가해야만 합니다. 이 피처가 작성될 레이어와 연결되어 있는 :cpp:class:`OGRFeatureDefn` 으로부터 이 피처를 인스턴스화해야만 합니다.

C++ 코드:

.. code-block:: c++

        OGRFeature *poFeature;
        OGRGeometry *poGeometry;
        char* pszWKT;

        poFeature = OGRFeature::CreateFeature( poLayer->GetLayerDefn() );

        pszWKT = (char*) "POINT (2 49)";
        OGRGeometryFactory::createFromWkt( &pszWKT, NULL, &poGeometry );
        poFeature->SetGeomFieldDirectly( "PointField", poGeometry );

        pszWKT = (char*) "POINT (500000 4500000)";
        OGRGeometryFactory::createFromWkt( &pszWKT, NULL, &poGeometry );
        poFeature->SetGeomFieldDirectly( "PointField2", poGeometry );

        if( poLayer->CreateFeature( poFeature ) != OGRERR_NONE )
        {
            printf( "Failed to create feature.\n" );
            exit( 1 );
        }

        OGRFeature::DestroyFeature( poFeature );

C 코드:

.. code-block:: c

        OGRFeatureH hFeature;
        OGRGeometryH hGeometry;
        char* pszWKT;

        poFeature = OGR_F_Create( OGR_L_GetLayerDefn(hLayer) );

        pszWKT = (char*) "POINT (2 49)";
        OGR_G_CreateFromWkt( &pszWKT, NULL, &hGeometry );
        OGR_F_SetGeomFieldDirectly( hFeature,
            OGR_F_GetGeomFieldIndex(hFeature, "PointField"), hGeometry );

        pszWKT = (char*) "POINT (500000 4500000)";
        OGR_G_CreateFromWkt( &pszWKT, NULL, &hGeometry );
        OGR_F_SetGeomFieldDirectly( hFeature,
            OGR_F_GetGeomFieldIndex(hFeature, "PointField2"), hGeometry );

        if( OGR_L_CreateFeature( hFeature ) != OGRERR_NONE )
        {
            printf( "Failed to create feature.\n" );
            exit( 1 );
        }

        OGR_F_Destroy( hFeature );

파이썬 코드:

.. code-block:: python

        feat = ogr.Feature( lyr.GetLayerDefn() )

        feat.SetGeomFieldDirectly( "PointField",
            ogr.CreateGeometryFromWkt( "POINT (2 49)" ) )
        feat.SetGeomFieldDirectly( "PointField2",
            ogr.CreateGeometryFromWkt( "POINT (500000 4500000)" ) )

        if lyr.CreateFeature( feat ) != 0:
            print( "Failed to create feature.\n" );
            sys.exit( 1 );

