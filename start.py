import os
import shutil


def copy_file(file, from_path, to_path, new_name):
    shutil.copy2(from_path+file, to_path + new_name)


def begin(from_path, to_path):
    file_list = os.listdir(from_path)
    count = 1
    for file in file_list:
        extantion = os.path.splitext(from_path+file)
        new_name = str(count) + str(extantion[1])
        copy_file(file, from_path, to_path, new_name)
        count = count + 1


unknown = 'D:/Vadym/Pictures/unknown date/video/'
to_path = 'D:/Vadym/Pictures/unknown rename/video/'
begin(unknown, to_path)
