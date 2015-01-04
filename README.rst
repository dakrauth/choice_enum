choice_enum
===========

Wrapper class for defining DRY, encapsulated choice options for CharFields.

ChoiceEnumeration
-----------------


``ChoiceEnumeration`` should be derived taking the following format::

    class ChoiceClass(ChoiceEnumeration):
        ATTR1 = ChoiceEnumeration.Option('db_value1', 'Human readable text 1')
        ATTR2 = ChoiceEnumeration.Option('db_value2', 'Human readable text 2')

The following attributes are generated on the ChoiceEnumeration child class:

- ``ALL_OPTIONS``  - a tuple of the supplied options
- ``CHOICES``      - a Django char field choices-compatible tuple
- ``CHOICES_DICT`` - a dictionary of option:text values
- ``DEFAULT``      - (optional) the item marked as default

Example::

    class SomeModel(models.Model):

        # ``MetaVar`` scoped here under the SomeModel class, but could have
        # been declared at the module level as well

        class MetaVar(ChoiceEnumeration):
            FOO  = ChoiceEnumeration.Option('foo',  'Foo Choice', default=True)
            BAR  = ChoiceEnumeration.Option('bar',  'Bar Option')
            BAZ  = ChoiceEnumeration.Option('baz',  'Baz Pick')
            SPAM = ChoiceEnumeration.Option('spam', 'Spam spam spam')
            EGGS = ChoiceEnumeration.Option('eggs', 'Eggs, Spam, and Ham')

        text = models.TextField()
        metavar = models.CharField(max_length=4, choices=MetaVar.CHOICES, default=MetaVar.DEFAULT)

Example interactive usage::

    >>> from myapp.models import SomeModel
    >>> m = SomeModel.objects.create(metavar=Markup.Format.FOO, text='Hello, World!')
    >>> m.metavar
    u'foo'
    >>> Markup.MetaVar.FOO
    u'foo'
    >>> Markup.MetaVar.ALL_OPTIONS
    (u'foo', u'bar', u'baz', u'spam', u'eggs')
    >>> Markup.MetaVar.CHOICES
    ((u'foo', 'Plain Text'), (u'basc', 'Basic'), (u'mkdn', 'Markdown'), (u'rest', 'reStructured'), (u'html', 'HTML'))
    ((u'foo', 'Foo Choice'), (u'bar', 'Bar Option'), (u'baz', 'Baz Pick'), (u'spam', 'Spam spam spam'), (u'eggs', 'Eggs, Spam, and Ham'))
    >>> Markup.MetaVar.CHOICES_DICT
    {u'foo': 'Foo Choice', u'bar': 'Bar Option', u'baz': 'Baz Pick', u'spam': 'Spam spam spam', u'eggs': 'Eggs, Spam, and Ham'}
    >>> Markup.MetaVar.DEFAULT
    u'mkdn'
    >>> m.metavar == Markup.MetaVar.Foo
    True
    >>> Markup.MetaVar.CHOICES_DICT[m.metavar]
    'Foo'
    
make_enum_class
---------------

``make_enum_class`` dynamically generates a ``ChoiceEnumeration`` derived class.

Example::

    from choice_enum import make_enum_class, Option
    MetaVar = make_enum_class('MetaVar',
        FOO=Option('foo',  'Foo Choice', default=True),
        BAR=Option('bar',  'Bar Option'),
        BAZ=Option('baz',  'Baz Pick')
    )
