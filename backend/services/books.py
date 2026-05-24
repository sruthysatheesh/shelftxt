import pandas as pd
from fastapi import HTTPException

from backend.repository.books_repository import get_all_books, save_books


def parse_date_or_today(date_str):
    try:
        return (
            pd.to_datetime(date_str)
            if date_str
            else pd.Timestamp.today().normalize()
        )
    except Exception:
        return pd.Timestamp.today().normalize()


def delete_book_by_title(title: str):
    df = get_all_books()

    if title not in df["Title"].values:
        raise HTTPException(status_code=404, detail="Book not found")

    df = df.loc[df["Title"] != title].copy()
    save_books(df)

    return {"message": "Book deleted"}