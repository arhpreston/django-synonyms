Django Synonyms
===============

Django Synonyms provides the ability to reference a field in a model
by any number of synonyms while retaining the ability to search the
original field.

For example, a model of an academic journal might include a name
field. 'Physical Review B' is the official name, but it is often
referred to as 'Phys Rev B' or 'prb'.

Installation
------------

1. Update your settings file:

    INSTALLED_APPS += ('synonyms',)

2. Sync the databse

    $ python manage.py syncdb    

Usage
-----

1. Your model might looks something like:

    class Journal(models.Model):
        objects = SynonymManager(target_field='name')
	name = models.CharField(max_length=100)
	...

2. Your view would then contain the following code:

    journal = Journal.objects.get(name='prb')

3. Your admin layout could be extended with:

    from synonyms.admin import SynonymInline

    class JournalAdmin(admin.ModelAdmin):
        inlines = (SynonymInline, ...)
	...

Known Limitations
-----------------

1. In the current version it is only possible to use Synonyms on one
field per model.
