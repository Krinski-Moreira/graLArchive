from django.shortcuts import render
from .models import Lens, LensComponent

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