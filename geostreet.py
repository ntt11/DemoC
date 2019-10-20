from flask import Flask, render_template, jsonify
import requests
import psycopg2
from key import key
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

connection = psycopg2.connect(user="postgres",
						  password="boohoo88",
						  host="localhost",
						  port="5432",
						  database="demo")

cursor = connection.cursor()
postgreSQL_select_Query = "select distinct fullname from tl_2014_01001_roads"

cursor.execute(postgreSQL_select_Query)
print("Selecting rows from tl_state table using cursor.fetchall")
street_records =cursor.fetchall()
#print("Print each row and it's columns values")
#for row in street_records:
#	print("St = ", row[0],)


@app.route("/",methods=["GET"])
def retrieve():
	return render_template('street.html',query=street_records)

@app.route("/sendRequest/<string:query>")
def results(query):


	search_payload = {"key":key, "query":query}
	search_req = requests.get(search_url, params=search_payload)
	search_json = search_req.json()

	place_id = search_json["results"][0]["place_id"]


	details_payload = {"key":key, "placeid":place_id}
	details_resp = requests.get(details_url, params=details_payload)
	details_json = details_resp.json()

	url = details_json["result"]["url"]
	return jsonify({'result' : url})

if __name__ ==  "__main__":
	app.run(debug=True)



