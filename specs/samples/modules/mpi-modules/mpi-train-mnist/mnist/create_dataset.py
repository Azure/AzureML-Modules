import hashlib
import argparse
import sys
from pathlib import Path
from azureml.core import Workspace, Dataset

RELATIVE_DST_DIR = 'sample_images'
DEFAULT_DATASET_NAME = 'mnist_samples'


def register_dataset_by_path(ws: Workspace, dataset_name, path):
    if not path.is_dir():
        raise ValueError(f"Dataset must be a folder.")
    # Upload path to datastore
    m = hashlib.sha256()
    m.update(str(path).encode())
    ds_path = m.hexdigest()

    datastore = ws.get_default_datastore()
    path_on_datastore = folder_on_datastore = f'/data/{ds_path}'
    datastore.upload(str(path), target_path=folder_on_datastore)

    # Create a FileDataset
    datastore_paths = [(datastore, path_on_datastore + '/**')]
    dataset = Dataset.File.from_files(datastore_paths)
    print(f"Registering dataset for path {path}")
    dataset.register(ws, name=dataset_name, create_new_version=True)
    print("Dataset registered", dataset)
    return Dataset.get_by_name(ws, name=dataset_name)


def parse_workspace(sys_args):
    parser = argparse.ArgumentParser()
    for arg_key in ['--resource-group', '--subscription-id', '--workspace-name']:
        parser.add_argument(arg_key)
    args, _ = parser.parse_known_args(sys_args)
    ws = Workspace.get(
        name=args.workspace_name, resource_group=args.resource_group, subscription_id=args.subscription_id,
    ) if args.workspace_name else Workspace.from_config()
    return ws


if __name__ == '__main__':
    default_dir = Path(__file__).parent / RELATIVE_DST_DIR
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name', default=DEFAULT_DATASET_NAME)
    parser.add_argument('--local-path', default=default_dir)
    args, _ = parser.parse_known_args()
    ws = parse_workspace(sys.argv)
    register_dataset_by_path(ws, args.dataset_name, args.local_path)
