import copy
import os.path
import threading
import time
from datetime import datetime, timedelta
from email.message import EmailMessage
from queue import Queue
import concurrent.futures
from socket import gaierror

import Database
import smtplib
from cryptography.fernet import Fernet

from PyQt5.QtCore import pyqtSignal, QObject

# Transaction dictionary elements are in the format: {contact_id, subject_line, email_body, from_email, to_emails,
# cc_emails, send_date (contact scope)

password_key = '6cLEW86I06XOjv2V6lJZ7HayQrJJe8t9VpiSH7fnUFk='


def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return encrypted_data


def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data


class TransactionManager(QObject):
    error_signal = pyqtSignal(list)
    transaction_sent = pyqtSignal(int)
    uploaded_transactions = pyqtSignal()
    transactions_failed = pyqtSignal(list)  # Used when a transaction fails to
    # remove from active and set flag in archive. Is in format [failed_transactions, error_type]
    thread_lock = threading.Lock()

    # Class that will be used to check for transactions that are coming up (scheduled in queue)
    # Will read from the database to acquire the transaction details to send

    def __init__(self, database):

        super().__init__()
        self.transaction_sender_daemon = None
        self.queue_reader_daemon = None
        self.transaction_queue = Queue()  # Queue that will hold transactions
        self.database_handle = database
        self.transaction_reader_daemon = None
        self.progress_bar = None
        self.max_sender_threads = 20
        self.active_sender_threads = 0
        print(f'Transaction manager doing work...')

    def start_transaction_manager(self):
        # Starts various components of the Transaction Manager

        self.transaction_reader_daemon = threading.Thread(target=self.start_transaction_reader_daemon)
        self.transaction_reader_daemon.start()

        self.transaction_sender_daemon = threading.Thread(target=self.start_transaction_sender_daemon)
        self.transaction_sender_daemon.start()

    def process_transaction_batch(self, total_contacts, transaction_batch):
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(total_contacts)

        settings_info = transaction_batch.pop(-2)  # Gets the settings dictionary from the list
        global_send_date = settings_info.pop('send_date')  # Strip the global send time
        global_attachments = transaction_batch.pop(-1)  # Gets the global attachments which is last in list
        # If a global send time is active; for any contacts that have none on the send_date it will use this value If
        # contact has a send_date, and we have a global date, we will use the contacts send date If no global date is
        # specified but a contact send date is we will use the contacts send date If neither a global or contact send
        # date is specified, it will be added to the queue directly to send immediate
        upload_transactions = []  # Holds all dictionary transactions that are being sent at a later date
        priority_transactions = {}  # Holds dictionary transactions that will be sent instantly
        # transactions should be in format: {'from@email.com' : [{transaction}, ]}
        for transaction in transaction_batch:  # Goes through transactions and partitions the instant vs future
            # transactions
            transaction_send_date = transaction['send_date']  # Send date for the contact specifically
            if not transaction_send_date and not global_send_date:  # If no transaction or global send_date is
                # specified (Instant)
                try:
                    priority_transactions[transaction['from_email']].append(transaction)
                except KeyError:
                    priority_transactions[transaction['from_email']] = [transaction]
            else:
                if not transaction_send_date:  # If no transaction send date is specified use the global date
                    # Store transaction into active transaction table using the global date
                    transaction['send_date'] = global_send_date

                upload_transactions.append(transaction)  # Need to change this to use from email instead of id

            curr_value = self.progress_bar.value()
            self.progress_bar.setValue(curr_value + 1)

        # Place the transaction in the archive
        # Place the priority transactions into the queue
        # Should not break up email since it will be needed and we can save a database hit
        if priority_transactions:
            priority_send_thread = threading.Thread(target=self.process_priority_transactions(priority_transactions,
                                                                                              global_attachments))
            # This will add the transaction to archive and send
            priority_send_thread.start()

        # Will break up email and attachments since it will upload to DB; to each table respectively for use later
        if upload_transactions:  # If we have transactions to send later
            upload_transactions_thread = threading.Thread(target=self.upload_transactions(upload_transactions,
                                                                                          global_attachments))
            # This will add it to the archive transaction table and the active transaction table
            upload_transactions_thread.start()

    def upload_transactions(self, transaction_batch, global_attachments):
        # Transaction batch here is a list that has a dictionary for each transaction and the transaction has emails
        to_emails_info = []  # Holds [contact_id, [to_emails_info]]
        cc_emails_info = []  # Holds [contact_id, [cc_emails_info]]
        transaction_email_info = []  # List that wil hold a tuple for the emails in the form [transaction_id,
        # contact_id, to_emails, cc_emails]
        transaction_attachments = []

        for transaction in transaction_batch:  # Goes through transactions in list
            to_emails = transaction.pop('to_emails')  # Removes to_emails from transaction
            cc_emails = transaction.pop('cc_emails')  # Removes cc_emails from transaction
            to_emails_info.append([transaction['contact_id'], to_emails])
            # Will be used to upload to transaction emails
            cc_emails_info.append([transaction['contact_id'], cc_emails])
            # Will be used to upload cc transaction emails

            attachments = transaction.pop('attachments')
            if global_attachments:
                if attachments:
                    attachments.extend(global_attachments)
                else:
                    attachments = global_attachments

            if attachments:
                transaction_attachments.append(attachments)
            else:
                transaction_attachments.append([])

        transaction_ids = self.database_handle.upload_archive_transactions(transaction_batch)
        # Uploads transaction to archive first and it returns a list in the same order of the transaction ids that
        # were created

        self.process_attachments(transaction_ids, transaction_attachments)

        # Gets email emails and creates tuple for upload
        for transaction_id, email_info in zip(transaction_ids, to_emails_info):
            # Goes through each transaction id and to_email
            contact_id = email_info[0]
            to_emails = email_info[1]

            transaction_email_info.append((transaction_id, contact_id, to_emails, 'to'))  # Uploads the transaction
            # emails that we're using to the DB as a tuple for the to emails

        for transaction_id, email_info in zip(transaction_ids, cc_emails_info):
            # Goes through each transaction id and cc_email
            contact_id = email_info[0]
            cc_emails = email_info[1]

            transaction_email_info.append((transaction_id, contact_id, cc_emails, 'cc'))  # Uploads the transaction
            # emails that we're using to the DB as a tuple for the cc emails

        # Archive upload was already done at this point to get transaction ids
        self.database_handle.upload_archive_emails(transaction_email_info)  # Uploads all transaction emails to archive

        self.database_handle.upload_active_emails(transaction_email_info)  # Uploads emails for transactions to send
        # later

        self.database_handle.upload_active_transaction(transaction_ids, transaction_batch)  # Uploads transactions to
        # send later
        self.uploaded_transactions.emit()

    def convert_to_list(self, transactions):

        # transaction = {from_email: [{dict_key: dict_value, ...}, {}, {}, ...]}  Only the case when sent from
        # priority transaction

        updated_dict = dict()  # Will hold the transactions for each from email with transaction info as a list
        for transaction in transactions.values():
            if type(transaction[0]) == list:  # If it's a list already we can return
                return transactions

        list_for_dict = []  # Will hold info for each transaction
        for from_email, transaction_values in transactions.items():  # transaction_values is the list with dict elements
            for transaction in transaction_values:  # transaction is the dictionary
                list_for_dict.append(list(transaction.values()))  # Upload the dict values to the list
            updated_dict[from_email] = list_for_dict  # Upload list info to dict using from_email as key
            list_for_dict = []  # Reset

        return updated_dict

    def send_transactions(self, transactions):
        transactions = self.convert_to_list(transactions)
        threads = []
        for from_email, email_transactions in transactions.items():
            thread = threading.Thread(target=self.handle_email_sending, args=(from_email, email_transactions))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def handle_email_sending(self, from_email, email_transactions):
        from_email_info = self.database_handle.get_from_email_info(from_email)
        domain_type = from_email.split('@')[1]

        if from_email_info[2]:  # If password
            password = decrypt_data(from_email_info[2], password_key)
        else:
            password = None

        if from_email_info[3]:  # If api key
            api_key = decrypt_data(from_email_info[3], password_key)
        else:
            api_key = None

        email_server = from_email_info[4]
        email_port = from_email_info[5]

        # try:
        try:
            with smtplib.SMTP(email_server, email_port) as server:
                server.starttls()
                if domain_type == 'gmail.com':
                    server.login(from_email, api_key)
                elif domain_type == 'yahoo.com':
                    server.login(from_email, api_key)
                else:
                    server.login(from_email, password)

                for transaction in email_transactions:
                    self.send_email(server, transaction, from_email)
        except gaierror:
            self.error_signal.emit(['Error with Network connection', f'There was a network issue. Please check your connection and try again.'])
            self.transactions_failed.emit([email_transactions, 'network'])
        except smtplib.SMTPAuthenticationError:
            self.error_signal.emit(['Error with email login info', f'There was an error while logging in with the provided credentials: {from_email}'])
            self.transactions_failed.emit([email_transactions, 'authenticate'])
        except smtplib.SMTPServerDisconnected:
            self.error_signal.emit(['Error with SMTP server info', f'There was an error while connecting using<br><br>server: {server}<br>port: {email_port}'])
            self.transactions_failed.emit([email_transactions, 'server'])
        except ConnectionRefusedError:
            self.error_signal.emit(['Error with connection.', f'There was an error while connecting to server<br><br>server: {server}<br>port: {email_port}'])
            self.transactions_failed.emit([email_transactions, 'server'])

    def send_email(self, server, transaction, from_email):
        message = EmailMessage()
        message["From"] = from_email
        message["To"] = ', '.join(transaction[4])  # to_emails
        message["Cc"] = ', '.join(transaction[5])  # cc_emails
        message["Subject"] = transaction[2]  # subject_line
        message.add_alternative(transaction[3], subtype='html')  # email_body

        if transaction[7]: # If attachments is not none
            for attachment_path in transaction[7]:  # attachments
                try:
                    with open(attachment_path, 'rb') as file_handle:
                        file_name = os.path.basename(attachment_path)
                        file_content = file_handle.read()
                        message.add_attachment(file_content, maintype='application', subtype='octet-stream', filename=file_name)
                except FileNotFoundError:
                    print(f'File: {attachment_path} was not found')

        server.send_message(message)
        self.transaction_sent.emit(transaction[-1])  # Emit transaction id

    def process_priority_transactions(self, transactions, global_attachments):
        # Class that will insert any transactions that are being sent now into the queue

        to_emails_info = []  # Holds [contact_id, [to_emails_info]]
        cc_emails_info = []
        transaction_email_info = []  # Will hold tuple elements for to and cc emails
        transaction_attachments = []

        # Use the current date and time to upload to archive
        date_now = datetime.now()
        date_string = date_now.strftime('%Y-%m-%d %H:%M:%S')

        transactions_data = []

        for from_email_transaction in transactions.items():  # Transactions is a dict with from_email grouping as key
            # and transactions for that email as values
            transaction_data = from_email_transaction[1]  # Transaction data is a dict with the transaction info
            transactions_data.extend(transaction_data)

            for transaction in transaction_data:  # Creates pointers to create a list to upload for emails and
                # attachments
                to_emails = transaction['to_emails']  # Gets the list of to emails
                cc_emails = transaction['cc_emails']  # Gets the list of cc emails
                to_emails_info.append([transaction['contact_id'], to_emails])  # Associates the contact_id with the
                # to_emails
                cc_emails_info.append([transaction['contact_id'], cc_emails])  # Associates the contact_id with the
                # cc_emails
                transaction['send_date'] = date_string
                attachments = transaction['attachments']
                if global_attachments:  # If global attachments exist
                    if attachments: # If contact attachments exist
                        transaction['attachments'].extend(global_attachments)
                        attachments.extend(global_attachments)  # Add global attachments
                    else:
                        attachments = global_attachments
                        transaction['attachments'] = global_attachments

                if attachments:  # If transactions attachments exist upload to list
                    transaction_attachments.append(attachments)


        transaction_ids = self.database_handle.upload_archive_transactions(transactions_data)  # Will ignore
        # to_email, cc_email and attachments when uploading

        transaction_attachments = self.process_attachments(transaction_ids, transaction_attachments)  # Process
        # attachments will rearrange our dictionary to be {file_path: [transactions]}

        transaction_id_iterator = iter(transaction_ids)
        for transaction_list in transactions.values():  # Goes through transactions
            # and appends the transaction id

            # I want to place the list of transactions for the same from_email in the
            # queue and it will have the email and attachment info which differs from upload_transactions() method
            for transaction in transaction_list:
                transaction['transaction_id'] = next(transaction_id_iterator, None)

        self.transaction_queue.put(transactions, block=True, timeout=None)  # Place the transaction dict with {
        # from_email: {key: value}}
        # Upload the emails used to the archive db

        # Creates a list with tuple elements for to_emails
        for transaction_id, email_info in zip(transaction_ids, to_emails_info):
            contact_id = email_info[0]
            to_emails = email_info[1]

            transaction_email_info.append((transaction_id, contact_id, to_emails, 'to'))

        # Creates a list with tuple elements for cc_emails
        for transaction_id, email_info in zip(transaction_ids, cc_emails_info):
            contact_id = email_info[0]
            cc_emails = email_info[1]

            transaction_email_info.append((transaction_id, contact_id, cc_emails, 'cc'))

        self.database_handle.upload_archive_emails(transaction_email_info)
        return

    def process_attachments(self, transaction_ids, transaction_attachments):

        # At this point there will be a match in list position between transaction_id and attachments_id
        # We iterate over attachments to create a dictionary with {transaction_id: transaction_attachments}

        transaction_attachment_dict = {}

        if len(transaction_attachments) > 0:  # If contact transactions exist
            for transaction_id, attachments in zip(transaction_ids, transaction_attachments):
                for attachment in attachments:
                    try:
                        transaction_attachment_dict[str(transaction_id)].append(attachment)
                    except KeyError:
                        transaction_attachment_dict[str(transaction_id)] = [attachment]

        # transaction_attachments_dict = {'transaction_id': ['paths', ...]}

        consolidated_attachments = self.group_attachments(
            transaction_attachment_dict)  # Returns [path: [transaction_id,]]
        #  Now we need to upload the attachments and return the attachment ids.
        # So we can update our consolidated attachments path to use id instead

        attachment_info = self.database_handle.upload_archive_attachments(
            list(consolidated_attachments.keys()))  # Returns [attachment_id, path]
        # We need to use the attachment path to find the paths in consolidated_attachments and use attachment_id instead

        consolidated_attachments_copy = copy.deepcopy(consolidated_attachments)

        for attachment in attachment_info:
            for consolidated_attachment_path, consolidated_attachment_transaction_ids in consolidated_attachments_copy.items():
                if attachment[1] == consolidated_attachment_path:
                    consolidated_attachments[attachment[0]] = consolidated_attachments.pop(consolidated_attachment_path)
        self.database_handle.upload_archive_attachment_associations(consolidated_attachments)

        return consolidated_attachments_copy

    def group_attachments(self, transaction_attachments_dict):

        # transaction_attachments_dict = {'transaction_id': ['paths', ...]}
        # We need to create a dict with the key as the path and the transaction ids as the values
        consolidated_attachments = {}
        for transaction_id, attachment_paths in transaction_attachments_dict.items():
            for attachment_path in attachment_paths:
                if attachment_path in consolidated_attachments.keys():
                    if transaction_id not in consolidated_attachments[attachment_path]: # If global attachment and
                        # contact attachment are the same we only want one association
                        consolidated_attachments[attachment_path].append(transaction_id)
                else:
                    consolidated_attachments[attachment_path] = [transaction_id]
        return consolidated_attachments

    def start_transaction_sender_daemon(self):

        while True:
            # Block until a transaction is available in the queue
            from_email_transactions = self.transaction_queue.get(block=True, timeout=None)
            # Instant transactions will be a list with dict elements
            # Upload transactions will be a list with list elements
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit the task to the thread pool
                future = executor.submit(self.send_transactions, from_email_transactions)
                with self.thread_lock:
                    self.active_sender_threads += 1

                # Add a callback to track the completion of the task
            future.add_done_callback(lambda x: self.sender_thread_callback())
            time.sleep(0.01)


    def sender_thread_callback(self):
        with self.thread_lock:
            self.active_sender_threads -= 1

    def start_transaction_reader_daemon(self):
        # Thread that every minute reads DB and returns rows with scheduled send dates that are less than 1 minute of
        # the current date If within one minute it places it in the transaction queue
        self.database_handle = Database.Database()
        # Statement needs to find the difference between the current date and the send date
        # If the difference is less than 1 minute we will want the transactions

        # Construct and execute the query
        statement = """
              SELECT *
              FROM active_transactions
              WHERE send_date <= ?;
          """
        period = 30
        while True:
            # query database for transactions in transaction table that are within 1 minute

            # If it is place it in the transaction query. Use put(block=True, timeout=None) so that it waits until
            # que slot is available Else wait another monite Calculate the datetime for 30 seconds ago
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=period)

            # Format the datetime strings
            end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
            transactions_to_process = self.database_handle.execute_thread_safe_query(statement, 'fetchall',
                                                                                     (end_datetime_str,))
            # Execute code to do what is needed to process transactions
            # Should create a dictionary with {from_email: [transactions_list], from_email2: [transactions_list2],..}
            transaction_ids_to_remove = []
            from_transactions = {}

            for transaction in transactions_to_process:
                # Place transaction in queue

                # Get active transaction emails
                transaction = list(transaction)
                transaction_id = transaction[0]

                contact_id = transaction[1]
                to_emails, cc_emails = self.database_handle.get_active_emails(transaction_id, contact_id)
                transaction.insert(5, to_emails)
                transaction.insert(6, cc_emails)
                # Enter the attachments list with the paths for each transaction
                attachments = self.database_handle.get_attachments_by_transaction(
                    transaction_id)  # Returns a list with list elements [attachment_name, attachment_path]
                # for each attachment corresponding to the transaction_id
                transaction.insert(8, attachments)
                from_email = transaction[2]

                try:
                    from_transactions[from_email].append(transaction)
                except KeyError:
                    from_transactions[from_email] = [transaction]

                transaction_ids_to_remove.append((transaction[0],))  # Adds transaction id to list

                transaction.pop(0)
                transaction.insert(8, transaction_id)

            if from_transactions:
                self.transaction_queue.put(from_transactions, block=True, timeout=None)
                from_transactions = {}

            if transaction_ids_to_remove:
                self.database_handle.remove_active_transactions(transaction_ids_to_remove)

            time.sleep(period)  # WIll be 65
