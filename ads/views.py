import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdSerializer, AdListSerializer, AdDetailSerializer, CategorySerializer, SelectionSerializer, \
    SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer


def main(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


'''class CategoryView(ListView):
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
        return JsonResponse({"status": "ok"}, status=200)'''


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    default_serializer = AdSerializer
    serializers = {
        "list": AdListSerializer,
        "retrieve": AdDetailSerializer
    }
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsStaff],
        "partial_update": [IsAuthenticated, IsOwner | IsStaff],
        "destroy": [IsAuthenticated, IsOwner | IsStaff]
    }

    default_permission = [AllowAny]

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        cat = request.GET.getlist('cat')
        if cat:
            self.queryset = self.queryset.filter(category_id__in=cat)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author_id__locations__name__icontains=location)

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        self.queryset = self.queryset.order_by("-price")

        return super().list(request, *args, **kwargs)


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


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer
    serializers = {
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer,
        "create": SelectionCreateSerializer
    }
    permissions = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner]
    }

    default_permission = [AllowAny]

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)