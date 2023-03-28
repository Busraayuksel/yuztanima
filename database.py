import pypyodbc

class DataBase:
        def __init__(self,studentNo, name, lastName, bornDate, clas):
            self.studentNo = studentNo
            self.name = name
            self.lastName = lastName
            self.bornDate = bornDate
            self.clas = clas

        def add_Student(self):
            conn = pypyodbc.connect(
            'Driver={SQL Server};'
            'Server=DESKTOP-9NMO9KA;'
            'Database=ogrenciKayit;'
            'Trusted_Connection=True;')

            cursor = conn.cursor()

            try:
                cursor.execute("SELECT COUNT(*) FROM Student WHERE StudentNo=?", (self.studentNo))
                row = cursor.fetchone() #mevcut konumda bir kayıt varsa, bu kaydı bir tuple olarak döndürür ve cursor konumunu bir sonraki kayda taşır. 
                if row[0] > 0:
                    return
                cursor.execute("INSERT INTO Student (StudentNo, Name, Surname, BornTime, Class) VALUES (?, ?, ?, ?, ?)", 
                (self.studentNo, self.name, self.lastName, self.bornDate, self.clas))
                conn.commit()
                print("Öğrenci başarıyla eklendi!")
            except pypyodbc.Error as ex:
                print("Sorgu hatası: ", ex)
            finally:
                conn.close()
