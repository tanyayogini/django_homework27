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

            result.append({"model": model, "fields": line})

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    convert('ads.csv', 'ads.json', 'ads.ad')
    convert('categories.csv', 'categories.json', 'ads.category')
