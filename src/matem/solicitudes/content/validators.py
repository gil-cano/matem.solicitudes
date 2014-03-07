from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
from matem.solicitudes import solicitudesMessageFactory as _


class isFloat:
    __implements__ = (IValidator,)

    def __init__(self, name, title='Float Validator', description='Is this a float number?'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        try:
            value = float(value)
            if value < 0:
                return("Transportation cost is required, please correct.")
        except:
                return("'%s' is not float (illegal value)" % str(value))





class StartBeforeEnd:
    """Validate as True when having at least one DataGrid item.
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        #import pdb; pdb.set_trace( )
        pass



# def validateStartEnd(data):
#         if data.start is not None and data.end is not None:
#             if data.start > data.end:
#                 raise StartBeforeEnd(_(
#                     u"The start time must be before the end time"))


        # try:
        #     length = len(value) - 1
        # except TypeError:
        #     return ("Validation failed(%s): cannot calculate length "
        #             "of %s.""" % (self.name, value))
        # except AttributeError:
        #     return ("Validation failed(%s): cannot calculate length "
        #             "of %s.""" % (self.name, value))
        # if length < 1:
        #     return _("Validation failed: Need at least one entry.")

        # for row in value:
        #     if row['orderindex_'] != 'template_row_marker':
        #         if not(row['name'] and row['patern']):
        #             return _("Validation failed: The name and the lastname are required.")
        # return True
