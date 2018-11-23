from flask import Flask, request, redirect, render_template
from db import DB
import mkqrcode

app = Flask(__name__)
app.config['DEBUG'] = True
@app.route('/')
def index():
    s = "/static/QRcode.png"
    return render_template('index.html', s=s)
 
@app.route('/authQRcode')
def authQRcode():
    if request.method == 'POST':
        result = request.form
        base64 = result['base64']
        print(base64)
        return render_template('index.html')

@app.route('/showQRcode', methods = ['POST'])
def showQRcode():
    if request.method == 'POST':
        db = DB()
        student_num = request.form['student-num']
        conditions = {'student_num':student_num}
        if not db.get_field('students', 'student_num', conditions):
            qrcode_file = None
            error = '学籍番号が存在しません。登録ページから登録してください。'
        else:
            qrcode_file = '/static/QRcode/' + str(student_num) + '.png'
            error = None
        print(qrcode_file)
        return render_template('index.html', qrcode = qrcode_file, error = error)

@app.route('/confirm', methods = ['POST'])
def confirm():
    if request.method == 'POST':
        db = DB()
        result = request.form
        kj_fam_name = result['kj_fam_name']
        kj_fir_name = result['kj_fir_name']
        ka_fam_name = result['ka_fam_name']
        ka_fir_name = result['ka_fir_name']
        student_num = result['student_num']
        student_num = student_num[:student_num.find('@')]
        conditions = {'student_num':student_num}
        if not db.get_field('students', 'student_num', conditions):
            s_num_hash = mkqrcode.get_hash(student_num)
            mkqrcode.makeQRcode(student_num, s_num_hash)
            values = [student_num, s_num_hash, kj_fam_name, kj_fir_name, ka_fam_name, ka_fir_name]
            db.insert_record('students', values)
        return redirect("http://127.0.0.1:5500/index.html", '301')

if __name__ == '__main__':
    app.run()
