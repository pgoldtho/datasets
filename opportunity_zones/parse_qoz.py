import json
import csv
import sys
import os

###################################################
# Global Variables
###################################################
BASE_DIR = '/home/pgoldtho/git/datasets/opportunity_zones/'
RESOURCE_DIR = BASE_DIR + 'resources/'
FILE_DIR = RESOURCE_DIR + 'data/2018/'
OUT_DIR = RESOURCE_DIR + 'data/2018out/'

CSV_FILE = FILE_DIR + 'Designated_QOZs.12.14.18.csv'
GEOJSON_FILE = FILE_DIR + 'zones.geojson'

def process_files():
    with open(GEOJSON_FILE) as json_file:
        data = json.load(json_file)
        geo = {}
        
        for feature in data['features']:
            if 'GEOID10' in feature['properties']:
                census_tract = feature['properties']['GEOID10']
                geo[census_tract] = {}
                if feature['geometry'] is not None:
                    geo[census_tract]['type'] = feature['geometry']['type']
                    geo[census_tract]['coordinates'] = feature['geometry']['coordinates']

    with open(CSV_FILE) as input_csv:
        qoz_data = csv.DictReader(input_csv)
        qoz_fields = qoz_data.fieldnames
        qoz_fields.append('GEO_COORDS')

        qoz_out = {}
        qoz_out['fieldnames'] = qoz_fields

        for row in qoz_data:
            census_tract = row['CENSUS_TRACT_NUMBER']
            geo_row = geo.get(census_tract, "")
            geo_row = json.dumps(geo_row)

            qoz_out[census_tract] = {}
            for key, value in row.items():
                qoz_out[census_tract][key] = value
            qoz_out[census_tract]['GEO_COORDS'] = geo_row

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    with open (OUT_DIR + 'qoz.csv', mode='w') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=qoz_out['fieldnames'], quotechar="'")
        writer.writeheader()
        line_count = 0
        for row_id in qoz_out:
            if line_count > 0:
                writer.writerow(qoz_out[row_id])
            line_count += 1

if __name__ == "__main__":
    process_files()



