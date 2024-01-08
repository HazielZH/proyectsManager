import flet as ft
import os
import subprocess
import json
import asyncio


def main(page: ft.Page):
    mainColumn = ft.Column()
    page.title = "Proyect Manager"
    page.window_width = 380
    page.window_max_width = 500
    page.window_min_width = 350
    page.scroll
    global currentDir
    listOfDirectories = ft.Column()
    page.scroll = True
    
    def customDir(e):
        if os.path.exists(e.control.value):
            if "vscode" in e.control.value:
                page.client_storage.set("CodePath", e.control.value)
            if "storage" in e.control.value:
                page.client_storage.set("StoragePath", e.control.value)
            else:
                page.client_storage.set("ProyectsPath", e.control.value)

            mainColumn.controls.remove(e.control)
            mainColumn.update()
        else: 
            e.control.value = "Ese path no existe"
            e.control.update()

    def checkCodePath():
        if page.client_storage.contains_key("CodePath"):
            return
        else : 
            osUser = os.getlogin()
            codePath = f"C:\\Users\\{osUser}\\AppData\\Local\\Programs\\Microsoft VS Code"
            if os.path.exists(codePath):
                page.client_storage.set("CodePath", codePath)
            else:
                openVLG(3)
    
    def checkStoragePath():
        if page.client_storage.contains_key("StoragePath"):
            return
        else:
            osUser = os.getlogin()
            storagePath = f"C:\\Users\\{osUser}\\AppData\\Roaming\\Code\\User\\globalStorage\\storage.json"
            if os.path.exists(storagePath):
                page.client_storage.set("StoragePath", storagePath)
            else: 
                openVLG(4)

    def perfJson():
        try:
            Json = open(page.client_storage.get("StoragePath"), 'r')
            perfData = json.load(Json)
            Json.close()

            for profiles in perfData['userDataProfiles']:
                dropMenu.options.append(ft.dropdown.Option(profiles['name']))

            print(dropMenu.options)
            return True
        except KeyError:
            # La clave 'userDataProfiles' no existe en el JSON
            page.controls.remove(dropMenu)
            return False
        except Exception as e:
            page.controls.remove(dropMenu)
            return False

    def checkProyectsPath():
        if page.client_storage.contains_key("ProyectsPath"):
            return
        else:
            openVLG(2)
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
                                tooltip="Open folder in VS-Code",
                                on_click=lambda e: ExecuteVSCODE(widgetPath)
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete Folder",
                                on_click=lambda e: deleteFolder(widgetPath, row)
                            )
                        ],
                    ),
                ],
                width= 250
            )
        return row
    
    def closeDlg(dlg, confirm, path, row):
        if confirm == 1:
            listOfDirectories.controls.remove(row)
            listOfDirectories.update()
            subprocess.run(f'rd /s /q "{path}"', shell=True)
        dlg.open = False
        page.update()

    def deleteFolder(path, row):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confimarcion"),
            content=ft.Text("Estas seguro de eliminar la carpeta?"),
            actions=[
                ft.TextButton("Si", on_click=lambda e: closeDlg(dlg, 1, path, row)),
                ft.TextButton("No", on_click=lambda e: closeDlg(dlg, 0, '', row)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    async def async_create_flet_proyect(command, dirButton):
        dirButton.controls[0].disabled = True
        dirButton.controls[1].controls[0].disabled = True
        dirButton.controls[1].controls[1].disabled = True
        dirButton.update()
        process = await asyncio.create_subprocess_shell(
            f'{command}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.wait()
        dirButton.controls[0].disabled = False
        dirButton.controls[1].controls[0].disabled = False
        dirButton.controls[1].controls[1].disabled = False
        dirButton.update()


    def newProyect(e):
        os.chdir(currentDir)
        # Ejecutar la creación del proyecto de manera asíncrona
        dirButton = createDirWidget(e.control.value, f'{currentDir}\\{e.control.value}')
        listOfDirectories.controls.append(dirButton)
        listOfDirectories.controls.remove(textFieldFlet)
        listOfDirectories.update()
        asyncio.run(async_create_flet_proyect(f'{e.control.hint_text} "{e.control.value}"', dirButton))
        textFieldFlet.value = ''
        os.chdir(page.client_storage.get("CodePath"))

    def getDirectories():
        with os.scandir(currentDir) as folders:
            for folder in folders:
                if folder.is_dir:
                    listOfDirectories.controls.append(createDirWidget(folder.name, folder.path))
        listOfDirectories.update()
        
    textFieldFlet = ft.TextField(hint_text='Nombre del proyecto', on_submit=newProyect)
    def addTextField(e):
        print("Folder" in e.control.text)
        if listOfDirectories.controls.__contains__(textFieldFlet): return
        if "Folder" in e.control.text :
            textFieldFlet.hint_text = 'mkdir'
        elif "Flet" in e.control.text:
            textFieldFlet.hint_text = 'flet create'
        listOfDirectories.controls.append(textFieldFlet)
        listOfDirectories.update()

    def changeDefaultDirectory(e):
        if "VSCode" in e.control.hint_text:
            path = "CodePath"
        elif "Storage.json" in e.control.hint_text:
            path = "StoragePath"
        else:
            path = "ProyectsPath"
            global currentDir
            currentDir = e.control.value
            listOfDirectories.controls.clear()
            getDirectories()
        page.client_storage.set(path, e.control.value)
        page.dialog.open = False
        checkClientStorage()
        page.update()
        

    def openVLG(i):
        if page.dialog is open: return 
        title_ = "Change path"
        content_ = "Leave blank if you do not want to change the path"
        if i == 1:
            path = "VSCode"
        elif i == 2:
            content_ = "Set the Path of your proyects"
            title_ = "Set path"
            path = "Proyects"
        elif i == 3:
            content_ = "Set the Path of your VSCode"
            title_ = "Set path"
            path = "VSCode"
        elif i == 4:
            content_ = "Set the Path of your storage.json"
            title_ = "Set path"
            path = "Storage.json"
        else:
            path = "Proyects"
        vlg = ft.AlertDialog(
            modal = True,
            title= ft.Text(title_),
            content= ft.Text(content_),
            actions=[
                ft.TextField(hint_text=f"Path {path}", on_submit=changeDefaultDirectory)
            ],
            actions_alignment= ft.MainAxisAlignment.END
        )
        print(vlg)
        page.dialog = vlg
        vlg.open = True
        page.update()
        pass


    dropMenu = ft.Dropdown(
        on_change=changeProfile,
        options=[]
    )
    page.add(
        ft.Row([
                dropMenu,
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(on_click=addTextField, icon=ft.icons.ADD, text='Create Flet Proyect'),
                        ft.PopupMenuItem(text='Create new Folder', icon=ft.icons.FOLDER, on_click=addTextField),
                        ft.PopupMenuItem(text='Change proyects directory', icon=ft.icons.CHANGE_CIRCLE, on_click=lambda e : openVLG(0)),
                        ft.PopupMenuItem(text='Change VSCode directory', icon=ft.icons.CHANGE_CIRCLE, on_click=lambda e : openVLG(1)),
                    ]
                ),
                ]
            ),
            ft.TextButton(
                text= '...',
                on_click=parentDirectory
            ),
            listOfDirectories,
            mainColumn
    )
    def checkClientStorage():
        if not page.client_storage.contains_key("CodePath"):
            checkCodePath()
        if not page.client_storage.contains_key("StoragePath"):
            checkStoragePath()
        if not page.client_storage.contains_key("ProyectsStorage"):
            checkProyectsPath()
    checkClientStorage()
    currentDir = page.client_storage.get('ProyectsPath')
    perfJson()
    dropMenu.update()
    getDirectories()


ft.app(main, assets_dir="assets")
