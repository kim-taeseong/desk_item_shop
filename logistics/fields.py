import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

class ThumbnailImageFieldFile(ImageFieldFile):
    pass


class ThumbnailImageField(ImageField):
    pass
