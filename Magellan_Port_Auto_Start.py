import os
import time
import subprocess
from pywinauto import Application

# get the path of the directory containing the python script
dir_path= os.path.dirname(os.path.realpath(__file__))

# construct the path to the text file relative to the script directory
file_path= os.path.join(dir_path,"Locations.txt")

# open the file and read its contents
with open(file_path,"r") as file:
    file_contents= file.readlines()
target= file_contents[0].strip()
start_in= file_contents[1].strip()
cfg_dir= file_contents[2].strip()

cfg_files=[f for f in os.listdir(cfg_dir) if f.endswith('.cfg')]

for cfg_file in cfg_files:
    cfg_path= os.path.join(cfg_dir,cfg_file)
    command= '{} Scripts\\tcp-relay-gui.py{}'.format(target,cfg_path)
    process= subprocess.Popen(command,cwd=start_in)
    # wait for software to open
    time.sleep(2)
    try:
        app= Application(backend='via').connect(path=target,timeout=2)
        main_window= app.top_window()
        main_window.print_control_identifiers()
        file_menu= main_window.child_window(title='File',control_type='MenuItem')
        file_menu.click_input()
        open_option= file_menu.child_window(title='Open...',control_type='MenuItem')
        open_option.click_input()
        main_window1=app.top_window()
        file_name_edit= main_window1.child_window(title='File name:',control_type='Edit')
        file_name_edit.set_text(cfg_path)
        open_button= main_window1.child_window(title='Open',control_type='Button',found_index=2)
        open_button.click_input()
        relay_button= main_window.child_window(title='start relay',control_type='Button')
        relay_button.click_input()
        close_but= main_window.child_window(title='Close',control_type='Button')
        close_but.click_input()
    finally:
        print('{} has been run..'.format(cfg_file))
