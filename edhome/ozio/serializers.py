from rest_framework import serializers
from ozio.models import *

## WHOLE FILE FOR REST FRAMEWORK

class TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Type
		fields = ('id', 'type', 'span_days', 'description') 
	
class CateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Cate
		fields = ('id', 'cate', 'description') 
		
class SubCateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SubCate
		fields = ('id', 'cate', 'sub_cate', 'description')
	
	cate = serializers.PrimaryKeyRelatedField()

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Keyword
		fields = ('id', 'keyword', 'type', 'cate', 'sub_cate', 'priority', 'description')
	
	type = serializers.PrimaryKeyRelatedField()
	cate = serializers.PrimaryKeyRelatedField()
	sub_cate = serializers.PrimaryKeyRelatedField()


class SourceFileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SourceFile
		fields = ('id', 'file_name', 'import_time', 'local_link')

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Transaction
		fields = ('id', 'date', 'amount', 'info', 'original_info', 'source_file', 'keyword')
		
	source_file = serializers.PrimaryKeyRelatedField()
	keyword = serializers.PrimaryKeyRelatedField()


class TransactionFilterSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = TransactionFilter
		fields = ('id', 'filter_name', 'description') 
		
class FilterSQLSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = FilterSQL
		fields = ('id', 'filter', 'filter_sql')
		
	filter = serializers.PrimaryKeyRelatedField()



		