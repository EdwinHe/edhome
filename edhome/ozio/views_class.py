from ozio.models import *

from rest_framework import viewsets
from rest_framework import serializers
from ozio.serializers import *

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
    
class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    
    def get_queryset(self):
        queryset = Keyword.objects.all()
        keyword_like = self.request.QUERY_PARAMS.get('keyword_like', None)
        
        if keyword_like:
            queryset = queryset.filter(keyword__icontains = keyword_like)
        
        return queryset
    
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
        
        #import pdb;pdb.set_trace()
        if yyyymm:
            yyyy = yyyymm.split('-')[0]
            mm =  yyyymm.split('-')[1]
            queryset = queryset.filter(Q(date__year = yyyy) & Q(date__month = mm))
        
        if cate:
            queryset = queryset.filter(keyword__cate__cate = cate)
        
        if subcate:
            queryset = queryset.filter(keyword__sub_cate__sub_cate = subcate)
        
        return queryset
    
class TransactionFilterViewSet(viewsets.ModelViewSet):
    queryset = TransactionFilter.objects.all()
    serializer_class = TransactionFilterSerializer   
    
class FilterSQLViewSet(viewsets.ModelViewSet):
    queryset = FilterSQL.objects.all()
    serializer_class = FilterSQLSerializer   

#===============================================================================
# class LineItemViewSet(viewsets.ModelViewSet):
#  
#     model = LineItem
#     #queryset = LineItem.objects.all()
#     serializer_class = LineItemSerializer
#      
#     def get_queryset(self):
#         #import pdb;pdb.set_trace()
#         # Ideally, cart is linked with user and user is retrieved by self.request.user
#         queryset = LineItem.objects.all()
#            
#         cartid = self.request.QUERY_PARAMS.get('cartid', None)
#         productid = self.request.QUERY_PARAMS.get('productid', None)
#          
#         if cartid and productid:
#             queryset = LineItem.objects.filter(Q(cart__exact = cartid) & Q(product__exact = productid))
#         elif cartid:
#             queryset = LineItem.objects.filter(cart__exact = cartid)
#         elif productid:
#             queryset = LineItem.objects.filter(cart__exact = productid)
#          
#         return queryset
#===============================================================================
    