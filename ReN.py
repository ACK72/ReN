import os
import sys

from unicodedata import normalize

def change_nfc_all_dir(dirname):
    filelist = os.listdir(dirname)
    for filename in filelist:
        filepath = os.path.join(dirname, filename)
        new_filepath = normalize('NFC', filepath)

        if filepath != new_filepath:
            if os.path.exists(new_filepath):
                # Dest name exist
                if os.path.isdir(new_filepath):
                    # Folder
                    index = filelist.index(filename)
                    new_index = filelist.index(normalize('NFC', filename))

                    if index > new_index:
                        # new_filepath already changed
                        change_nfc_all_dir(filepath)
                        file_copy_all_dir(filepath, new_filepath)
                    else:
                        # new_filepath not changed
                        file_copy_all_dir(filepath, new_filepath)
                else:
                    # File
                    os.remove(new_filepath)
                    os.rename(filepath, new_filepath)
            else:
                os.rename(filepath, new_filepath)
        else:
            if os.path.isdir(filepath):
                change_nfc_all_dir(filepath)


def file_copy_all_dir(dirname, new_dirname):
    if dirname == new_dirname:
        return

    filelist = os.listdir(dirname)
    for filename in filelist:
        filepath = os.path.join(dirname, filename)
        new_filepath = os.path.join(new_dirname, filename)

        if os.path.exists(new_filepath):
            # Same name exist
            if os.path.isdir(new_filepath):
                # Folder
                file_copy_all_dir(filepath, new_filepath)
                os.remove(filepath)
            else:
                # File
                filetime = os.path.getmtime(filepath)
                new_filetime = os.path.getmtime(new_filepath)

                if filetime > new_filetime:
                    os.remove(new_filepath)
                    os.rename(filepath, new_filepath)
                else:
                    os.remove(filepath)
        else:
            os.rename(filepath, new_filepath)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        change_nfc_all_dir(os.getcwd())
    else:
        for arg in sys.argv[1:]:
            change_nfc_all_dir(arg)