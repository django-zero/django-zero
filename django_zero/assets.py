import json
import os
import warnings

from markupsafe import Markup


class AssetsHelper:
    def __init__(self, filename):
        self.filename = filename
        self._data = None
        self._mtime = None

    @property
    def data(self):
        mtime = os.path.getmtime(self.filename)
        if mtime != self._mtime or not self._data:
            try:
                with open(self.filename) as f:
                    self._data = json.load(f)
                self._mtime = mtime
            except OSError as exc:
                warnings.warn(
                    "Unreadable assets (looked for %r). Maybe webpack is still running?".format(self.filename)
                )
                return {}
        return self._data

    def get_stylesheets(self, *names):
        return Markup("".join(map(self.get_stylesheet, names)))

    def get_stylesheet(self, name):
        try:
            bundle = self.data[name]
        except KeyError as e:
            return ""

        try:
            return Markup('<link href="' + bundle["css"] + '" rel="stylesheet">')
        except KeyError as e:
            message = "Stylesheet bundle not found: {}".format(name)
            warnings.warn(message)
            return Markup("<!-- {} -->".format(message))

    def get_javascripts(self, *names):
        return Markup("".join(map(self.get_javascript, names)))

    def get_javascript(self, name):
        try:
            bundle = self.data[name]
        except KeyError as e:
            return ""

        try:
            return Markup('<script src="' + bundle["js"] + '" type="text/javascript"></script>')
        except KeyError as e:
            message = "Javascript bundle not found: {}".format(name)
            warnings.warn(message)
            return Markup("<!-- {} -->".format(message))


_default_helper = None


def get_helper():
    global _default_helper
    if _default_helper is None:
        from django.conf import settings

        _default_helper = AssetsHelper(os.path.join(settings.BASE_DIR, "assets.json"))
    return _default_helper
