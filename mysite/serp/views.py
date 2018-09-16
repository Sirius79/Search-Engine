from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from .models import Tool
import pymongo
from pymongo import MongoClient
import itertools
import numpy as np
from rake_nltk import Rake
from .desc import serp

@csrf_exempt
def search(request):
    query = request.POST.get("query")
    keywords = parser(query)
    client = MongoClient('localhost', 27017)
    db = client['new']
    collection = db.test['keys']
    link = []
    count = []
    print(keywords)
    for i in keywords:
        item = db.keys.find_one({'keyword':i})
        for j in range(len(item['site'])):
            if item['site'][j] not in link:
                link.append(item['site'][j])
                count.append(item['count'][j])
    matrix = np.random.rand(15, 15)
    np.fill_diagonal(matrix, 0)
    partition = np.sum(matrix, axis=0)
    matrix = np.divide(matrix, partition)
    ranks = ranker(matrix, 0.8, 0.01)
    link = [link for _, link in sorted(zip(ranks, link),reverse=True)]
    ranks = sorted(ranks)
    s = serp(link)
    title,desc = s.Descriptions()
    result = {'title': title,'link': link,'description':desc}

    return render(request, 'serp/query.html', result)


def parser(query):
    r = Rake()
    r.extract_keywords_from_text(query)

    phrase = r.get_ranked_phrases()[0].split()
    if len(phrase) < 2:
        return phrase
    else:
        keywords = list(itertools.combinations(phrase, 2))
        keywords = [' '.join(w) for w in keywords]
        keywords += phrase
        return keywords


def ranker(M, d, err):
    N = M.shape[1]
    v = np.random.rand(N, 1)
    v /= np.linalg.norm(v)
    last_v = np.ones((N, 1)) * 999
    M_hat = (d * M) + (((1 - d) / N) * np.ones((N, N)))

    while (np.linalg.norm(v - last_v) > err):
        last_v = v
        v = np.dot(M_hat, v)
    return v