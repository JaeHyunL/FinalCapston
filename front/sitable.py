import bcrypt
from database import Database


class Signdatabase(Database):
    def insert_studentInfo(self, stuend_no, pw, user_name, student_ID):

        sql = "INSERT INTO info(student_no,pw,user_name,student_ID)"
        sql += " VALUES('{}','{}','{}','{}');".format(stuend_no,
                                                      pw, user_name, student_ID)

        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error": "{}".format(e)}

        return result

    def auth(self, id, passwd):
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
        return result
