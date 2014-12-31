'''Wrapper class for defining DRY, encapsulated choice options for CharFields.'''
import itertools

__version_info__ = (0, 2)
__version__ = '.'.join(map(str, __version_info__))

#===============================================================================
class ChoiceOption(unicode):
    '''
    An enumeration instance "factory"
    '''
    _counter = itertools.count()
    
    #---------------------------------------------------------------------------
    def __new__(cls, value, display, default=False):
        u = super(ChoiceOption, cls).__new__(cls, value)
        u.display = display
        u.default = default
        u.rank = next(ChoiceOption._counter)
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
        for key, value in attrs.iteritems():
            if isinstance(value, ChoiceOption):
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

        class Markup(models.Model):

            # ``Format`` scoped here under the Markup class, but could have been a 
            # declared at the module level as well

            class Format(ChoiceEnumeration):
                TEXT      = ChoiceEnumeration.Option('text',  'Plain Text')
                BASIC     = ChoiceEnumeration.Option('basc',  'Basic')
                MARKDOWN  = ChoiceEnumeration.Option('mkdn',  'Markdown', default=True)
                RST       = ChoiceEnumeration.Option('rest',  'reStructured')
                HTML      = ChoiceEnumeration.Option('html',  'HTML')

            text = models.TextField()
            format = models.CharField(
                choices=Format.CHOICES,
                default=Format.DEFAULT,
                max_length=4
            )
    
    Example interactive usage::

        >>> from annotation.models import Markup
        >>> m = Markup.objects.create(format=Markup.Format.MARKDOWN, text='Hello\n=====\n\nFoo!')
        >>> m.format
        u'mkdn'
        >>> Markup.Format.MARKDOWN
        u'mkdn'
        >>> Markup.Format.ALL_OPTIONS
        (u'text', u'basc', u'mkdn', u'rest', u'html')
        >>> Markup.Format.CHOICES
        ((u'text', 'Plain Text'), (u'basc', 'Basic'), (u'mkdn', 'Markdown'), (u'rest', 'reStructured'), (u'html', 'HTML'))
        >>> Markup.Format.CHOICES_DICT
        {u'text': 'Plain Text', u'mkdn': 'Markdown', u'html': 'HTML', u'basc': 'Basic', u'rest': 'reStructured'}
        >>> Markup.Format.DEFAULT
        u'mkdn'
        >>> m.format == Markup.Format.MARKDOWN
        True
        >>> Markup.Format.CHOICES_DICT[m.format]
        'Markdown'
        
    '''
    __metaclass__ = ChoiceEnumMetaclass
    Option = ChoiceOption
