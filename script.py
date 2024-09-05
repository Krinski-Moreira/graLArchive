csv_filepathnameLens="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Lens.csv"
csv_filepathnameComponents="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/Components.csv"
your_djangoproject_home="C:/Users/otavio.LAPTOP-D1DO624H/web-projects/djangosite/graLArchive"

import sys,os, django
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='graLArchive.settings'
django.setup()

from catalog.models import Lens, LensComponent

import csv

Lens.objects.all().delete()

dataReaderLens = csv.reader(open(csv_filepathnameLens), delimiter=',', quotechar='"')

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
    #component.Name = row[0]
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
    component.save()