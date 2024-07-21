from django import forms
from .models import Profile,User,Food_Category,Food_Recipe,Comments


class UpdateProfileForm(forms.ModelForm):

   

    image = forms.ImageField(label='Avatar')
    profile_bio = forms.CharField(label="Profile Bio",required=False,widget=forms.Textarea(attrs={

     'placeholder':'Profile Bio',
     'class':'form-control'   

    }))
    facebook_link = forms.CharField(label="Facebook link",required=False,widget=forms.TextInput(attrs={

     'placeholder':'Facebook link',
     'class':'form-control'   

    }))
    youtube_chanel = forms.CharField(label="Youtube channel",required=False,widget=forms.TextInput(attrs={

     'placeholder':'Youtube channel',
     'class':'form-control'   

    }))

    class Meta:
        model = Profile
        fields=('image','profile_bio','facebook_link','youtube_chanel')



class UpdateUserForm(forms.ModelForm):


        username = forms.CharField(label='Username',required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter username',
        'class':'form-control'      

        }))

        first_name = forms.CharField(label='First name',required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter your first name',
        'class':'form-control'      

        }))

        last_name = forms.CharField(label='Last name',required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter your last name',
        'class':'form-control'      

        }))

        email = forms.CharField(label='Email',required=True,widget=forms.EmailInput(attrs={
             'placeholder':'Enter email',
             'class':'form-control'
             
        }))

        class Meta:
             model = User

             fields = ('username','first_name','last_name','email')


class AddFoodRecipeForm(forms.ModelForm):

     food_category = forms.ModelChoiceField(queryset=Food_Category.objects.all(),widget=forms.Select(attrs={
          'class':'form-select form-control fw-bolder'
     }),required=True)

     image = forms.ImageField(label='Food Picture',required=False)

     name = forms.CharField(label="food name",required=True,widget=forms.TextInput(attrs={
          'placeholder':'Enter Food name',
          'class':'form-control'
     }))

    

     times = [(i,i) for i in range(10,130,10) ]

     complexity_values = [  

          ('Trivial','Trivial'),
          ('Easy','Easy'),
          ('Advanced','Advanced'),
          ('Complicated','Complicated'),
         
     ]
     

     required_time = forms.ChoiceField(
        
        choices=times,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
        }))
     

     complexity = forms.ChoiceField(
        
        choices=complexity_values,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
        }))




     class Meta:
          model = Food_Recipe

          fields =('food_category','image','required_time','complexity','name','description')


class UpdateCommentForm(forms.ModelForm):

     comment = forms.CharField(widget=forms.TextInput(attrs={

          'class':'form-control'

     }))

     class Meta:
          model = Comments

          fields=('comment',)



class AddFoodCategoryForm(forms.ModelForm):

     image = forms.ImageField(label='Category picture',required=False)

     name = forms.CharField(label='Category name',required=True,widget=forms.TextInput(attrs={
          'placeholder':'Enter Category name',
          'class':'form-control'
     }))

     description = forms.CharField(label="Description",required=True,widget=forms.Textarea(attrs={
          'placeholder':'Enter Description',
          'class':'form-control'
     }))


     class Meta:
          model = Food_Category
          fields=('name','description','image')

 



    


    




