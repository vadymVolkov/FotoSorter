import subprocess
import os
import shutil
import filetype
import exiftool
FINAL_DIR = 'D:/Vadym/Pictures/Sorted 2/'


def get_exif(path):
    files = [path]
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)
    data = metadata[0]
    file_type = get_file_type(path)
    date = 'other'
    #for a in data:
        #print(str(a) + ' - ' + str(data[a]))
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
        try:
            date = format_date(data['File:FileCreateDate'])
            return date
        except Exception as e:
            print(e)
    else:
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
        try:
            date = format_date(data['File:FileCreateDate'])
            return date
        except Exception as e:
            print(e)
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
    if file == "Thumbs.db":
        shutil.copy2(from_path, to_path + file)
    elif check_if_exist_file(file, to_path):
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
        file_date = "unknown date"
        new_path = path + file
        is_file = is_folder_or_file(new_path)
        if is_file:
            file_type = get_file_type(new_path)
            if file_type == 'image':
                try:
                    file_date = get_exif(new_path)
                except Exception as e:
                    add_log("error image")
                    add_log(new_path)
                create_dir(file_date)
                create_dir(file_date+"/image")
                copy_file(file, new_path, FINAL_DIR + file_date + "/image/")
            elif file_type == "video":
                try:
                    file_date = get_exif(new_path)
                except Exception as e:
                    add_log("error video")
                    add_log(new_path)
                create_dir(file_date)
                create_dir(file_date + "/video")
                copy_file(file, new_path, FINAL_DIR + file_date + "/video/")
            else:
                try:
                    file_date = get_exif(new_path)
                except Exception as e:
                    add_log("error video")
                    add_log(new_path)
                create_dir(file_date)
                create_dir(file_date + "/another_format")
                copy_file(file, new_path, FINAL_DIR + file_date +  "/another_format/")
        else:
            scan(new_path + '/')

unknown = "D:/Vadym/Pictures/another_format 2/"
test_folder = 'D:/Vadym/Pictures/test/'
all = 'D:/Vadym/Pictures/all/'
unsorted = 'D:/Vadym/Pictures/unknown rename/'
#scan("E:/Photo/")
#scan(test_folder)
#scan(unknown)
#a = get_exif("D:/Vadym/Pictures/unknown date/image/dub.jpg")
#print(a)
#scan(all)
scan(unknown)
