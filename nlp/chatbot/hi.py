import pymysql
import pandas as pd

db = None
try:
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='1234',
        db='mydb',
        charset='utf8'
    )

    print('DB 연결 성공')

    sql_create = '''
        CREATE TABLE tb_student (
            id int primary key auto_increment not null,
            name varchar(32),
            age int,
            address varchar(32)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    sql_insert = '''
        INSERT tb_student(name, age, address) values('hee', 20, 'Korea')
    '''

    id = 1
    sql_update = '''
        UPDATE tb_student SET name='새벽', age=30 WHERE id=%d
    ''' % id

    sql_delete = '''
        DELETE FROM tb_student WHERE id=%d
    ''' % id

    # with db.cursor() as cursor:
    # cursor.execute(sql_create)
    # cursor.execute(sql_insert)
    # cursor.execute(sql_update)
    # cursor.execute(sql_delete)
    # db.commit() # insert/update/delete 사용 => 즉, 수정시만 commit!


    students = [
        {'name': 'Kei', 'age': 36, 'address': '부산'},
        {'name': 'Tony', 'age': 34, 'address': '부산'},
        {'name': 'Jaeyoo', 'age': 39, 'address': '광주'},
        {'name': 'Grace', 'age': 28, 'address': '서울'},
        {'name': 'Jenny', 'age': 27, 'address': '서울'},
    ]

    for s in students:
        with db.cursor() as cursor:
            sql = '''
                INSERT tb_student(name, age, address) values('%s', %d, '%s')
            ''' % (s['name'], s['age'], s['address'])
            cursor.execute(sql)
    db.commit()

    cond_age = 30
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''
            SELECT * FROM tb_student WHERE age > %d
        ''' % cond_age
        cursor.execute(sql)
        results = cursor.fetchall()
    print(results)

    cond_name = 'Grace'
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''
            SELECT * FROM tb_student WHERE name = '%s'
        ''' % cond_name
        cursor.execute(sql)
        result = cursor.fetchone()
    print(result['name'], result['age'])

    df = pd.DataFrame(results)
    print(df)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 닫기 성공')