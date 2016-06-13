from settings import TMP_DIR, DAYS_TO_PURGE
import os, datetime, shutil


def remove_old_files():
    for dir_name in os.listdir(TMP_DIR):
        file_or_dir_path = '%s%s' %(TMP_DIR, dir_name)
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_or_dir_path))
        current_time = datetime.datetime.now()

        diff = current_time - modified_time

        if diff.days >= DAYS_TO_PURGE:
            if os.path.isdir(file_or_dir_path):
                shutil.rmtree(file_or_dir_path)
            else:
                os.remove(file_or_dir_path)


if __name__ == '__main__':
    remove_old_files()
