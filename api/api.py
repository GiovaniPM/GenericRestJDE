from flask import request, jsonify, abort
from unicodedata import normalize

import datetime
import cx_Oracle
import flask
import json
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

def removePrefix(term):
    if isinstance(term, (int, float)):
        term = str(term)
    elif term.find("TAB.") == 0:
        term = term.replace("TAB.","")
    else:
        term = "'" + term + "'"
    return term

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
        return removePrefix(term1) + " = " + removePrefix(term2)
    elif operator == ">":
        return removePrefix(term1) + " > " + removePrefix(term2)
    elif operator == "<":
        return removePrefix(term1) + " < " + removePrefix(term2)
    elif operator == "<>":
        return removePrefix(term1) + " <> " + removePrefix(term2)
    elif operator == ">=":
        return removePrefix(term1) + " >= " + removePrefix(term2)
    elif operator == "<=":
        return removePrefix(term1) + " <= " + removePrefix(term2)

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

def makeHeader(json_data):
    json_data = flask.request.json
    output_list = json_data["data"]
    objects_list = []
    for json_object in output_list:
        header = json_object["column"]
        if isinstance(header, (int, float)):
            header = str(header)
        elif header.find("TAB.") == 0:
            header = header.replace("TAB.","")
        else:
            header = "'" + header + "'"
        objects_list.append(header)
    return objects_list

def qtyHeader(json_data):
    json_data = flask.request.json
    output_list = json_data["data"]
    qty = 0
    for json_object in output_list:
        qty =  qty + 1
    return qty

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
    return '''<h1>Web Service Directory</h1><br>https://github.com/GiovaniPM/GenericRestJDE'''

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/oracle/select', methods=['GET'])
def api_oracle_select():
    conn = createConnection()
    cur = conn.cursor()
    sql_string = makeSelect(flask.request.json)
    if app.config["DEBUG"] == True:
        outputLog(flask.request.json)
        outputLog(sql_string)
    cur.prepare(sql_string)
    cur.execute(None, {})
    rv = cur.fetchall()    
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        headers = makeHeader(flask.request.json)
        for row in rv:
            reg = {}
            for i in range(qtyHeader(flask.request.json)):
                reg[headers[i]] = row[i]
            objects_list.append(reg)
        cur.close()
        conn.close()
    return jsonify(objects_list)

app.run()