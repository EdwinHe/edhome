from ozio.models import *
from ozio.serializers import *

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


# WHOLE FILE IS FOR REST FRAMEWORK 

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    
class CateViewSet(viewsets.ModelViewSet):
    queryset = Cate.objects.all()
    serializer_class = CateSerializer    

class SubCateViewSet(viewsets.ModelViewSet):
    queryset = SubCate.objects.all()
    serializer_class = SubCateSerializer    
    
    def list(self, request):
        return Response(SubCateListSerializer(SubCate.objects.all()).data)
    
class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    
    def get_queryset(self):
        queryset = Keyword.objects.all()
        keyword_like = self.request.QUERY_PARAMS.get('keyword_like', None)
        
        if keyword_like:
            queryset = queryset.filter(keyword__icontains = keyword_like)
        
        return queryset
    
    def list(self, request):
        return Response(KeywordListSerializer(self.get_queryset()).data)
    
class SourceFileViewSet(viewsets.ModelViewSet):
    queryset = SourceFile.objects.all()
    serializer_class = SourceFileSerializer   
    
    def get_queryset(self):
        queryset = SourceFile.objects.all()
        file_name = self.request.QUERY_PARAMS.get('file_name', None)
        
        if file_name:
            queryset = queryset.filter(file_name__exact = file_name)
        
        return queryset
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer   
    
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        # Ideally, cart is linked with user and user is retrieved by self.request.user
        queryset = Transaction.objects.select_related()
        
        yyyymm = self.request.QUERY_PARAMS.get('yyyymm', None)
        cate = self.request.QUERY_PARAMS.get('cate', None)
        subcate = self.request.QUERY_PARAMS.get('subcate', None)
        keyword = self.request.QUERY_PARAMS.get('keyword', None)
        span_status = self.request.QUERY_PARAMS.get('span_status', None)
        
        #import pdb;pdb.set_trace()
        if yyyymm:
            yyyy = yyyymm.split('-')[0]
            mm =  yyyymm.split('-')[1]
            queryset = queryset.filter(Q(date__year = yyyy) & Q(date__month = mm))
        
        if cate:
            queryset = queryset.filter(keyword__cate__cate = cate)
        
        if subcate:
            queryset = queryset.filter(keyword__sub_cate__sub_cate = subcate)
        
        if keyword != None:
            if keyword == '':
                queryset = queryset.filter(keyword__isnull = True)
            else:
                queryset = queryset.filter(keyword__keyword__exact = keyword)
        
        if span_status:
            queryset = queryset.filter(span_status__exact = span_status)
        
        
        return queryset
    
    def list(self, request):
        return Response(TransactionListSerializer(self.get_queryset()).data)
    
    
class TransactionFilterViewSet(viewsets.ModelViewSet):
    queryset = TransactionFilter.objects.all()
    serializer_class = TransactionFilterSerializer
    
    
class FilterSQLViewSet(viewsets.ModelViewSet):
    queryset = FilterSQL.objects.all()
    serializer_class = FilterSQLSerializer   

    def list(self, request):
            return Response(FilterSQLListSerializer(FilterSQL.objects.all()).data)

    