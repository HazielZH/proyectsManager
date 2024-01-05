import flet as ft
import os
import subprocess
import json


def main(page: ft.Page):
    mainColumn = ft.Column()
    page.title = "Proyect Manager"
    codePathChecked = False
    storagePathChecked = False
    proyectsPath = False
    profilesVS = []
    profile = "Default"
    def customDir(e):
        if os.path.exists(e.control.value):
            if "vscode" in e.control.value:
                page.client_storage.set("CodePath", e.control.value)
                codePathChecked = True
            if "storage" in e.control.value:
                page.client_storage.set("StoragePath", e.control.value)
                storagePathChecked = True
            else:
                page.client_storage.set("ProyectsPath", e.control.value)
                proyectsPath = True
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
                page.client_storage.set("CodePath", codePath)
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
            if os.path.exists(storagePath):
                page.client_storage.set("StoragePath", storagePath)
                storagePathChecked = True
            else: 
                textDir = ft.TextField(helper_text="Ingresa el dir de storage.json, este debe terminar tal que \\storage.json", on_submit=customDir)
                mainColumn.controls.append(textDir)
                mainColumn.update()

    def perfJson():
        Json = open(page.client_storage.get("StoragePath"), 'r')
        perfData = json.load(Json)
        for profiles in perfData['userDataProfiles']:
            dropMenu.options.append(ft.dropdown.Option(profiles['name']))
        Json.close()
        print(dropMenu.options)
        return True

    def checkProyectsPath():
        if page.client_storage.contains_key("ProyectsPath"):
            proyectsPath = True
        else:
            textDir = ft.TextField(helper_text="Ingresa el dir de tus proyectos", on_submit=customDir)
            mainColumn.controls.append(textDir)
            mainColumn.update()

    def changeProfile(e):
        profile = dropMenu.value

    def ExecuteVSCODE(e):
        os.chdir(page.client_storage.get('CodePath'))
        subprocess.run(f'code --profile {dropMenu.value} {page.client_storage.get('ProyectsPath')}')

    dropMenu = ft.Dropdown(
        on_change=changeProfile,
        options=[]
    )
    page.add(
        mainColumn,
        dropMenu
    )
    if not page.client_storage.contains_key("CodePath"):
        checkCodePath()
    if not page.client_storage.contains_key("StoragePath"):
        checkStoragePath()
    if not page.client_storage.contains_key("ProyectsStorage"):
        checkProyectsPath()
    perfJson()
    dropMenu.update()
    page.add(ft.FloatingActionButton(ft.icons.PLAY_ARROW_OUTLINED, on_click=ExecuteVSCODE))



ft.app(main)
