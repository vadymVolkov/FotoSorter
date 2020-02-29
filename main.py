from PIL import Image, ExifTags
import subprocess
import filetype
import os
import shutil

FINAL_DIR = './final/'


def get_date(path):
    exe = 'exiftool'
    process = subprocess.Popen([exe, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    dict = {}
    for output in process.stdout:
        data = output.strip().split(":")
        if len(data) > 4:
            dict[data[0].strip()] = data[1] + '-' + data[2] + "-" + data[3] + ":" + data[4]
    date = dict["File Modification Date/Time"].strip().split(" ")[0]
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    final = year + '.' + month + '.' + day
    return final


def get_file_type(path):
    kind = filetype.guess(path)
    if kind is None:
        return 'unknown'
    else:
        file_type_name = kind.mime.split('/')[0]
        return file_type_name


def is_folder_or_file(path):
    answer = os.path.isfile(path)
    return answer


def create_dir(folder_name):
    path = FINAL_DIR + folder_name
    try:
        os.mkdir(path)
        return True
    except FileExistsError:
        return False


def check_if_exist_file(file1, path):
    file_list = os.listdir(path)
    result = True
    if len(file_list) > 0:
        for file2 in file_list:
            if file1 == file2:
                result = False
    return result


def copy_file(file, from_path, to_path):
    if check_if_exist_file(file, to_path):
        shutil.copy2(from_path, to_path + file)
    else:
        new_name = "dub_" + file
        copy_file(new_name, from_path, to_path)


def scan(path):
    file_list = os.listdir(path)
    count = 1
    for file in file_list:
        print(count)
        print(file)
        new_path = path + file
        is_file = is_folder_or_file(new_path)
        if is_file:
            file_type = get_file_type(new_path)
            if file_type == 'image' or file_type == "video":
                try:
                    file_date = get_date(new_path)
                except UnicodeDecodeError:
                    print(new_path)
                    return

                create_dir(file_date)
                copy_file(file, new_path, FINAL_DIR + file_date + "/")
        else:
            scan(new_path + '/')
        count = count + 1

scan("/Volumes/HDD/Photo/test1/")
