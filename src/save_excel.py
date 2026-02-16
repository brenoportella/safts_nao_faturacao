import pandas as pd


def save_to_excel(df, counter, month, year):
    if counter % 10 == 0:
        df.to_excel(f"output_{month}_{year}.xlsx", index=False)
