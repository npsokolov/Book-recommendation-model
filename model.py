import pandas as pd
import numpy as np


def get_recommendation(user_id, df_recommendation, user_books_liked, k=5):
    # получить топ 5 книг, в качестве рекомендуемых

    user_pred = df_recommendation[df_recommendation.index == user_id].copy().sort_values(by=user_id, axis=1)
    # получили предсказания для пользователя

    book_for_user = []
    for i in range(len(user_pred.columns) - 1, -1, -1):
        if user_pred.columns[i] not in user_books_liked:
            book_for_user.append(user_pred.columns[i])
        if len(book_for_user) >= k:
            return book_for_user
    return book_for_user


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
