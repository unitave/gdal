.. _csharp_vector:

================================================================================
C# 벡터 및 공간 좌표계 인터페이스
================================================================================

기본 아키텍처
-------------

벡터 인터페이스는 :file:`OSGeo.OGR` 이름공간 안에 있으며 공간 좌표계 인터페이스는 :file:`OSGeo.OSR` 이름공간 안에 있습니다.

**주** 클래스들은 다음과 같습니다:

::

    OGR
    |
    |- DataSource
    |
    |- Layer
    |
    |- Feature
    |
    |- Geometry

::

    OSR
    |
    |- SpatialReference
    |
    |- CoordinateTransform

피처 도형에 접근하기
--------------------

기본 과정은 :file:`DataSource` => :file:`Layer` => :file:`Feature` => :file:`Geometry` 입니다.

데이터소스 열기
+++++++++++++++

:file:`DataSource` 가 OGR 소스를 (예: 파일명을) 둘러싸는데, 다음과 같이 생성됩니다:

.. code-block:: 

    /* -------------------------------------------------------------------- */
    /*      포맷(들) 등록                                                   */
    /* -------------------------------------------------------------------- */
    Ogr.RegisterAll();

    /* -------------------------------------------------------------------- */
    /*      데이터소스 열기                                                 */
    /* -------------------------------------------------------------------- */
    using (DataSource ds = Ogr.Open( "... add your own valid OGR source", 0 ))
    {
        if (ds == null) {
            // 오류 생성
        }
        // 여기에서 처리 수행
    }

레이어에 접근
+++++++++++++

각 :file:`DataSource` 는 다음과 같이 반복할 수 있는 레이어를 하나 이상 가질 것입니다:

.. code-block:: C#

    /* -------------------------------------------------------------------- */
    /*      레이어 반복하기                                                 */
    /* -------------------------------------------------------------------- */

    for( int iLayer = 0; iLayer < ds.GetLayerCount(); iLayer++ )
    {
        Layer layer = ds.GetLayerByIndex(iLayer);

        if( layer == null )
        {
            // 오류 생성
        }
        // 여기에서 처리 수행
    }

레이어의 피처에 접근
++++++++++++++++++++

각 :file:`Layer` 는 :file:`Feature` 를 0개 이상 가질 수 있습니다. 피처에는 다음과 같이 접근해야 합니다:

.. code-block:: C#

    layer.ResetReading();
    Feature f = null;
    do {
        f = layer.GetNextFeature();
        if (f != null)
            // 여기에서 처리 수행
    } while (f != null);

피처의 도형에 접근
++++++++++++++++++

.. code-block:: C#

    Geometry geom = feature.GetGeometryRef();
    wkbGeometryType type = geom.GetGeometryType();

:file:`Geometry` 객체는 내포되어 있기 때문에, 예를 들어:

-  :file:`wkbGeometryType.wkbTIN` 유형의 :file:`Geometry` 은 :file:`wkbGeometryType.wkbTriangle` 유형의 하위 :file:`Geometry` 객체를 여러 개 가집니다.
-  :file:`wkbGeometryType.wkbTriangle` 유형의 각 :file:`Geometry` 객체는 :file:`wkbGeometryType.LinearRing` 유형의 하위 :file:`Geometry` 객체를 가집니다.
-  :file:`wkbGeometryType.LinearRing` 유형의 각 :file:`Geometry` 는 포인트를 여러 개 담고 있습니다.

가장 기본적인 유형에 도달했을 때 -- 보통 :file:`wkbGeometryType.wkbPoint`, :file:`wkbGeometryType.wkbLineString` 또는 :file:`wkbGeometryType.wkbLinearRing` 유형, 또는 이 유형들의 다중 버전, 25D 버전 또는 ZM 버전이 나타나는 경우 -- 다음과 같이 포인트 좌표에 접근할 수 있습니다:

.. code-block:: C#

    int count = geom.GetPointCount();
    if (count > 0)
        for (int i = 0; i < count; i++) {
            double[] argout = new double[3];
            geom.GetPoint(i, argout);
            // 여기에서 처리 수행
        }

.. note::

   :file:`double[]` 의 값은 :file:`Geometry` 의 차원 개수에 따라 달라집니다.

피처의 데이터 필드에 접근
+++++++++++++++++++++++++

각 :file:`Feature` 객체는 관련된 데이터 필드 여러 개를 가질 수 있습니다. 이 데이터 필드에 대한 스키마는 :file:`FieldDefn` 객체에 정의됩니다. 이런 필드를 다음과 같이 가져올 수 있습니다:

.. code-block:: C#

    Dictionary<string, object> ret = new Dictionary<string, object>();
    if (feature != null) {
        int fieldCount = feature.GetFieldCount();
        for (int i = 0; i < fieldCount; i++) {
            FieldDefn fd = feature.GetFieldDefnRef(i);
            string key = fd.GetName();
            object value = null;
            FieldType ft = fd.GetFieldType();
            switch (ft) {
                case FieldType.OFTString:
                    value = feature.GetFieldAsString(i);
                    break;
                case FieldType.OFTReal:
                    value = feature.GetFieldAsDouble(i);
                    break;
                case FieldType.OFTInteger:
                    value = feature.GetFieldAsInteger(i);
                    break;
                // 가능한 필드 유형들 가운데 이것이 유일한 하위 집합이라는 사실을 기억하십시오
            }
            ret.Add(key, value);
        }
    }

도형 좌표계에 접근
++++++++++++++++++

:file:`Geometry` 에 좌표계(공간 좌표계)가 정의되어 있는 경우 다음과 같이 가져올 수 있습니다:

.. code-block:: C#

    SpatialReference crs = geom.GetSpatialReference()

:file:`SpatialReference` 는 좌표계/투영법을 표현하기 위한 주 클래스입니다. 이 좌표계는 예를 들면 터미널에 출력하기 위해 다음과 같이 WKT 문자열로 변환시킬 수 있습니다:

.. code-block:: C#

    string wkt;
    crs.ExportToWkt(out wkt, null);

.. note::

   레이어에 정의된 좌표계가 피처로 전파되지 않는 경우가 있습니다. 이 경우 다시 레이어를 참조해야 합니다.

도형 재투영
+++++++++++

:file:`Geometry` 에 무결한 :file:`SpatialReference` 가 정의되어 있다면, 다음과 같은 명령어를 사용해서 :file:`Geometry` 을 새 좌표계로 변환할 수 있습니다:

.. code-block:: C#

    if (geom.TransformTo(newProjection) != 0)
        throw new NotSupportedException("projection failed");

하지만 많은 경우 사용할 :file:`CoordinateTransform` 을 명확하게 정의하는 편이 낫습니다:

.. code-block:: C#

    SpatialReference from_crs = new SpatialReference(null) 
        // 메모: WKT로부터 정의하는 경우 'null'을 'wkt'로 대체하십시오
    from_crs.SetWellKnownGeogCS("EPSG:4326");
    
    SpatialReference to_crs = new SpatialReference(null);
    to_crs.ImportFromEPSG(27700);
    
    CoordinateTransform ct = new CoordinateTransform(from_crs, to_crs, new CoordinateTransformationOptions())
        // CoordinateTransformationOptions를 사용해서 작업 또는 관심 영역 등을 설정할 수 있습니다
    
    if (geom.Transform(ct) != 0)
        throw new NotSupportedException("projection failed");


관련 C# 예시
+++++++++++++++++++

다음 예시들은 앞에서 설명한 GDAL 벡터 작업의 사용례를 보여줍니다:

-  `ogrinfo.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/ogrinfo.cs>`_
-  `OGRLayerAlg.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/OGRLayerAlg.cs>`_
-  `OGRFeatureEdit.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/OGRFeatureEdit.cs>`_
-  `OSRTransform.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/OSRTransform.cs>`_
-  `GetCRSInfo.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/GetCRSInfo.cs>`_

