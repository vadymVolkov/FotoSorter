import subprocess
import os
import shutil
import filetype
import piexif
import exiftool
from image_match.goldberg import ImageSignature
gis = ImageSignature()

a = gis.generate_signature('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
b = gis.generate_signature('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
gis.normalized_distance(a, b)

FINAL_DIR = 'D:/Vadym/Pictures/Sorted/'


def get_exif(path):
    files = [path]
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)
    data = metadata[0]
    file_type = get_file_type(path)
    date = 'other'
    if file_type == 'image':
        try:
            date = format_date(data['EXIF:CreateDate'])
            return date
        except Exception as e:
            print(e)
        try:
            date = format_date(data['File:FileModifyDate'])
            return date
        except Exception as e:
            print(e)
        try:
            date = format_date(data['File:FileCreateDate'])
            return date
        except Exception as e:
            print(e)
    elif file_type == "video":
        try:
            date = format_date(data['QuickTime:CreateDate'])
            return date
        except Exception as e:
            print(e)
        try:
            date = format_date(data['File:FileModifyDate'])
            return date
        except Exception as e:
            print(e)
    #for a in data:
        #print(str(a) + ' - ' + str(data[a]))
    return date


def format_date(date):
    date = date.split(' ')[0].strip()
    date = date.split(":")
    year = date[0]
    month = date[1]
    day = date[2]
    date = year + "." + month + '.' + day
    return date


def get_date(path):
    exe = './exiftool.exe'
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


def get_date_new(path):
    exe = './exiftool.exe'
    process = subprocess.Popen([exe, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for output in process.stdout:
        data = output.strip().split(":")
        key = data[0].strip()
        if key == 'Create Date':
            year = data[1].strip()
            month = data[2].strip()
            day = data[3].split(' ')[0].strip()
            return year + "." + month + "." + day
    process2 = subprocess.Popen([exe, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for output in process2.stdout:
        data = output.strip().split(":")
        key = data[0].strip()
        if key == 'File Modification Date/Time':
            year = data[1].strip()
            month = data[2].strip()
            day = data[3].split(' ')[0].strip()
            return year + "." + month + "." + day
    return 'other'


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
    return result


def copy_file(file, from_path, to_path):
    if check_if_exist_file(file, to_path):
        shutil.copy2(from_path, to_path + file)
    else:
        new_name = "dub_" + file
        copy_file(new_name, from_path, to_path)


def add_log(text):
    log = open("log.txt", "a")
    try:
        log.write(text)
        log.write('\n')
    except Exception as e:
        log.write("encode error: " + str(e))
        log.write('\n')


def scan(path):
    file_list = os.listdir(path)
    for file in file_list:
        file_date = "unknown"
        new_path = path + file
        is_file = is_folder_or_file(new_path)
        if is_file:
            file_type = get_file_type(new_path)
            if file_type == 'image' or file_type == "video":
                try:
                    file_date = get_exif(new_path)
                except Exception as e:
                    add_log("error")
                    add_log(new_path)
                create_dir(file_date)
                copy_file(file, new_path, FINAL_DIR + file_date + "/")
            else:
                create_dir("another_format")
                copy_file(file, new_path, FINAL_DIR + "another_format/")
        else:
            scan(new_path + '/')

unknown = "D:/Vadym/Pictures/unknown/"
test_folder = 'D:/Vadym/Pictures/test/'
#scan("E:/Photo/")
#scan(test_folder)
#scan(unknown)
#a = get_exif("test5.MPG")
#print(a)
