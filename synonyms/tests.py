from django.test import TestCase
from django.db import models

from synonyms.managers import SynonymManager
from synonyms.models import Synonym

class City(models.Model):
    objects = SynonymManager(target_field='name')
    name = models.CharField(max_length=50)
    population = models.IntegerField()
    def __unicode__(self): return self.name

class SynonymTest(TestCase):

    def setUp(self):
        City.objects.create(name='Hamilton', population=50)

    def test_get(self):
        """
        Ensure the default get behaviour is still functional.
        """
        city = City.objects.get(name='Hamilton')

        self.assertRaises(
            City.DoesNotExist,
            lambda: City.objects.get(name='not a city'))
        
    def test_get_synonym(self):
        """
        Ensure the synonyms extension works as expected.
        """
        city = City.objects.get(name='Hamilton')

        Synonym.objects.create(synonym='Hamiltron', content_object=city)

        syn_city = City.objects.get(name='Hamiltron')

        self.assertEquals(city, syn_city)
