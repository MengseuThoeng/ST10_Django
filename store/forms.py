from django import forms
from .models import UserProfile

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['user']
        if self.instance.pk is None:  # Only on create, not update
            if UserProfile.objects.filter(user=user).exists():
                raise forms.ValidationError('A profile already exists for this user.')
        return user
