import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

# cursor.execute("""CREATE TABLE students(
#         name text,
#         admission_number integer,
#         class text,
#         second_language text,
#         nationality text,
#         gender text,
#         religion text,
#         father_name text,
#         mother_name text,
#         phone integer,
#         adress,
#         term_1_fees text,
#         term_2_fees text,
#         id_card_fee text,
#         tutition_fees text,
#         transportation_fees text,
#         fees_amount_to_be_paid integer)
#         """)

# cursor.execute("""INSERT INTO students VALUES (
#                     'Mohammed Abdullah Amaan',
#                     353,
#                     '11-B',
#                     'urdu',
#                     'Indian',
#                     'Male',
#                     'Islam',
#                     'Mohammed Ayyub Sayeed',
#                     'Amena Tabassum',
#                     33543497,
#                     'Al-mansoura, doha-qatar',
#                     'paid',
#                     'not paid',
#                     'paid',
#                     'paid',
#                     'not paid',
#                     350
#                 )
#                 """)

                
# cursor.execute("DROP TABLE students")

cursor.execute("SELECT * FROM students WHERE admission_number=353")
print(cursor.fetchone())
connection.commit()
connection.close()