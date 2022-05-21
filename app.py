from flask import Flask, render_template, request, redirect, url_for
import pymysql
db_connection = None
tb_cursor = None

#create object of Flask class
app = Flask(__name__)

# function to connect to databse
def connectToDb():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",user="root",
    passwd="",database="hotel_db",port=3306)
    if(db_connection):
        print("Done!!!")
    else:
        print("Not done")
    tb_cursor=db_connection.cursor()

# function to dicconnect from databse
def disconnectDb():
    db_connection.close()
    tb_cursor.close()

# function to get data from databse
def getAllCustomerData():
    connectToDb()
    selectQuery = "SELECT * FROM hotel_info;"
    tb_cursor.execute(selectQuery)
    allData = tb_cursor.fetchall()
    disconnectDb()
    return allData

#function to insert data into the table
def insertIntoTable(name,phone,checkin,checkout,address):
    connectToDb()
    inserQuery = "INSERT INTO hotel_info(NAME,PHONE,CHECKIN,CHECKOUT,ADDRESS) VALUES(%s, %s, %s, %s, %s);"
    tb_cursor.execute(inserQuery,(name,phone,checkin,checkout,address))
    db_connection.commit()
    disconnectDb()
    return True

# function to get data of one hotel from databse
def getCustomerID(customer_id):
    connectToDb()
    selectQuery = "SELECT * FROM hotel_info WHERE ID=%s;"
    tb_cursor.execute(selectQuery,(customer_id,))
    oneData = tb_cursor.fetchone()
    disconnectDb()
    return oneData

#function to update data into the table
def updateCustomerIntoTable(name,phone,checkin,checkout,address,id):
    connectToDb()
    updateQuery = "UPDATE hotel_info SET NAME=%s,PHONE=%s,CHECKIN=%s,CHECKOUT=%s,ADDRESS=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(name,phone,checkin,checkout,address,id))
    db_connection.commit()
    disconnectDb()
    return True

#function to update data into the table
def deleteCustomerFromTable(id):
    connectToDb()
    deleteQuery = "DELETE FROM hotel_info WHERE ID=%s;"
    tb_cursor.execute(deleteQuery,(id,))
    db_connection.commit()
    disconnectDb()
    return True



#a method that envoked at server execution
@app.route("/")
@app.route("/index/")
def index():
    #return "Hello flask"
    #return render_template("index.html")
    allData = getAllCustomerData()
    return render_template("index.html",data = allData)

@app.route("/add/",methods=["GET","POST"])
def addCustomer():
    if request.method == "POST":
        data = request.form
        isiInserted = insertIntoTable(data['txtName'],data['txtPhone'],data['txtcheckin'],data['txtcheckout'],data['txtAddress'])
        if(isiInserted):
            message = "Insertion sucess"
        else:
            message = "Insertion Error"
        return render_template("add.html",message = message)
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updateCustomer():
    id = request.args.get("ID",type=int,default=1)
    idData = getCustomerID(id)
    if request.method == "POST":
        data = request.form
        print(data)
        isUpdated = updateCustomerIntoTable(data['txtName'],data['txtPhone'],data['txtcheckin'],data['txtcheckout'],data['txtAddress'],id)
        if(isUpdated):
            message = "Updattion sucess"
        else:
            message = "Updattion Error"
        return render_template("update.html",message = message)
    return render_template("update.html",data=idData)

@app.route("/delete/")
def deleteCustomer():
    id = request.args.get("ID",type=int,default=1)
    deleteCustomerFromTable(id)
    return redirect(url_for("index"))


#to execute the code
if __name__=='__main__':
    app.run(debug=True)