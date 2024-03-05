from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sys
import linecache
import string
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    # Perform stemming using Porter Stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    # Reconstruct the preprocessed text from processed words
    processed_text = " ".join(words)
    return processed_text

def get_files(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().splitlines()
    return content

# Function to read text from file and convert to a list
def get_doc4mtxt(folder_path):
    # List all the text files in the folder
    all_lists=[]
    text_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    for file_name in text_files:
        file_path = os.path.join(folder_path, file_name)
        file_list = get_files(file_path)
        all_lists.append(file_list)
    return all_lists



def top_results(names, top_indices):
    top_document_names = [names[i] for i in top_indices]
    return top_document_names


def get_results(query, path):

    vectorizer = TfidfVectorizer(analyzer='word',
                                 sublinear_tf=True,
                                 strip_accents='unicode',
                                 token_pattern=r'\w{1,}',
                                 ngram_range=(1, 1),
                                 max_features=10000)
    # Transform the query using the same vectorizer
    query_pp = preprocess_text(query)
    data, indexes,names = get_doc4mtxt(path)
    data_tfidf = vectorizer.fit_transform(data)
    query_tfidf = vectorizer.transform([query_pp])
    # Compute cosine similarity between query and all documents
    cosine_similarities = cosine_similarity(query_tfidf, data_tfidf).flatten()
    indices = [i for i, similarity in enumerate(
        cosine_similarities) if similarity > 0]
    top_indices = sorted(
        indices, key=lambda i: cosine_similarities[i], reverse=True)[:20]
    # Sort indices based on similarity scores
    # top_indices = cosine_similarities.argsort()[::-1][:20]

    return top_indices, names, indexes


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, checkbox1: bool = False, checkbox2: bool = False):
    if checkbox2:
        return templates.TemplateResponse("another_page.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search/", response_class=HTMLResponse)
async def search(request: Request, query: str):
    path = "Lists Fol"
    top_indices, names, indexes = get_results(query, path)
    top_similarities = top_results(names, top_indices)
    name_of = [" ".join(top_similaritie.split("-")).upper()
               for top_similaritie in top_similarities]
    name_ques = [string[:42] +
                 "..." if len(string) > 42 else string for string in name_of]
    with open("links.txt", "r", encoding="utf-8") as file:
        link_arr = file.read()
    links = link_arr.split("\n")
    top_links = [links[int(indexes[i])-1] for i in top_indices]
    results = [{"Link Name": link_name, "Link": link_url}
               for link_name, link_url in zip(name_ques, top_links)]
    return templates.TemplateResponse("index.html", {"request": request, "query": query, "results": results})


@app.get("/question_page", response_class=HTMLResponse)
async def read_another(request: Request, problem_link: str):
    return templates.TemplateResponse("question_page.html", {"request": request, "result": problem_link})
