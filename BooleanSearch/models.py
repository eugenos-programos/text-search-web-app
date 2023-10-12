from django.db import models
from eldar import Query
import re
from fuzzysearch import find_near_matches


class Document(models.Model):
    title = models.CharField(max_length=1000, null=True, default='Title')
    text = models.TextField(null=True, default='Sample text.')
    snippet = models.CharField(max_length=300, null=True, default='Sample snippet.')
    url = models.CharField(max_length=100, null=True)
    pattern = models.CharField(max_length=1000, null=True, default='None')


class Search(models.Model):
    query = models.CharField(max_length=1000, null=True, default='Query')

    def search(self, query):

        result = {}
        documents = Document.objects.all()
        for document in documents:
            for match in find_near_matches(query, document.text, max_l_dist=1):
                window_size = 50
                pattern = match.matched

                text = document.text
                start_text_index = text.find(pattern) if text.find(pattern) != -1 else window_size
                end_text_index = start_text_index + len(pattern)

                start_window_index = start_text_index - window_size if start_text_index - window_size > 0 else 0
                end_window_index = end_text_index + window_size if end_text_index + window_size < len(text) else len(text) - 1
                snippet = text[start_window_index:end_window_index]

                document.snippet = snippet
                document.pattern = pattern
                result[document] = 1
        return result


class Validation(models.Model):
    date = models.DateTimeField()
    recall = models.FloatField()
    precision = models.FloatField()
    accuracy = models.FloatField()
    error = models.FloatField()
    Fmeasure = models.FloatField()
    avgPrecision = models.FloatField(default=0.)
