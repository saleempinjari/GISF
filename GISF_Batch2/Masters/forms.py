from django import forms
import datetime
from Masters.models import XxgenProductMaster,XxgenProductRiskMaster

month = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "may", "6": "June",
             "7": "July", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

class ProductsMasterForm(forms.ModelForm):
    prod_start_date = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.date.today)
    prod_end_date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = XxgenProductMaster
        fields =[
            'prod_code',
            'prod_description',
            'prod_start_date',
            'prod_end_date',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by',
            'last_updated_by']

        labels = {
            'prod_code': 'Product Code',
            'prod_start_date': 'Start Date',
            'prod_end_date': 'End Date',
        }

    def clean_prod_code(self, *args, **kwargs):  # syntax for filed validate is clean_<fildName>
        data = self.cleaned_data['prod_code']
        if not data.isupper():
            raise forms.ValidationError("prod code should be in UpperCase")
        if '@' in data or '*' in data or '|' in data:
            raise forms.ValidationError("prod code should not have special characters. @,*,|")

        if len(data) < 5:
            self._errors['prod_code'] = self.error_class([
                'Minimum 5 characters required'])
        return data

    def clean(self):
        # data from the form is fetched using super function
        super(ProductsMasterForm, self).clean()
        prod_desc = self.cleaned_data.get('prod_description')
        if len(prod_desc) < 10:
            self._errors['prod_description'] = self.error_class([
                'Description Should Contain minimum 10 characters chagnes'])
            # return any errors if found
        return self.cleaned_data

class ProductRiskForm(forms.ModelForm):

    cal_method = (
        ('','---------'),
        ('F', ("Fixed")),
        ('P', ("Percentage"))
    )

    risk_start_date = forms.DateField(widget=forms.SelectDateWidget(months=month),required = False)
    risk_end_date = forms.DateField(widget=forms.SelectDateWidget(months=month),required=False)
    risk_code = forms.CharField(required=True,widget=forms.TextInput(attrs={"size": 10,'style': 'width:150px'}))
    risk_description = forms.CharField(required=True,widget=forms.TextInput(attrs={"size": 10,'style': 'width:100px'}))
    risk_premium_percent = forms.DecimalField(required=False,widget=forms.TextInput(attrs={'style': 'width:100px'}))
    fixed_prem = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    fixed_si = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    prem_calc_method = forms.ChoiceField(choices = cal_method,required = False)
    risk_description = forms.CharField(required=True,widget=forms.TextInput(attrs={"size": 10, 'style': 'width:200px'}))



    class Meta:
        model = XxgenProductRiskMaster
        fields =[
            'prod_code',
            'risk_code',
            'risk_description',
            'risk_premium_percent',
            'risk_start_date',
            'risk_end_date',
            'prem_calc_method',
            'fixed_prem',
            'fixed_si',
            'created_by',
            'last_updated_by',
        ]

        exclude = ['created_by',
                   'last_updated_by']


    def clean_risk_code(self, *args, **kwargs):  # syntax for filed validate is clean_<fildName>
        data = self.cleaned_data['risk_code']
        if not data.isupper():
            raise forms.ValidationError("risk_code code should be in UpperCase")
        if '@' in data or '*' in data or '|' in data:
            raise forms.ValidationError("risk_code should not have special characters. @,*,|")

        if len(data) < 5:
            self._errors['risk_code'] = self.error_class([
                'Minimum 5 characters required'])
        return data

    def clean_risk_premium_percent(self, *args, **kwargs):  # syntax for filed validate is clean_<fildName>
        data = self.cleaned_data['risk_premium_percent']
        if data is None:
            print("is none")
        else:
            if data>100:
                raise forms.ValidationError("Premium Percent shouldnot exceed 100")
        return data

    def clean(self):

        # data from the form is fetched using super function
        super(ProductRiskForm, self).clean()
        risk_desc = self.cleaned_data.get('risk_description')
        calmethod = self.cleaned_data.get('prem_calc_method')

        if calmethod == 'F':
            if self.cleaned_data.get('fixed_prem')==''or self.cleaned_data.get('fixed_prem') is None :
                self._errors['fixed_prem'] = self.error_class([
                    'Fixed Premium should not be null when Prem Cal Method is Fixed '])

            if self.cleaned_data.get('fixed_si') =='' or self.cleaned_data.get('fixed_si') is None:
                self._errors['fixed_si'] = self.error_class([
                    'Fixed SI should not be null when Prem Cal Method is Fixed '])
        elif calmethod == 'P':
            print('percent',self.cleaned_data.get('risk_premium_percent'))
            if  self.cleaned_data.get('risk_premium_percent') is None:
                self._errors['risk_premium_percent'] = self.error_class([
                    'risk_premium_percent should not be null when Prem Cal Method is Percentage'])

        return self.cleaned_data