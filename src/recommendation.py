import pandas as pd

def recommend(occasion,budget):

    df=pd.read_csv("dataset/fashion_products.csv")

    results=df[
        (df["Occasion"]==occasion)
        &
        (df["Price"]<=budget)
    ]

    return results