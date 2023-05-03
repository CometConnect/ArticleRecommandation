from flask import Flask, jsonify
from pandas import read_csv

app = Flask(__name__)
data = read_csv("data.csv")
liked_data = read_csv("liked.csv")
unliked_data = read_csv("unliked.csv")

"""
/        -> Return the first article
/liked   -> Like the first article
/unliked -> Dislike the first article
"""

def sync_files():
  try: data.drop(columns=["Unnamed: 0.1"], inplace=True)
  except: pass
  try: liked_data.drop(columns=["Unnamed: 0.1"], inplace=True)
  except: pass
  try: unliked_data.drop(columns=["Unnamed: 0.1"], inplace=True)
  except: pass

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
  try:
    article = data.iloc[0]
    data.drop([article["Unnamed: 0"]], inplace=True)
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
    data.drop([article["Unnamed: 0"]], inplace=True)
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

if __name__ == "__main__":
  app.run()