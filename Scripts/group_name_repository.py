from database_context import DatabaseContext
from contact_book_repository import ContactBookRepository

database_context = DatabaseContext()
contact_book_repository = ContactBookRepository()


class GroupNameRepository:
    def __init__(self):
        self.database_name = 'contact_book_db'
        self.database_context = DatabaseContext(self.database_name)

    def get_all_group_names(self):
        self.lock_tables(False, 'group_name')
        sql_command = 'SELECT * FROM group_name;'
        self.database_context.execute_database(sql_command)
        result = self.database_context.cursor.fetchall()
        self.unlock_table_contact_book()
        return result

    def is_exists_by_title_and_id(self, got_group_name_title):
        got_group_name_title = got_group_name_title.replace(' ', '')
        self.lock_tables(False, 'group_name')
        sql_command = '''
        SELECT 
            * 
        FROM
            group_name
        WHERE              
            REPLACE(GroupNameTitle, ' ', '')=%s;'''

        self.database_context.execute_database(sql_command, (got_group_name_title,))
        result = self.database_context.fetchone() is not None
        self.unlock_table_contact_book()
        return result

    def search_group_name(self, got_group_name_title):
        got_group_name_title = got_group_name_title.replace(' ', '')
        self.lock_tables(False, 'group_name')
        sql_command = '''
                            SELECT 
                                * 
                            FROM
                                group_name
                            WHERE              
                                REPLACE(GroupNameTitle, ' ', '') LIKE %s;
                            '''
        got_group_name_title = '%' + got_group_name_title + '%'
        self.database_context.execute_database(sql_command, (got_group_name_title,))
        result = self.database_context.fetchall()
        self.unlock_table_contact_book()
        return result

    def delete_group_name_by_id(self, group_name_id):
        if len(contact_book_repository.get_contact_book_by_group_name_id(group_name_id)) > 0:
            return 'This group name is used for many contact books Try again after change group name'

        sql_command = '''
            DELETE 
                FROM 
                    group_name
            WHERE 
                GroupNameID=%s
        '''
        self.lock_tables(True, 'group_name')
        self.database_context.execute_database(sql_command, (group_name_id,))
        self.database_context.commit_database()
        self.unlock_table_contact_book()

    def get_group_name_by_id(self, group_name_id):
        self.lock_tables(False, 'group_name')
        sql_command = '''
        SELECT 
            * 
        FROM 
            group_name
        WHERE 
            GroupNameID=%s;
        '''
        self.database_context.execute_database(sql_command, (group_name_id,))
        result = self.database_context.cursor.fetchone()
        self.unlock_table_contact_book()
        return result

    def add_group_name(self, group_name_title):
        sql_command = '''
            INSERT INTO 
                    group_name
            VALUES
                (Null, %s)
        '''
        self.lock_tables(True, 'group_name')
        self.database_context.execute_database(sql_command, (group_name_title,))
        self.database_context.commit_database()
        self.unlock_table_contact_book()

    def edit_group_name(self, group_name_title, group_name_id):
        sql_command = '''
            UPDATE
                group_name
            SET
                GroupNameTitle=%s
            WHERE
                GroupNameID=%s
        '''
        self.lock_tables(True, 'group_name')
        self.database_context.execute_database(sql_command, (group_name_title, group_name_id,))
        self.database_context.commit_database()
        self.unlock_table_contact_book()

    def lock_tables(self, write: bool, *args):
        sql_command = 'LOCK TABLES '
        for table_name in args:
            sql_command += table_name + f" {'WRITE' if write else 'READ'},"
        sql_command = sql_command[:-1] + ';'

        self.database_context.execute_database(sql_command)

    def unlock_table_contact_book(self):
        sql_command = 'UNLOCK TABLES'
        self.database_context.execute_database(sql_command)
