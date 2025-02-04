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


# Create your views here.

def create_table_pd(fields, filter= None):
    #print(fields)
    start_time = timezone.now()
    lensfields = [f.name for f in Lens._meta.get_fields() if f.name in fields]
    compfields = [f.name for f in LensComponent._meta.get_fields() if f.name in fields]
    lensfields.append("id")
    compfields.append("Name_id")
    lens_data = Lens.objects.values(*lensfields)  # Get all Lens data as a QuerySet of dictionaries

    # Step 2: Load the data into Pandas DataFrames
    lens_df = pd.DataFrame(list(lens_data))  # Convert to DataFrame

    # Step 3: Merge the two DataFrames on Lens ID and Name_id in LensComponent
    if(compfields == ['Name', 'Name_id']):
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
    print("before: ", filter)
    if(filter != None):
        print("filter: ", filter)
        if(filter == "doubles"):
            print("Doubles!")
            final_table = final_table[final_table["Type"] == "Double"]
        elif(filter == "quads"):
            print("Quads!")
            final_table = final_table[final_table["Type"] == "Quad"]

    # Step 5: Convert the final DataFrame back to a list (optional, if needed)
    final_table_list = final_table.values.tolist()
    #final_table_json = final_table.to_json()
    #print(final_table_json)
    del final_table
    final_table_list.insert(0, fields)
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print("duração create_table_pd:", elapsed_time.total_seconds())
    

    return final_table_list

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
    num_gaia = Lens.objects.filter(GraL="TRUE").count()
    num_quad = Lens.objects.filter(Type="Quad").count()
    num_double = Lens.objects.filter(Type="Double").count()

    context = {
        'date' : date,
        'num_lenses' : num_lenses,
        'num_gaia' : num_gaia,
        'num_quad' : num_quad,
        'num_double' : num_double
    }

    return render(request, 'index.html', context=context)

def help(request):
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    fields = lensfields[2:] + compfields[2:]

    context = {
        'fields' : fields,
    }
    return render(request, 'catalog/help.html', context = context)
    
def lens(request):
    start_time = timezone.now()
    print(gc.get_stats())
    if(not(gc.isenabled())):
        gc.enable()
    #components = LensComponent.objects.values()
    #lenses = Lens.objects.values()
    defaultlist = ["Name", "RA_mean", "DEC_mean", "Type", "Author", "BibCode", "Max_separation", "z_source", "z_lens", "z_bibcode"]
    request.session['defaultfields'] = defaultlist
    lensfields = [f.name for f in Lens._meta.get_fields()]
    #compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = lensfields[2:]# + compfields[2:]
    #savedfields = request.session.get('sfields', fields)
    
    typefilterform = CreatetypefilterForm()
    typefilterform_values = request.GET.getlist('typefilterform')
    print(typefilterform_values)

    defaultform = CreatedefaultForm()
    defaultform_values = request.GET.getlist('defaultform')
    print(defaultform_values)

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
        table = create_table_pd(savedfields)
    else:
        print("where??", typefilterform_values[0])
        table = create_table_pd(savedfields, typefilterform_values[0])

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
            "savedfields": savedfields
        }
        print(defaultform_values)
        return render(request, 'catalog/table_partial.html', context=context)

    defaultform_values = ["default"]
    print(defaultform_values)
    context = {
        'table' : table,
        "defaultform": defaultform,
        "defaultselected": defaultform_values,
        "form": form,
        "options": options,
        "savedfields": savedfields,
        "defaultfields": defaultlist
    }
    return render(request, 'catalog/lens_list.html', context=context)

def components(request):
    start_time = timezone.now()
    print(gc.get_stats())
    if(not(gc.isenabled())):
        gc.enable()
    #components = LensComponent.objects.values()
    #lenses = Lens.objects.values()
    defaultlistcomp = ["Name", "Component","RA_best", "DEC_best","RA_sexa", "DEC_sexa", "Type", "Author", "BibCode", "Max_separation", "z_source", "z_lens", "z_bibcode"]
    request.session['defaultfieldscomp'] = defaultlistcomp
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = [lensfields[2]] + compfields[2:6] + lensfields[3:] + compfields[7:]
    #savedfields = request.session.get('sfields', fields)
    
    typefilterform = CreatetypefilterForm()
    typefilterform_values = request.GET.getlist('typefilterform')
    print("nandedayoo: ",typefilterform_values)

    defaultform = CreatedefaultForm()
    defaultform_values = request.GET.getlist('defaultform')
    print("defaultform_values")
    print(defaultform_values)

    form = CreatefieldsForm()
    options = []
    for i in range(len(fields)):
        options.append((i,fields[i], fields[i]+"popup"))

    form_values = request.GET.getlist('fieldsformcomp')
    request.session['sfields'] = form_values
    savedfields = form_values
    print(savedfields, form_values)
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
        print("whyy??", typefilterform_values)
        table = create_table_pd(savedfields)
    else:
        print("where??", typefilterform_values[0])
        table = create_table_pd(savedfields, typefilterform_values[0])

    gc.collect()
    #QuerySet.explain()
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print("duração lens:", elapsed_time.total_seconds())
    if(request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('x-requested-with') == 'XMLHttpRequest2'):
        render_start_time = timezone.now()
        print("duração lens function:", (render_start_time - start_time).total_seconds())
        print("aaaaa: ", savedfields)
        context = {
            'table' : table,
            "defaultselected": defaultform_values,
            "savedfields": savedfields
        }
        print(defaultform_values)
        return render(request, 'catalog/table_partial.html', context=context)

    defaultform_values = ["default"]
    print(defaultform_values)
    context = {
        'table' : table,
        "defaultform": defaultform,
        "defaultselected": defaultform_values,
        "form": form,
        "options": options,
        "savedfields": savedfields,
        "defaultfieldscomp": defaultlistcomp
    }
    print("aaaabbbb: ", savedfields)
    return render(request, 'catalog/components.html', context=context)

def download(request):
    date = opendate()
    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = lensfields[2:]
    compfields = [lensfields[2]] + compfields[2:6] + lensfields[3:] + compfields[7:]
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
    savedfields = request.GET.getlist('fieldsformcomp')
    print("Selected fields:", savedfields)
    #print("test", savedfields)
    if not savedfields:
        defaultlist = request.session.get('defaultfieldscomp')
        savedfields = defaultlist
        print("why, ", defaultlist)
    table = create_table_pd(savedfields)
    for row in table:
        writer.writerow(row)

    return response

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    date = opendate()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="graldatabase_system_version-{date}.csv"'},
    )

    writer = csv.writer(response)
    savedfields = request.GET.getlist('fieldsform')
    print("Selected fields:", savedfields)
    if not savedfields:
        defaultlist = request.session.get('defaultfields')
        savedfields = defaultlist
    table = create_table_pd(savedfields)
    for row in table:
        writer.writerow(row)

    return response