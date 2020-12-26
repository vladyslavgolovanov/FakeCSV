import csv
from random import randint

from django.contrib.auth.decorators import login_required
from faker import Faker
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse

from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from data.forms import ColumnFormSet
from data.models import Schemas, Column

fake = Faker()


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schemas
    template_name = 'schemas.html'
    context_object_name = 'result'
    login_url = '/accounts/login'


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schemas
    fields = ['name', 'column_separators', 'string_chapter', 'rows']
    template_name = 'new_schema.html'
    login_url = '/accounts/login'

    def get_context_data(self, **kwargs):
        data = super(SchemaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['column_form'] = ColumnFormSet(self.request.POST)
        else:
            data['column_form'] = ColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        column_form = context['column_form']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            if column_form.is_valid():
                column_form.instance = self.object
                column_form.save()
        return super(SchemaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('schema:list')


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    model = Schemas
    fields = ['name', 'column_separators', 'string_chapter', 'rows']
    template_name = 'new_schema.html'
    login_url = '/accounts/login'
    pk_url_kwarg = 'item_id'

    def get_context_data(self, **kwargs):
        data = super(SchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['column_form'] = ColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['column_form'] = ColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        column_form = context['column_form']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            if column_form.is_valid():
                column_form.instance = self.object
                column_form.save()
        return super(SchemaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('schema:list')


class SchemaDeleteView(DeleteView):
    model = Schemas
    template_name = 'new_schema.html'
    success_msg = 'Successful deleted'
    pk_url_kwarg = 'item_id'

    def get_success_url(self):
        return reverse('schema:list')


@login_required(login_url='/accounts/login/')
def generate_csv(request, slug):
    schema_data = Schemas.objects.get(pk=slug)
    column_data = Column.objects.filter(schemas_id=slug)
    field_schema = ['name', 'column_separators', 'string_chapter', 'rows']
    field_column = ['column_name', 'type']
    schema = [getattr(schema_data, i) for i in field_schema]
    schema_atr = []
    column_atr = []
    for data in column_data:
        column = [getattr(data, i) for i in field_column]
        schema_atr.append(column[0])
        column_atr.append(column[1])
    n = len(schema_atr)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={schema[0]}'
    writer = csv.writer(response, delimiter=f'{schema[1]}', quotechar=f'{schema[2]}')
    writer.writerow(schema_atr)
    dataset = []
    for i in range(schema[3]):
        for j in range(0, len(column_atr)):
            constant = column_atr[j]
            if constant == 'Full Name':
                dataset.append(fake.name())
            if constant == 'Integer':
                dataset.append(randint(18, 60))
            if constant == 'Email':
                dataset.append(fake.email())
            if constant == 'Job':
                dataset.append(fake.job())
            if constant == 'Phone':
                dataset.append(fake.phone_number())
    list_data = [dataset[i:i + n] for i in range(0, len(dataset), n)]
    for i in range(schema[3]):
        writer.writerow(list_data[i])
    return response
