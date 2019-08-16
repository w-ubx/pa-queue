import json
import os
from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User

from face_recog.utils import encode_photo


class FaceData(models.Model):
    user = models.ForeignKey(User, on_delete='models.CASCADE',
        related_name='face_data')
    encoded = JSONField()

    def encode_photo(self, path):
        self.encoded = encode_photo(path)
        self.save()

    def __str__(self):
        return self.user.username