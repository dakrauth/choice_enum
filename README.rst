choice_enum
===========

Wrapper class for defining DRY, encapsulated choice options for CharFields.

ChoiceEnumeration
-----------------

``ChoiceEnumeration`` class can be declared at the module or class level in 
the following format::

    class ChoiceClass(ChoiceEnumeration):
        ATTR1 = ChoiceEnumeration.Option('db_value1', 'Human readable text 1')
        ATTR2 = ChoiceEnumeration.Option('db_value2', 'Human readable text 2')

The following attributes are generated on the ChoiceEnumeration child class:

- ``ALL_OPTIONS``  - a tuple of the supplied options
- ``CHOICES``      - a Django char field choices-compatible tuple
- ``CHOICES_DICT`` - a dictionary of option:text values
- ``DEFAULT``      - (optional) the item marked as default

A typical Django example would look like::

    class SomeModel(models.Model):
        class MetaVar(ChoiceEnumeration):
            FOO  = ChoiceEnumeration.Option('foo',  'Foo Choice', default=True)
            BAR  = ChoiceEnumeration.Option('bar',  'Bar Option')
            BAZ  = ChoiceEnumeration.Option('baz',  'Baz Pick')
            SPAM = ChoiceEnumeration.Option('spam', 'Spam spam spam')
            EGGS = ChoiceEnumeration.Option('eggs', 'Eggs, Spam, and Ham')

Example interactive usage::
    >>> class MetaVar(ChoiceEnumeration):
    ...     FOO  = ChoiceEnumeration.Option('foo',  'Foo Choice', default=True)
    ...     BAR  = ChoiceEnumeration.Option('bar',  'Bar Option')
    ...     BAZ  = ChoiceEnumeration.Option('baz',  'Baz Pick')
    ...     SPAM = ChoiceEnumeration.Option('spam', 'Spam spam spam')
    ...     EGGS = ChoiceEnumeration.Option('eggs', 'Eggs, Spam, and Ham')
    >>> MetaVar.FOO
    u'foo'
    >>> MetaVar.ALL_OPTIONS
    (u'foo', u'bar', u'baz', u'spam', u'eggs')
    >>> MetaVar.CHOICES
    ((u'foo', 'Foo Choice'), (u'bar', 'Bar Option'), (u'baz', 'Baz Pick'), (u'spam', 'Spam spam spam'), (u'eggs', 'Eggs, Spam, and Ham'))
    >>> MetaVar.CHOICES_DICT
    {u'baz': 'Baz Pick', u'eggs': 'Eggs, Spam, and Ham', u'foo': 'Foo Choice', u'bar': 'Bar Option', u'spam': 'Spam spam spam'}
    >>> MetaVar.DEFAULT
    u'foo'
    >>> MetaVar.CHOICES_DICT[MetaVar.FOO]
    'Foo Choice'
    
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
