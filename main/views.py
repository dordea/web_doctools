from django.shortcuts import render, redirect
from .models import upload
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('downloads')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link !!!!'
            message = render_to_string('email_acctivation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'sended.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'thx.html')
    else:
        return render(request, 'invalid.html')


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def downloads(request):
    if request.method == 'POST':
        title = request.POST['title']
        upload1 = request.FILES['upload']
        obiect = upload.objects.create(title=title, upload=upload1)
        obiect.save()
    context = upload.objects.order_by('-id')
    last = upload.objects.order_by('id').last()
    mac = upload.objects.get(title="Beta")
    lin = upload.objects.get(title="DocsTool v0")
    return render(request, 'download.html', {'context': context, 'last': last, 'mac': mac, 'lin': lin})
