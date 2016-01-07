#!/usr/bin/python

#http://www.pythonschool.net/pyqt/switching-layouts/
#Use QTextEdit to read files

import sys
import os
from PyQt4.QtGui import *

tstpath = "/tmp/interactive"


class RadioButtonWidget(QWidget):
    def __init__(self,label,instruction,button_list):
        super().__init__()
        self.title_label = QLabel(label)
        self.radio_group_box = QGroupBox(instruction)
        self.radio_button_group = QButtonGroup()
        self.radio_button_list = []
        for each in button_list:
            self.radio_button_list.append(QRadioButton(each))
        self.radio_button_list[0].setChecked(True)
        self.radio_button_layout = QVBoxLayout()
        counter = 1
        for each in self.radio_button_list:
            self.radio_button_layout.addWidget(each)
            self.radio_button_group.addButton(each)
            self.radio_button_group.setId(each,counter)
            counter+=1
            
        self.radio_group_box.setLayout(self.radio_button_layout)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.radio_group_box)
        self.setLayout(self.main_layout)

    def selected_button(self):
        return self.radio_button_group.checkedId()

class TextView(QDialog):
    def __init__(self,title,filepath,main):
        super().__init__()
        self.title_label = QLabel(title)
        self.text_edit = QTextEdit()
        updateFiles(main.choices)
        f = open(filepath)
        self.text_edit.setText(f.read())
        f.close()
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.done)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.addWidget(self.ok_button)
        self.setLayout(self.main_layout)
    

def updateFiles(choices):
    apppath = os.path.join(tstpath,"application.py")
    updpath = os.path.join(tstpath,"update.py")
    print("updating files")



    
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chose your own strategy update")
        self.choices = {"manager":0,"static":0,"picskel":0,"type":0,"access":0,"funskel":0,"funalt":0,"funapp":0}
        self.current_layout = 0
        #Create all option select widgetand layouts
        i0 = self.create_info("Here, you will chose how to update your picture server!\n\nLet's look at its code first.",action=self.genview(os.path.join(tstpath,"application.py")))
        i1 = self.create_info("Before starting the application, we need to decide a few things")
        mantype = self.create_mec_select("Do we add a manager to the application?",("Add a threaded manager","Add a non-threaded manager","Do not add a manager"),"manager")
        staticpoint = self.create_mec_select("Do we put static update points?",("Put a point in main's loop","Put a point in threads loop","Do not pout static update points"),"static")
        i2 = self.create_info("We are now ready to start the application.")
        launch = self.create_launch()
        i3 = self.create_info("It is now time to launch the client",back=False)
        #Update picture type
        i4 = self.create_info("Ready for a dynamic update?\nLet's take a look at the code.",action=self.checkman)
        i5 = self.create_info("Let's update the Picture class\nBecause the new version of Picture is backward compatible, we don't have to mind alterability\n\nLet's look at the skeleton of our update",action=self.genview(os.path.join(tstpath,"update.py")))
        picupd = self.create_mec_select("How do we update the Picture class?",("Redefine the class","Add the new version along the old one"),"type")
        access = self.create_mec_select("How do we access Picture instances?",("Eagerly","Lazily"),"access")
        i6 = self.create_info("Then, send the update to the manager",action=self.genview(os.path.join(tstpath,"update.py")))
        #Update functions
        i7 = self.create_info("Now,let's update the threads handling the connections.\n\nFor consistency, we need to update both do_command and serve_folder at the same time.\nLet's chose alterability criteria.",action=self.startfun)

        #Add them to a stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(i0)
        self.stacked_layout.addWidget(i1)
        self.stacked_layout.addWidget(mantype)
        self.stacked_layout.addWidget(staticpoint)
        self.stacked_layout.addWidget(i2)
        self.stacked_layout.addWidget(launch)
        self.stacked_layout.addWidget(i3)
        self.stacked_layout.addWidget(i4)
        self.stacked_layout.addWidget(i5)
        self.stacked_layout.addWidget(picupd)
        self.stacked_layout.addWidget(access)
        self.stacked_layout.addWidget(i6)
        self.stacked_layout.addWidget(i7)

        #Set the stacked layout as the central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def genview(self,path):
        def action():
            title = "Code of "+os.path.basename(path)
            d = TextView(title,path,self)
            d.exec_()
            self.next()
        return action

    def checkman(self):
        if self.choices["manager"] == 3:
            #Manager was not installed, install it now
            title = "We need to add a manager to the application"
        else:
            title = "Code of "+os.path.join(tstpath,"update.py")
        d = TextView(title,os.path.join(tstpath,"update.py"),self)
        d.exec_()
        self.choices["picskel"] = 1
        self.next()

    def startfun(self):
        if self.choices["static"] == 1: #main loop
            i7b = self.create_info("Unfortunately, we cannot use our static update point in main's loop : the functions are not alterable here.")
            self.stacked_layout.addWidget(i7b)
            funalt = self.create_mec_select("When shall we update the functions?",("When the functions are quiescent",),"funalt")
        elif self.choices["static"] == 2: #thread loop
            funalt = self.create_mec_select("When shall we update the functions?",("When a static point is reached","When the functions are quiescent"),"funalt")
        else:
            funalt = self.create_mec_select("When shall we update the functions?",("When the functions are quiescent",),"funalt")
        i8 = self.create_info("We can modify the apply method of the update, then send it to the manager.",action=self.funcomplete)
        i9 = self.create_info("The update is now ready to be applied!",action=self.update)
        i10 = self.create_info("The updating process as started.\nDo you see thenew features?",back=False)
        q = self.create_quit_info()
        self.stacked_layout.addWidget(funalt)
        self.stacked_layout.addWidget(i8)
        self.stacked_layout.addWidget(i9)
        self.stacked_layout.addWidget(i10)
        self.stacked_layout.addWidget(q)
        self.choices["funskel"] = 1
        self.next()

    def funcomplete(self):
        self.choices["funapp"] = 1
        self.genview(os.path.join(tstpath,"update.py"))()
        self.next()

    def update(self):
        print("update!")
        self.next()
        
    def back(self):
        if self.current_layout > 5:
            self.current_layout -= 1
        elif self.current_layout < 5 and self.current_layout > 0:
            self.current_layout -= 1 
        self.stacked_layout.setCurrentIndex(self.current_layout)

    def next(self):
        self.current_layout += 1
        self.stacked_layout.setCurrentIndex(self.current_layout)

    def quit(self):
        self.close()
        
    def mec_select_action(self,radio_buttons,key):
        def action():
            mec_id = radio_buttons.selected_button()
            self.choices[key] = mec_id
            if key in ["manager","static"]:
                self.genview(os.path.join(tstpath,"application.py"))()
            else:
                self.genview(os.path.join(tstpath,"update.py"))()
        return action

    def launch(self,paths_field):
        def action():
            print(paths_field.text())
            self.next()
        return action

    def create_mec_select(self,title,options,key):
        radio_buttons = RadioButtonWidget(title,'Select one mechanism',options)
        apply_button = QPushButton("Use this mechanism")
        back_button = QPushButton("Back")
        #layout
        layout = QVBoxLayout()
        layout0 = QHBoxLayout()
        layout0.addWidget(back_button)
        layout0.addWidget(apply_button)
        layout.addWidget(radio_buttons)
        layout.addLayout(layout0)
        mec_widget = QWidget()
        mec_widget.setLayout(layout)
        apply_button.clicked.connect(self.mec_select_action(radio_buttons,key))
        back_button.clicked.connect(self.back)
        return mec_widget
    
    def create_info(self,text,back=True,action=None):
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        ok_button = QPushButton("Ok")
        back_button = QPushButton("Back")
        if back:
            back_button.clicked.connect(self.back)
        else:
            back_button.setEnabled(False)
        layout = QVBoxLayout()
        layout0 = QHBoxLayout()
        layout0.addWidget(back_button)
        layout0.addWidget(ok_button)
        layout.addWidget(text_label)
        layout.addLayout(layout0)
        info_widget = QWidget()
        info_widget.setLayout(layout)
        if action:
            ok_button.clicked.connect(action)
        else:
            ok_button.clicked.connect(self.next)
        return info_widget

    def create_quit_info(self):
        text_label = QLabel("The demo is now finished.\n\nGood bye!")
        text_label.setWordWrap(True)
        quit_button = QPushButton("Quit")
        back_button = QPushButton("Back")
        layout = QVBoxLayout()
        layout0 = QHBoxLayout()
        layout0.addWidget(back_button)
        layout0.addWidget(quit_button)
        layout.addWidget(text_label)
        layout.addLayout(layout0)
        quit_widget = QWidget()
        quit_widget.setLayout(layout)
        quit_button.clicked.connect(self.quit)
        back_button.clicked.connect(self.back)
        return quit_widget

    def create_launch(self):
        text_label= QLabel("It is now time to launch the application\nPlease enter paths fo the folders to serve (separated by spaces)")
        text_label.setWordWrap(True)
        paths_field = QLineEdit()
        launch_button = QPushButton("Launch")
        back_button = QPushButton("Back")
        layout = QVBoxLayout()
        layout0 = QHBoxLayout()
        layout0.addWidget(back_button)
        layout0.addWidget(launch_button)
        layout.addWidget(text_label)
        layout.addWidget(paths_field)
        layout.addLayout(layout0)
        launch_widget = QWidget()
        launch_widget.setLayout(layout)
        launch_button.clicked.connect(self.launch(paths_field))
        back_button.clicked.connect(self.back)
        return launch_widget

        
app = QApplication(sys.argv)

mec = MainWindow()
mec.show()
mec.raise_()

app.exec_()

