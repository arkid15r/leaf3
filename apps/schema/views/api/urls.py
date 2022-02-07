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
                    path('list/',
                         person.DataTableList.as_view(),
                         name='api-person-list'),
                    path('<str:pk>/',
                         person.Item.as_view(),
                         name='api-person-item'),
                    path('<str:pk>/simple-tree/',
                         person.SimpleTree.as_view(),
                         name='api-person-simple-tree'),
                    path('<str:person_uid>/entry/',
                         entry.DataTableList.as_view(),
                         name='api-entry-list'),
                    path('<str:person_uid>/timeline/',
                         entry.Timeline.as_view(),
                         name='api-person-timeline'),
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
