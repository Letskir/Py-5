from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QInputDialog,QMessageBox
from ui import Ui_Main
import json

data=""

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        global data
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        with open ("new.json","r") as file:
            data=json.load(file)
        
app = QApplication([])
ex = Widget()
ex.show()


print(data)

ex.ui.search_btn.setText("Шукати по тегу")
def f_add_text_note():
    if ex.ui.list_zamitok.selectedItems():
        note_name = ex.ui.list_zamitok.selectedItems()[0].text()
        ex.ui.list_tegs.clear()
        ex.ui.list_tegs.addItems(data[note_name]["tegs"])
def show_note():
    if ex.ui.list_zamitok.selectedItems():
        name = ex.ui.list_zamitok.selectedItems()[0].text()
        ex.ui.text_area_edit.setText(data[name]["text"])
        ex.f_add_text_note()

  
def f_create_note():
    note_name, result=QInputDialog.getText(ex,"Додати замітку","Назва замітки")
    if note_name!="" and result==True:
        data[note_name]={"text":"", "tegs":[]}
        print(data)
        with open ("new.json","w") as file:
            json.dump(data, file)
        ex.ui.list_zamitok.addItem(note_name)
def save_note():
    if ex.ui.list_zamitok.selectedItems():
        name= ex.ui.list_zamitok.selectedItems()[0].text()
        data[name]['text']=ex.ui.text_area_edit.toPlainText()
        with open ("new.json","w") as file:
            json.dump(data, file)
def del_note():
    if ex.ui.list_zamitok.selectedItems():
        name= ex.ui.list_zamitok.selectedItems()[0].text()
        del data[name]
        with open ("new.json","w") as file:
            json.dump(data, file)
        ex.ui.list_zamitok.clear()
        ex.ui.list_tegs.clear()
        ex.ui.text_area_edit.clear()
        ex.ui.list_zamitok.addItems(data)
def add_tag():
    if ex.ui.list_zamitok.selectedItems():
        name = ex.ui.list_zamitok.selectedItems()[0].text()
        new_tag = ex.ui.search_line.text()
        if new_tag and new_tag not in data[name]["tegs"]:
            data[name]["tegs"].append(new_tag)
            with open("new.json", "w") as file:
                json.dump(data, file, sort_keys=True)
            ex.ui.list_tegs.addItem(new_tag)  
        elif new_tag in data[name]["tegs"]:
          message_box=QMessageBox()
          message_box.setText("Тег з таким ім'ям існує, виберіть іншу назву")
          message_box.show()
          message_box.exec_() 
        ex.ui.search_line.clear()

def del_tag():
    if ex.ui.list_tegs.selectedItems():
        key = ex.ui.list_zamitok.selectedItems()[0].text()
        tag = ex.ui.list_tegs.selectedItems()[0].text()
        data[key]["tegs"].remove(tag)
        ex.ui.list_tegs.clear()
        ex.ui.list_tegs.addItems(data[key]["tegs"])
        with open("new.json", "w") as file:
            json.dump(data, file, sort_keys=True, ensure_ascii=False) 

def search_tag():
    tag=ex.ui.search_line.text()
    if ex.ui.search_btn.text()=="Шукати по тегу" and tag:
        notes_filtered={}
        for note in data:
            if tag in data[note]["tegs"]:
                notes_filtered[note]=data[note]
        ex.ui.search_btn.setText("Закінчити пошук")
        ex.ui.list_zamitok.clear()
        ex.ui.list_tegs.clear()
        ex.ui.list_zamitok.addItems(notes_filtered)
    elif ex.ui.search_btn.text()=="Закінчити пошук":
        ex.ui.search_line.clear() 
        ex.ui.list_zamitok.clear()
        ex.ui.list_tegs.clear() 
        ex.ui.list_zamitok.addItems(data)
        ex.ui.search_btn.setText("Шукати по тегу")  
    else:
        pass
ex.ui.search_btn.clicked.connect(search_tag)
ex.ui.list_zamitok.addItems(data)
ex.ui.btn_dontadd.clicked.connect(del_tag)
ex.ui.btn_delete_zam.clicked.connect(del_note)
ex.ui.list_zamitok.itemClicked.connect(f_add_text_note)
ex.ui.btn_create_zam.clicked.connect(f_create_note)
ex.ui.btn_save_zam.clicked.connect(save_note)
ex.ui.btn_add.clicked.connect(add_tag)

app.exec_()

