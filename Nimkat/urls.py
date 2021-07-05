"""Nimkat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .views import PrivateGraphQLView
from django.contrib.auth.views import LogoutView
from graphene_file_upload.django import FileUploadGraphQLView
from django.conf import settings
from .views import DownloadGraphQlSchema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('download_schema', csrf_exempt(DownloadGraphQlSchema.as_view())),
    path('logout', LogoutView.as_view()),
    path('api/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=False)))
]

if settings.DEBUG:
    urlpatterns.append(path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
                       )
