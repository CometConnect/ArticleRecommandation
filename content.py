from pandas import read_csv, DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = read_csv("data.csv")

count = CountVectorizer(stop_words='english')
matrix = count.fit_transform(data['soup'])

similarity = cosine_similarity(matrix, matrix)

def get_recommandation(i):
    scores = sorted(
        list(enumerate(similarity[i])),
        key=lambda x: x[1],
        reverse=True
    )[1:11]
    response = DataFrame(columns=data.columns)
    for index, _ in scores:
        response.loc[len(response.index)] = data.iloc[index]
    response.drop(columns=['soup'], inplace=True)
    return response