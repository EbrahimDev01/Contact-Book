from database_context import DatabaseContext


class ContactBookRepository:
    def __init__(self):
        self.database_name = 'contact_book_db'
        self.database_context = DatabaseContext(self.database_name)

    def get_all_contact_books(self):
        self.lock_tables(False, 'contact_book')
        sql_command = 'SELECT * FROM contact_book;'
        self.database_context.execute_database(sql_command)
        result = self.database_context.cursor.fetchall()
        self.unlock_table_contact_book()
        return result

    def delete_contact_by_id(self, contact_book_id):
        sql_command = '''
            DELETE 
                FROM 
                    contact_book 
            WHERE
                ContactBookID=%s           
        '''
        self.database_context.execute_database(sql_command, (contact_book_id,))
        self.database_context.commit_database()

    def search_contact_book(self, got_title='', got_group_name_id=None):
        got_title = got_title.replace(' ', '')
        self.lock_tables(False, 'contact_book', 'group_name')
        sql_command = '''
            SELECT 
                * 
            FROM
                contact_book
            WHERE              
                (REPLACE(FirstName, ' ', '') LIKE %s OR               
                REPLACE(LastName, ' ', '') LIKE %s OR                
                REPLACE(Email, ' ', '') LIKE %s OR 
                REPLACE(Email, ' ', '')  LIKE %s)
            '''
        got_title = '%' + got_title + '%'
        value = [got_title, got_title, got_title, got_title]

        if got_group_name_id is not None:
            sql_command += 'AND GroupNameID=%s;'
            value.append(got_group_name_id)

        self.database_context.execute_database(sql_command, value)
        result = self.database_context.fetchall()
        self.unlock_table_contact_book()
        return result

    def get_contact_book_by_id(self, item_id):
        self.lock_tables(False, 'contact_book')
        sql_command = '''
            SELECT
                *
            FROM
                contact_book
            WHERE
                ContactBookID=%s
        '''
        self.database_context.execute_database(sql_command, (item_id,))
        result = self.database_context.fetchone()
        self.unlock_table_contact_book()
        return result

    def get_contact_book_by_group_name_id(self, group_name_id):
        self.lock_tables(False, 'contact_book')
        sql_command = '''
               SELECT
                   *
               FROM
                   contact_book
               WHERE
                   GroupNameID=%s
           '''
        self.database_context.execute_database(sql_command, (group_name_id,))
        result = self.database_context.fetchall()
        self.unlock_table_contact_book()
        return result

    def insert_contact_book(self, got_first_name, got_last_name, got_phone_number, got_email, got_group_name_id):

        sql_command = '''
            INSERT INTO 
                contact_book
            VALUES (NULL, %s, %s, %s, %s, %s)
        '''
        self.lock_tables(True, 'contact_book')
        self.database_context.execute_database(sql_command, (got_first_name, got_last_name,
                                                             got_phone_number, got_email, got_group_name_id))
        self.database_context.commit_database()
        self.unlock_table_contact_book()

    def edit_contact_book(self, got_item_id, got_first_name, got_last_name, got_phone_number, got_email,
                          got_group_name_id):
        sql_command = '''
            UPDATE
                contact_book
            SET 
                FirstName=%s,
                LastName=%s ,
                PhoneNumber=%s,
                Email=%s ,
                GroupNameID=%s
            WHERE 
                ContactBookID=%s
        '''
        self.lock_tables(True, 'contact_book')
        self.database_context.execute_database(sql_command, (got_first_name, got_last_name, got_phone_number,
                                                             got_email, got_group_name_id, got_item_id))
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


def initialize_database():
    sql_command_create_tables = '''
        CREATE TABLE IF NOT EXISTS contact_book (
            ContactBookID INT NOT NULL AUTO_INCREMENT,
            FirstName VARCHAR(80),
            LastName VARCHAR(80),
            PhoneNumber VARCHAR(11),
            Email VARCHAR(200),
            GroupNameID INT,
            
            PRIMARY KEY (ContactBookID),
            FOREIGN KEY (GroupNameID) REFERENCES group_name(GroupNameID)                  
        );              
        CREATE TABLE IF NOT EXISTS group_name (
            GroupNameID INT NOT NULL AUTO_INCREMENT,
            GroupNameTitle VARCHAR(100),
                        
            PRIMARY KEY (GroupNameID)             
        );  
    '''
    database_context = DatabaseContext()
    database_context.create_database('contact_book_db')
    database_context.close_database()
    database_context = DatabaseContext('contact_book_db')
    database_context.execute_database(sql_command_create_tables, got_multi=True)
    database_context.close_database()


if __name__ == '__main__':
    contact_book_repository = ContactBookRepository()
    result_contact_book = contact_book_repository.search_contact_book('Ebrahim', None)
    print(result_contact_book)
    print(contact_book_repository.get_all_contact_books())
    print(contact_book_repository.get_all_group_names())
