from flask import Flask, g, request,jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
        host="host.docker.internal",
        user="mk",
        password="midhun@2002",
        port = 3306
        )
        with g.db.cursor() as curr:
            curr.execute("use proj;")
        return g.db
    
    else:
        return g.db
    
def execute_procedure(proc,*args, has_crud = False):
    try:
        mydb = get_db()
        with mydb.cursor() as curr:
            curr.callproc(proc,args)
            if has_crud:
                mydb.commit()
            if proc == "GetCustomer":
                res = next(curr.stored_results())
                result = res.fetchall()
                return result
        return {}

    except Exception as e:
        print("an exception occured:")
        s = f"%s: %s" % (type(e).__name__,e)
        print(s)
        return {"error_type" : type(e).__name__, "error" : str(e)}

@app.route("/api/customer", methods=["GET","POST","DELETE","PUT"])
def customer_table_apis():
    if request.method == 'GET':
        data = request.get_json()
        c_id = data['customer_id']
        data = execute_procedure('GetCustomer',c_id)
        if "error_type" not in data:
            return jsonify({"datas":data})
    elif request.method == 'POST':
        data = request.get_json()
        c_id = data['customer_id']
        c_name = data['customer_name']
        c_type = data['customer_type']
        dt = data['datetime']
        data = execute_procedure('CreateCustomer',c_id,c_name,c_type,dt,has_crud=True)
        if "error_type" not in data:
            return jsonify({'message':f'Customer Created succesfully'})
    elif request.method == 'DELETE':
        data = request.get_json()
        c_id = data['customer_id']
        data = execute_procedure('DeleteCustomer',c_id,has_crud=True)
        if "error_type" not in data:
            return jsonify({'message':f'Customer Deleted succesfully'})
        print(data)
    elif request.method == 'PUT':
        data = request.get_json()
        r_id = data['reference_id']
        c_id = data['customer_id']
        c_name = data['customer_name']
        c_type = data['customer_type']
        dt = data['datetime']
        data = execute_procedure('UpdateCustomer',r_id,c_id,c_name,c_type,dt,has_crud=True)
        if "error_type" not in data:
            return jsonify({'message':f'Customer Updated succesfully'})
    print(data)
    return jsonify(data)
