.. _rfc-41:

====================================================
RFC 41 : OGR에서의 다중 도형 필드 지원
====================================================

요약
----

OGR 데이터 모델에 도형 필드를 여러 개 가지고 있는 피처를 위한 읽기/쓰기 지원을 추가합니다.

동기
----

OGR 데이터 모델은 현대 피처, 피처 정의 및 레이어 당 단일 도형 필드로 묶여 있습니다. 그러나 여러 데이터 포맷들이 다중 도형 필드를 지원합니다. OGC 단순 피처 사양 또한 레이어 하나 당 도형 필드 하나로 제한하고 있지 않습니다. (예를 들면 `OGC 06-104r4 "지리 정보를 위한 OpenGIS® 구현 표준 - 단순 피처 접근 - 2부: SQL 옵션 <https://portal.ogc.org/files/?artifact_id=25354>`_ 의 §7.1.4 단락을 참조하십시오.)

차선책은 있습니다 -- (현재 PostGIS 또는 SQLite 드라이버에서처럼) GEOMETRYCOLLECTION 도형 유형을 사용하거나 레이어에 있는 도형 열의 개수만큼의 레이어들을 노출시키는 것입니다. 이런 접근법들은 기껏해야 다음과 같은 한계를 가진 차선책들일 뿐입니다:

-  GEOMETRYCOLLECTION 접근법:
   각 하위 도형의 이름/의미를 알 수 있는 방법이 없습니다. 모든 하위 도형이 동일한 공간 좌표계로 표현되어야만 합니다. GEOMETRYCOLLECTION에 항상 동일한 개수의 하위 도형들이 있거나 일관된 도형 유형이 있다고 보장할 수 있는 방법이 없습니다.

-  도형 열 1개 당 레이어 1개 접근법:
   읽기 전용 시나리오인 경우에만 적절합니다. 쓰기 시나리오에서는 작동하지 않습니다.

이 RFC의 목적은 OGR 데이터 모델이 피처 한 개 당 도형 열 여러 개를 제대로 지원하도록 만드는 것입니다.

제안 해결책
-----------

(주의: 대안 해결책들도 연구했습니다. 이 RFC의 다음 단락에서 대한 해결책들을 설명합니다.)

한 마디로 말하자면 :cpp:class:`OGRFeatureDefn` 및 :cpp:class:`OGRFeature` 수준에서 속성 필드를 처리하는 것과 비슷하게 도형 필드들을 취급하지만, 개별적으로 유지할 것입니다. 속성 필드 및 도형 필드는 피처 정의에 자신만의 개별 색인을 가질 것입니다.

새 케이퍼빌리티를 제공하면서도 하위 호환성을 최대화하기 위해 이 해결책을 선택했습니다.

이를 위해 :cpp:class:`OGRGeomFieldDefn` 클래스를 생성하고, :cpp:class:`OGRFieldDefn`, :cpp:class:`OGRFeatureDefn`, :cpp:class:`OGRFeature` 및 :cpp:class:`OGRLayer` 클래스를 수정합니다.

OGRGeomFieldDefn 클래스
~~~~~~~~~~~~~~~~~~~~~~~

:cpp:class:`OGRGeomFieldDefn` 은 새로운 클래스입니다. 그 구조는 :cpp:class:`OGRFieldDefn` 클래스로부터 직접 영감을 받았습니다:

.. code-block:: cpp

   class CPL_DLL OGRGeomFieldDefn
   {
   protected:
           char                *pszName;
           OGRwkbGeometryType   eGeomType; /* wkbNone을 제외한 모든 값을 사용 가능 */
           OGRSpatialReference* poSRS;

           int                 bIgnore;

   public:
                               OGRGeomFieldDefn(char *pszName,
                                                OGRwkbGeometryType eGeomType);
           virtual            ~OGRGeomFieldDefn();

           void                SetName( const char * );
           const char         *GetNameRef();

           OGRwkbGeometryType  GetType();
           void                SetType( OGRwkbGeometryType eTypeIn );

           virtual OGRSpatialReference* GetSpatialRef();
           void                 SetSpatialRef(OGRSpatialReference* poSRS);

           int                 IsIgnored();
           void                SetIgnored( int bIgnoreIn );
   };

멤버 변수들이 예전에 :cpp:class:`OGRLayer` 수준에서 찾아볼 수 있던 멤버들이라는 사실을 알 수 있습니다.

공간 좌표계 객체의 개수를 참조 개수로 셉니다. 참조 개수는 구성자(constructor) 및 SetSpatialRef()에서 증가하고 삭제자(destructor)에서 감소합니다.

의도적으로 GetSpatialRef()를 가상으로 설정했기 때문에 지연 평가(lazy evaluation)를 구현할 수 있습니다. (공간 좌표계를 가져오는 것은 -- 추가 파일을 읽어오거나 SQL 요청을 발행하는 것처럼 -- 일부 드라이버 구현에서 상당한 리소스를 사용할 수 있습니다.)

OGRFeatureDefn 클래스
~~~~~~~~~~~~~~~~~~~~~

:cpp:class:`OGRFeatureDefn` 클래스를 다음과 같이 확장할 것입니다:

.. code-block:: cpp

   class CPL_DLL OGRFeatureDefn
   {
     protected:
           // OGRwkbGeometryType eGeomType 및 bIgnoreGeometry를 제거하고
           // 그 대신 다음을 추가합니다:

           int nGeomFieldCount;
           OGRGeomFieldDefn* papoGeomFieldDefn;
     public:
           virtual int         GetGeomFieldCount();
           virtual OGRGeomFieldDefn *GetGeomFieldDefn( int i );
           virtual int         GetGeomFieldIndex( const char * );

           virtual void        AddGeomFieldDefn( OGRGeomFieldDefn * );
           virtual OGRErr      DeleteGeomFieldDefn( int iGeomField );

           // 첫 번째 도형 필드 정의에 OGRwkbGeometryType GetGeomType() 및
           // void SetGeomType()을 전송(route)합니다.

           // IsGeometryIgnored() 및 SetGeometryIgnored()에 대해서도 동일합니다.
   }

인스턴스화 단계에서 :cpp:class:`OGRFeatureDefn` 클래스가 이름이 ""이고 유형이 wkbUnknown인 기본 도형 필드 정의를 생성할 것입니다. SetGeomType()을 호출하는 경우, 이 기본 도형 필드 정의를 'papoGeomFieldDefn[0]' 상으로 전송할 것입니다. 도형 필드 정의가 하나만 존재한다면 ``SetGeomType(wkbNone)`` 이 해당 도형 필드 정의를 제거할 것입니다.

도형 유형이 존재하는 경우 GetGeomType()이 'papoGeomFieldDefn[0]' 상으로 전송될 것입니다. 그렇지 않다면 wkbNone을 반환할 것입니다.

정규 필드 이름들과 도형 필드 이름들의 합집합에서 이름 유일성(uniqueness)이 존재해야 한다고 강력하게 권고합니다. 동일한 이름이 2개 이상 존재할 경우 SQL 쿼리에서 지정한 적 없는 동작이 발생할 것입니다. 코드 수준에서 이 권고를 확인하지는 않을 것입니다. (현재 정규 필드에 대해서도 확인하고 있지 않습니다.)

필요한 경우 :cpp:class:`OGRFeatureDefn` 가상 클래스를 하위 클래스화시킬 수 있도록 이 클래스의 모든 기존 메소드에도 또다른 변경 사항을 적용할 것입니다. (그리고 개인(private) 가시성을 보호(protected) 가시성으로 변경할 것입니다.) 이렇게 하면 객체를 지연 생성(lazy creation)할 수 있습니다. 타당성: 완전한 피처 정의를 확립하는 데 리소스가 많이 사용될 수 있기 때문입니다. 그러나 응용 프로그램이 데이터소스의 모든 레이어들을 목록화한 다음 중요한 정보 몇 가지만 출력하려 할 수도 있는데, 이 경우 피처 정의를 확립하는 데 리소스가 많이 들지 않습니다. 예전에는 차선책으로써 :cpp:func:`OGRLayer::GetName` 및 :cpp:func:`OGRLayer::GetGeomType` 을 도입했습니다.

현재로서는 ReorderGeomFieldDefns()도 예상하고 있지 않는다는 사실을 기억하십시오. 이후 단계에서 추가할 수도 있지만, 먼저 그 필요성이 대두되어야 할 것입니다. DeleteGeomFieldDefn()은 주로 ``SetGeomType(wkbNone)`` 을 호출하는 경우 :cpp:class:`OGRFeatureDefn` 클래스 자체의 유용성을 위해 존재합니다.

OGRFeature 클래스
~~~~~~~~~~~~~~~~~

:cpp:class:`OGRFeature` 클래스를 다음과 같이 확장할 것입니다:

.. code-block:: cpp

   class CPL_DLL OGRFeature
   {
     private:
           // poGeometry 필드를 제거하고 그 대신 OGRGeometry** papoGeometries를 추가합니다.
           // poFDefn->GetGeomFieldCount()로 크기를 지정합니다.

     public:

           int                 GetGeomFieldCount();
           OGRGeomFieldDefn   *GetGeomFieldDefnRef( int iField );
           int                 GetGeomFieldIndex( const char * pszName);

           OGRGeometry*        GetGeomFieldRef(int iField);
           OGRErr              SetGeomFieldDirectly( int iField, OGRGeometry * );
           OGRErr              SetGeomField( int iField, OGRGeometry * );

           // 배열에 있는 첫 번째 도형 필드에 SetGeometryDirectly(), SetGeometry(),
           // GetGeometryRef(), StealGeometry()를 전송(route)합니다.

           // 모든 도형을 복제하기 위해 SetFrom()의 구현을 수정합니다.
   }

주의: RFC 41 이전에는, SetGeometry() 또는 SetGeometryDirectly()가 피처 정의가 'GetGeomType() == wkbNone'인 (일관성이 없는) 피처 상에서 작동할 수 있었습니다. 이제 papoGeometries 배열의 크기가 GetGeomFieldCount()를 기반으로 하기 때문에 더 이상 작동하지 않을 것입니다. 'GetGeomType() == wkbNone'인 경우 도형 필드 개수는 0이 되기 때문입니다. VRT 및 CSV 드라이버가 자신의 도형 유형을 일관되게 선언하도록 수정할 것입니다.

OGRLayer 클래스
~~~~~~~~~~~~~~~

:cpp:class:`OGRLayer` 클래스에 미치는 영향:

-  공간 필터:
   고려되는 선택지는 한 번에 하나의 공간 필터만 허용하는 것입니다.

   -  도형 필드 여러 개에 공간 필터를 동시에 적용해야 할 필요성이 분명하지 않습니다.
   -  OGR 코드베이스에서 'm_poFilterGeom' 보호(protected) 멤버를 250회 이상 사용하기 때문에 이를 전부 배열로 변환하는 작업이 매우 더딜 것입니다.

   추가 사항:

   .. code-block:: cpp

           protected:
               int m_iGeomFieldFilter // 공간 필터를 활성화할 색인을 지정합니다.

           public:
               virtual void        SetSpatialFilter( int iGeomField, OGRGeometry * );
               virtual void        SetSpatialFilterRect( int iGeomField,
                                                       double dfMinX, double dfMinY,
                                                       double dfMaxX, double dfMaxY );

-  GetNextFeature(): 
   도형 필드를 바르게 선택하려면 이 메소드의 구현이 m_iGeomFieldFilter 색인을 확인해야만 합니다.

-  GetGeomType():
   변경하지 않습니다. 다른 필드들의 경우, GetLayerDefn()->GetGeomField(i)->GetType()을 사용하십시오.

-  GetSpatialRef():
   기본 구현은 현재 NULL을 반환합니다. (도형 필드가 적어도 하나 이상 있는 경우) GetLayerDefn()->GetGeomField(0)->GetSpatialRef()를 반환하도록 변경할 것입니다. 새로운 드라이버들이 더 이상 GetSpatialRef()만 한정해서 사용하지 않고 첫 번째 도형 필드의 공간 좌표계를 적절하게 설정하도록 권장합니다.
   다른 필드들의 경우, GetLayerDefn()->GetGeomField(i)->GetSpatialRef()를 사용하십시오.

   주의할 점: 이전에 :cpp:class:`OGRFeatureDefn` 수준에서 공간 좌표계를 저장하지 않았기 때문에, 업데이트하지 않는 경우 GetGeomField(0)->GetSpatialRef()가 NULL을 반환하게 될 것입니다. test_ogrsf 유틸리티가 이를 확인하고 경고할 것입니다. 기존 드라이버들의 업데이트는 점진적으로 진행될 것입니다. 그 동안 첫 번째 도형 필드의 공간 좌표계를 신뢰할 수 있는 방식으로 가져오려면 :cpp:func:`OGRLayer::GetSpatialRef` 메소드를 사용할 것을 권고합니다.

-  추가 사항:

   .. code-block:: cpp

           virtual OGRErr GetExtent(int iGeomField, OGREnvelope *psExtent,
                                    int bForce = TRUE);

   'iGeomField == 0'인 경우 기본 구현이 GetExtent()를 호출할 것입니다.

-  추가 사항:

   .. code-block:: cpp

           virtual OGRErr CreateGeomField(OGRGeomFieldDefn *poField);

-  현재 DeleteGeomField(), ReorderGeomFields() 또는 AlterGeomFieldDefn()을 추가하지 않을 것입니다. 필요성이 대두되는 경우 향후 추가할 수 있습니다.

-  GetGeometryColumn():
   변경하지 않습니다. 첫 번째 도형 필드 상으로 전송합니다. 다른 필드들의 경우, GetLayerDefn()->GetGeomField(i)->GetNameRef()를 사용하십시오.

-  SetIgnoredFields():
   정규 필드들은 물론이고 도형 필드들도 반복합니다. 첫 번째 도형 필드에만 "OGR_GEOMETRY" 특수 값을 적용할 것입니다.

-  Intersection(), Union() 등등:
   변경하지 않습니다. 향후 대안 도형 필드를 지정하기 위해 papszOptions 파라미터를 사용하도록 개선할 수 있습니다.

-  TestCapability():
   CreateGeomField()를 구현했는지 여부를 알려주기 위한 OLCCreateGeomField 케이퍼빌리티를 추가합니다.

OGRDataSource 클래스
~~~~~~~~~~~~~~~~~~~~

:cpp:class:`OGRDataSource` 클래스에 미치는 영향:

-  CreateLayer():
   서명을 변경하지 않을 것입니다. 하나 이상의 도형 필드가 필요한 경우, :cpp:func:`OGRLayer::CreateGeomField` 를 사용해야만 합니다. ODsCCreateGeomFieldAfterCreateLayer를 지원하는 데이터소스를 위해 첫 번째 도형 필드의 이름을 지정해야만 하는 경우, CreateLayer()를 'eGType = wkbNone'으로 호출한 다음 :cpp:func:`OGRLayer::CreateGeomField` 를 이용해서 모든 도형 필드를 추가하는 코드를 사용해야 합니다.

-  CopyLayer():
   (대상 레이어가 지원하는 경우) 모든 도형 필드를 복제하도록 수정합니다.

-  ExecuteSQL():
   공간 필터를 입력받을 수 있게 변경합니다. 일반 OGR SQL 구현의 경우, 이 필터는 기능(facility)입니다. 반환되는 레이어 객체에 대해서도 적용할 수 있습니다. 즉 ExecuteSQL() API 수준에서 도형 필드를 지정하는 방법을 추가해야 할 필요가 없습니다.

-  TestCapability():
   레이어 생성 후 CreateGeomField()를 구현했는지 그리고 CreateLayer()를 'eGType = wkbNone'으로 안전하게 호출할 수 있는지 여부를 알려주는 ODsCCreateGeomFieldAfterCreateLayer 케이퍼빌리티를 추가합니다.

대안 해결책 탐색
----------------

(앞에서 자세히 설명한 제안 접근법을 완전히 확신한다면 이 단락을 건너뛰어도 상관없습니다. :-) )

가능한 대안 해결책 가운데 하나는 기존 :cpp:class:`OGRFieldDefn` 객체를 도형 관련 정보로 확장하는 것일 것입니다. 이를 위해 OGRFieldType 열거형(enumeration)에 OFTGeometry 값을 추가하고 :cpp:class:`OGRFieldDefn` 클래스에  OGRwkbGeometryType eGeomType 및 OGRSpatialReference\* poSRS 멤버를 추가해야 합니다.
:cpp:class:`OGRFeature` 클래스 수준에서 OGRField 합집합(union)을 OGRGeometry\* 필드로 확장할 수 있습니다. 마찬가지로 :cpp:class:`OGRLayer` 클래스 수준에서 CreateField()를 사용, 새 도형 필드를 생성할 수도 있습니다.

가장 네이티브한 방식으로 보이는 이 접근법의 주요 단점은 하위 호환성입니다. 이 접근법은 OGR 자체 코드 또는 외부 코드에서 필드를 검색하고 도형을 예상할 수 없는 모든 지점에 영향을 미칠 것입니다. 예를 들어 (대부분의 드라이버에 있는 CreateFeature()에서 또는 GetNextFeature()가 반환하는 피처를 입력받는 사용자 코드에서 매우 흔히 사용되는) 다음과 같은 코드에서 말입니다:

.. code-block:: cpp

   switch( poFieldDefn->GetType() )
   {
           case OFTInteger: something1(poField->GetFieldAsInteger()); break;
           case OFTReal: something2(poField->GetFieldAsDouble()): break;
           default: something3(poField->GetFieldAsString()); break;
   }

레거시 코드의 경우 이 접근법 때문에 도형을 정규 필드로 처리하게 되었을 것입니다. GetFieldAsString()를 이용해서 도형을 WKT로 변환시키면 된다고 상상해볼 수 있겠지만, 그것이 과연 바람직한지에 대해서는 의심할 수밖에 없습니다. 근본적으로, 거의 모든 사용례에서 속성 처리와 도형 필드 처리는 서로 다릅니다.

(다른 한 편으로 64비트 정수형을 OGR 유형으로 도입하는 경우 (해당 RFC는 구현 대기중입니다) 앞의 코드가 그래도 의미 있는 결과물을 생성할 것입니다. 64비트 정수형의 문자열 표현이 기본 습성만큼 나쁘지는 않기 때문입니다.)

GetFieldCount()도 도형 필드를 연산에 넣긴 하지만, 대부분의 경우 도형 필드는 제외해야 합니다.

앞에서 말한 호환성 문제점을 막을 수 있는 방법은 :cpp:class:`OGRFeatureDefn` 및 :cpp:class:`OGRFeature` 수준에서 도형 필드를 무시하는 현재 사용 중인 API와 도형 필드를 연산에 넣는 "확장" API 2개를 사용하는 것입니다. 예를 들면, :cpp:func:`OGRFeatureDefn::GetFieldCountEx`, :cpp:func:`OGRFeatureDefn::GetFieldIndexEx`, :cpp:func:`OGRFeatureDefn::GetFieldDefnEx`, :cpp:func:`OGRFeature::GetFieldEx`, :cpp:func:`OGRFeature::SetFieldAsXXXEx` 메소드들은 속성 필드와 도형 필드 둘 다 연산에 넣을 것입니다. 이 접근법의 짜증나는 점은 :cpp:class:`OGRFeature` 클래스에서 GetField() 및 SetFieldXXX() 메소드를 20개까지 복제한다는 점입니다.

C API
-----

C API에 다음 함수들을 추가합니다:

.. code-block:: c

   /* OGRGeomFieldDefnH */

   typedef struct OGRGeomFieldDefnHS *OGRGeomFieldDefnH;

   OGRGeomFieldDefnH    CPL_DLL OGR_GFld_Create( const char *, OGRwkbGeometryType ) CPL_WARN_UNUSED_RESULT;
   void                 CPL_DLL OGR_GFld_Destroy( OGRGeomFieldDefnH );

   void                 CPL_DLL OGR_GFld_SetName( OGRGeomFieldDefnH, const char * );
   const char           CPL_DLL *OGR_GFld_GetNameRef( OGRGeomFieldDefnH );

   OGRwkbGeometryType   CPL_DLL OGR_GFld_GetType( OGRGeomFieldDefnH );
   void                 CPL_DLL OGR_GFld_SetType( OGRGeomFieldDefnH, OGRwkbGeometryType );

   OGRSpatialReferenceH CPL_DLL OGR_GFld_GetSpatialRef( OGRGeomFieldDefnH );
   void                 CPL_DLL OGR_GFld_SetSpatialRef( OGRGeomFieldDefnH,
                                                        OGRSpatialReferenceH hSRS );

   int                  CPL_DLL OGR_GFld_IsIgnored( OGRGeomFieldDefnH hDefn );
   void                 CPL_DLL OGR_GFld_SetIgnored( OGRGeomFieldDefnH hDefn, int );

   /* OGRFeatureDefnH */

   int               CPL_DLL OGR_FD_GetGeomFieldCount( OGRFeatureDefnH hFDefn );
   OGRGeomFieldDefnH CPL_DLL OGR_FD_GetGeomFieldDefn( OGRFeatureDefnH hFDefn, int i );
   int               CPL_DLL OGR_FD_GetGeomFieldIndex( OGRFeatureDefnH hFDefn, const char * );

   void              CPL_DLL OGR_FD_AddGeomFieldDefn( OGRFeatureDefnH hFDefn, OGRGeomFieldDefnH );
   OGRErr            CPL_DLL OGR_FD_DeleteGeomFieldDefn( OGRFeatureDefnH hFDefn, int iGeomField );

   /* OGRFeatureH */

   int               CPL_DLL OGR_F_GetGeomFieldCount( OGRFeatureH hFeat );
   OGRGeomFieldDefnH CPL_DLL OGR_F_GetGeomFieldDefnRef( OGRFeatureH hFeat, int iField );
   int               CPL_DLL OGR_F_GetGeomFieldIndex( OGRFeatureH hFeat, const char * pszName);

   OGRGeometryH      CPL_DLL OGR_F_GetGeomFieldRef( OGRFeatureH hFeat, int iField );
   OGRErr            CPL_DLL OGR_F_SetGeomFieldDirectly( OGRFeatureH hFeat, int iField, OGRGeometryH );
   OGRErr            CPL_DLL OGR_F_SetGeomField( OGRFeatureH hFeat, int iField, OGRGeometryH );

   /* OGRLayerH */

   void     CPL_DLL OGR_L_SetSpatialFilterEx( OGRLayerH, int iGeomField, OGRGeometryH );
   void     CPL_DLL OGR_L_SetSpatialFilterRectEx( OGRLayerH, int iGeomField,
                                                  double dfMinX, double dfMinY,
                                                  double dfMaxX, double dfMaxY );
   OGRErr   CPL_DLL OGR_L_GetExtentEx( OGRLayerH, int iGeomField,
                                       OGREnvelope *psExtent, int bForce );
   OGRErr   CPL_DLL OGR_L_CreateGeomField( OGRLayerH, OGRGeomFieldDefnH hFieldDefn );

OGR SQL 엔진
------------

현재 ``SELECT fieldname1[, ...fieldnameN] FROM layername`` 이 지정한 필드는 물론 관련 도형까지 반환합니다. 이 습성은 도형 필드를 명확하게 지정해야만 하는 공간 RDBMS의 습성을 명백하게 따르고 있지 않습니다.

하위 호환성과 이 RFC의 새로운 케이퍼빌리티 간에 다음과 같은 절충안을 채택했습니다:

-  SELECT 절에서 어떤 도형 필드도 명확하게 지정하지 않고 레이어와 연결된 도형 필드가 하나뿐인 경우 암묵적으로 해당 도형 필드를 반환합니다.
-  그렇지 않은 경우 명확하게 지정한 도형 필드만 (또는 ``*`` 를 사용한 경우 모든 도형 필드를) 반환합니다.

제한 사항
~~~~~~~~~

-  현재로서는 결합(joined) 레이어들로부터 도형을 가져오지 않을 것입니다.

-  현재로서는 ``UNION ALL`` 이 기본 도형만 처리할 것입니다. (향후 작업을 통해 확장될 수 있습니다.)

-  OGR_GEOMETRY, OGR_GEOM_WKT 및 OGR_GEOM_AREA 특수 필드는 첫 번째 도형 필드 상에서 작업할 것입니다. 이 임시(ad-hoc) 문법을 확장하는 것은 현명하지 않을 듯합니다. 더 나은 대안은 (Spatialite를 지원하는) OGR SQLite 방언일 것입니다. 이 방언이 다중 도형 테이블을 지원하도록 업데이트한 다음에 말입니다. (이 업데이트는 이 RFC의 범위를 벗어납니다.)

드라이버
--------

이 RFC의 맥락에서 업데이트된 드라이버
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  PostGIS:

   -  임시 지원 형식이 이미 존재합니다. 현재 도형 필드를 여러 개 가진 테이블을 (도형 열 개수만큼 많은) "table_name(geometry_col_name)" 이라는 레이어들로 리포트합니다. 이 습성은 테이블을 OGR 레이어 하나로 한 번만 리포트하도록 변경될 것입니다.

-  PGDump:

   -  다중 도형 테이블에 대한 쓰기 지원을 추가할 것입니다.

-  Memory:

   -  새 케이퍼빌리티의 간단한 설명(illustration)으로 업데이트될 것입니다.

-  Interlis:

   -  도형 필드 여러 개를 지원하도록 (이 RFC와 관련없는 다른 변경 사항들과 함께) 업데이트될 것입니다.

기타 후보 드라이버 (이 RFC가 원래 커버하지 않는 업그레이드)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  GML:
   현재, 피처 하나당 도형 하나만 리포트합니다. .gfs 파일을 직접 편집해서 이를 변경할 수도 있습니다.
   --> 이 RFC 이후 GDAL 1.11버전에 구현했습니다.

-  SQLite:

   -  현재, 현재 PostGIS 드라이버와 동일한 습성을 보입니다.
   -  드라이버 및 SQLite 방언 둘 다 다중 도형 레이어를 지원하도록 업데이트할 수 있습니다.
      --> 이 RFC 이후 GDAL 2.0버전에 구현했습니다.

-  Google Fusion Tables:
   현재, 가장 처음 찾은 도형 열만 사용합니다.
   GetLayerByName()에 전송되는 레이어 이름으로 "table_name(geometry_column_name)"을 지정할 수도 있습니다.

-  VRT:
   다중 도형 테이블을 지원하는 문법을 찾는 데 숙고가 필요합니다. 영향을 받을 XML 문법은:

   -  OGRVRTLayer 요소 수준: GeometryType, LayerSRS, GeomField, SrcRegion, ExtentXMin/YMin/XMax/YMax
   -  OGRVRTWarpedLayer 요소 수준: 도형 필드를 선택할 수 있는 새 요소를 추가해야 합니다.
   -  OGRVRTUnionLayer 요소 수준: GeometryType, LayerSRS, ExtentXMin/YMin/XMax/YMax
   
   --> 이 RFC 이후 GDAL 1.11버전에 구현했습니다.

-  CSV:
   현재, "WKT"라는 이름의 열로부터 도형을 가져옵니다. 도형 열 여러 개를 지원하도록 확장해야 하는데 그럴 가치가 있는지 확실하지 않습니다. 확장된 VRT 드라이버로 지원할 수 있기 때문입니다.
   --> 이 RFC 이후 GDAL 1.11버전에 구현했습니다.

-  WFS:
   현재 단일 도형 레이어만 지원합니다. 표준 사양은 다중 도형 레이어도 지원합니다. 먼저 GML 드라이버 지원이 필요할 것입니다.

-  기타 RDBMS 기반 드라이버들:
   MySQL? MSSQLSpatial? Oracle Spatial?

유틸리티
--------

ogrinfo
~~~~~~~

ogrinfo가 다중 도형 필드 지원 관련 정보를 리포트하도록 업데이트할 것입니다. 업데이트된 유틸리티의 산출물은 단일 도형 데이터소스의 경우 현재 산출물과 비교해서 변하지 않을 것으로 예상됩니다.

다중 도형 데이터소스의 경우 다음과 같은 산출물이 예상됩니다:

::

   $ ogrinfo PG:dbname=mydb
   INFO: Open of `PG:dbname=mydb'
         using driver `PostgreSQL' successful.
   1: test_multi_geom (Polygon, Point)

::

   $ ogrinfo PG:dbname=mydb -al
   INFO: Open of `PG:dbname=mydb'
         using driver `PostgreSQL' successful.

   Layer name: test_multi_geom
   Geometry (polygon_geometry): Polygon
   Geometry (centroid_geometry): Point
   Feature Count: 10
   Extent (polygon_geometry): (400000,4500000) - (500000, 5000000)
   Extent (centroid_geometry): (2,48) - (3,49)
   Layer SRS WKT (polygon_geometry):
   PROJCS["WGS 84 / UTM zone 31N",
       GEOGCS["WGS 84",
           DATUM["WGS_1984",
               SPHEROID["WGS 84",6378137,298.257223563,
                   AUTHORITY["EPSG","7030"]],
               AUTHORITY["EPSG","6326"]],
           PRIMEM["Greenwich",0,
               AUTHORITY["EPSG","8901"]],
           UNIT["degree",0.0174532925199433,
               AUTHORITY["EPSG","9122"]],
           AUTHORITY["EPSG","4326"]],
       PROJECTION["Transverse_Mercator"],
       PARAMETER["latitude_of_origin",0],
       PARAMETER["central_meridian",3],
       PARAMETER["scale_factor",0.9996],
       PARAMETER["false_easting",500000],
       PARAMETER["false_northing",0],
       UNIT["metre",1,
           AUTHORITY["EPSG","9001"]],
       AXIS["Easting",EAST],
       AXIS["Northing",NORTH],
       AUTHORITY["EPSG","32631"]]
   Layer SRS WKT (centroid_geometry):
   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0,
           AUTHORITY["EPSG","8901"]],
       UNIT["degree",0.0174532925199433,
           AUTHORITY["EPSG","9122"]],
       AUTHORITY["EPSG","4326"]]
   FID Column = ogc_fid
   Geometry Column 1 = polygon_geometry
   Geometry Column 2 = centroid_geometry
   area: Real
   OGRFeature(test_multi_geom):1
     area (Real) = 500
     polygon_geometry = POLYGON ((400000 4500000,400000 5000000,500000 5000000,500000 4500000,400000 4500000))
     centroid_geometry = POINT(2.5 48.5)

"-spat" 옵션이 어떤 필드에 적용되는지 지정하는 "-geomfield" 옵션을 추가할 것입니다.

ogr2ogr
~~~~~~~

개선 사항:

-  산출 레이어가 지원하는 경우 (OLCCreateGeomField 케이퍼빌리티) 다중 도형 레이어를 다중 도형 레이어로 변환할 것입니다. 지원하지 않는 경우, 첫 번째 도형만 변환합니다.

-  "-select" 옵션을 개선해서 속성 필드 이름만 지정한 경우 모든 입력 도형을 암묵적으로 선택할 것입니다. (하위 호환을 위한 습성입니다.) 하나 이상의 도형 필드 이름을 지정한 경우, 지정한 필드들만 선택할 것입니다.

-  "-spat" 옵션이 어떤 필드에 적용되는지 지정하는 "-geomfield" 옵션을 추가할 것입니다.

-  모든 도형 필드에 다양한 도형 변환(재투영, 자르기 등등)을 적용할 것입니다.

test_ogrsf
~~~~~~~~~~

몇몇 일관성 검증으로 개선시킬 것입니다:

-  OGRLayer::GetSpatialRef() == OGRFeatureDefn::GetGeomField(0)->GetSpatialRef()
-  OGRLayer::GetGeomType() == OGRFeatureDefn::GetGeomField(0)->GetGeomType()
-  OGRLayer::GetGeometryColumn() == OGRFeatureDefn::GetGeomField(0)->GetNameRef()

공간 필터 작업 테스트는 모든 도형 필드를 반복할 것입니다.

문서화
------

:ref:`vector_data_model` 및 :ref:`vector_api_tut` 문서에 함수 수준 문서화뿐만 아니라 새 케이퍼빌리티도 문서화될 것입니다.

파이썬 및 기타 언어 바인딩
--------------------------

새로운 C API가 SWIG 바인딩에 매핑될 것입니다. 새 C API는 파이썬 바인딩과만 테스트될 것입니다. 새로운 유형 매핑(typemap)이 예상되지는 않기 때문에, 다른 언어들과도 단도직입적으로 작동할 것입니다.

호환성
------

-  이 변경 사항들은 기존 API에 추가될 뿐이고 기존 습성은 유지될 것이기 때문에, 하위 호환성을 보장할 것입니다.

-  C++ ABI가 변경될 것입니다.

-  GDAL 1.10버전과 관련해서, PostGIS 드라이버에서의 도형을 여러 개 가진 테이블에 대한 습성이 변경될 것입니다.

구현
----

이벤 루올이 GDAL 1.11버전 배포판에 앞에서 설명한 변경 사항들을 구현할 것입니다.
다만 Interlis 드라이버의 업그레이드는 피르민 칼베러(Pirmin Kalberer)가 수행할 것입니다.

후원
----

`연방 지형 사무국(swisstopo), COGIS <https://www.swisstopo.admin.ch/en/swisstopo/organisation/cogis.html>`_ 이 이 작업을 후원했습니다.

Voting history
--------------

-  이벤 루올 +1
-  프랑크 바르메르담 +1
-  하워드 버틀러 +1
-  대니얼 모리셋 +1
-  세케레시 터마시 +1

