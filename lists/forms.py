from django import forms
from lists.models import Item

EMPTY_ERROR_MSG = 'You can\'t add an empty item'
DUPLICATE_ITEM_ERROR_MSG = 'You already added that list item'


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


class ExistingItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR_MSG]}
            self._update_errors(e)
