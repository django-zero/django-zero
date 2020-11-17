import re

from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import gettext
from django_includes.jinja2 import DjangoIncludesExtension
from jinja2 import Environment, lexer, nodes
from jinja2.ext import Extension

from django_zero import assets


class DjangoCsrfExtension(Extension):
    """
    Implements django's `{% csrf_token %}` tag.
    """

    tags = {"csrf_token"}

    def parse(self, parser):
        lineno = parser.stream.expect("name:csrf_token").lineno
        call = self.call_method("_csrf_token", [nodes.Name("csrf_token", "load", lineno=lineno)], lineno=lineno)
        return nodes.Output([nodes.MarkSafe(call)])

    def _csrf_token(self, csrf_token):
        if not csrf_token or csrf_token == "NOTPROVIDED":
            return ""
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

    tags = {"url"}

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
            if token.test("name:as"):
                next(parser.stream)
                token = parser.stream.expect(lexer.TOKEN_NAME)
                as_var = nodes.Name(token.value, "store", lineno=token.lineno)
                break
            if args is not None:
                args.append(self.parse_expression(parser))
            elif kwargs is not None:
                if token.type != lexer.TOKEN_NAME:
                    parser.fail(
                        "got '{}', expected name for keyword argument" "".format(lexer.describe_token(token)),
                        lineno=token.lineno,
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

        call = self.call_method("_url_reverse", args, kwargs, lineno=lineno)
        if as_var is None:
            return nodes.Output([call], lineno=lineno)
        else:
            return nodes.Assign(as_var, call, lineno=lineno)


class SpacelessExtension(Extension):
    """
    Removes whitespace between HTML tags at compile time, including tab and newline characters.
    It does not remove whitespace between jinja2 tags or variables. Neither does it remove whitespace between tags
    and their text content.
    Adapted from coffin:
        https://github.com/coffin/coffin/blob/master/coffin/template/defaulttags.py
    """

    tags = {"spaceless"}

    def parse(self, parser):
        next(parser.stream)
        lineno = parser.stream.current.lineno
        body = parser.parse_statements(["name:endspaceless"], drop_needle=True)
        return nodes.CallBlock(self.call_method("_strip_spaces", [], [], None, None), [], [], body).set_lineno(lineno)

    def _strip_spaces(self, caller=None):
        return re.sub(r">\s+<", "><", caller().strip())


def environment(**options):
    from django.conf import settings
    from django.urls import translate_url
    from django.utils import translation

    env = Environment(extensions=["jinja2.ext.i18n"], **options)
    env.install_gettext_translations(translation)

    env.globals.update(
        {
            "_": gettext,
            "get_messages": messages.get_messages,
            "settings": settings,
            "static": staticfiles_storage.url,
            "url": reverse,
            "get_language": translation.get_language,
            "translate_url": translate_url,
        }
    )

    from django_zero.config.settings import features

    if features.is_webpack_enabled():
        env.globals.update(
            {
                "assets": assets.get_helper(),
            }
        )

    env.add_extension(DjangoCsrfExtension)
    env.add_extension(DjangoIncludesExtension)
    env.add_extension(DjangoUrlExtension)
    env.add_extension(SpacelessExtension)

    return env
