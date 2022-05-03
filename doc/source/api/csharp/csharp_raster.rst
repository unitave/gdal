.. _csharp_raster:

================================================================================
C# 래스터 인터페이스
================================================================================

GDAL C# 인터페이스는 C# 응용 프로그램과 GDAL 간의 래스터 데이터 전송을 지원합니다.

다양한 :file:`Band.ReadRaster`, :file:`Band.WriteRaster`, :file:`Dataset.ReadRaster`, :file:`Dataset.WriteRaster` 오버로드(overload) 들이 응용 프로그램의 관리 부분과 비관리 부분 간의 래스터 데이터 전송에 관여하고 있습니다.

이 페이지에서는 특히 C# 인터페이스에 관련된 래스터 데이터 처리의 주요 측면을 요약할 것입니다.

:file:`Band` 클래스는 다음 :file:`ReadRaster`/:file:`WriteRaster` 오버로드들을 담고 있습니다:

.. code-block:: C#

    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, byte[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, byte[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, short[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, short[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, int[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, int[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, float[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, float[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, double[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, double[] buffer, 
        int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace){}
        
    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, IntPtr buffer, i
        nt buf_xSize, int buf_ySize, DataType buf_type, int pixelSpace, int lineSpace){}
  
    public CPLErr WriteRaster(int xOff, int yOff, int xSize, int ySize, IntPtr buffer, 
        int buf_xSize, int buf_ySize, DataType buf_type, int pixelSpace, int lineSpace){}

이 함수들 사이의 유일한 차이점은 버퍼 파라미터의 실제 유형뿐입니다. 마지막 두 오버로드는 일반 오버로드로, 호출자가 래스터 데이터를 담고 있는 버퍼에 대한 적절한 정렬(marshaling) 코드를 작성해야 합니다. C# 배열을 버퍼 파라미터로 가지고 있는 오버로드는 호출자에 적절한 정렬 코드를 구현합니다.

래스터 이미지 읽어오기
----------------------

GDAL로부터 래스터 데이터를 읽어올 때, 사용자가 데이터의 C# 표현을 담을 .NET 이미지를 생성할 수도 있습니다. 래스터 데이터를 직접 또는 버퍼를 이용해서 읽어올 수 있습니다.

버퍼 이용 읽기 접근법 사용하기
++++++++++++++++++++++++++++++

이미지를 이 방법으로 읽어오는 경우 C# API가 C 배열과 C# 배열 간에 이미지 데이터를 복사할 것입니다:

.. code-block:: C#

    // GDAL 이미지를 저장할 비트맵 생성
    Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format32bppRgb);
    // 이미지 데이터를 담을 C# 배열 생성
    byte[] r = new byte[width * height];
    band.ReadRaster(0, 0, width, height, r, width, height, 0, 0);
    // C# 비트맵에 픽셀 복사
    int i, j;
    for (i = 0; i< width; i++) 
    {
        for (j=0; j<height; j++)
        {
            Color newColor = Color.FromArgb(Convert.ToInt32(r[i+j*width]),Convert.ToInt32(r[i+j*width]), Convert.ToInt32(r[i+j*width]));
                    bitmap.SetPixel(i, j, newColor);
        }
    }

이 경우 인터페이스 구현이 내부적으로 생성된 비관리 배열을 이용해서 코드의 C 부분과 C++ 부분 간에 데이터를 다음과 같이 전송합니다:

.. code-block:: C#

    public CPLErr ReadRaster(int xOff, int yOff, int xSize, int ySize, byte[] buffer, int buf_xSize, int buf_ySize, int pixelSpace, int lineSpace) {
        CPLErr retval;
        IntPtr ptr = Marshal.AllocHGlobal(buf_xSize * buf_ySize * Marshal.SizeOf(buffer[0]));
        try {
            retval = ReadRaster(xOff, yOff, xSize, ySize, ptr, buf_xSize, buf_ySize, DataType.GDT_Byte, pixelSpace, lineSpace);
            Marshal.Copy(ptr, buffer, 0, buf_xSize * buf_ySize);
        } finally {
            Marshal.FreeHGlobal(ptr);
        }
        GC.KeepAlive(this);
        return retval;
    }

직접 읽기 접근법 사용하기
+++++++++++++++++++++++++

다음과 같은 접근법을 사용해서 C# 비트맵에 래스터 데이터를 직접 읽어올 수 있습니다:

.. code-block:: C#

    // GDAL 이미지를 저장할 비트맵 생성
    Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format8bppIndexed);
    // 비트맵 버퍼 가져오기
    BitmapData bitmapData = bitmap.LockBits(new Rectangle(0, 0, width, height), ImageLockMode.ReadWrite, PixelFormat.Format8bppIndexed);
    try 
    {
        int stride = bitmapData.Stride;
        IntPtr buf = bitmapData.Scan0;
        band.ReadRaster(0, 0, width, height, buf, width, height, DataType.GDT_Byte, 1, stride);
    }
    finally 
    {
        bitmap.UnlockBits(bitmapData);
    }

이 접근법이 앞의 접근법보다 성능면에서 좋습니다. 데이터를 전송하기 위해 중간(intermediary) 배열을 할당할 필요가 없기 때문입니다.

/unsafe 코드 및 고정 선언문 사용하기
++++++++++++++++++++++++++++++++++++

앞의 예시들에서는 프로그래머가 래스터 배열 용 정렬 코드를 굳이 구현하지 않아도 괜찮았습니다. 두 예시 모두 P/Invoke 호출을 실행하는 동안 가비지 수거기가 배열을 재배치하는 일을 방지하기 때문입니다. 프로그래머는 중간 배열을 사용하지 않고서도 다음과 같은 방법을 사용해서 래스터 데이터를 읽어올 수 있습니다:

.. code-block:: C#

    byte[] buffer = new byte[width * height];
    fixed (IntPtr ptr = buffer) {
    band.ReadRaster(0, 0, width, height, ptr, width, height, 1, width);
    }

이 접근법을 사용하는 경우 응용 프로그램을 :program:`/unsafe` 명령줄 옵션을 이용해서 컴파일해야만 합니다.

색인/회색조 이미지 사용하기
+++++++++++++++++++++++++++

:file:`PaletteInterp` 목록을 이용해서 다양한 유형의 이미지 색상 해석들을 구분할 수 있습니다:

.. code-block:: C#

    Band band = dataset.GetRasterBand(1);
    ColorTable ct = band.GetRasterColorTable();
    if (ct.GetPaletteInterpretation() == PaletteInterp.GPI_RGB)
    {
        Console.WriteLine("   This raster band has RGB palette interpretation!");
    }

색인된 색상 표현을 가진 이미지를 읽어오는 경우, 프로그래머가 다음과 같이 색상표를 복사하는 추가 작업을 해야 할 수도 있습니다:

.. code-block:: C#

    // 데이터셋으로부터 GDAL 밴드 객체 가져오기
    Band band = dataset.GetRasterBand(1);
    ColorTable ct = band.GetRasterColorTable();
    // GDAL 이미지를 저장할 비트맵 생성
    Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format8bppIndexed);
    // 비트맵 버퍼 가져오기
    BitmapData bitmapData = bitmap.LockBits(new Rectangle(0, 0, width, height), ImageLockMode.ReadWrite, PixelFormat.Format8bppIndexed);
    try 
        {
            int iCol = ct.GetCount();
            ColorPalette pal = bitmap.Palette;
            for (int i = 0; i < iCol; i++)
            {
                ColorEntry ce = ct.GetColorEntry(i);
                pal.Entries[i] = Color.FromArgb(ce.c4, ce.c1, ce.c2, ce.c3);
            }
            bitmap.Palette = pal;
                
            int stride = bitmapData.Stride;
            IntPtr buf = bitmapData.Scan0;

            band.ReadRaster(0, 0, width, height, buf, width, height, DataType.GDT_Byte, 1, stride);
            }
            finally 
            {
                bitmap.UnlockBits(bitmapData);
            }
        }

회색조 이미지를 읽어오는 경우, 프로그래머는 .NET 이미지를 위해 충분한 색상표를 생성해야 합니다:

.. code-block:: C#

    // 데이터셋으로부터 GDAL 밴드 객체 가져오기
    Band band = ds.GetRasterBand(1);
    // GDAL 이미지를 저장할 비트맵 생성
    Bitmap bitmap = new Bitmap(width, height, PixelFormat.Format8bppIndexed);
    // 비트맵 버퍼 가져오기
    BitmapData bitmapData = bitmap.LockBits(new Rectangle(0, 0, width, height), ImageLockMode.ReadWrite, PixelFormat.Format8bppIndexed);
    try 
        {
            ColorPalette pal = bitmap.Palette; 
            for(int i = 0; i < 256; i++) 
                pal.Entries[i] = Color.FromArgb( 255, i, i, i ); 
            bitmap.Palette = pal;
                
            int stride = bitmapData.Stride;
            IntPtr buf = bitmapData.Scan0;

            band.ReadRaster(0, 0, width, height, buf, width, height, DataType.GDT_Byte, 1, stride);
        }
        finally 
        {
            bitmap.UnlockBits(bitmapData);
        }

관련 C# 예시
++++++++++++

다음 예시들은 앞에서 설명한 GDAL 래스터 작업의 사용례를 보여줍니다:

-  `GDALRead.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/GDALRead.cs>`_
-  `GDALReadDirect.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/GDALReadDirect.cs>`_
-  `GDALWrite.cs <https://github.com/OSGeo/gdal/blob/master/swig/csharp/apps/GDALReadDirect.cs>`_

.. note::

   이 문서는 `https://trac.osgeo.org/gdal/wiki/GdalOgrCsharpRaster <https://trac.osgeo.org/gdal/wiki/GdalOgrCsharpRaster>`_ 에 있는 이전 버전을 수정한 것입니다.

