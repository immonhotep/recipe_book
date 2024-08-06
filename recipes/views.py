from django.shortcuts import render,redirect
from .models import Food_Category,User,Profile,Food_Recipe,Comments
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm,UpdateUserForm,AddFoodRecipeForm,UpdateCommentForm,AddFoodCategoryForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
import re 




def home(request):

    recipes = Food_Recipe.objects.annotate(like_count=Count('like')).order_by('-like_count')
   

    context={'recipes':recipes}
    return render(request,'recipes/home.html',context)



def all_category(request):

   
    all_category = Food_Category.objects.all().order_by('name')
    p = Paginator(all_category,6)
    page = request.GET.get('page')
    categories = p.get_page(page)


    context={'categories':categories,'all_category':all_category}
    return render(request,'recipes/categories.html',context)


    



def all_recipes(request):

    if request.method == "POST":

        search = request.POST.get('search')
        recipes = Food_Recipe.objects.filter(Q(name__icontains=search)|Q(description__icontains=search))
        
        if not recipes:
            messages.error(request,f'Not found any recipe with {search}')



        context = {'recipes':recipes}
        return render(request,'recipes/all_recipes.html',context)



    all_recipes = Food_Recipe.objects.all().order_by('date_added')
    p = Paginator(all_recipes,6)
    page = request.GET.get('page')
    recipes = p.get_page(page)


    context = {'recipes':recipes,'all_recipes':all_recipes}
    return render(request,'recipes/all_recipes.html',context)



def user_recipes(request,pk):

    recipe_user = User.objects.get(id=pk)
    all_recipes = Food_Recipe.objects.filter(user=recipe_user).order_by('date_added')

    p = Paginator(all_recipes,6)
    page = request.GET.get('page')
    recipes = p.get_page(page)



    context={'recipes':recipes,'all_recipes':all_recipes,'recipe_user':recipe_user}
    return render(request,'recipes/all_recipes.html',context)



def user_signup(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        
        

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pat = re.compile(regex)
        mat = re.search(pat, password1)

        if not mat:

             messages.error(request,f'Invalid password')
             return redirect('user_signup')



        if password1 == password2:
            
            if User.objects.filter(username=username).exists():

                messages.error(request,f'the Username: {username} already exist on the database')
                return redirect('user_signup')
            
            elif User.objects.filter(email=email).exists():

                messages.error(request,f'the Email: {email} already exist on the database')
                return redirect('user_signup')
            
            
            
            else:
                
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()

                user_login = authenticate(username=username,password=password1)

                if user_login  is  not None:

                    login(request,user_login)
                    messages.success(request,'Your account has been created successfully')
                    return redirect('update_profile')


                

        else:

            messages.error(request,"The two password field didn't matched" )
            return redirect('user_signup')
            

    context={}
    return render(request,'recipes/register.html',context)



def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_login = authenticate(username=username,password=password)

        if user_login is not None:
            login(request,user_login)
            messages.success(request,f'You have been logged in - {username} ')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials ')

    context={}
    return render(request,'recipes/login.html',context)


@login_required(login_url='user_login')
def user_logout(request):

    logout(request)
    messages.success(request,'You have been  logged out ')
    return redirect('home')




def show_all_profiles(request):

    all_profiles = Profile.objects.all().order_by('user')
    p = Paginator(all_profiles,5)
    page = request.GET.get('page')
    profiles = p.get_page(page)

   

    context={'profiles':profiles,'all_profiles':all_profiles}
    return render(request,'recipes/all_profiles.html',context)



@login_required(login_url='user_login')
def show_profile(request,pk):

    user = get_object_or_404(User,pk=pk)
    profile = get_object_or_404(Profile,user=user)

    all_recipes = Food_Recipe.objects.filter(user=user).order_by('date_added')

    p = Paginator(all_recipes,6)
    page = request.GET.get('page')
    recipes = p.get_page(page)



    context={'profile':profile,'recipes':recipes,'all_recipes':all_recipes}
    return render(request,'recipes/profile_page.html',context)



@login_required(login_url='user_login')
def update_profile(request):

    profile = Profile.objects.get(id = request.user.profile.id)


    if request.method == "POST":

        user_form = UpdateUserForm(request.POST,instance=request.user)
        profile_form = UpdateProfileForm(request.POST,request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect(update_profile)
        
        else:

            for error in list(user_form.errors.values()):

                messages.error(request,error)
                return redirect(update_profile)
            
            for error in list(profile_form.errors.values()):

                messages.error(request,error)
                return redirect(update_profile)
            



    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)

    context={'user_form':user_form,'profile_form':profile_form}
    return render(request,'recipes/update_profile.html',context)





@login_required(login_url='user_login')
def change_user_password(request):

    if request.method == "POST":

        user = User.objects.get(id=request.user.id)

        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if user.check_password(old_password):


            if new_password1 != new_password2:
                messages.error(request,"The Two Password fileds didn't matched")
                return redirect('change_user_password')
    


            
            else:

                regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
                pat = re.compile(regex)
                mat = re.search(pat, new_password1)
                if not mat:
                    messages.error(request,f'Invalid password')
                    return redirect('change_user_password')
                
                else:

                    user.set_password(new_password1)
                    update_session_auth_hash(request, user)
                    user.save()
                    messages.success(request,"Your Password has been changed")
                    return redirect('show_profile',user.pk)





        else:
            messages.error(request,"Your old password is wrong")
            return redirect('change_user_password')


    context={}
    return render(request,'recipes/change_password.html',context)




    
@login_required(login_url='user_login')
def add_recipe(request):

    if request.method == "POST":

        form = AddFoodRecipeForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request,f'You have been added new recipe:{data.name}')
            return redirect('show_recipe',data.pk)

        else:

            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('add_recipe')


    else:

        form = AddFoodRecipeForm()


    context={'form':form,'add':"add"}
    return render(request,'recipes/add_recipe.html',context)



@login_required(login_url='user_login')
def add_category(request):

    if request.user.is_superuser:

        if request.method == "POST":

            form = AddFoodCategoryForm(request.POST,request.FILES)

            if form.is_valid():

                form.save()
                messages.success(request,f'You have been added new category: {form.instance.name}')
                return redirect('add_category')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('add_category')
        else:
            form = AddFoodCategoryForm()       

        context={'form':form,'add':'add'}
        return render(request,'recipes/add_category.html',context)
    else:
        messages.error(request,'only the side administrator has permission to add new category')
        return redirect('home')
    


@login_required(login_url='user_login')
def update_category(request,pk):

    if request.user.is_superuser:

        category = get_object_or_404(Food_Category,pk=pk)

        if request.method == "POST":

            form = AddFoodCategoryForm(request.POST,request.FILES,instance=category)

            if form.is_valid():
                form.save()
                messages.success(request,f'You have been modified the category: {form.instance.name}')
                return redirect('update_category',category.pk)
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('add_category')
        else:
            form = AddFoodCategoryForm(instance=category)       

        context={'form':form,'update':'update'}
        return render(request,'recipes/add_category.html',context)
    
    else:
        messages.error(request,'only the side administrator has permission to add new category')
        return redirect('home')


    


@login_required(login_url='user_login')
def delete_category(request,pk):

    category = get_object_or_404(Food_Category,id=pk)

    if  request.user.is_superuser:

        if request.method == "POST":
            category.delete()
            messages.success(request,f'You deleted this category: {category.name}')
            return redirect('all_category')
    else:
        return redirect('all_category')

 

    

@login_required(login_url='user_login')
def update_recipe(request,pk):
     
    recipe = get_object_or_404(Food_Recipe,pk=pk)

    if recipe.user.pk != request.user.pk:
        return redirect('show_recipe',pk)
     

    if request.method == "POST":

        form = AddFoodRecipeForm(request.POST,request.FILES,instance=recipe)

        if form.is_valid():

            data = form.save()           
            messages.success(request,f'You have been modified {data.name}')
            return redirect('update_recipe', data.pk)

        else:

            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('update_recipe', data.pk)


    else:
        form = AddFoodRecipeForm(instance=recipe)


    context={'form':form,'modify':'modify'}
    return render(request,'recipes/add_recipe.html',context)


def show_category(request,pk):


    category = get_object_or_404(Food_Category,pk=pk)
    recipes = Food_Recipe.objects.filter(food_category=category)
   

    context={'category':category,'recipes':recipes}
    return render(request,'recipes/show_category.html',context)



def show_recipe(request,pk):

    recipe = get_object_or_404(Food_Recipe,pk=pk)

    context={'recipe':recipe}

    return render(request,'recipes/show_recipe.html',context)




@login_required(login_url='user_login')
def delete_recipe(request,pk):

    recipe = get_object_or_404(Food_Recipe,id=pk)

    if (request.user.pk == recipe.user.pk) or request.user.is_superuser:

        if request.method == "POST":
            recipe.delete()
            messages.success(request,f'You deleted the recipe: {recipe.name}')
            return redirect('show_profile',request.user.pk)
    else:
        return redirect('show_profile',request.user.pk)




@login_required(login_url='user_login')
def send_like(request,pk):

    recipe = get_object_or_404(Food_Recipe,id=pk)

    if recipe.like.filter(id = request.user.id):
        recipe.like.remove(request.user)
        messages.error(request,f'You have unliked the recipe {recipe.name}')
    else:
        recipe.like.add(request.user)
        messages.success(request,f'You have liked the recipe {recipe.name}')

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='user_login')
def comment_like(request,pk):

    comment = get_object_or_404(Comments,id=pk)

    if comment.likes.filter(id = request.user.id ):

        comment.likes.remove(request.user)
        messages.error(request,f'You  unliked the comment')

    else:

        comment.likes.add(request.user)
        messages.success(request,f'You liked the comment')

    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='user_login')

def send_comment(request,pk):

    food_recipe = get_object_or_404(Food_Recipe,id=pk)

    all_comments = Comments.objects.filter(food_recipe=food_recipe).order_by('-date_added')

    p = Paginator(all_comments,6)
    page = request.GET.get('page')
    comments = p.get_page(page)

   

    if request.method == "POST":

        comment = request.POST.get('comment')
        
        
        p = Paginator(Comments.objects.filter(food_recipe=food_recipe).order_by('-date_added'),6)
        page = request.GET.get('page')
        comments = p.get_page(page)
        

        if comment:


            comment_post, created =  Comments.objects.get_or_create(comment=comment,user=request.user,food_recipe=food_recipe)
            messages.success(request,'You posted new comment')
            return redirect('send_comment',pk)



    context = {'comments':comments,'food_recipe':food_recipe,'all_comments':all_comments}
    return render(request,'recipes/send_comment.html',context)



@login_required(login_url='user_login')
def delete_comment(request,pk):

    comment = get_object_or_404(Comments,id=pk)

    if (request.user.pk == comment.user.pk) or request.user.is_superuser:

        if request.method == "POST":

            comment.delete()
            messages.success(request,'You deleted your comment')
            return redirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='user_login')
def modify_comment(request,pk):

    comment = get_object_or_404(Comments,id=pk)

    if request.method == "POST":

        if (comment.user.pk == request.user.pk):

            updated_message = request.POST['updated_message']
        
            if updated_message:

                comment.comment = updated_message
                comment.save()
                messages.success(request,'You successfully modified your comment')
       

    return redirect(request.META.get('HTTP_REFERER'))



           
    











@login_required(login_url='user_login')
def account_status(request,pk):


    account = get_object_or_404(User, pk=pk)


    if  request.user.is_superuser:
        
        if request.method == "POST":
            if account.is_active == True:
             account.is_active = False
             account.save()
             messages.success(request,f'you successfully deactivated the account: {account.username}')

            else: 
                account.is_active = True
                account.save()
                messages.success(request,f'you successfully activated the account: {account.username}')
               
    return redirect('show_all_profiles')
    
