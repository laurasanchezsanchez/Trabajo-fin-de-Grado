from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tienda'

urlpatterns = [
    path('', views.categorias, name='tienda'),
    path('categoria/<slug>/', views.categoria_filtrada, name='categoria'),
    path('producto/<slug>/', views.ProductDetailView.as_view(),
         name='producto-detallado'),
    path('carrito/', views.CarritoView.as_view(), name='resumen-carrito'),
    path('eliminar-del-carrito/<pk>/', views.EliminarDelCarritoView.as_view(), name='eliminar-del-carrito'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('mis-pedidos/', views.MisPedidosView.as_view(), name='mis-pedidos'),
    path('payment/', views.PaymentView.as_view(), name='payment'),

    path('config/', views.stripe_config),  
    path('create-checkout-session/', views.create_checkout_session), # new
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()), # new
    path('search',views.search,name='search'),
    path('detalles-pedido/<pk>',views.detallesPedido, name='detalles-pedido'),
]
