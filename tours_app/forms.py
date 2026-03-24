from django import forms
from .models import Order
'''
訂單報名表單 (ModelForm)
功能：
1. 自動對應 Order 模型欄位進行資料驗證與儲存。
2. 強制套用 Bootstrap 5 的 'form-control' 樣式。
3. 針對人數 (pax) 進行前後端雙重限制。
'''
class OrderForm(forms.ModelForm):
    pax = forms.IntegerField(
        min_value=1,
        label="報名人數",
        #model 模板生成的input 賦予class = form-control 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )

    class Meta:
        model = Order
        fields = ['contact_name', 'contact_phone', 'contact_email', 'pax']
        widgets = {
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '王小明'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0912-345-678'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
        }
