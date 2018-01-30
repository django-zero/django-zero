import json
import os

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import gettext
from django_includes.jinja2 import DjangoIncludesExtension
from jinja2 import Environment, nodes, lexer
from jinja2.ext import Extension
from markupsafe import Markup


class AssetsHelper:
    def __init__(self, filename):
        self.filename = filename
        self._data = None
        self._path = '/static'

    @property
    def data(self):
        if not self._data:
            with open(self.filename) as f:
                self._data = json.load(f)
        return self._data

    def get_stylesheets(self, name):
        try:
            bundle = self.data[name]
        except KeyError as e:
            return ''

        try:
            return Markup('<link href="' + staticfiles_storage.url(bundle['css']) + '" rel="stylesheet">')

        except KeyError as e:
            return ''

    def get_javascripts(self, name):
        try:
            bundle = self.data[name]
        except KeyError as e:
            return ''

        try:
            return Markup(
                '<script src="' + os.path.join(self._path, bundle['js']) + '" type="text/javascript"></script>')
        except KeyError as e:
            return ''


class DjangoCsrfExtension(Extension):
    """
    Implements django's `{% csrf_token %}` tag.
    """
    tags = {'csrf_token'}

    def parse(self, parser):
        lineno = parser.stream.expect('name:csrf_token').lineno
        call = self.call_method('_csrf_token', [nodes.Name('csrf_token', 'load', lineno=lineno)], lineno=lineno)
        return nodes.Output([nodes.MarkSafe(call)])

    def _csrf_token(self, csrf_token):
        if not csrf_token or csrf_token == 'NOTPROVIDED':
            return ''
        else:
            return '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)


class DjangoUrlExtension(Extension):
    """
    Imlements django's `{% url %}` tag.
    It works as it does in django, therefore you can only specify either
    args or kwargs::
        Url with args: {% url 'my_view' arg1 "string arg2" %}
        Url with kwargs: {% url 'my_view' kwarg1=arg1 kwarg2="string arg2" %}
        Save to variable:
        {% url 'my_view' 'foo' 'bar' as my_url %}
        {{ my_url }}
    """
    tags = {'url'}

    def _url_reverse(self, name, *args, **kwargs):
        return reverse(name, args=args, kwargs=kwargs)

    @staticmethod
    def parse_expression(parser):
        # Due to how the jinja2 parser works, it treats "foo" "bar" as a single
        # string literal as it is the case in python.
        # But the url tag in django supports multiple string arguments, e.g.
        # "{% url 'my_view' 'arg1' 'arg2' %}".
        # That's why we have to check if it's a string literal first.
        token = parser.stream.current
        if token.test(lexer.TOKEN_STRING):
            expr = nodes.Const(force_text(token.value), lineno=token.lineno)
            next(parser.stream)
        else:
            expr = parser.parse_expression(False)

        return expr

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        view_name = parser.stream.expect(lexer.TOKEN_STRING)
        view_name = nodes.Const(view_name.value, lineno=view_name.lineno)

        args = None
        kwargs = None
        as_var = None

        while parser.stream.current.type != lexer.TOKEN_BLOCK_END:
            token = parser.stream.current
            if token.test('name:as'):
                next(parser.stream)
                token = parser.stream.expect(lexer.TOKEN_NAME)
                as_var = nodes.Name(token.value, 'store', lineno=token.lineno)
                break
            if args is not None:
                args.append(self.parse_expression(parser))
            elif kwargs is not None:
                if token.type != lexer.TOKEN_NAME:
                    parser.fail(
                        "got '{}', expected name for keyword argument"
                        "".format(lexer.describe_token(token)),
                        lineno=token.lineno
                    )
                arg = token.value
                next(parser.stream)
                parser.stream.expect(lexer.TOKEN_ASSIGN)
                token = parser.stream.current
                kwargs[arg] = self.parse_expression(parser)
            else:
                if parser.stream.look().type == lexer.TOKEN_ASSIGN:
                    kwargs = {}
                else:
                    args = []
                continue

        if args is None:
            args = []
        args.insert(0, view_name)

        if kwargs is not None:
            kwargs = [nodes.Keyword(key, val) for key, val in kwargs.items()]

        call = self.call_method('_url_reverse', args, kwargs, lineno=lineno)
        if as_var is None:
            return nodes.Output([call], lineno=lineno)
        else:
            return nodes.Assign(as_var, call, lineno=lineno)


def environment(**options):
    env = Environment(extensions=['jinja2.ext.i18n'], **options)
    from django.utils import translation
    env.install_gettext_translations(translation)

    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'assets': AssetsHelper('.cache/assets.json'),
        '_': gettext,
    })

    env.add_extension(DjangoCsrfExtension)
    env.add_extension(DjangoIncludesExtension)
    env.add_extension(DjangoUrlExtension)

    return env
