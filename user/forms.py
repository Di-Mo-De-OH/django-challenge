from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ("password1","password2"):
            self.fields[field].widget.attrs["class"]= "form-control"
            self.fields[field].widget.attrs["placeholder"] = "password"
            if field =="password1":
                self.fields[field].label = "비밀번호"
            else:
                self.fields[field].label = "비밀번화 확인"

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("name","email")
        labels = {
            "name":"이름",
            "email":"이메일"
        }
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "example@example.com",
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "이름",
                    "class": "form-control",
                }
            ),
        }
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        required = True,
        widget= forms.EmailInput(
            attrs= {
                "class": "form-control",
                "placeholder": "example@example.com",
            }
        )
    )
    password = forms.CharField(
        label="password",
        required = True,
        widget =forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
            }
        )
    )




