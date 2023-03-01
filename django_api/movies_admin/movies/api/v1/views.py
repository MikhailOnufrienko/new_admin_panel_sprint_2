from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.db import connection

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_queryset(self):
        queryset = Filmwork.objects.prefetch_related(
            'genres', 'persons'
        ).values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg(
                'genres__name', distinct=True
            ),
            actors=ArrayAgg(
                'persons__full_name', filter=Q(persons__personfilmwork__role='actor'), distinct=True
            ),
            directors=ArrayAgg(
                'persons__full_name', filter=Q(persons__personfilmwork__role='director'), distinct=True
            ),
            writers=ArrayAgg(
                'persons__full_name', filter=Q(persons__personfilmwork__role='writer'), distinct=True
            ),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = context['page_obj']
        results = list(page.object_list.values())
        count = paginator.count
        total_pages = paginator.num_pages
        prev_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None

        context = {
            'count': count,
            'total_pages': total_pages,
            'prev': prev_page,
            'next': next_page,
            'results': results
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = context['object']
        data = {
            'id': movie['id'],
            'title': movie['title'],
            'description': movie['description'],
            'creation_date': movie['creation_date'],
            'rating': movie['rating'],
            'type': movie['type'],
            'genres': movie['genres'],
            'actors': movie['actors'],
            'directors': movie['directors'],
            'writers': movie['writers'],
        }
        return data
