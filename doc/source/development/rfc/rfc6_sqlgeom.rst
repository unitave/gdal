.. _rfc-6:

=======================================================================================
RFC 6: OGR 특수 필드로서의 도형 및 피처 스타일
=======================================================================================

저자: 세케레시 터마시(Szekeres Tamás)

연락처: szekerest@gmail.com

상태: 승인

요약
----

이 제안은 오래 전 발견되었지만 OGR가 이제까지 대응하는 해결 방법을 제공하지 않은 문제점을 지적합니다.

Mapinfo.tab 같은 몇몇 지원 포맷은 도형 유형 및 스타일 정보 여러 개를 담을 수도 있습니다. 이런 종류의 데이터소스를 제대로 처리하려면 도형 유형 또는 스타일 정보로 레이어를 선택할 수 있는 기능을 반드시 지원해야 합니다. 더 자세한 정보는 이 문서 후반에 있는 MapServer 관련 버그를 참조하십시오.

모든 변경 사항 제안은 이 문서 후반에 있는 이 RFC에 대한 버그 추적에서 찾아볼 수 있습니다.

주요 개념
---------

이 기능을 지원할 수 있는 가장 합리적인 방법은 현재 하나 이상의 필드들을 지정할 수 있게 해주는 기존 '특수 필드' 접근법을 확장하는 것입니다. 이미 정의된 'FID' 필드에 더해 다음 필드들을 추가할 것입니다:

-  'OGR_GEOMETRY': 'POINT' 또는 'POLYGON' 같은 도형 유형을 담는 필드입니다.
-  'OGR_STYLE': 스타일 문자열을 담는 필드입니다.
-  'OGR_GEOM_WKT': 도형의 완전한 WKT를 담는 필드입니다.

이런 필드들을 지정하면, 예를 들어 다음과 같이 레이어를 선택할 수 있습니다:

-  ``select FID, OGR_GEOMETRY, OGR_STYLE, OGR_GEOM_WKT, * from MyTable where OGR_GEOMETRY='POINT' OR OGR_GEOMETRY='POLYGON'``
-  ``select FID, OGR_GEOMETRY, OGR_STYLE, OGR_GEOM_WKT, * from MyTable where OGR_STYLE LIKE '%BRUSH%'``
-  ``select FID, OGR_GEOMETRY, OGR_STYLE, OGR_GEOM_WKT, * from MyTable where OGR_GEOM_WKT LIKE 'POLYGON%'``
-  ``select distinct OGR_GEOMETRY from MyTable order by OGR_GEOMETRY desc``

구현
----

이 기능이 역할을 수행할 수 있는 두 가지 별개의 영역이 있습니다:

-  :file:`ogrfeaturequery.cpp` 에 구현된 피처 쿼리

-  :file:`ogr_gensql.cpp` 및 :file:`ogrdatasource.cpp` 에 구현된 SQL 기반 선택 작업

임의 개수의 특수 필드를 지정하려면, :file:`ogrfeaturequery.cpp` 에 필드명 및 유형을 위한 배열을 다음과 같이 선언합니다:

::

   char* SpecialFieldNames[SPECIAL_FIELD_COUNT] 
       = {"FID", "OGR_GEOMETRY", "OGR_STYLE", "OGR_GEOM_WKT"};
   swq_field_type SpecialFieldTypes[SPECIAL_FIELD_COUNT] 
       = {SWQ_INTEGER, SWQ_STRING, SWQ_STRING, SWQ_STRING};

따라서 다른 파일들이 이 배열에 접근할 수 있게 하려면 :file:`ogr_p.h` 에 다음 내용을 추가합니다:

::

   CPL_C_START
   #include "ogr_swq.h"
   CPL_C_END

   #define SPF_FID 0
   #define SPF_OGR_GEOMETRY 1
   #define SPF_OGR_STYLE 2
   #define SPF_OGR_GEOM_WKT 3
   #define SPECIAL_FIELD_COUNT 4

   extern char* SpecialFieldNames[SPECIAL_FIELD_COUNT];
   extern swq_field_type SpecialFieldTypes[SPECIAL_FIELD_COUNT];

필드 색인으로 특수 필드의 값을 지정해서 :file:`ogrfeature.cpp` 필드 접근자 함수(GetFieldAsInteger, GetFieldAsDouble, GetFieldAsString)를 수정할 것입니다.

:cpp:func:`OGRFeature::GetFieldAsInteger` 의 시작 부분에 다음 코드를 추가합니다:

::

   int iSpecialField = iField - poDefn->GetFieldCount();
   if (iSpecialField >= 0)
   {
   // 특수 필드 값 접근자
       switch (iSpecialField)
       {
       case SPF_FID:
           return GetFID();
       default:
           return 0;
       }
   }

:cpp:func:`OGRFeature::GetFieldAsDouble` 의 시작 부분에 다음 코드를 추가합니다:

::

   int iSpecialField = iField - poDefn->GetFieldCount();
   if (iSpecialField >= 0)
   {
   // 특수 필드 값 접근자
       switch (iSpecialField)
       {
       case SPF_FID:
           return GetFID();
       default:
           return 0.0;
       }
   }

:cpp:func:`OGRFeature::GetFieldAsString` 의 시작 부분에 다음 코드를 추가합니다:

::

   int iSpecialField = iField - poDefn->GetFieldCount();
   if (iSpecialField >= 0)
   {
   // 특수 필드 값 접근자
       switch (iSpecialField)
       {
       case SPF_FID:
           sprintf( szTempBuffer, "%d", GetFID() );
           return m_pszTmpFieldValue = CPLStrdup( szTempBuffer );
       case SPF_OGR_GEOMETRY:
           return poGeometry->getGeometryName();
       case SPF_OGR_STYLE:
           return GetStyleString();
       case SPF_OGR_GEOM_WKT:
           {
               if (poGeometry->exportToWkt( &m_pszTmpFieldValue ) == OGRERR_NONE )
                   return m_pszTmpFieldValue;
               else
                   return "";
           }
       default:
           return "";
       }
   }

현재 :cpp:func:`OGRFeature::GetFieldAsString` 구현은 코드 스레드를 안전하지 않게 만들기 때문에 피하는 편이 좋은 'const char\*' 반환값을 담기 위해 정적 문자열을 사용합니다. 이런 측면에서 'static char szTempBuffer[80]'을 비정적(non static)으로 변경하고 :file:`ogrfeature.h` 에 있는 :cpp:class:`OGRFeature` 에 새 멤버를 다음과 같이 추가할 것입니다:

::

   char * m_pszTmpFieldValue; 

구성자(constructor)가 이 멤버를 NULL로 초기화할 것이며, :cpp:class:`OGRFeature` 의 삭제자(destructor)가 CPLFree() 함수를 이용해서 해제할 것입니다.

:cpp:func:`OGRFeature::GetFieldAsString` 에서 'return szTempBuffer;'를 모두 'return m_pszTmpFieldValue = CPLStrdup( szTempBuffer );'로 변경할 것입니다.

:cpp:func:`OGRFeature::GetFieldAsString` 은 함수 시작 부분에서 'm_pszTmpFieldValue'의 예전 값을 삭제해야 합니다:

::

   CPLFree(m_pszTmpFieldValue);
   m_pszTmpFieldValue = NULL; 

:file:`ogrfeaturequery.cpp` 에서 :cpp:func:`OGRFeatureQuery::Compile` 이 특수 필드를 추가하도록 다음과 같이 변경해야 합니다:

::

   iField = 0;
   while (iField < SPECIAL_FIELD_COUNT)
   {
       papszFieldNames[poDefn->GetFieldCount() + iField] = SpecialFieldNames[iField];
       paeFieldTypes[poDefn->GetFieldCount() + iField] = SpecialFieldTypes[iField];
       ++iField;
   }

:file:`ogrfeaturequery.cpp` 에서 필드 특화 액션에 따라 OGRFeatureQueryEvaluator()를 다음과 같이 수정해야 합니다:

::

   int iSpecialField = op->field_index - poFeature->GetDefnRef()->GetFieldCount();
   if( iSpecialField >= 0 )
   {
       if ( iSpecialField < SPECIAL_FIELD_COUNT )
       {
           switch ( SpecialFieldTypes[iSpecialField] )
           {
           case SWQ_INTEGER:
               sField.Integer = poFeature->GetFieldAsInteger( op->field_index );
           case SWQ_STRING:
               sField.String = (char*) poFeature->GetFieldAsString( op->field_index );
           }      
       }
       else
       {
           CPLDebug( "OGRFeatureQuery", "Illegal special field index.");
           return FALSE;
       }
       psField = &sField;
   }
   else
       psField = poFeature->GetRawFieldRef( op->field_index );

:file:`ogrfeaturequery.cpp` 에서 :cpp:func:`OGRFeatureQuery::FieldCollector` 가 필드명을 추가하도록 다음과 같이 변경해야 합니다:

::

   if( op->field_index >= poTargetDefn->GetFieldCount()
           && op->field_index < poTargetDefn->GetFieldCount() + SPECIAL_FIELD_COUNT) 
           pszFieldName = SpecialFieldNames[op->field_index];

:file:`ogrdatasource.cpp` 에서 ExecuteSQL() 함수가 특수 필드의 개수에 따라 배열들을 할당할 것입니다:

::

   sFieldList.names = (char **) 
           CPLMalloc( sizeof(char *) * (nFieldCount+SPECIAL_FIELD_COUNT) );
   sFieldList.types = (swq_field_type *)  
           CPLMalloc( sizeof(swq_field_type) * (nFieldCount+SPECIAL_FIELD_COUNT) );
   sFieldList.table_ids = (int *) 
           CPLMalloc( sizeof(int) * (nFieldCount+SPECIAL_FIELD_COUNT) );
   sFieldList.ids = (int *) 
           CPLMalloc( sizeof(int) * (nFieldCount+SPECIAL_FIELD_COUNT) );

그러면 필드를 다음과 같이 추가할 것입니다:

::

   for (iField = 0; iField < SPECIAL_FIELD_COUNT; iField++)
   {
       sFieldList.names[sFieldList.count] = SpecialFieldNames[iField];
       sFieldList.types[sFieldList.count] = SpecialFieldTypes[iField];
       sFieldList.table_ids[sFieldList.count] = 0;
       sFieldList.ids[sFieldList.count] = nFIDIndex + iField;
       sFieldList.count++;
   }

SQL 기반 쿼리를 지원하기 위해 :file:`ogr_gensql.cpp` 에 있는 :cpp:class:`OGRGenSQLResultsLayer` 의 구성자도 수정하고 필드 유형을 알맞게 설정해야 합니다:

::

   else if ( psColDef->field_index >= iFIDFieldIndex )
   {
       switch ( SpecialFieldTypes[psColDef->field_index - iFIDFieldIndex] )
       {
       case SWQ_INTEGER:
           oFDefn.SetType( OFTInteger );
           break;
       case SWQ_STRING:
           oFDefn.SetType( OFTString );
           break;
       case SWQ_FLOAT:
           oFDefn.SetType( OFTReal );
           break;
       }
   }

일부 쿼리의 경우 :file:`ogr_gensql.cpp` 에 있는 :cpp:func:`OGRGenSQLResultsLayer::PrepareSummary` 를 수정해야 하기 때문에 단순화될 것입니다. (필드 값에 접근하기 위해 모든 경우에 GetFieldAsString을 사용할 것입니다):

::

   pszError = swq_select_summarize( psSelectInfo, iField, poSrcFeature->GetFieldAsString( psColDef->field_index ) );

기본 레코드(primary record)로부터 대상 피처로 필드를 복사하는 경우 :cpp:func:`OGRGenSQLResultsLayer::TranslateFeature` 도 수정해야 합니다:

::

    if ( psColDef->field_index >= iFIDFieldIndex &&
               psColDef->field_index < iFIDFieldIndex + SPECIAL_FIELD_COUNT )
   {
       switch (SpecialFieldTypes[psColDef->field_index - iFIDFieldIndex])
       {
       case SWQ_INTEGER:
           poDstFeat->SetField( iField, poSrcFeat->GetFieldAsInteger(psColDef->field_index) );
       case SWQ_STRING:
           poDstFeat->SetField( iField, poSrcFeat->GetFieldAsString(psColDef->field_index) );
       }
   }

'order by' 쿼리를 지원하려면, :cpp:func:`OGRGenSQLResultsLayer::CreateOrderByIndex` 도 다음과 같이 수정해야 합니다:

::

   if ( psKeyDef->field_index >= iFIDFieldIndex)
   {
       if ( psKeyDef->field_index < iFIDFieldIndex + SPECIAL_FIELD_COUNT )
       {
           switch (SpecialFieldTypes[psKeyDef->field_index - iFIDFieldIndex])
           {
           case SWQ_INTEGER:
               psDstField->Integer = poSrcFeat->GetFieldAsInteger(psKeyDef->field_index);
           case SWQ_STRING:
               psDstField->String = CPLStrdup( poSrcFeat->GetFieldAsString(psKeyDef->field_index) );
           }
       }
       continue;
   }

이전에 할당한 모든 문자열을 이후 동일한 함수에서 다음과 같이 할당 해제해야 합니다:

::

   if ( psKeyDef->field_index >= iFIDFieldIndex )
   {
       /* 경고: 문자열 유형 특수 필드만 할당 해제해야 합니다. */
       if (SpecialFieldTypes[psKeyDef->field_index - iFIDFieldIndex] == SWQ_STRING)
       {
           for( i = 0; i < nIndexSize; i++ )
           {
               OGRField *psField = pasIndexFields + iKey + i * nOrderItems;
               CPLFree( psField->String );
           }
       }
       continue;
   }

필드 값을 기준으로 정렬하는 경우 :cpp:func:`OGRGenSQLResultsLayer::Compare` 도 수정해야 합니다:

::

   if( psKeyDef->field_index >= iFIDFieldIndex )
       poFDefn = NULL;
   else
       poFDefn = poSrcLayer->GetLayerDefn()->GetFieldDefn( 
           psKeyDef->field_index );

   if( (pasFirstTuple[iKey].Set.nMarker1 == OGRUnsetMarker 
           && pasFirstTuple[iKey].Set.nMarker2 == OGRUnsetMarker)
       || (pasSecondTuple[iKey].Set.nMarker1 == OGRUnsetMarker 
           && pasSecondTuple[iKey].Set.nMarker2 == OGRUnsetMarker) )
       nResult = 0;
   else if ( poFDefn == NULL )
   {
       switch (SpecialFieldTypes[psKeyDef->field_index - iFIDFieldIndex])
       {
       case SWQ_INTEGER:
           if( pasFirstTuple[iKey].Integer < pasSecondTuple[iKey].Integer )
               nResult = -1;
           else if( pasFirstTuple[iKey].Integer > pasSecondTuple[iKey].Integer )
               nResult = 1;
           break;
       case SWQ_STRING:
           nResult = strcmp(pasFirstTuple[iKey].String,
                           pasSecondTuple[iKey].String);
           break;
       }
   }

새 특수 필드 추가하기
---------------------

후속 개발 단계에서 새로운 특수 필드를 추가하는 것은 꽤 간단하며 다음 단계를 거쳐야 합니다:

1. :file:`ogr_p.h` 에 SPECIAL_FIELD_COUNT 값을 가진 새 상수를 추가하고 SPECIAL_FIELD_COUNT를 1만큼 증가시켜야 합니다.

2. :file:`ogrfeaturequery.cpp` 에서 SpecialFieldNames 및 SpecialFieldTypes에 특수 필드 문자열 및 그 유형을 각각 추가해야 합니다.

3. 새 특수 필드의 값을 지정하려면 필드값 접근자(:cpp:func:`OGRFeature::GetFieldAsString`, :cpp:func:`OGRFeature::GetFieldAsInteger`, :cpp:func:`OGRFeature::GetFieldAsDouble`)를 수정해야 합니다. 이 모든 함수들은 상수 값을 반환하기 때문에 :cpp:func:`GetFieldAsString` 이 'm_pszTmpFieldValue' 멤버에 값을 유지해야 합니다.

4. SWQ_INTEGER 및 SWQ_STRING 유형이 아닌 다른 유형의 새로운 값을 추가하는 경우 다음 함수들도 그에 따라 수정해야 할 수도 있습니다:

-  :cpp:func:`OGRGenSQLResultsLayer::OGRGenSQLResultsLayer`
-  :cpp:func:`OGRGenSQLResultsLayer::TranslateFeature`
-  :cpp:func:`OGRGenSQLResultsLayer::CreateOrderByIndex`
-  :cpp:func:`OGRGenSQLResultsLayer::Compare`
-  :cpp:func:`OGRFeatureQueryEvaluator`

하위 호환성
-----------

대부분의 경우 OGR 라이브러리의 하위 호환성은 유지될 것입니다. 하지만 특수 필드가 명명된 이름을 가진 필드와 충돌을 일으킬 가능성은 있습니다. 필드값에 접근하는 경우 특수 필드가 동일한 이름을 가진 다른 필드보다 우선할 것입니다.

:cpp:func:`OGRFeature::GetFieldAsString` 을 사용하는 경우 반환 값을 정적 변수 대신 멤버 변수로 저장할 것입니다. 피처 삭제 후 문자열을 할당 해제할 것이기 때문에 더 이상 사용할 수 없게 됩니다.

회귀 테스트
-----------

새로운 :file:`gdalautotest/ogr/ogr_sqlspecials.py` 스크립트가 ExecuteSQL() 호출 및 WHERE 절에 있는 모든 특수 필드에 대한 지원을 테스트합니다.

문서화
------

특수 필드에 대한 지원을 반영해서 OGR SQL 문서를 업데이트할 것입니다.

구현 인력
---------

세케레시 터마시가 GDAL/OGR 1.4.0 배포 시기에 맞춰 이 RFC 대부분을 구현할 것입니다.

프랑크 바르메르담은 하위 호환성 문제가 (특히 :cpp:func:`GetFieldAsString` 반환값의 수정된 수명이라는 측면에서) OGR 프로젝트의 다른 부분들에 어떤 영향을 미칠지 고려해서 파이썬 회귀 테스트 스크립트를 작성할 것입니다.

참조
----

-  이 기능에 대한 버그 추적(제안 코드 변경 사항을 모두 담고 있습니다): #1333

-  MapServer 관련 버그들:

   -  `1129 <http://trac.osgeo.org/mapserver/ticket/1129>`_
   -  `1438 <http://trac.osgeo.org/mapserver/ticket/1438>`_

투표 이력
---------

-  프랑크 바르메르담(Frank Warmerdam) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  하워드 버틀러(Howard Butler) +0
-  안드레이 키셀레프(Andrey Kiselev) +1

