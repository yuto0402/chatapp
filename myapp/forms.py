from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Friend, TalkRoom
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            self.add_error(None, "The two password fields didn't match.")

        if username.lower() in password1.lower() or password1.lower() in username.lower():
            self.add_error(None, "Password cannot be similar to your name.")

        if len(password1) < 8:
            self.add_error(None, "Password must be at least 8 characters long.")
        
        return cleaned_data
    
class LoginForm(AuthenticationForm):
    error_messages = {
        'inactive':'このユーザーは存在しません。',
        'invalid_login': 'ユーザーとパスワードが一致しません。',
    }

class TalkForm(forms.ModelForm):

    class Meta:
        model = TalkRoom
        fields = ('message',)
        widgets = {
        'message': forms.Textarea(attrs={'rows':1})
        }
    
class ChangeForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        image = cleaned_data.get('image')
        return cleaned_data
