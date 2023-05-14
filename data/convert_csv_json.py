import csv
import json


def convert(csv_file, json_file, model):
    result = []
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        for line in csv.DictReader(csv_f):
            if 'is_published' in line:
                if line['is_published'] == 'TRUE':
                    line['is_published'] = True
                else:
                    line['is_published'] = False
            if 'location_id' in line:
                line['locations'] = [line['location_id']]
                del line['location_id']

            result.append({"model": model, "fields": line})

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    convert('ad.csv', 'ad.json', 'ads.ad')
    convert('category.csv', 'category.json', 'ads.category')
    convert('user.csv', 'user.json', 'users.user')
    convert('location.csv', 'location.json', 'users.location')
