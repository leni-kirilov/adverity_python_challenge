import petl
import datetime

from django.utils.dateformat import format as date_format
from django.utils.dateparse import parse_datetime

from . import wapi
from ..models import Dataset

PAGE_SIZE = 10


def transform(characters: dict):
    now = datetime.datetime.now()
    print('Transforming characters')
    filename = "petl_characters_" + now.strftime("%Y_%m_%d %H-%M-%S")  + ".csv"

    # ODO surround in try-catch ?
    print('Storing dataset to the DB...')
    dataset = Dataset.objects.create_dataset(filename, now)
    dataset.save()  # TODO REQ1 should I store to filesystem and then to db?

    print("Writing to csv")
    return (petl
            .fromdicts(characters)
            .addfield("date",
                      lambda character: date_format(parse_datetime(character['edited']), "Y-m-d"))
            .convert("homeworld",
                     lambda planet_url: wapi.get_planet_name(planet_url))
            .cutout("films", "species", "vehicles", "starships", "created", "edited")
            .tocsv(filename))


def get_paginated_data_from_file(filename: str, page_number: int) -> list:
    start_entry_index = 0
    end_entry_index = (page_number + 1) * PAGE_SIZE

    # TODO REQ3 - add totalrows to make LoadMore unclickable?
    return ((petl.fromcsv(filename)
             .rowslice(start_entry_index, end_entry_index))
            .dicts()
            .list())


def aggregate(dataset_file_name: str, *columns: list) -> list:
    characters = petl.fromcsv(dataset_file_name)

    if not all(column in petl.header(characters) for column in columns):
        raise ValueError(f"Column(s) {columns} not found in the CSV file.")

    valuecounts = petl.valuecounts(characters, *columns)
    aggregate_result = petl.cutout(valuecounts, "frequency")
    return list(petl.dicts(aggregate_result))
