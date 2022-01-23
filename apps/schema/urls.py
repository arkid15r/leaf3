"""Schema URLs."""

from django.urls import include, path

from apps.schema.views import person

urlpatterns = [
    path(
        'tree/<str:tree_uid>/',
        include([
            # Person.
            path('person/', person.List.as_view(), name='person-list'),
            path('person/new/', person.Create.as_view(), name='person-create'),
            path('person/<str:pk>/edit',
                 person.Edit.as_view(),
                 name='person-edit'),
            path('person/<str:pk>/delete/',
                 person.Delete.as_view(),
                 name='person-delete'),
        ]))
]
