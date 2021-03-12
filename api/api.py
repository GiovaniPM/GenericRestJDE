from flask import request, jsonify, abort
from unicodedata import normalize

import datetime
import cx_Oracle
import flask
import json
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# Create a connection with Oracle
def createConnection():
    db_host = 'localhost'
    db_port = 1521
    db_servicename = 'XE'
    db_user = 'C##GIOVANIPM'
    db_pass = 'Pm11092j'

    conn_string = "\
                   (DESCRIPTION =\
                        (ADDRESS_LIST =\
                            (ADDRESS = (PROTOCOL = TCP)\
                                (HOST = %s)\
                                (PORT = %s))\
                            )\
                        (CONNECT_DATA =\
                            (SERVICE_NAME = %s)\
                        )\
                    )" % (db_host, str(db_port), db_servicename)
    return cx_Oracle.connect(user=db_user, password=db_pass, dsn=conn_string, encoding='UTF-8')

def outputLog(text):
    text = str(text)
    print(" ".join(text.split()))

def removeExtendCharacters(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def makeWhere(operator, term1, term2):
    if operator == "(":
        return "("
    elif operator == ")":
        return ")"
    elif operator == "AND":
        return " AND "
    elif operator == "OR":
        return " OR "
    elif operator == "NOT":
        return " NOT "
    elif operator == "=":
        if isinstance(term1, (int, float)):
            term1 = str(term1)
        elif term1.find("TAB.") == 0:
            term1 = term1.replace("TAB.","")
        else:
            term1 = "'" + term1 + "'"
        if isinstance(term2, (int, float)):
            term2 = str(term2)
        elif term1.find("TAB.") == 0:
            term2 = term2.replace("TAB.","")
        else:
            term2 = "'" + term2 + "'"
        return term1 + " = " + term2

def makeOrder(column, order):
    object_value = column
    if object_value.find("TAB.") == 0:
        object_value = object_value.replace("TAB.","")
    if order == "A":
        object_value = object_value + " ASC,"
    elif order == "D":
        object_value = object_value + " DESC,"
    else:
        object_value = object_value + ","
    return object_value

def makeSelect(json_data):
    json_data = flask.request.json
    object_name = json_data["object"]
    filter_list = json_data["filter"]
    order_list = json_data["order"]
    output_list = json_data["data"]
    sql_string = "SELECT"
    for json_object in output_list:
        object_value = json_object["column"]
        if object_value.find("TAB.") == 0:
            object_value = object_value.replace("TAB.","")
        sql_string = sql_string + " " + object_value + ","
    sql_string = sql_string + " rownum "
    sql_string = sql_string + " FROM "
    sql_string = sql_string + object_name
    if filter_list != None:
        sql_string = sql_string + " WHERE "
        for json_object in filter_list:
            object_value = makeWhere(json_object["operator"], json_object["term1"], json_object["term2"])
            sql_string = sql_string + " " + object_value
    if order_list != None:
        sql_string = sql_string + " ORDER BY "
        for json_object in order_list:
            object_value = makeOrder(json_object["column"], json_object["sort"])
            sql_string = sql_string + " " + object_value
        sql_string = sql_string + " 1 "
    return sql_string

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/oracle/F4101', methods=['GET'])
def api_oracle_f4101():
    conn = createConnection()
    cur = conn.cursor()
    sql_string =   "SELECT\
                        IMITM,\
                        IMLITM,\
                        IMDSC1,\
                        IMDSC2\
                    FROM\
                        F4101\
                    ORDER BY\
                        IMITM"
    cur.prepare(sql_string)
    cur.execute(None, {})
    rv = cur.fetchall()    
    outputLog(sql_string)
    outputLog(datetime.datetime.now())
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        for row in rv:
            reg           = {}
            reg['IMITM' ] = row[0]
            reg['IMLITM'] = row[1]
            reg['IMPRP1'] = removeExtendCharacters(row[2])
            reg['IMPRP2'] = removeExtendCharacters(row[3])
            objects_list.append(reg)
        cur.close()
        conn.close()
    return jsonify(objects_list)

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/oracle/select', methods=['GET'])
def api_oracle_select():
    conn = createConnection()
    cur = conn.cursor()
    sql_string = makeSelect(flask.request.json)
    cur.prepare(sql_string)
    cur.execute(None, {})
    rv = cur.fetchall()    
    outputLog(sql_string)
    outputLog(datetime.datetime.now())
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        for row in rv:
            reg           = {}
            reg['IMITM' ] = row[0]
            reg['IMPRP1'] = row[1]
            reg['IMPRP2'] = row[2]
            objects_list.append(reg)
        cur.close()
        conn.close()
    return jsonify(objects_list)

app.run()