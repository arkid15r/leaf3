"""Tree URLs."""

from django.urls import path

from apps.tree import views as tree_views

urlpatterns = [
    path('dashboard/', tree_views.Dashboard.as_view(), name='tree-dashboard'),
    path('tree/new/', tree_views.Create.as_view(), name='tree-create'),
    path('tree/<str:pk>/', tree_views.View.as_view(), name='tree-view'),
    path('tree/<str:pk>/edit/', tree_views.Update.as_view(),
         name='tree-update'),
    path('tree/<str:pk>/delete/',
         tree_views.Delete.as_view(),
         name='tree-delete'),
]
