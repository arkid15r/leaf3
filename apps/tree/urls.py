"""Tree URLs."""

from django.urls import path

from apps.tree import views as tree_views

urlpatterns = [
    path('dashboard/', tree_views.Dashboard.as_view(), name='tree-dashboard'),
    path('tree/<str:pk>/', tree_views.Manage.as_view(), name='tree-manage'),
    path('tree/new/', tree_views.Create.as_view(), name='tree-create'),
    path('tree/<str:pk>/edit/', tree_views.Edit.as_view(), name='tree-edit'),
    path('tree/<str:pk>/delete/',
         tree_views.Delete.as_view(),
         name='tree-delete'),
]
