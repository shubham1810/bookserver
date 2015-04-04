from django.db import models

from parse_rest.connection import register
from parse_rest.datatypes import Object
from credentials import parse_credentials

register(parse_credentials["application_id"], parse_credentials["rest_api_key"])


class Book(Object):
    pass