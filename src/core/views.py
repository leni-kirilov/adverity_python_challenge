from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from core.models import Dataset
from core.services import swapi, datasets

CHARACTERS_SELECTABLE_FIELDS = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender',
                       'homeworld', 'url', 'date']


class IndexView(TemplateView):
    template_name = 'index.html'


def index(request):
    links = []
    for dataset in Dataset.objects.all():
        links.append({'name': dataset.filename, 'url': 'http://localhost:8000/dataset/' + str(dataset.id)})

    return render(request, 'index.html', {'links': links})


def fetch_characters(request):
    if request.method == 'POST':  # TODO does it need to be a POST?
        characters = swapi.get_all_characters()
        result_csv_filename, now = datasets.transform(characters)

        print('Storing dataset to the DB...')
        Dataset.objects.create_dataset(result_csv_filename, now).save()

        print('Done. [' + result_csv_filename + '] was created')
        return redirect('index')


def show_dataset(request, id):
    page_index = request.GET.get('page_index', 0)
    dataset = Dataset.objects.filter(id=id).get()
    data = datasets.get_data_up_to_page(dataset.filename, int(page_index))

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

def show_dataset_aggregate(request, id):
    dataset = Dataset.objects.filter(id=id).get()
    selected_fields: str = request.GET.get('selected_fields')

    if not selected_fields:
        default_fields = 'homeworld'
        return redirect(f"{request.path}?selected_fields={default_fields}")

    split: list = list(filter(None, selected_fields.split(',')))
    data = datasets.aggregate(dataset.filename, *split)
    header = list(data[0].keys())

    return render(
        request,
        'dataset_aggregate.html',
        {
            'id': id,
            'filename': dataset.filename,
            'fields': CHARACTERS_SELECTABLE_FIELDS, #TODO make it dynamic from datasets.get_header
            'selected_fields': split,
            'header': header,
            'data': data
        }
    )
