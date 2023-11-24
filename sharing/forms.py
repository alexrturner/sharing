from django import forms

from .models import Message


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['text', 'audio', 'recorded_together']
#         widgets = {
#             'recorded_together': forms.CheckboxInput()
#         }