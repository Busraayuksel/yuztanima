import pypyodbc

class DataBase:
        def __init__(self):
            # self.studentNo = studentNo
            # self.name = name
            # self.lastName = lastName
            # self.bornDate = bornDate
            # self.clas = clas
            # self.gender = gender

            self.conn = pypyodbc.connect(
            'Driver={SQL Server};'
            'Server=DESKTOP-9NMO9KA;'
            'Database=ogrenciKayit;'
            'Trusted_Connection=True;')

            self.cursor = self.conn.cursor()

        def add_Student(self, studentNo, name, lastName, bornDate, clas, gender):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM Student WHERE StudentNo=?", (studentNo,))
                row = self.cursor.fetchone() #mevcut konumda bir kayıt varsa, bu kaydı bir tuple olarak döndürür ve cursor konumunu bir sonraki kayda taşır. 
                if row[0] > 0:
                    print("kayıtlı kullanıcı")
                else:
                    self.cursor.execute("INSERT INTO Student (StudentNo, Name, Surname, BornTime, Class, Gender) VALUES (?, ?, ?, ?, ?, ?)", 
                    (studentNo, name, lastName, bornDate, clas, gender))
                    self.conn.commit()
                    print("Öğrenci başarıyla eklendi!")
                    self.showStudent()
            except pypyodbc.Error as e:
                print("hata : ", e)
            finally:
                self.conn.close()
        
        def showStudent(self):
            self.cursor.execute('SELECT * FROM Student')
            students = self.cursor.fetchall()
            for student in students:
                print(student)

        def control(self, no):
            self.cursor.execute("SELECT COUNT(*) FROM Student WHERE StudentNo=?", (no,))
            var = self.cursor.fetchone()
            if var[0] > 0 :
                print("var bu kişi")
                return True
