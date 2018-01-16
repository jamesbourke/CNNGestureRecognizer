# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from cnn import cnninterface


class Config(AppConfig):
    name = 'gesture'

    def ready(self):
        cnninterface.load_model()
