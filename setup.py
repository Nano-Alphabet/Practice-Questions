import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = "MyGalaxy"
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Practice-Questions.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Practice Questions").sheet1
sh = client.open("Practice Questions").get_worksheet(1)

@app.route("/")
def HelloWorld():
    hi = sheet.get_all_records()
    return render_template('exp.html', items=hi)


@app.route("/Home", methods=['GET', 'POST'])
def home():
    hi = sheet.get_all_records()
    if request.method == 'POST':
        Exp = request.form.get('experiment_name')
        if Exp=="":
            return render_template("error.html")
        Ar = [int(x.get("id")) for x in hi]
        try:
            I = max(Ar)+1
        except:
            I=1
        row = [I, Exp]
        sheet.append_row(row)
    hi = sheet.get_all_records()
    return render_template('exp.html', items=hi)

@app.route("/experiments/<int:exp_id>/", methods=['GET', 'POST'])
def AddItems(exp_id):
    item = sh.get_all_records()
    if request.method=='POST':
        Question=request.form.get('question')
        Answer=request.form.get('answer')
        if Question=="":
            return render_template("error.html")
        Ar = [int(x.get("id")) for x in item]
        try:
            I = max(Ar)+1
        except:
            I=1
        row = [I, Question, Answer, exp_id]
        sh.append_row(row)
    item = sh.get_all_records()
    Ar=[]
    for i in item:
        if i.get("exp_id")==exp_id:
            Ar.append(i)
    return render_template('index.html', items=Ar, id=exp_id)
@app.route("/edit_item/<int:exp_id>/<int:item_id>/", methods=['GET', 'POST'])
def edit_item(exp_id,item_id):
    if (request.method == 'POST'):
        Answer = request.form.get('answer')
        if Answer=="":
            return render_template("error.html")
        item = sh.get_all_records()
        for i in range(len(item)):
            if item[i].get("id") == item_id:
                sh.update_cell(i+2, 3, Answer)
    item = sh.get_all_records()
    Ar = []
    for i in item:
        if i.get("exp_id") == exp_id:
            Ar.append(i)
    return render_template('index.html', items=Ar, id=exp_id)
