import random

from django.shortcuts import render
from django.views import View
from tours import data


def _get_list_of_tours_with_id(tours: dict) -> list:
    """ Из словаря dict получаем список словарей с добавлением в каждый поля id """
    trs = [t for t in tours.items()]
    for t in trs:
        t[1].update({'id': t[0]})
    trs = [t[1] for t in trs]
    return trs


class MainView(View):
    def get(self, request, *args, **kwargs):
        tours = _get_list_of_tours_with_id(data.tours)
        random_tours = random.sample(tours, 6)
        return render(request=request,
                      template_name='tours/index.html',
                      context={
                          'title': data.title,
                          'navigation': data.departures,
                          'navtitle': data.title,
                          'subtitle': data.subtitle,
                          'description': data.description,
                          'tours': random_tours,
                      })


class DepartureView(View):
    def get(self, request, *args, **kwargs):
        departure = kwargs['departure']
        tours = _get_list_of_tours_with_id(data.tours)
        selected_tours = [t for t in tours if t['departure'] == departure]
        filter_values = {'tours_num': len(selected_tours)}
        pricemin = min(t['price'] for t in selected_tours)
        pricemax = max(t['price'] for t in selected_tours)
        nightsmin = min(t['nights'] for t in selected_tours)
        nightsmax = max(t['nights'] for t in selected_tours)
        filter_values.update({'pricemin': pricemin, 'pricemax': pricemax,
                              'nightsmin': nightsmin, 'nightsmax': nightsmax})
        return render(request=request,
                      template_name='tours/departure.html',
                      context={
                          'title': "Летим " + data.departures[departure],
                          'navigation': data.departures,
                          'navtitle': data.title,
                          'subtitle': data.subtitle,
                          'description': data.description,
                          'tours': selected_tours,
                          'filter_values': filter_values,
                          'departure': data.departures[departure].split()[-1]
                      })


class TourView(View):
    def get(self, request, *args, **kwargs):
        tour = data.tours[self.kwargs.get('id')]
        return render(request=request,
                      template_name='tours/tour.html',
                      context={
                          'title': f"{tour['title']} {tour['stars']} {int(tour['stars'])*'★'}",
                          'navigation': data.departures,
                          'navtitle': data.title,
                          'tour': tour,
                          'departure': data.departures[tour['departure']],
                          'departures': data.departures
                      })


def page_not_found_view(request, exception):
    return render(request=request, template_name='tours/error.html', status=404, context={'code': '404'})


def error_view(request):
    return render(request=request, template_name='tours/error.html', status=500, context={'code': '500'})
