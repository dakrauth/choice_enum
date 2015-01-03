'''Wrapper class for defining DRY, encapsulated choice options for CharFields.'''
import itertools

__version_info__ = (0, 2)
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
    Takes the following format::
    
        class ChoiceClass(ChoiceEnumeration):
            CLASS_ATTR1 = ChoiceEnumeration.Option('db_value1', 'Human readable text 1')
            CLASS_ATTR2 = ChoiceEnumeration.Option('db_value2', 'Human readable text 2')
    
    The following attributes are generated on the ChoiceEnumeration child class:

    * ALL_OPTIONS  - a tuple of the supplied options
    * CHOICES      - a Django char field choices-compatible tuple
    * CHOICES_DICT - a dictionary of option:text values
    * DEFAULT      - (optional) the item marked as default
    
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
        
    '''
    __metaclass__ = ChoiceEnumMetaclass
    Option = Option


#-------------------------------------------------------------------------------
def make_options(cls_name, **kws):
    return type(name, (ChoiceEnumeration,), kws)
