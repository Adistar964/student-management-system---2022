import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE students")
connection.commit()

cursor.execute("""CREATE TABLE students(
        admission_number INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        class text,
        roll_number text,
        second_language text,
        nationality text,
        gender text,
        religion text,
        father_name text,
        mother_name text,
        phone text,
        email text,
        address,
        term_1_fees text,
        term_2_fees text,
        id_card_fee text,
        tutition_fees text,
        transportation_fees text,
        fees_amount_to_be_paid text)
        """)

cursor.execute("""INSERT INTO students VALUES (
                        NULL,
                    'Mohammed Ali',
                    '11-B',
                    '2',
                    'urdu',
                    'Indian',
                    'Male',
                    'Islam',
                    'Mohammed Ayyub Sayeed',
                    'Amena Tabassum',
                    '+974 33543497',
                    'test@gmail.com'
                    'Al-mansoura, doha-qatar',
                    'paid',
                    'not paid',
                    'paid',
                    'paid',
                    'not paid',
                    'QAR. 350'
                )
                """)
connection.commit()
                
cursor.execute("SELECT * FROM students")
print(cursor.fetchall())
connection.commit()
connection.close()