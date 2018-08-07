# Authentication related settings.

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    "login": "django_zero.auth.forms.LoginForm",
    "reset_password": "django_zero.auth.forms.ResetPasswordForm",
    "signup": "django_zero.auth.forms.SignupForm",
}

__all__ = ["AUTHENTICATION_BACKENDS", "AUTH_PASSWORD_VALIDATORS", "ACCOUNT_EMAIL_REQUIRED", "ACCOUNT_FORMS"]
