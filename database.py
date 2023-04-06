import pypyodbc

class DataBase:
        def __init__(self,studentNo, name, lastName, bornDate, clas, gender):
            self.studentNo = studentNo
            self.name = name
            self.lastName = lastName
            self.bornDate = bornDate
            self.clas = clas
            self.gender = gender

            self.conn = pypyodbc.connect(
            'Driver={SQL Server};'
            'Server=DESKTOP-9NMO9KA;'
            'Database=ogrenciKayit;'
            'Trusted_Connection=True;')

        def add_Student(self):
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM Student WHERE StudentNo=?", (self.studentNo,))
                row = cursor.fetchone() #mevcut konumda bir kayıt varsa, bu kaydı bir tuple olarak döndürür ve cursor konumunu bir sonraki kayda taşır. 
                if row[0] > 0:
                    print("-----------------------------------------------------------")
                else:
                    cursor.execute("INSERT INTO Student (StudentNo, Name, Surname, BornTime, Class, Gender) VALUES (?, ?, ?, ?, ?, ?)", 
                    (self.studentNo, self.name, self.lastName, self.bornDate, self.clas, self.gender))
                    self.conn.commit()
                    print("Öğrenci başarıyla eklendi!")
                    self.showStudent()
            except pypyodbc.Error as e:
                print("hata : ", e)
            finally:
                self.conn.close()
        
        def showStudent(self):
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM Student')
            students = cursor.fetchall()
            for student in students:
                print(student)
