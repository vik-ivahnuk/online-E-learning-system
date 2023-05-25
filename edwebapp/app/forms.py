from django.forms import *
from .models import *
from django.core.exceptions import ValidationError


class SignInForm(Form):
    username = CharField(
        label='username',
        max_length=50,
        widget=TextInput(attrs={
            'class': 'line-input',
            'placeholder': 'Username'
        })
    )

    password = CharField(
        label='password',
        max_length=50,
        widget=PasswordInput(attrs={
            'class': 'line-input',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username:
            raise ValidationError("Поле username не може бути порожнім.")
        if not password:
            raise ValidationError("Поле password не може бути порожнім.")

        return cleaned_data


# class SignUpForm(ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password'
#         ]
#         widgets = {
#             'username': TextInput(attrs={
#                 'class': 'line-input',
#                 'placeholder': 'Username'
#             }),
#             'email': EmailInput(attrs={
#                 'class': 'line-input',
#                 'placeholder': 'Email'
#             }),
#             'first_name': TextInput(attrs={
#                 'class': 'line-input',
#                 'placeholder': 'First name'
#             }),
#             'last_name': TextInput(attrs={
#                 'class': 'line-input',
#                 'placeholder': 'Last name'
#             }),
#             'password': PasswordInput(attrs={
#                 'class': 'line-input',
#                 'placeholder': 'Password'
#             })
#         }
#
#         error_messages = {
#             'username': {
#                 'unique': "Цей username вже використовується"
#             },
#             'email': {
#                 'unique': "Цей email вже використовується"
#             }
#         }
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         users = User.objects.filter(username=username)
#         if users.exists():
#             raise ValidationError(self.fields['username'].error_messages['unique'], code='unique')
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         users = User.objects.filter(email=email)
#         if users.exists():
#             raise ValidationError(self.fields['email'].error_messages['unique'], code='unique')
#         return email
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()


class SignUpForm(Form):
    username = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'line-input',
            'placeholder': 'Username'
        })
    )
    email = EmailField(
        max_length=60,
        widget=EmailInput(attrs={
            'class': 'line-input',
            'placeholder': 'Email'
        })
    )
    first_name = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'line-input',
            'placeholder': 'First name'
        })
    )
    last_name = CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'line-input',
            'placeholder': 'Last name'
        })
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'class': 'line-input',
            'placeholder': 'Password'
        })
    )
    password_confirmation = CharField(
        label='Password Confirmation',
        widget=PasswordInput(attrs={
            'class': 'line-input',
            'placeholder': 'Confirm Password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        users = User.objects.filter(username=username)
        if users.exists():
            raise ValidationError("Цей username вже використовується")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            raise ValidationError("Цей email вже використовується")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Паролі не співпадають")

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.save()


class CourseForm(Form):
    name = CharField(
        label='ведіть назву',
        max_length=50,
        widget=TextInput(attrs={
            'class': 'form-control rounded-3',
            'id': 'id_name',
            'placeholder': 'Назва'
        })
    )
    description = CharField(
        label='Введіть опис',
        max_length=200,
        widget=TextInput(attrs={
            'class': 'form-control rounded-3',
            'id': 'id_description',
            'placeholder': 'Опис курсу'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if not name:
            raise ValidationError("Поле 'назва' не може бути порожнім.")
        if not description:
            raise ValidationError("Поле 'опис' не може бути порожнім.")

        return cleaned_data


class TestForm(Form):
    name = CharField(
        label='ведіть назву',
        max_length=50,
        widget=TextInput(attrs={
            'class': 'form-control me-2',
            'placeholder': 'Уведіть назву нового тесту'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if not name:
            raise ValidationError("Поле 'назва' не може бути порожнім.")
        return cleaned_data


class AddCourseForm(Form):
    code = CharField(label='Код курсу', max_length=8, widget=TextInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Уведіть код курсу',
        'rows': 2
    }))

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        if not code:
            raise ValidationError("Поле 'код курсу' не може бути порожнім.")
        return cleaned_data


class Test(Form):
    name = CharField(label='Назва тесту', max_length=255, widget=TextInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Уведіть назву тесту'
    }))

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if not name:
            raise ValidationError("Поле 'код тесту' не може бути порожнім.")
        return cleaned_data


class AnswerForm(Form):
    answer_text = CharField(max_length=255, required=True, widget=Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введіть варіант відповіді',
            'rows': 1
        })
                            )
    is_correct = BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        answer_text = cleaned_data.get("answer_text")
        if not answer_text:
            raise ValidationError("Варіант відповіді не може бути порожнім.")
        return cleaned_data


AnswerFormSet = formset_factory(AnswerForm, extra=1)


class QuestionForm(Form):
    question_text = CharField(max_length=255,
                              required=True,
                              widget=Textarea(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Уведіть питання',
                                      'rows': 1
                                  })
                              )
    hidden_input = CharField(widget=HiddenInput(), required=False)
    answers = AnswerFormSet(prefix='answer')


class TestStudentForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super(TestStudentForm, self).__init__(*args, **kwargs)

        for question in questions:
            choices = [(option.id, option.text) for option in question.answer_set.all()]

            if question.photo:
                self.fields[str(question.id) + '-photo'] = CharField(
                    widget=HiddenInput(attrs={'value': question.photo.url}),
                    initial=question.photo.url,
                    required=False
                )
                print(question.photo.url)

            self.fields[str(question.id)] = MultipleChoiceField(
                label=question.question,
                widget=CheckboxSelectMultiple,
                choices=choices,
                required=False
            )


class DateTimeForm(forms.Form):
    deadline = DateTimeField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'id': 'datetimepicker',
                'placeholder': 'Виберіть дату та час'
            }
        )
    )
