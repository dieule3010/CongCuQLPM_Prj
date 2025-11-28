from django import forms
from .models import MenuItem, Staff, Customer, Feedback, InventoryItem, Promotion

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
