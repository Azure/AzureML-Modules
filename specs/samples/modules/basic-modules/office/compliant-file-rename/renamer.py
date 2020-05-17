import os
import sys
from shutil import copyfile
from scrubber import compliant_handle

@compliant_handle()
def main():
    script, source, target_dir, target_file_name, dummy = sys.argv

    if (not os.path.exists(source)):
        print('SystemLog: Source does not exist')
        sys.exit(-1)

    if os.path.isfile(source):
        print('SystemLog: copying file', source)
        source_path = source
    else:
        files = os.listdir(source)
        if len(files) != 1:
            print('SystemLog: Expected exactly 1 file in input blob. Found', len(files))
            sys.exit(-2)
        source_path = os.path.join(source, files[0])
        print('SystemLog: copying file from dir', source_path)

    target_path = os.path.join(target_dir, target_file_name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    print('SystemLog: source path', source_path)
    print('SystemLog: target path', target_path)
    copyfile(source_path, target_path)
    sys.exit(0)

if __name__ == '__main__':
    main()

    

