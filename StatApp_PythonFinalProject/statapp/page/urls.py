from django.urls import path
from . import views
from page.views import upload_fileDes, view_dataset, upload_fileReg

urlpatterns = [
    path("", views.home, name="home"),
    path("upload-file/", upload_fileDes, name="upload-fileDes"),
    path("regression-output/", upload_fileReg, name="upload-fileReg"),
    path('dataset/<int:dataset_id>/', view_dataset, name='view_dataset')
]