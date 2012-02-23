from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from synonyms.models import Synonym

import logging
logger = logging.getLogger(__name__)

class SynonymManager(models.Manager):
    """
    Use this manager wherever you have a model containing a field that
    will regularly be referred to with more than one value. For
    example:
    
       class Journal(models.Model):
           objects = SynonymManager(target_field='name')
           name = models.CharField(max_length=100)
           ...

       The journal named 'Physical Review B', is regularly referred to
       as 'Phys Rev B', 'prb', etc.
       
    This app duplicates a lot of the functionality of tagging apps
    like django-tagging and django-taggit (try those first). Synonyms
    fits the particular niche where you want to be able to refer to
    your target_field by an arbitrary number of synonyms while
    retaining the ability to search the base model field first.
    """

    def __init__(self, target_field='name', *args, **kwargs):
        super(SynonymManager, self).__init__(*args, **kwargs)
        self.target_field = target_field

    def get(self, *args, **kwargs):
        try:
            return super(SynonymManager, self).get(*args, **kwargs)
        except self.model.DoesNotExist:
            pass

        try:
            q = kwargs[self.target_field]
        except ValueError:
            raise self.model.DoesNotExist
        
        q = slugify(q) # 'Phys Rev B' => 'phys-rev-b'

        # Look for synonym, but filter with content_type to ensure
        # only synonyms which point to the current model are returned
        # (i.e., a synonym for ZnO should only return a Topic, not a
        # Journal).
        try:
            content_type = ContentType.objects.get_for_model(self.model)
            synonym = Synonym.objects.get(synonym=q, content_type=content_type)
            return synonym.content_object
        except Synonym.DoesNotExist:
            logger.debug(
                "Could not find synonym '%s' for model '%s'" % (q,self.model))
            raise self.model.DoesNotExist(
                "Tried looking for synonym '%s' on field '%s'" % (q,self.target_field))
