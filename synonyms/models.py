from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify

class Synonym(models.Model):
    """
    Define a generic relation between a synonym and another model.

    Note that it's possible to add an extra field to the related
    models:
    
      synonyms = generic.GenericRelation(Synonym)

    Which enables reverse lookups:

      journal
      => <Journal: Physical Review B>
      
      journal.synonyms
      => [<Synonym: phys-rev-b>, <Synonym: prb>, ...]
    """
    synonym = models.SlugField()

    # Future: add ability to use synonyms on more than one field in a
    # model. The field will need to be stored in the model for this to
    # be possible.
    #target_field = models.CharField(default='', max_length=50)

    content_type = models.ForeignKey(ContentType, related_name='asdf')  # Model (table)
    object_id = models.PositiveIntegerField()      # pk (row)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return '<%s: %s>' % (self.synonym, self.content_object)
    
    def save(self, *args, **kwargs):
        # Ensure the synonym looks like a slug, which is what
        # SynonymManager assumes.
        self.synonym = slugify(self.synonym)
        super(Synonym, self).save(*args, **kwargs)
