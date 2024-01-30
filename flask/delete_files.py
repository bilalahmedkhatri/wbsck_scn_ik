import os
import shutil

folder = str(os.curdir + "/uploads/")
print(folder)
# List all files in directory
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
            print('Deleted %s' % file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print('Deleteds %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
