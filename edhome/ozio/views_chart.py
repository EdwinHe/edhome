from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs.views.pie import HighChartPieView
from chartjs.views import JSONView, HighChartsView
from ozio.models import *
from django.db.models import Sum

# LINE CHART 
def linechart_get_labels_data():
    # Excluse 'Off Balance' and 'Income' from Type 
    types=Type.objects.filter(~Q(type__exact = 'Off Balance') & ~Q(type__exact = 'Income') )
    
    # Excluse 'Properties' and 'Off Balance' from Cates
    cates=Cate.objects.filter(~Q(cate__exact = 'Properties') & ~Q(cate__exact = 'Off Balance'))
    
    # Loop up keywords whose types in filtered types and cates
    keywords=Keyword.objects.filter(Q(type__in = types) & Q(cate__in = cates))
    
    monthly_total = Transaction.objects \
                    .filter(Q(keyword__in = keywords)) \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}, order_by = ['YYYY-MM']) \
                    .values('YYYY-MM') \
                    .annotate(month_total=Sum('amount'))
                    
    labels = [m['YYYY-MM'] for m in list(monthly_total)]
    data = [m['month_total'] * -1.0 for m in list(monthly_total)]
    
    return [labels, data]

class LineChartJSONView(BaseLineChartView):
    [labels, data] = linechart_get_labels_data()
    
    def get_labels(self):
        """Return 7 labels."""
        return self.labels

    def get_data(self):
        """Return 3 dataset to plot."""
        return [self.data,]

line_chart_json = LineChartJSONView.as_view()