from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from core.models import Dataset
from core.services import swapi, datasets

CHARACTERS_SELECTABLE_FIELDS = ["name", "height", "mass",
                                "hair_color", "skin_color", "eye_color",
                                "birth_year", "gender",
                                "homeworld", "url", "date"]


class IndexView(TemplateView):
    template_name = "index.html"


def index(request):
    """Displays initial page of existing datasets in DB and option to create a new entry"""
    links = []
    for dataset in Dataset.objects.all():
        links.append({"name": dataset.filename, "url": "http://localhost:8000/dataset/" + str(dataset.id)})

    return render(request, "index.html", {"links": links})


def fetch_characters(request):
    """Handles button the fetch and persist characters"""
    if request.method == "POST":  # TODO does it need to be a POST?

        characters = swapi.get_all_characters()

        result_csv_filename, now = datasets.transform_and_write_to_file(characters)

        print("Storing dataset to the DB...")
        Dataset.objects.create(filename=result_csv_filename, date_created=now).save()

        print("Done. [" + result_csv_filename + "] was created")
        return redirect("index")


def show_dataset(request, id):
    """Prepare data for the dataset template

    Keyword arguments:
    id -- dataset id
    page_index -- up to which page do we want to display the data (button Load More)
    """
    page_index = request.GET.get("page_index", 0)
    dataset = Dataset.objects.get(id=id)
    data = datasets.get_data_up_to_page(dataset.filename, int(page_index))

    header = list(data[0].keys())
    return render(
        request,
        "dataset/dataset.html",
        {
            "id": id,
            "filename": dataset.filename,
            "page_index": page_index,
            "header": header,
            "data": data
        }
    )


def show_dataset_aggregate(request, id):
    """Prepare data for the dataset aggregate

    Keyword arguments:
    id -- dataset id
    selected_fields -- list of fields to aggregate on
    """
    dataset = Dataset.objects.get(id=id)
    selected_fields: str = request.GET.get("selected_fields")

    if not selected_fields:
        default_fields = "homeworld"
        return redirect(f"{request.path}?selected_fields={default_fields}")

    aggregation_fields = list(filter(None, selected_fields.split(",")))
    data = datasets.aggregate(dataset.filename, *aggregation_fields)
    header = list(data[0].keys())

    return render(
        request,
        "dataset/dataset_aggregate.html",
        {
            "id": id,
            "filename": dataset.filename,
            "fields": CHARACTERS_SELECTABLE_FIELDS,
            "selected_fields": aggregation_fields,
            "header": header,
            "data": data
        }
    )
