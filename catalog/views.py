from django.shortcuts import render
from .models import Lens, LensComponent
from django.views import generic

# Create your views here.

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
    test = Lens.objects.values()
    fields = [f.name for f in Lens._meta.get_fields()]
    print(test)
    print(fields)
    table = [fields]
    for lens in test:
        line = []
        print(lens)
        #for f in fields:
        #    print(f)
        for k, v in lens.items():
            print(k, v)
            line.append(v)
        table.append(line)
    print(table)
    context = {
        'table' : table
    }

    return render(request, 'catalog/lens_list.html', context=context)