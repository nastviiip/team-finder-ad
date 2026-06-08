import random

from django import forms
from django.contrib.auth import get_user_model

from team_finder.utils import validate_github_url

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        user.phone = f"+7{random.randint(1000000000, 9999999999)}"

        if commit:
            user.save()
        return user


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Проверка формата
        if not (phone.startswith("8") or phone.startswith("+7")):
            raise forms.ValidationError("Телефон должен начинаться с 8 или +7")

        if phone.startswith("8"):
            phone = "+7" + phone[1:]

        if len(phone) != 12:  # +7 и 10 цифр = 12 символов
            raise forms.ValidationError("Неверная длина номера телефона")

        if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("Пользователь с таким номером уже существует")

        return phone

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))
