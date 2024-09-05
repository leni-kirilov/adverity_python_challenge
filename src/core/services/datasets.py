import os.path
from datetime import datetime

import petl

from core.services import swapi
from core.models import Dataset

CSV_FILENAME_PREFIX = "petl_characters_"
UNNECESSARY_COLUMNS = "films", "species", "vehicles", "starships", "created", "edited"

RAW_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DESTINATION_DATE_TIME_FORMAT = "%Y-%m-%d"

PAGE_SIZE = 10


def transform_and_write_to_file(characters: list):
    """Transforms and write to filesystem the SWAPI character entity to our internal model

    Keyword arguments:
    characters -- a list of dicts to be processed
    """
    if not characters:
        raise ValueError("Empty list cannot be transformed")

    now = datetime.now()
    print("Transforming characters")
    filename = CSV_FILENAME_PREFIX + now.strftime("%Y_%m_%d %H-%M-%S") + ".csv"

    print("Writing to csv")
    (petl
     .fromdicts(characters)
     .addfield("date",
               lambda character:
               datetime.strptime(character["edited"], RAW_DATE_TIME_FORMAT).strftime(DESTINATION_DATE_TIME_FORMAT))
     .convert("homeworld",
              lambda planet_url: swapi.get_planet_name(planet_url))
     .cutout(*UNNECESSARY_COLUMNS)
     .tocsv(filename))

    return filename, now


def get_data_up_to_page(filename: str, page_number: int) -> list:
    """Returns a list of data from beginning of a file to the desired page_number

    Keyword arguments:
    filename -- a list of dicts to be processed
    page_number
    """
    if not filename:
        raise ValueError("Filename is empty")
    if not os.path.exists(filename):
        raise ValueError("Filename " + filename + " does not exist")
    if page_number < 0:
        raise ValueError("page_number must be non-negative")

    start_entry_index = 0
    end_entry_index = (page_number + 1) * PAGE_SIZE

    return ((petl.fromcsv(filename)
             .rowslice(start_entry_index, end_entry_index))
            .dicts()
            .list())


def aggregate(dataset_filename: str, *columns) -> list:
    """Reads from file and aggregates based on column values

    Keyword arguments:
    filename -- source of data
    columns -- the columns to group by and produce aggregate data for

    If no columns are provided, it defaults to "homeworld"
    """
    if not dataset_filename:
        raise ValueError("dataset_file_name is empty")
    if not columns:
        raise ValueError("Aggregating columns cannot be empty")

    characters = petl.fromcsv(dataset_filename)

    if not all(column in petl.header(characters) for column in columns):
        raise ValueError(f"Column(s) {columns} not found in the CSV file.")

    return (petl
            .valuecounts(characters, *columns)
            .cutout("frequency")
            .dicts()
            .list())


def fetch_transform_persist():
    """Fetch data from SWAPI and persist it

    Returns the DB record for the new Dataset
    """
    characters = swapi.get_all_characters()

    result_csv_filename, now = transform_and_write_to_file(characters)

    print("Storing dataset to the DB...")
    db_dataset = Dataset.objects.create(filename=result_csv_filename, date_created=now)
    db_dataset.save()

    print("Done. [" + result_csv_filename + "] was created")
    return db_dataset
