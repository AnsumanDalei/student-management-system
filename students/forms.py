from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'phone',
            'address',
            'age',
            'course',
            'profile_photo',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = name != 'profile_photo'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        students = Student.objects.filter(email__iexact=email)
        if self.instance.pk:
            students = students.exclude(pk=self.instance.pk)
        if students.exists():
            raise forms.ValidationError(
                'A student with this email address already exists.'
            )
        return email
