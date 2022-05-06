.. _gnm_api_tut:

================================================================================
지리 네트워크 모델 API 예제
================================================================================

.. highlight:: cpp

이 문서에서는 GNM C++ 클래스를 이용해서 네트워크를 작업하는 방법을 설명하려 합니다. GNM 클래스의 목적 및 구조를 이해하기 위해 :ref:`gnm_data_model` 을 먼저 읽어볼 것을 권장합니다.

네트워크 관리하기
-----------------

첫 예시에서는 공간 데이터 집합(``autotest\gnm\data`` GDAL 소스 트리에 있는 수관(pipe) 및 수원(well) 2개의 shapefile)을 기반으로 작은 수로망(water network)을 생성할 것입니다. 공통 네트워크 포맷 -- :cpp:class:`GNMGdalNetwork` 클래스 -- 을 사용하면 이 네트워크를 위해 GDAL이 지원하는 벡터 포맷 가운데 하나를, 여기에서는 ESRI Shapefile을 선택할 수 있습니다. 수로망을 생성한 다음 네트워크 위상을 직접 편집하기 위해 위상(topology)을 작성하고 추가 데이터인 펌프(pump) 레이어를 추가할 것입니다.

가장 먼저 GDAL 드라이버를 등록하고 몇몇 옵션을 (문자열 쌍을) 생성합니다. 네트워크 생성 도중 이 옵션들을 파라미터로 전송할 것입니다. 이때 네트워크의 이름을 생성합니다.

.. code-block::

    #include "gnm.h"
    #include <vector>

    int main ()
    {
        GDALAllRegister();

        char **papszDSCO = NULL;
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_NAME, "my_pipes_network");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_SRS, "EPSG:4326");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_DESCR, "My pipes network");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_FORMAT, "ESRI Shapefile");

몇몇 옵션은 필수적입니다. 네트워크 생성 도중 경로/이름, 네트워크 저장 포맷, 공간 좌표계(EPSG, WKT 등등)는 반드시 지정해야만 합니다. 이런 옵션에 따라 "네트워크 부분"을 가진 데이터셋을 생성하고 산출 네트워크를 반환할 것입니다.

.. code-block::

    GDALDriver *poDriver = GetGDALDriverManager()->GetDriverByName("GNMFile");
    GNMGenericNetwork* poDS = (GNMGenericNetwork*) poDriver->Create( "..\\network_data", 0, 0, 0, GDT_Unknown,
                                                       papszDSCO );
    CSLDestroy(papszDSCO);

이제 "시스템 레이어"로만 이루어진 비어 있는 네트워크를 생성했습니다. 이 네트워크를 피처로 가득 찬 "클래스 레이어"로 채워야 하기 때문에, 특정 외부 데이터셋을 열고 해당 데이터셋의 레이어를 네트워크로 복사해옵니다. :cpp:class:`GDALDataset` 클래스로부터 :cpp:class:`GNMNetwork` 클래스를 상속받기 때문에 "클래스 레이어"를 작업하기 위해 ``GDALDataset::`` 메소드를 사용한다는 사실을 기억하십시오.

.. code-block::

    GDALDataset *poSrcDS = (GDALDataset*) GDALOpenEx("..\\in_data",
                                    GDAL_OF_VECTOR | GDAL_OF_READONLY, NULL, NULL, NULL );

    OGRLayer *poSrcLayer1 = poSrcDS->GetLayerByName("pipes");
    OGRLayer *poSrcLayer2 = poSrcDS->GetLayerByName("wells");

    poDS->CopyLayer(poSrcLayer1, "pipes");
    poDS->CopyLayer(poSrcLayer2, "wells");

    GDALClose(poSrcDS);

복사가 성공했다면 피처로 가득 찼지만 위상은 없는 네트워크가 있을 것입니다. 네트워크에 피처를 추가하고 등록했지만 아직 서로 연결되어 있지 않습니다. 이제 네트워크 위상을 작성할 차례입니다. GNM에서는 직접 또는 자동 두 가지 방법으로 네트워크 위상을 작성할 수 있습니다. 대부분의 경우 자동 작성이 더 편리하지만, 조금씩 편집하기에는 직접 작성이 유용합니다. 자동 작성에는 파라미터가 몇 개 필요합니다 -- 위상 작업에 어떤 "클래스 레이어"를 사용할지(이 예제의 경우 선택한 두 레이어를 사용합니다), 스냅 작업 허용 오차, 직접 비용(direct cost) 및 역 비용(inverse cost), 방향을 지정해야만 합니다. 이 예제의 경우 0.00005입니다. 위상 작성이 성공했다면 네트워크의 그래프가 위상에 따른 연결로 채워질 것입니다.

.. code-block::

    printf("\nBuilding network topology ...\n");
    char **papszLayers = NULL;
    for(int i = 0; i < poDS->GetLayerCount(); ++i)
    {
        OGRLayer* poLayer = poDS->GetLayer(i);
        papszLayers = CSLAddString(papszLayers, poLayer->GetName() );
    }

    if(poGenericNetwork->ConnectPointsByLines(papszLayers, dfTolerance,
                                        dfDirCost, dfInvCost, eDir) != CE_None )
    {
        printf("Building topology failed\n");
    }
    else
    {
        printf("Topology has been built successfully\n");
    }

이제 위상 및 공간 데이터를 가진 네트워크가 준비되었습니다. 이 네트워크를 서로 다른 (분석, 다른 포맷으로 변환 등등) 목적으로 사용할 수 있습니다. 그러나 그 전에 네트워크의 일부 데이터를 수정해야 하는 경우가 있습니다. 예를 들면 추가적인 피처를 추가하고 작성된 위상에 추가해야 (위상을 수정해야) 할 수도 있습니다. 다음은 네트워크에 새 "클래스 레이어"를 생성하고 이 레이어에 피처 하나를 추가하는 예시입니다.

.. code-block::

    OGRLayer *poNewLayer = poDS->CreateLayer("pumps", , NULL, wkbPoint, NULL );
    if( poNewLayer == NULL )
    {
        printf( "Layer creation failed.\n" );
        exit( 1 );
    }

    OGRFieldDefn fieldDefn ("pressure",OFTReal);
    if( poNewLayer->CreateField( &fieldDefn ) != OGRERR_NONE )
    {
        printf( "Creating Name field failed.\n" );
        exit( 1 );
    }

    OGRFeature *poFeature = OGRFeature::CreateFeature(poNewLayer->GetLayerDefn());
    OGRPoint pt;
    pt.setX(37.291466);
    pt.setY(55.828351);
    poFeature->SetGeometry(&pt);
    if( poNewLayer->CreateFeature( poFeature ) != OGRERR_NONE )
    {
        printf( "Failed to create feature.\n" );
        exit( 1 );
    }

    GNMGFID gfid = poFeature->GetFID();

    OGRFeature::DestroyFeature( poFeature );

새 레이어를 성공적으로 생성했다면 네트워크에 새 피처가 등록되었을 것이고, 이를 다른 피처들과 연결시킬 수 있습니다. 두 가지 방법으로 피처들을 서로 연결시킬 수 있습니다. 첫 번째 방법은 연결에서 경계가 될 실제 피처가 필요합니다. 두 번째 방법은 이런 피처가 필요없고, :cpp:func:`GNMGenericNetwork::ConnectFeatures` 메소드에 이 연결을 위한 특수 시스템 경계를 생성해서 그래프에 자동으로 추가하라는 의미를 가진 -1을 전송하는 것입니다. 앞의 예시에서 포인트 피처 1개만 추가했고 경계가 될 라인은 추가하지 않았기 때문에, "가상" 연결을 사용할 것입니다. 포인트 피처의 GFID(Global Feature ID)를 소스로, 기존 피처 가운데 하나의 GFID를 대상으로, 그리고 -1을 연결자(connector)로 전송합니다. (직접 및 역) 비용과 경계의 방향도 직접 설정해서 그래프에 그 값들을 작성하게 만들 것이라는 사실을 기억하십시오. 자동 연결을 사용하는 경우 (이때도 내부적으로 :cpp:func:`ConnectFeatures` 를 사용합니다) 앞에서 설정했던 규칙에 따라 이런 값들을 자동으로 설정합니다.

.. code-block::

    if (poDS->ConnectFeatures(gfid ,63, -1, 5.0, 5.0, GNMDirection_SrcToTgt) != GNMError_None)
    {
        printf("Can not connect features\n");
    }

모두 끝났다면 네트워크를 정확하게 종료해서 할당된 리소스들을 해제합니다.

.. code-block::

    GDALClose(poDS);

이 코드들을 모두 합치면 다음과 같이 보일 것입니다:

.. code-block::

    #include "gnm.h"
    #include "gnm_priv.h"

    int main ()
    {
        GDALAllRegister();

        char **papszDSCO = NULL;
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_NAME, "my_pipes_network");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_SRS, "EPSG:4326");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_DESCR, "My pipes network");
        papszDSCO = CSLAddNameValue(papszDSCO, GNM_MD_FORMAT, "ESRI Shapefile");


        GDALDriver *poDriver = GetGDALDriverManager()->GetDriverByName("GNMFile");
        GNMGenericNetwork* poDS = (GNMGenericNetwork*) poDriver->Create( "..\\network_data", 0, 0, 0, GDT_Unknown,
                                                        papszDSCO );
        CSLDestroy(papszDSCO);
        if (poDS == NULL)
        {
            printf("Failed to create network\n");
            exit(1);
        }

        GDALDataset *poSrcDS = (GDALDataset*) GDALOpenEx("..\\in_data",GDAL_OF_VECTOR | GDAL_OF_READONLY, NULL, NULL, NULL );
        if(poSrcDS == NULL)
        {
            printf("Can not open source dataset at\n");
            exit(1);
        }

        OGRLayer *poSrcLayer1 = poSrcDS->GetLayerByName("pipes");
        OGRLayer *poSrcLayer2 = poSrcDS->GetLayerByName("wells");
        if (poSrcLayer1 == NULL || poSrcLayer2 == NULL)
        {
            printf("Can not process layers of source dataset\n");
            exit(1);
        }

        poDS->CopyLayer(poSrcLayer1, "pipes");
        poDS->CopyLayer(poSrcLayer2, "wells");

        GDALClose(poSrcDS);

        printf("\nBuilding network topology ...\n");
        char **papszLayers = NULL;
        for(int i = 0; i < poDS->GetLayerCount(); ++i)
        {
            OGRLayer* poLayer = poDS->GetLayer(i);
            papszLayers = CSLAddString(papszLayers, poLayer->GetName() );
        }

        if(poGenericNetwork->ConnectPointsByLines(papszLayers, dfTolerance,
                                            dfDirCost, dfInvCost, eDir) != CE_None )
        {
            printf("Building topology failed\n");
            exit(1);
        }
        else
        {
            printf("Topology has been built successfully\n");
        }

        OGRLayer *poNewLayer = poDS->CreateLayer("pumps", , NULL, wkbPoint, NULL );
        if( poNewLayer == NULL )
        {
            printf( "Layer creation failed.\n" );
            exit( 1 );
        }

        OGRFieldDefn fieldDefn ("pressure",OFTReal);
        if( poNewLayer->CreateField( &fieldDefn ) != OGRERR_NONE )
        {
            printf( "Creating Name field failed.\n" );
            exit( 1 );
        }

        OGRFeature *poFeature = OGRFeature::CreateFeature(poNewLayer->GetLayerDefn());
        OGRPoint pt;
        pt.setX(37.291466);
        pt.setY(55.828351);
        poFeature->SetGeometry(&pt);
        if( poNewLayer->CreateFeature( poFeature ) != OGRERR_NONE )
        {
            printf( "Failed to create feature.\n" );
            exit( 1 );
        }

        GNMGFID gfid = poFeature->GetFID();

        OGRFeature::DestroyFeature( poFeature );

        if (poDS->ConnectFeatures(gfid ,63, -1, 5.0, 5.0, GNMDirection_SrcToTgt) != GNMError_None)
        {
            printf("Can not connect features\n");
        }

        GDALClose(poDS);
    }

네트워크 분석하기
-----------------

두 번째 예시에서는 첫 번째 예시에서 작성했던 네트워크를 분석할 것입니다. 피처 차단(feature blocking)을 수행하는 데이크스트라(Dijkstra) 알고리즘을 통해 두 포인트 사이의 최단 경로를 계산한 다음, 파일에 산출되는 경로를 저장할 것입니다.

먼저 Shapefile 데이터셋을 가리키는 경로를 전송해서 네트워크를 엽니다.

.. code-block::

    #include "gnm.h"
    #include "gnm_priv.h"

    int main ()
    {
        GDALAllRegister();

        GNMGenericNetwork *poNet = (GNMGenericNetwork*) GDALOpenEx("..\\network_data",GDAL_OF_GNM | GDAL_OF_UPDATE, NULL, NULL, NULL );
        if(poSrcDS == NULL)
        {
            printf("Can not open source dataset at\n");
            exit(1);
        }

어떤 계산도 하기 전에, 산출 경로를 가진 레이어를 담게 될 데이터셋을 엽니다.

.. code-block::

        GDALDataset *poResDS;
        poResDS = (GDALDataset*) GDALOpenEx("..\\out_data",
                                            GDAL_OF_VECTOR | GDAL_OF_UPDATE,
                                            NULL, NULL, NULL);
        if (poResDS == NULL)
        {
            printf("Failed to open resulting dataset\n");
            exit(1);
        }

마지막으로 데이크스트라 최단 경로 메소드를 사용해서 계산합니다. 차단된 피처를 피해 이 경로를 찾고 내부 메모리 :cpp:class:`OGRLayer` 에 저장합니다. 이렇게 내부 메모리에 저장된 경로를 실제 데이터셋으로 복사합니다. 이제 GIS가 최단 경로를 가시화할 수 있습니다.

.. code-block::

        OGRLayer *poResLayer = poNet->GetPath(64, 41, GATDijkstraShortestPath, NULL);
        if (poResLayer == NULL)
        {
            printf("Failed to save or calculate path\n");
        }
        else if (poResDS->CopyLayer(poResLayer, "shp_tutorial.shp") == NULL)
        {
            printf("Failed to save path to the layer\n");
        }
        else
        {
            printf("Path saved successfully\n");
        }

        GDALClose(poResDS);
        poNet->ReleaseResultSet(poRout);
        GDALClose(poNet);
    }

이 코드들을 모두 합치면 다음과 같이 보일 것입니다:

.. code-block::

    #include "gnm.h"
    #include "gnmstdanalysis.h"

    int main ()
    {
        GDALAllRegister();

        GNMGenericNetwork *poNet = (GNMGenericNetwork*) GDALOpenEx("..\\network_data",
                                                        GDAL_OF_GNM | GDAL_OF_UPDATE,
                                                        NULL, NULL, NULL );
        if(poSrcDS == NULL)
        {
            printf("Can not open source dataset at\n");
            exit(1);
        }

        GDALDataset *poResDS;
        poResDS = (GDALDataset*) GDALOpenEx("..\\out_data",
                                            GDAL_OF_VECTOR | GDAL_OF_UPDATE,
                                            NULL, NULL, NULL);
        if (poResDS == NULL)
        {
            printf("Failed to open resulting dataset\n");
            exit(1);
        }

        poNet->ChangeBlockState(36, true);

        OGRLayer *poResLayer = poNet->GetPath(64, 41, GATDijkstraShortestPath, NULL);
        if (poResLayer == NULL)
        {
            printf("Failed to save or calculate path\n");
        }
        else if (poResDS->CopyLayer(poResLayer, "shp_tutorial.shp") == NULL)
        {
            printf("Failed to save path to the layer\n");
        }
        else
        {
            printf("Path saved successfully\n");
        }

        GDALClose(poResDS);
        poNet->ReleaseResultSet(poRout);
        GDALClose(poNet);
    }

