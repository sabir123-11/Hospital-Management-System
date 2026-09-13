from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from hospital import views
from pathlib import Path

STATIC_ROOT_DIR = Path(settings.BASE_DIR) / 'static'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages
    path('', views.index, name='index'),
    path('index.html', views.index),
    path('about.html', views.about, name='about'),
    path('departments.html', views.departments, name='departments'),
    path('doctors.html', views.doctors, name='doctors'),
    path('services.html', views.services, name='services'),
    path('gallery.html', views.gallery, name='gallery'),
    path('blog.html', views.blog, name='blog'),
    path('faq.html', views.faq, name='faq'),
    path('careers.html', views.careers, name='careers'),
    path('contact.html', views.contact, name='contact'),
    path('appointment.html', views.appointment, name='appointment'),
    path('login.html', views.login_page, name='login'),
    path('register.html', views.register_page, name='register'),
    path('privacy-policy.html', views.privacy, name='privacy'),
    path('terms.html', views.terms, name='terms'),

    # API / form endpoints
    path('api/appointment/', views.submit_appointment, name='api_appointment'),
    path('api/contact/', views.submit_contact, name='api_contact'),
    path('api/career/', views.submit_career, name='api_career'),
    path('api/register/', views.submit_register, name='api_register'),
    path('api/login/', views.submit_login, name='api_login'),
    path('api/logout/', views.submit_logout, name='api_logout'),
    path('api/chatbot/', views.chatbot_api, name='api_chatbot'),

    # Serve original asset paths so existing HTML works unchanged
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT_DIR / 'css'}),
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT_DIR / 'js'}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT_DIR / 'images'}),
    re_path(r'^icons/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT_DIR / 'icons'}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT_DIR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
