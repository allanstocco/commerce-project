from django.db.models.fields import DateField, DateTimeField, TimeField
from django.forms import forms, ModelForm, widgets, MultiWidget
from .models import *


class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ['title', 'description', 'category',
                  'pictureURL', 'pictureUpload', 'price', 'bid_timer']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control col-sm-4', 'placeholder': 'Item name'}),
            'description': widgets.Textarea(attrs={'class': 'form-control col-sm-6', 'placeholder': 'Write a description'}),
            'pictureURL': widgets.URLInput(attrs={'class': 'form-control col-sm-6', 'placeholder': 'Image URL'}),
            'pictureUpload': widgets.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': widgets.Select(attrs={'class': 'form-control col-sm-4'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control col-sm-1', 'placeholder': '£'}),
            'bid_timer': widgets.DateInput(attrs={'type': 'datetime-local', 'class':'form-control col-sm-3'})
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'pictureURL': 'Copy and Paste the URL of your list',
            'pictureUpload': 'Upload your own list photo',
            'category': 'Category',
            'price': 'Initial Price',
            'bid_timer': 'Set a day so that your auction will get closed automatically'
        }
    
        

class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['field']
        widgets = {
            'field': widgets.Textarea(attrs={'class': 'descp'})
        }
        labels = {
            'field': ''
        }


class BidsForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        widgets = {
            'price': widgets.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'price': ''
        }
