import app_engine
import dependencies_builder
import constants


def start_analysis(files, tools, progress, parent):
    app_engine.init()
    progress = 10
    #parent.update_idletasks()
    #pb_update_interval = 100/len(files)
    for file in files:
        filename = str(file).split('/')[-1]
        path = str(file).replace('/' + filename, '')
        if constants.DEFAULT_DIRECTORY != path:
            constants.DEFAULT_DIRECTORY = path
            dependencies_builder.create_output_dir(constants.DEFAULT_OUTPUT)
        results = app_engine.exec_start_gui(filename, get_tools_selected(tools))
        code = '200'
        #progress = progress + pb_update_interval
        #parent.update_idletasks()
    return results, code
    #progress = 100
    #parent.update_idletasks()


def get_tools_selected(tools):
    temp = []
    for i in range(0, len(tools)):
        if tools[i].get():
            temp.append(constants.TOOLS_PROPERTIES[i])
    return temp

