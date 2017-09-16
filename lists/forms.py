from django import forms
from lists.models import Item

EMPTY_ERROR_MSG = 'You can\'t add an empty item'

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ERROR_MSG}
        }

    def save(self, for_list):
        self.instance.list = for_list
        super().save()
