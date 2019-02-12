from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # previous login view
    url(r'^login/$', LoginView.as_view(template_name='account/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]
