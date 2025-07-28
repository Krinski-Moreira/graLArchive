csv_filepathname = "/home/otavio/GaiaGraL_database_20250630.csv"
#csv_filepathnameLens="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Lens.csv"
#csv_filepathnameComponents="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Components.csv"
djangoproject_home="/home/otavio/web-projects/graLArchive-main"
td_filepathname = "/home/otavio/time_delays_25032025.csv" #time delay file

import sys,os, django
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='graLArchive.settings'
django.setup()

from catalog.models import Lens, LensComponent

import pandas as pd
from datetime import datetime

Lens.objects.all().delete()

with open(djangoproject_home+'/catalog/static/date.txt', 'w') as filedate:
    now = datetime.today().strftime('%Y-%m-%d')
    filedate.write(now)

df = pd.read_csv(csv_filepathname, na_filter=False, keep_default_na=False)

#data frame of time delays
td_df = pd.read_csv(td_filepathname, na_filter=False, keep_default_na=False)

table_df = df[(df["Confirmed"] != 0) & ((df["Type"] == "Double") | (df["Type"] == "Quad"))]

lensfields = [f.name for f in Lens._meta.get_fields()]
compfields = [f.name for f in LensComponent._meta.get_fields()]
print(lensfields, compfields)
lens_names = table_df['Name'].unique()
#print(lens_names)

td_columns = td_df.columns.tolist()
if("BibCode" in td_columns):
    td_df.rename({"BibCode":"BibCode_TD"}, axis=1, inplace=True)
td_columns = td_df.columns.tolist()
print("test:", td_columns)

columns_csv = table_df.columns.tolist()

for columnName in columns_csv:
    if((columnName in td_columns) and (columnName != "Name")):
        print(columnName)
        td_df.drop(columnName, axis=1, inplace=True)
print(td_df.columns.tolist())

print(table_df)
table_df = pd.merge(table_df, td_df, how="left", on="Name")

columns = table_df.columns.tolist()
print(columns)
print(table_df)

for lens_name in lens_names:
    lens=Lens()
    print(lens_name)
    #save = True
    for lensfield in lensfields:
        if(lensfield == "z_deflector_text"):
            z_list = table_df[table_df["Name"] == lens_name]["z_deflector"].to_list()
            #print(z_list)
            value = ""
            for z in z_list:
                try:
                    float(z)
                    value += str(z) + "/"
                except:
                    value += ""
            if(len(value)>1):
                if(value[-1] == "/"):
                    value = value[:-1]
            #print(value)
            try:
                setattr(lens, lensfield, value)
            except:
                print("Error in setattr", lens, lensfield, value)

        elif(lensfield in columns):
            value = table_df[table_df["Name"] == lens_name][lensfield].to_list()[0]
            if pd.isna(value):  # Check if the value is NaN
                value = ""  # Replace NaN with an empty string
            if(value == ""):
                #save = False
                #print(lens_name, lensfield, value, type(value), table_df[table_df["Name"] == lens_name]["Confirmed"].to_list()[0])
                continue
            try:
                setattr(lens, lensfield, value) 
            except:
                print("Error in setattr", lens, lensfield, value)           
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
            if pd.isna(value):  # Check if the value is NaN
                value = ""  # Replace NaN with an empty string
            if(value == ""):
                #save = False
                #print(lens_name, compfield, value, type(value), table_df[table_df["Name"] == lens_name]["Confirmed"].to_list()[0])
                continue
            try:
                setattr(component, compfield, value)
            except:
                print("Error in setattr", component, compfield, value)
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