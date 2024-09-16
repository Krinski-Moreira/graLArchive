from django.shortcuts import render
from .models import Lens, LensComponent
from django.views import generic
from .forms import CreatefieldsForm
import csv
from django.http import HttpResponse


# Create your views here.

def create_table(fields):
    table = [fields]
    components = LensComponent.objects.values()

    for component in components:
        line = []
        lens = Lens.objects.filter(id = component['Name_id']).values()
        #print(component, lens, type(lens))
        for k, v in lens[0].items():
            #print(k, v)
            if(k in fields):
                line.append(v)
        for k, v in component.items():
            #print(k, v)
            if(k in fields):
                line.append(v)
        table.append(line)

    return table

def index(request):
    """View function for home page of site."""
    num_lenses = Lens.objects.all().count()
    num_gaia = Lens.objects.filter(GraL="TRUE").count()

    context = {
        'num_lenses' : num_lenses,
        'num_gaia' : num_gaia,
    }

    return render(request, 'index.html', context=context)
    
def lens(request):
    #components = LensComponent.objects.values()
    #lenses = Lens.objects.values()
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = lensfields[2:] + compfields[2:]
    savedfields = request.session.get('sfields', fields)
    form = CreatefieldsForm()
    options = []
    for i in range(len(fields)):
        options.append((i,fields[i]))

    form_values = request.GET.getlist('fieldsform')
    request.session['sfields'] = form_values
    savedfields = form_values
    print(form_values)

    table = create_table(form_values)

    context = {
        'table' : table,
        "form": form,
        "options": options,
        "savedfields": savedfields
    }

    return render(request, 'catalog/lens_list.html', context=context)

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="database.csv"'},
    )

    writer = csv.writer(response)
    savedfields = request.session.get('sfields')
    table = create_table(savedfields)
    for row in table:
        writer.writerow(row)

    return response