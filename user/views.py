from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from user.forms import LoginForm,SignupForm
from django.core.signing import TimestampSigner, SignatureExpired
from django.shortcuts import redirect, render, get_object_or_404
from django.core import signing
from django.views.generic import (
    CreateView,
    FormView,
)
from utils.email import send_email

User = get_user_model()


class UserSignUp(CreateView):
    form_class = SignupForm
    template_name = "user/user_signup.html"


    def form_valid(self,form):
        user = form.save(commit=False)
        user.save()
        signer = TimestampSigner()
        signed_user = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user)
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}'
        subject = "[Pystagram] 이메일 인증을 완료해주세요"
        message = f"다음 링크를 클릭해주세요.<br><a href='{url}'>url</a>"

        send_email(subject, message,user.email,to_email=user.email)

        return render(
            self.request,
            "user/signup_done.html",
        )

    def verify_email(request):
        code = request.GET.get("code","")
        signer = TimestampSigner()
        try:
            decided_user_email = signing.loads(code)
            email = signer.unsign(decided_user_email,max_age = 60*30)
        except (TypeError, SignatureExpired):
            return render(request,"user/verify_failed.html")
        user = get_object_or_404(User, email=email, is_active=False)
        user.is_active = True
        user.save()
        return render(request, "user/verify_success.html",)


class LoginView(FormView):
    form_class =LoginForm
    template_name = "user/user_login.html"
    success_url = reverse_lazy("todo:list")

    def form_valid(self,form):
        user = form.get_user()
        login(self.request, user=user)
        return HttpResponseRedirect(self.get_success_url())



