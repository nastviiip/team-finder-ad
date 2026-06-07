# users/forms.py
import random
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        # Генерируем временный случайный телефон, чтобы БД не ругалась на уникальность
        # (например: +71234567890). Пользователь изменит его в профиле.
        user.phone = f"+7{random.randint(1000000000, 9999999999)}"
        
        if commit:
            user.save()
        return user


# Добавь это в users/forms.py
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Проверка формата
        if not (phone.startswith("8") or phone.startswith("+7")):
            raise forms.ValidationError("Телефон должен начинаться с 8 или +7")

        # Приведение к одному формату (+7)
        if phone.startswith("8"):
            phone = "+7" + phone[1:]

        if len(phone) != 12:  # +7 и 10 цифр = 12 символов
            raise forms.ValidationError("Неверная длина номера телефона")

        # Проверка на уникальность (исключая текущего юзера)
        if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("Пользователь с таким номером уже существует")

        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на github.com")
        return url
