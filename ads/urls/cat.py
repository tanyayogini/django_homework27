from django.urls import path

from ads.views import CategoryView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('', CategoryView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('create/', CategoryCreateView.as_view()),
    path('<int:pk>/update/', CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryDeleteView.as_view()),

]