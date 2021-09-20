import csv
from datetime import datetime
from io import StringIO

import petl
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render

from .models import CSVFiles


def get_CSV_file_list(request):
    """
    View for listing of all CSV files stored in the db
    """
    csv_files = CSVFiles.objects.all()
    return render(request, 'file_list.html', {'csv_files': csv_files})


def _fetch_data_from_URL(fetch_url):
    """
    Helper function for getting data from the API
    :param fetch_url: URL to connect to
    :return: fetched data
    """
    headers = {
        'Accept': 'application/json'
    }
    req = requests.get(fetch_url,
                       timeout=settings.SWAPI_API_TIMEOUT,
                       headers=headers)
    req.raise_for_status()
    return req.json()


def fetch_people_list(request):
    """
    View for getting actual people data from the API
    """
    people = []
    planets = dict()

    # prefetch planet data
    fetch_url = settings.SWAPI_API_URL + 'planets/'
    while fetch_url:
        fetched_data = _fetch_data_from_URL(fetch_url)
        fetch_url = fetched_data['next']
        for planet in fetched_data['results']:
            planets[planet['url']] = planet['name']

    # fetch people data
    fetch_url = settings.SWAPI_API_URL + 'people/'
    while fetch_url:
        fetched_data = _fetch_data_from_URL(fetch_url)
        fetch_url = fetched_data['next']
        for person in fetched_data['results']:
            people += [{
                'name': person['name'],
                'height': person['height'],
                'mass': person['mass'],
                'hair_color': person['hair_color'],
                'skin_color': person['skin_color'],
                'eye_color': person['eye_color'],
                'birth_year': person['birth_year'],
                'gender': person['gender'],
                'homeworld': planets[person['homeworld']],
                #  'date': person['edited'].split('T')[0],
                'date': datetime.strptime(person['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')
                .strftime('%Y-%m-%d'),
            }]
    if people:
        # create csv file
        # TODO: could be done with petl
        csv_buffer = StringIO()
        fieldnames = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color',
                      'birth_year', 'gender', 'homeworld', 'date']
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(people)
        csv_file = CSVFiles()
        date = datetime.now()
        csv_file.date = date
        csv_file.file.save(str(date)+'.csv', ContentFile(csv_buffer.getvalue().encode('utf-8')))
    return redirect('get_CSV_file_list')


def get_CSV_details(request, csv_id):
    """
    View for listing all persons and their syntetic data from a given CSV file
    :param csv_id: id of the CSVFile stored in the database
    """
    # TODO: id should be encrypted

    csv_file = get_object_or_404(CSVFiles, id=csv_id)

    data = petl.fromcsv(csv_file.file)
    filter_fields = header = petl.header(data)

    limit = int(request.GET.get('limit', 10))
    group_by = set(request.GET.keys()).intersection(set(filter_fields))
    if group_by:
        aggregation = {'Count': len}
        if len(group_by) == 1:
            #  TODO: this has to be done better. An issue with petl?
            data = petl.aggregate(data, list(group_by)[0], aggregation=aggregation)
        else:
            data = petl.aggregate(data, list(group_by), aggregation=aggregation)
        header = petl.header(data)

    if data.len() > limit:
        next_url = '&'.join(list(group_by)+[f'limit={limit+10}'])
    else:
        next_url = None
    url_params = list(group_by)+[f'limit={limit}']

    return render(request, 'details.html', {
        'csv_id': csv_id,
        'data': data.data().list()[:limit],
        'header': header,
        'filter_fields': filter_fields,
        'next_url': next_url,
        'url_get_params': url_params   # TODO: use urllib
    })
