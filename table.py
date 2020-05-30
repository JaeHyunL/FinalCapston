from database import Database


class CRUDdatabase(Database):
    """DB 이미지 가져오기 """
    def getImage(self, no):

        sql = "SELECT image_file_str "
        sql += "FROM images "
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
    def insertImage(self, img_str):

        sql = "INSERT INTO images(image_file_str) "
        sql += "values ('{}');".format(img_str)
        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error": "{}".format(e)}

        return result
