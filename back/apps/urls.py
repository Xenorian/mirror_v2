
from django.urls import path
from . import views
from back import settings
from django.conf.urls.static import static

app_name = 'apps'

urlpatterns = [
    path('findContributor/', views.findContributor, name='findContributor'),
    path('findIssues/', views.findIssues, name='findIssues'),
    path('findActivity/', views.findActivity, name='findActivity'),
    path('basic/', views.basic, name='basic'),
    path('get_basic', views.get_basic, name='get_basic'),
    path('get_creator', views.get_creator,name='get_creator'),
    path('get_commit_activity', views.get_commit_activity, name='get_commit_activity'),
    path('pulls/',views.pulls, name='pulls'),
    path('commits/',views.commits, name='commits'),
    path('add_new_repo',views.add_new_repo, name='add_new_repo'),
    path('get_user',views.get_user, name='get_user'),
    path('get_day_count',views.get_day_count, name='get_day_count'),
    path('get_all', views.get_all, name='get_all'),
    path('delete', views.delete, name='delete'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
