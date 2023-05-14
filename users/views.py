import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django_homework import settings
from users.models import User, Location


class UserView(ListView):
    model = User
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')

    def get(self, request, *args, **kwargs):

        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("username")
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        users = []

        for user in page_obj:
            users.append({'id': user.id,
                          'first_name': user.first_name,
                          'last_name': user.last_name,
                          'username': user.username,
                          'role': user.role,
                          'age': user.age,
                          'locations': [location.name for location in user.locations.all()],
                          'total_ads': user.total_ads
                          })
        return JsonResponse({"items": users,
                             "num_pages": paginator.num_pages,
                             "total": paginator.count}, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({'id': user.id,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'username': user.username,
                             'role': user.role,
                             'age': user.age,
                             'locations': [location.name for location in user.locations.all()]
                             })


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        locations = user_data.pop('locations')
        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'])
        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.locations.add(loc)
        user.save()
        return JsonResponse({'id': user.id,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'username': user.username,
                             'role': user.role,
                             'age': user.age,
                             'locations': [loc.name for loc in user.locations.all()]})


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'role', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)
        if 'first_name' in user_data:
            self.object.first_name = user_data['first_name']
        if 'last_name' in user_data:
            self.object.last_name = user_data['last_name']
        if 'username' in user_data:
            self.object.username = user_data['username']
        if 'role' in user_data:
            self.object.role = user_data['role']
        if 'age' in user_data:
            self.object.age = user_data['age']

        if 'locations' in user_data:
            self.object.locations.clear()
            for loc_name in user_data['locations']:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.locations.add(loc)

        self.object.save()

        return JsonResponse({'id': self.object.id,
                             'first_name': self.object.first_name,
                             'last_name': self.object.last_name,
                             'username': self.object.username,
                             'role': self.object.role,
                             'age': self.object.age,
                             'locations': [loc.name for loc in self.object.locations.all()]}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
