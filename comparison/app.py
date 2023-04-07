import streamlit as st
import pandas as pd
import mmh3
import random
from nltk import ngrams
from tqdm import tqdm
from urllib.parse import urlparse
import os

def generate_random_seeds(n, seed=5):
    random.seed(seed)
    return random.sample(range(1, n+1), n)

def jaccard_similarity(set_a, set_b):
    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

class ShingledText:
    def __init__(self, text, random_seed=5, shingle_length=5, minhash_size=200):
        split_text = text.split()
        if len(split_text) < shingle_length:
            raise ValueError(u'input text is too short for specified shingle length of {}'.format(shingle_length))

        self.minhash = []
        self.shingles = ngrams(split_text, shingle_length)

        for hash_seed in generate_random_seeds(minhash_size, random_seed):
            min_value = float('inf')
            for shingle in ngrams(split_text, shingle_length):
                value = mmh3.hash(' '.join(shingle), hash_seed)
                min_value = min(min_value, value)
            self.minhash.append(min_value)

    def similarity(self, other_shingled_text):
        return jaccard_similarity(set(self.minhash),
                set(other_shingled_text.minhash))

def apply_shingled(row, urls, shingles):
    url = row['address']
    urli = urls.index(url)
    urlsh = shingles[urli]

    if not urlsh:
        row['Sim Score'] = 0.0
        row['Sim Match'] = ""
        return row

    high = 0.0
    match = ""

    for i, sh in enumerate(shingles):
        if not urli == i and sh:
            sim = jaccard_similarity(set(urlsh), set(sh))
            if sim > high:
                high = sim
                match = urls[i]

    row['Sim Score'] = high
    row['Sim Match'] = match

    return row

def process_input_file(file, content_column):
    df = pd.read_csv(file)

    df.columns = [c.lower().strip() for c in df.columns]  # Add this line to clean up the column names
    content_col = content_column.lower()

    # Print the columns for debugging
    st.write("Columns in the DataFrame:", df.columns)

    df = df[df[content_col] == df[content_col]]
    df.reset_index(drop=True, inplace=True)

    urls = []
    shingles = []

    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        text = row[content_col]
        url = row['address']
        default = "Maecenas vestibulum euismod dui id scelerisque."

        if isinstance(text, str) and len(text.split()) > 5:
            urls.append(url)
            shingles.append(ShingledText(text).minhash)
        else:
            urls.append(url)
            shingles.append(ShingledText(default).minhash)

    df_comp = df.apply(apply_shingled, args=(urls, shingles), axis=1)

    return df_comp

st.title('Screaming Frog Content Similarity Analysis')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    content_column = "article text"
    df_result = process_input_file(uploaded_file, content_column)
    # You can display the resulting DataFrame or handle it as needed
    st.write(df_result)
