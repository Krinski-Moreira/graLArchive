csv_filepathname = "C:/Users/otavio.LAPTOP-D1DO624H/GaiaGraL_database_05082024_DR4.csv"
csv_filepathnameLens="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Lens.csv"
csv_filepathnameComponents="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Components.csv"
your_djangoproject_home="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/graLArchive"

import sys,os, django
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='graLArchive.settings'
django.setup()

from catalog.models import Lens, LensComponent

import pandas as pd


Lens.objects.all().delete()

df = pd.read_csv(csv_filepathname, na_filter=False)

table_df = df[df["Confirmed"] != 0]

columns = table_df.columns.tolist()
lensfields = [f.name for f in Lens._meta.get_fields()]
compfields = [f.name for f in LensComponent._meta.get_fields()]
print(lensfields, compfields)
lens_names = table_df['Name'].unique()
print(lens_names)

for lens_name in lens_names:
    lens=Lens()
    #save = True
    for lensfield in lensfields:
        if(lensfield in columns):
            value = table_df[table_df["Name"] == lens_name][lensfield].to_list()[0]
            if(value == ""):
                #save = False
                print(lens_name, lensfield, value, type(value), table_df[table_df["Name"] == lens_name]["Confirmed"].to_list()[0])
            setattr(lens, lensfield, value)            
    lens.save()
    
    rows_df = table_df[table_df["Name"] == lens_name]
    for index, row in rows_df.iterrows():
        #save = True
        component = LensComponent()
        try:
            lens = Lens.objects.get(Name=lens_name)
            component.Name = lens
        except Lens.DoesNotExist:
            print(f"Lens '{lens_name}' does not exist in the database.")
            continue
        for compfield in compfields[2:]:
            value = row[compfield]
            if(value == ""):
                #save = False
                print(lens_name, compfield, value, type(value), table_df[table_df["Name"] == lens_name]["Confirmed"].to_list()[0])
            setattr(component, compfield, value)
        component.save()

        

            #setattr(lens, lensfield, )
            #print(table_df[lensfield])
print(compfields)

#table_df[table_df[lensfield] == lens_name]
#table_df[lensfield]

print("how often does this script run?")
'''dataReaderLens = csv.reader(open(csv_filepathnameLens), delimiter=',', quotechar='"')

for row in dataReaderLens:
    lens=Lens()
    lens.Name = row[0]
    lens.RA_mean = row[1]
    lens.DEC_mean = row[2]
    lens.Author = row[3]
    lens.BibCode = row[4]
    lens.GraL = row[5]
    lens.Max_separation = row[6]
    lens.save()

dataReaderComponents = csv.reader(open(csv_filepathnameComponents), delimiter=',', quotechar='"')

for row in dataReaderComponents:
    component = LensComponent()
    # Fetch the corresponding Lens object by name
    try:
        lens = Lens.objects.get(Name=row[0])
        component.Name = lens
    except Lens.DoesNotExist:
        print(f"Lens '{row[0]}' does not exist in the database.")
        continue
    component.Component = row[1]
    component.RA_best = row[2]
    component.DEC_best = row[3]
    component.save() '''