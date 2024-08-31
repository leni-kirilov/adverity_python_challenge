from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import Dataset
from .services import wapi, petl


class IndexView(TemplateView):
    template_name = 'index.html'


def index(request):
    links = []
    for dataset in Dataset.objects.all():
        filename = dataset.filename
        if filename.startswith('petl_characters'):
            links.append({'name': filename, 'url': 'http://localhost:8000/dataset/' + str(dataset.id)})

    return render(request, 'index.html', {'links': links})


def fetch_characters(request):
    if request.method == 'POST': #TODO does it need to be a POST?
        characters = wapi.get_all_characters()
        petl.transform(characters)
        print("Done")
        return redirect('index')


def show_dataset(request, id):
    page_index = request.GET.get('page_index', 0)

    dataset = Dataset.objects.filter(id=id).get()

    data = petl.get_paginated_data_from_file(dataset.filename, int(page_index))
    header = list(data[0].keys())
    return render(
        request,
        'dataset.html',
        {
            'id': id,
            'filename': dataset.filename,
            'page_index': page_index,
            'header': header,
            'data': data
        }
    )
