from django.urls import path
from . import views
from .views import PostListView, UserPostListView, PostUpdateView, PostDetailView, PostCreateView, PostDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),    #List View
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),    #Detail View
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    # path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('login/', views.login, name='blog-login'),
    path('logout/', views.logout, name='blog-logout'),
    path('register/', views.register, name='blog-register'),
    path('profile/', views.profile, name='blog-profile'),
    path('create/', views.postCreate, name='blog-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
