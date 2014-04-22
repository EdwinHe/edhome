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
	
	cate = serializers.PrimaryKeyRelatedField(label = 'Category')
	#cate = serializers.RelatedField(source = 'cate', label = 'Category')
	#cate = serializers.ModelField(model_field=Cate()._meta.get_field('cate'), label = 'Category')
	#===========================================================================
	# cate = serializers.SerializerMethodField('id_and_cate')
	# cate.label = 'Category'
	#===========================================================================
	
	#===========================================================================
	# def id_and_cate(self, obj):
	# 	return {'id': obj.cate.id, 'text': obj.cate.cate}
	#===========================================================================

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Keyword
		fields = ('id', 'keyword', 'type', 'cate', 'sub_cate', 'priority', 'description')
	
	type = serializers.PrimaryKeyRelatedField(label = 'Type')
	#type = serializers.RelatedField(source='type',label = 'Type')
	#===========================================================================
	# type = serializers.SerializerMethodField('id_and_type')
	# type.label = 'Type'
	#===========================================================================
	
	cate = serializers.PrimaryKeyRelatedField(label = 'Category')
	#cate = serializers.RelatedField(source='cate',label = 'Category')
	#===========================================================================
	# cate = serializers.SerializerMethodField('id_and_cate')
	# cate.label = 'Category'
	#===========================================================================
	
	sub_cate = serializers.PrimaryKeyRelatedField(label = 'Sub Category')
	#sub_cate = serializers.RelatedField(source='sub_cate',label = 'Sub Category')
	#===========================================================================
	# sub_cate = serializers.SerializerMethodField('id_and_subcate')
	# sub_cate.label = 'Sub Category'
	#===========================================================================
	
	#===========================================================================
	# def id_and_type(self, obj):
	# 	return {'id': obj.type.id, 'text': obj.type.type}
	# 
	# def id_and_cate(self, obj):
	# 	return {'id': obj.cate.id, 'text': obj.cate.cate}
	# 
	# def id_and_subcate(self, obj):
	# 	return {'id': obj.sub_cate.id, 'text': obj.sub_cate.sub_cate}
	#===========================================================================


class SourceFileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SourceFile
		fields = ('id', 'file_name', 'import_time', 'local_link')

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Transaction
		fields = ('id', 'date', 'amount', 'info', 'original_info', 'source_file', 'keyword')
		
	source_file = serializers.PrimaryKeyRelatedField(label = 'Source File')
	#source_file = serializers.RelatedField(source = 'source_file', label = 'Source File')
	#===========================================================================
	# source_file = serializers.SerializerMethodField('id_and_source_file')
	# source_file.label = 'Source File'
	#===========================================================================
	
	keyword = serializers.PrimaryKeyRelatedField(label = 'Keyword', required=False)
	#keyword = serializers.RelatedField(source = 'keyword', label = 'Keyword')
	#===========================================================================
	# keyword = serializers.SerializerMethodField('id_and_keyword')
	# keyword.label = 'Keyword'
	#===========================================================================
	
	#===========================================================================
	# def id_and_source_file(self, obj):
	# 	return {'id': obj.source_file.id, 'text': obj.source_file.file_name}
	# 
	# def id_and_keyword(self, obj):
	# 	if obj.keyword: # this is needed for all foreign key fields that can be null
	# 		return {'id': obj.keyword.id, 'text': obj.keyword.keyword}
	# 	else:
	# 		return {'id': 'TBC', 'text': 'TBC'}
	#===========================================================================


class TransactionFilterSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = TransactionFilter
		fields = ('id', 'filter_name', 'description') 
		
class FilterSQLSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = FilterSQL
		fields = ('id', 'filter', 'filter_sql')
		
	filter = serializers.PrimaryKeyRelatedField(label = 'Filter')
	#===========================================================================
	# filter = serializers.SerializerMethodField('id_and_filter')
	# filter.label = 'Filter'
	# 
	# def id_and_filter(self, obj):
	# 	return {'id': obj.filter.id, 'text': obj.filter.filter}
	#===========================================================================


		