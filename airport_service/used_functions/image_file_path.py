import os
import uuid

from django.utils.text import slugify


def crew_image_file_path(instance: "airport_service.Crew", filename: str):
    _, extensions = os.path.splitext(filename)

    filename = f"{slugify(instance.last_name)}-{uuid.uuid4()}.{extensions}"

    return os.path.join("uploads/crew/", filename)


def airplane_image_file_path(instance: "airport_service.Airplane", filename: str):
    _, extensions = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}.{extensions}"

    return os.path.join("uploads/airplanes/", filename)
