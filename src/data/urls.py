from django.urls import path, include

from data import views
from data.views import SchemaListView, SchemaCreateView, SchemaUpdateView, SchemaDeleteView
app_name = 'schema'

urlpatterns = [

    path('', SchemaListView.as_view(), name='list'),
    path('add/', SchemaCreateView.as_view(), name='add'),
    path('edit/<item_id>', SchemaUpdateView.as_view(), name='update'),
    path('generate/<slug>', views.generate_csv, name='den'),
    path('delete/<item_id>', SchemaDeleteView.as_view(), name='delete')

]