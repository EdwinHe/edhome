from django.db import models
from django.db.models import Q

# Create your models here.
class Type(models.Model):
	type = models.CharField('Type', max_length = 40)
	span_months = models.PositiveIntegerField('Span Months')
	description = models.CharField('Description', max_length = 60, blank = True)
	
	def __str__(self):
		return self.type
	
class Cate(models.Model):
	cate = models.CharField('Category', max_length = 40)
	description = models.CharField('Description', max_length = 60, blank = True)
	
	def __str__(self):
		return self.cate
	
class SubCate(models.Model):
	cate = models.ForeignKey(Cate)
	sub_cate = models.CharField('Sub Category', max_length = 40)
	description = models.CharField('Description', max_length = 60, blank = True)
	
	def __str__(self):
		return self.sub_cate
	
class Keyword(models.Model):
	keyword = models.CharField('Keywords', max_length = 100)
	type = models.ForeignKey(Type)
	cate = models.ForeignKey(Cate)
	sub_cate = models.ForeignKey(SubCate)
	priority = models.PositiveIntegerField('Priority')
	description = models.CharField('Description', max_length = 60, blank = True)
	
	def __str__(self):
		return self.keyword

class SourceFile(models.Model):
	file_name = models.CharField('File Name', max_length = 100, unique=True)
	import_time = models.DateTimeField('Import Time', auto_now_add = True)
	local_link = models.FileField(upload_to="ozio/uploaded_files/%Y")
	
	def __str__(self):
		return self.file_name

class Transaction(models.Model):
	date = models.DateField('Date')
	amount = models.FloatField('Amount')
	info = models.CharField('Info', max_length = 100)
	original_info = models.CharField('Raw Info', max_length = 100)
	source_file = models.ForeignKey(SourceFile)
	
	NA = '-'
	PENDING = 'N'
	SPLITTED = 'Y'
	CHILD = 'C'
	SPAN_STATUS = (
        (NA, 'N/A'),
        (PENDING, 'Pending'),
        (SPLITTED, 'Splitted'),
        (CHILD, 'Child'),
    )
	
	span_status = models.CharField('Span Status', max_length = 10, choices=SPAN_STATUS, default=NA)
	
	keyword = models.ForeignKey(Keyword, blank = True, null = True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.info
	
class TransactionFilter(models.Model):
	filter_name = models.CharField('Filter Name', max_length = 60)
	description = models.CharField('Description', max_length = 100, blank = True)
	
	def __str__(self):
		return self.filter_name
	
	
class FilterSQL(models.Model):
	
	filter = models.ForeignKey(TransactionFilter)

	FILTER = 'filter'
	EXCLUDE = 'exclude'
	TYPES = (
        (FILTER, FILTER),
        (EXCLUDE, EXCLUDE),
    )
	filter_type =  models.CharField('Type', max_length = 10, choices=TYPES, default=FILTER)
	
	filter_sql = models.CharField('SQL', max_length = 100)
	
	ENABLED = 'enabled'
	DISABLED = 'disabled'
	ONOFF = (
	    (ENABLED, ENABLED),
	    (DISABLED, DISABLED),
	)
	filter_onoff =  models.CharField('On/Off', max_length = 10, choices=ONOFF, default=ENABLED)
	
	PENDING = 'pending'
	FAILED = 'failed'
	SUCCESS = 'passed'
	STATUS = (
		(PENDING,PENDING),
	    (FAILED, FAILED),
	    (SUCCESS, SUCCESS),
	)
	filter_status =  models.CharField('Status', max_length = 10, choices=STATUS, default=PENDING)
	 
	def __str__(self):
		return self.filter_sql

