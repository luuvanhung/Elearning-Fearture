# Generated by Django 3.2.3 on 2021-10-08 00:07

from os import listdir
from os.path import join

from api_seat_map.models.object_type import name_file
from binary_database_files.storage import DatabaseStorage
from django.conf import settings
from django.db import migrations

SVG_FOLDER = join(settings.BASE_DIR, "common/seat_map_svg")


def initial_data(apps, schema_editor):
    object_types = []
    object_type_model = apps.get_model("api_seat_map", "ObjectType")
    svg_files = [f for f in listdir(SVG_FOLDER)]
    ds = DatabaseStorage()
    for svg_file in svg_files:
        storage_filename = name_file(None, svg_file)
        ds.save(storage_filename, open(join(SVG_FOLDER, svg_file)))
        # Interview-Room => Interview Room
        filename_readable = " ".join(svg_file.split("-"))
        object_type = object_type_model(
            name=filename_readable, svg_file=storage_filename
        )
        object_types.append(object_type)

    object_type_model.objects.bulk_create(object_types)


class Migration(migrations.Migration):

    dependencies = [
        ("api_seat_map", "0001_initial"),
        ("binary_database_files", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(initial_data, migrations.RunPython.noop),
    ]