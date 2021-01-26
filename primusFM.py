from PyQt5 import QtWidgets, QtCore, QtGui
from base import Ui_form
from sys import argv, exit
from getpass import getuser
user=getuser()

# IF YOU WANT AN EXPLANATION TO UNDERSTAND WHICH PART WHY HERE, JUST CONTACT ME. https://github.com/duxeph // furieuxx13@gmail.com
class window(QtWidgets.QWidget):
    def __init__(self):
        super(window,self).__init__()

        self.ui=Ui_form()
        self.ui.setupUi(self)

        from os import chdir, getcwd
        from json import load, dump
        from sys import argv, executable
        from pkg_resources import working_set
        from subprocess import DEVNULL, check_call
        
        self._translate = QtCore.QCoreApplication.translate

        self.tickOn=False # hidden files will be shown
        self.lastPage=[]
        self.ui.baseTree.setColumnWidth(0, 430)
        self.ui.redoButton.setEnabled(0)

        file_name=argv[0].split("/")[-1]
        mainfile=argv[0][:-len(file_name):]
        check=load(open(f"{mainfile}/controller.txt"))

        if not bool(check["controls"][1]["is_os_checked"]):
            import platform
            if platform.system()=="Linux":
                check["controls"][1]["is_os_checked"]=1
                dump(check,open(f"{mainfile}/controller.txt","w"))
            else:
                QtWidgets.QMessageBox.information(self,"Quick Information","This application made for linux based systems. If you are a windows user, just wait until it releases. Thanks for your endurance!",QtWidgets.QMessageBox.Ok)
                exit()

        if not bool(check["controls"][0]["is_req_checked"]):
            required = {'pyqt5'}
            installed = {pkg.key for pkg in working_set}
            missing = required - installed
            if missing:
                python = executable
                check_call([python, '-m', 'pip', 'install', *missing], stdout=DEVNULL)
            check["controls"][0]["is_req_checked"]=1

        if not bool(check["controls"][2]["is_info_checked"]):
            QtWidgets.QMessageBox.information(self,"Welcome!","Thanks for coming and choosing me! This is the first version of application. So, please contact its owner if you see any error or mistake in codes, thanks!\n\nOwner's GitHub: https://github.com/duxeph\nContact mail: furieuxx13@gmail.com",QtWidgets.QMessageBox.Ok)
            check["controls"][2]["is_info_checked"]=1
            dump(check,open(f"{mainfile}/controller.txt","w"))


        self.home=f"/home/{user}/Desktop"
        chdir(self.home) # cd {directory} => change directory
        self.regard()

        self.ui.baseTree.clicked.connect(self.opener)

        self.ui.backButton.clicked.connect(self.backFunction)
        self.ui.homeButton.clicked.connect(self.homeFunction)
        self.ui.redoButton.clicked.connect(self.redoFunction)
        
        self.ui.baseTree.doubleClicked.connect(self.goInFunction)

        self.ui.renameButton.clicked.connect(self.renameFunction)
        self.ui.removeButton.clicked.connect(self.removeFunction)
        self.ui.newFolderButton.clicked.connect(self.newFolderFunction)

        self.ui.goButton.clicked.connect(self.goFunction)
        self.ui.execButton.clicked.connect(self.execFunction)

    def regard(self):
        from os import stat, listdir, getcwd
        from os.path import isdir
        from time import strftime, localtime

        if getcwd()=="/":
            self.ui.directoryLabel.setText(getcwd()) # pwd => current directory
        else:
            self.ui.directoryLabel.setText(getcwd()+"/") # pwd => current directory
        self.sorted_list = sorted(listdir(), key=str.lower) #ls; but shows all the items as python;list

        self.ui.baseTree.clear()
        check=-1

        for i in range(len(self.sorted_list)):
            if not self.sorted_list[i].startswith(".") or self.tickOn:
                check+=1
                item_0 = QtWidgets.QTreeWidgetItem(self.ui.baseTree) # empty item added
                self.ui.baseTree.topLevelItem(check).setText(0, self._translate("form", self.sorted_list[i])) # add its name
    
                if isdir(self.sorted_list[i]): # => true if it is a folder/directory
                    self.ui.baseTree.topLevelItem(check).setText(1, self._translate("form", "Folder")) # add item's type
                else: # os.path.isfile(ls[i]) # => true if it is a file
                    self.ui.baseTree.topLevelItem(check).setText(1, self._translate("form", "File")) # add item's type

                # self.size = '{:.1f}'.format(stat(self.sorted_list[i])[6]/1024) # KiB
                if stat(self.sorted_list[i])[6] < 1024: # bytes
                    self.ui.baseTree.topLevelItem(check).setText(2, self._translate("form", f'{str(stat(self.sorted_list[i])[6])} bytes')) # size
                elif 1024 <= stat(self.sorted_list[i])[6] < 1024*1024: # KiB
                    self.ui.baseTree.topLevelItem(check).setText(2, self._translate("form", f"{'{:.1f}'.format(stat(self.sorted_list[i])[6]/1024)} KiB")) # size
                elif 1024*1024 <= stat(self.sorted_list[i])[6] < 1024*1024*1024: # MiB
                    self.ui.baseTree.topLevelItem(check).setText(2, self._translate("form", f"{'{:.1f}'.format(stat(self.sorted_list[i])[6]/(1024*1024))} MiB")) # size
                elif 1024*1024*1024 <= stat(self.sorted_list[i])[6] < 1024*1024*1024*1024: # GiB
                    self.ui.baseTree.topLevelItem(check).setText(2, self._translate("form", f"{'{:.1f}'.format(stat(self.sorted_list[i])[6]/(1024*1024*1024))} GiB")) # size
                else:
                    self.ui.baseTree.topLevelItem(check).setText(2, self._translate("form", f"{'{:.1f}'.format(stat(self.sorted_list[i])[6]/(1024*1024*1024*1024))} TiB")) # size

                self.ui.baseTree.topLevelItem(check).setText(3, self._translate("form", strftime('%H:%M %d/%m/%Y', localtime(stat(self.sorted_list[i])[7])))) # last access
                self.ui.baseTree.topLevelItem(check).setText(4, self._translate("form", strftime('%H:%M %d/%m/%Y', localtime(stat(self.sorted_list[i])[8])))) # last modification


    def opener(self):
        self.ui.renameButton.setEnabled(1)
        self.ui.removeButton.setEnabled(1)
    
    def closer(self):
        self.ui.renameButton.setEnabled(0)
        self.ui.removeButton.setEnabled(0)
        self.regard()


    def goInFunction(self):
        from os import system, chdir, getcwd
        from os.path import isdir, splitext

        self.selectedIndex = self.ui.baseTree.selectedIndexes()[0].row()
        self.selectedName = self.ui.baseTree.selectedItems()[0].text(0)

        if isdir(self.selectedName):
            chdir(getcwd()+"/"+self.selectedName)

        else:
            self.ext=splitext(self.selectedName)[1] #splits file's name and its extension ==> ("file",".py")
            
            if self.ext=='.txt' or self.ext=='.md':
                self.ui.commandArea.setText('gedit '+self.selectedName)
                system('gedit '+self.selectedName)

            elif self.ext=='' or self.ext=='.sh' or self.ext=='.py' or self.ext=='.c' or self.ext=='.cpp' or self.ext=='.html':
                option=QtWidgets.QMessageBox.question(self,"Open process","Do you want to execute the file?",QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)

                if option==QtWidgets.QMessageBox.Yes:
                    if self.ext=='' or self.ext=='.sh':
                        self.ui.commandArea.setText(f'chmod +x ./{self.selectedName} && ./{self.selectedName}')
                        system(f'chmod +x ./{self.selectedName} && ./{self.selectedName}')  # x && y ==> if x is True; after y
                    elif self.ext=='.py':
                        self.ui.commandArea.setText('python3 '+self.selectedName)
                        system('python3 '+self.selectedName)
                    elif self.ext=='.c' or self.ext=='.cpp' or self.ext=='.html':
                        QtWidgets.QMessageBox.information(self,"Information","Not supported, edit opening...",QtWidgets.QMessageBox.Ok)
                        self.ui.commandArea.setText('gedit '+self.selectedName)
                        system('gedit '+self.selectedName)

                elif option==QtWidgets.QMessageBox.No:
                    self.ui.commandArea.setText('gedit '+self.selectedName)
                    system('gedit '+self.selectedName)

            elif self.ext=='.desktop':
                self.f=open(self.selectedName).readlines()
                for i in range(len(self.f)):
                    if self.f[i].startswith("Exec="):
                        self.ui.commandArea.setText(self.f[i][5::].strip())
                        system(self.f[i][5::].strip())
                        break

        self.ui.renameButton.setEnabled(0)
        self.ui.removeButton.setEnabled(0)
        self.regard()
	

    def goFunction(self):
        from os import chdir
        from os.path import exists

        if exists(self.ui.directoryLabel.text()):
            chdir(self.ui.directoryLabel.text())
        self.closer()

    def execFunction(self):
        from os import system
        system(self.ui.commandArea.text()+' > results.txt')
        see=open('results.txt').read()
        QtWidgets.QMessageBox.information(self,"Result(s)",see,QtWidgets.QMessageBox.Ok)
        system('mv results.txt ~/.local/share/Trash/files')


    def backFunction(self):
        from os import chdir, getcwd

        if len(self.lastPage)>0:
            if self.lastPage[-1]!=getcwd():
                self.lastPage.append(getcwd())
                self.ui.redoButton.setEnabled(1)
        else:
            self.lastPage.append(getcwd())
            self.ui.redoButton.setEnabled(1)
            
        if len(self.lastPage)>5:
            self.lastPage.pop(0)

        self.current=''
        for i in range(len(getcwd().split('/'))):
            if i+1==len(getcwd().split('/')):
                break
            self.current+=f"/{getcwd().split('/')[i]}"

        chdir(self.current)
        self.regard()

    def homeFunction(self):
        from os import chdir
        chdir(self.home)
        self.regard()

    def redoFunction(self):
        from os import chdir
        if len(self.lastPage)>0:
            chdir(self.lastPage[-1])
            self.lastPage.pop(-1)

            if len(self.lastPage)==0:
                self.ui.redoButton.setEnabled(0)
        self.regard()


    def renameFunction(self):
        from os import rename

        self.selectedIndex = self.ui.baseTree.selectedIndexes()[0].row()
        self.selectedName = self.ui.baseTree.selectedItems()[0].text(0)

        name, accept = QtWidgets.QInputDialog.getText(self, 'Change folder name', "Put the new name you want.",text=self.selectedName)
        if accept and len(name)>0:
            sureness=QtWidgets.QMessageBox.question(self,"Confirm","Are you sure?",QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Cancel)
            if sureness==QtWidgets.QMessageBox.Yes:
                try:
                    rename(self.selectedName,name) #changes name of file/folder
                    QtWidgets.QMessageBox.information(self,"Information","Successfully changed.",QtWidgets.QMessageBox.Ok)
                except Exception as error:
                    QtWidgets.QMessageBox.information(self,"Information","Couldn't change.",QtWidgets.QMessageBox.Ok)
        self.closer()

    def removeFunction(self):
        # from os import rmdir
        from os import system

        self.selectedIndex = self.ui.baseTree.selectedIndexes()[0].row()
        self.selectedName = self.ui.baseTree.selectedItems()[0].text(0)

        sureness=QtWidgets.QMessageBox.question(self,"Confirm","Are you sure?",QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Cancel)
        if sureness==QtWidgets.QMessageBox.Yes:
            try:
                # rmdir(self.selectedName) #deletes a folder as {name} from current directory.
                system(f"mv '{self.selectedName}' ~/.local/share/Trash/files")
                QtWidgets.QMessageBox.information(self,"Information","Successfully deleted.",QtWidgets.QMessageBox.Ok)
            except Exception as error:
                QtWidgets.QMessageBox.information(self,"Information","Couldn't delete.",QtWidgets.QMessageBox.Ok)
        self.closer()

    def newFolderFunction(self):
        from os import mkdir
        from os.path import exists
        name, accept = QtWidgets.QInputDialog.getText(self, 'Create a folder', "Put the folder's name you want.",text="New Folder")
        if accept and len(name)>0 and not exists(name):
            mkdir(name) #creates a folder to current directory as name
            QtWidgets.QMessageBox.information(self,"Information",f"{name} created.",QtWidgets.QMessageBox.Ok)
        elif exists(name):
            QtWidgets.QMessageBox.information(self,"Information",f"{name} already exists.",QtWidgets.QMessageBox.Ok)
        elif len(name)==0:
            QtWidgets.QMessageBox.information(self,"Information","Need to put a name.",QtWidgets.QMessageBox.Ok)

        self.regard()

if __name__=='__main__':
    app=QtWidgets.QApplication(argv)
    win=window()
    win.show()
    exit(app.exec_())
