# by Calhiari

import os
import shutil

# asks if the user wants to append an arbitrary prefix
user_in = input("Do you want to append a prefix to evey picture? (Yes/No): ")
if user_in in ["y", "Y", "yes", "Yes", "YES"]:
    user_append = True
    prefix_list = input("Enter the prefixes separated by space and finish with 'enter':\n>>> ").split(" ")
    if prefix_list[0] == "":
        print("You've entered no prefix after saying you want them!\n Terminating the program...\n")
        exit()
elif user_in in ["n", "N", "no", "No", "NO"]:
    user_append = False
else: 
    print("You've entered an invalid option!\nTerminating program...\n")
    exit()

# defines some system variables
device_name = os.popen("adb shell getprop ro.product.vendor.name").read()[:-1]
pwd = os.getcwd()
pwd = pwd + "/" + device_name
sep = os.sep

# checks wether the folder for this device already exists
if not os.path.exists(pwd): 
    os.mkdir(pwd)

# append prefixes
def append_before(path_to_folder, app_name, file_name):
    os.rename(path_to_folder + sep + file_name, path_to_folder + sep + app_name + "_" + file_name)
    file_name = app_name + "_" + file_name

    # append the user defined prefix
    if user_append:
        path_to_file = path_to_folder + sep + app_name + "_" + file_name
        old_file_name = file_name
        for i in range(len(prefix_list) - 1, -1, -1):
            file_name = prefix_list[i] + "_" + file_name
        
        new_path = sep.join(path_to_file.split(sep)[:-1])

        os.rename(new_path + sep + old_file_name, new_path + sep + file_name)

def move_from_temp(path_to_folder, destination):
    for file in os.listdir(path_to_folder):
        if os.path.isfile(path_to_folder + sep + file):
            os.rename(path_to_folder + sep + file, destination + sep + file)
            

# fetch pictures
file_paths = [
    "/sdcard/DCIM/Camera/",
    "/sdcard/Pictures/Discord/",
    "/sdcard/Pictures/Facebook/",
    "/sdcard/Pictures/Instagram/",
    "/sdcard/Pictures/Reddit/",
    "/sdcard/Pictures/Telegram/",
    "/sdcard/Pictures/Twitter/",
    "/sdcard/Pictures/", # this one is for Signal
    "/sdcard/Snapchat/",
    "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\ Images/Sent/"
]


# the core of the application
temp_folder = pwd + "/" + "temp"
for path in file_paths: 
    os.mkdir(temp_folder)
    app_name = path.split(sep)
    temp_wd = pwd + sep + app_name[-2] # the -2 position stores the actual name (last but one)
    # os.system("adb pull -a " + path + ". " + temp_folder)
    if "error" in os.popen("adb pull -a " + path + ". " + temp_folder).read():
        shutil.rmtree(temp_folder)
        continue
    new_app_name = ""

    # fixes the name if the file is from one of these 2 special cases
    if app_name[-2] == "Pictures": new_app_name = "Signal"
    elif app_name[-2] == "Sent": new_app_name = "Whatsapp"
    else: new_app_name = app_name[-2]
    if not os.path.exists(pwd + sep + new_app_name):
        os.mkdir(pwd + sep + new_app_name)

    for file in os.listdir(temp_folder):
        # if the specified path is not a file, do nothing
        if not os.path.isfile(temp_folder + sep + file):
            continue
        # delete trashed files
        if "trashed" in file: 
            os.remove(temp_folder + sep + file)
        else:
            append_before(temp_folder, new_app_name, file)

    move_from_temp(temp_folder, pwd + sep + new_app_name)

    shutil.rmtree(temp_folder)


# clean the generated folders mess
lil_dic = {
    "Pictures": "Signal",
    "Sent": "Whatsapp"
}
for old, correct in lil_dic.items():
    if not os.path.isdir(pwd + sep + old):
        continue
    os.mkdir(pwd + sep + correct)
    for file in os.listdir(pwd + sep + old):
        if file.endswith(".jpg"):
            shutil.move(pwd + sep + old + sep + file, pwd + sep + correct)
    shutil.rmtree(pwd + sep + old)