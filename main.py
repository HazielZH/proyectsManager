import flet as ft
import os
import subprocess



def main(page: ft.Page):
    mainColumn = ft.Column()
    page.title = "Proyect Manager"
    codePathChecked = False
    storagePathChecked = False
    def customDir(e):
        if os.path.exists(e.control.value):
            if "vscode" in e.control.value:
                page.client_storage.set("CodePath", e.control.value)
                codePathChecked = True
            if "storage" in e.control.value:
                page.client_storage.set("StoragePath", e.control.value)
                storagePathChecked = True
            mainColumn.controls.remove(e.control)
            mainColumn.update()
        else: 
            e.control.value = "Ese path no existe"
            e.control.update()

    def checkCodePath():
        if page.client_storage.contains_key("CodePath"):
            codePathChecked = True
        else : 
            osUser = os.getlogin()
            codePath = f"C:\\Users\\{osUser}\\AppData\\Local\\Programs\\Microsoft VS Code"
            if os.path.exists(codePath):
                page.add(ft.Text(value="Existe code"))
                os.chdir(codePath)
                page.client_storage.set("CodePath", codePath)
                subprocess.run('code')
                codePathChecked = True
            else:
                textDir = ft.TextField(helper_text="Ingresa el dir de vscode", on_submit=customDir)
                mainColumn.controls.append(textDir)
    
    def checkStoragePath():
        if page.client_storage.contains_key("StoragePath"):
            storagePathChecked = True
        else:
            osUser = os.getlogin()
            storagePath = f"C:\\Users\\{osUser}\\AppData\\Roaming\\Code\\User\\globalStorage\\storage.json"
            if os.path.exists(storagePath) and True == False:
                page.client_storage.set("StoragePath", storagePath)
                storagePathChecked = True
            else: 
                textDir = ft.TextField(helper_text="Ingresa el dir de storage.json, este debe terminar tal que \\storage.json", on_submit=customDir)
                mainColumn.controls.append(textDir)
                mainColumn.update()

    page.add(
        mainColumn
    )
    if not page.client_storage.contains_key("CodePath"):
        checkCodePath()
    if not page.client_storage.contains_key("StoragePath"):
        checkStoragePath()
    while True:
        if checkCodePath:
            a = 1




ft.app(main)
