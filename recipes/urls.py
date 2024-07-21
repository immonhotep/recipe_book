from django.urls import path
from . import views



urlpatterns = [

    path('',views.home,name='home'),
    path('all_category',views.all_category,name='all_category'),
    path('all_recipes/',views.all_recipes,name='all_recipes'),
    path('user_recipes/<int:pk>/',views.user_recipes,name='user_recipes'),
    path('show_category/<int:pk>/',views.show_category,name='show_category'),
    path('user_signup/',views.user_signup,name='user_signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('show_profile/<int:pk>/',views.show_profile,name='show_profile'),
    path('change_user_password/',views.change_user_password,name='change_user_password'),
    path('show_all_profiles/',views.show_all_profiles,name='show_all_profiles'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('add_recipe/',views.add_recipe,name='add_recipe'),
    path('add_category/',views.add_category,name='add_category'),
    path('update_recipe/<int:pk>/',views.update_recipe,name='update_recipe'),
    path('update_category/<int:pk>',views.update_category,name='update_category'),
    path('show_recipe/<int:pk>/',views.show_recipe,name='show_recipe'),
    path('delete_recipe/<int:pk>',views.delete_recipe,name='delete_recipe'),
    path('delete_category/<int:pk>/',views.delete_category,name="delete_category"),
    path('send_like/<int:pk>/',views.send_like,name='send_like'),
    path('comment_like/<int:pk>',views.comment_like,name='comment_like'),
    path('send_comment/<int:pk>/',views.send_comment,name='send_comment'),
    path('delete_comment/<int:pk>/',views.delete_comment,name='delete_comment'),
    path('modify_comment/<int:pk>/',views.modify_comment,name='modify_comment'),
    path('account_status/<int:pk>/',views.account_status,name='account_status'),
    

]

