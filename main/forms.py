from django import forms
from main.models import Video, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class VideoUpload(forms.ModelForm):
	class Meta:
		model = Video
		exclude = ['user','stamp',]
    
class SignUpForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

	class Meta:
		model = CustomUser
		fields = ('email',)

class LoginForm(forms.Form):
	email = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())