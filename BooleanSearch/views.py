from django.shortcuts import render
import os
from django.http import HttpResponse
from BooleanSearch.models import Document, Search, Validation
import time
import datetime
from .MetricCalculater import Metrics
import matplotlib.pyplot as plt
import numpy as np


def index(request):
    return render(request, 'index.html')


def help(request):
    return render(request, 'help.html')


def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        new_search, _ = Search.objects.update_or_create(query=query)
        results = new_search.search(new_search.query)
        return render(request, 'search_results.html', {'results': results, 'query': query})


def search_results(request):
    return render(request, 'search_results.html')


def refresh_database(request):
    Document.objects.all().delete()

    data_folder_path = "data"


    def generate_title(text):
        import requests

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            status_code = 404
            while status_code != 200:
                response = requests.post(API_URL, headers=headers, json=payload)
                status_code = response.status_code
            return response.json()
            
        output = query({
            "inputs": text + "Generate now theme on this text snipet",
        })
        return output[0]['summary_text']
    
    for file_name in os.listdir(data_folder_path):  
        file_path = os.path.join(data_folder_path, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.replace('\n', '') for line in lines]
        text = '.'.join(lines)
        title = generate_title('.'.join(lines[:2])).split('.')[0]
        Document.objects.update_or_create(title=title, url=file_name, text=text, snippet='', pattern='')
        print(f'Got article: Title: {title}. File name: {file_name}')
        time.sleep(1)

    return render(request, 'index.html')

def validate(request):

    tp = fp = tn = fn = 0
    test_input_path = 'test/input'
    test_output_path = 'test/output'

    positions = [False] * 13
    for idx, file_name in enumerate(os.listdir(test_input_path)):
        input_file_name = os.path.join(test_input_path, file_name)
        output_file_name = os.path.join(test_output_path, file_name)
        with open(input_file_name, 'r') as inp_file:
            text = inp_file.read().replace('\n', ' ')
        with open(output_file_name, 'r') as out_file:
            target = out_file.read().replace('\n', ' ')
        new_search, _ = Search.objects.update_or_create(query=text)
        results = new_search.search(new_search.query)
        found_doc = False
        empty_target = target == 'None'
        for result in results:
            if result.url == target:
                tp += 1
                positions[idx] = found_doc = True
                break
        if found_doc:
            continue
        if empty_target and not len(results):
            tn += 1
        elif empty_target and len(results):
            fp += 1
        else:
            fn += 1
        metric_calulater = Metrics(tp, tn, fp, fn)        

    try:
        results, _  = Validation.objects.update_or_create(
            date=datetime.datetime.now(),
            recall=metric_calulater.getRecall(),
            precision=metric_calulater.getPrecision(),
            accuracy=metric_calulater.getAccuracy(),
            error=metric_calulater.getError(),
            Fmeasure=metric_calulater.getF_measure(),
            avgPrecision=metric_calulater.getAveragePrecision(sum(positions), positions),
        )
    except ZeroDivisionError as exc:
        return render(request, "error_metric.html")


    interpolated_precisions = metric_calulater.calculateInterpolatedPrecision(sum(positions), positions)

    plt.plot(np.arange(0, 1.1, 0.1), interpolated_precisions, marker='o', linestyle='-')
    plt.xlabel('Полнота')
    plt.ylabel('Точность')
    plt.title('11-точечный график полноты/точности')
    plt.savefig('./Booleanplot.png')

    return render(request, "validate.html", {'results': results})
