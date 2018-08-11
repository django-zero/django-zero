from jinja2.ext import Extension


def camelcase(s):
    return "".join(x for x in s.title() if x.isalpha())


class DjangoZeroTemplatesExtension(Extension):
    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super(DjangoZeroTemplatesExtension, self).__init__(environment)

        environment.filters["camelcase"] = camelcase
