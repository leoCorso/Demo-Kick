from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import pyqtSignal


class QSearchWidget(QComboBox):

    enter_pressed = pyqtSignal()

    def __init__(self, database_handle, parent=None):
        super().__init__(parent)

        self.database_handle = database_handle
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.lineEdit().textEdited.connect(self.updateFilter)
        self.filterString = ""
        self.suggestions = []
        self.cacheSuggestions()

        self.lineEdit().returnPressed.connect(self.return_pressed)

    def cacheSuggestions(self):
        self.suggestions = self.database_handle.get_cache_tags()
        self.clear()
        self.addItems(self.suggestions)
        self.setCurrentText('')

    def updateFilter(self, text):

        if self.lineEdit().text() == '':
            self.cacheSuggestions()
            return

        found = False


        for suggestion in self.suggestions:
            if text in suggestion:
                found = True
                break
        if not found:
            text = self.currentText()
            self.clear()
            self.lineEdit().setText(text)

            self.suggestions = self.database_handle.get_matching_tags(text)
            self.addItemsCombobox(self.suggestions)


    def addItemsCombobox(self, items):
        self.addItems(items)
        self.suggestions.extend(items)  # Add items to the full list

    def text(self):
        return self.currentText()

    def extract_text(self):
        text = self.currentText()
        self.cacheSuggestions()
        self.setCurrentText('')
        return text

    def setPlaceholderText(self, text):
        self.lineEdit().setPlaceholderText(text)

    def return_pressed(self):
        self.enter_pressed.emit()
        self.setCurrentText('')
