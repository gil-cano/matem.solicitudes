from Products.validation.interfaces.IValidator import IValidator


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
