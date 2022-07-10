import codecs
import os
import errno
import shutil

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def clear_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def drop_files(directory, lib, problems, names):
    print("Result recording started")
    lib_file = codecs.open(directory + "\\library.xml", "w+", "UTF-8")
    lib_file.write(lib)
    lib_file.close()
    q_i = 0
    new_dir = directory + "\\problem"
    make_sure_path_exists(new_dir)
    clear_dir(new_dir)
    for problem in problems:
        problem_file = codecs.open(new_dir + "\\" + names[q_i] + ".xml", "w+", "UTF-8")
        problem_file.write(problem)
        problem_file.close()
        q_i += 1
    new_dir = directory + "\\policies"
    make_sure_path_exists(new_dir)
    clear_dir(new_dir)
    assets_file = codecs.open(new_dir + "\\assets.json", "w+", "UTF-8")
    assets_file.write("{}")
    assets_file.close()
    print("Result recording completed")

