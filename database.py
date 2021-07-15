import pymysql

#проверка создания таблицы. В случай ее отсутствия создание ее.
def connect():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            # cursor = connection.cursor()

            with connection.cursor() as cursor:
                create_table_query = "CREATE TABLE IF NOT EXISTS `main_info_about_users`(id INT," \
                                     "name TEXT, lastname TEXT, users_status TEXT, buying_time TEXT, " \
                                     "number_of_trail_time_usages INT, " \
                                     "last_use TEXT, number_of_usages INT, PRIMARY KEY (id));"
                cursor.execute(create_table_query)

                print("Table created successfully")



        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#регистрация пользователя при первом использовании
def registration_user(id, name, lastname):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Successfully connected...")
        print("#" * 20)

        try:

            with connection.cursor() as cursor:
                values = (id, name, lastname, '0', '-', 15, '-', 0)
                #users_status = 0 - пользователь с бесплатной версией
                #users_status = 1 - пользователь с пробной версией
                #users_status = 2 - пользователь с платной версией
                insert_query = "INSERT INTO registration_table (id, name, lastname, users_status, buying_time, " \
                               "number_of_trail_time_usages, last_use, number_of_usages VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_query, values)
                connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка id
def select_id():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                id = []
                select_id = "SELECT id FROM main_info_about_users"
                cursor.execute(select_id)
                rows_id = cursor.fetchall()
                len_id = len(rows_id)
                for i in range(len_id):
                    id.append(rows_id[i]['id'])
                return id

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка имени по id
def select_name(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                name = []
                values = (id, )
                select_name = "SELECT name FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_name, values)
                rows_name = cursor.fetchall()
                len_name = len(rows_name)
                for i in range(len_name):
                    name.append(rows_name[i]['name'])
                return name

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка фамилии по id
def select_lastname(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                lastname = []
                values = (id, )
                select_lastname = "SELECT lastname FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_lastname, values)
                rows_lastname = cursor.fetchall()
                len_lastname = len(rows_lastname)
                for i in range(len_lastname):
                    lastname.append(rows_lastname[i]['lastname'])
                return lastname

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка статуса пользователя по id
def select_users_status(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                users_status = []
                values = (id, )
                select_users_status = "SELECT users_status FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_users_status, values)
                rows_users_status = cursor.fetchall()
                len_users_status = len(rows_users_status)
                for i in range(len_users_status):
                    users_status.append(rows_users_status[i]['users_status'])
                return users_status

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка времени покупки по id
def select_buying_time(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                users_buying_time = []
                values = (id, )
                select_buying_time = "SELECT buying_time FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_buying_time, values)
                rows_buying_time = cursor.fetchall()
                len_buying_time = len(rows_buying_time)
                for i in range(len_buying_time):
                    users_buying_time.append(rows_buying_time[i]['buying_time'])
                return users_buying_time

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка колличество тестовых использований по id
def select_number_of_trail_time_usages(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                number_of_trail_time_usages = []
                values = (id, )
                select_number_of_trail_time_usages = "SELECT number_of_trail_time_usages FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_number_of_trail_time_usages, values)
                rows_number_of_trail_time_usages = cursor.fetchall()
                len_number_of_trail_time_usages = len(rows_number_of_trail_time_usages)
                for i in range(len_number_of_trail_time_usages):
                    number_of_trail_time_usages.append(rows_number_of_trail_time_usages[i]['number_of_trail_time_usages'])
                return number_of_trail_time_usages

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка последнего использования по id
def select_last_use(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                last_use = []
                values = (id, )
                select_last_use = "SELECT last_use FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_last_use, values)
                rows_last_use = cursor.fetchall()
                len_last_use = len(rows_last_use)
                for i in range(len_last_use):
                    last_use.append(rows_last_use[i]['last_use'])
                return last_use

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

#выборка колличества использований по id
def select_number_of_usages(id):

    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="soldan1512",
            database="base_for_video_maker",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            # insert data

            with connection.cursor() as cursor:
                number_of_usages = []
                values = (id, )
                select_number_of_usages = "SELECT number_of_usages FROM main_info_about_users WHERE id = %s"
                cursor.execute(select_number_of_usages, values)
                rows_number_of_usages = cursor.fetchall()
                len_number_of_usages = len(rows_number_of_usages)
                for i in range(len_number_of_usages):
                    number_of_usages.append(rows_number_of_usages[i]['number_of_usages'])
                return number_of_usages

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)




connect()