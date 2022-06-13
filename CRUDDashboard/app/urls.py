from django.urls import path
from . import views
urlpatterns = [    
    path('home/', views.home , name='home'),
    path('company/', views.company , name='company'),
    path('plan/', views.plan , name='plan'),
    path('addPlan/', views.addPlan , name='addPlan'),
    path('editPlan/<data>', views.editPlan , name='editPlan'),
    path('deletePlan/<data>', views.deletePlan , name='deletePlan'),
    path('add/', views.addDetails , name='add'),
]