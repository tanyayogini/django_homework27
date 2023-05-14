import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from users.models import Location, User
from django_homework import settings


def main(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        response = []
        for category in self.object_list:
            response.append({'id': category.id,
                             'name': category.name})
        return JsonResponse(response, safe=False, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({'id': category.id,
                             'name': category.name}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category.objects.create(name=category_data["name"])
        return JsonResponse({'id': category.id,
                             'name': category.name}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)
        self.object.name = category_data["name"]
        self.object.save()
        return JsonResponse({'id': self.object.id,
                             'name': self.object.name}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


class AdView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("-price")
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        ads = []

        for ad in page_obj:
            ads.append({'id': ad.id,
                        'name': ad.name,
                        'author_id': ad.author_id.id,
                        'price': ad.price,
                        'description': ad.description,
                        'is_published': ad.is_published,
                        'category_id': ad.category_id.id,
                        'image': ad.image.url if ad.image else None
                        })
        return JsonResponse({"items": ads,
                             "num_pages": paginator.num_pages,
                             "total": paginator.count}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({'id': ad.id,
                             'name': ad.name,
                             'author_id': ad.author_id.id,
                             'price': ad.price,
                             'description': ad.description,
                             'is_published': ad.is_published,
                             'category_id': ad.category_id.id,
                             'image': ad.image.url if ad.image else None
                             })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, pk=ad_data["author_id"])
        category = get_object_or_404(Category, pk=ad_data["category_id"])
        ad = Ad.objects.create(name=ad_data["name"],
                               author_id=author,
                               price=ad_data["price"],
                               description=ad_data["description"],
                               is_published=ad_data["is_published"],
                               category_id=category)
        return JsonResponse({'id': ad.id,
                             'name': ad.name,
                             'author_id': ad.author_id.id,
                             'price': ad.price,
                             'description': ad.description,
                             'is_published': ad.is_published,
                             'category_id': ad.category_id.id
                             }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author_id', 'price', 'description', 'category_id', 'image']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        if "name" in ad_data:
            self.object.name = ad_data["name"]
        if "price" in ad_data:
            self.object.price = ad_data["price"]
        if "description" in ad_data:
            self.object.description = ad_data["description"]
        if "author_id" in ad_data:
            author = get_object_or_404(User, pk=ad_data["author_id"])
            self.object.author_id = author
        if "category_id" in ad_data:
            category = get_object_or_404(Category, pk=ad_data["category_id"])
            self.object.category_id = category
        self.object.save()

        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author_id': self.object.author_id.id,
                             'price': self.object.price,
                             'description': self.object.description,
                             'is_published': self.object.is_published,
                             'category_id': self.object.category_id.id,
                             'image': self.object.image.url if self.object.image else None
                             }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'author_id', 'price', 'description', 'category_id', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author_id': self.object.author_id.id,
                             'price': self.object.price,
                             'description': self.object.description,
                             'is_published': self.object.is_published,
                             'category_id': self.object.category_id.id,
                             'image': self.object.image.url
                             }, status=200)
