from database import Database


class CRUDdatabase(Database):

    """DB 이미지 가져오기 """

    def get_Image(self, no):

        sql = "SELECT image_file_str "
        sql += "FROM student "
        sql += "WHERE user_no={};".format(no)
        result = {}
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            return("error : {}".format(e))
        result = {} if len(result) == 0 else result[0]

        return result

    """DB 이미지 저장 """

    def insert_Image(self, img_str):

        sql = "INSERT INTO student(image_file_str)"
        sql += " VALUES('{}');".format(img_str)
        print(sql)
        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error": "{}".format(e)}

        return result

    def insert_FaceDifference(self, characteristic):

        sql = "INSERT INTO student(student_characteristic)"
        sql += " values('{}');".format(characteristic)
        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error": "{}".format(e)}

        return result

    def login(self, id, passwd):
        sql = "SELECT student_ID,pw "
        sql += "FROM info "
        sql += "WHERE student_ID='{}';".format(id)
        result = False
        try:
            onerow = self.executeOne(sql)
            if passwd == onerow.get('pw'):
                result = True

        except Exception as e:
            return {"error": "{}".format(e)}
        print(result)
        return result
