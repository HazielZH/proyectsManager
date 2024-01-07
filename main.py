import flet as ft
import os
import subprocess
import json
import asyncio




def main(page: ft.Page):
    mainColumn = ft.Column()
    page.title = "Proyect Manager"
    page.window_width = 350
    page.window_max_width = 500
    page.window_min_width = 350
    codePathChecked = False
    global currentDir
    storagePathChecked = False
    proyectsPath = False
    profilesVS = []
    profile = "Default"
    listOfDirectories = ft.Column()

    
    
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

    def ExecuteVSCODE(widgetPath):
        os.chdir(page.client_storage.get('CodePath'))
        print(f'code --profile {dropMenu.value} {widgetPath}')
        subprocess.run(f'code --profile {dropMenu.value} "{widgetPath}" --new-window')

    def goToXDirectory(e):
        global currentDir
        currentDir  = f"{e.control.tooltip}"
        listOfDirectories.controls.clear()
        getDirectories()

    def parentDirectory(e):
        os.chdir("..")
        global currentDir
        currentDir  = f"{os.path.dirname(currentDir)}"
        print(currentDir)
        listOfDirectories.controls.clear()
        getDirectories()
        listOfDirectories.update()

    def createDirWidget(widgetName, widgetPath):
        row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextButton(text=f'{widgetName}', on_click=goToXDirectory, tooltip=f'{widgetPath}'),
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Row([ft.Image(src="vscode-icon.png", width=25, height=25)]),
                                tooltip="Ejecutar en VS-Code",
                                on_click=lambda e: ExecuteVSCODE(widgetPath)
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete To-Do",
                            ),
                            ft.Image(src=ft.icons.ABC)
                        ],
                    ),
                ],
                width= 250
            )
        return row
    
    def newDirectory(e):
        a = 1


    async def async_create_flutter_project(e, dirButton):
        dirButton.controls[0].disabled = True
        dirButton.controls[1].controls[0].disabled = True
        dirButton.controls[1].controls[1].disabled = True
        dirButton.update()
        process = await asyncio.create_subprocess_shell(
            f'flet create {e.control.value}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.wait()
        dirButton.controls[0].disabled = False
        dirButton.controls[1].controls[0].disabled = False
        dirButton.controls[1].controls[1].disabled = False
        dirButton.update()


    def newFlutterProyect(e):
        os.chdir(currentDir)
        # Ejecutar la creación del proyecto de manera asíncrona
        dirButton = createDirWidget(e.control.value, f'{currentDir}\\{e.control.value}')
        listOfDirectories.controls.append(dirButton)
        listOfDirectories.controls.remove(textFieldFlet)
        listOfDirectories.update()
        asyncio.run(async_create_flutter_project(e, dirButton))
        textFieldFlet.value = ''
        os.chdir(page.client_storage.get("CodePath"))

    def getDirectories():
        with os.scandir(currentDir) as folders:
            for folder in folders:
                if folder.is_dir:
                    listOfDirectories.controls.append(createDirWidget(folder.name, folder.path))
        listOfDirectories.update()
        
    textFieldFlet = ft.TextField(hint_text='Nombre del proyecto', on_submit=newFlutterProyect)
    def addTextField(e):
        listOfDirectories.controls.append(textFieldFlet)
        listOfDirectories.update()

    dropMenu = ft.Dropdown(
        on_change=changeProfile,
        options=[]
    )
    page.add(
        mainColumn,
        dropMenu,
        ft.TextButton(
            text= '...',
            on_click=parentDirectory
        ),
        listOfDirectories,
    )
    if not page.client_storage.contains_key("CodePath"):
        checkCodePath()
    if not page.client_storage.contains_key("StoragePath"):
        checkStoragePath()
    if not page.client_storage.contains_key("ProyectsStorage"):
        checkProyectsPath()
    currentDir = page.client_storage.get('ProyectsPath')
    perfJson()
    dropMenu.update()
    getDirectories()
    page.add(ft.FloatingActionButton(on_click=addTextField, icon=ft.icons.ADD))


ft.app(main, assets_dir="assets")
