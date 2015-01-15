'''Wrapper class for defining DRY, encapsulated choice options for CharFields.'''
import itertools

__version_info__ = (0, 2, 1)
__version__ = '.'.join(map(str, __version_info__))

#===============================================================================
class Option(unicode):
    '''
    An enumeration instance "factory"
    '''
    _counter = itertools.count()
    
    #---------------------------------------------------------------------------
    def __new__(cls, value, display, default=False):
        u = super(Option, cls).__new__(cls, value)
        u.display = display
        u.default = default
        u.rank = next(Option._counter)
        return u
        
    #---------------------------------------------------------------------------
    def __deepcopy__(self, memo):
        '''
        Need this so that cloned querysets can effectively copy the instance
        '''
        obj = unicode(self)
        memo[id(self)] = obj
        return obj


#===============================================================================
class ChoiceEnumMetaclass(type):
    
    #---------------------------------------------------------------------------
    def __new__(cls, name, bases, attrs):
        all_opts = []
        choices = []
        new_attrs = {}
        default = None
        reserved = ('ALL_OPTIONS', 'CHOICES', 'CHOICES_DICT', 'DEFAULT')
        
        for key, value in attrs.iteritems():
            if key in reserved:
                raise ValueError('"%s" is reserved')
                
            if isinstance(value, Option):
                u = unicode(value)
                if value.default:
                    if default is not None:
                        raise ValueError('Only one default option allowed')
                    default = u
                        
                all_opts.append((value.rank, u))
                choices.append((value.rank, u, value.display))
                
            new_attrs[key] = value
                
        new_attrs['ALL_OPTIONS'] = tuple([v[1] for v in sorted(all_opts)])
        new_attrs['CHOICES'] = tuple([v[1:] for v in sorted(choices)])
        new_attrs['CHOICES_DICT'] = dict(new_attrs['CHOICES'])
        new_attrs['DEFAULT'] = default or None
        return super(ChoiceEnumMetaclass, cls).__new__(cls, name, bases, new_attrs)


#===============================================================================
class ChoiceEnumeration(object):
    '''
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
        
    '''
    __metaclass__ = ChoiceEnumMetaclass
    Option = Option


#-------------------------------------------------------------------------------
def make_enum_class(cls_name, **kws):
    '''
    ``make_enum_class`` dynamically generates a ``ChoiceEnumeration`` derived class.
    
    Example::
    
        from choice_enum import make_enum_class, Option
        MetaVar = make_enum_class('MetaVar',
            FOO=Option('foo',  'Foo Choice', default=True),
            BAR=Option('bar',  'Bar Option'),
            BAZ=Option('baz',  'Baz Pick')
        )
    '''
    return type(cls_name, (ChoiceEnumeration,), kws)


################################################################################
if __name__ == "__main__":
    import doctest
    doctest.testmod()
