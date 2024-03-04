import datetime
import random
from functools import partial
from cryptography.fernet import Fernet

from PyQt5.QtCore import Qt, pyqtSignal, QDateTime, QTime, QSize
from PyQt5.QtGui import QFont, QColor, QTextCursor, QFontMetrics, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QTabWidget, QVBoxLayout, \
    QHBoxLayout, QFrame, QCheckBox, QTextBrowser, QPushButton, QTextEdit, QScrollArea, QListWidget, QPlainTextEdit, \
    QLineEdit, QCalendarWidget, QDialog, QScrollBar, QComboBox, QInputDialog, QListWidgetItem, QSpacerItem, QSizePolicy, \
    QStyledItemDelegate, QTimeEdit, QToolButton, QProgressBar, QFormLayout, QCompleter, QToolBar, QAction

from QCorsoExtensions import QSearchWidget
import resources_rc
import sys
import os
from tkinter import filedialog

from re import compile
from bs4 import BeautifulSoup
import re

import Database
import TransactionEngine


heading_one = 24
heading_two = 18
heading_three = 16
media_info = {}
FONT = 'Roboto'
text_size = 12

password_key = '6cLEW86I06XOjv2V6lJZ7HayQrJJe8t9VpiSH7fnUFk='

edit_button_icon_path = ':resource/media/edit_icon.png'
delete_button_icon_path = ':resource/media/delete_icon.png'
add_button_icon_path = ':resource/media/add_icon.png'
new_contact_icon_path = ':resource/media/new_contact.png'
contact_icon_path = ':resource/media/contact.png'
new_file_icon_path = ':resource/media/new_file.png'
logo_icon_path = ':resource/media/demo_kick_logo.png'
help_button_path = ':resource/media/help_button.png'
from_email_icon_path = ':resource/media/new_from_email.png'
error_icon_path = ":resource/media/error_icon.png"
# When Add Contact is clicked, it should provide a

highlight_color = '#A367B1'
selected_color = '#392467'

button_style = f"""
        QPushButton {{
            outline: none;

        }}
        QPushButton:selected {{
            outline: none;
            background-color: #392467;
            color: white;
        }}
        QPushButton:hover {{
            background-color: #A367B1;
            color: white;
            outline: none;
        }}
        QPushButton:focus {{
            outline: none;
        }}
"""

button_selected_style = f"""
        QPushButton {{
            outline: none;
            background-color: #5D3587;
            color: white;
        }}
        QPushButton:selected {{
            outline: none;
        }}
        QPushButton:hover {{
            background-color: #A367B1;
            color: white;
            outline: none;
        }}
        QPushButton:focus {{
            outline: none;
        }}
"""

list_style_sheet = """
        QListWidget:item:hover {
            background-color: #A367B1;
            color: white;
            outline: 0px;
        }
        QListWidget:item:selected {
            background-color: #A367B1;
            color: white;
            outline: 0px;
        }        
"""

combobox_style_sheet = """
         QComboBox {
            color: white;
            background: #5D3587;
            outline: none;
            selection-background-color: #5D3587;

        }           
         QComboBox:selected {
            color: white;
            background: #5D3587;
        }           
        QComboBox QAbstractItemView {
            outline: none;
            selection-background-color: #5D3587;
        }
"""

checkbox_style_sheet = """
    QCheckBox::indicator:unchecked{
        border: 1px solid grey;
        background-color: white;
    }
    QCheckBox::indicator:unchecked:hover {
        background-color: #A367B1;
    }
    QCheckBox::indicator:checked:hover {
        background-color: #A367B1;
    }
    QCheckBox::indicator:unchecked:pressed {
        background-color: #392467;
    }
    QCheckBox::indicator:checked {
        background-color: #392467;
    }
"""

line_edit_style_sheet = """
    QLineEdit {
        border-color: #5D3587;
        outline: none;
    }
    QLineEdit:focus {
        border: 1px solid #392467;
        selection-background-color: #5D3587;
        outline: none;
    }
"""

text_edit_style_sheet = """
    QTextEdit:focus {
        border: 1px solid #392467;
        selection-background-color: #5D3587;
        outline: none;
    }
"""

calendar_style_sheet = """

    QCalendarWidget QWidget {
        background-color: #5D3587;
        color: white;
        outline: none;
        font: 12pt 'Roboto'; /* Example: 12pt size */
    }
    QCalendarWidget QToolButton {
        background-color: #A367B1;
        color: white;
    }
    QCalendarWidget QMenu {
        background-color: #A367B1;
        color: white;
    } 
    QCalendarWidget QSpinBox {
        background-color: #A367B1;
        color: white;
        selection-background-color: #5D3587;
    } 
    QCalendarWidget QPushButton {
        background-color: #FFD1E3; 
        color: white; 
    }
    QCalendarWidget QAbstractItemView:hover {
        background-color: #FFD1E3; 
        color: white; 
    }
    QCalendarWidget QAbstractItemView:selected {
        background-color: #5D3587;
        color: white; 
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: white; 
        selection-background-color: #A367B1;
        selection-color: white;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: white; 
        selection-background-color: #A367B1;
        selection-color: white;
    }
    QCalendarWidget QWidget{ 
        alternate-background-color: #A367B1;
        color: white;
    }
    QCalendarWidget QSpinBox::up-button { 
        subcontrol-origin: border;  
        subcontrol-position: top right;  
    }
    QCalendarWidget QToolButton#qt_calendar_nextmonth 
    {icon: url(right_arrow.png);}

    QCalendarWidget QWidget#qt_calendar_nextmonth{
       qproperty-icon:url ("media/next_arrow.png");
    }
"""

time_edit_style_sheet = """
    QTimeEdit {
        selection-background-color: #5D3587;
        selection-color: white;

    }
"""

progress_bar_style_sheet = """
    QProgressBar {
         border: 2px solid grey;
         border-radius: 5px;
         background-color: #5D3587;
     }

    QProgressBar::chunk {
        color: #5D3587; /* Color of the progress indicator */
    }
"""

scroll_bar_style = """

    QScrollBar:horizontal
    {
        height: 15px;
        margin: 3px 15px 3px 15px;
        border: 1px transparent #2A2929;
        border-radius: 4px;
        background-color: #392467;    /* #2A2929; */
    }

    QScrollBar::handle:horizontal
    {
        background-color: #A367B1;      /* #605F5F; */
        min-width: 5px;
        border-radius: 4px;
    }

    QScrollBar::add-line:horizontal
    {
        margin: 0px 3px 0px 3px;
        border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
        width: 10px;
        height: 10px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:horizontal
    {
        margin: 0px 3px 0px 3px;
        border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
    {
        border-image: url(:/qss_icons/rc/right_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }


    QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
    {
        border-image: url(:/qss_icons/rc/left_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
    {
        background: none;
    }


    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
    {
        background: none;
    }

    QScrollBar:vertical
    {
        background-color: #392467;
        width: 15;
        margin: 15px 3px 15px 3px;
        border: 1px transparent #2A2929;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical
    {
        background-color: #A367B1;         /* #605F5F; */
        min-height: 5px;
        border-radius: 4px;
    }

    QScrollBar::sub-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
    {
        border-image: url(:/qss_icons/rc/up_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
    {
        border-image: url(:/qss_icons/rc/down_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }
    
"""

tabs_style = """

    QTabBar::tab {
        min-height: 35px;
        
    }
    QTabBar::tab:hover {
        background-color: #A367B1; /* Set the hover background color */
        color: white;
    }
    QTabBar::tab:selected {
        background-color: #392467; /* Set the hover background color */
        color: white;
    }
    QTabBar QToolButton{
        background: white;
        border: 1px solid white;
    }
    QTabBar QToolButton:hover{
        background: white;
        border: 1px solid white;
    }
    QTabBar QToolButton::left-arrow:hover {
        color: white;
        background-color: #A367B1;
    }
    QTabBar QToolButton::right-arrow:hover {
        color: white;
        background-color: #A367B1;
    }
"""

toolbar_style = """
    QToolBar {
        background-color: #f0f0f0;
    }
    QToolButton { 
        background-color: transparent;
        border: none;
    }
    QToolButton:hover {
        background-color: #A367B1; 
    }
    QToolButton:pressed {
        background-color: #392467;
    }
"""

application_style = button_style + combobox_style_sheet + list_style_sheet + checkbox_style_sheet + line_edit_style_sheet + text_edit_style_sheet + calendar_style_sheet + time_edit_style_sheet + progress_bar_style_sheet + scroll_bar_style


def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return encrypted_data


def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data


def email_valid(email):
    # Regular expression for a basic email validation
    email_pattern = compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    # Check if the provided email matches the pattern
    if email_pattern.match(email):
        return True
    else:
        return False


def password_valid(password):
    return True


def html_paragraph_empty(html_content):
    if not html_content or html_content == '':
        return True
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraph_element = soup.find('p')
    # Check if the paragraph element is empty
    if paragraph_element and not paragraph_element.text.strip():
        return True
    else:
        return False


def reformat_date(date_string):
    parsed_date = datetime.datetime.strptime(date_string, '%a %b %d %H:%M:%S %Y')
    formated_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    # formated_date = parsed_date.strftime('%H:%M:%S %a %b %d %Y')
    return formated_date


class QClickableLabel(QLabel):
    label_clicked = pyqtSignal(str)
    mouse_hovering = pyqtSignal(str)
    mouse_exit = pyqtSignal(str)

    def __init__(self, label_text):
        super().__init__()
        self.setText(label_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.label_clicked.emit('left_click')

    def enterEvent(self, event):
        self.mouse_hovering.emit('hover')

    def leaveEvent(self, event):
        self.mouse_exit.emit('hover_leave')


class QErrorPrompt(QDialog):

    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle(title)
        # Create vertical layout
        # Will have title in big font and a message

        # Create title label
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont(FONT, heading_two))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Create message browser
        self.message_browser = QTextBrowser()
        self.message_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.message_browser.setFont(QFont(FONT, text_size))

        # Create push button
        self.ok_button = QPushButton('Ok')
        self.ok_button.setFocusPolicy(Qt.NoFocus)

        # Create html content so we can center the message
        html_content = f"<div align='center'>{message}</div>"
        self.message_browser.setHtml(html_content)
        self.message_browser.setAlignment(Qt.AlignCenter)

        # Add widgets
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.message_browser)
        self.layout.addWidget(self.ok_button)

        # Connect button
        self.ok_button.clicked.connect(self.okay_button_clicked)

    def okay_button_clicked(self):
        self.accept()

    def keyPressEvent(self, event):
        # Override keyPressEvent to capture the Return key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.accept()  # Call the accept function when Return key is pressed


class QAcceptDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)

        self.database_handle = database_handle
        # Set propeties
        self.width = 350
        self.height = 350
        self.resize(self.width, self.height)
        self.setWindowTitle(title)
        # Create the layout
        self.layout = QVBoxLayout(self)
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)

        # Create text browser
        self.dialog_message = QTextBrowser()

        self.dialog_message.setText(message)
        self.dialog_message.setReadOnly(True)

        self.dialog_message.setAlignment(Qt.AlignVCenter)
        self.dialog_message.setAlignment(Qt.AlignHCenter)

        # Create buttons
        self.accept_button = QPushButton('Accept')
        self.accept_button.setFocusPolicy(Qt.NoFocus)
        self.accept_button.setFocus()

        self.reject_button = QPushButton('Reject')
        self.reject_button.setFocusPolicy(Qt.NoFocus)

        # Add to layout
        self.buttons_layout.addWidget(self.accept_button)
        self.buttons_layout.addWidget(self.reject_button)

        self.layout.addWidget(self.dialog_message, )
        self.layout.addWidget(self.buttons_widget)

        # Connect buttons
        self.accept_button.clicked.connect(self.accept_dialog)
        self.reject_button.clicked.connect(self.reject_dialog)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.accept()

    def accept_dialog(self):
        # Emit the value_returned signal with the value from the line edit
        self.accept()

    def reject_dialog(self):
        self.reject()

    def center_on_main_window(self, main_window):
        # Calculate the center position relative to the main window
        main_window_geometry = main_window.geometry()
        width = main_window_geometry.width()
        height = main_window_geometry.height()
        x = main_window_geometry.x()
        y = main_window_geometry.y()

        center_x = x + (width - self.width / 2)
        center_y = y + (height - self.height / 2)

        self.move(int(center_x), int(center_y))


class QCreateContactFormDialog(QDialog):
    contact_info = pyqtSignal(dict)
    edited_contact_info = pyqtSignal(dict)
    edited_from_email = pyqtSignal(list)

    def __init__(self, database_handle, parent=None, contact_to_edit=None):
        super().__init__(parent)

        self.add_tag_layout = None
        self.add_tag_widget = None
        self.email_name_input_layout = None
        self.edit_from_email_button = None
        self.email_name_input_widget = None
        self.email_button_layout = None
        self.email_button_widget = None
        self.create_from_email_button = None
        self.database_handle = database_handle
        self.add_contact_tag_button = None
        self.tag_edit = None
        self.remove_tags_button = None
        self.contact_tags_list = None
        self.contact_tag_input_layout = None
        self.contact_tag_input_widget = None
        self.contact_tags_label = None
        self.contact_tags_layout = None
        self.contact_tags_widget = None
        self.add_email_button = None
        self.email_type_combo = None
        self.email_input_edit = None
        self.email_input_layout = None
        self.email_input_widget = None
        self.remove_email_button = None
        self.contact_emails_list = None
        self.email_input_layout = None
        self.email_input_widget = None
        self.contact_emails_label = None
        self.contact_emails_layout = None
        self.from_email_combobox = None
        self.from_email_label = None
        self.from_contact_email_layout = None
        self.from_contact_email_widget = None
        self.contact_name_line = None
        self.contact_name_label = None
        self.contact_name_layout = None
        self.contact_name_widget = None
        self.website_line = None
        self.website_label = None
        self.website_layout = None
        self.website_widget = None
        self.contact_emails_widget = None
        self.ig_followers_line = None
        self.ig_followers_label = None
        self.ig_followers_layout = None
        self.ig_followers_widget = None
        self.country_line = None
        self.country_label = None
        self.country_layout = None
        self.country_widget = None
        self.official_name_label = None
        self.official_name_line = None
        self.official_name_layout = None
        self.official_name_widget = None
        self.contact_to_edit = None
        if contact_to_edit:
            self.setWindowTitle(f'Editing [{contact_to_edit}]')
            self.contact_to_edit = contact_to_edit.split('.', maxsplit=1)
            if self.contact_to_edit:
                self.contact_to_edit = self.contact_to_edit[0]

        else:
            self.setWindowTitle('Create new contact form')

        self.setMaximumHeight(750)

        # Create the layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        # Create the forms layout

        self.contact_form_frame = QFrame()
        self.contact_form_layout = QVBoxLayout(self.contact_form_frame)
        self.contact_form_layout.setAlignment(Qt.AlignTop)
        self.contact_form_frame.setFrameShape(QFrame.Box)

        # Create the form widgets

        self.add_form_fields()

        # Create the buttons layout
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        # Create buttons
        self.submit_button = QPushButton('Save')
        self.submit_button.setFocusPolicy(Qt.NoFocus)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFocusPolicy(Qt.NoFocus)

        # Add widgets to button layout
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)

        # Add widget to main layout
        self.layout.addWidget(self.contact_form_frame)
        self.layout.addWidget(self.buttons_widget)

        # Connect buttons
        self.submit_button.clicked.connect(self.submit_form)
        self.cancel_button.clicked.connect(self.cancel_form)
        self.add_contact_tag_button.clicked.connect(self.add_tag_to_contact_form)

        # Populate information if edit button was clicked
        if contact_to_edit:
            self.populate_form_info(contact_to_edit)

    def populate_form_info(self, contact_to_edit):

        contact_id = contact_to_edit.split('.', maxsplit=1)
        if contact_id:
            contact_id = contact_id[0]
        else:
            return
        contact_info = self.database_handle.get_contacts_full_info(contact_id)

        self.official_name_line.setText(contact_info[0])  # Sets the official name field
        self.country_line.setText(contact_info[1])  # Sets the country field
        self.ig_followers_line.setText(str(contact_info[2]))  # Sets the ig followers field
        self.website_line.setText(contact_info[3])  # Sets the website info
        self.contact_name_line.setText(contact_info[4])  # Sets the contact name field

        if contact_info[5] != '':  # If there is a default from email
            contact_info[5] = self.database_handle.get_from_email_by_id(
                contact_info[5])  # Gets the actual email name from the email id
            self.from_email_combobox.setCurrentText(str(contact_info[5]))  # Set it to that
        else:  # If not
            self.from_email_combobox.setCurrentIndex(-1)  # Set it empty

        if contact_info[6] != '':  # If there is a default to emails
            for email in contact_info[6]:
                email = f'(to) : {email}'
                self.contact_emails_list.addItem(email)

        if contact_info[7] != '':  # If there is a default to emails
            for email in contact_info[7]:
                email = f'(cc) : {email}'
                self.contact_emails_list.addItem(email)

        if contact_info[8]:  # If tags exist
            for tag in contact_info[8]:
                self.contact_tags_list.addItem(tag)

    def add_tag_to_contact_form(self):
        tag = self.tag_edit.extract_text()

        if self.contact_tags_list.findItems(tag, Qt.MatchExactly):  # If tag is already on list
            QErrorPrompt('Tag already added', f'You have already added the tag {tag}.', parent=self)
        else:
            # Else add the tag to the list
            self.contact_tags_list.addItem(tag)

    def contact_valid(self):
        # Needs to ensure there doesn't exist a contact with the unique fields
        # Needs to ensure the required fields are included
        if self.official_name_line.text() == '':
            QErrorPrompt('Missing Official name', 'Missing the required official name of the contact.',
                         parent=self).show()
            return False
        if not self.ig_followers_line.text().isdigit() and self.ig_followers_line.text() != '':
            QErrorPrompt('Invalid Instagram followers', 'Instagram followers field should have number input.',
                         parent=self).show()
            return False
        if self.contact_emails_list.count() == 0:
            QErrorPrompt('Invalid number of emails provided', 'You should have at least one To email for the contact.',
                         parent=self).show()
            return False
        else:
            return True

    def get_dictionary_from_new_contact_form(self):
        # Gets widgets and extracts a dictionary with key value

        contact_info = dict()

        # Iterates through widgets and find the information needed to upload
        for widget in self.contact_form_frame.findChildren(QWidget):
            if widget.objectName() == 'official_name':
                contact_info['official_name'] = self.official_name_line.text().strip()

            elif widget.objectName() == 'country':
                contact_info['country'] = self.contact_name_line.text().strip()

            elif widget.objectName() == 'instagram_followers':
                contact_info['instagram_followers'] = self.ig_followers_line.text().strip()

            elif widget.objectName() == 'contact_website':
                contact_info['contact_website'] = self.website_line.text().strip()

            elif widget.objectName() == 'contact_name':
                contact_info['contact_name'] = self.contact_name_line.text().strip()

            elif widget.objectName() == 'from_email_combobox':
                from_email = self.from_email_combobox.currentText().lower()
                from_email_id = self.database_handle.get_source_email_id_by_name(from_email)
                contact_info['default_from_email_id'] = from_email_id

            elif widget.objectName() == 'emails':
                emails = []
                for i in range(widget.count()):
                    emails.append(widget.item(i).text())
                contact_info['contact_emails'] = emails

            elif widget.objectName() == 'tags':
                tags = []
                for i in range(widget.count()):
                    tags.append(widget.item(i).text())
                contact_info['contact_tags'] = tags

        return contact_info

    def create_new_contact(self, contact_info):
        if not self.database_handle.contact_exists(contact_info):  # If contact does not already exists
            # fields input matches in the DB
            contact_id = self.database_handle.upload_new_contact(contact_info)  # Uploads contact

            try:  # Try's to upload contact emails but if it doesn't exist (wasn't entered) add empty list
                self.database_handle.overwrite_contact_emails(contact_id, contact_info['contact_emails'])
            except KeyError:
                contact_info['contact_emails'] = []
                self.database_handle.overwrite_contact_emails(contact_id, contact_info['contact_emails'])

            try:
                self.database_handle.overwrite_contact_tags(contact_id, contact_info['contact_tags'])
            except KeyError:
                contact_info['contact_tags'] = []
                self.database_handle.overwrite_contact_tags(contact_id, contact_info['contact_tags'])

            # Needs to emit values to the list parent widget to display and be selectable
            self.contact_info.emit(contact_info)
            self.accept()
        else:
            accept_handle = QAcceptDialog('Contact Already Exists',
                                          'The contact with the selected information already exists would you like to overwrite?',
                                          parent=self)
            accept_handle.show()

            if accept_handle.exec_() == QDialog.Accepted:
                self.update_contact(contact_info)
                self.accept()

    def update_contact(self, contact_info):

        if self.contact_to_edit is None:
            if contact_info['official_name']:
                self.contact_to_edit = self.database_handle.get_contact_id_from_name(contact_info['official_name'])
            else:
                return
        try:
            emails = contact_info['contact_emails']
            del contact_info['contact_emails']

        except KeyError:
            emails = []
        try:
            tags = contact_info['contact_tags']
            del contact_info['contact_tags']
        except KeyError:
            tags = []

        self.database_handle.update_contact_information(self.contact_to_edit, list(contact_info.values()))
        self.database_handle.overwrite_contact_emails(self.contact_to_edit, emails)
        self.database_handle.overwrite_contact_tags(self.contact_to_edit, tags)

        self.accept()

    def submit_form(self):
        # Check that all fields are submitted as required. Add the values to the contact_info dictionary which
        # will be returned to be uploaded and the widget drawn
        # If contact info is invalid
        if self.contact_valid():
            contact_info = self.get_dictionary_from_new_contact_form()  # Returns a dictionary from the form values
            # submitted
            if not self.contact_to_edit:  # Checks if we're editing or creating. In this case we're creating new
                self.create_new_contact(contact_info)

            else:  # If contact already exists, we will update the info instead
                self.update_contact(contact_info)  # Updates contact info [0:6] is
                # the contact info that relates to the contacts table.

                contact_info['contact_id'] = self.contact_to_edit

                # Needs to emit values to the list parent widget to display and be selectable
                self.edited_contact_info.emit(
                    contact_info)  # Needs to emit the contact id and new contact info to populate contact widgets
                self.accept()

    def cancel_form(self):
        value = dict()
        self.reject()

    def add_form_fields(self):
        # Input for official name
        self.official_name_widget = QWidget()
        self.official_name_widget.setObjectName('official_name_widget')

        self.official_name_layout = QHBoxLayout(self.official_name_widget)
        self.official_name_layout.setObjectName('official_name_layout')

        self.official_name_label = QLabel('*Official Name:')
        self.official_name_label.setObjectName('official_name_label')

        self.official_name_line = QLineEdit()
        self.official_name_line.returnPressed.connect(self.submit_form)
        self.official_name_line.setPlaceholderText('Enter a name to address by the official name of this contact')
        self.official_name_line.setObjectName('official_name')

        self.official_name_layout.addWidget(self.official_name_label)
        self.official_name_layout.addWidget(self.official_name_line)

        # Input for country

        self.country_widget = QWidget()
        self.country_widget.setObjectName('country_widget')

        self.country_layout = QHBoxLayout(self.country_widget)
        self.country_layout.setObjectName('country_layout')

        self.country_widget.setObjectName('country_widget')

        self.country_label = QLabel('Country:')
        self.country_label.setObjectName('country_label')

        self.country_line = QLineEdit()
        self.country_line.returnPressed.connect(self.submit_form)
        self.country_line.setObjectName('country')

        self.country_line.setPlaceholderText('Enter the contacts country (Optional)')

        self.country_layout.addWidget(self.country_label)
        self.country_layout.addWidget(self.country_line)

        # Input for instagram followers

        self.ig_followers_widget = QWidget()
        self.ig_followers_widget.setObjectName('ig_followers_widget')

        self.ig_followers_layout = QHBoxLayout(self.ig_followers_widget)
        self.ig_followers_layout.setObjectName('ig_followers_layout')

        self.ig_followers_label = QLabel('Instagram followers:')
        self.ig_followers_label.setObjectName('ig_followers_label')

        self.ig_followers_line = QLineEdit()
        self.ig_followers_line.returnPressed.connect(self.submit_form)
        self.ig_followers_line.setObjectName('instagram_followers')

        self.ig_followers_line.setPlaceholderText('Enter the number of instagram followers (Optional)')

        self.ig_followers_layout.addWidget(self.ig_followers_label)
        self.ig_followers_layout.addWidget(self.ig_followers_line)
        self.ig_followers_layout.setObjectName('ig_followers_layout')

        # Input for contact website

        self.website_widget = QWidget()
        self.website_widget.setObjectName('website_widget')

        self.website_layout = QHBoxLayout(self.website_widget)
        self.website_layout.setObjectName('website_layout')

        self.website_label = QLabel('Contact website:')
        self.website_label.setObjectName('website_label')

        self.website_line = QLineEdit()
        self.website_line.returnPressed.connect(self.submit_form)
        self.website_line.setObjectName('contact_website')

        self.website_line.setPlaceholderText('Enter the URL of the contacts website (Optional)')

        self.website_layout.addWidget(self.website_label)
        self.website_layout.addWidget(self.website_line)

        # Input for contact name

        self.contact_name_widget = QWidget()
        self.contact_name_widget.setObjectName('contact_name_widget')

        self.contact_name_layout = QHBoxLayout(self.contact_name_widget)
        self.contact_name_layout.setObjectName('contact_name_layout')

        self.contact_name_label = QLabel('Contact name:')
        self.contact_name_label.setObjectName('contact_name_label')

        self.contact_name_line = QLineEdit()
        self.contact_name_line.returnPressed.connect(self.submit_form)
        self.contact_name_line.setObjectName('contact_name')
        self.contact_name_line.setPlaceholderText('Enter the human name for the contact (Optional)')

        self.contact_name_layout.addWidget(self.contact_name_label)
        self.contact_name_layout.addWidget(self.contact_name_line)

        # Input for contact emails

        # Create default from email selection widget

        self.from_contact_email_widget = QWidget()
        self.from_contact_email_widget.setObjectName('from_contact_email_widget')
        self.from_contact_email_layout = QHBoxLayout(self.from_contact_email_widget)
        self.from_contact_email_layout.setObjectName('from_contact_email_layout')

        self.from_email_label = QLabel('*Default from email:')
        self.from_email_label.setObjectName('default_from_email_id')
        self.from_email_combobox = QComboBox()
        self.from_email_combobox.setObjectName('from_email_combobox')

        # Create from email buttons
        self.create_from_email_button = QPushButton('')
        self.create_from_email_button.setFocusPolicy(Qt.NoFocus)
        self.create_from_email_button.setIcon(QIcon(add_button_icon_path))

        self.edit_from_email_button = QPushButton('')
        self.edit_from_email_button.setFocusPolicy(Qt.NoFocus)
        self.edit_from_email_button.setIcon((QIcon(edit_button_icon_path)))

        from_emails = self.database_handle.get_from_email_addresses()
        if from_emails:
            for email in from_emails:
                self.from_email_combobox.addItem(email)
        else:
            self.from_email_combobox.setCurrentText('')

        self.from_contact_email_layout.addWidget(self.from_email_label)
        self.from_contact_email_layout.addWidget(self.from_email_combobox, stretch=1)
        self.from_contact_email_layout.addWidget(self.create_from_email_button)
        self.from_contact_email_layout.addWidget(self.edit_from_email_button)

        # Contact emails widget
        self.contact_emails_widget = QFrame()
        self.contact_emails_widget.setFrameShape(QFrame.Box)
        self.contact_emails_widget.setObjectName('contact_emails_widget')

        self.contact_emails_layout = QHBoxLayout(self.contact_emails_widget)
        self.contact_emails_layout.setObjectName('contact_emails_layout')
        self.contact_emails_layout.setAlignment(Qt.AlignCenter)

        # Label
        self.contact_emails_label = QLabel('*Contact emails:')
        self.contact_emails_label.setObjectName('contact_emails_label')

        # Email input widget
        self.email_input_widget = QWidget()

        self.email_input_widget.setObjectName('email_list_button_widget')

        self.email_input_layout = QVBoxLayout(self.email_input_widget)
        self.email_input_layout.setObjectName('email_list_button_layout')

        self.contact_emails_list = QListWidget()  # List with emails
        self.contact_emails_list.setFocusPolicy(Qt.NoFocus)
        self.contact_emails_list.setObjectName('emails')
        self.contact_emails_list.setMaximumHeight(85)
        self.contact_emails_list.setSelectionMode(QListWidget.MultiSelection)

        # Create add and remove button
        # Email button widget
        self.email_button_widget = QWidget()
        self.email_button_layout = QHBoxLayout(self.email_button_widget)
        self.email_button_layout.setContentsMargins(0, 0, 0, 0)
        # Add button
        self.add_email_button = QPushButton('Add email')
        self.add_email_button.setFocusPolicy(Qt.NoFocus)
        self.add_email_button.setObjectName('add_email_button')

        # Remove button
        self.remove_email_button = QPushButton('Remove email')  # Used to remove listed emails
        self.remove_email_button.setFocusPolicy(Qt.NoFocus)
        self.remove_email_button.setObjectName('remove_email_button')

        # Add buttons to layout
        self.email_button_layout.addWidget(self.add_email_button)
        self.email_button_layout.addWidget(self.remove_email_button)

        # Email input
        self.email_name_input_widget = QWidget()
        self.email_name_input_widget.setObjectName('email_input_widget')

        self.email_name_input_layout = QHBoxLayout(self.email_name_input_widget)
        self.email_name_input_layout.setContentsMargins(0, 0, 0, 0)
        self.email_name_input_layout.setObjectName('email_input_layout')
        self.email_name_input_layout.setAlignment(Qt.AlignTop)

        # Email line edit
        self.email_input_edit = QLineEdit()
        self.email_input_edit.setObjectName('email_input_edit')
        self.email_input_edit.setPlaceholderText('Enter email')
        self.email_input_edit.returnPressed.connect(self.add_email_button_clicked)

        # Email type combobox (to or cc)
        self.email_type_combo = QComboBox()
        self.email_type_combo.setObjectName('email_type_combo')
        self.email_type_combo.addItem('to')
        self.email_type_combo.addItem('cc')

        # Add widgets to H Layout
        self.email_name_input_layout.addWidget(self.email_type_combo)
        self.email_name_input_layout.addWidget(self.email_input_edit, stretch=1)

        # Add components to email input/view widget
        self.email_input_layout.addWidget(self.contact_emails_list)
        self.email_input_layout.addWidget(self.email_name_input_widget)
        self.email_input_layout.addWidget(self.email_button_widget)

        # Add main elements to main email input widget
        self.contact_emails_layout.addWidget(self.contact_emails_label)
        self.contact_emails_layout.addWidget(self.email_input_widget)

        # Input for contact tags
        self.contact_tags_widget = QFrame()

        self.contact_tags_widget.setFrameShape(QFrame.Box)
        self.contact_tags_widget.setObjectName('contact_tags_widget')

        self.contact_tags_layout = QHBoxLayout(self.contact_tags_widget)
        self.contact_tags_layout.setObjectName('contact_tags_layout')
        self.contact_tags_layout.setAlignment(Qt.AlignTop)

        self.contact_tags_label = QLabel('Contact tags:')
        self.contact_tags_label.setObjectName('contact_tags_label')

        self.contact_tag_input_widget = QWidget()
        self.contact_tag_input_widget.setObjectName('contact_list_and_remove_widget')

        self.contact_tag_input_layout = QVBoxLayout(self.contact_tag_input_widget)
        self.contact_tag_input_layout.setObjectName('contact_list_and_remove_layout')

        self.contact_tags_list = QListWidget()
        self.contact_tags_list.setFocusPolicy(Qt.NoFocus)
        self.contact_tags_list.setObjectName('tags')
        self.contact_tags_list.setMaximumHeight(100)
        self.contact_tags_list.setSelectionMode(QListWidget.MultiSelection)

        self.remove_tags_button = QPushButton('Remove tag')
        self.remove_tags_button.setContentsMargins(0, 0, 0, 0)
        self.remove_tags_button.setFocusPolicy(Qt.NoFocus)
        self.remove_tags_button.setObjectName('remove_tags_button')
        self.remove_tags_button.clicked.connect(self.remove_tags_from_contact_form)

        # Add tag widget
        self.add_tag_widget = QWidget()
        self.add_tag_layout = QHBoxLayout(self.add_tag_widget)
        self.add_tag_layout.setContentsMargins(0, 0, 0, 0)

        self.tag_edit = QSearchWidget(self.database_handle)
        self.tag_edit.setObjectName('tag_edit')
        self.tag_edit.enter_pressed.connect(self.add_tag_to_contact_form)
        self.tag_edit.setPlaceholderText('Enter tags to describe the contact.')

        self.add_contact_tag_button = QPushButton('Add Tag')
        self.add_contact_tag_button.setFocusPolicy(Qt.NoFocus)
        self.add_contact_tag_button.setObjectName('add_contact_tag_button')

        # Add line edit and add button to layout
        self.add_tag_layout.addWidget(self.tag_edit)
        self.add_tag_layout.addWidget(self.add_contact_tag_button)

        self.contact_tag_input_layout.addWidget(self.contact_tags_list)
        self.contact_tag_input_layout.addWidget(self.add_tag_widget)
        self.contact_tag_input_layout.addWidget(self.remove_tags_button)

        self.contact_tags_layout.addWidget(self.contact_tags_label)
        self.contact_tags_layout.addWidget(self.contact_tag_input_widget)

        # Add widgets to contact form layout
        self.contact_form_layout.addWidget(self.official_name_widget)
        self.contact_form_layout.addWidget(self.country_widget)
        self.contact_form_layout.addWidget(self.ig_followers_widget)
        self.contact_form_layout.addWidget(self.website_widget)
        self.contact_form_layout.addWidget(self.contact_name_widget)
        self.contact_form_layout.addWidget(self.from_contact_email_widget)
        self.contact_form_layout.addWidget(self.contact_emails_widget)
        self.contact_form_layout.addWidget(self.contact_tags_widget)

        # Connect buttons
        self.add_email_button.clicked.connect(self.add_email_button_clicked)
        self.remove_email_button.clicked.connect(self.remove_emails_from_contact_form)
        self.create_from_email_button.clicked.connect(self.create_from_email)
        self.edit_from_email_button.clicked.connect(
            lambda: self.edit_from_email(self.from_email_combobox.currentText()))

    def remove_emails_from_contact_form(self):
        emails_to_remove = self.contact_emails_list.selectedItems()
        for email in emails_to_remove:
            email_item = self.contact_emails_list.findItems(email.text(), Qt.MatchExactly)
            for email_in_list in email_item:
                row = self.contact_emails_list.row(email_in_list)
                self.contact_emails_list.takeItem(row)

    def remove_tags_from_contact_form(self):
        tags_to_remove = self.contact_tags_list.selectedItems()
        for tag in tags_to_remove:
            tag_item = self.contact_tags_list.findItems(tag.text(), Qt.MatchExactly)
            for tag_in_list in tag_item:
                row = self.contact_tags_list.row(tag_in_list)
                self.contact_tags_list.takeItem(row)

    def add_email_button_clicked(self):
        # Check if email is already listed
        email = self.email_input_edit.text().strip()

        if self.email_listed(
                email) or email == '' or email == '' or not email_valid(
            email):
            QErrorPrompt('Invalid Email',
                         f'An invalid email was used ({email}). Please ensure you enter a valid email address.',
                         parent=self).show()
            return
        list_string = f'({self.email_type_combo.currentText()}) : {email}'
        self.contact_emails_list.addItem(list_string)
        self.email_input_edit.clear()

    def email_listed(self, new_email):
        for contact_email in range(self.contact_emails_list.count()):
            if self.contact_emails_list.item(contact_email).text() == new_email:
                return True
        return False

    def create_from_email(self):
        create_from_handle = QLinkEmailAccountForm(self.database_handle, parent=self)
        create_from_handle.email_created.connect(self.email_created)
        create_from_handle.show()

    def edit_from_email(self, from_email_to_edit):
        create_from_handle = QLinkEmailAccountForm(self.database_handle, from_email_to_edit=from_email_to_edit,
                                                   parent=self)
        create_from_handle.email_edited.connect(self.email_updated)
        create_from_handle.show()

    def email_updated(self, emails):
        index = self.from_email_combobox.findText(emails[1])
        if index != -1:
            self.from_email_combobox.setCurrentText(emails[1])
            self.edited_from_email.emit(emails)
        else:
            remove_index = self.from_email_combobox.findText(emails[0])
            self.from_email_combobox.removeItem(remove_index)

            self.from_email_combobox.addItem(emails[1])
            self.from_email_combobox.setCurrentText(emails[1])

    def email_created(self, email):

        self.from_email_combobox.addItem(email)
        self.from_email_combobox.setCurrentText(email)


class QHelpFromMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('How to connect from email')
        self.image_index = 0
        self.max_img_height = 600
        self.max_img_width = 600
        self.current_img = QLabel()
        self.current_img.setAlignment(Qt.AlignCenter)
        self.font = QFont()
        self.font.setPointSize(12)
        self.font.setFamily('Roboto')

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.header_help_label = QLabel('Below are some instruction on connecting your email.')

        domains = ['gmail', 'yahoo']
        self.gmail_images = [
            ':resource/media/instructions/gmail link instructions/first step.png',
            ':resource/media/instructions/gmail link instructions/second step.png',
            ':resource/media/instructions/gmail link instructions/third step.png',
            ':resource/media/instructions/gmail link instructions/fourth step.png',
            ':resource/media/instructions/gmail link instructions/fifth step.png',
            ':resource/media/instructions/gmail link instructions/sixth step.png',
        ]
        self.yahoo_images = [
            ':resource/media/instructions/yahoo link instructions/first step.png',
            ':resource/media/instructions/yahoo link instructions/second step.png',
            ':resource/media/instructions/yahoo link instructions/third step.png',
            ':resource/media/instructions/yahoo link instructions/fourth step.png',
            ':resource/media/instructions/yahoo link instructions/fifth step.png',
            ':resource/media/instructions/yahoo link instructions/sixth step.png',

        ]

        self.method_widget = QWidget()
        self.method_layout = QHBoxLayout(self.method_widget)
        self.method_label = QLabel('Domain type:')
        self.method_combobox = QComboBox()

        # Block signals, so we don't call populate when adding items
        self.method_combobox.blockSignals(True)
        for domain in domains:  # Add the domain types we will cover
            self.method_combobox.addItem(domain)
        self.method_combobox.blockSignals(False)

        self.method_layout.addWidget(self.method_label, alignment=Qt.AlignCenter)
        self.method_layout.addWidget(self.method_combobox, stretch=1)

        self.instruction_widget = QFrame()
        self.instruction_widget.setFrameShape(QFrame.Box)
        self.instruction_layout = QVBoxLayout(self.instruction_widget)
        self.instruction_text_browser = QTextBrowser()
        self.instruction_text_browser.setFont(self.font)
        self.instruction_text_browser.setStyleSheet("""
        background-color: #392467;
        color: white;
        """)
        self.instruction_layout.addWidget(self.instruction_text_browser)

        self.current_image_label = QLabel()
        self.current_image_label.setAlignment(Qt.AlignRight)

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)

        next_button_icon = QIcon(':resource/media/next_arrow_black.png')
        self.next_button = QPushButton()
        self.next_button.setFocusPolicy(Qt.NoFocus)
        self.next_button.setIcon(next_button_icon)
        self.next_button.clicked.connect(self.next_button_clicked)

        prev_button_icon = QIcon(':resource/media/previous_arrow_black.png')
        self.previous_button = QPushButton()
        self.previous_button.setFocusPolicy(Qt.NoFocus)
        self.previous_button.setIcon(prev_button_icon)
        self.previous_button.clicked.connect(self.previous_button_clicked)

        self.buttons_layout.addWidget(self.previous_button)
        self.buttons_layout.addWidget(self.next_button)

        self.instruction_layout.addWidget(self.current_img)
        self.instruction_layout.addWidget(self.current_image_label)
        self.instruction_layout.addWidget(self.buttons_widget, alignment=Qt.AlignBottom)

        self.layout.addWidget(self.header_help_label)
        self.layout.addWidget(self.method_widget)
        self.layout.addWidget(self.instruction_widget)

        self.method_combobox.currentTextChanged.connect(self.method_changed)

        self.populate_help_screen()

    def next_button_clicked(self):

        self.image_index = (self.image_index + 1) % len(self.gmail_images)
        self.populate_help_screen()

    def previous_button_clicked(self):
        self.image_index = (self.image_index - 1) % len(self.gmail_images)
        self.populate_help_screen()

    def method_changed(self):
        self.image_index = 0
        self.populate_help_screen()

    def populate_help_screen(self):
        if self.method_combobox.currentText() == 'gmail':
            image = QPixmap(self.gmail_images[self.image_index])
            image = image.scaled(QSize(self.max_img_width, self.max_img_height), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)

            self.current_img.setPixmap(image)
            self.instruction_text_browser.setMaximumHeight(150)

            self.instruction_text_browser.setHtml("""
                                <div style="text-align: center;"> \
                                <p>
For Gmail we can use the steps below to obtain the application password and to set the server and port.<br><br>
    
Server: smtp.gmail.com<br>
Port: 587 
                                </p>\
                                </div>""")

            self.current_image_label.setText(str(self.image_index + 1) + "/" + str(len(self.gmail_images)))

        elif self.method_combobox.currentText() == 'yahoo':
            image = QPixmap(self.yahoo_images[self.image_index])
            image = image.scaled(QSize(self.max_img_width, self.max_img_height), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)

            self.current_img.setPixmap(image)
            self.instruction_text_browser.setMaximumHeight(150)
            self.instruction_text_browser.setHtml("""
                    <div style="text-align: center;"> \
                    <p>
For Yahoo we can use the steps below to obtain the application password and to set the server and port.<br>

Server: smtp.mail.yahoo.com<br>
Port: 587<br>
                    </p> \
                    </div>""")

            self.current_image_label.setText(str(self.image_index + 1) + "/" + str(len(self.yahoo_images)))


class QLinkEmailAccountForm(QDialog):
    email_created = pyqtSignal(str)
    email_edited = pyqtSignal(list)

    def __init__(self, database_handle, from_email_to_edit=None, parent=None):
        super().__init__(parent)

        self.help_button = None
        self.email_port_edit = None
        self.email_port_label = None
        self.email_port_layout = None
        self.email_port_widget = None
        self.email_server_edit = None
        self.email_server_label = None
        self.server_name_layout = None
        self.server_name_widget = None
        self.api_line_edit = None
        self.api_label = None
        self.api_widget_layout = None
        self.api_widget = None
        self.source_select_combobox = None
        self.source_select_label = None
        self.source_select_layout = None
        self.source_select_widget = None
        self.database_handle = database_handle
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.from_email_id_to_edit = None
        self.from_email_to_edit = from_email_to_edit
        self.email_name_widget = None
        self.email_name_layout = None
        self.email_name_label = None
        self.email_name_edit = None
        self.email_password_widget = None
        self.email_password_layout = None
        self.email_password_label = None
        self.email_password_edit = None
        self.buttons_widget = None
        self.buttons_layout = None
        self.submit_button = None
        self.cancel_button = None

        if from_email_to_edit:  # If we're editing a from email account
            email_info = self.database_handle.get_from_email_info(from_email_to_edit)
            self.from_email_id_to_edit = email_info[0]  # Sets the ID of the from email ew're editing
            self.create_form_fields()  # We create the form fields
            self.populate_form()
        else:
            self.create_form_fields()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.submit_button_clicked()

    def create_form_fields(self):

        # Create form widgets
        if self.from_email_to_edit:  # If we're editing add the extra fields
            self.setWindowTitle('Editing from email')
            self.source_select_widget = QWidget()
            self.source_select_layout = QHBoxLayout(self.source_select_widget)
            self.source_select_label = QLabel('Account:')
            self.source_select_combobox = QComboBox()  # Combobox to select from account to edit.
            accounts = self.database_handle.get_from_email_addresses()  # Get all from accounts that exist in the DB

            for account in accounts:
                self.source_select_combobox.addItem(account)

            self.source_select_combobox.setCurrentText(self.from_email_to_edit)
            self.source_select_layout.addWidget(self.source_select_label)
            self.source_select_layout.addWidget(self.source_select_combobox, stretch=1)
            self.layout.addWidget(self.source_select_widget)
            button_content = 'Update'

        else:
            self.setWindowTitle('Creating from email')
            button_content = 'Create'

        # Create email name input widget
        self.email_name_widget = QWidget()  # Widget for email name input
        self.email_name_layout = QHBoxLayout(self.email_name_widget)

        # Create name label
        self.email_name_label = QLabel('Email:')

        # Create name line edit
        self.email_name_edit = QLineEdit()
        self.email_name_edit.returnPressed.connect(self.submit_button_clicked)
        self.email_name_edit.setPlaceholderText('Enter your email address here')

        # Create email pass input widget
        self.email_password_widget = QWidget()
        self.email_password_layout = QHBoxLayout(self.email_password_widget)

        # Create label
        self.email_password_label = QLabel('Password:')

        # Create line edit
        self.email_password_edit = QLineEdit()
        self.email_password_edit.setEchoMode(QLineEdit.Password)
        self.email_password_edit.setPlaceholderText('Enter your password here')

        # Create api widget components
        self.api_widget = QWidget()

        self.api_widget_layout = QHBoxLayout(self.api_widget)
        self.api_label = QLabel('API Key:')
        self.api_line_edit = QLineEdit()
        self.api_line_edit.setEchoMode(QLineEdit.Password)
        self.api_line_edit.setPlaceholderText('Enter the API key if needed')

        # Add widget components to api widget
        self.api_widget_layout.addWidget(self.api_label)
        self.api_widget_layout.addWidget(self.api_line_edit)
        self.api_widget_layout.addWidget(self.api_line_edit)

        # Create server name widget components
        self.server_name_widget = QWidget()
        self.server_name_layout = QHBoxLayout(self.server_name_widget)

        self.email_server_label = QLabel('Email server:')
        self.email_server_edit = QLineEdit()
        self.email_server_edit.setPlaceholderText('Enter the email server like "smtp.gmail.com"')

        # Add widget components to server name widget
        self.server_name_layout.addWidget(self.email_server_label)
        self.server_name_layout.addWidget(self.email_server_edit)

        # Create email port widget components
        self.email_port_widget = QWidget()
        self.email_port_layout = QHBoxLayout(self.email_port_widget)

        self.email_port_label = QLabel('Email port:')
        self.email_port_edit = QLineEdit()
        self.email_port_edit.setPlaceholderText('Enter the port to use')
        self.email_port_edit.setText('587')

        # Add widget components to email port widget
        self.email_port_layout.addWidget(self.email_port_label)
        self.email_port_layout.addWidget(self.email_port_edit)

        # Creates help button widget
        self.help_button = QPushButton('')
        self.help_button.setFocusPolicy(Qt.NoFocus)

        self.help_button.setMaximumWidth(45)
        self.help_button.setIcon(QIcon(help_button_path))

        # Create submit and cancel button widget

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)

        # Create submit button
        self.submit_button = QPushButton(button_content)
        self.submit_button.setFocusPolicy(Qt.NoFocus)

        # Create cancel button
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFocusPolicy(Qt.NoFocus)

        # Add widget components to form
        self.email_name_layout.addWidget(self.email_name_label)
        self.email_name_layout.addWidget(self.email_name_edit)

        self.email_password_layout.addWidget(self.email_password_label)
        self.email_password_layout.addWidget(self.email_password_edit)

        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)

        # Add a help button

        # Add widgets to form
        self.layout.addWidget(self.email_name_widget)
        self.layout.addWidget(self.email_password_widget)
        self.layout.addWidget(self.api_widget)
        self.layout.addWidget(self.server_name_widget)
        self.layout.addWidget(self.email_port_widget)
        self.layout.addWidget(self.buttons_widget, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.help_button, alignment=Qt.AlignRight)

        # Connect buttons
        self.submit_button.clicked.connect(self.submit_button_clicked)
        self.help_button.clicked.connect(self.help_from_form_clicked)
        self.cancel_button.clicked.connect(self.reject)

        if self.source_select_combobox:  # If we're editing connect the button
            self.source_select_combobox.currentIndexChanged.connect(self.populate_form)

    def help_from_form_clicked(self):
        help_dialog = QHelpFromMenu(self)
        help_dialog.show()

    def submit_button_clicked(self):
        # Should check if email account already exists
        # If it doesn't and its valid, it should upload to the database
        if self.email_name_edit.text() == '':
            # Display error that input is empty
            error_handle = QErrorPrompt('Email is empty!', f'Please enter a valid email address.', parent=self)
            error_handle.show()
            return
        if not email_valid(self.email_name_edit.text()):
            # Display error that email is invalid
            error_handle = QErrorPrompt('Invalid email!', f'{self.email_name_edit.text()} is an invalid email.',
                                        parent=self)
            error_handle.show()

            return
        if not password_valid(self.email_password_edit.text()):
            # Will check that password constraints are met
            # Display error if true
            pass
        if self.database_handle.email_account_exists(self.email_name_edit.text()) and not self.from_email_to_edit:
            # Display error that account already exists
            error_handle = QErrorPrompt('Email already exists!', f'{self.email_name_edit.text()} is already added. '
                                                                 f'Please edit the contact or select it to use.',
                                        parent=self)
            error_handle.show()

            return
        # Else it should upload it to the database and emit a signal so the from combo box can be updated.

        info = self.get_populated_info()

        if self.from_email_to_edit:  # Upload the edit
            self.database_handle.update_from_email(self.from_email_id_to_edit, info)
            self.email_edited.emit([self.source_select_combobox.currentText(), self.email_name_edit.text()])
        else:  # Upload the new from email
            self.database_handle.upload_from_information(info)
            self.email_created.emit(self.email_name_edit.text())

        self.accept()

    def get_populated_info(self):

        email = self.email_name_edit.text().lower().strip()
        password = encrypt_data(self.email_password_edit.text(), password_key)
        api_key = encrypt_data(self.api_line_edit.text(), password_key).strip()
        email_server = self.email_server_edit.text().lower().strip()
        email_port = self.email_port_edit.text()

        return [email, password, api_key, email_server, email_port]

    def populate_form(self):
        from_email = self.source_select_combobox.currentText()
        email_info = self.database_handle.get_from_email_info(from_email)
        self.email_name_edit.setText(email_info[1])
        self.email_password_edit.setText(decrypt_data(email_info[2], password_key))
        self.api_line_edit.setText(decrypt_data(email_info[3], password_key))
        self.email_server_edit.setText(email_info[4])
        self.email_port_edit.setText(str(email_info[5]))  # We convert to string since port is an int


class QConfirmTransactionDialog(QDialog):
    def __init__(self, transactions, total_transactions, parent=None):
        super().__init__(parent)

        # Set properties
        self.width = 350
        self.height = 550
        self.resize(self.width, self.height)
        self.setFixedWidth(self.width)

        self.setWindowTitle(f'Sending {total_transactions} transactions')

        # Create the layout
        self.layout = QVBoxLayout(self)

        # Create confirm header label
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setFamily('Arial')
        header_font.setUnderline(True)

        header = QLabel('Confirm transaction details')
        header.setFont(header_font)

        # Create scroll widest to hold transfer items
        self.scroll_widget = QScrollArea()
        self.scroll_widget.setStyleSheet(scroll_bar_style)
        self.scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_widget.setWidgetResizable(True)

        # Create content widget and layout
        self.content_widget = QWidget()
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)

        # Create dictionary with {'date': [total, emails, attachments]}
        totals_dict = {}
        global_send_date = transactions[-2]['send_date']
        global_attachments = transactions[-1]

        transactions = transactions[0:-2]  # [-2:] has the global send_date and global_attachments

        for transfer in transactions:  # Transfers

            send_date = transfer['send_date']
            if send_date is None and global_send_date is None:  # If sending instantly

                send_date = 'instant'

            elif transfer['send_date']:  # If contact has a contact level send date

                send_date = datetime.datetime.strptime(send_date, '%Y-%m-%d %H:%M:%S')
                send_date = send_date.strftime('%Y-%m-%d')

            else:

                send_date = datetime.datetime.strptime(global_send_date, '%Y-%m-%d %H:%M:%S')
                send_date = send_date.strftime('%Y-%m-%d')

            try:  # If the count for this send date exists
                # Add one to transfers total
                totals_dict[send_date][0] += 1

                # Add emails count to the total emails count
                totals_dict[send_date][1] += len(transfer['to_emails'])
                if transfer['cc_emails']:
                    totals_dict[send_date][1] += len(transfer['cc_emails'])

                # Add attachments count to the total attachments count
                if transfer['attachments']:
                    totals_dict[send_date][2] += len(transfer['attachments'])

                if global_attachments:
                    totals_dict[send_date][2] += len(global_attachments)

            except KeyError:  # Else start the count
                totals_dict[send_date] = [0, 0, 0]

                totals_dict[send_date][0] = 1
                totals_dict[send_date][1] = len(transfer['to_emails'])

                if transfer['cc_emails']:
                    totals_dict[send_date][1] += len(transfer['cc_emails'])


                if transfer['attachments']:
                    totals_dict[send_date][2] += len(transfer['attachments'])

                if global_attachments:
                    totals_dict[send_date][2] += len(global_attachments)

        self.create_date_widgets(totals_dict)

        # Create totals widget
        self.totals_widget = QWidget()
        self.totals_layout = QHBoxLayout(self.totals_widget)

        totals_spacer = QSpacerItem(70, 0)
        self.totals_label = QLabel('Total transactions:')
        self.totals_count = QLineEdit()
        self.totals_count.setText(str(total_transactions))
        self.totals_count.setReadOnly(True)

        # Add widgets to total widget
        self.totals_layout.addItem(totals_spacer)
        self.totals_layout.addWidget(self.totals_label)
        self.totals_layout.addWidget(self.totals_count)

        # Create the buttons widget
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)

        # Create buttons
        self.accept_button = QPushButton('Send')
        self.accept_button.setFocusPolicy(Qt.NoFocus)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFocusPolicy(Qt.NoFocus)

        # Add to layout
        self.buttons_layout.addWidget(self.accept_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addWidget(header, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.layout.addWidget(self.scroll_widget)
        self.layout.addWidget(self.totals_widget, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.buttons_widget, alignment=Qt.AlignBottom)

        # Connect buttons
        self.accept_button.clicked.connect(self.accept_dialog)
        self.cancel_button.clicked.connect(self.reject)

    def accept_dialog(self):
        # Emit the value_returned signal with the value from the line edit
        self.accept()

    def center_on_main_window(self, main_window):
        # Calculate the center position relative to the main window
        main_window_geometry = main_window.geometry()
        width = main_window_geometry.width()
        height = main_window_geometry.height()
        x = main_window_geometry.x()
        y = main_window_geometry.y()

        center_x = x + (width - self.width / 2)
        center_y = y + (height - self.height / 2)

        self.move(int(center_x), int(center_y))


    def create_date_widgets(self, totals_dict):

        # We need to go through dict and sort the elements by instant -> later dates
        # Sort dictionary items based on the date key
        sorted_items = sorted(totals_dict.items())

        # Move 'instant' key to the front
        try:
            sorted_items.insert(0, sorted_items.pop(sorted_items.index(('instant', totals_dict['instant']))))
        except KeyError:
            pass
        # Create a new dictionary from the sorted items
        sorted_totals_dict = dict(sorted_items)


        for day_info in sorted_totals_dict.items():

            day_transfer_widget = QTransactionTotalItem(day_info)
            self.content_layout.addWidget(day_transfer_widget)

        # Set content widget as the scroll widget widget
        self.scroll_widget.setWidget(self.content_widget)


class QTransactionTotalItem(QWidget):
    def __init__(self, info):
        super().__init__()
        self.setFocusPolicy(Qt.NoFocus)
        day = info[0]
        self.totals = list(info[1])

        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        # Create button with day
        self.toggle_visibility_button = QPushButton(day)
        self.toggle_visibility_button.setStyleSheet(button_selected_style)
        self.toggle_visibility_button.setContentsMargins(5, 5, 5, 0)
        self.toggle_visibility_button.setFocusPolicy(Qt.NoFocus)

        # Create visible frame
        self.visible_widget = QWidget()
        self.visible_widget.setContentsMargins(5, 0, 5, 0)

        self.visible_layout = QVBoxLayout(self.visible_widget)
        self.visible_widget.setVisible(True)

        # Create scroll widget
        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)

        # Create total fields
        self.create_totals_fields()

        # Add widgets to visible frame
        self.visible_layout.addWidget(self.content_widget)

        # Add widgets to main layout
        self.layout.addWidget(self.toggle_visibility_button)
        self.layout.addWidget(self.visible_widget)


    def create_totals_fields(self):

        # Create total transactions widget
        total_transactions_widget = QWidget()
        total_transactions_layout = QHBoxLayout(total_transactions_widget)


        total_transactions_label = QLabel('Total transactions:')
        total_transactions_label.setAlignment(Qt.AlignRight)
        total_transactions_line = QLineEdit()
        total_transactions_line.setText(str(self.totals[0]))
        total_transactions_line.setReadOnly(True)

        # Add widgets to total transactions widget
        total_transactions_layout.addWidget(total_transactions_label)
        total_transactions_layout.addWidget(total_transactions_line)

        # Create total emails widget
        total_emails_widget = QWidget()
        total_emails_layout = QHBoxLayout(total_emails_widget)

        # Create widget elements
        total_emails_label = QLabel('Total emails:')
        total_emails_label.setAlignment(Qt.AlignRight)
        total_emails_line = QLineEdit()
        total_emails_line.setText(str(self.totals[1]))
        total_emails_line.setReadOnly(True)

        # Add widgets to total emails widget
        total_emails_layout.addWidget(total_emails_label)
        total_emails_layout.addWidget(total_emails_line)

        # Create total attachments widget
        total_attachments_widget = QWidget()
        total_attachments_layout = QHBoxLayout(total_attachments_widget)

        # Create attachment widget elements
        total_attachments_label = QLabel('Total attachments:')
        total_attachments_label.setAlignment(Qt.AlignRight)
        total_attachments_line = QLineEdit()
        total_attachments_line.setText(str(self.totals[2]))
        total_attachments_line.setReadOnly(True)

        # Add elements to total attachments widget
        total_attachments_layout.addWidget(total_attachments_label, alignment=Qt.AlignRight)
        total_attachments_layout.addWidget(total_attachments_line)

        # Add widgets to consent widget
        self.content_layout.addWidget(total_transactions_widget)
        self.content_layout.addWidget(total_emails_widget)
        self.content_layout.addWidget(total_attachments_widget)

        # Connect buttons
        self.toggle_visibility_button.clicked.connect(self.toggle_widget_visibility)

    def toggle_widget_visibility(self):
        if self.visible_widget.isVisible():
            self.visible_widget.setVisible(False)
            self.toggle_visibility_button.setStyleSheet(button_style)
        else:
            self.visible_widget.setVisible(True)
            self.toggle_visibility_button.setStyleSheet(button_selected_style)


class QSelectContactsDialog(QDialog):

    # Should show the contacts that exist in DB and should provide some filter options
    # Will also indicate the already selected contact by highlighting them
    edited_contact_info_parent = pyqtSignal(dict)
    contact_deleted = pyqtSignal(list)
    from_email_edited = pyqtSignal(list)

    def __init__(self, contacts_already_listed, database_handle, parent=None):
        super().__init__(parent)

        self.database_handle = database_handle
        self.contacts_already_listed = contacts_already_listed
        self.edit_contacts_dialog = None
        self.setWindowTitle('Select contacts to add')
        self.create_contact_dialog = None

        # Create layout
        self.layout = QVBoxLayout(self)

        # Create edit buttons area widget
        self.edit_buttons_widget = QWidget()
        self.edit_buttons_layout = QHBoxLayout(self.edit_buttons_widget)
        self.edit_buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Create actual buttons
        self.add_selected_contacts_button = QPushButton('Select')
        self.add_selected_contacts_button.setFocusPolicy(Qt.NoFocus)
        self.add_selected_contacts_button.setStyleSheet(button_style)

        self.edit_selected_contacts_button = QPushButton('')
        self.edit_selected_contacts_button.setFocusPolicy(Qt.NoFocus)

        self.edit_selected_contacts_button.setToolTip('Edit the selected contact')
        self.edit_selected_contacts_button.setStyleSheet(button_style)
        self.edit_selected_contacts_button.setMaximumWidth(50)
        edit_icon = QIcon(edit_button_icon_path)
        self.edit_selected_contacts_button.setIcon(edit_icon)

        icon = QIcon(new_contact_icon_path)
        self.create_new_contact_button = QPushButton('')
        self.create_new_contact_button.setFocusPolicy(Qt.NoFocus)

        self.create_new_contact_button.setToolTip('Create a new contact')
        self.create_new_contact_button.setStyleSheet(button_style)
        self.create_new_contact_button.setMaximumWidth(50)
        self.create_new_contact_button.setIcon(icon)

        # Create delete contact button
        self.remove_contact_button = QPushButton()
        self.remove_contact_button.setFocusPolicy(Qt.NoFocus)
        self.remove_contact_button.setMaximumWidth(50)
        remove_icon = QIcon(delete_button_icon_path)
        self.remove_contact_button.setIcon(remove_icon)
        self.remove_contact_button.clicked.connect(self.remove_contact)

        # Add widgets to edit buttons layout
        self.edit_buttons_layout.addWidget(self.add_selected_contacts_button)
        self.edit_buttons_layout.addWidget(self.edit_selected_contacts_button)
        self.edit_buttons_layout.addWidget(self.create_new_contact_button)
        self.edit_buttons_layout.addWidget(self.remove_contact_button)

        # Create the filter list button which will add a filter into
        # the layout which will remove items from the list if they dont meet the specified filter.
        self.filter_list_widget = QFilterWidget(self.database_handle, 'contacts')

        # Create the list which will list the selectable and not selectable contacts
        self.list_widget = QListWidget()
        self.list_widget.setItemDelegate(CenteredItemDelegate())
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.itemDoubleClicked.connect(self.accept)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)  # Allows click and drag selection
        # and multiple row selections
        self.list_contacts(None)

        # Connect buttons
        self.add_selected_contacts_button.clicked.connect(self.accept)
        self.create_new_contact_button.clicked.connect(self.create_contact_clicked)
        self.edit_selected_contacts_button.clicked.connect(self.edit_contacts_clicked)

        # Add widgets to layout
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.filter_list_widget)
        self.layout.addWidget(self.edit_buttons_widget)

        # Connect signal of updated filter button clicked
        self.filter_list_widget.filter_updated.connect(self.list_contacts)
        self.filter_list_widget.filter_reset.connect(lambda : self.list_contacts(None))

    def list_contacts(self, filters):
        # Should list the contacts and apply formatting to indicate the contacts that are already listed
        # Will also apply filters before listing the contact
        self.list_widget.clear()
        all_contacts = self.database_handle.get_contacts_basic_info(filters)  # Get all the contacts the user has
        # created
        for contact in all_contacts:  # List the contact after filter is applied to the list
            # Formats it with client id and contact name
            # Will also check if the contact is already listed and if so,
            # it will format it in some manner. (For now we will just make row highlighted)
            contact_is_listed = False
            for contact_listed in self.contacts_already_listed:  # Checks if the contact is  already listed and
                # adds formatting if contact is already listed
                if int(contact_listed[0]) == contact[0]:  # if contact ids match
                    # contact_listed[1] = contact_official_name
                    contact_is_listed = True  # If contact is found listed set flag to true
                    # so the selection statement below is aware

                    item = QListWidgetItem()
                    item.setText(f'{contact_listed[0]}. {contact_listed[1]}')
                    self.list_widget.addItem(item)

                    selected_color_code = "#392467"  # Example hex color code (red)
                    self.list_widget.item(self.list_widget.count() - 1).setBackground(
                        QColor(selected_color_code))  # Add
                    self.list_widget.item(self.list_widget.count() - 1).setForeground(QColor('#FFFFFF'))  # Add
                    # background color to the contact that's already listed

            if not contact_is_listed:  # If contact wasn't listed we can add it normally
                self.list_widget.addItem(f'{contact[0]}. {contact[1]}')

    def contact_edited(self, contact_info):  # Called when a contact is submitted successfully in the edit contacts
        # widget
        # Contact info has the old official name. We need to find the id that matches and update the name in the list
        for contact in self.contacts_already_listed:
            if contact[0] == contact_info['contact_id']:
                contact[1] = contact_info['official_name']
                self.list_widget.clear()
                self.list_contacts(None)
                self.edited_contact_info_parent.emit(contact_info)
                return
        self.list_widget.clear()
        self.list_contacts(None)
        self.edited_contact_info_parent.emit(contact_info)

    def edit_contacts_clicked(self):  # Called whenever the edit button is clicked
        selected_items = self.get_selected_contacts()
        if not selected_items:
            return

        self.edit_contacts_dialog = QCreateContactFormDialog(self.database_handle, parent=self,
                                                             contact_to_edit=selected_items[-1])  #
        # Calls the create contact dialog form in edit mode
        self.edit_contacts_dialog.edited_contact_info.connect(self.contact_edited)  # Emits signal that
        self.edit_contacts_dialog.edited_from_email.connect(self.from_email_changed)
        # contact was edited when contact is edited so widgets can update

        self.edit_contacts_dialog.show()
        if self.edit_contacts_dialog.exec_() == QDialog.Accepted:
            return

    def create_contact_clicked(self):
        self.create_contact_dialog = QCreateContactFormDialog(self.database_handle, self)

        self.create_contact_dialog.show()
        if self.create_contact_dialog.exec_() == QDialog.Accepted:
            # If contact was created, re-query db to get updated contacts list
            self.list_widget.clear()
            self.list_contacts(False)
        else:
            return

    def get_selected_contacts(self):
        selected_items = []
        for item in self.list_widget.selectedItems():
            selected_items.append(item.text())
        return selected_items

    def filter_list(self):
        # Should clear the current list displayed
        # Should populate with the records that match the filter criteria
        contact = str(random.randint(0, 100))
        self.list_widget.clear()
        self.list_widget.addItem(contact)

    def remove_contact(self):

        # Should delete any active transaction for contact
        # Should delete the contact from DB
        selected_items = self.get_selected_contacts()
        if not selected_items:
            return
        accept_dialog = QAcceptDialog('Delete contact?', 'Are you sure you want to delete this contact? '
                                                        'This will delete all the scheduled and archived transactions '
                                                         'as well?')
        accept_dialog.show()
        if accept_dialog.exec_() == QDialog.Rejected:
            return

        contacts_to_remove = []
        for selected_contact in selected_items:
            contact_id_to_remove = selected_contact.split('.')[0] # Gets the contact id
            self.database_handle.delete_contact(contact_id_to_remove)
            contacts_to_remove.append(contact_id_to_remove)

        self.list_contacts(filters=None)
        self.contact_deleted.emit(contacts_to_remove)

    def from_email_changed(self, emails):
        self.from_email_edited.emit(emails)


class QFilterWidget(QWidget):

    filter_updated = pyqtSignal(list)
    filter_reset = pyqtSignal(str)

    def __init__(self, database_handle, table_name, custom_table=None):
        super().__init__()
        self.setMinimumWidth(590)

        self.database_handle = database_handle
        self.column_names = []

        if custom_table:
            for table in custom_table:
                self.column_names.extend(self.database_handle.get_table_columns(table))
        else:
            self.column_names = self.database_handle.get_table_columns(table_name)
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Create widgets
        self.toggle_filter_button = QPushButton('Hide filter')
        self.toggle_filter_button.setFocusPolicy(Qt.NoFocus)
        self.toggle_filter_button.setContentsMargins(0, 0, 0, 0)
        self.toggle_filter_button.setStyleSheet(button_selected_style)

        self.visible_widget = QWidget()
        self.visible_layout = QVBoxLayout(self.visible_widget)
        self.visible_widget.setVisible(True)

        self.scroll_widget = QScrollArea()
        self.scroll_widget.setWidgetResizable(True)
        no_border_scroll = scroll_bar_style + """
            QScrollArea{
                border: none;
            }
        """
        self.scroll_widget.setStyleSheet(no_border_scroll)

        self.scroll_widget.setContentsMargins(0, 0, 0, 0)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Create update and reset buttons widget
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)

        self.update_button = QPushButton('Update')
        self.update_button.setFocusPolicy(Qt.NoFocus)

        self.reset_button = QPushButton('Reset')
        self.reset_button.setFocusPolicy(Qt.NoFocus)

        # Add buttons to button layout
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.reset_button)

        # Add widgets to visible layout
        self.visible_layout.addWidget(self.scroll_widget)
        self.visible_layout.addWidget(self.buttons_widget)

        # Add widgets to main layout
        self.layout.addWidget(self.toggle_filter_button)
        self.layout.addWidget(self.visible_widget)

        self.create_dynamic_widgets()

        # Set scroll area widget
        self.scroll_widget.setWidget(self.content_widget)

        # Connect buttons
        self.toggle_filter_button.clicked.connect(self.toggle_filter_visibility)
        self.update_button.clicked.connect(self.update_button_clicked)
        self.reset_button.clicked.connect(self.reset_button_clicked)

    def toggle_filter_visibility(self):

        if self.visible_widget.isVisible():
            self.toggle_filter_button.setText('Show filter')
            self.toggle_filter_button.setStyleSheet(button_style)
            self.visible_widget.setVisible(False)
        else:
            self.toggle_filter_button.setText('Hide filter')
            self.toggle_filter_button.setStyleSheet(button_selected_style)
            self.visible_widget.setVisible(True)

    def create_dynamic_widgets(self):
        for column in self.column_names:
            filter_item = QFilterItem(column)
            self.content_layout.addWidget(filter_item)

    def update_button_clicked(self):
        filter_info = []

        for filter_item in self.content_widget.findChildren(QFilterItem):
            if filter_item.filter_enabled.isChecked():
                filter_info.append(filter_item.get_filter_data())

        self.filter_updated.emit(filter_info)

    def reset_button_clicked(self):
        for filter_item in self.content_widget.findChildren(QFilterItem):
            filter_item.clear()

        self.filter_reset.emit('reset')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_button_clicked()


class QFilterItem(QFrame):

    def __init__(self, column_name):
        super().__init__()
        self.column_name = column_name

        self.setFrameShape(QFrame.Panel)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setContentsMargins(10, 5, 10, 5)

        # Create checkbox to activate filter
        self.filter_enabled = QCheckBox()
        self.filter_enabled.setChecked(False)

        # Create a label with column name
        self.label = QLabel(column_name + ':')
        self.label = QClickableLabel(column_name + ':')
        self.label.label_clicked.connect(self.label_clicked)
        self.label.mouse_hovering.connect(self.mouse_hovering)
        self.label.mouse_exit.connect(self.mouse_exit)

        # Create a combobox with [equal to, contains, in, not equal to]
        conditions = ['equal to', 'contains', 'in', 'not equal to', 'not in', 'does not contain', 'greater than', 'less than']
        self.condition_type = QComboBox()
        self.condition_type.addItems(conditions)

        # Create line edit for input

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText('Enter the value')
        self.value_input.textChanged.connect(self.value_input_changed)

        self.layout.addWidget(self.filter_enabled)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.condition_type)
        self.layout.addWidget(self.value_input)

    def get_filter_data(self):
        condition_type = self.condition_type.currentText()
        value = self.value_input.text()
        return self.column_name, condition_type, value

    def label_clicked(self):
        self.filter_enabled.setChecked(not self.filter_enabled.isChecked())

    def mouse_hovering(self):
        updated_style = checkbox_style_sheet + """
            QCheckBox::indicator:unchecked{
                background-color: #A367B1;
            }
        """
        self.filter_enabled.setStyleSheet(updated_style)

    def mouse_exit(self):
        updated_style = checkbox_style_sheet + """
            QCheckBox::indicator:unchecked{
                background-color: white;
                border: 1px solid grey;
            }
        """
        self.filter_enabled.setStyleSheet(updated_style)

    def value_input_changed(self):
        if self.value_input.text() != '':
            self.filter_enabled.setChecked(True)
        else:
            self.filter_enabled.setChecked(False)

    def clear(self):
        self.filter_enabled.setChecked(False)
        self.condition_type.setCurrentText('equal to')
        self.value_input.setText('')


class QContactWidget(QWidget):
    # The actual contact widget that is displayed.
    # Also holds contact information like emails and options for the contact

    contact_selected = pyqtSignal(QWidget)  # Used signal to inform the QSendToContact widget that our selection/edit
    contact_edited_parent = pyqtSignal(dict)
    # button was clicked
    contact_removed = pyqtSignal(QWidget)  # Used signal to inform the QSendToContact widget that our remove
    from_email_updated = pyqtSignal(list)

    # Official contact name button style sheets

    def __init__(self, contact_id, contact_official_name, database_handle, parent=None, added_manually=False):
        super().__init__(parent)
        self.database_handle = database_handle
        self.contact_id, self.contact_official_name = contact_id, contact_official_name
        self.setObjectName(f'{self.contact_id}_{self.contact_official_name}_widget')
        self.added_manually = added_manually  # Dictates if the contact was added via "add to contact" or by tag
        self.personal_message = None  # Will hold the personal html message that is being sent to the contact.
        self.personal_message_subject_line = None  # Will be ignored and use global message if == ''
        self.from_email = None  # Email that we will be sending from as viewed by this contact. Should have a
        self.send_date = None  # When the email will be sent. Will be instant if its None
        self.attachments = []  # List that will hold the path of each of the attachments
        self.attachments_size = 0  # Float that will hold the value of the total attachments
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setFamily('Roboto')

        # option that can be set for each contact
        self.to_emails = []  # Emails that will be used to send to this contact
        self.cc_emails = []  # Emails that will  be used to cc to this contact
        self.from_email = self.database_handle.get_default_from_email_name(self.contact_id)
        self.to_emails, self.cc_emails = self.database_handle.get_contact_emails(self.contact_id)

        # Create layout
        self.contact_layout = QHBoxLayout(self)
        self.contact_layout.setContentsMargins(0, 0, 0, 0)

        # Create widgets
        self.contact_id_label = QLabel(str(contact_id))
        self.contact_id_label.setVisible(False)
        self.contact_id_label.setMaximumWidth(270)

        self.contact_official_name_button = QPushButton(contact_official_name)
        self.contact_official_name_button.setMinimumHeight(35)
        self.contact_official_name_button.setFont(self.font)
        self.contact_official_name_button.setFocusPolicy(Qt.NoFocus)
        self.contact_official_name_button.setStyleSheet(button_style)
        self.contact_official_name_button.setContentsMargins(0, 0, 0, 0)

        self.contact_buttons_widget = QWidget()
        self.contact_buttons_layout = QHBoxLayout(self.contact_buttons_widget)
        self.contact_buttons_layout.setContentsMargins(0, 0, 0, 0)

        icon = QIcon(edit_button_icon_path)
        self.edit_contact_button = QPushButton('')
        self.edit_contact_button.setMinimumSize(35, 35)
        self.edit_contact_button.setFocusPolicy(Qt.NoFocus)

        self.edit_contact_button.setStyleSheet(button_style)
        self.edit_contact_button.setContentsMargins(0, 0, 0, 0)
        self.edit_contact_button.setMaximumWidth(50)
        self.edit_contact_button.setIcon(icon)

        icon = QIcon(delete_button_icon_path)
        self.remove_contact_button = QPushButton('')
        self.remove_contact_button.setMinimumSize(35, 35)

        self.remove_contact_button.setFocusPolicy(Qt.NoFocus)

        self.remove_contact_button.setStyleSheet(button_style)
        self.remove_contact_button.setContentsMargins(0, 0, 0, 0)
        self.remove_contact_button.setMaximumWidth(50)
        self.remove_contact_button.setIcon(icon)
        # Add buttons to layout
        self.contact_buttons_layout.addWidget(self.edit_contact_button)
        self.contact_buttons_layout.addWidget(self.remove_contact_button)

        # Add widgets to layout
        self.contact_layout.addWidget(self.contact_id_label)
        self.contact_layout.addWidget(self.contact_official_name_button, stretch=1)
        self.contact_layout.addWidget(self.contact_buttons_widget, alignment=Qt.AlignRight)

        # Connect buttons
        self.contact_official_name_button.clicked.connect(self.contact_widget_selected)
        self.remove_contact_button.clicked.connect(partial(self.remove_contact_from_list))
        self.edit_contact_button.clicked.connect(partial(self.edit_contact_button_clicked))

    def edit_contact_button_clicked(self):
        edit_contact_form = QCreateContactFormDialog(self.database_handle, self,
                                                     contact_to_edit=f'{self.contact_id}. {self.contact_official_name_button.text()}')
        edit_contact_form.edited_contact_info.connect(self.contact_edited)
        edit_contact_form.edited_from_email.connect(self.from_email_changed)
        edit_contact_form.show()  # Sends the 'contact_id. official_name' string which is expected by the create/edit
        # contact widget

    def contact_edited(self, contact_info):

        self.contact_edited_parent.emit(contact_info)

    def contact_widget_selected(self):
        # Emits the signal and the dynamic widget
        # Will be captured in the Main window and passed to the sendTo widget to list the emails
        self.contact_selected.emit(self)

    def remove_contact_from_list(self):
        # Removes the widget from the listed contacts
        self.contact_removed.emit(self)

    def update_email_options(self, contact_options):
        # Updates contact widget info that will be used for sending later
        # Uses the dictionary passed from the QSendToContainer
        # Does not modify permanent contact options. Only for this current
        self.from_email = contact_options['from_email']
        self.to_emails = contact_options['to_emails']
        self.cc_emails = contact_options['cc_emails']

    def remove_email(self, email_to_remove):
        if email_to_remove in self.to_emails:
            self.to_emails.remove(email_to_remove)
        elif email_to_remove in self.cc_emails:
            self.cc_emails.remove(email_to_remove)

    def update_contact_date_options(self, complete_date_string):
        # Convert the input string to a datetime object
        date_format = 'yyyy-MM-dd HH:mm:ss'
        self.send_date = QDateTime.fromString(complete_date_string, date_format)

    def from_email_changed(self, emails):
        self.from_email_updated.emit(emails)


class QSendToContacts(QFrame):
    contact_selected_parent = pyqtSignal(QWidget)
    contact_selected_removed = pyqtSignal(QWidget)
    removed_all_contacts = pyqtSignal()
    contact_edited_parent = pyqtSignal(dict)
    from_email_updated = pyqtSignal(list)

    def __init__(self, database_handle):
        # Create frame, toolbar, and buttons
        super().__init__()

        self.database_handle = database_handle
        self.setMaximumWidth(500)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.current_contact_selected = None  # Will be used to keep track of the contact we have seleceted
        # Will hold record widget for each label widget
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setFamily('Roboto')

        self.sending_to_contacts_widget = QWidget()
        self.total_contacts = 0

        # Scroll area for label widgets
        self.sending_to_contacts_scroll_area = QScrollArea()
        self.sending_to_contacts_scroll_area.setStyleSheet(scroll_bar_style)
        self.sending_to_contacts_scroll_area.setWidgetResizable(True)
        self.sending_to_contacts_scroll_area.setWidget(self.sending_to_contacts_widget)

        self.sending_to_contacts_layout = QVBoxLayout(self.sending_to_contacts_widget)
        self.sending_to_contacts_layout.setAlignment(Qt.AlignTop)

        # Create counter widget
        self.contacts_counter_widget = QWidget()
        self.contacts_counter_layout = QHBoxLayout(self.contacts_counter_widget)
        self.contacts_counter_layout.setAlignment(Qt.AlignRight)
        self.contacts_counter_layout.setContentsMargins(0, 0, 0, 0)
        # Create elements of counter widget
        self.counter_label = QLabel('Contacts:')
        self.counter_spacer = QSpacerItem(400, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.counter_line_edit = QLineEdit()
        self.counter_line_edit.setText(str(self.total_contacts))
        self.counter_line_edit.setReadOnly(True)

        self.contacts_counter_layout.addItem(self.counter_spacer)
        self.contacts_counter_layout.addWidget(self.counter_label)
        self.contacts_counter_layout.addWidget(self.counter_line_edit)

        # Will hold buttons for adding a new label manually
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        # Create buttons
        self.add_contact_to_list_button = QPushButton('Add Contact')
        self.add_contact_to_list_button.setMinimumHeight(25)
        self.add_contact_to_list_button.setFont(self.font)
        self.add_contact_to_list_button.setFocusPolicy(Qt.NoFocus)

        self.add_contact_to_list_button.setToolTip('Import or create a contact')
        self.add_contact_to_list_button.setStyleSheet(button_style)

        self.remove_all_contacts_button = QPushButton('Remove All')
        self.remove_all_contacts_button.setMinimumHeight(25)
        self.remove_all_contacts_button.setFont(self.font)

        self.remove_all_contacts_button.setFocusPolicy(Qt.NoFocus)

        self.remove_all_contacts_button.setToolTip('Clear all imported contacts')
        self.remove_all_contacts_button.setStyleSheet(button_style)

        # Add button to buttons layout
        buttons_layout.addWidget(self.add_contact_to_list_button)
        buttons_layout.addWidget(self.remove_all_contacts_button)

        # Connect buttons
        self.add_contact_to_list_button.clicked.connect(self.add_contact_to_list)
        self.remove_all_contacts_button.clicked.connect(self.remove_all_contact_widgets)

        # Set frame shape
        self.setFrameShape(QFrame.Box)

        # Add layout to hold the labels container and the buttons
        self.layout.addWidget(self.sending_to_contacts_scroll_area)
        self.layout.addWidget(self.contacts_counter_widget)
        self.layout.addWidget(buttons_widget)

    def contact_widget_selected(self, contact_widget):
        # Emits the signal with the dynamic widgets value that was passed.
        # Will be captured in the Main window and passed to the sendTo widget to list the email
        found = False
        if self.current_contact_selected:  # If a contact was previously selected
            # We will reset the contact to white before selecting the new one
            self.current_contact_selected.contact_official_name_button.setStyleSheet(button_style)

        self.current_contact_selected = contact_widget
        if self.current_contact_selected:
            self.current_contact_selected.contact_official_name_button.setStyleSheet(button_selected_style)

        for __ in self.sending_to_contacts_scroll_area.findChildren(QContactWidget):
            found = True
            break
        if found:
            self.contact_selected_parent.emit(self.current_contact_selected)

    def remove_all_contact_widgets(self):
        self.current_contact_selected = None  # Remove the current contact selected reference

        widgets = self.sending_to_contacts_widget.findChildren(QContactWidget)
        if not widgets:
            return
        confirm_remove = QAcceptDialog('Remove all widgets?',
                                       'Are you sure you want to remove all the widgets from the queue, this will '
                                       'undo all edits?',
                                       parent=self)
        confirm_remove.show()
        if confirm_remove.exec_() == QDialog.Accepted:
            for widget in self.sending_to_contacts_widget.findChildren(QContactWidget):
                widget.deleteLater()
            self.removed_all_contacts.emit()

        self.total_contacts = 0
        self.counter_line_edit.setText(str(self.total_contacts))

    def get_listed_contacts(self):  # Gets the client id and official name of the listed contacts
        listed_contacts = []
        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact:
                listed_contacts.append([contact.contact_id, contact.contact_official_name])
        return listed_contacts

    def get_contact_widgets(self):
        listed_contacts = []
        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact:
                listed_contacts.append(contact)
        return listed_contacts

    def get_contact_widget_by_id(self, contact_id):

        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact:
                if contact.contact_id == contact_id:
                    return contact
        return None

    def get_listed_contact_widgets(self):
        # Returns a list of the contact_widgets currently listed
        listed_contact_widgets = []
        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact:
                listed_contact_widgets.append(contact)
        return listed_contact_widgets

    def edit_contact_widget(self, contact_info):
        contact = self.get_contact_widget_by_id(contact_info['contact_id'])

        if contact:  # If contact widget exists (was selected and is currently displayed)
            contact.contact_official_name_button.setText(contact_info['official_name'])
            contact.contact_official_name = contact_info['official_name']

    def add_contact_to_list(self):
        # Will display the available contacts
        # Will include a button to open the contact creation form to create a new contact
        # Will also display a list of the added contacts which can be manually included

        contacts_already_selected = self.get_listed_contacts()
        selected_contacts = QSelectContactsDialog(contacts_already_selected, self.database_handle,
                                                  parent=self)  # Display dialog and returns the selected contacts
        selected_contacts.contact_deleted.connect(self.contact_deleted_handle)
        selected_contacts.edited_contact_info_parent.connect(partial(self.edit_contact_widget))
        duplicate_contacts = []
        official_names = []
        contact_ids = []

        selected_contacts.show()
        if selected_contacts.exec_() == QDialog.Accepted:
            selected_items = selected_contacts.get_selected_contacts()  # Returns list of selected contacts with
            # client id and official name
            for contact in selected_items:
                # Goes through contacts and extracts client id and official name
                # Also checks if it already is painted and listed on the selected contact scroll area
                contact_id = contact.split('.', maxsplit=1)[0]  # Removes the client id .
                official_name = contact.split(' ', maxsplit=1)[1]
                # Create the contact widget that provides a remove contact button & edit button which has the name
                # and contact id (only for specific send does not edit the actual contact in DB)

                # Check if contact is already in the list
                if self.contact_listed(contact_id):
                    duplicate_contacts.append([official_name, contact_id])

                else:
                    # Here we need to create a widget with these values. That way the class can have information
                    # that can be used in the other widgets.
                    self.total_contacts += 1
                    contact_id = contact.split(' ', maxsplit=1)[0].replace('.', '')

                    contact_official_name = contact.split(' ', maxsplit=1)[1]
                    from_email = self.database_handle.get_default_from_email_name(contact_id)

                    contact_widget = QContactWidget(contact_id, contact_official_name, self.database_handle, self,
                                                    added_manually=True)
                    contact_widget.from_email = from_email

                    # Connect the edit and remove signals
                    contact_widget.contact_selected.connect(partial(self.contact_widget_selected, contact_widget))
                    contact_widget.contact_edited_parent.connect(self.contact_edited)
                    contact_widget.contact_removed.connect(partial(self.remove_contact_from_list, contact_widget))
                    contact_widget.from_email_updated.connect(self.from_email_changed)

                    # Add widget to contacts section
                    self.sending_to_contacts_layout.addWidget(contact_widget)

                # Gets the list of duplicate contacts to display 1 error
                for duplicate in duplicate_contacts:
                    official_names.append(duplicate[0])
                    contact_ids.append(duplicate[1])

            self.counter_line_edit.setText(str(self.total_contacts))
            contact_widget = self.sending_to_contacts_widget.findChild(QContactWidget)
            self.contact_widget_selected(contact_widget)

    def contact_edited(self, contact_info):
        self.edit_contact_widget(contact_info)
        self.contact_edited_parent.emit(contact_info)

    def contact_deleted_handle(self, contact_ids):
        for contact_id in contact_ids:
            contact = self.get_contact_widget_by_id(contact_id)
            self.remove_contact_from_list(contact)

    def add_matching_contacts_to_list(self, contact_info):
        contact_ids = contact_info[0]
        contact_official_names = contact_info[1]

        for contact_id, contact_official_name in zip(contact_ids, contact_official_names):
            contact_id = str(contact_id)
            # If contact is already listed it should ignore
            if not self.contact_listed(contact_id):
                self.total_contacts += 1
                contact_widget = QContactWidget(contact_id, contact_official_name, self.database_handle, self,
                                                added_manually=False)

                # Connect the edit and remove signals
                contact_widget.contact_selected.connect(partial(self.contact_widget_selected, contact_widget))
                contact_widget.contact_edited_parent.connect(self.contact_edited)
                contact_widget.contact_removed.connect(partial(self.remove_contact_from_list, contact_widget))

                # Add widget to contacts section
                self.sending_to_contacts_layout.addWidget(contact_widget)

        self.counter_line_edit.setText(str(self.total_contacts))

    def update_from_email_name(self, emails):
        # Will receive parameters [old_email, new_email]
        # Needs to find each contact with old_email and update to new_email
        old_email, new_email = emails
        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact.from_email == old_email:
                contact.from_email = new_email

    def remove_contact_from_list(self, contact_widget):
        if contact_widget is None:
            return

        if self.current_contact_selected == contact_widget:
            self.current_contact_selected = None
        self.contact_selected_removed.emit(contact_widget)
        self.total_contacts -= 1
        self.counter_line_edit.setText(str(self.total_contacts))
        contact_widget.deleteLater()

    def contact_listed(self, contact_id):
        # Go over the sending to widget which lists the contacts we're sending to
        for contact in self.sending_to_contacts_widget.findChildren(QContactWidget):
            if contact:
                if contact.contact_id == contact_id:
                    return True
        return False

    def update_contact_list_via_tags(self, tags):
        # Will be called when a tag is removed Will remove all contacts that do not have the added_contact_manually
        # flag set to True and with no matching tags
        matching_contacts = str(self.database_handle.get_matching_contacts_from_tags(tags))  # Gets the contact id of
        # the contacts which have a matching tag
        listed_contacts_widget = self.get_listed_contact_widgets()

        for contact in listed_contacts_widget:
            if contact:
                if contact.contact_id not in matching_contacts and not contact.added_manually:  # If contact is not
                    # listed in the matching contact list and was not added manually we will remove
                    self.total_contacts -= 1
                    contact.deleteLater()
                else:
                    pass
        self.counter_line_edit.setText(str(self.total_contacts))
        # For each contact in the list, query tag associations and if only one result

    def from_email_changed(self, emails):
        # Get contacts, update each contact widget if they have the email that was chagned.
        if self.current_contact_selected: # If a contact is selected we check if it has the updated email and update it
            if self.current_contact_selected.from_email == emails[0]:
                self.current_contact_selected.from_email = emails[1]
        contacts = self.get_contact_widgets()
        for contact in contacts:  # Go through all imported contacts and check if they have the updated email
            if contact.from_email == emails[0]:
                contact.from_email = emails[1]

        self.from_email_updated.emit(emails)  # Emit so we can change current combobox in contact options


class QEmailTextEditor(QFrame):

    # Will hold the email body tab (global and label) and the label properties which can be added into the email body
    # text editor
    def __init__(self, database_handle):
        super().__init__()

        self.database_handle = database_handle
        # Layout for the email body edit, buttons and label properties
        self.layout = QHBoxLayout(self)
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.contact_editing = None
        # Widget for the email body editor and buttons
        self.email_and_buttons_widget = QWidget()
        self.email_and_buttons_layout = QVBoxLayout(self.email_and_buttons_widget)

        # Create the email tabs so user can select global or label specific message
        self.email_tabs = QTabWidget()
        self.email_tabs.tabBar().setMinimumHeight(35)
        self.email_tabs.tabBar().setFont(self.font)
        self.email_tabs.setStyleSheet(tabs_style)

        self.global_body_widget = QWidget()
        self.global_body_widget.setToolTip('Used as the default email message when no personal message is specified')
        self.global_body_layout = QVBoxLayout(self.global_body_widget)

        subject_line_font = QFont()
        subject_line_font.setFamily('Arial')
        subject_line_font.setPointSize(16)

        body_font = QFont()
        body_font.setFamily('Arial')
        body_font.setPointSize(11)

        self.global_body_editor = QTextEdit()
        self.global_body_editor.setFont(body_font)
        self.global_body_subject_line = QLineEdit()
        self.global_body_subject_line.setFont(subject_line_font)

        self.global_body_subject_line.setPlaceholderText('Enter the subject line for the global email here.')
        self.use_global_message_flag = QCheckBox('Use global message for all transactions?')
        self.use_global_message_flag.setToolTip(
            'Check this to disregard any personal messages and use the global message for all contacts')

        self.global_body_layout.addWidget(self.global_body_subject_line)
        self.global_body_layout.addWidget(self.global_body_editor)
        self.global_body_layout.addWidget(self.use_global_message_flag, alignment=Qt.AlignRight)

        self.personal_body_widget = QWidget()
        self.personal_body_widget.setToolTip('Used to send contact specific messages')
        self.personal_body_layout = QVBoxLayout(self.personal_body_widget)
        self.personal_body_editor = QTextEdit()

        self.personal_body_editor.setFont(body_font)
        self.personal_body_subject_line = QLineEdit()
        self.personal_body_subject_line.setFont(subject_line_font)
        self.personal_body_subject_line.setPlaceholderText('Enter the subject line for the personal email here.')

        self.personal_body_layout.addWidget(self.personal_body_subject_line)
        self.personal_body_layout.addWidget(self.personal_body_editor)

        self.email_tabs.addTab(self.global_body_widget, 'Global Message')
        self.email_tabs.addTab(self.personal_body_widget, 'Personal Message')


        # Add the email tabs widget and the buttons to the layout
        self.email_and_buttons_layout.addWidget(self.email_tabs)

        # Create the label properties widget
        self.email_addons_widget = QEmailAddonsWidget(self.database_handle)
        self.email_addons_widget.field_selected_from_email_addons.connect(self.add_field_selected)

        # Add the emails and buttons widget and the label properties widget to the email text editor complete widget
        self.layout.addWidget(self.email_and_buttons_widget)
        self.layout.addWidget(self.email_addons_widget)

        self.setFrameShape(QFrame.Box)

    def add_field_selected(self, property_name):
        tab_selected = self.email_tabs.currentIndex()
        property_name = '{{' + property_name + '}}'

        if tab_selected == 0:  # If global message tab is open
            self.global_body_editor.insertHtml(property_name)
            self.global_body_editor.setFocus()  # Returns to Qtext edit so user can type

        else:
            self.personal_body_editor.insertHtml(property_name)
            self.personal_body_editor.setFocus()  # Returns to Qtext edit so user can type

    def save_message_clicked(self):
        if self.contact_editing is None:  # If no contact was clicked on for editing return
            return
        self.contact_editing.personal_message = self.personal_body_editor.toHtml()
        self.contact_editing.personal_message_subject_line = self.personal_body_subject_line.text()

    def clear_contacts(self):  # Called when remove all is clicked
        self.clear_global_message()
        self.clear_personal_message()
        self.email_addons_widget.clear_addons_data()

    def remove_contact_email_message(self, contact_widget):

        if self.contact_editing is None or contact_widget is None:
            return

        if contact_widget.contact_id == self.contact_editing.contact_id:
            self.clear_personal_message()

    def clear_personal_message(self):
        self.personal_body_subject_line.setText('')
        self.personal_body_editor.setHtml('')
        if self.contact_editing:
            self.contact_editing.personal_message = self.personal_body_editor.toHtml()

    def clear_global_message(self):
        self.global_body_editor.setHtml('')
        self.global_body_subject_line.setText('')

    def contact_selected(self, contact_widget):
        # Needs to set the personal message text to what the contact has
        if self.contact_editing is not None:  # If we were editing a contact email message and then we select another
            # we want it to stick so we save
            self.save_message_clicked()
        else:
            pass

        self.contact_editing = contact_widget

        # Import the contact personal message to texteditor
        if html_paragraph_empty(self.contact_editing.personal_message):
            self.personal_body_editor.setHtml('')
            contact_widget.personal_message = self.personal_body_editor.toHtml()
        else:
            self.personal_body_editor.setHtml(self.contact_editing.personal_message)

        # Import the contact subject line to the line edit
        if self.contact_editing.personal_message_subject_line is None:
            self.personal_body_subject_line.setText('')
        else:
            self.personal_body_subject_line.setText(self.contact_editing.personal_message_subject_line)

        # Call the contact selected method of the emails addons passing the contact_widget
        self.email_addons_widget.contact_selected(contact_widget)

    def get_global_email_attachments(self):
        attachments = self.email_addons_widget.get_global_email_attachments()
        return attachments


class QEmailAddonsWidget(QWidget):
    field_selected_from_email_addons = pyqtSignal(str)

    def __init__(self, database_handle):
        super().__init__()
        self.global_attachments_widget = None
        self.contacts_attachments_widget = None

        self.database_handle = database_handle
        self.setMinimumWidth(250)
        self.setMaximumWidth(500)
        self.layout = QVBoxLayout(self)

        self.dynamic_fields_widget = None
        self.scroll_widget = QWidget()

        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet(scroll_bar_style)
        self.scroll_area.setWidgetResizable(True)

        self.create_fields()
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

    def create_fields(self):
        # Create the dynamic fields widget
        self.dynamic_fields_widget = QDynamicProperties()
        self.dynamic_fields_widget.field_selected_parent.connect(self.dynamic_field_selected)

        self.global_attachments_widget = QAttachmentsWidget(self.database_handle, parent=self, global_attachments=True)
        self.contacts_attachments_widget = QAttachmentsWidget(self.database_handle, parent=self,
                                                              global_attachments=False)

        self.scroll_layout.addWidget(self.dynamic_fields_widget)
        self.scroll_layout.addWidget(self.global_attachments_widget)
        self.scroll_layout.addWidget(self.contacts_attachments_widget)

    def dynamic_field_selected(self, property_name):
        self.field_selected_from_email_addons.emit(property_name)

    def clear_addons_data(self):
        self.global_attachments_widget.clear_attachments()
        self.contacts_attachments_widget.clear_attachments()

    def contact_selected(self, contact_widget):
        self.contacts_attachments_widget.contact_selected(contact_widget)

    def get_global_email_attachments(self):
        return self.global_attachments_widget.get_email_attachments()


class QDynamicProperties(QWidget):
    field_selected_parent = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        properties = {'contact official name': 'official_name', 'country': 'country',
                      'instagram followers': 'instagram_followers', 'contact website': 'contact_website',
                      'contact name': 'contact_name',
                      'from name': 'from_name'}
        self.setToolTip('Used with the global widget as placeholder text')

        # Layout that will hold the toggle button and dynamic widget content
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        # Create header button that will toggle widget
        self.toggle_header_button = QPushButton('Show dynamic fields')
        self.toggle_header_button.setMinimumHeight(35)
        self.toggle_header_button.setFont(self.font)
        self.toggle_header_button.setStyleSheet(button_selected_style)

        # Create widget that will be toggled
        self.visible_widget = QWidget()
        self.visible_layout = QVBoxLayout(self.visible_widget)
        self.visible_layout.setAlignment(Qt.AlignTop)
        self.visible_widget.setVisible(True)

        # Create widget to hold content for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)

        # Create the scroll area
        self.scroll_area = QScrollArea(self.visible_widget)
        self.scroll_area.setWidgetResizable(True)

        # Create the dynamic field buttons
        for item in properties.items():
            property_item = QDynamicPropertyItem(item)
            property_item.field_selected.connect(self.field_selected)
            content_layout.addWidget(property_item)

        # Set the content widget as the scroll area widget
        self.scroll_area.setWidget(content_widget)

        # Add widgets to layout
        self.visible_layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.toggle_header_button)
        self.layout.addWidget(self.visible_widget)

        # Connect buttons
        self.toggle_header_button.clicked.connect(self.dynamic_fields_toggled)

    def dynamic_fields_toggled(self):
        if self.visible_widget.isVisible():
            self.visible_widget.setVisible(False)
            self.toggle_header_button.setText('Show dynamic fields')
            self.toggle_header_button.setStyleSheet(button_style)

        else:
            self.visible_widget.setVisible(True)
            self.toggle_header_button.setText('Hide dynamic fields')
            self.toggle_header_button.setStyleSheet(button_selected_style)

    def field_selected(self, property_name):
        # Emits the property name which was selected so the main window can connect it to the QEmailText editor to
        # add the field
        self.field_selected_parent.emit(property_name)


class QDynamicPropertyItem(QWidget):
    field_selected = pyqtSignal(str)

    def __init__(self, field_name):
        super().__init__()
        # Create a button with the property name
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)
        self.display_name = field_name[0]
        self.property_name = field_name[1]
        self.property_button = QPushButton(self.display_name)
        self.property_button.setFocusPolicy(Qt.NoFocus)

        self.property_button.clicked.connect(self.field_clicked)
        self.layout.addWidget(self.property_button)

    def field_clicked(self):
        # Needs to emit the property_name so that the QDynamicProperties widget can
        # emit a signal so that the QEmailTextEditor can add the {{field}}
        self.field_selected.emit(self.property_name)


class CenteredItemDelegate(QStyledItemDelegate):  # Used to set items in a QListWidget to be centered Horizontally
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)  # Calls the base class's (QStyledItemDelegate) initStyleOption()
        option.displayAlignment = Qt.AlignCenter
        option.font.setPointSize(12)


class QContactOptionsWidget(QFrame):
    email_edited_parent = pyqtSignal(list)

    # Will hold the To widget and the CC widget and any future options

    def __init__(self, database_handle):
        super().__init__()

        self.database_handle = database_handle
        self.setFrameShape(QFrame.Box)

        self.current_contact_editing = None
        self.emails_widget = None
        self.date_widget = None

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet(scroll_bar_style)
        self.scroll_area.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.emails_widget = QEmailContactsInfoWidget(None, self.database_handle)
        self.emails_widget.setToolTip('Sets the emails to use for this transaction on each contact')
        self.date_widget = QEmailTimeInfoWidget(None)  # Will be used to specify a date to send the email.
        self.date_widget.setToolTip('Sets the date for an email to send for a specific contact')

        # Add the to and checkbox selection options to the layout
        self.scroll_layout.addWidget(self.emails_widget)
        self.scroll_layout.addWidget(self.date_widget)

        self.layout.addWidget(self.scroll_area)

    def edit_contact_options(self, current_contact):
        self.current_contact_editing = current_contact
        self.emails_widget.edit_contact_info(self.current_contact_editing)
        self.date_widget.edit_contact_info(self.current_contact_editing)

    def contact_removed(self):
        self.current_contact_editing = None
        self.date_widget.current_contact_editing = None

    def from_email_changed(self, emails):
        if self.emails_widget.from_email.currentText() == emails[0]:
            index = self.emails_widget.from_email.findText(emails[0])
            self.emails_widget.from_email.removeItem(index)
            self.emails_widget.from_email.addItem(emails[1])
            self.emails_widget.from_email.setCurrentText(emails[1])

    def reinit_from_emails(self):
        from_emails = self.database_handle.get_from_email_addresses()

        if from_emails:  # If from emails exist
            self.emails_widget.from_email.clear()
            for email in from_emails:
                self.emails_widget.from_email.addItem(email)


class QAttachmentsWidget(QWidget):

    def __init__(self, database_handle, parent=None, global_attachments=False):

        super().__init__()
        self.global_attachments = global_attachments
        self.database_handle = database_handle
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.total_attachment_size = 0
        self.total_attachments = 0
        self.contact_editing = None

        self.visible_frame = QFrame()
        self.visible_frame.setFrameShape(QFrame.Box)

        if self.global_attachments:
            self.toggle_visibility_header = QPushButton('Hide global attachments')
        else:
            self.toggle_visibility_header = QPushButton('Hide contact attachments')

        self.toggle_visibility_header.setMinimumHeight(35)
        self.toggle_visibility_header.setFont(self.font)

        self.toggle_visibility_header.setStyleSheet(button_selected_style)
        self.visible_frame.setVisible(True)

        self.visible_frame_layout = QVBoxLayout(self.visible_frame)

        # Create the song info section (containing name and link info)
        self.attachment_info_widget = QWidget()
        attachment_info_layout = QVBoxLayout(self.attachment_info_widget)

        # Create media source sections
        attachment_source_label = QLabel('Path:')
        self.attachment_source_link = QLineEdit()
        self.attachment_source_link.setPlaceholderText('Enter file path for attachment')
        self.attachment_source_link.returnPressed.connect(
            lambda: self.add_attachment_to_list(self.attachment_source_link.text()))
        self.attachment_source_link.setReadOnly(False)
        icon = QIcon(add_button_icon_path)
        attachment_media_file_button = QPushButton('')
        attachment_media_file_button.setFocusPolicy(Qt.NoFocus)
        attachment_media_file_button.setIcon(icon)

        # Create and add the media source info to layout
        attachment_source_widget = QWidget()
        attachment_source_layout = QHBoxLayout(attachment_source_widget)
        attachment_source_layout.addWidget(attachment_source_label)
        attachment_source_layout.addWidget(self.attachment_source_link)
        attachment_source_layout.addWidget(attachment_media_file_button)

        # Add widgets to song info
        attachment_info_layout.addWidget(attachment_source_widget)
        self.visible_frame_layout.addWidget(self.attachment_info_widget)

        # Create the scroll area section that will display the song widgets that were added

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        scroll_area = QScrollArea(self.visible_frame)
        scroll_area.setWidgetResizable(True)

        scroll_area.setWidget(self.scroll_content)
        self.visible_frame_layout.addWidget(scroll_area)

        # Create the attachments count and MB total widgets
        self.attachments_total_widget = QWidget()
        self.attachments_total_layout = QVBoxLayout(self.attachments_total_widget)
        self.attachments_total_layout.setContentsMargins(0, 0, 0, 0)

        self.attachments_count_widget = QWidget()
        self.attachments_count_layout = QHBoxLayout(self.attachments_count_widget)
        self.attachments_count_layout.setContentsMargins(0, 0, 0, 0)
        self.attachment_count_label = QLabel('Attachments:')
        self.attachments_count_spacer = QSpacerItem(150, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.attachments_count_line = QLineEdit()
        self.attachments_count_line.setMaximumWidth(85)
        self.attachments_count_line.setReadOnly(True)

        self.attachments_count_line.setText(str(f'{self.total_attachments}'))

        self.attachments_count_layout.addWidget(self.attachment_count_label)
        self.attachments_count_layout.addItem(self.attachments_count_spacer)
        self.attachments_count_layout.addWidget(self.attachments_count_line)

        self.attachments_size_widget = QWidget()
        self.attachments_size_layout = QHBoxLayout(self.attachments_size_widget)
        self.attachments_size_layout.setContentsMargins(0, 0, 0, 0)

        self.attachments_size_label = QLabel('Total:')
        self.attachments_size_spacer = QSpacerItem(184, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.attachments_size_line = QLineEdit()
        self.attachments_size_line.setMaximumWidth(85)
        self.attachments_size_line.setReadOnly(True)
        self.attachments_size_line.setText(str(f'{self.total_attachment_size:.2f}MB'))

        self.attachments_size_layout.addWidget(self.attachments_size_label)
        self.attachments_size_layout.addItem(self.attachments_size_spacer)
        self.attachments_size_layout.addWidget(self.attachments_size_line)

        self.attachments_total_layout.addWidget(self.attachments_count_widget)
        self.attachments_total_layout.addWidget(self.attachments_size_widget)

        # Create the button section (will hold add widget button)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        self.add_attachment_button = QPushButton('Add attachment')
        self.add_attachment_button.setContentsMargins(50, 50, 50, 0)
        self.add_attachment_button.setFocusPolicy(Qt.NoFocus)

        buttons_layout.addWidget(self.add_attachment_button)

        self.visible_frame_layout.addWidget(self.attachments_total_widget)
        self.visible_frame_layout.addWidget(buttons_widget)

        self.layout.addWidget(self.toggle_visibility_header)
        self.layout.addWidget(self.visible_frame)

        # Connect buttons
        self.add_attachment_button.clicked.connect(
            lambda: self.add_attachment_to_list(self.attachment_source_link.text()))
        attachment_media_file_button.clicked.connect(self.add_attachment_file)
        self.toggle_visibility_header.clicked.connect(self.toggle_attachments)

    def toggle_attachments(self):
        if self.visible_frame.isVisible():
            if self.global_attachments:
                self.toggle_visibility_header.setText('Show global attachments')
            else:
                self.toggle_visibility_header.setText('Show contact attachments')

            self.toggle_visibility_header.setStyleSheet(button_style)
            self.visible_frame.setVisible(False)

        else:
            if self.global_attachments:
                self.toggle_visibility_header.setText('Hide global attachments')
            else:
                self.toggle_visibility_header.setText('Hide contact attachments')

            self.toggle_visibility_header.setStyleSheet(button_selected_style)

            self.visible_frame.setVisible(True)

    def add_attachment_file(self):

        files = filedialog.askopenfilenames()
        if files:
            for file in files:
                if self.add_attachment_to_list(file):  # If adding attachment was successful
                    if not self.global_attachments:  # If its a personal attachment widget we're working on
                        if self.contact_editing:  # Addd the file to the contact widget
                            self.contact_editing.attachments.append(file)
                            self.contact_editing.attachment_size = self.total_attachment_size

    def add_attachment_to_list(self, attachment_source_link):

        attachment_source_link = attachment_source_link.strip()

        # If song name or link is empty return
        if attachment_source_link == '':
            QErrorPrompt('Missing attachment path',
                         'Attach a file by clicking the + icon or typing the path in the text box.', parent=self).show()
            return False

        # If media widget already exists in list return
        if self.scroll_content.findChild(QEmailAttachment, attachment_source_link) is not None:
            QErrorPrompt('Attachment already selected', 'The selected attachment is already included.', parent=self)
            return False

        # If is not a valid link or path return
        if not os.path.isfile(attachment_source_link):
            QErrorPrompt('Invalid Path',
                         'Invalid path provided for file. Please use a valid file path.', parent=self)
            return False

        attachment_widget = QEmailAttachment(attachment_source_link)
        attachment_widget.setObjectName(attachment_source_link)
        attachment_widget.attachment_edit_clicked.connect(self.attachment_item_edit)
        attachment_widget.attachment_removed.connect(self.attachment_removed)

        # Update the float number with the total file size
        # Update the label representation

        self.total_attachment_size += attachment_widget.attachment_size
        self.attachments_size_line.setText(f'{self.total_attachment_size: .2f} MB')

        self.total_attachments += 1
        self.attachments_count_line.setText(str(self.total_attachments))

        self.attachment_source_link.clear()
        self.scroll_content.layout().addWidget(attachment_widget)

        return True

    def attachment_item_edit(self, attachment_info):

        attachment_path = attachment_info[0]
        attachment_size = attachment_info[1]

        if self.attachment_source_link.text() != '':
            attachment_widget = QEmailAttachment(self.attachment_source_link.text())
            self.scroll_layout.addWidget(attachment_widget)

        # Decrease total while we edit
        self.total_attachments -= 1
        self.total_attachment_size -= attachment_size

        self.attachments_count_line.setText(str(self.total_attachments))
        self.attachments_size_line.setText(f'{self.total_attachment_size: .2f} MB')
        self.attachment_source_link.setText(attachment_path)

    def attachment_removed(self, attachment_info):

        attachment_path = attachment_info[0]
        attachment_size = attachment_info[1]

        self.total_attachments -= 1
        self.total_attachment_size -= attachment_size

        self.attachments_count_line.setText(str(self.total_attachments))
        self.attachments_size_line.setText(f'{self.total_attachment_size: .2f} MB')

        # If its not a global attachment we remove the item from attachments list in contact widget.
        # We also reduce the total size
        if not self.global_attachments:
            if self.contact_editing:
                if attachment_path in self.contact_editing.attachments:
                    self.contact_editing.attachments.remove(attachment_path)
                self.contact_editing.attachment_size -= attachment_size

    def clear_attachments(self):
        for attachment in self.scroll_content.findChildren(QEmailAttachment):
            attachment.deleteLater()

        self.total_attachments = 0
        self.total_attachment_size = 0

        self.attachments_count_line.setText(str(self.total_attachments))
        self.attachments_size_line.setText(f'{self.total_attachment_size: .2f} MB')

    def get_email_attachments(self):
        attachments = []
        for attachment in self.scroll_content.findChildren(QEmailAttachment):
            attachments.append(attachment.attachment_source_line.text())

        return attachments

    def contact_selected(self, contact_widget):
        self.contact_editing = contact_widget
        self.clear_attachments()
        for attachment in self.contact_editing.attachments:
            self.add_attachment_to_list(attachment)


class QEmailAttachment(QWidget):
    attachment_removed = pyqtSignal(list)
    attachment_edit_clicked = pyqtSignal(list)

    def __init__(self, attachment_source_link):
        super().__init__()
        # Create H Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Create attachment name line edit

        # Create Media source line edit
        self.attachment_source_line = QLineEdit()
        self.attachment_source_line.setReadOnly(True)
        self.attachment_source_line.setText(attachment_source_link)
        self.attachment_source_line.setToolTip(attachment_source_link)
        # Create attachment size line edit
        self.attachment_size = 0
        self.attachment_size_line = QLineEdit()
        self.attachment_size_line.setMaximumWidth(50)
        self.attachment_size_line.setText('0MB')
        self.attachment_size_line.setReadOnly(True)

        self.find_attachment_size()

        # Create Edit button
        icon = QIcon(edit_button_icon_path)
        self.edit_attachment_button = QPushButton('')
        self.edit_attachment_button.setFocusPolicy(Qt.NoFocus)

        self.edit_attachment_button.setIcon(icon)
        self.edit_attachment_button.setMaximumWidth(25)

        # Create Remove button
        icon = QIcon(delete_button_icon_path)
        self.remove_attachment_button = QPushButton('')
        self.remove_attachment_button.setFocusPolicy(Qt.NoFocus)

        self.remove_attachment_button.setIcon(icon)

        self.remove_attachment_button.setMaximumWidth(25)

        # Add widgets to H Layout
        self.layout.addWidget(self.attachment_source_line, stretch=2)
        self.layout.addWidget(self.attachment_size_line)
        self.layout.addWidget(self.edit_attachment_button)
        self.layout.addWidget(self.remove_attachment_button)

        # Connect buttons
        self.remove_attachment_button.clicked.connect(self.remove_attachment)
        self.edit_attachment_button.clicked.connect(self.edit_attachment_button_clicked)

    def find_attachment_size(self):
        file_path = self.attachment_source_line.text()

        if os.path.isfile(file_path):
            # Get the file size in bytes
            size_bytes = os.path.getsize(file_path)

            # Convert bytes to megabytes
            size_mb = size_bytes / (1024.0 ** 2)

            # Update the QLineEdit with the formatted megabyte value
            self.attachment_size_line.setText(f"{size_mb:.2f} MB")

            # Update the float variable
            self.attachment_size = size_mb
        else:
            # Handle the case when the file doesn't exist
            self.attachment_size = 0.0

    def edit_attachment_button_clicked(self):
        # Get the path and return it to parent so it can edit it then delete the widget
        self.attachment_edit_clicked.emit([self.attachment_source_line.text(), self.attachment_size])
        self.deleteLater()

    def remove_attachment(self):
        self.attachment_removed.emit([self.attachment_source_line.text(), self.attachment_size])
        self.deleteLater()


class QTagsWidget(QFrame):
    tagRemoveParent = pyqtSignal(list)
    found_matching_tags = pyqtSignal(list)

    def __init__(self, database_handle, parent=None):
        super().__init__()
        self.database_handle = database_handle
        self.parent = parent
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        # Create widget layout
        self.layout = QVBoxLayout(self)  # Self must be passed as a param
        self.layout.setObjectName('tags_layout_widget')

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName('tags_scroll_widget')

        scroll_layout = QVBoxLayout(self.scroll_widget)
        scroll_layout.setAlignment(Qt.AlignTop)
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(scroll_bar_style)
        self.scroll_area.setObjectName('tags_scroll_area')
        self.scroll_area.setWidgetResizable(True)

        # Create the line edit
        self.tag_description_edit = QSearchWidget(self.database_handle, parent=self)
        self.tag_description_edit.setMinimumHeight(30)
        font = QFont()
        font.setPointSize(16)
        font.setFamily('Roboto')
        self.tag_description_edit.lineEdit().setFont(font)
        self.tag_description_edit.enter_pressed.connect(self.add_tag_to_media)
        self.tag_description_edit.setObjectName('tags_description_widget')
        self.tag_description_edit.setPlaceholderText('Type contact tags here to start importing contacts.')
        self.tag_description_edit.setToolTip('Add contact tags to find and import contacts.')

        # Create the buttons section
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        # Create button
        self.add_tag_button = QPushButton('Add Tag')
        self.add_tag_button.setFont(self.font)
        self.add_tag_button.setContentsMargins(0, 0, 0, 0)
        self.add_tag_button.setMinimumHeight(35)
        self.add_tag_button.setFocusPolicy(Qt.NoFocus)

        self.add_tag_button.setObjectName('add_tag_button')
        buttons_layout.addWidget(self.add_tag_button)

        # Add widgets to scroll area and scroll area to layout
        self.scroll_area.setWidget(self.scroll_widget)

        # Add the scroll area and buttons widget to tags widget
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.tag_description_edit)
        self.layout.addWidget(buttons_widget)

        # Set solid frame
        self.setFrameShape(QFrame.Box)

        self.add_tag_button.clicked.connect(self.add_tag_to_media)

    def add_tag_to_media(self):
        # Check if tag is not empty and not already in list
        tag_name = self.tag_description_edit.extract_text().lower().strip()

        self.scroll_widget = self.scroll_widget

        if tag_name == '':
            return
        if self.scroll_widget.findChild(TagItemWidget, tag_name) is not None:
            return
        self.database_handle.upload_new_tags((tag_name,), tag_description=None)  # Upload tag to DB
        tag_widget = TagItemWidget(tag_name)
        tag_widget.tagRemoved.connect(self.tag_removed)

        # Get value of tag_description_edit and create a tag_widget with its tag_description
        self.scroll_widget.layout().addWidget(tag_widget)

        # Using the tag, retrieve all contacts that have the associated tags
        # Create the contact widget in the contacts list
        self.list_contact_with_tags(tag_name)
        self.tag_description_edit.lineEdit().setText('')

    def list_contact_with_tags(self, tag):
        contact_ids = self.database_handle.get_contact_id_from_tag(
            tag)  # Should get the contact ids from database where contact has the specified tag
        contact_names = self.database_handle.get_contact_official_name_from_id(
            contact_ids)  # Should get the contact ids from database where contact has the specified tag
        if contact_ids is None or contact_names is None:
            return
        else:
            # contact_tag_associations that have the tag code passed as parameter
            # Using the IDs, it should pass a signal to the send to contacts widget to create the widget in contact list
            self.found_matching_tags.emit([contact_ids, contact_names])

    def tag_removed(self, tag_removed):
        # Gets the current tags after removal and emits a signal so the contacts list can be updated.
        tags = self.get_listed_tags()
        tags.remove(tag_removed)
        self.tagRemoveParent.emit(tags)

    def get_listed_tags(self):
        # Should return a list of all the tags listed
        tag_list = []
        for tag in self.scroll_widget.findChildren(TagItemWidget):
            tag_list.append(tag.tag_edit.text())

        return tag_list


class TagItemWidget(QFrame):
    tagRemoved = pyqtSignal(str)

    def __init__(self, tag_description):
        super().__init__()
        # Create h layout
        self.layout = QHBoxLayout(self)
        self.setObjectName(tag_description)
        # Create line edit widget
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.tag_edit = QLineEdit()  # Holds the tag_code
        self.tag_edit.setFont(self.font)
        self.tag_edit.setMinimumHeight(35)
        self.tag_edit.setAlignment(Qt.AlignCenter)
        self.tag_edit.setReadOnly(True)

        self.tag_edit.setText(tag_description)

        # Create remove button
        icon = QIcon(delete_button_icon_path)

        self.remove_tag_button = QPushButton('')
        self.remove_tag_button.setMinimumHeight(35)
        self.remove_tag_button.setFocusPolicy(Qt.NoFocus)

        self.remove_tag_button.setIcon(icon)

        self.layout.addWidget(self.tag_edit)
        self.layout.addWidget(self.remove_tag_button)

        self.setMaximumHeight(60)
        self.remove_tag_button.clicked.connect(self.remove_tag)

    def remove_tag(self):
        self.deleteLater()  # Deletes widget
        self.tagRemoved.emit(self.tag_edit.text())  # Emits signal for tag widget on which tag was removed


class QEmailContactsInfoWidget(QWidget):
    email_edited_parent = pyqtSignal(list)

    def __init__(self, current_contact_editing, database_handle):
        super().__init__()
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setFamily('Roboto')

        self.database_handle = database_handle
        self.current_contact_editing = current_contact_editing

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.visible_widgets = QWidget()
        self.visible_layouts = QHBoxLayout(self.visible_widgets)
        self.visible_layouts.setContentsMargins(0, 0, 0, 0)

        self.content_frame = QFrame()  # Frame that holds the email widgets
        self.content_frame.setFrameShape(QFrame.Box)
        self.content_frame.setVisible(True)

        self.frame_layout = QVBoxLayout(self.content_frame)

        self.toggle_email_widget_visibility_button = QPushButton("Hide transaction emails")
        self.toggle_email_widget_visibility_button.setFont(self.font)
        self.toggle_email_widget_visibility_button.setMinimumHeight(35)
        self.toggle_email_widget_visibility_button.setFocusPolicy(Qt.NoFocus)
        self.toggle_email_widget_visibility_button.setStyleSheet(button_selected_style)

        self.toggle_email_widget_visibility_button.clicked.connect(self.toggle_email_options_visibility)

        # Create email frame widgets
        from_widget = QWidget(self)
        from_layout = QHBoxLayout(from_widget)

        self.from_label = QLabel('From:')
        self.from_email = QComboBox()
        self.from_email.currentTextChanged.connect(lambda: self.set_from_email(self.current_contact_editing))
        self.from_email.setStyleSheet(combobox_style_sheet)

        self.from_emails = self.database_handle.get_from_email_addresses()
        if self.from_emails:  # If from emails exist
            for email in self.from_emails:
                self.from_email.addItem(email)
        else:
            pass
        self.from_email.setCurrentIndex(-1)

        icon = QIcon(edit_button_icon_path)
        self.from_edit_button = QPushButton('')
        self.from_edit_button.setFocusPolicy(Qt.NoFocus)

        self.from_edit_button.setIcon(icon)

        self.from_create_button = QPushButton('')
        self.from_create_button.setFocusPolicy(Qt.NoFocus)

        self.from_create_button.setIcon(QIcon(add_button_icon_path))
        from_layout.addWidget(self.from_label)
        from_layout.addWidget(self.from_email, stretch=1)
        from_layout.addWidget(self.from_create_button)
        from_layout.addWidget(self.from_edit_button)

        # Create to widget
        to_widget = QWidget(self)
        to_layout = QHBoxLayout(to_widget)
        to_widget.setLayout(to_layout)
        to_label = QLabel('To:')

        # Create the emails list widget which holds the emails list and the remove button
        self.to_emails_list_widget = QWidget()
        self.to_emails_list_layout = QVBoxLayout(self.to_emails_list_widget)

        # Create to emails list
        self.to_emails_list = QListWidget()
        self.to_emails_list.setFocusPolicy(Qt.NoFocus)
        self.to_emails_list.setItemDelegate(CenteredItemDelegate())
        self.to_emails_list.setSelectionMode(QListWidget.MultiSelection)

        # Create remove email button
        self.to_remove_button = QPushButton('Remove')
        self.to_remove_button.setFocusPolicy(Qt.NoFocus)

        new_to_email_widget = QWidget()
        new_to_email_layout = QHBoxLayout(new_to_email_widget)
        new_to_email_layout.setContentsMargins(0, 0, 0, 0)
        new_to_email_layout.setAlignment(Qt.AlignTop)

        self.to_add_email_edit = QLineEdit()
        self.to_add_email_edit.returnPressed.connect(
            lambda: self.add_to_email_to_contact(self.to_add_email_edit.text()))
        self.to_add_email_edit.setPlaceholderText('Enter a new email to send message to')
        icon = QIcon(add_button_icon_path)
        self.to_add_button = QPushButton('')
        self.to_add_button.setFocusPolicy(Qt.NoFocus)

        self.to_add_button.setIcon(icon)
        self.to_add_button.setContentsMargins(0, 0, 0, 0)

        new_to_email_layout.addWidget(self.to_add_email_edit)
        new_to_email_layout.addWidget(self.to_add_button)

        # Add widgets
        self.to_emails_list_layout.addWidget(self.to_emails_list, stretch=1)
        self.to_emails_list_layout.addWidget(new_to_email_widget)
        self.to_emails_list_layout.addWidget(self.to_remove_button)

        # Add the to elements into to widget layout
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_emails_list_widget)

        # Create CC widget
        cc_widget = QWidget(self)
        cc_layout = QHBoxLayout(cc_widget)
        cc_layout.setAlignment(Qt.AlignTop)
        cc_widget.setLayout(cc_layout)

        cc_label = QLabel('CC:')

        self.cc_email_list_widget = QWidget()
        self.email_list_edit_layout = QVBoxLayout(self.cc_email_list_widget)

        self.cc_emails_list = QListWidget()
        self.cc_emails_list.setFocusPolicy(Qt.NoFocus)
        self.cc_emails_list.setItemDelegate(CenteredItemDelegate())
        self.cc_remove_button = QPushButton('Remove')
        self.cc_remove_button.setFocusPolicy(Qt.NoFocus)

        self.add_cc_email_widget = QWidget()
        self.add_cc_email_layout = QHBoxLayout(self.add_cc_email_widget)
        self.add_cc_email_layout.setContentsMargins(0, 0, 0, 0)
        self.add_cc_email_layout.setAlignment(Qt.AlignTop)

        icon = QIcon(add_button_icon_path)
        self.cc_add_button = QPushButton('')
        self.cc_add_button.setFocusPolicy(Qt.NoFocus)

        self.cc_add_button.setIcon(icon)

        self.cc_add_email_edit = QLineEdit()
        self.cc_add_email_edit.returnPressed.connect(
            lambda: self.add_cc_email_to_contact(self.cc_add_email_edit.text()))
        self.cc_add_email_edit.setPlaceholderText('Enter a new email to send message via cc')

        self.add_cc_email_layout.addWidget(self.cc_add_email_edit)
        self.add_cc_email_layout.addWidget(self.cc_add_button)

        self.email_list_edit_layout.addWidget(self.cc_emails_list)
        self.email_list_edit_layout.addWidget(self.add_cc_email_widget)
        self.email_list_edit_layout.addWidget(self.cc_remove_button)

        # Add the cc elements into widget layout

        cc_layout.addWidget(cc_label)
        cc_layout.addWidget(self.cc_email_list_widget)

        # Add toggle button to visible widget
        self.visible_layouts.addWidget(self.toggle_email_widget_visibility_button, stretch=1)

        # Create the save contact options button
        options_buttons_widget = QWidget(self)
        options_buttons_layout = QHBoxLayout(options_buttons_widget)

        self.save_contact_options_button = QPushButton('Save edits')
        self.save_contact_options_button.setFocusPolicy(Qt.NoFocus)

        self.undo_options_button = QPushButton('Undo edits')
        self.undo_options_button.setFocusPolicy(Qt.NoFocus)

        options_buttons_layout.addWidget(self.save_contact_options_button)
        options_buttons_layout.addWidget(self.undo_options_button)

        self.layout.addWidget(self.visible_widgets)
        self.layout.addWidget(self.content_frame)

        # Add to and cc emails to the emails widget
        self.frame_layout.addWidget(from_widget)
        self.frame_layout.addWidget(to_widget)
        self.frame_layout.addWidget(cc_widget)
        self.frame_layout.addWidget(options_buttons_widget, alignment=Qt.AlignBottom)

        # Connect buttons
        self.to_remove_button.clicked.connect(lambda: self.remove_to_contact_email(self.to_emails_list))
        self.cc_remove_button.clicked.connect(lambda: self.remove_cc_contact_email(self.cc_emails_list))
        self.to_add_button.clicked.connect(lambda: self.add_to_email_to_contact(self.to_add_email_edit.text()))
        self.cc_add_button.clicked.connect(lambda: self.add_cc_email_to_contact(self.cc_add_email_edit.text()))
        self.undo_options_button.clicked.connect(self.undo_edits)
        self.save_contact_options_button.clicked.connect(self.save_edits)
        self.from_create_button.clicked.connect(self.from_create_button_clicked)
        self.from_edit_button.clicked.connect(self.from_edit_button_clicked)

    def set_from_email(self, contact_widget):
        if not contact_widget:
            return
        contact_widget.from_email = self.from_email.currentText()

    def toggle_email_options_visibility(self):
        if self.content_frame.isVisible():
            self.toggle_email_widget_visibility_button.setText('Show transaction emails')
            self.toggle_email_widget_visibility_button.setStyleSheet(button_style)
            self.content_frame.setVisible(False)
        else:
            self.toggle_email_widget_visibility_button.setText('Hide transaction emails')
            self.toggle_email_widget_visibility_button.setStyleSheet(button_selected_style)
            self.content_frame.setVisible(True)

    def save_edits(self):
        # Get the emails from the to and cc list
        # WIll take the to and cc emails that are currently in the list and save them to the database
        if self.current_contact_editing is None:  # If no contact is being edited
            return
        contact_id = self.current_contact_editing.contact_id
        to_emails = self.current_contact_editing.to_emails
        cc_emails = self.current_contact_editing.cc_emails
        from_email = self.from_email.currentText()

        from_email_id = self.database_handle.get_from_email_id(from_email)
        self.database_handle.set_contact_emails(contact_id, from_email_id, to_emails, cc_emails)

    def from_edit_button_clicked(self):
        edit_source_form = QLinkEmailAccountForm(self.database_handle, from_email_to_edit=self.from_email.currentText(),
                                                 parent=self)
        edit_source_form.email_edited.connect(self.edit_emails)
        edit_source_form.show()

    def from_create_button_clicked(self):
        # Create the QCreateEmailSourceForm()
        create_source_form = QLinkEmailAccountForm(self.database_handle, parent=self)
        create_source_form.email_created.connect(self.add_new_from_email)

        create_source_form.show()

    def undo_edits(self):
        # Will get the contact info that's in the database
        # Will uncheck checkbox which is default behavior
        if self.current_contact_editing is None:
            return

        to_emails, cc_emails = self.database_handle.get_contact_emails(
            self.current_contact_editing.contact_id)  # Gets emails saved in DB
        # Clears current emails listed
        self.to_emails_list.clear()
        self.cc_emails_list.clear()

        # Adds emails to list
        for to_email in to_emails:
            self.to_emails_list.addItem(to_email)

        for cc_email in cc_emails:
            self.cc_emails_list.addItem(cc_email)

    def add_to_email_to_contact(self, email):
        if not self.current_contact_editing:  # If no contact is being edited we cannot add an email
            return
        email = email.lower().strip()

        # Check if email already exists in to email and that its not empty
        # If good, then add it to the list
        # Also add it to the contact widget
        if email_valid(email) and not self.email_listed(email):
            self.current_contact_editing.to_emails.append(email)
            self.to_emails_list.addItem(email)
            self.to_add_email_edit.clear()

    def add_cc_email_to_contact(self, email):
        if not self.current_contact_editing:  # If no contact is being edited we cannot add an email
            return
        email = email.lower().strip()

        # Check if email already exists in to email and that its not empty
        # If good, then add it to the list
        # Also add it to the contact widget
        if email_valid(email) and not self.email_listed(email):
            self.current_contact_editing.cc_emails.append(email)
            self.cc_emails_list.addItem(email)
            self.cc_add_email_edit.clear()

    def add_new_from_email(self, from_email):
        self.from_email.addItem(from_email)
        if not self.current_contact_editing:  # If no contact is being edited we cannot add an email
            self.from_email.setCurrentText(from_email)
        else:
            last_index = self.from_email.count() - 1
            self.from_email.setCurrentIndex(last_index)

    def edit_emails(self, emails):
        # Edit the from email name in each send to contact
        # emails includes [old_email, new_email]
        index = self.from_email.findText(emails[0])
        self.from_email.setItemText(index, emails[1])
        self.from_email.setCurrentText(emails[1])
        self.email_edited_parent.emit(emails)

    def email_listed(self, email):
        for i in range(self.to_emails_list.count()):
            if email == self.to_emails_list.item(i).text():
                return True
        for i in range(self.cc_emails_list.count()):
            if email == self.cc_emails_list.item(i).text():
                return True
        return False

    def remove_to_contact_email(self, to_emails_list):
        # Check if the list contains only one email, if it does we let the user know they must have at least one email
        if self.to_emails_list.count() == 1:
            QErrorPrompt('Cannot remove email', 'You must have at least one to email address for a contact. Please '
                                                'add another email address to remove this email address.',
                         parent=self).show()
            return

        contact_email_to_remove = to_emails_list.item(to_emails_list.currentRow())
        if contact_email_to_remove:
            contact_email_to_remove = contact_email_to_remove.text()
            self.current_contact_editing.remove_email(contact_email_to_remove)
            to_emails_list.takeItem(to_emails_list.currentRow())

    def remove_cc_contact_email(self, cc_emails_list):
        contact_email_to_remove = cc_emails_list.item(cc_emails_list.currentRow())
        if contact_email_to_remove:
            contact_email_to_remove = contact_email_to_remove.text()
            self.current_contact_editing.remove_email(contact_email_to_remove)
            cc_emails_list.takeItem(cc_emails_list.currentRow())

    def edit_contact_info(self, contact_widget):
        if contact_widget is None:
            return

        if self.current_contact_editing:  # If a contact was already selected
            # Save the current contact before populating the new info
            updated_contact_info = self.get_contact_options()
            self.current_contact_editing.update_email_options(updated_contact_info)

        self.current_contact_editing = contact_widget

        if self.current_contact_editing:
            self.populate_contact_info(contact_widget)

    def remove_contact_info(self, contact_widget):
        if self.current_contact_editing is None or contact_widget is None:
            return
        if contact_widget.contact_id == self.current_contact_editing.contact_id or contact_widget is None:
            self.current_contact_editing = None
            self.clear_contact_info()

    def clear_contact_info(self):
        self.from_email.setCurrentIndex(-1)
        self.to_emails_list.clear()
        self.cc_emails_list.clear()

    def populate_contact_info(self, contact_widget):
        # Clear the current items
        self.to_emails_list.clear()
        self.cc_emails_list.clear()

        # set default from email
        index = self.from_email.findText(contact_widget.from_email)

        if index == -1:
            self.from_email.addItem(contact_widget.from_email)

        self.from_email.setCurrentText(contact_widget.from_email)

        # Populate the QListWidgets
        for email in contact_widget.to_emails:
            self.to_emails_list.addItem(email)

        for email in contact_widget.cc_emails:
            self.cc_emails_list.addItem(email)

    def get_contact_options(self):
        # Should return a dictionary with keys 'from_email', 'to_emails', 'cc_emails' and further
        # options that may be added
        contact_options = dict()
        from_email = self.from_email.currentText()
        contact_options['from_email'] = from_email

        to_emails = []
        for i in range(self.to_emails_list.count()):
            item = self.to_emails_list.item(i)
            to_emails.append(item.text())
        contact_options['to_emails'] = to_emails

        cc_emails = []
        for i in range(self.cc_emails_list.count()):
            item = self.cc_emails_list.item(i)
            cc_emails.append(item.text())
        contact_options['cc_emails'] = cc_emails

        return contact_options


class QEmailTimeInfoWidget(QWidget):
    # Calendar widget that can be

    def __init__(self, current_contact_editing, global_widget=False):
        super().__init__()

        self.current_contact_editing = current_contact_editing
        self.global_widget = global_widget

        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # These widgets are always visible
        self.visible_widgets = QWidget()
        self.visible_layouts = QHBoxLayout(self.visible_widgets)
        self.visible_layouts.setContentsMargins(0, 0, 0, 0)

        self.content_frame = QFrame()
        self.content_frame.setFrameShape(QFrame.Box)
        self.content_frame.setEnabled(False)

        self.frame_layout = QVBoxLayout(self.content_frame)


        # Button to toggle visibility of the calendar
        if global_widget:
            self.toggle_button = QPushButton("Hide global date", self)
        else:
            self.toggle_button = QPushButton("Hide transaction date", self)

        self.toggle_button.setFocusPolicy(Qt.NoFocus)
        self.toggle_button.setFont(self.font)
        self.toggle_button.setMinimumHeight(35)

        self.toggle_button.setStyleSheet(button_selected_style)
        self.toggle_button.clicked.connect(self.toggle_widget_visibility)

        self.enable_checkbox = QCheckBox()  # Used to enable a date modification on the transaction
        self.enable_checkbox.setChecked(False)
        self.enable_checkbox.setToolTip('Enable the specified date to send email')
        self.enable_checkbox.clicked.connect(self.enable_checkbox_clicked)

        # Label widget
        self.schedule_label = QLabel('Schedule email for later')

        # Time widget
        self.time_edit = QTimeEdit()  # Get time input
        self.time_edit.setFont(self.font)
        self.time_edit.setAlignment(Qt.AlignCenter)

        # Calendar widget
        self.calendar_widget = QCalendarWidget(self)

        calendar_next_month_button = self.calendar_widget.findChild(QToolButton, "qt_calendar_nextmonth")
        next_icon = QIcon(':resource/media/next_arrow.png')
        calendar_next_month_button.setIcon(next_icon)

        calendar_previous_month_button = self.calendar_widget.findChild(QToolButton, "qt_calendar_prevmonth")
        previous_icon = QIcon(':resource/media/previous_arrow.png')
        calendar_previous_month_button.setIcon(previous_icon)

        self.calendar_widget.setFocusPolicy(Qt.NoFocus)
        # Apply a stylesheet to customize the next and previous arrows

        # Turn off widgets visibility by default
        self.content_frame.setVisible(True)

        # Add widgets to the layout
        self.visible_layouts.addWidget(self.enable_checkbox)
        self.visible_layouts.addWidget(self.toggle_button, stretch=1)

        self.layout.addWidget(self.visible_widgets)
        self.layout.addWidget(self.content_frame)

        # Add widgets to the frame
        self.frame_layout.addWidget(self.schedule_label, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.time_edit)
        self.frame_layout.addWidget(self.calendar_widget)

    def enable_checkbox_clicked(self):
        if self.enable_checkbox.isChecked():
            if self.current_contact_editing:  # If we're editing for a contact
                date = self.get_selected_date()
                self.current_contact_editing.update_contact_date_options(date)
                self.content_frame.setEnabled(True)
            elif self.global_widget:  # If we're editing for global widget
                self.content_frame.setEnabled(True)
            else:  # If neither then we need to add contacts first
                QErrorPrompt("Add contacts.",
                             "Please select contacts to configure the date options for the contacts.",
                             parent=self).show()
                self.enable_checkbox.setChecked(False)
        else:
            self.content_frame.setEnabled(False)
            if self.current_contact_editing:  # If we're editing a contact date
                self.current_contact_editing.send_date = None
            elif not self.global_widget:  # If we're not editing a contact date we're editing a global widget so if it is none we should return
                return

                self.content_frame.setEnabled(False)

    def toggle_widget_visibility(self):
        # Toggle the visibility of the calendar widget
        if self.time_edit.isVisible():
            if self.global_widget:
                self.toggle_button.setText("Show global date")
            else:
                self.toggle_button.setText("Show transaction date")

            self.toggle_button.setStyleSheet(button_style)
            # Toggle each widget's visibility
            self.content_frame.setVisible(False)
            self.time_edit.setVisible(False)
            self.schedule_label.setVisible(False)
            self.calendar_widget.setVisible(False)

        else:
            if self.global_widget:
                self.toggle_button.setText("Hide global date")
            else:
                self.toggle_button.setText("Hide transaction date")

            self.toggle_button.setStyleSheet(button_selected_style)
            self.content_frame.setVisible(True)
            self.time_edit.setVisible(True)
            self.schedule_label.setVisible(True)
            self.calendar_widget.setVisible(True)

    def edit_contact_info(self, contact_widget):
        if self.current_contact_editing:  # If a contact was already selected
            if self.enable_checkbox.isChecked():  # If date edit was enabled update the contact
                # Save the current contact before populating the new info
                updated_date = self.get_selected_date()
                self.current_contact_editing.update_contact_date_options(updated_date)

        self.current_contact_editing = contact_widget
        self.populate_contact_info(contact_widget)

    def populate_contact_info(self, contact_widget):
        if contact_widget.send_date is None:  # If contact does not have a send date that means they want it to send
            # instantly
            self.enable_checkbox.setChecked(False)
            self.content_frame.setEnabled(False)
        else:
            self.enable_checkbox.setChecked(True)
            self.content_frame.setEnabled(True)
            self.set_contact_date(contact_widget)

    def get_selected_date(self):
        if self.enable_checkbox.isChecked():
            date_string = self.calendar_widget.selectedDate().toString(
                'yyyy-MM-dd') + ' ' + self.time_edit.time().toString()
        else:
            date_string = None
        return date_string

    def set_contact_date(self, contact_widget):
        self.time_edit.setTime(contact_widget.send_date.time())
        self.calendar_widget.setSelectedDate(contact_widget.send_date.date())

    def set_date(self, send_date):
        self.time_edit.setTime(send_date.time())
        self.calendar_widget.setSelectedDate(send_date.date())

    def save_contact_options(self):
        if self.current_contact_editing is None:
            return
        date = self.get_selected_date()
        if date:
            self.current_contact_editing.update_contact_date_options(date)

    def clear_date_info(self):
        self.enable_checkbox.setChecked(False)
        self.content_frame.setEnabled(False)


class QSettingsWidget(QFrame):
    # Will hold the settings widget
    def __init__(self, database_handle):
        super().__init__()
        self.database_handle = database_handle
        # Create settings layout
        self.layout = QVBoxLayout(self)

        # Create scroll widget and layout
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        # Create scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setStyleSheet(scroll_bar_style)
        scroll_area.setWidgetResizable(True)

        # Create schedule widget

        self.global_schedule_widget = QEmailTimeInfoWidget(None, global_widget=True)
        self.global_schedule_widget.setToolTip('Sets the date for the email to send globally')

        # Set the scroll widget to scroll area
        scroll_area.setWidget(self.scroll_widget)

        # Add widgets to layouts
        self.scroll_layout.addWidget(self.global_schedule_widget)

        self.layout.addWidget(scroll_area)

        # Set frame shape
        self.setFrameShape(QFrame.Box)


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableFrame, self).__init__(parent)

    def mousePressEvent(self, event):
        # This function is called when the frame is clicked
        self.clicked.emit()  # Emit the clicked signal


class QTransactionsWidget(QWidget):

    transaction_edited = pyqtSignal(int)
    transaction_removed = pyqtSignal(int)

    def __init__(self, type, database_handle, parent=None):
        super().__init__(parent)
        self.database_handle = database_handle
        self.offset = 0
        self.type = type
        self.total_count = 0
        # Create scroll area
        # Queue database for info
        # From info create transaction widgets and add them to the Qscroll area
        # When transactions are sent/uploaded it should receive that signal and insert at the top the transaction widget
        self.transactions = []
        self.transactions_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(scroll_bar_style)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.scroll_area.setWidgetResizable(True)
        self.transactions_list_widget = QWidget()
        self.transactions_list_layout = QVBoxLayout(self.transactions_list_widget)
        self.transactions_list_layout.setAlignment(Qt.AlignTop)

        self.count_widget = QWidget()
        self.count_layout = QHBoxLayout(self.count_widget)

        spacer = QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding)

        self.count = QLineEdit()

        if self.type == 'archive':
            self.total_count = self.database_handle.execute_query("""
                SELECT COUNT(*)
                FROM archived_transactions;
            """, 'fetchone', ())[0]
            self.count_label = QLabel('Archived transactions:')
            self.count.setText(str(self.total_count))

        else:
            self.total_count = self.database_handle.execute_query("""
                SELECT COUNT(*)
                FROM active_transactions;
            """, 'fetchone', ())[0]
            self.count_label = QLabel('Scheduled transactions:')
            self.count.setText(str(self.total_count))


        self.count_layout.addItem(spacer)
        self.count_layout.addWidget(self.count_label)
        self.count_layout.addWidget(self.count)

        self.load_transactions()
        self.scroll_area.setWidget(self.transactions_list_widget)
        self.transactions_layout.addWidget(self.scroll_area)
        self.transactions_layout.addWidget(self.count_widget)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

    def load_transactions(self, new=False):
        # Query active_transactions in active transactions
        # Use offset and limit to dynamically find and append transactions

        transactions = self.database_handle.get_transactions(self.type, self.offset)

        # For each transaction
        for transaction in transactions:
            transaction_widget = QTransactionWidget(self.type, transaction, parent=self)
            transaction_widget.edit_active_transaction_signal.connect(self.edit_transaction)
            self.transactions.append(transaction_widget)
            transaction_widget.remove_transaction.connect(self.remove_transaction_from_db)

            self.transactions_list_layout.addWidget(transaction_widget)
        if new:
            self.total_count += len(transactions)
            self.count.setText((str(self.total_count)))
        self.offset += len(transactions)

    def on_scroll(self, value):
        # Check if the scroll bar is at the bottom
        if value == self.scroll_area.verticalScrollBar().maximum():
            self.load_transactions()

    def remove_transaction_from_db(self, transaction_id):
        self.database_handle.remove_all_transactions(transaction_id)
        self.offset -= 1
        self.transaction_removed.emit(transaction_id)
        self.total_count -= 1
        self.count.setText(str(self.total_count))

    def remove_transaction_widget(self, transaction_id):
        # If transaction_id is not a list, make it a one-item list
        if not isinstance(transaction_id, list):
            transaction_id = [transaction_id]

        # Iterate over a copy of the list since you're modifying the list inside the loop
        for transaction in self.transactions[:]:
            if transaction.transaction_id in transaction_id:
                self.transaction_removed.emit(transaction.transaction_id)
                transaction.deleteLater()
                self.offset -= 1
                self.total_count -= 1
                self.count.setText(str(self.total_count))
                # Optional: Remove the transaction from the self.transactions list if needed
                # self.transactions.remove(transaction)

    def edit_transaction(self, transaction_id):
        self.transaction_edited.emit(transaction_id)

    def transactions_failed(self, transaction_ids):

        # If transaction_id is not a list, make it a one-item list
        if not isinstance(transaction_ids, list):
            transaction_ids = [transaction_ids]

        # Needs to find the transaction and add the failed icon
        # Maybe a retry button
        for transaction in self.transactions[:]:
            if transaction.transaction_id in transaction_ids:
                vLine5 = QFrame()
                vLine5.setFrameShape(QFrame.VLine)

                transaction.transaction_failed = True

                error_icon = QIcon(error_icon_path)
                error_button = QPushButton()
                error_button.setMaximumWidth(40)
                error_button.setToolTip('This transaction failed and did not send.')
                error_button.setIcon(error_icon)

                transaction.layout.addWidget(vLine5)
                transaction.layout.addWidget(error_button)


class QTransactionWidget(QFrame):

    remove_transaction = pyqtSignal(int)
    edit_active_transaction_signal = pyqtSignal(int)

    def __init__(self, type, info, parent=None):
        super().__init__(parent)
        self.transaction_edit = None
        self.failed_transaction = False
        self.transaction_item_layout = QVBoxLayout(self)

        self.transaction_record_frame = ClickableFrame()
        self.transaction_record_frame.setObjectName('transaction_frame')
        self.layout = QHBoxLayout(self.transaction_record_frame)

        self.transaction_record_frame.setFrameShape(QFrame.StyledPanel)
        self.transaction_record_frame.setFrameShadow(QFrame.Raised)
        self.transaction_record_frame.setStyleSheet("""
            QFrame{
                color: black;
            }

            #transaction_frame { 
                background-color: white; 
                color: white;
                border: 2px solid black
            }

            #transaction_frame:hover {
                border-color: #A367B1;  /* Background color on hover */
            }
            }
        """)

        self.transactions_layout = QHBoxLayout()
        self.transaction_record_frame.setMinimumHeight(75)

        # Extract field values
        self.transaction_id = info[0]
        self.official_name = info[1]
        self.send_date = info[2]
        self.to_count = info[3]
        self.cc_count = info[4]
        if len(info) > 5:
            self.failed_transaction = info[5]
            if self.failed_transaction == 1:
                self.failed_transaction = True
            elif self.failed_transaction == 0:
                self.failed_transaction = False

        # Create sub-widgets

        # Create transaction line
        self.transaction_id_line = QLineEdit()
        line_style = """
            QLineEdit{
                background-color: black;
                color: white;
            }
        """
        self.transaction_id_line.setStyleSheet(line_style)
        self.transaction_id_line.setMaximumWidth(100)
        self.transaction_id_line.setText(str(self.transaction_id))
        self.transaction_id_line.setAlignment(Qt.AlignCenter)
        self.transaction_id_line.setReadOnly(True)
        self.transaction_id_line.setToolTip("Transaction ID")

        # Create line
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)

        # Create official name
        self.official_name_label = QLabel(f'Official name: {self.official_name}')

        # Create date

        self.date_label = QLabel(f'Date: {self.send_date}')

        # Create line
        vline2 = QFrame()
        vline2.setFrameShape(QFrame.VLine)

        # Create emails counts widget
        self.email_count_widget = QWidget()
        email_count_layout = QVBoxLayout(self.email_count_widget)
        self.to_count_label = QLabel(f'To emails: {self.to_count}')
        self.cc_count_label = QLabel(f'Cc emails: {self.cc_count}')

        email_count_layout.addWidget(self.to_count_label)
        email_count_layout.addWidget(self.cc_count_label)

        # Create line
        vline3 = QFrame()
        vline3.setFrameShape(QFrame.VLine)

        self.layout.addWidget(self.transaction_id_line, stretch=-1)
        self.layout.addWidget(vline)
        self.layout.addWidget(self.official_name_label)
        self.layout.addWidget(vline2)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(vline3)
        self.layout.addWidget(self.email_count_widget)

        self.transaction_item_layout.addWidget(self.transaction_record_frame)

        self.remove_button = QPushButton()
        self.remove_button.setMaximumSize(35, 35)
        icon = QIcon(delete_button_icon_path)
        self.remove_button.setIcon(icon)

        # Create line
        vline4 = QFrame()
        vline4.setFrameShape(QFrame.VLine)

        self.layout.addWidget(vline4)
        self.layout.addWidget(self.remove_button)

        if type == 'scheduled':
            self.remove_button.clicked.connect(self.remove_transaction_from_db)
            self.transaction_record_frame.clicked.connect(lambda : self.edit_active_transaction_clicked('scheduled'))

        else:
            if self.failed_transaction:
                vline5 = QFrame()
                vline5.setFrameShape(QFrame.VLine)

                error_icon = QIcon(error_icon_path)
                error_button = QPushButton()
                error_button.setMaximumWidth(40)
                error_button.setToolTip('This transaction failed and did not send.')
                error_button.setIcon(error_icon)

                self.layout.addWidget(vline5)
                self.layout.addWidget(error_button)

            self.remove_button.clicked.connect(self.remove_transaction_from_db)
            self.transaction_record_frame.clicked.connect(lambda : self.edit_active_transaction_clicked('archived'))

    def remove_transaction_from_db(self):
        confirm_remove = QAcceptDialog(f'Remove transaction?', 'Are you sure you want to remove this transaction?')
        confirm_remove.show()

        if confirm_remove.exec_() == QDialog.Accepted:
            self.remove_transaction.emit(self.transaction_id)
            self.deleteLater()

    def edit_active_transaction_clicked(self, source):
        if self.transaction_edit:

            if self.transaction_edit.isVisible():
                self.transaction_edit.setVisible(False)
                self.transaction_record_frame.setStyleSheet("""
                    QFrame{
                        color: black;
                    }
                    
                    #transaction_frame { 
                        background-color: white; 
                        color: white;
                        border: 2px solid black
                    }
                    
                    #transaction_frame:hover {
                        border-color: #A367B1;  /* Background color on hover */
                    }
                """)
            else:
                self.transaction_edit.setVisible(True)
                self.transaction_record_frame.setStyleSheet("""
                    QFrame{
                        color: white;
                    }
                    #transaction_frame { 
                        background-color: #392467; 
                        color: white;
                        border: 5px solid #392467
                    }
                    #transaction_frame:hover {
                        border-color: #A367B1;  /* Background color on hover */
                    }
                """)

        else:
            # Needs to get transaction info to populate widgets in send tab
            # Needs to set the send tab as the active tab
            self.edit_active_transaction_signal.emit(self.transaction_id)
            self.transaction_edit = QTransactionEdit(source, self.transaction_id, database_handle, parent=self)
            self.transaction_edit.transaction_updated.connect(self.redraw_transaction_widget)
            self.transaction_item_layout.addWidget(self.transaction_edit)
            self.transaction_record_frame.setStyleSheet("""
                QFrame{
                    color: white;
                }
                #transaction_frame { 
                    background-color: #392467; 
                    color: white;
                    border: 5px solid #392467
                }
                #transaction_frame:hover {
                    border-color: #A367B1;  /* Background color on hover */
                }
            """)

    def redraw_transaction_widget(self, info):

        # should redraw the rectangle transaction widget
        # info will contact the new date, to_emails, cc_emails

        self.date_label.setText(f'Date: {info[6]}')
        self.to_count_label.setText(f'To emails: {str(len(info[4]))}')
        self.cc_count_label.setText(f'Cc emails: {str(len(info[5]))}')

        self.edit_active_transaction_signal.emit(info[0])

        if self.transaction_edit:
            self.transaction_edit.email_text_edit.subject_line.setText(info[2])
            self.transaction_edit.email_text_edit.body.setHtml(info[3])
            self.transaction_edit.email_editor.from_email.setCurrentText(info[1])

            self.transaction_edit.email_editor.to_emails_list.clear()
            self.transaction_edit.email_editor.cc_emails_list.clear()

            for to_email in info[4]:
                self.transaction_edit.email_editor.to_emails_list.addItem(to_email)

            for cc_email in info[5]:
                self.transaction_edit.email_editor.cc_emails_list.addItem(cc_email)

            date_object = datetime.datetime.strptime(info[6], '%Y-%m-%d %H:%M:%S')
            self.transaction_edit.date_editor.set_date(date_object)

            self.transaction_edit.attachments.clear_attachments()
            if info[7]:
                for attachment in info[7]:
                    self.transaction_edit.attachments.add_attachment_to_list(attachment)


class QTransactionEdit(QFrame):

    transaction_updated = pyqtSignal(list)

    def __init__(self, source, transaction_id, database_handle, parent=None):
        super().__init__(parent)
        self.database_handle = database_handle
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)
        self.transaction_id = transaction_id
        self.setMinimumHeight(500)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.content_widget)
        self.info = self.database_handle.get_transaction_edit_info(source, transaction_id)

        self.info.insert(0, transaction_id)
        # Need to get the contact_id using transaction_id
        # Need to get official name from contact_id


        self.layout = QVBoxLayout(self)

        # Need to create a scroll area that adds email options widget, send_date widget
        # contact_attachments widget
        self.contact_editing = QContactWidget(self.info[0], self.info[5], self.database_handle, self, True)
        self.contact_editing.send_date = datetime.datetime.strptime(self.info[5], '%Y-%m-%d %H:%M:%S')
        self.contact_editing.setVisible(False)

        self.email_text_edit = QBasicEmailEditor(self)
        self.email_editor = QEmailContactsInfoWidget(self.contact_editing, self.database_handle)
        self.date_editor = QEmailTimeInfoWidget(self.contact_editing, False)
        self.attachments = QAttachmentsWidget(self.database_handle, self, False)

        self.content_layout.addWidget(self.email_text_edit)
        self.content_layout.addWidget(self.email_editor)
        self.content_layout.addWidget(self.date_editor)
        self.content_layout.addWidget(self.attachments)

        if source != 'archived':
            space = QSpacerItem(0, 50, vPolicy=QSizePolicy.Expanding)
            self.content_layout.addItem(space)
            self.save_transaction_button = QPushButton('Update transaction')
            self.save_transaction_button.clicked.connect(self.update_transaction)
            self.save_transaction_button.setMaximumHeight(50)
            self.save_transaction_button.setFont(self.font)
            self.content_layout.addWidget(self.save_transaction_button, alignment=Qt.AlignBottom)

        self.layout.addWidget(self.scroll_area)

        self.populate_email_message()
        self.populate_email_widget()
        self.populate_send_widget()
        self.populate_attachments_widget()

        if source == 'archived':  # If this is a transaction in the archived widget, the widget should be disabled
            self.email_text_edit.subject_line.setEnabled(False)
            self.email_text_edit.body.setEnabled(False)

            self.email_editor.from_email.setEnabled(False)
            self.email_editor.to_emails_list_widget.setEnabled(False)
            self.email_editor.cc_email_list_widget.setEnabled(False)
            self.email_editor.save_contact_options_button.setEnabled(False)
            self.email_editor.undo_options_button.setEnabled(False)

            self.date_editor.time_edit.setEnabled(False)
            self.date_editor.calendar_widget.setEnabled(False)
            self.date_editor.enable_checkbox.setEnabled(False)

            self.attachments.attachment_info_widget.setEnabled(False)
            self.attachments.add_attachment_button.setEnabled(False)

    def update_transaction(self):
        dialog_handle = QAcceptDialog('Update transaction?', 'Are you sure you want to update the selected transaction?')

        dialog_handle.show()

        if dialog_handle.exec_() != QDialog.Accepted:
            return

        # Save email subject and body
        # Save email info
        # Save send date
        # Save attachments

        subject = self.email_text_edit.subject_line.text()
        body = self.email_text_edit.body.toHtml()
        from_email = self.email_editor.from_email.currentText()
        send_date = self.date_editor.get_selected_date()
        attachments = self.attachments.get_email_attachments()
        to_emails = []
        cc_emails = []

        for index in range(self.email_editor.to_emails_list.count()):
            to_emails.append(self.email_editor.to_emails_list.item(index).text())

        for index in range(self.email_editor.cc_emails_list.count()):
            cc_emails.append(self.email_editor.cc_emails_list.item(index).text())

        self.info = self.info[0:2]
        self.info.append(from_email)
        self.info.append(subject)
        self.info.append(body)
        self.info.append(to_emails)
        self.info.append(cc_emails)
        self.info.append(send_date)
        self.info.append(attachments)

        self.database_handle.update_active_transaction_info(self.info)

        self.transaction_updated.emit([self.transaction_id, from_email, subject, body, to_emails, cc_emails, send_date, attachments])

    def populate_email_message(self):
        self.email_text_edit.subject_line.setText(self.info[3])
        self.email_text_edit.body.setHtml(self.info[4])

    def populate_email_widget(self):
        from_email = self.info[2]
        self.email_editor.from_email.setCurrentText(from_email)

        to_emails = self.info[7]
        for email in to_emails:
            self.email_editor.to_emails_list.addItem(email)

        cc_emails = self.info[8]
        for email in cc_emails:
            self.email_editor.cc_emails_list.addItem(email)

    def populate_send_widget(self):
        self.date_editor.enable_checkbox.setChecked(True)
        self.date_editor.populate_contact_info(self.contact_editing)

    def populate_attachments_widget(self):

        for attachment in self.info[8]:
            self.attachments.add_attachment_to_list(attachment)


class QBasicEmailEditor(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.toggle_header_button = QPushButton('Hide email message')
        self.toggle_header_button.setStyleSheet(button_selected_style)
        self.toggle_header_button.setMinimumHeight(35)
        self.toggle_header_button.setFont(self.font)

        self.email_info_frame = QFrame()
        self.email_info_frame.setFrameShape(QFrame.Box)
        self.email_info_layout = QVBoxLayout(self.email_info_frame)

        self.subject_line = QLineEdit()
        self.subject_line.setFont(self.font)
        self.subject_line.setMinimumHeight(30)
        self.subject_line.setPlaceholderText('Enter subject line')

        self.body = QTextEdit()
        self.body.setMinimumHeight(100)

        self.email_info_layout.addWidget(self.subject_line)
        self.email_info_layout.addWidget(self.body)

        self.layout.addWidget(self.toggle_header_button)
        self.layout.addWidget(self.email_info_frame)

        self.toggle_header_button.clicked.connect(self.toggle_visibility)

    def toggle_visibility(self):
        if self.email_info_frame.isVisible():
            self.email_info_frame.setVisible(False)
            self.toggle_header_button.setText('Show email message')
            self.toggle_header_button.setStyleSheet(button_style)

        else:
            self.email_info_frame.setVisible(True)
            self.toggle_header_button.setText('Hide email message')
            self.toggle_header_button.setStyleSheet(button_selected_style)


class QToolBar(QToolBar):
    edit_contact = pyqtSignal()
    edit_from_email = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(toolbar_style)
        # Create an action with an icon and a text label
        # Here, you need to replace 'icon.png' with the path to your icon file
        contacts_action = QAction(QIcon(contact_icon_path), 'Contact Menu', self)
        contacts_action.setStatusTip('Modify, create, or edit contacts')
        contacts_action.triggered.connect(self.contact_clicked)  # Connect the action to a function

        from_email_action = QAction(QIcon(from_email_icon_path), 'Create or edit a source email', self)
        from_email_action.setStatusTip('Create or edit a source email')
        from_email_action.triggered.connect(self.from_email_clicked)

        self.addAction(contacts_action)
        self.addAction(from_email_action)

    def contact_clicked(self):
        self.edit_contact.emit()

    def from_email_clicked(self):
        self.edit_from_email.emit()


class MainWindow(QMainWindow):

    def __init__(self, database_handle, transaction_manager):
        super().__init__()
        self.send_progress_bar = None
        self.toolbar = None
        self.dashboard_layout = None
        self.dashboard_tab = None
        self.active_transactions_widget = None
        self.archived_transactions_widget = None
        self.email_engine_handle = transaction_manager
        self.email_engine_handle.error_signal.connect(self.transaction_engine_error_occured)
        self.database_handle = database_handle
        self.setObjectName('main_window')
        self.setWindowTitle('Demo Kick')
        self.setWindowIcon(QIcon(logo_icon_path))
        self.width = 1280
        self.height = 740
        self.font = QFont()
        self.font.setFamily('Roboto')
        self.font.setPointSize(16)

        self.central_widget = None
        self.central_layout = None
        self.tab_selection = None
        self.setGeometry(0, 0, self.width, self.height)

        self.sending_to_contacts_widget = None
        self.email_editor_widget = None
        self.contact_options_widget_container = None
        self.media_info_widget = None
        self.tags_widget = None
        self.settings_widget = None
        self.send_button = None
        self.clear_button = None

        self.load_gui_elements()
        # Create handles to each widget so we can call

    def load_gui_elements(self):

        # Add central widget and layout
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        # Add gui elements into layout

        # Create toolbar
        self.toolbar = QToolBar()
        self.central_layout.addWidget(self.toolbar)

        # Create tabs
        self.create_tabs()
        self.init_dashboard()
        self.init_send_tab()

        # Create footer
        footer = QLabel('Corso - Software')
        self.central_layout.addWidget(footer, alignment=Qt.AlignHCenter)

        # Set central widget layout to central layout
        self.central_widget.setLayout(self.central_layout)
        self.central_widget.setObjectName('central_widget_widget')
        self.central_layout.setObjectName('central_layout')

        self.setCentralWidget(self.central_widget)
        self.toolbar.edit_contact.connect(partial(self.sending_to_contacts_widget.add_contact_to_list))
        self.toolbar.edit_from_email.connect(self.create_from)

    def create_tabs(self):
        
        # Create tab object
        self.tab_selection = QTabWidget()
        self.tab_selection.setStyleSheet(tabs_style)
        self.tab_selection.tabBar().setFont(self.font)
        self.tab_selection.setObjectName("tab_selection")

        # Create widget for send tab
        send_tab_widget = QWidget()

        send_tab_widget.setObjectName('send_tab_widget')

        # Create layout for send tab widget
        send_tab_layout = QVBoxLayout(send_tab_widget)
        send_tab_layout.setObjectName('send_tab_layout')


        # Repeat for profiles tab below
        dashboard_tab_widget = QWidget()
        dashboard_tab_widget.setObjectName('profiles_tab_widget')

        profiles_tab_layout = QGridLayout(dashboard_tab_widget)
        profiles_tab_layout.setObjectName('profiles_tab_layout')

        # Create the tab via the widget and name it
        self.tab_selection.addTab(send_tab_widget, 'Send')
        self.tab_selection.addTab(dashboard_tab_widget, 'Transactions')

        # Add the tab widget to the central widget
        self.central_layout.addWidget(self.tab_selection, 0)

    def init_dashboard(self):
        self.dashboard_tab = self.tab_selection.widget(1)
        self.dashboard_layout = self.dashboard_tab.layout()

        scheduled_tab = QWidget()
        scheduled_tab_layout = QVBoxLayout(scheduled_tab)

        archived_tab = QWidget()
        archived_tab_layout = QVBoxLayout(archived_tab)

        transaction_type_tag = QTabWidget()
        transaction_type_tag.addTab(scheduled_tab, 'Scheduled')
        transaction_type_tag.addTab(archived_tab, 'Archived')

        self.init_archived_tab(archived_tab)
        self.init_scheduled_tab(scheduled_tab)

        self.dashboard_layout.addWidget(transaction_type_tag)

    def init_archived_tab(self, archived_tab):
        self.archived_transactions_widget = QTransactionsWidget('archive', self.database_handle, parent=self)
        archived_tab_layout = archived_tab.layout()
        archived_tab_layout.addWidget(self.archived_transactions_widget)

    def init_scheduled_tab(self, scheduled_tab):
        self.active_transactions_widget = QTransactionsWidget('scheduled', self.database_handle, parent=self)
        self.active_transactions_widget.transaction_edited.connect(self.active_transaction_edited)
        self.active_transactions_widget.transaction_removed.connect(self.archived_transactions_widget.remove_transaction_widget)
        scheduled_tab_layout = scheduled_tab.layout()

        scheduled_tab_layout.addWidget(self.active_transactions_widget)

    def init_send_tab(self):
        # Create top_widget in first row of vertical layout of send tab
        # Create QHBoxLayout top_layout for top_widget
        # Set the layout of top_widget to top_layout

        # Get send tab widget reference
        send_tab_widget = self.tab_selection.widget(0)
        # Get layout widget reference
        send_tab_layout = send_tab_widget.layout()

        # Create the top widget & H layout
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_widget.setLayout(top_layout)

        # Create the Sending to Labels Preview widget
        self.sending_to_contacts_widget = QSendToContacts(self.database_handle)
        self.sending_to_contacts_widget.setObjectName('send_to_contact_widget')

        top_layout.addWidget(self.sending_to_contacts_widget)

        # Create the email text editor widget
        self.email_editor_widget = QEmailTextEditor(self.database_handle)
        top_layout.addWidget(self.email_editor_widget)

        # Create the bottom widget and H Layout
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_widget.setLayout(bottom_layout)
        # Creates the container widget and the to and cc widgets
        self.contact_options_widget_container = QContactOptionsWidget(self.database_handle)
        self.contact_options_widget_container.email_edited_parent.connect(
            self.sending_to_contacts_widget.update_from_email_name)
        bottom_layout.addWidget(self.contact_options_widget_container)

        # Connect the contact selected signal to the contact options widget to display configs
        self.sending_to_contacts_widget.contact_selected_parent.connect(
            partial(self.contact_options_widget_container.edit_contact_options))
        # Connect the contact selected signal to the email editor widget
        self.sending_to_contacts_widget.contact_selected_parent.connect(self.email_editor_widget.contact_selected)

        self.sending_to_contacts_widget.contact_selected_removed.connect(
            self.contact_options_widget_container.emails_widget.remove_contact_info)
        self.sending_to_contacts_widget.contact_selected_removed.connect(
            self.contact_options_widget_container.contact_removed)
        self.sending_to_contacts_widget.removed_all_contacts.connect(
            self.contact_options_widget_container.emails_widget.clear_contact_info)
        self.sending_to_contacts_widget.removed_all_contacts.connect(
            self.contact_options_widget_container.date_widget.clear_date_info)
        self.sending_to_contacts_widget.from_email_updated.connect(self.contact_options_widget_container.from_email_changed)
        self.sending_to_contacts_widget.removed_all_contacts.connect(self.email_editor_widget.clear_contacts)

        self.sending_to_contacts_widget.contact_selected_removed.connect(
            self.email_editor_widget.remove_contact_email_message)

        self.sending_to_contacts_widget.send_to_widget = self.contact_options_widget_container

        # Create the source widget and the media widget

        # Create tags widget
        self.tags_widget = QTagsWidget(self.database_handle, self)
        self.tags_widget.tagRemoveParent.connect(self.sending_to_contacts_widget.update_contact_list_via_tags)
        self.tags_widget.setObjectName('tags_widget')
        self.tags_widget.found_matching_tags.connect(self.sending_to_contacts_widget.add_matching_contacts_to_list)
        # Connect add_tag button
        # Connect the add tag button clicked callback

        # Create song widget container

        bottom_layout.addWidget(self.tags_widget)

        # Create settings and send clear button container widget
        self.settings_widget = QSettingsWidget(self.database_handle)

        self.send_button = QPushButton('Send')
        self.send_button.setFocusPolicy(Qt.NoFocus)

        self.send_button.clicked.connect(
            partial(self.send_button_clicked, self.sending_to_contacts_widget, self.contact_options_widget_container,
                    self.email_editor_widget, self.settings_widget, testing=True))

        self.send_button.setMinimumHeight(40)
        self.send_button.setFont(self.font)
        self.clear_button = QPushButton('Clear')
        self.clear_button.setFocusPolicy(Qt.NoFocus)

        self.clear_button.setToolTip('Clear all transaction information')
        self.clear_button.clicked.connect(
            partial(self.clear_all, self.sending_to_contacts_widget, self.email_editor_widget,
                    self.tags_widget, self.contact_options_widget_container, self.settings_widget))
        self.clear_button.setMinimumHeight(40)
        self.clear_button.setFont(self.font)
        # Create buttons horizontal widget and layout
        horizontal_button_widget = QWidget()
        horizontal_button_container = QHBoxLayout(horizontal_button_widget)
        horizontal_button_container.setAlignment(Qt.AlignBottom)
        horizontal_button_container.setContentsMargins(0, 0, 0, 0)
        horizontal_button_container.addWidget(self.clear_button)
        horizontal_button_container.addWidget(self.send_button)

        # Create vertical container for settings widget and buttons
        settings_buttons_widget = QWidget()
        vertical_container = QVBoxLayout(settings_buttons_widget)
        vertical_container.setContentsMargins(0, 0, 0, 0)
        vertical_container.addWidget(self.settings_widget)
        vertical_container.addWidget(horizontal_button_widget)

        bottom_layout.addWidget(settings_buttons_widget)

        self.send_progress_bar = QProgressBar()
        self.send_progress_bar.setTextVisible(False)
        self.send_progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 5px;
                border: 1px solid #FFFFFF;
             }

             QProgressBar::chunk {
                background-color: #5D3587;
                width: 20px;
             }

        """)
        self.send_progress_bar.setMaximumHeight(15)
        self.send_progress_bar.setAlignment(Qt.AlignCenter)
        self.email_engine_handle.progress_bar = self.send_progress_bar  # Gives email engine handle to progress bar

        # Add the top & bottom widgets to the send tab layout
        send_tab_layout.addWidget(top_widget)
        send_tab_layout.addWidget(bottom_widget)
        send_tab_layout.addWidget(self.send_progress_bar)

    def clear_all(self, sending_to_contacts_widget, email_editor_widget, tags_widget,
                  contact_options_widget_container, settings_widget):


        confirm = QAcceptDialog('Clear all information?',
                                'Are you sure you want to clear everything? This will remove all queued contacts, '
                                'media and any edits.',
                                parent=self)
        confirm.show()
        if confirm.exec_() == QDialog.Accepted:
            self.send_progress_bar.setValue(0)

            for contact in sending_to_contacts_widget.findChildren(QContactWidget):
                contact.deleteLater()

            sending_to_contacts_widget.current_contact_selected = None  # Resets the current contact selected
            sending_to_contacts_widget.total_contacts = 0
            sending_to_contacts_widget.counter_line_edit.setText(str(sending_to_contacts_widget.total_contacts))

            # Clears text editors
            email_editor_widget.clear_contacts()
            email_editor_widget.clear_global_message()
            email_editor_widget.clear_personal_message()

            # Clears the contact options
            contact_options_widget_container.emails_widget.clear_contact_info()
            contact_options_widget_container.date_widget.clear_date_info()

            # Clears the attachments widgets
            email_editor_widget.email_addons_widget.clear_addons_data()

            for tag in tags_widget.findChildren(TagItemWidget):
                tag.deleteLater()
            tags_widget.tag_description_edit.lineEdit().setText('')
            # Unchecks the global schedule widget

            settings_widget.global_schedule_widget.clear_date_info()

    @staticmethod
    def contacts_queued(sending_to_contacts_widget):
        widget_count = 0
        for widget in sending_to_contacts_widget.findChildren(QContactWidget):
            widget_count += 1

        if widget_count == 0:
            return False
        else:
            return True

    def check_contact_email_message(self, sending_to_contacts_widget, email_editor_widget):
        # Should check that a global subject line and body exists, or that each contact has a personal subject and body
        if email_editor_widget.global_body_subject_line.text() == '' or email_editor_widget.global_body_editor.toPlainText() == '':  # If no global subject line is set or global body is empty
            for contact in sending_to_contacts_widget.findChildren(
                    QContactWidget):  # It will check that each contact is using a personal message since no global message is set to default to
                if html_paragraph_empty(
                        contact.personal_message) or contact.personal_message_subject_line == '':  # If no personal subject line exists
                    return False
        return True

    def populate_dynamic_fields(self, contact_id, email_body_editor):

        email_body_editor_copy = QTextBrowser()
        email_body_editor_copy.setHtml(email_body_editor.toHtml())

        fields_pattern = r'{{(.*?)}}'
        fields = re.findall(fields_pattern, email_body_editor_copy.toPlainText())

        for field in fields:
            if field == 'official_name':
                official_name = self.database_handle.get_official_name(contact_id)
                if official_name is None:  # If no official_name is found
                    official_name = ''  # Use empty string

                key = '{{' + field + '}}'
                email_body_editor_copy = email_body_editor_copy.replace(key, official_name)

            elif field == 'country':
                country = self.database_handle.get_contact_country(contact_id)
                if country is None:  # If no official_name is found
                    country = ''  # Use empty string

                key = '{{' + field + '}}'

                email_body_editor_copy = email_body_editor_copy.replace(key, country)

            elif field == 'instagram_followers':

                instagram_followers = self.database_handle.get_instagram_followers(contact_id)
                if instagram_followers is None:  # If no official_name is found
                    instagram_followers = ''  # Use empty string
                key = '{{' + field + '}}'

                email_body_editor_copy = email_body_editor_copy.replace(key, instagram_followers)

            elif field == 'contact_website':
                contact_website = self.database_handle.get_contact_website(contact_id)
                if contact_website is None:  # If no official_name is found
                    contact_website = ''  # Use empty string

                key = '{{' + field + '}}'
                email_body_editor_copy = email_body_editor_copy.replace(key, contact_website)

            elif field == 'contact_name':
                contact_name = self.database_handle.get_contact_name(contact_id)
                if contact_name is None:  # If no official_name is found
                    contact_name = ''  # Use empty string

                key = '{{' + field + '}}'
                email_body_editor_copy = email_body_editor_copy.replace(key, contact_name)


            elif field == 'from_name':
                from_email = self.database_handle.get_from_email_by_id(contact_id)
                # from_email should always exist
                key = '{{' + field + '}}'

                email_body_editor_copy = email_body_editor_copy.replace(key, from_email)

            fields = [x for x in fields if x != field]

        return email_body_editor_copy

    def extract_contact_options(self, contact_widget, email_editor_widget):
        contact_info = dict()

        contact_info['contact_id'] = int(contact_widget.contact_id)  # Sets the contact ID to be an integer

        contact_info['from_email'] = contact_widget.from_email  # Sets the
        # from_email_id

        if email_editor_widget.use_global_message_flag.isChecked():  # If user has checked option to send global
            # message to everyone
            email_body = self.populate_dynamic_fields(contact_widget.contact_id,
                                                      email_editor_widget.global_body_editor)  # Replaces
            # placeholders with actual values
            contact_info['subject_line'] = email_editor_widget.global_body_subject_line.text()
            contact_info['email_body'] = email_body.toHtml()

        else:  # If that is not checked, it will check each contact for a personal email and if not use the global
            if contact_widget.personal_message_subject_line:  # If contact has a personal subject line
                contact_info['subject_line'] = contact_widget.personal_message_subject_line
            else:  # Else it uses the global subject line
                contact_info['subject_line'] = email_editor_widget.global_body_subject_line.text()

            if contact_widget.personal_message and not html_paragraph_empty(
                    contact_widget.personal_message):  # Checks if contact has a personal email body
                contact_info['email_body'] = contact_widget.personal_message
            else:  # Else use the global email body

                email_body = self.populate_dynamic_fields(contact_widget.contact_id,
                                                          email_editor_widget.global_body_editor)  # Repalce
                # placeholders with actual values
                contact_info['email_body'] = email_body.toHtml()

        # Get from_email_id from text so we can save the ID into the DB
        contact_info['to_emails'] = contact_widget.to_emails  # Gets to emails from contact object
        contact_info['cc_emails'] = contact_widget.cc_emails  # Gets cc emails from contact object

        if contact_widget.send_date:  # If the contact has a specific send date. It may be empty ''
            contact_info['send_date'] = contact_widget.send_date.toString('yyyy-MM-dd HH:mm:ss')
            if contact_widget.send_date.toString() == '':  # If send date is empty set to non
                contact_info['send_date'] = None
            else:  # If not empty set it to the specified format
                contact_info['send_date'] = contact_widget.send_date.toString('yyyy-MM-dd HH:mm:ss')
        else:  # If  no specific send_date is specified
            contact_info['send_date'] = None

        if contact_widget.attachments:
            contact_info['attachments'] = contact_widget.attachments
        else:
            contact_info['attachments'] = None

        return contact_info  # Return the dictionary with the contact info

    def get_settings_info(self, settings_info_widget):
        settings_info = dict()

        if settings_info_widget.global_schedule_widget.enable_checkbox.isChecked():
            date_string = settings_info_widget.global_schedule_widget.get_selected_date()
        else:
            date_string = None
        settings_info['send_date'] = date_string
        return settings_info

    def send_button_clicked(self, sending_to_contacts_widget, contact_options_widget_container, email_editor_widget,
                            settings_widget, testing=False):
        # Needs to check that all required info exists. If not, display error prompts
        # Needs to get all the info from widgets and send the emails out
        if not self.contacts_queued(sending_to_contacts_widget):  # If no contacts are queued
            error_prompt = QErrorPrompt('No contacts queued',
                                        'No contacts are queued. Click add contacts or add tags to import contacts!',
                                        parent=self)
            error_prompt.show()
            return

        email_editor_widget.save_message_clicked()  # Ensure save if contacts were just imported and then email sent
        contact_options_widget_container.date_widget.save_contact_options()  # Ensure any date changes are saved for
        # the last selected contact

        all_contacts_options = []  # List that will hold a dictionary for each of the contact
        settings_info = self.get_settings_info(settings_widget)  # Gets a dictionary for the settings info
        global_attachments = email_editor_widget.get_global_email_attachments()

        for contact in sending_to_contacts_widget.findChildren(QContactWidget):  # Iterates the contact widgets
            contact_options = self.extract_contact_options(contact,
                                                           email_editor_widget)  # Gets the contact info like contact
            # id, from_email, to_emails, cc_emails
            all_contacts_options.append(contact_options)

        transaction_info = all_contacts_options  # Use this value to send to email engine to send out
        # emails
        transaction_info.append(settings_info)
        transaction_info.append(global_attachments)

        confirm_transfer = QConfirmTransactionDialog(transaction_info, sending_to_contacts_widget.total_contacts, parent=self)
        confirm_transfer.show()

        if confirm_transfer.exec_() == QDialog.Accepted:
            self.email_engine_handle.process_transaction_batch(sending_to_contacts_widget.total_contacts,
                                                               transaction_info)  # Processes the transactions to
            self.archived_transactions_widget.load_transactions(new=True)

    def transaction_engine_error_occured(self, Error):
        error_handle = QErrorPrompt(Error[0], Error[1], self)
        error_handle.exec_()

    def transaction_sent(self, transaction_id):
        # Using transaction id, we need to check if it's a listed transaction in scheduled transactions and remove it
        self.active_transactions_widget.remove_transaction_widget(transaction_id)  # Use transaction_id to remove any
        # transaction widgets
        # In the scheduled tab

    def transactions_failed(self, fail_info):

        # Set the failed bit to true for each failed transaction
        # Add failed logo to the transactions that failed
        # Remove transaction
        failed_transactions = fail_info[0]  # List with failed transactions
        fail_type = fail_info[1]

        # Needs to use the transaction ids of failed transactions to change the failed flag bit in
        # archived transactions and remove it from active transactions if it exists
        # archived transactions list should then redraw the currently shown archive transactions
        # so that those with the failed bit have a fail icon indicating that it failed
        transaction_ids = []

        for transaction in failed_transactions:
            transaction_ids.append(transaction[-1])

        self.active_transactions_widget.remove_transaction_widget(transaction_ids) # Removes them from the scheduled
        # transaction list
        self.archived_transactions_widget.transactions_failed(transaction_ids)
        self.database_handle.set_failed_transactions(transaction_ids)

    def active_transaction_edited(self, transaction_id):
        # Update the archived transaction
        for transaction in self.archived_transactions_widget.transactions:
            if transaction.transaction_id == transaction_id:
                info = self.database_handle.get_archived_transaction_by_id(transaction_id)
                to_emails, cc_emails = self.database_handle.get_archived_emails(transaction_id)
                info.insert(4, to_emails)
                info.insert(5, cc_emails)
                attachments = self.database_handle.get_attachments_by_transaction(transaction_id)
                info.insert(7, attachments)

                transaction.redraw_transaction_widget(info)

    def create_from(self):
        handle = QLinkEmailAccountForm(self.database_handle, parent=self)
        handle.show()

        if handle.exec_() == QDialog.Accepted:
            self.contact_options_widget_container.reinit_from_emails()
            return handle.accept()
        else:
            return handle.reject()


application_handle = QApplication(sys.argv)
application_handle.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
application_handle.setAttribute(Qt.AA_EnableHighDpiScaling)
application_handle.setAttribute(Qt.AA_UseHighDpiPixmaps)

application_handle.setWindowIcon(QIcon(logo_icon_path))
application_handle.setStyleSheet(application_style)

database_handle = Database.Database()
connection_pool = Database.ConnectionPool()
#database_handle.create_test_data()

email_engine_handle = TransactionEngine.TransactionManager(database_handle)
email_engine_handle.start_transaction_manager()

main_window_handle = MainWindow(database_handle, email_engine_handle)
main_window_handle.show()

email_engine_handle.transactions_failed.connect(partial(main_window_handle.transactions_failed))
email_engine_handle.transaction_sent.connect(partial(main_window_handle.transaction_sent))
email_engine_handle.uploaded_transactions.connect(partial(main_window_handle.active_transactions_widget.load_transactions, True))
sys.exit(application_handle.exec())
