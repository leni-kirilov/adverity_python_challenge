import petl
import datetime
import os.path

from django.utils.dateformat import format as date_format
from django.utils.dateparse import parse_datetime

from core.services import swapi

CSV_FILENAME_PREFIX = "petl_characters_"

PAGE_SIZE = 10


def transform(characters: list):
    if not characters:
        raise ValueError("Empty dictionary cannot be transformed")

    now = datetime.datetime.now()
    print('Transforming characters')
    filename = CSV_FILENAME_PREFIX + now.strftime("%Y_%m_%d %H-%M-%S") + ".csv"

    print("Writing to csv")
    (petl
     .fromdicts(characters)
     .addfield("date",
               lambda character: date_format(parse_datetime(character['edited']), "Y-m-d"))
     .convert("homeworld",
              lambda planet_url: swapi.get_planet_name(planet_url))
     .cutout("films", "species", "vehicles", "starships", "created", "edited")
     .tocsv(filename))

    return filename, now


def get_data_up_to_page(filename: str, page_number: int) -> list:
    if not filename:
        raise ValueError("Filename is empty")
    if not os.path.exists(filename):
        raise ValueError("Filename does not exist")
    if page_number < 0:
        raise ValueError("page_number must be non-negative")

    start_entry_index = 0
    end_entry_index = (page_number + 1) * PAGE_SIZE

    return ((petl.fromcsv(filename)
             .rowslice(start_entry_index, end_entry_index))
            .dicts()
            .list())


def aggregate(dataset_file_name: str, *columns) -> list:
    if not dataset_file_name:
        raise ValueError("dataset_file_name is empty")
    if not columns:
        raise ValueError("Aggregating columns cannot be empty")

    characters = petl.fromcsv(dataset_file_name)

    if not all(column in petl.header(characters) for column in columns):
        raise ValueError(f"Column(s) {columns} not found in the CSV file.")

    return (petl
            .valuecounts(characters, *columns)
            .cutout("frequency")
            .dicts()
            .list())
