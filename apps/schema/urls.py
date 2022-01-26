"""Schema URLs."""

from django.urls import include, path

from apps.schema.views import entity, location, person

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

            # Entity.
            path('entity/', entity.List.as_view(), name='entity-list'),
            path('entity/new/', entity.Create.as_view(), name='entity-create'),
            path('entity/<str:pk>/edit',
                 entity.Edit.as_view(),
                 name='entity-edit'),
            path('entity/<str:pk>/delete/',
                 entity.Delete.as_view(),
                 name='entity-delete'),

            # Location.
            path('location/', location.List.as_view(), name='location-list'),
            path('location/new/',
                 location.Create.as_view(),
                 name='location-create'),
            path('location/<str:pk>/edit',
                 location.Edit.as_view(),
                 name='location-edit'),
            path('location/<str:pk>/delete/',
                 location.Delete.as_view(),
                 name='location-delete'),
        ]))
]
