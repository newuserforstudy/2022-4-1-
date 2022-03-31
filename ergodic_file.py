import os


def ergodic_file(dir_path):
    all_file = os.walk(dir_path)
    file_list = []
    for i,file in enumerate(all_file):

        for sub_file in file[-1]:
            file_path = file[0]+"/"+sub_file
            file_list.append(file_path)

    return file_list


if __name__ == '__main__':
    print(ergodic_file("./test"))
