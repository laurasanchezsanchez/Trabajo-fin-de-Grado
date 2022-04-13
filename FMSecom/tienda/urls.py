from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.categorias, name='categorias'),
    path('categoria/<slug>/', views.categoria_filtrada, name='categoria'),
    path('producto/<slug>/', views.ProductDetailView.as_view(),
         name='producto-detallado'),
    path('carrito/', views.CarritoView.as_view(), name='resumen-carrito'),
    path('incrementar-cantidad/<pk>/', views.IncrementarCantidadView.as_view(), name='incrementar-cantidad'),
    path('decrementar-cantidad/<pk>/', views.DecrementarCantidadView.as_view(), name='decrementar-cantidad'),
    path('eliminar-del-carrito/<pk>/', views.EliminarDelCarritoView.as_view(), name='eliminar-del-carrito'),

]
