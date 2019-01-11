import sys
from db import DB


def update_admin(new_id, new_password):
    db = DB()
    TABLE_NAME = 'administrator'
    admin_info = db.get_table_tuple(TABLE_NAME)[0]
    old_id = admin_info[0]
    old_password = admin_info[1]
    # Update id
    conditions = {'id':old_id}
    column = 'id'
    db.update_field(TABLE_NAME, column, conditions, new_id)
    # Update password
    conditions = {'password':old_password}
    column = 'password'
    db.update_field(TABLE_NAME, column, conditions, new_password)
    print('idとpasswordを更新しました。')
    
args = sys.argv
if len(args) == 3:
    update_admin(args[1], args[2])
else:
    print("エラー：id、password、２つの引数が必要です。")