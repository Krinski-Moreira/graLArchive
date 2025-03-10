from django.shortcuts import render
from .models import Lens, LensComponent
from django.views import generic
from .forms import CreatefieldsForm, CreatedefaultForm, CreatetypefilterForm
import csv
from django.http import HttpResponse
import pandas as pd
from django.http import JsonResponse
from django.db import reset_queries
import gc
from django.utils import timezone
from django.template import loader
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from django.contrib.staticfiles import finders

from django.views import generic

import json

from django.shortcuts import get_object_or_404
from django.utils.text import slugify


# Create your views here.

class lensDetailView(generic.DetailView):
    model = Lens

    def get_object(self):
        slug = self.kwargs.get("slug")
        print(slug)
        return get_object_or_404(Lens, Name__in=[lens.Name for lens in Lens.objects.all() if slugify(lens.Name) == slug])
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        lensfields = [f.name for f in Lens._meta.get_fields()]
        compfields = [f.name for f in LensComponent._meta.get_fields()]
        context["fieldnames"] = lensfields[2:]
        fields = lensfields[2:] + compfields[2:]
        name = context['lens']
        fields1 = ["Name","RA_center_sexa", "DEC_center_sexa", "Type", "BibCode", "Max_separation", "z_source", "z_lens", "z_bibcode"]
        table1, lens_id = create_table_pd(fields1,name=name)
        fields2 = ["Name","Component","RA_best", "DEC_best","RA_sexa", "DEC_sexa"]
        table2, lens_id = create_table_pd(fields2,name=name)
        context["lens_id"] = lens_id
        context['table1'] = table1
        context['table2'] = table2
        help_row = help_texts(fields)
        context['help_row'] = help_row
        return context

def round_table_floats(value):
    
    return('{:.3f}'.format(value))

def create_table_pd(fields, filter= None, name = False):
    #print(fields)
    start_time = timezone.now()
    lensfields = [f.name for f in Lens._meta.get_fields() if f.name in fields]
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields() if f.name in fields]
    lensfields.append("id")
    compfields.append("Name_id")
    if("lenscomponent" in lensfields):
        lensfields.remove("lenscomponent")
    lens_data = Lens.objects.values(*lensfields)  # Get all Lens data as a QuerySet of dictionaries
    # Step 2: Load the data into Pandas DataFrames
    lens_df = pd.DataFrame(list(lens_data))  # Convert to DataFrame
    # Step 3: Merge the two DataFrames on Lens ID and Name_id in LensComponent
    if(compfields == ['Name', 'Name_id'] or compfields == ['Name_id']):
        merged_df = lens_df
    else:
        component_data = LensComponent.objects.values(*compfields)  # Get all LensComponent data
        component_df = pd.DataFrame(list(component_data))  # Convert to DataFrame
        if('Name' in fields):
            del component_df['Name']
        merged_df = pd.merge(lens_df, component_df, left_on='id', right_on='Name_id', suffixes=(None, None))
        del component_df

    reset_queries()

    # Step 4: Filter the fields (columns) you want to include in the final table
    final_table = merged_df[fields]
    del lens_df
    del merged_df
    final_table = final_table.fillna('')
    if(filter != None):
        if(filter == "doubles"):
            final_table = final_table[final_table["Type"] == "Double"]
        elif(filter == "quads"):
            final_table = final_table[final_table["Type"] == "Quad"]
    name_list = final_table["Name"].to_list()
    slug_list = [slugify(x) for x in name_list]


    if("Max_separation" in fields):
        final_table["Max_separation"] = final_table["Max_separation"].map(round_table_floats)
    
    if(name != False):
        final_table = final_table[final_table["Name"] == str(name)]
        final_table = final_table.drop('Name', axis=1)
        fields.remove("Name")
        

    # Convert the final DataFrame back to a list

    final_table_list = final_table.values.tolist()
    #final_table_json = final_table.to_json()
    del final_table
    final_table_list.insert(0, fields)
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print("duração create_table_pd:", elapsed_time.total_seconds())
    

    return final_table_list, slug_list

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

def opendate():
    resultfile = finders.find('date.txt')
    with open(resultfile) as datefile:
        date = datefile.readline()
    return date

def index(request):
    """View function for home page of site."""

    date = opendate()

    num_lenses = Lens.objects.all().count()
    num_quad = Lens.objects.filter(Type="Quad").count()
    num_double = Lens.objects.filter(Type="Double").count()

    context = {
        'date' : date,
        'num_lenses' : num_lenses,
        'num_quad' : num_quad,
        'num_double' : num_double
    }

    return render(request, 'index.html', context=context)

def help(request):
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    fields = lensfields[2:] + compfields[2:]
    help_row = help_texts(fields)

    context = {
        'fields' : fields,
        'help_row' : help_row
    }
    return render(request, 'catalog/help.html', context = context)
    
def lenses(request):
    start_time = timezone.now()
    print(gc.get_stats())
    if(not(gc.isenabled())):
        gc.enable()
    #components = LensComponent.objects.values()
    #lenses = Lens.objects.values()
    defaultlist = ["Name", "RA_center", "DEC_center","RA_center_sexa", "DEC_center_sexa", "Type", "BibCode", "Max_separation", "z_source", "z_lens", "z_bibcode"]
    request.session['defaultfields'] = defaultlist
    lensfields = [f.name for f in Lens._meta.get_fields()]
    #compfields = [f.name for f in LensComponent._meta.get_fields()]
    fields = lensfields[2:]# + compfields[2:]
    #savedfields = request.session.get('sfields', fields)
    
    typefilterform = CreatetypefilterForm()
    typefilterform_values = request.GET.getlist('typefilterform')


    defaultform = CreatedefaultForm()
    defaultform_values = request.GET.getlist('defaultform')

    form = CreatefieldsForm()
    options = []
    for i in range(len(fields)):
        options.append((i,fields[i], fields[i]+"popup"))

    form_values = request.GET.getlist('fieldsform')
    request.session['sfields'] = form_values
    savedfields = form_values
    if len(savedfields) == 0:
        savedfields = defaultlist
        #defaultform_values = ["default"]

    if(request.headers.get('x-requested-with') == 'XMLHttpRequest2'):
        if(defaultform_values[0] == "default"):
            savedfields = defaultlist
        elif(defaultform_values[0] == "all"):
            savedfields = fields
    else:   
        if(set(savedfields) == set(defaultlist)):
            defaultform_values = ["default"]
        elif(set(savedfields) == set(fields)):
            defaultform_values = ["all"]
        else:
            defaultform_values = []

    if not typefilterform_values:
        table, lens_id = create_table_pd(savedfields)
    else:
        table, lens_id = create_table_pd(savedfields, typefilterform_values[0])


    help_row = help_texts(fields)

    gc.collect()
    #QuerySet.explain()
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print("duração lens:", elapsed_time.total_seconds())
    if(request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('x-requested-with') == 'XMLHttpRequest2'):
        render_start_time = timezone.now()
        print("duração lens function:", (render_start_time - start_time).total_seconds())
        context = {
            'table' : table,
            "defaultselected": defaultform_values,
            "savedfields": savedfields,
            "lens_id": lens_id,
            "help_row": help_row
        }
        print(defaultform_values)
        return render(request, 'catalog/table_partial.html', context=context)

    defaultform_values = ["default"]
    context = {
        'table' : table,
        "defaultform": defaultform,
        "defaultselected": defaultform_values,
        "form": form,
        "options": options,
        "savedfields": savedfields,
        "defaultfields": defaultlist,
        "lens_id": lens_id,
        "help_row": help_row
    }
    return render(request, 'catalog/lens_list.html', context=context)

def components(request):
    start_time = timezone.now()
    print(gc.get_stats())
    if(not(gc.isenabled())):
        gc.enable()
    #components = LensComponent.objects.values()
    #lenses = Lens.objects.values()
    defaultlistcomp = ["Name", "Component","RA_best", "DEC_best","RA_sexa", "DEC_sexa", "Type", "BibCode", "Max_separation", "z_source", "z_lens", "z_bibcode"]
    request.session['defaultfields'] = defaultlistcomp
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = [lensfields[2]] + compfields[2:5] + lensfields[3:] + compfields[5:]
    #savedfields = request.session.get('sfields', fields)
    
    typefilterform = CreatetypefilterForm()
    typefilterform_values = request.GET.getlist('typefilterform')

    defaultform = CreatedefaultForm()
    defaultform_values = request.GET.getlist('defaultform')

    help_row = help_texts(fields)

    form = CreatefieldsForm()
    options = []
    for i in range(len(fields)):
        options.append((i,fields[i], fields[i]+"popup"))

    form_values = request.GET.getlist('fieldsform')
    request.session['sfields'] = form_values
    savedfields = form_values
    if len(savedfields) == 0:
        savedfields = defaultlistcomp
        #defaultform_values = ["default"]

    if(request.headers.get('x-requested-with') == 'XMLHttpRequest2'):
        if(defaultform_values[0] == "default"):
            savedfields = defaultlistcomp
        elif(defaultform_values[0] == "all"):
            savedfields = fields
    else:   
        if(set(savedfields) == set(defaultlistcomp)):
            defaultform_values = ["default"]
        elif(set(savedfields) == set(fields)):
            defaultform_values = ["all"]
        else:
            defaultform_values = []

    if not typefilterform_values:
        table, lens_id = create_table_pd(savedfields)
    else:
        table, lens_id = create_table_pd(savedfields, typefilterform_values[0])


    gc.collect()
    #QuerySet.explain()
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print("duração lens:", elapsed_time.total_seconds())
    if(request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('x-requested-with') == 'XMLHttpRequest2'):
        render_start_time = timezone.now()
        print("duração lens function:", (render_start_time - start_time).total_seconds())
        context = {
            'table' : table,
            "defaultselected": defaultform_values,
            "savedfields": savedfields,
            "lens_id": lens_id,
            "help_row": help_row
        }
        return render(request, 'catalog/table_partial.html', context=context)

    defaultform_values = ["default"]
    context = {
        'table' : table,
        "defaultform": defaultform,
        "defaultselected": defaultform_values,
        "form": form,
        "options": options,
        "savedfields": savedfields,
        "defaultfields": defaultlistcomp,
        "lens_id": lens_id,
        "help_row": help_row
    }
    return render(request, 'catalog/components.html', context=context)

def help_texts(fields):
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    help_dict = {}
    for field in fields:
        if(field in lensfields):
            help_text=Lens._meta.get_field(field).help_text
        elif(field in compfields):
            help_text=LensComponent._meta.get_field(field).help_text
        if(help_text == ""):
            help_text = field
        help_dict[field] = help_text
    help_json = json.dumps(help_dict)
    return help_json

def download(request):
    date = opendate()
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = lensfields[2:]
    compfields = [lensfields[2]] + compfields[2:5] + lensfields[3:] + compfields[5:]
    context = {
        'date' : date,
        'lensfields': fields,
        'compfields': compfields
    }
    return render(request, 'catalog/download.html', context= context)

def export_csv_comp(request):
    # Create the HttpResponse object with the appropriate CSV header.
    date = opendate()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="graldatabase__lensedimages_version-{date}.csv"'},
    )

    writer = csv.writer(response)
    typefilterform_values = request.GET.getlist('typefilterform')
    savedfields = request.GET.getlist('fieldsformcomp')
    if not savedfields:
        defaultlist = request.session.get('defaultfields')
        savedfields = defaultlist

    if not typefilterform_values:
        table, id_list = create_table_pd(savedfields)
    else:
        table, id_list = create_table_pd(savedfields, typefilterform_values[0])
    for row in table:
        writer.writerow(row)

    return response

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    date = opendate()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="graldatabase_lenses_version-{date}.csv"'},
    )

    writer = csv.writer(response)
    typefilterform_values = request.GET.getlist('typefilterform')
    savedfields = request.GET.getlist('fieldsform')
    if not savedfields:
        defaultlist = request.session.get('defaultfields')
        savedfields = defaultlist
    
    if not typefilterform_values:
        table, id_list = create_table_pd(savedfields)
    else:
        table, id_list = create_table_pd(savedfields, typefilterform_values[0])
    for row in table:
        writer.writerow(row)

    return response