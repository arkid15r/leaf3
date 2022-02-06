"""Schema API views URLs."""

from django.urls import include, path

from apps.schema.views.api import entity, entry, location, person

urlpatterns = [
    path(
        'api/tree/<str:tree_uid>/',
        include([
            path(
                'person/',
                include([
                    path('',
                         person.DataTableList.as_view(),
                         name='api-person-list'),
                    path('<str:pk>/simple-tree/',
                         person.SimpleTree.as_view(),
                         name='api-person-simple-tree'),
                    path('<str:person_uid>/entry/',
                         entry.DataTableList.as_view(),
                         name='api-entry-list'),
                ])),
            path(
                'location/',
                include([
                    path('',
                         location.DataTableList.as_view(),
                         name='api-location-list'),
                ])),
            path(
                'entity/',
                include([
                    path('',
                         entity.DataTableList.as_view(),
                         name='api-entity-list'),
                ])),
        ])),
]
