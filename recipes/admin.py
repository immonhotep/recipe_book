from django.contrib import admin
from .models import Profile,Food_Category,Food_Recipe,Comments
from django.contrib.auth.models import User


admin.site.register(Food_Category)
admin.site.register(Food_Recipe)
admin.site.register(Comments)

class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):

    model = User

    fields = ['username','first_name','last_name','email']

    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)





