from django.contrib import admin
from django.contrib.contenttypes import generic

from synonyms.models import Synonym

class SynonymInline(generic.GenericStackedInline):
    model = Synonym
