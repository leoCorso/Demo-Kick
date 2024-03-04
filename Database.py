import copy
import datetime
import os.path
import random
import sqlite3
import threading
import time
from queue import Queue


class ConnectionPool:
    _instance_lock = threading.Lock()

    def __init__(self):
        self.max_connections = 5
        self.database = 'Demo Kick.db'
        self.connections = Queue(maxsize=self.max_connections)

        for _ in range(self.max_connections):
            connection = sqlite3.connect(self.database)
            self.connections.put(connection)

    def get_connection(self):
        return self.connections.get()

    def release_connection(self, connection):
        self.connections.put(connection)


class Database:
    thread_lock = threading.Lock()

    def __init__(self):
        self.connection_pool = ConnectionPool()

        self.check_if_tables_exist()

    def execute_query(self, query, fetch_type, values):
        # Executes a query statement of the specified fetch type using a connection from connection pool
        done = False
        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()
                    with self.thread_lock:  # Locks
                        if values:  # If values are passed in the values list
                            return_values = cursor.execute(query, values)
                        else:
                            return_values = cursor.execute(query, ())

                        if fetch_type == 'fetchone':
                            return_values = return_values.fetchone()
                        elif fetch_type == 'fetchall':
                            return_values = return_values.fetchall()
                        done = True
                        return return_values
                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
                    else:
                        raise
        finally:
            self.connection_pool.release_connection(connection)

    def execute_thread_safe_query(self, query, fetch_type, values):
        # Executes a query statement of the specified fetch type using a connection from connection pool
        done = False
        try:
            connection = sqlite3.connect('Demo Kick.db')
            while not done:
                try:
                    cursor = connection.cursor()

                    with self.thread_lock:  # Locks

                        if values:  # If values are passed in the values list
                            return_values = cursor.execute(query, values)
                        else:
                            return_values = cursor.execute(query, ())

                        if fetch_type == 'fetchone':
                            return_values = return_values.fetchone()
                        elif fetch_type == 'fetchall':
                            return_values = return_values.fetchall()
                        done = True
                        return return_values
                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
                    else:
                        raise Error
        finally:
            connection.close()

    def execute_thread_safe_update(self, statement, values):
        done = False

        try:
            connection = sqlite3.connect('Demo Kick.db')

            while not done:
                try:
                    with self.thread_lock:
                        cursor = connection.cursor()
                        if values:
                            cursor.execute(statement, values)

                        else:
                            cursor.execute(statement, ())
                        connection.commit()
                        done = True
                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
        finally:
            connection.close()

    def execute_insert(self, insert, values):

        # Executes a insert statement using a connection from connection pool
        done = False
        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()

                    with self.thread_lock:  # Locks thread lock before executing code below. Means only one thread
                        # can execute the code below at a time
                        if values is not None:
                            cursor.execute(insert, values)

                        else:
                            cursor.execute(insert, ())

                        connection.commit()
                        done = True

                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        if str(Error) == 'database is locked':
                            print(f'DB LOCKED WAITING ONE SECOND {Error}')
                            time.sleep(1)
        finally:
            self.connection_pool.release_connection(connection)

    def execute_many_inserts(self, statement, values):

        # Will use statement template with ? binding
        # Uses values list of tuples which will execute insert for each element tuple in list

        done = False
        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()
                    with self.thread_lock:
                        cursor.executemany(statement, values)
                        connection.commit()
                    done = True
                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
        finally:
            self.connection_pool.release_connection(connection)

    def execute_many_inserts_thread_safe_w_id(self, statement, values):

        # Will use statement template with ? binding
        # Uses values list of tuples which will execute insert for each element tuple in list
        done = False

        try:
            connection = sqlite3.connect('Demo Kick.db')
            while not done:
                try:
                    cursor = connection.cursor()
                    transaction_ids = []

                    with self.thread_lock:
                        for value in values:
                            cursor.execute(statement, value)
                            transaction_ids.append(cursor.lastrowid)

                            connection.commit()
                    done = True
                    return transaction_ids
                except sqlite3.OperationalError as Error:  # If database is locked wait one second
                    if str(Error) == ': database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
                    else:
                        print(f'Error: {Error}')
        finally:
            cursor.close()

    def execute_many_inserts_thread_safe_no_id(self, statement, values):

        # Will use statement template with ? binding
        # Uses values list of tuples which will execute insert for each element tuple in list
        # Does not return a transaction id
        done = False

        try:
            connection = sqlite3.connect('Demo Kick.db')
            while not done:
                try:
                    cursor = connection.cursor()
                    transaction_ids = []

                    with self.thread_lock:
                        cursor.executemany(statement, values)
                        connection.commit()
                    done = True
                except sqlite3.OperationalError as Error:  # If database is locked wait one second
                    if str(Error) == ': database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
        finally:
            cursor.close()

    def execute_update(self, statement, values):
        done = False

        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()
                    if values:
                        cursor.execute(statement, values)

                    else:
                        cursor.execute(statement, ())
                    connection.commit()
                    done = True
                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print(f'DB LOCKED WAITING ONE SECOND {Error}')
                        time.sleep(1)
                    else:
                        raise Error
        finally:
            self.connection_pool.release_connection(connection)

    def create_table(self, statement, values):

        # Executes a table creation statement using a connection from connection pool
        done = False
        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()

                    with self.thread_lock:
                        if values:
                            cursor.execute(statement, values)
                        else:
                            cursor.execute(statement)
                    done = True

                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print('DB LOCKED WAITING ONE SECOND')
                        time.sleep(1)
        finally:
            self.connection_pool.release_connection(connection)

    def execute_delete(self, statement, values):

        # Executes a delete statement using a connection from connection pool
        done = False

        try:
            connection = self.connection_pool.get_connection()
            while not done:
                try:
                    cursor = connection.cursor()

                    if values:
                        cursor.execute(statement, values)
                    else:
                        cursor.execute(statement)
                    connection.commit()
                    done = True

                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print('DB LOCKED WAITING ONE SECOND')
                        time.sleep(1)
        finally:
            self.connection_pool.release_connection(connection)

    def execute_delete_many_thread_safe(self, statement, values):

        done = False

        try:
            connection = sqlite3.connect('Demo Kick.db')
            while not done:
                try:
                    cursor = connection.cursor()
                    if values:
                        cursor.executemany(statement, values)
                    else:
                        cursor.executemany(statement, values)
                    connection.commit()
                    done = True

                except sqlite3.OperationalError as Error:
                    if str(Error) == 'database is locked':
                        print('DB LOCKED WAITING ONE SECOND')
                        time.sleep(1)
        finally:
            cursor.close()

    def check_if_tables_exist(self):

        # Checks if the database table structure exists and creates the needed table if not

        try:
            self.execute_query('SELECT COUNT(transaction_id) FROM archived_transactions;', 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            statement = F"""
                CREATE TABLE "archived_transactions" (
                    "transaction_id"	INTEGER NOT NULL UNIQUE,
                    "contact_id"	INTEGER NOT NULL,
                    "from_email"	TEXT NOT NULL,
                    "subject_line"	TEXT,
                    "body"	TEXT,
                    "send_date"	datetime,
                    "failed"	bit DEFAULT 0,
                    FOREIGN KEY("contact_id") REFERENCES "contacts"("contact_id"),
                    FOREIGN KEY("from_email") REFERENCES "from_emails"("from_email_id"),
                    PRIMARY KEY("transaction_id" AUTOINCREMENT)
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query('SELECT COUNT(attachment_id) FROM archived_attachments;', 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            statement = F"""
                    CREATE TABLE "archived_attachments" (
                        "attachment_id"	INTEGER NOT NULL UNIQUE,
                        "attachment_name"	TEXT NOT NULL,
                        "attachment_path"	TEXT NOT NULL,
                        PRIMARY KEY("attachment_id" AUTOINCREMENT)
                    );
            """
            self.create_table(statement, None)

        try:
            self.execute_query('SELECT COUNT(*) FROM archived_attachment_transaction_associations;', 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            statement = F"""
                CREATE TABLE "archived_attachment_transaction_associations" (
                    "transaction_id"	INTEGER NOT NULL,
                    "attachment_id"	INTEGER NOT NULL,
                    FOREIGN KEY("transaction_id") REFERENCES "archived_transactions"("transaction_id"),
                    FOREIGN KEY("attachment_id") REFERENCES "attachments"("attachment_id"),
                    PRIMARY KEY("transaction_id","attachment_id")
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query("SELECT COUNT(contact_id) FROM contacts", 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            print('CREATING TABLE contacts')
            statement = """
                CREATE TABLE "contacts" (
                    "contact_id"	INTEGER NOT NULL UNIQUE,
                    "official_name"	TEXT NOT NULL,
                    "country"	TEXT,
                    "instagram_followers"	INTEGER,
                    "contact_website"	TEXT,
                    "contact_name"	TEXT,
                    "default_from_email_id"	INTEGER,
                    PRIMARY KEY("contact_id")
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query("SELECT COUNT(tag_code) FROM tags", 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            print('CREATING TABLE Tags')
            statement = """
                CREATE TABLE "tags" (
                    "tag_code"	TEXT NOT NULL UNIQUE,
                    "tag_description"	TEXT,
                    PRIMARY KEY("tag_code")
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query("SELECT COUNT(*) FROM contact_tag_associations", 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            print('CREATING TABLE contact_tag_associations')
            statement = """
                CREATE TABLE "contact_tag_associations" (
                    "tag_code"	TEXT NOT NULL,
                    "contact_id"	INTEGER NOT NULL,
                    FOREIGN KEY("tag_code") REFERENCES "tags"("tag_code"),
                    PRIMARY KEY("tag_code","contact_id")
                );
            """
            self.create_table(statement, None)
        try:
            self.execute_query("SELECT COUNT(*) FROM contact_emails", 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            print('CREATING TABLE contact_emails')
            statement = """
                CREATE TABLE "contact_emails" (
                    "email_id"	INTEGER NOT NULL UNIQUE,
                    "contact_id"	INTEGER NOT NULL,
                    "email"	TEXT NOT NULL,
                    "type"	TEXT(2) NOT NULL,
                    FOREIGN KEY("contact_id") REFERENCES "contacts"("contact_id"),
                    PRIMARY KEY("email_id" AUTOINCREMENT)
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query("SELECT COUNT(*) FROM from_emails;", 'fetchone', None)

        except sqlite3.OperationalError:
            # Creates client_info if it does not exist
            print('CREATING TABLE from_emails')
            statement = """
                CREATE TABLE "from_emails" (
                    "from_email_id"	INTEGER NOT NULL UNIQUE,
                    "email"	TEXT NOT NULL,
                    "password"	TEXT NOT NULL,
                    "api_key"	TEXT,
                    "email_server"	TEXT,
                    "email_port"	INTEGER,
                    PRIMARY KEY("from_email_id" AUTOINCREMENT)
                );
            """
            self.create_table(statement, None)

        try:
            self.execute_query('SELECT COUNT(*) FROM active_transactions;', 'fetchone', None)

        except sqlite3.OperationalError:
            print('CREATING TABLE active_transactions')
            statement = """
            CREATE TABLE "active_transactions" (
                "transaction_id"	INTEGER NOT NULL UNIQUE,
                "contact_id"	INTEGER NOT NULL,
                "from_email"	TEXT NOT NULL,
                "subject_line"	TEXT,
                "body"	TEXT,
                "send_date"	datetime,
                PRIMARY KEY("transaction_id" AUTOINCREMENT),
                FOREIGN KEY("contact_id") REFERENCES "contacts"("contact_id"),
                FOREIGN KEY("from_email") REFERENCES "from_emails"("email"));"""

            self.create_table(statement, None)

        try:
            self.execute_query('SELECT COUNT(*) FROM active_transaction_emails;', 'fetchone', None)
        except sqlite3.OperationalError:
            statement = """
            CREATE TABLE "active_transaction_emails" (
                "transaction_id"	INTEGER NOT NULL,
                "contact_id"	INTEGER NOT NULL,
                "email"	TEXT NOT NULL,
                "type"	TEXT NOT NULL,
                PRIMARY KEY("contact_id","transaction_id","type","email")
            );"""
            self.create_table(statement, None)

        try:
            self.execute_query('SELECT COUNT(*) FROM archived_transaction_emails;', 'fetchone', None)
        except sqlite3.OperationalError:
            statement = """
            CREATE TABLE "archived_transaction_emails" (
                "transaction_id"	INTEGER NOT NULL,
                "contact_id"	INTEGER,
                "email"	TEST,
                "type"	char(2),
                PRIMARY KEY("transaction_id","email","type","contact_id"),
                FOREIGN KEY("contact_id") REFERENCES "contacts"("contact_id")
            );"""
            self.create_table(statement, None)

    def attachment_exists(self, attachment_source_link):
        query = """
            SELECT COUNT(attachment_id) 
            FROM attachments
            WHERE attachment_path = ?
        """
        count = self.execute_query(query, 'fetchone', (attachment_source_link,))[0]

        if count == 0:
            return False
        else:
            return True

    def contact_exists(self, original_contact_info):

        contact_info = copy.deepcopy(original_contact_info)
        if 'contact_tags' in contact_info:
            del contact_info['contact_tags']
        if 'contact_emails' in contact_info:
            del contact_info['contact_emails']

        keys = []
        for key in contact_info.keys():
            keys.append(f'{key} = ?')

        keys = ' AND '.join(keys)

        values = []
        for item in contact_info.values():
            values.append(item)

        contact_found = self.execute_query(f"""
            SELECT COUNT(*)
            FROM contacts
            WHERE {keys}
        """, 'fetchall', values)[0][0]

        if contact_found:
            return True
        else:
            return False

    def upload_archive_attachments(self, transaction_attachments):
        # It will  upload each attachment with one attachment_id.
        # That way we can use attachment_id in association table
        # Create a tuple with attachment_name, attachment_path

        query = f"""
            SELECT attachment_id, attachment_path
            FROM archived_attachments
            WHERE attachment_path IN ({', '.join(['?'] * len(transaction_attachments))})
        """
        existing_attachments = self.execute_thread_safe_query(query, 'fetchall',
                                                              transaction_attachments)  # Returns a list with [(attachment_id, attachment_path)]

        for transaction in existing_attachments:
            if transaction[1] in transaction_attachments:  # If transaction path in transaction_attachments
                transaction_attachments.remove(transaction[1])

        all_attachment_info = []
        for attachment_path in transaction_attachments:
            attachment_name = os.path.basename(attachment_path)
            all_attachment_info.append((attachment_name, attachment_path))

        # We need to check if the path already exists in the archived_attachments table
        # If it does we return the attachment id

        statement = """
        INSERT INTO archived_attachments(attachment_name, attachment_path)
        VALUES(?, ?);
        """

        attachments_ids = self.execute_many_inserts_thread_safe_w_id(statement,
                                                                     all_attachment_info)  # Uploads attachment and returns the attachment ids.

        complete_attachment_info = []

        for attachment_id, attachment_info in zip(attachments_ids,
                                                  all_attachment_info):  # Concats newly created attachments
            complete_attachment_info.append([attachment_id, attachment_info[1]])

        complete_attachment_info += existing_attachments

        return complete_attachment_info

    def upload_archive_attachment_associations(self, consolidated_attachments):

        upload_list = []

        for attachmet_id, transaction_ids in consolidated_attachments.items():
            for transaction_id in transaction_ids:
                upload_list.append((transaction_id, attachmet_id))

        statement = """
            INSERT INTO archived_attachment_transaction_associations(transaction_id, attachment_id)
            VALUES(?, ?);
        """
        self.execute_many_inserts_thread_safe_no_id(statement, upload_list)

    def get_attachments_by_transaction(self, transaction_id):

        attachment_paths = []
        # Needs to return a list with [attachment_paths, ...]

        # First we need to obtain the attachment_ids for this transaction in attachment_transaction_associations
        attachment_ids = self.get_attachment_ids_by_transaction_id(transaction_id)

        # Using the attachment_id we need to obtain the attachment_name, attachment_path for each
        query = F"""
            SELECT attachment_path
            FROM archived_attachments
            WHERE attachment_id IN  ({', '.join(['?'] * len(attachment_ids))})
        """

        attachment_paths_tuple = self.execute_thread_safe_query(query, 'fetchall', attachment_ids)
        for attachment in attachment_paths_tuple:
            if attachment:
                attachment_paths.append(attachment[0])
        if len(attachment_paths) == 0:
            attachment_paths = None

        return attachment_paths

    def get_attachment_ids_by_transaction_id(self, transaction_id):
        # Needs to return all the attachment_ids corresponding to the transaction_id
        query = """
            SELECT attachment_id
            FROM archived_attachment_transaction_associations
            WHERE transaction_id = ?
        """
        attachment_ids_tuple = self.execute_thread_safe_query(query, 'fetchall', (transaction_id,))
        attachment_ids = []
        for attachment in attachment_ids_tuple:
            if attachment:
                attachment = attachment[0]
                attachment_ids.append(attachment)

        return tuple(attachment_ids)

    def upload_new_contact(self, original_contact_info):

        # Upload contact to contact table
        # Upload contact tags to tag associations
        contact_info = copy.deepcopy(original_contact_info)
        # These will get uploaded to their own tables
        if 'contact_tags' in contact_info:
            del contact_info['contact_tags']  # Removes tag detail since that will be
        if 'contact_emails' in contact_info:
            del contact_info['contact_emails']
        # uploaded to another table in another function

        # Gets columns
        columns = list(contact_info.keys())
        values = []

        # Creates a ? for each value we will use to insert into contacts form
        for item in contact_info.values():
            values.append('?')
        insert_statement = f"""INSERT INTO contacts ({', '.join(columns)})
                    VALUES ({', '.join(values)});"""

        self.execute_insert(insert_statement, tuple(contact_info.values()))

        del contact_info['default_from_email_id']
        # Gets the client id and returns it
        query = f"""SELECT contact_id
                    FROM contacts
                    WHERE {' = ? AND '.join(contact_info)}"""
        query += ' = ?;'  # For last field which didnt have one added

        contact_id = self.execute_query(query, 'fetchone', tuple(contact_info.values()))

        if contact_id:
            return contact_id[0]
        else:
            return None

    def set_contact_emails(self, contact_id, from_email, to_emails, cc_emails):
        # Remove the current emails for this contact id
        contact_id = int(contact_id)

        info = (from_email, contact_id)

        update_statement = """
            UPDATE contacts
            SET default_from_email_id = ?
            WHERE contact_id = ?;
        """
        self.execute_update(update_statement, info)

        self.execute_delete(f"""
            DELETE FROM contact_emails
            WHERE contact_id = ?;
        """, (contact_id,))

        # Upload the to and cc emails for the client id

        statement = """
                INSERT INTO contact_emails (contact_id, email, type)
                VALUES (?, ?, 'to');
            """

        insert_values = []
        for email in to_emails:
            insert_values.append((contact_id, email))  # Appends a tupple to the insert_values list

        self.execute_many_inserts(statement, insert_values)

        statement = """
                INSERT INTO contact_emails (contact_id, email, type)
                VALUES (?, ?, 'cc');
            """
        insert_values = []

        for email in cc_emails:
            insert_values.append((contact_id, email))

        self.execute_many_inserts(statement, insert_values)

    def get_contact_emails(self, contact_id):

        # Needs to get the to emails and the cc emails and return a list [to_emails, cc_emails]
        query = """
            SELECT email
            FROM contact_emails
            WHERE contact_id = ? AND type = 'to';
        """
        to_emails = self.execute_query(query, 'fetchall', (contact_id,))

        for i in range(len(to_emails)):  # Restructures the list so that it is a single list with the emails as
            # string elements
            to_emails[i] = to_emails[i][0]

        query = """
            SELECT email
            FROM contact_emails
            WHERE contact_id = ? AND type = 'cc';
        """
        cc_emails = self.execute_query(query, 'fetchall', (contact_id,))

        for i in range(len(cc_emails)):  # Restructures the list so that it is a single list with the emails as
            # string elements
            cc_emails[i] = cc_emails[i][0]

        return to_emails, cc_emails

    def upload_contact_emails(self, contact_id, emails):

        statement = """
            INSERT into contact_emails(contact_id, email, type)
            VALUES(?, ?, ?)
        """

        insert_values = []
        # Adds emails to contact emails list
        for email in emails:
            type = ''
            if 'to' in email[
                       :4]:  # Checks if the first 4 characters in email includes cc. Email looks like '(to) :
                # email@domain.com'
                type = 'to'
                email = email.split('(to) : ', maxsplit=1)
                if email:
                    email = email[1]
            elif 'cc' in email[:4]:
                type = 'cc'
                email = email.split('(cc) : ', maxsplit=1)
                if email:
                    email = email[1]

            # Upload each email for the contact id
            insert_values.append((contact_id, email, type))

        self.execute_many_inserts(statement, insert_values)

    def overwrite_contact_emails(self, contact_id, emails):
        # Remove the emails for the specified contact id
        self.execute_delete("""
            DELETE
            FROM contact_emails
            WHERE contact_id = ?
        """, (contact_id,))

        # Adds emails to contact emails list
        statement = """
                INSERT into contact_emails(contact_id, email, type)
                VALUES(?, ?, ?)
            """
        insert_values = []

        for email in emails:
            type = ''
            if 'to' in email[
                       :4]:  # Checks if the first 4 characters in email includes cc. Email looks like '(to) :
                # email@domain.com'
                type = 'to'
                email = email.split('(to) : ', maxsplit=1)
                if email:
                    email = email[1]
            elif 'cc' in email[:4]:
                type = 'cc'
                email = email.split('(cc) : ', maxsplit=1)
                if email:
                    email = email[1]

            # Upload each email for the contact id
            insert_values.append((contact_id, email, type))

        self.execute_many_inserts(statement, insert_values)

    def upload_contact_tags(self, contact_id, tags):
        # Doesnt access DB so no connection is needed
        # Should upload tag if its new and associate it with the contact in the tag association table
        self.upload_new_tags(tags, tag_description=None)
        self.upload_tag_associations(contact_id, tags)

    def overwrite_contact_tags(self, contact_id, tags):

        # Delete the current tag associations
        self.execute_delete("""
            DELETE 
            FROM contact_tag_associations
            WHERE contact_id = ?;
        """, (contact_id,))

        # Should upload tag if its new and associate it with the contact in the tag association table
        self.upload_new_tags(tags, tag_description=None)
        self.upload_tag_associations(contact_id, tags)

    def upload_tag_associations(self, contact_id, tags):
        insert_values = []

        for tag in tags:
            insert_values.append((contact_id, tag))

        self.execute_many_inserts("""
                INSERT into contact_tag_associations(contact_id, tag_code)
                VALUES(?, ?)
            """, insert_values)

    def upload_new_tags(self, tags, **kwargs):
        # Should check if any of the tags on the list exist and if they don't, it should upload it
        # If the tag_description provided is None simply upload tag codes

        if kwargs['tag_description'] is None:
            insert_values = []
            for tag in tags:
                insert_values.append((tag,))

            try:
                self.execute_many_inserts("""
                        INSERT OR REPLACE INTO tags(tag_code)
                        VALUES(?)
                    """, insert_values)
            except sqlite3.IntegrityError:  # Since we want to upload only new tags, we can disregard error thrown
                # since it wont upload duplicates
                print('Integrity error')

    def get_contact_id_from_tag(self, tag):

        query = """
            SELECT contact_id
            FROM contact_tag_associations
            WHERE tag_code = ?
        """

        contact_ids = self.execute_query(query, 'fetchall', (tag,))

        for i in range(len(contact_ids)):
            contact_ids[i] = contact_ids[i][0]

        return contact_ids

    def get_contact_id_from_name(self, official_name):
        query = """
            SELECT contact_id
            FROM contacts
            WHERE official_name = ?
        """
        contact_id = self.execute_query(query, 'fetchone', (official_name,))[0]
        return contact_id

    def get_contact_official_name_from_id(self, contact_ids):
        contact_ids = tuple(contact_ids)

        if len(contact_ids) == 1:
            query = f"""
                SELECT official_name
                FROM contacts
                WHERE contact_id = {contact_ids[0]};
            """
        elif len(contact_ids) > 1:
            query = f"""
                SELECT official_name
                FROM contacts
                WHERE contact_id IN {contact_ids};
            """
        else:
            return None

        contact_names = self.execute_query(query, 'fetchall', None)

        for i in range(len(contact_names)):
            contact_names[i] = contact_names[i][0]

        return contact_names

    def get_matching_contacts_from_tags(self, tags):
        # Should query the db contact_tag_associations table and retrieve all contact_ids that are in the tags list
        tags = tuple(tags)
        value = None
        if len(tags) == 0:
            #  Clear all the contacts that have the add manually flag false
            matching_contacts = []
        elif len(tags) == 1:
            value = tags[0]
            query = f"""SELECT contact_id FROM contact_tag_associations WHERE tag_code = ?;"""
            matching_contacts = self.execute_query(query, 'fetchall', (value,))

        elif len(tags) > 1:
            value = tags
            query = f"""SELECT contact_id FROM contact_tag_associations WHERE tag_code IN {tags};"""
            matching_contacts = self.execute_query(query, 'fetchall', ())

        contacts = []
        for contact in matching_contacts:
            if contact:
                contacts.append(contact[0])
        return contacts

    def get_from_email_addresses(self):
        # Gets the emails that have been setup to send as the source
        from_emails = self.execute_query("""
            SELECT email
            FROM from_emails;
        """, 'fetchall', None)

        if from_emails:
            for i in range(len(from_emails)):
                from_emails[i] = from_emails[i][0]
            return from_emails
        else:
            return None

    def get_source_email_id_by_name(self, email_name):

        query = """
            SELECT from_email_id 
            FROM from_emails
            WHERE email = ?;
        """

        from_email_id = self.execute_query(query, 'fetchone', (email_name,))

        if from_email_id:
            from_email_id = from_email_id[0]
        return from_email_id

    def get_from_email_info(self, from_email):
        query = """
            SELECT *
            FROM from_emails
            WHERE email = ?;
        """
        info = list(self.execute_thread_safe_query(query, 'fetchall', (from_email,)))

        if info:
            return info[0]

    def get_from_email_info_by_id(self, from_email_id):
        query = """
            SELECT *
            FROM from_emails
            WHERE from_email_id = ?;
        """

        info = self.execute_thread_safe_query(query, 'fetchall', (from_email_id,))

        if info:
            return list(info[0])

    def get_default_from_email_name(self, contact_id):

        query = """
            SELECT default_from_email_id
            FROM contacts
            WHERE contact_id = ?
        """
        default_email_id = self.execute_query(query, 'fetchone', (contact_id,))

        # Will get the default email id from the contacts table
        if not default_email_id:
            return None

        default_email_id = default_email_id[0]
        # Gets email name from email id
        query = """
            SELECT email
            FROM from_emails
            WHERE from_email_id = ?
        """
        default_email_name = self.execute_query(query, 'fetchone', (default_email_id,))

        if default_email_name:
            default_email_name = default_email_name[0]
            return default_email_name

        else:
            return None

    def update_from_email(self, from_email_id, new_info):
        # Update the from email information for the specified email id
        new_info = list(new_info)
        new_info.append(from_email_id)

        statement = """
            UPDATE from_emails
            SET email = ?, password = ?, api_key = ?, email_server = ?, email_port = ?
            WHERE from_email_id = ?;
        """
        self.execute_update(statement, (new_info))

    def update_active_transaction_info(self, info):
        # Create statements
        active_transaction_update_statement = """
            UPDATE active_transactions
            SET from_email = ?, subject_line = ?, body = ?, send_date = ?
            WHERE transaction_id = ?
        """
        archived_transaction_update_statement = """
             UPDATE archived_transactions
             SET from_email = ?, subject_line = ?, body = ?, send_date = ?
             WHERE transaction_id = ?
         """
        archived_transaction_email_statement = """
            INSERT INTO archived_transaction_emails
            VALUES(?, ?, ?, ?)
        """
        active_transaction_email_statement = """
            INSERT INTO active_transaction_emails
            VALUES(?, ?, ?, ?)
        """
        archived_emails_delete_statement = """
            DELETE 
            FROM archived_transaction_emails
            WHERE transaction_id = ?
        """
        active_emails_delete_statement = """
            DELETE 
            FROM active_transaction_emails
            WHERE transaction_id = ?
        """
        attachments_delete_statement = """
            DELETE
            FROM archived_attachment_transaction_associations
            WHERE transaction_id = ?
        """

        # Extract info
        transaction_id = info[0]
        contact_id = info[1]
        from_email = info[2]
        subject_line = info[3]
        body = info[4]
        to_emails = info[5]
        cc_emails = info[6]
        send_date = info[7]
        attachments = info[8]

        email_tuple = []
        attachments_dict = {}

        for email in to_emails:  # We create the row tuple for many inserts
            email_tuple.append((transaction_id, contact_id, email, 'to'))

        for email in cc_emails:  # We create the row tuple for many inserts
            email_tuple.append((transaction_id, contact_id, email, 'cc'))

        # Execute updates
        self.execute_update(active_transaction_update_statement,
                            (from_email, subject_line, body, send_date, transaction_id))
        self.execute_update(archived_transaction_update_statement,
                            (from_email, subject_line, body, send_date, transaction_id))
        self.execute_delete(archived_emails_delete_statement, (transaction_id,))  # Remove current emails in archived
        self.execute_delete(active_emails_delete_statement, (transaction_id,))  # Remove current emails in archived
        self.execute_many_inserts_thread_safe_no_id(archived_transaction_email_statement, email_tuple)  # Add emails
        self.execute_many_inserts_thread_safe_no_id(active_transaction_email_statement, email_tuple)  # Add emails
        attachment_ids = self.upload_archive_attachments(attachments)

        for id in attachment_ids:  # We format the row info using the dict to reuse the
            # upload_archive_attachment_association method
            attachments_dict[id[0]] = [transaction_id]

        self.execute_delete(attachments_delete_statement, (transaction_id,))
        self.upload_archive_attachment_associations(attachments_dict)

        # Overwrite data in active transactions for specified transaction id
        # Overwrite data in emails for specified transaction id
        # Overwrite attachments in archived_transaction_associations

    def update_contact_information(self, contact_id, contact_info):
        contact_info.append(contact_id)
        statement = """
            UPDATE contacts
            SET official_name = ?, country = ?, instagram_followers = ?, contact_website = ?, contact_name = ?, default_from_email_id = ?
            WHERE contact_id = ?;
        """
        self.execute_update(statement, contact_info)

    def update_from_email_name(self, from_email_id, new_email):
        # Update the from email information for the specified email id

        statement = """
            UPDATE from_emails
            SET email = ?
            WHERE from_email_id = ?
        """
        self.execute_update(statement, (new_email, from_email_id))

    def upload_new_attachment(self, attachment_source_link):

        self.execute_insert("""
            INSERT INTO attachments(attachment_path)
            VALUES(?)
        """, (attachment_source_link,))

    def get_contacts_basic_info(self, filters):

        # Start building the SQL query
        query = """
            SELECT contact_id, official_name
            FROM contacts
        """

        # Check if filters are provided
        if filters:
            query += "WHERE "

            # Construct the WHERE clause based on the filters
            conditions = []
            values = []

            for column, condition, value in filters:
                if condition == 'equal to':
                    conditions.append(f"{column} = ?")
                    values.append(value)

                elif condition == 'contains':
                    conditions.append(f"{column} LIKE ?")
                    value = f"%{value}%"
                    values.append(value)

                elif condition == 'in':
                    # Assuming value is a comma-separated list of values
                    value_list = value.split(',')
                    conditions.append(f"{column} IN ({','.join(['?'] * len(value_list))})")
                    values.extend(value_list)
                elif condition == 'not equal to':
                    conditions.append(f"{column} != ?")
                    values.append(value)

                elif condition == 'does not contain':
                    conditions.append(f"{column} NOT LIKE ?")
                    value = f"%{value}%"
                    values.append(value)

                elif condition == 'not in':
                    # Assuming value is a comma-separated list of values
                    value_list = value.split(',')
                    conditions.append(f"{column} NOT IN ({','.join(['?'] * len(value_list))})")
                    values.extend(value_list)

                elif condition == 'greater than':
                    if value == '':
                        value = '0'

                    conditions.append(f"{column} > ? AND {column} != ''")
                    values.append(value)

                elif condition == 'less than':
                    if value == '':
                        value = '0'

                    conditions.append(f"{column} < ? AND {column} IS NOT NULL")
                    values.append(value)

            query += " AND ".join(conditions)

            # Execute the query using parameterized values
            contacts = self.execute_query(query, 'fetchall', tuple(values))
        else:
            contacts = self.execute_query(query, 'fetchall', ())

        return contacts

    def get_official_name(self, contact_id):

        official_name = self.execute_query("""
            SELECT official_name
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,))

        if official_name:
            return official_name[0]
        else:
            return None

    def get_from_email_by_id(self, from_email_id, thread_safe=False):

        if not thread_safe:
            email = self.execute_query("""
                SELECT email
                FROM from_emails
                WHERE from_email_id = ?
            """, 'fetchone', (from_email_id,))
        else:
            email = self.execute_thread_safe_query("""
                SELECT email
                FROM from_emails
                WHERE from_email_id = ?
            """, 'fetchone', (from_email_id,))

        return email[0]

    def get_matching_tags(self, tag_code):
        cache_tags = """
            SELECT tag_code
            FROM tags
            WHERE tag_code LIKE ?
        """
        matching_tags = self.execute_query(cache_tags, 'fetchall', (tag_code + '%',))
        matching_tags_copy = []

        for tag in matching_tags:
            if tag:
                matching_tags_copy.append(tag[0])

        return matching_tags_copy

    def get_cache_tags(self):
        cache_tags = """
            SELECT tag_code
            FROM tags
            LIMIT 100
        """
        cached_tags = self.execute_query(cache_tags, 'fetchall', ())

        cached_tags_copy = []

        for tag in cached_tags:
            if tag:
                cached_tags_copy.append(tag[0])

        return cached_tags_copy

    def get_contact_tags(self, contact_id):
        # Gets the tags of the contact id
        contact_tags = self.execute_query(f"""
            SELECT tag_code
            FROM contact_tag_associations
            WHERE contact_id = ?
        """, 'fetchall', (contact_id,))

        # Reformat the tags to be elements in a list
        tags = []
        if contact_tags:
            for tag in contact_tags:
                if tag:
                    tags.append(tag[0])

        return tags

    def get_contacts_full_info(self, contact_id):
        # Should get all the contact info that will be needed to populate form
        # Includes fields and emails

        # Gets contact info
        contact_info = list(self.execute_query("""
            SELECT *
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,)))

        contact_info.pop(0)  # Remove contact id from list

        # Get additional info
        emails = self.get_contact_emails(contact_id)
        tags = self.get_contact_tags(contact_id)

        # Concatenate info
        if emails:
            for email in emails:
                contact_info.append(email)
        else:
            contact_info.append([])
        if tags:
            contact_info.append(tags)
        else:
            contact_info.append([])

        return contact_info

    def get_contact_name_from_id(self, contact_id):
        query = """
            SELECT official_name
            FROM contacts
            WHERE contact_id = ?
        """

        name = self.execute_thread_safe_query(query, 'fetchone', (contact_id,))
        if name:
            name = list(name)
            name = name[0]
        return name

    def get_transaction_edit_info(self, source, transaction_id):
        if source == 'archived':
            transactions_info = self.get_archived_transaction_by_id(transaction_id)  # returns a tuple
            to_emails, cc_emails = self.get_archived_emails(transaction_id)  # Get to and cc emails

        else:
            transactions_info = self.get_active_transaction_by_id(transaction_id)  # returns a tuple
            to_emails, cc_emails = self.get_active_emails(transaction_id)  # Get to and cc emails

        contact_id = transactions_info[0]
        official_contact_name = self.get_contact_name_from_id(contact_id)
        transactions_info.append(official_contact_name)
        # containing contact_id, from_email, subject_line, email_body, send_date

        if type(to_emails) is not list:
            if to_emails:
                to_emails = [to_emails]
            else:
                to_emails = []

        transactions_info.append(to_emails)

        if type(cc_emails) is not list:
            if cc_emails:
                cc_emails = [cc_emails]
            else:
                cc_emails = []

        transactions_info.append(cc_emails)

        attachments = self.get_attachments_by_transaction(transaction_id)

        if attachments:
            if type(attachments) != list:
                attachments = [attachments]
            transactions_info.append(attachments)
        else:
            transactions_info.append([])

        return transactions_info

    def get_active_transaction_by_id(self, transaction_id):
        query = """
            SELECT contact_id, from_email, subject_line, body, send_date
            FROM active_transactions
            WHERE transaction_id = ?;
        """

        active_trans_info = self.execute_thread_safe_query(query, 'fetchall', (transaction_id,))

        if active_trans_info:
            active_trans_info = active_trans_info[0]

        return list(active_trans_info)

    def get_active_transaction_by_contact(self, contact_id):
        query = """
             SELECT transaction_id
             FROM active_transactions
             WHERE contact_id = ?;
         """
        active_trans_info = self.execute_query(query, 'fetchall', (contact_id,))
        return active_trans_info

    def get_archived_transaction_by_id(self, transaction_id):
        query = """
            SELECT contact_id, from_email, subject_line, body, send_date
            FROM archived_transactions
            WHERE transaction_id = ?;
        """

        archived_trans_info = self.execute_thread_safe_query(query, 'fetchall', (transaction_id,))

        if archived_trans_info:
            archived_trans_info = archived_trans_info[0]

        return list(archived_trans_info)

    def email_account_exists(self, email):
        # Query database to see if an email with this info is already

        found_accounts = self.execute_query("""
            SELECT from_email_id 
            FROM from_emails
            WHERE email = ?;
        """, 'fetchall', (email,))

        if found_accounts:
            return True
        else:
            return False

    def upload_from_information(self, info):
        self.execute_insert("""
            INSERT INTO from_emails(email, password, api_key, email_server, email_port)
            VALUES(?, ?, ?, ?, ?)
        """, info)

    def get_from_email_id(self, email):
        from_email_id = self.execute_query("""
        SELECT from_email_id
        FROM from_emails
        WHERE email = ?;
        """, 'fetchone', (email,))

        if from_email_id:
            return from_email_id[0]

    def get_contact_country(self, contact_id):
        country = self.execute_query("""
            SELECT country
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,))

        if country:
            return country[0]
        else:
            return None

    def get_instagram_followers(self, contact_id):
        instagram_followers = self.execute_query("""
            SELECT instagram_followers
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,))

        if instagram_followers:
            return instagram_followers[0]
        else:
            return None

    def get_contact_website(self, contact_id):
        website = self.execute_query("""
            SELECT contact_website
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,))

        if website:
            return website[0]
        else:
            return None

    def get_contact_name(self, contact_id):
        contact_name = self.execute_query("""
            SELECT contact_name
            FROM contacts
            WHERE contact_id = ?
        """, 'fetchone', (contact_id,))
        if contact_name:
            return contact_name[0]
        else:
            return None

    def get_active_emails(self, transaction_id):

        to_emails_list = []
        cc_emails_list = []

        to_emails = self.execute_thread_safe_query("""
            SELECT email
            FROM active_transaction_emails
            WHERE transaction_id = ? AND type = 'to'
        """, 'fetchall', (transaction_id,))
        for email in to_emails:
            if email:
                to_emails_list.append(email[0])  # Gets it out of tuple

        cc_emails = self.execute_thread_safe_query("""
            SELECT email, type
            FROM active_transaction_emails
            WHERE transaction_id = ? AND type = 'cc'
        """, 'fetchall', (transaction_id,))

        for email in cc_emails:
            if email:
                cc_emails_list.append(email[0])  # Gets it out of tuple

        return to_emails_list, cc_emails_list

    def get_archived_emails(self, transaction_id):
        to_emails_list = []
        cc_emails_list = []

        to_emails = self.execute_thread_safe_query("""
            SELECT email
            FROM archived_transaction_emails
            WHERE transaction_id = ? AND type = 'to'
        """, 'fetchall', (transaction_id,))

        for email in to_emails:
            if email:
                to_emails_list.append(email[0])  # Gets it out of tuple

        cc_emails = self.execute_thread_safe_query("""
            SELECT email, type
            FROM active_transaction_emails
            WHERE transaction_id = ? AND type = 'cc'
        """, 'fetchall', (transaction_id,))

        for email in cc_emails:
            if email:
                cc_emails_list.append(email[0])  # Gets it out of tuple

        return to_emails_list, cc_emails_list

    def create_test_data(self):
        print('CREATING TEST DATA')

        self.create_from_emails_links()  # Creates dummy from emails
        self.create_contacts()
        self.create_emails()
        self.create_tags()
        self.create_tag_associations()
        self.create_attachments()

        print('TEST DATA CREATED')

    def create_from_emails_links(self):

        # Does not have its own connection
        from_emails = open('test data/from emails.txt', 'r')
        password = 'password1'

        insert_values = []
        for email in from_emails:
            email = email.strip()
            insert_values.append((email, password))

        self.execute_many_inserts("""
                INSERT INTO from_emails(email, password)
                VALUES(?, ?)
            """, insert_values)

        print(f'CREATED FROM EMAILS')

    def create_contacts(self):
        # Does not have its own connections

        official_names_file = open('test data/1000 company names.txt', 'r')
        country_file = open('test data/all countries.txt', 'r')
        instagram_followers_file = open('test data/1000 ig folower counts.txt', 'r')
        websites_file = open('test data/1000 websites.txt', 'r')
        contact_names_file = open('test data/1000 contact names.txt', 'r')

        countries = []
        for country in country_file:
            country = country.strip()
            countries.append(country)

        insert_values = []
        statement = """
                INSERT INTO contacts(official_name, country, instagram_followers, contact_website, contact_name, default_from_email_id)
                VALUES(?, ?, ?, ?, ?, ?)
            """
        for official_name, instagram_followers, website, contact_name in zip(official_names_file,
                                                                             instagram_followers_file, websites_file,
                                                                             contact_names_file):
            default_from_email_id = random.randint(0, 276)  # 276 random from emails
            country = countries[random.randint(0, len(countries) - 1)]

            official_name = official_name.strip().lower()
            instagram_followers = instagram_followers.strip()
            website = website.strip()
            contact_name = contact_name.strip()

            insert_values.append(
                (official_name, country, instagram_followers, website, contact_name, default_from_email_id))

        self.execute_many_inserts(statement, insert_values)
        print(f'CREATED CONTACTS')

    def create_emails(self):

        to_emails_file = open('test data/1000 to emails.txt', 'r')
        cc_emails_file = open('test data/1000 cc emails.txt', 'r')

        to_emails = []
        for email in to_emails_file:
            email = email.strip()
            to_emails.append(email)

        cc_emails = []
        for email in cc_emails_file:
            email = email.strip()
            cc_emails.append(email)

        for contact_id in range(1, 1001):

            to_email_count = random.randint(1, 7)
            cc_email_count = random.randint(1, 4)

            insert_values = []
            for count in range(1, to_email_count):
                max = len(to_emails) - 1
                email_selection = to_emails[random.randint(0, max)]
                insert_values.append((contact_id, email_selection))

            self.execute_many_inserts("""
                    INSERT INTO contact_emails(contact_id, email, type)
                    VALUES (?, ?, 'to')
                """, insert_values)

            insert_values = []
            for count in range(1, cc_email_count):
                max = len(cc_emails) - 1
                email_selection = cc_emails[random.randint(0, max)]
                insert_values.append((contact_id, email_selection))

            self.execute_many_inserts("""
                    INSERT INTO contact_emails(contact_id, email, type)
                    VALUES (?, ?, 'cc')
                """, insert_values)

        print(f'CREATED EMAILS')

    def create_tags(self):

        tags_file = open('test data/1000 tags.txt', 'r')
        tags = []
        for tag in tags_file:
            tag = tag.strip()
            tags.append(tag)

        insert_values = []

        self.execute_many_inserts("""
                INSERT INTO tags(tag_code)
                VALUES(?)
            """, insert_values)

        print(f'CREATED TAGS')

    def create_tag_associations(self):
        tags_file = open('test data/1000 tags.txt', 'r')
        tags = []
        for tag in tags_file:
            tag = tag.strip()
            tags.append(tag)

        for contact_id in range(1, len(tags) - 1):  # Goes through each contact id to set tags
            tag_count = random.randint(1, 10)  # Gets the # of tags to be added
            tag_selection = []

            for i in range(0, tag_count):  # Performs operation tag count times.
                tag = tags[random.randint(0, len(tags) - 1)]
                while tag in tag_selection:
                    tag = tags[random.randint(0, len(tags) - 1)]
                tag_selection.append(tag)

            insert_values = []
            statement = """
                    INSERT INTO contact_tag_associations(tag_code, contact_id)
                    VALUES(?, ?);
                """
            for tag in tag_selection:
                insert_values.append((tag, contact_id))
            self.execute_many_inserts(statement, insert_values)

        print(f'CREATED TAG ASSOCIATIONS')

    def upload_archive_transactions(self, transactions):
        print(f'transactions: {transactions}')
        # Transaction from priority function will include
        # to_emails, cc_emails and attachments. Database should ignore those

        statement = """
        INSERT INTO archived_transactions(contact_id, from_email, subject_line, body, send_date)
        VALUES(?, ?, ?, ?, ?);
        """
        transactions_list = []  # WIll hold list with elements to upload to archive

        if len(transactions[0]) == 8:  # Samples a transaction from transactions and
            # checks if its 8 elements which means it was sent from priority function
            for transaction in transactions:
                complete_trans_val = []
                transaction_vals = list(transaction.values())
                complete_trans_val = transaction_vals[0:4]  # Everything except send_date
                complete_trans_val.append(transaction_vals[-2])  # Adds send_date
                # cc_emails and attachments. They will be uploaded in another function
                transactions_list.append(tuple(complete_trans_val))
        else:

            for transaction in transactions:
                # we want just the from_email_id
                transactions_list.append(tuple(transaction.values()))
        print(F'transaction_list: {transactions_list}')
        transaction_ids = self.execute_many_inserts_thread_safe_w_id(statement, transactions_list)

        return transaction_ids

    def upload_active_transaction(self, transaction_ids, transactions):

        # Will upload transactions into active_transactions that are to be sent in the future
        statement = """
        INSERT INTO active_transactions(transaction_id, contact_id, from_email, subject_line, body, send_date)
        VALUES(?, ?, ?, ?, ?, ?);
        """

        transactions_list = []  # Will hold a tuple for each transaction info with no emails

        for transaction, transaction_id in zip(transactions, transaction_ids):  # Goes through each transaction and
            # transaction id
            transaction = list(transaction.values())
            transaction.insert(0, transaction_id)
            transaction = tuple(transaction)  # Gets the values from the dictionary and converts it to a tuple
            transactions_list.append(transaction)  # Adds the transaction tuple to the list

        self.execute_many_inserts_thread_safe_no_id(statement, transactions_list)  # Executes to and also creates

    def reload_failed_transaction(self, transaction):

        upload_trans_statement = """
        INSERT INTO active_transactions(contact_id, from_email_id, subject_line, body, send_date)
        VALUES(?, ?, ?, ?, ?);
        """

        upload_emails_statement = """
        INSERT INTO active_transaction_emails(transaction_id, contact_id, email, type)
        VALUES(?, ?, ?, ?);
        """

        transaction_id = transaction.pop(0)
        contact_id = transaction[0]
        send_date = transaction[-2]  # Send date

        if not send_date:  # If send date is none
            send_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        send_date_obj = datetime.datetime.strptime(send_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
            minutes=2)  # Add two minutes to the send date so it can try again
        send_date_string = send_date_obj.strftime('%Y-%m-%d %H:%M:%S')  # Newest string with correct updated upload date

        transaction[-2] = send_date_string

        to_emails = transaction.pop(4)
        cc_emails = transaction.pop(4)

        emails_list = []
        for to_email in to_emails:
            emails_list.append((transaction_id, contact_id, to_email, 'to'))

        for cc_email in cc_emails:
            emails_list.append((transaction_id, contact_id, cc_email, 'cc'))

        attachments = transaction.pop(-1)
        transaction = (tuple(transaction),)

        self.execute_many_inserts_thread_safe_no_id(upload_trans_statement, transaction)  # Executes to and also creates
        self.execute_many_inserts_thread_safe_w_id(upload_emails_statement, emails_list)

    def upload_active_emails(self, transaction_emails):

        insert_values = []
        for item in transaction_emails:

            transaction_id = item[0]
            contact_id = item[1]
            emails = item[2]  # The emails list
            type = item[3]

            for email in emails:  # Need to make a tuple with each email
                insert_values.append((transaction_id, contact_id, email, type))

        statement = """
        INSERT INTO active_transaction_emails(transaction_id, contact_id, email, type)
        VALUES(?, ?, ?, ?);
        """
        self.execute_many_inserts_thread_safe_w_id(statement, insert_values)

    def upload_archive_emails(self, transaction_emails):
        # transaction_emails is a list that will hold a tuple for the emails in the form [transaction_id,
        # contact_id, to_emails, cc_emails]

        insert_values = []  # List that will hold a tuple for each email in the form (transaction_id, contact_id,
        # email, type)

        for item in transaction_emails:

            transaction_id = item[0]
            contact_id = item[1]
            emails = item[2]  # The emails list
            email_type = item[3]

            for email in emails:  # Need to make a tuple for each email
                insert_values.append((transaction_id, contact_id, email, email_type))

        # Insert into the DB
        statement = """
        INSERT INTO archived_transaction_emails(transaction_id, contact_id, email, type)
        VALUES(?, ?, ?, ?);
        """
        self.execute_many_inserts_thread_safe_w_id(statement, insert_values)

    def remove_all_transactions(self, transaction_id):
        # Remove from active transactions
        remove_active_statement = """
            DELETE FROM active_transactions
            WHERE transaction_id = ?
        """
        self.execute_delete(remove_active_statement, (transaction_id,))

        # Remove from active transaction emails
        remove_active_email_statement = """
            DELETE FROM active_transaction_emails
            WHERE transaction_id = ?
        """
        self.execute_delete(remove_active_email_statement, (transaction_id,))

        # Remove from archived transactions
        remove_archive_statement = """
            DELETE FROM archived_transactions
            WHERE transaction_id = ?
        """
        self.execute_delete(remove_archive_statement, (transaction_id,))

        # Remove from archived transaction emails
        remove_archived_email_statement = """
            DELETE FROM archived_transaction_emails
            WHERE transaction_id = ?
        """
        self.execute_delete(remove_archived_email_statement, (transaction_id,))

        # Remove from archived attachment transaction associations
        remove_attachment_statement = """
            DELETE FROM archived_attachment_transaction_associations
            WHERE transaction_id = ?
        """
        self.execute_delete(remove_attachment_statement, (transaction_id,))

    def get_transactions(self, type, offset):
        if type == 'archive':
            # Query for archived transactions including the failed flag
            query = """
                SELECT 
                    t.transaction_id, 
                    COALESCE(c.official_name, 'DELETED') AS official_name,
                    t.send_date,
                    COUNT(DISTINCT CASE WHEN e.type = 'to' THEN e.email END) AS to_emails_count,
                    COUNT(DISTINCT CASE WHEN e.type = 'cc' THEN e.email END) AS cc_emails_count,
                    t.failed
                FROM archived_transactions t
                LEFT JOIN contacts c ON c.contact_id = t.contact_id 
                LEFT JOIN archived_transaction_emails e ON e.transaction_id = t.transaction_id
                GROUP BY t.transaction_id, official_name, t.send_date, t.failed
                ORDER BY t.transaction_id
                LIMIT 50
                OFFSET ?
            """
        else:
            # Query for active transactions without the failed flag
            query = """
                SELECT 
                    t.transaction_id, 
                    COALESCE(c.official_name, 'DELETED') AS official_name,
                    t.send_date,
                    COUNT(DISTINCT CASE WHEN e.type = 'to' THEN e.email END) AS to_emails_count,
                    COUNT(DISTINCT CASE WHEN e.type = 'cc' THEN e.email END) AS cc_emails_count
                FROM active_transactions t
                LEFT JOIN contacts c ON c.contact_id = t.contact_id
                LEFT JOIN active_transaction_emails e ON e.transaction_id = t.transaction_id
                GROUP BY t.transaction_id, official_name, t.send_date
                ORDER BY t.transaction_id
                LIMIT 50
                OFFSET ?
            """

        # Execute the selected query
        transactions = self.execute_query(query, 'fetchall', (offset,))
        return transactions

    def remove_active_transactions(self, transaction_ids):
        statement = """
        DELETE FROM active_transactions
        WHERE transaction_id = ?;
        """
        self.execute_delete_many_thread_safe(statement, transaction_ids)

        statement = """
        DELETE FROM active_transaction_emails
        WHERE transaction_id = ?;
        """
        self.execute_delete_many_thread_safe(statement, transaction_ids)

    def remove_archived_transactions(self, transaction_ids):
        statement = """
        DELETE FROM archived_transactions
        WHERE transaction_id = ?;
        """
        self.execute_delete_many_thread_safe(statement, transaction_ids)

        statement = """
        DELETE FROM archived_transaction_emails
        WHERE transaction_id = ?;
        """
        self.execute_delete_many_thread_safe(statement, transaction_ids)

        statement = """
            DELETE
            FROM archived_attachment_transaction_associations
            WHERE transaction_id = ?
        """
        self.execute_delete_many_thread_safe(statement, transaction_ids)


    def get_table_columns(self, table):

        column_names = []

        query = f"""
            PRAGMA table_info({table})
        """
        column_info = self.execute_query(query, 'fetchall', ())

        for column in column_info:
            column_names.append(column[1])

        return column_names

    def delete_contact(self, contact_id):
        # We need to get the transaction ids of the scheduled transactions for the specified contact_id
        transactions = self.get_active_transaction_by_contact(contact_id)
        # Using that we will delete the emails, attachments and the transaction itself
        # Then we will delete the contact
        delete_contacts_statement = """
            DELETE
            FROM contacts
            WHERE contact_id = ?
        """
        delete_contact_emails_statement = """
        
            DELETE
            FROM contact_emails
            WHERE contact_id = ?
        """
        delete_tags_associations_statement = """
            DELETE
            FROM contact_tag_associations
            WHERE contact_id = ?
        """

        self.remove_archived_transactions(tuple(transactions))
        self.remove_active_transactions(tuple(transactions))
        self.execute_delete(delete_contacts_statement, (contact_id,))
        self.execute_delete(delete_contact_emails_statement, (contact_id,))
        self.execute_delete(delete_tags_associations_statement, (contact_id,))

    def set_failed_transactions(self, failed_transaction_ids):
        failed_transaction_ids_str = []

        for transaction_id in failed_transaction_ids:
            failed_transaction_ids_str.append(str(transaction_id))

        # Prepare the SQL statement with placeholders for IDs
        update_statement = f"""
            UPDATE archived_transactions
            SET failed = 1
            WHERE transaction_id IN ({", ".join(failed_transaction_ids_str)})
        """
        # Execute the query safely with the list of IDs
        self.execute_update(update_statement, None)
