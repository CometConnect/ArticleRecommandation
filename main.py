from flask import Flask, jsonify
from pandas import read_csv
from content import get_recommandation

app = Flask(__name__)
data = read_csv("data.csv")
liked_data = read_csv("liked.csv")
unliked_data = read_csv("unliked.csv")

"""
/               -> Return the first article
/liked          -> Like the first article
/unliked        -> Dislike the first article
/popular        -> Demographicly Filtered Top Movies
/recommandation -> Content based Filtered Top Movies
"""


def sync_files():
    try:
        data.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)
    except:
        pass
    try:
        liked_data.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)
    except:
        pass
    try:
        unliked_data.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)
    except:
        pass

    data.to_csv("data.csv")
    liked_data.to_csv("liked.csv")
    unliked_data.to_csv("unliked.csv")


def dbg():
    print(data.info())
    print(liked_data.info())
    print(unliked_data.info())


@app.route("/")
def article():
    return data.iloc[0].to_json()


@app.route("/liked")
def liked():
    article = data.iloc[0]
    try:
        try:
            data.drop([data.iloc[0]["Unnamed: 0"]], inplace=True)
        except:
            pass
        liked_data.loc[len(liked_data)] = article
        sync_files()
        return jsonify({
            "status": "Ok"
        })
    except:
        dbg()
        return jsonify({
            "status": "Not Ok"
        })


@app.route("/unliked")
def unliked():
    try:
        article = data.iloc[0]
        try:
            data.drop([data.iloc[0]["Unnamed: 0"]], inplace=True)
        except:
            pass
        unliked_data.loc[len(unliked_data)] = article
        sync_files()
        return jsonify({
            "status": "Ok"
        })
    except:
        dbg()
        return jsonify({
            "status": "Not Ok"
        })


@app.route("/popular")
def popular():
    popular = []
    for item in data.head(10).iloc:
        popular.append(item.to_json())

    return jsonify(popular)


@app.route("/recommandation")
def recommandation():
    recommandation = []
    for movie in liked_data.iloc:
        for item in get_recommandation(movie["Unnamed: 0"]).iloc:
            recommandation.append(item.to_json())

    return jsonify(recommandation)


if __name__ == "__main__":
    app.run()
