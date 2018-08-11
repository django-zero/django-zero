from allauth.account.forms import LoginForm as BaseLoginForm
from allauth.account.forms import ResetPasswordForm as BaseResetPasswordForm
from allauth.account.forms import SignupForm as BaseSignupForm
from django.utils.translation import ugettext_lazy as _


class LoginForm(BaseLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""

        self.fields["login"].widget.attrs["class"] = "form-control"
        self.fields["login"].widget.attrs["placeholder"] = ""

        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = ""

        self.fields["remember"].label = _("Keep me signed in.")


class SignupForm(BaseSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""

        if "username" in self.fields:
            self.fields["username"].widget.attrs["class"] = "form-control"
            self.fields["username"].widget.attrs["placeholder"] = ""
            self.fields["username"].label = _("Your username")

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = ""
        self.fields["email"].label = _("Email address")

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = _("At least 8 characters")

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = ""
        self.fields["password2"].label = _("Re-enter password")


class ResetPasswordForm(BaseResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = ""
