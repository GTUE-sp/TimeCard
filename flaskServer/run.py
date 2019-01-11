import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, redirect, render_template
from db import DB
import mkqrcode
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authAdmin', methods = ['POST'])
def authAdmin():
    if request.method == 'POST':
        db = DB()
        result = request.form
        id = result['admin_id']
        password = result['admin_password']
        conditions = {'id':id, 'password':password}
        if db.get_field('administrator', 'id', conditions):
            message = ''
            auth_history = db.get_table_tuple('authHistory') 
            auth_history_text = """
                <table>
                    <thead>
                        <tr>
                            <th>日付時間</th>
                            <th>名前</th>
                            <th>写真</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for line in auth_history:
                auth_history_text += '<tr><td>' + line[0] + '</td><td>' + line[1] + '</td><td><img src="../static/Face/' + line[0] + '.png"></td></tr>'
            auth_history_text += """
                    </tbody>
                </table>
            """
        else:
            message = 'ログインに失敗しました'
            auth_history_text = None
        return render_template('admin.html', message = message, authHistory = auth_history_text)

@app.route('/registry')
def registry():
    return render_template('registry.html')

@app.route('/authQRcode', methods=['POST'])
def authQRcode():
    qrcode_data = request.form['qrcodeData']
    db = DB()
    conditions = {'hash':qrcode_data}
    if not db.get_field('students', 'student_num', conditions):
        result = '有効なQRコードではありません。'
    else:
        dt_now = str(datetime.datetime.now())
        enc_data  = request.form['base64']
        dec_data = base64.b64decode(enc_data.split(',')[1])#環境依存の様(","で区切って本体をdecode)
        dec_img  = Image.open(BytesIO(dec_data))
        dec_img.save('./static/Face/' + dt_now + '.png', 'png')
        values = [dt_now, db.get_field('students', 'kj_family_name', conditions) + db.get_field('students', 'kj_first_name', conditions) ]
        db.insert_record('authHistory', values)
        result = '認証に成功しました。'
    print(qrcode_data)
    return render_template('authResult.html', result = result)

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
        conditions = {'student_num':student_num}
        print(db.get_field('students', 'student_num', conditions))
        if not db.get_field('students', 'student_num', conditions):
            s_num_hash = mkqrcode.get_hash(student_num)
            mkqrcode.makeQRcode(student_num, s_num_hash)
            values = [student_num, s_num_hash, kj_fam_name, kj_fir_name, ka_fam_name, ka_fir_name]
            db.insert_record('students', values)
            message = "新規登録に成功しました。"
        else:
            message = "既に登録されている学籍番号です"
        
        return render_template('registry.html', message = message)

if __name__ == '__main__':
    app.run()
