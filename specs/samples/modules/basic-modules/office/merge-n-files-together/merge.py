import shutil
import sys
from os import listdir
from os.path import isfile, join
import math
import os

input_folder = sys.argv[1]
output_folder = sys.argv[2]
merge_count = int(sys.argv[3])

print("SystemLog: Reading from input folder %s"%input_folder)
print("SystemLog: Reading from output folder %s"%output_folder)
print("SystemLog: Merging every %d file together"%merge_count)
sys.stdout.flush()

total_files_processed = 0
onlyfiles = [os.path.abspath(join(input_folder, f)) for f in listdir(input_folder) if isfile(join(input_folder, f))]
total_files = len(onlyfiles)
total_merges = int(math.ceil(total_files/merge_count))
print("SystemLog: Total files in input_folder %d and total expected merged ones %d"% (total_files, total_merges))
sys.stdout.flush()

# This line should be added since in AzureML, output folder is not created.
os.makedirs(output_folder, exist_ok=True)

for merge_idx in range(total_merges):
    merged_file = open(os.path.abspath(os.path.join(output_folder, str(merge_idx))), 'wb')
    files_to_be_merged = onlyfiles[merge_idx * merge_count: (merge_idx + 1) * merge_count]
    #print(files_to_be_merged)
    for file_to_be_merged in files_to_be_merged:
        shutil.copyfileobj(open(file_to_be_merged, 'rb'), merged_file)
        total_files_processed += 1
        if total_files_processed % 1000 == 0:
            print("SystemLog: Total files processed %d"%total_files_processed)
            sys.stdout.flush()
print("Total files processed are %d and merged to %d files"%(total_files_processed, total_merges))
sys.stdout.flush()