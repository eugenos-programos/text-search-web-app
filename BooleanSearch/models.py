from django.db import models
from eldar import Query
import re
from fuzzysearch import find_near_matches


class Document(models.Model):
    title = models.CharField(max_length=1000, null=True, default='Title')
    text = models.TextField(null=True, default='Sample text.')
    snippet = models.CharField(max_length=300, null=True, default='Sample snippet.')
    url = models.CharField(max_length=1000, null=True)


class Search(models.Model):
    query = models.CharField(max_length=1000, null=True, default='Query')

    def search(self, query):
        eldar_q = Query(query, ignore_case=True, match_word=False)
        match = re.search('[a-zA-Z]+', query)

        result = {}
        documents = Document.objects.all()
        for document in documents:
            if find_near_matches():
                i = document.text.find(match.group())
                snippet = document.text[max(0, i - 100):min(i + 100, len(document.text))]
                document.snippet = snippet
                result[document] = 1

        return result
