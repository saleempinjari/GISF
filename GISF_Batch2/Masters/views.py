from django.shortcuts import render
from Masters.forms import ProductsMasterForm,ProductRiskForm
from django.contrib.auth.decorators import login_required
from Masters.models import XxgenProductRiskMaster
from django.forms import modelformset_factory
# Create your views here.


@login_required(login_url='/MyAdmin/clogin/')
def ProductsMaster(request):
    Pform = ProductsMasterForm(request.POST or None)
    if Pform.is_valid():
        form = Pform.save(commit=False)
        form.created_by = str(request.user)
        form.last_updated_by = str(request.user)
        form.save()
        Pform = ProductsMasterForm()
    context = {'Pform': Pform}
    return render(request, 'Masters/ProductMaster.html', context)

def ProductRisk(request):
    cformset = modelformset_factory(XxgenProductRiskMaster, form=ProductRiskForm, extra=4)
    formset = cformset(request.POST or None)

    if request.method == 'GET':
        search_id = request.GET.get('Sid')
        if request.GET.get('Sid') != "None" :
            try:
                formset = cformset(request.POST or None,
                                   queryset=XxgenProductRiskMaster.objects.filter(prod_code=search_id)
                                   )
            except XxgenProductRiskMaster.DoesNotExist:
                formset = cformset(queryset=XxgenProductRiskMaster.objects.none())

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset.forms:
                if form['risk_code'].value() != '':
                    for name, field in form.fields.items():
                        tmpform = form.save(commit=False)
                        setattr(tmpform, 'created_by', str(request.user))
                        setattr(tmpform, 'last_updated_by', str(request.user))
                        tmpform.save()
            formset = cformset(queryset=XxgenProductRiskMaster.objects.none())

    context = {'formset':formset}
    return render(request, 'Masters/ProdRiskDetails.html', context)