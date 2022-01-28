"""Schema URLs."""

from django.urls import include, path

from apps.schema.views import entity, entry, location, person

urlpatterns = [
    path(
        'tree/<str:tree_uid>/',
        include([
            # Person.
            path('person/', person.List.as_view(), name='person-list'),
            path('person/new/', person.Create.as_view(), name='person-create'),
            path('person/<str:pk>/edit',
                 person.Update.as_view(),
                 name='person-update'),
            path('person/<str:pk>/delete/',
                 person.Delete.as_view(),
                 name='person-delete'),
            path(
                'person/<str:person_uid>/entry/',
                include([
                    # Entry.
                    path('', entry.List.as_view(), name='entry-list'),
                    path('new/', entry.Create.as_view(), name='entry-create'),
                    path('<str:pk>/edit',
                         entry.Update.as_view(),
                         name='entry-update'),
                    path('<str:pk>/delete/',
                         entry.Delete.as_view(),
                         name='entry-delete'),
                ])),

            # Entity.
            path('entity/', entity.List.as_view(), name='entity-list'),
            path('entity/new/', entity.Create.as_view(), name='entity-create'),
            path('entity/<str:pk>/edit',
                 entity.Update.as_view(),
                 name='entity-update'),
            path('entity/<str:pk>/delete/',
                 entity.Delete.as_view(),
                 name='entity-delete'),

            # Location.
            path('location/', location.List.as_view(), name='location-list'),
            path('location/new/',
                 location.Create.as_view(),
                 name='location-create'),
            path('location/<str:pk>/edit',
                 location.Update.as_view(),
                 name='location-update'),
            path('location/<str:pk>/delete/',
                 location.Delete.as_view(),
                 name='location-delete'),
        ]))
]
