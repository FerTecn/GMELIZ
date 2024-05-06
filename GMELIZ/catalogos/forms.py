from django import forms
from .models import Categoria, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class ProductoForm(forms.ModelForm):
    # fechaSalida = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False,label='Fecha de Salida (solo si ya salió del ganado)')

    class Meta:
        model = Producto
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen'].widget.attrs.update({'class': 'btn btn-info btn-icon-split'})

