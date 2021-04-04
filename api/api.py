from flask import request, jsonify, abort
from unicodedata import normalize

import datetime
import cx_Oracle
import flask
import logging
import json
import os
import re
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = False
# logging.basicConfig(level=logging.DEBUG)


class Binders:
    activate = True
    parameters = {}
    next = 0


class DBKeys:
    db_host = 'localhost'
    db_port = 1521
    db_servicename = 'XE'
    db_user = 'C##GIOVANIPM'
    db_pass = 'Pm11092j'


class Errors:
    qty = 0
    list = []


class Error(Exception):
    """Base class for other exceptions"""
    pass


class NoColumnedQuery(Error):
    """Return column(s) are expected!"""
    pass


class NoFilteredQuery(Error):
    """Filter column(s) are expected!"""
    pass


class NoInsertedValuesQuery(Error):
    """Insert value(s) and/or column(s) are expected!"""
    pass


class NoUpdatedValuesQuery(Error):
    """Update value(s) and/or column(s) are expected!"""
    pass


class DateBadFormated(Error):
    """Date Must be YYYY-MM-DD!"""
    pass


class TimeBadFormated(Error):
    """Date Must be HH:mm:SS!"""
    pass


class GenericError(Error):
    """This is a generic error!"""
    pass


def thereisJson():
    if request.environ['CONTENT_LENGTH'] == '0':
        errorCatch(500.07, "JSON in BODY is required!")
        raise GenericError
    return ""


def findWord(dictseq, txt):
    for word in dictseq:
        if word == txt:
            return True
    return False


def findValue(dictseq, txt):
    for word in dictseq:
        if dictseq[word] == txt:
            return True
    return False


def errorCatch(number, text):
    reg = {}
    reg['number'] = number
    reg['text'] = text
    Errors.list.append(reg)
    Errors.qty = Errors.qty + 1
    return True


def clearDefinitions():
    global Binders, Errors
    Binders.parameters = {}
    Binders.next = 0
    Errors.list = []
    Errors.qty = 0


def createConnection():
    try:
        DBKeys.db_host = os.environ['ORACLE_SERVER']
    except Exception:
        DBKeys.db_host = 'localhost'
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
                    )" % (DBKeys.db_host, str(DBKeys.db_port), DBKeys.db_servicename)
    return cx_Oracle.connect(user=DBKeys.db_user, password=DBKeys.db_pass, dsn=conn_string, encoding='UTF-8')


def outputLog(text):
    text = str(text)
    print(" ".join(text.split()))


def removeExtendCharacters(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def datestdtojd(stddate):
    fmt = '%Y-%m-%d'
    sdtdate = datetime.datetime.strptime(stddate, fmt)
    nmyear = sdtdate.year
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return(nmyear*1000+jdate)


def jdtodatestd(jdate):
    fmt = '%Y%j'
    datestd = datetime.datetime.strptime(jdate, fmt).date()
    return(datestd)


def timestdtonum(stddate):
    fmt = '%H:%M:%S'
    stddate = datetime.datetime.strptime(stddate, fmt)
    mmHour = stddate.hour
    mnMinute = stddate.minute
    mnSecond = stddate.second
    return(mnSecond+100*mnMinute+10000*mmHour)


def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def valid_time(datestring):
    try:
        datetime.datetime.strptime(datestring, '%H:%M:%S')
        return True
    except ValueError:
        return False


def binderCreate(txt):
    global Binders
    Binders.next = Binders.next + 1
    bindersName = "B" + str(Binders.next)
    key = bindersName
    Binders.parameters[key] = txt
    return ":" + bindersName


def defineType(txt):
    if txt != None:
        if isinstance(txt, (int, float)):
            return "int"
        elif txt.find("TAB.") == 0:
            return "tab"
        elif txt.find("DTA.") == 0:
            return "dta"
        elif txt.find("TME.") == 0:
            return "tme"
        elif txt.find("CNJ.") == 0:
            return "cnj"
        else:
            return "str"


def removePrefix(term):
    if Binders.activate == True:
        if defineType(term) == "int":
            term = binderCreate(str(term))
        elif defineType(term) == "tab":
            term = term.replace("TAB.", "")
        elif defineType(term) == "dta":
            term = term.replace("DTA.", "")
            if valid_date(term):
                term = binderCreate(str(datestdtojd(term)-1900000))
            else:
                term = binderCreate(str(999999))
                errorCatch(500.05, "Date must be YYYY-MM-DD format!")
        elif defineType(term) == "tme":
            term = term.replace("TME.", "")
            if valid_time(term):
                term = binderCreate(str(timestdtonum(term)))
            else:
                term = binderCreate(str(999999))
                errorCatch(500.06, "Time must be HH:mm:SS format!")
        elif defineType(term) == "cnj":
            term = term.replace("CNJ.", "")
        else:
            term = binderCreate(term.strip())
        return term
    else:
        if defineType(term) == "int":
            term = str(term)
        elif defineType(term) == "tab":
            term = term.replace("TAB.", "")
        elif defineType(term) == "dta":
            term = term.replace("DTA.", "")
            if valid_date(term):
                term = str(datestdtojd(term)-1900000)
            else:
                term = str(999999)
                errorCatch(500.05, "Date must be YYYY-MM-DD format!")
        elif defineType(term) == "tme":
            term = term.replace("TME.", "")
            if valid_time(term):
                term = str(timestdtonum(term))
            else:
                term = str(999999)
                errorCatch(500.06, "Time must be HH:mm:SS format!")
        elif defineType(term) == "cnj":
            term = term.replace("CNJ.", "")
        else:
            term = "'" + term + "'"
        return term


def makeWhere(operator, term1, term2):
    if Binders.activate == True:
        string1 = defineType(term1)
        string2 = defineType(term2)
        if term1 != None:
            term1 = removePrefix(term1)
        if term2 != None:
            term2 = removePrefix(term2)
        if string1 == "str" or string2 == "str":
            if string1 == "str":
                term1 = term1.strip()
            else:
                term1 = "TRIM(" + term1 + ")"
            if string2 == "str":
                term2 = term2.strip()
            else:
                term2 = "TRIM(" + term2 + ")"
    else:
        if term1 != None:
            term1 = removePrefix(term1)
        if term2 != None:
            term2 = removePrefix(term2)
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
    elif operator == "==":
        return term1 + " = " + term2
    elif operator == "=":
        return term1 + " = " + term2
    elif operator == ">":
        return term1 + " > " + term2
    elif operator == "<":
        return term1 + " < " + term2
    elif operator == "<>":
        return term1 + " <> " + term2
    elif operator == "!=":
        return term1 + " <> " + term2
    elif operator == ">=":
        return term1 + " >= " + term2
    elif operator == "<=":
        return term1 + " <= " + term2
    elif operator == "IN":
        return term1 + " IN " + term2
    elif operator == "NOT IN":
        return term1 + " NOT IN " + term2


def makeSet(term1, term2):
    if term1 != None:
        term1 = removePrefix(term1)
    if term2 != None:
        term2 = removePrefix(term2)
    return term1 + " = " + term2


def makeOrder(column, order):
    object_value = column
    if object_value.find("TAB.") == 0:
        object_value = object_value.replace("TAB.", "")
    if order == "A":
        object_value = object_value + " ASC,"
    elif order == "D":
        object_value = object_value + " DESC,"
    else:
        object_value = object_value + ","
    return object_value


def makeHeader(json_data):
    output_list = json_data["data"]
    objects_list = []
    for json_object in output_list:
        header = json_object["column"]
        if isinstance(header, (int, float)):
            header = str(header)
        elif header.find("TAB.") == 0:
            header = header.replace("TAB.", "")
        else:
            header = "'" + header + "'"
        objects_list.append(header)
    return objects_list


def qtyHeader(json_data):
    output_list = json_data["data"]
    qty = 0
    for json_object in output_list:
        qty = qty + 1
    return qty


def makeSelect(json_data):
    object_name = json_data["object"]
    filter_list = json_data["filter"]
    order_list = json_data["order"]
    output_list = json_data["data"]
    if output_list == None:
        errorCatch(500.01, "Output column(s) are required!")
    else:
        sql_string = "SELECT"
        for json_object in output_list:
            object_value = json_object["column"]
            if object_value.find("TAB.") == 0:
                object_value = object_value.replace("TAB.", "")
            sql_string = sql_string + " " + object_value + ","
        sql_string = sql_string + " rownum "
        sql_string = sql_string + " FROM "
        sql_string = sql_string + object_name
        if filter_list != None:
            sql_string = sql_string + " WHERE "
            for json_object in filter_list:
                object_value = makeWhere(
                    json_object["operator"], json_object["term1"], json_object["term2"])
                sql_string = sql_string + " " + object_value
        if order_list != None:
            sql_string = sql_string + " ORDER BY "
            for json_object in order_list:
                object_value = makeOrder(
                    json_object["column"], json_object["sort"])
                sql_string = sql_string + " " + object_value
            sql_string = sql_string + " 1 "
    if Errors.qty > 0:
        raise GenericError
    else:
        return sql_string


def makeUpdate(json_data):
    object_name = json_data["object"]
    filter_list = json_data["filter"]
    output_list = json_data["data"]
    sql_string = "UPDATE "
    sql_string = sql_string + object_name
    sql_string = sql_string + " SET "
    update_list = ""
    if output_list == None:
        errorCatch(500.04, "Update column(s) are required!")
    else:
        for json_object in output_list:
            if update_list == "":
                update_list = makeSet(
                    json_object["column"], json_object["value"])
            else:
                update_list = update_list + ", " + \
                    makeSet(json_object["column"], json_object["value"])
    sql_string = sql_string + " " + update_list
    if filter_list == None:
        errorCatch(500.02, "Filter column(s) are required!")
    else:
        sql_string = sql_string + " WHERE "
        for json_object in filter_list:
            object_value = makeWhere(
                json_object["operator"], json_object["term1"], json_object["term2"])
            sql_string = sql_string + " " + object_value
    if Errors.qty > 0:
        raise GenericError
    else:
        return sql_string


def makeInsert(json_data):
    object_name = json_data["object"]
    output_list = json_data["data"]
    sql_string = "INSERT INTO "
    sql_string = sql_string + object_name
    sql_string = sql_string + " ( "
    insert_list = ""
    if output_list == None:
        errorCatch(500.03, "Insert column(s) are required!")
    else:
        for json_object in output_list:
            if insert_list == "":
                insert_list = removePrefix(json_object["column"])
            else:
                insert_list = insert_list + ", " + \
                    removePrefix(json_object["column"])
        sql_string = sql_string + " " + insert_list
        sql_string = sql_string + " ) VALUES ( "
        insert_list = ""
        for json_object in output_list:
            if insert_list == "":
                insert_list = removePrefix(json_object["value"])
            else:
                insert_list = insert_list + ", " + \
                    removePrefix(json_object["value"])
        sql_string = sql_string + " " + insert_list
        sql_string = sql_string + " ) "
    if Errors.qty > 0:
        raise GenericError
    else:
        return sql_string


def makeDelete(json_data):
    object_name = json_data["object"]
    filter_list = json_data["filter"]
    sql_string = "DELETE FROM "
    sql_string = sql_string + object_name
    sql_string = sql_string + " WHERE "
    if filter_list == None:
        errorCatch(500.02, "Filter column(s) are required!")
    else:
        for json_object in filter_list:
            object_value = makeWhere(
                json_object["operator"], json_object["term1"], json_object["term2"])
            sql_string = sql_string + " " + object_value
    if Errors.qty > 0:
        raise GenericError
    else:
        return sql_string


@app.route('/api/v1/oracle/select', methods=['GET'])
def api_oracle_select():
    clearDefinitions()
    conn = createConnection()
    cur = conn.cursor()
    try:
        thereisJson()
        sql_string = makeSelect(flask.request.json)
    except GenericError:
        return jsonify(Errors.list), 406
    except Exception as e:
        cur.close()
        conn.close()
        errorCatch(-1, format(e))
        return jsonify(Errors.list), 406
    if app.config["DEBUG"] == True:
        outputLog(flask.request.json)
        outputLog(sql_string)
        if Binders.activate == True:
            outputLog(Binders.parameters)
    try:
        cur.prepare(sql_string)
        if Binders.activate == True:
            cur.execute(None, Binders.parameters)
        else:
            cur.execute(None, {})
        rv = cur.fetchall()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        errorCatch(errorObj.code, errorObj.message)
        cur.close()
        conn.close()
        return jsonify(Errors.list), 406
    if rv is None or rv == []:
        cur.close()
        conn.close()
        return jsonify(rv), 204
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
    return jsonify(objects_list), 200


@app.route('/api/v1/oracle/update', methods=['PUT'])
def api_oracle_update():
    clearDefinitions()
    conn = createConnection()
    cur = conn.cursor()
    try:
        thereisJson()
        sql_string = makeUpdate(flask.request.json)
    except GenericError:
        return jsonify(Errors.list), 406
    except Exception as e:
        cur.close()
        conn.close()
        errorCatch(-1, format(e))
        return jsonify(Errors.list), 406
    if app.config["DEBUG"] == True:
        outputLog(flask.request.json)
        outputLog(sql_string)
        if Binders.activate == True:
            outputLog(Binders.parameters)
    try:
        cur.prepare(sql_string)
        if Binders.activate == True:
            cur.execute(None, Binders.parameters)
        else:
            cur.execute(None, {})
        conn.commit()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        errorCatch(errorObj.code, errorObj.message)
        cur.close()
        conn.close()
        return jsonify(Errors.list), 406
    cur.close()
    conn.close()
    return jsonify([]), 200


@app.route('/api/v1/oracle/insert', methods=['POST'])
def api_oracle_insert():
    clearDefinitions()
    conn = createConnection()
    cur = conn.cursor()
    try:
        thereisJson()
        sql_string = makeInsert(flask.request.json)
    except GenericError:
        return jsonify(Errors.list), 406
    except Exception as e:
        cur.close()
        conn.close()
        errorCatch(-1, format(e))
        return jsonify(Errors.list), 406
    if app.config["DEBUG"] == True:
        outputLog(flask.request.json)
        outputLog(sql_string)
        if Binders.activate == True:
            outputLog(Binders.parameters)
    try:
        cur.prepare(sql_string)
        if Binders.activate == True:
            cur.execute(None, Binders.parameters)
        else:
            cur.execute(None, {})
        conn.commit()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        errorCatch(errorObj.code, errorObj.message)
        cur.close()
        conn.close()
        return jsonify(Errors.list), 406
    cur.close()
    conn.close()
    return jsonify([]), 200


@app.route('/api/v1/oracle/delete', methods=['DELETE'])
def api_oracle_delete():
    clearDefinitions()
    conn = createConnection()
    cur = conn.cursor()
    try:
        thereisJson()
        sql_string = makeDelete(flask.request.json)
    except GenericError:
        return jsonify(Errors.list), 406
    except Exception as e:
        cur.close()
        conn.close()
        errorCatch(-1, format(e))
        return jsonify(Errors.list), 406
    if app.config["DEBUG"] == True:
        outputLog(flask.request.json)
        outputLog(sql_string)
        if Binders.activate == True:
            outputLog(Binders.parameters)
    try:
        cur.prepare(sql_string)
        if Binders.activate == True:
            cur.execute(None, Binders.parameters)
        else:
            cur.execute(None, {})
        conn.commit()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        errorCatch(errorObj.code, errorObj.message)
        cur.close()
        conn.close()
        return jsonify(Errors.list), 406
    cur.close()
    conn.close()
    return jsonify([]), 200


@app.route('/', methods=['GET'])
def home():
    #app.logger.warning('A warning occurred (%d apples)', 42)
    #app.logger.error('An error occurred')
    # app.logger.info('Info')
    return '''
    <h1>Web Service Directory</h1>
    To see more information please visite the <a href="https://github.com/GiovaniPM/GenericRestJDE">project site.</a><br>
    <h2>Available functions:</h2>

    <h3>- This directory <a href="http://127.0.0.1:8080/">http://127.0.0.1:8080/</a></h3>

    <h3>- GET information <a href="http://127.0.0.1:8080/api/v1/oracle/select">http://127.0.0.1:8080/api/v1/oracle/select</a></h3>
    <div style="font-family:Verdana;font-size:60%;background-color:gray;color:black;padding:10px;">
        <div style="background-color:white;color:black;padding:30px;">
            URL - <mark>http://127.0.0.1:8080/api/v1/oracle/select</mark><br>
            Heards - <mark>{"Content-Type":"application/json"}</mark><br>
            Method - <mark>GET</mark><br>
            Body - <mark>{ "object": "F4111", "filter": [ { "operator": ">", "term1": "TAB.ILCRDJ", "term2": 118000 }, { "operator": "AND", "term1": null, "term2": null }, { "operator": "<", "term1": "TAB.ILCRDJ", "term2": 119000 } ], "order": null, "data": [ { "column": "TAB.ILITM", "value": null }, { "column": "TAB.ILLITM", "value": null }, { "column": "TAB.ILMCU", "value": null }, { "column": "TAB.ILCRDJ", "value": null } ] }</mark><br>
            <br>
            curl -X GET -i -H "Content-Type: application/json" -d "{\"object\": \"F4111\", \"filter\": [{\"operator\": \"=\", \"term1\": \"TAB.ILLITM\", \"term2\": \"ME00004N                 \"}], \"order\": null, \"data\": [{\"column\": \"TAB.ILITM\", \"value\": null}, {\"column\": \"TAB.ILLITM\", \"value\": null}, {\"column\": \"TAB.ILMCU\", \"value\": null}, {\"column\": \"TAB.ILCRDJ\", \"value\": null}]}" http://127.0.0.1:8080/api/v1/oracle/select
        </div>
    </div>

    <h3>- CHANGE information <a href="http://127.0.0.1:8080/api/v1/oracle/update">http://127.0.0.1:8080/api/v1/oracle/update</a></h3>
    <div style="font-family:Verdana;font-size:60%;background-color:gray;color:black;padding:10px;">
        <div style="background-color:white;color:black;padding:30px;">
            URL - <mark>http://127.0.0.1:8080/api/v1/oracle/update</mark><br>
            Heards - <mark>{"Content-Type":"application/json"}</mark><br>
            Method - <mark>POST</mark><br>
            Body - <mark>{ "object": "F4101", "filter": [ { "operator": "(", "term1": null, "term2": null }, { "operator": "=", "term1": "TAB.IMPRP1", "term2": "A01" }, { "operator": "OR", "term1": null, "term2": null }, { "operator": "=", "term1": "TAB.IMPRP1", "term2": "A02" }, { "operator": ")", "term1": null, "term2": null }, { "operator": "AND", "term1": null, "term2": null }, { "operator": "=", "term1": "TAB.IMPRP2", "term2": "B01" } ], "order": null, "data": [ { "column": "TAB.IMDSC1", "value": "TAB.IMDSC2" }, { "column": "TAB.IMDSC2", "value": "TAB.IMDSC1" } ] }</mark><br>
            <br>
            curl -X POST -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": [ { \"operator\": \"(\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP1\", \"term2\": \"A01\" }, { \"operator\": \"OR\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP1\", \"term2\": \"A02\" }, { \"operator\": \")\", \"term1\": null, \"term2\": null }, { \"operator\": \"AND\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP2\", \"term2\": \"B01\" } ], \"order\": null, \"data\": [ { \"column\": \"TAB.IMDSC1\", \"value\": \"TAB.IMDSC2\" }, { \"column\": \"TAB.IMDSC2\", \"value\": \"TAB.IMDSC1\" } ] }" http://127.0.0.1:8080/api/v1/oracle/update
        </div>
    </div>

    <h3>- ADD information <a href="http://127.0.0.1:8080/api/v1/oracle/insert">http://127.0.0.1:8080/api/v1/oracle/insert</a></h3>
    <div style="font-family:Verdana;font-size:60%;background-color:gray;color:black;padding:10px;">
        <div style="background-color:white;color:black;padding:30px;">
            URL - <mark>http://127.0.0.1:8080/api/v1/oracle/insert</mark><br>
            Heards - <mark>{"Content-Type":"application/json"}</mark><br>
            Method - <mark>POST</mark><br>
            Body - <mark>{ "object": "F4101", "filter": null, "order": null, "data": [ { "column": "TAB.IMITM", "value": 123 }, { "column": "TAB.IMDSC1", "value": "ITEM ONE" }, { "column": "TAB.IMDSC2", "value": "First Item" } ] } </mark><br>
            <br>
            curl -X POST -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": null, \"order\": null, \"data\": [ { \"column\": \"TAB.IMITM\", \"value\": 123 }, { \"column\": \"TAB.IMLITM\", \"value\": "123" }, { \"column\": \"TAB.IMAITM\", \"value\": 123 }, { \"column\": \"TAB.IMDSC1\", \"value\": \"ITEM ONE\" }, { \"column\": \"TAB.IMDSC2\", \"value\": \"First Item\" } ] } " http://127.0.0.1:8080/api/v1/oracle/insert
        </div>
    </div>

    <h3>- DELETE information <a href="http://127.0.0.1:8080/api/v1/oracle/delete">http://127.0.0.1:8080/api/v1/oracle/delete</a></h3>
    <div style="font-family:Verdana;font-size:60%;background-color:gray;color:black;padding:10px;">
        <div style="background-color:white;color:black;padding:30px;">
            URL - <mark>http://127.0.0.1:8080/api/v1/oracle/delete</mark><br>
            Heards - <mark>{"Content-Type":"application/json"}</mark><br>
            Method - <mark>DELETE</mark><br>
            Body - <mark>{ "object": "F4101", "filter": [ { "operator": "=", "term1": "TAB.IMITM", "term2": 123 } ], "order": null, "data": null }</mark><br>
            <br>
            curl -X DELETE -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": [ { \"operator\": \"=\", \"term1\": \"TAB.IMITM\", \"term2\": 123 } ], \"order\": null, \"data\": null }" http://127.0.0.1:8080/api/v1/oracle/delete
        </div>
    </div>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))
