import pandas as pd


def get_urls():
    with open("urls.txt", "r") as f:
        urls = f.readlines()
    return urls


def save_array_to_excel(array, filename):
    df = pd.DataFrame(array)
    df.to_excel(filename, index=False)
