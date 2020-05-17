from torchvision.datasets import MNIST
from pathlib import Path
import argparse
import shutil
import random


RELATIVE_DST_DIR = 'sample_images'


def generate_mnist_test_samples(dst_dir, count=100, dataset_dir='./mnist'):
    dst_dir = Path(dst_dir)
    dataset = MNIST(dataset_dir, train=False, download=True)
    sample_index = random.sample(range(len(dataset)), count)
    dst_dir.mkdir(exist_ok=True)
    for i in sample_index:
        img, idx = dataset[i]
        path = dst_dir / f'{i}_{MNIST.classes[idx]}.png'
        img.save(path)


if __name__ == '__main__':
    default_dst_dir = Path(__file__).parent / RELATIVE_DST_DIR
    parser = argparse.ArgumentParser()
    parser.add_argument('--dst', default=default_dst_dir)
    parser.add_argument('--count', type=int, default=100)
    args, _ = parser.parse_known_args()
    dst_dir = Path(args.dst)
    if dst_dir.is_dir():
        shutil.rmtree(dst_dir)
    generate_mnist_test_samples(dst_dir, count=args.count)
