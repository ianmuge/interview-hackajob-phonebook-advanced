from flask import Flask,jsonify,Response,make_response,render_template,request
import requests,traceback, os,sqlite3 as sql,logging

app = Flask(__name__)
database_loc="./phonebook.db"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
init=False

def initialize():
    try:
        if os.path.exists(database_loc):
            os.remove(database_loc)
            print("Database Removed")
        conn=sql.connect(database_loc)
        print("Database created")
        conn.execute("CREATE TABLE  IF NOT EXISTS contacts"
                     "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "name TEXT, "
                     "address TEXT, "
                     "phonenumber TEXT)")
        print("Table created")
        datasource_url = "http://www.mocky.io/v2/581335f71000004204abaf83"
        x = requests.get(datasource_url)
        init_contacts = x.json()
        cur = conn.cursor()
        for cont in init_contacts["contacts"]:
            cur.execute("INSERT INTO contacts "
                        "(name,address,phonenumber) "
                        "VALUES(?, ?, ?)",
                        (cont["name"],cont["address"],cont["phone_number"])
                        )
        conn.commit()
        print("Records successfully added")
        conn.close()
    except Exception as exc:
        logger.exception(exc)


if init:
    app.before_first_request(initialize)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as exc:
        logger.exception(exc)
        return "Exception Raised: {0}".format(exc)

@app.route("/contacts",methods=["GET"])
def get_contacts():
    try:
        conn=sql.connect(database_loc)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("select * from contacts;")
        rows = cur.fetchall()
        res = {
            "data": rows,
            "code": 1,
            "msg": "Loaded Successfully"
        }
    except Exception as exc:
        logger.exception(exc)
        res = {
            "data": "",
            "code": 0,
            "msg": "Exception Raised: {0}".format(exc)
        }
    finally:
        conn.close()
        return jsonify(res)
@app.route("/contacts/<id>",methods=["GET"])
def get_contact(id):
    try:
        conn=sql.connect(database_loc)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("select * from contacts where id=?;",[id])
        rows = cur.fetchone()
        res = {
            "data": rows,
            "code": 1,
            "msg": "Loaded Successfully"
        }
    except Exception as exc:
        logger.exception(exc)
        res = {
            "data": "",
            "code": 0,
            "msg": "Exception Raised: {0}".format(exc)
        }
    finally:
        conn.close()
        return jsonify(res)


@app.route("/contacts",methods=["POST"])
def create_contact():
    conn = sql.connect(database_loc)
    try:
        name = request.form["name"]
        address = request.form["address"]
        phonenumber = request.form["phonenumber"]
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts "
                    "(name,address,phonenumber)"
                    "VALUES(?, ?, ?);",
                    [name,address,phonenumber])
        conn.commit()
        row={
            "id":cur.lastrowid,
            "name":name,
            "address":address,
            "phonenumber":phonenumber
        }
        res = {
            "data": row,
            "code": 1,
            "msg": "Added Successfully"
        }
    except Exception as exc:
        logger.exception(exc)
        res = {
            "data": "",
            "code": 0,
            "msg": "Exception Raised: {0}".format(exc)
        }
    finally:
        conn.close()
        return res


@app.route("/contacts",methods=["PUT"])
def update_contact():
    conn = sql.connect(database_loc)
    try:
        id=request.form["edit_id"]
        name = request.form["name"]
        address = request.form["address"]
        phonenumber = request.form["phonenumber"]

        cur = conn.cursor()
        cur.execute("UPDATE contacts set "
                    "name=?,address=?,phonenumber=? "
                    "where id=?;",
                    [name, address, phonenumber,id])
        conn.commit()
        res = {
            "data": "",
            "code": 1,
            "msg": "Updated Successfully"
        }
    except Exception as exc:
        logger.exception(exc)
        res = {
            "data": "",
            "code": 0,
            "msg": "Exception Raised: {0}".format(exc)
        }
    finally:
        conn.close()
        return res


@app.route("/contacts",methods=["DELETE"])
def delete_contact():
    conn = sql.connect(database_loc)
    try:
        id = request.form["id"]
        cur = conn.cursor()
        cur.execute("DELETE FROM contacts WHERE id=?;",[id])
        conn.commit()
        res = {
            "data": "",
            "code": 1,
            "msg": "Deleted Successfully"
        }
    except Exception as exc:
        logger.exception(exc)
        res = {
            "data": "",
            "code": 0,
            "msg": "Exception Raised: {0}".format(exc)
        }
    finally:
        conn.close()
        return res


if __name__ == "__main__":
    app.run(debug=True)
