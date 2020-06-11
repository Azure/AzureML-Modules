# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import torch
import pandas as pd
from uuid import uuid4
from pathlib import Path
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from PIL import Image
from torchvision import transforms
from torchvision.datasets import MNIST
import torch.nn as nn
import os

transform = transforms.Compose([
               transforms.ToTensor(),
               transforms.Normalize((0.1307,), (0.3081,))
            ])


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-input', default='model_input')
    parser.add_argument('--data-output', default='output')
    # Here we must use parse_known_args to make sure the additional args for driver code will be ignored.
    args, _ = parser.parse_known_args()
    global model, output_dir
    map_location = 'cpu' if not torch.cuda.is_available() else None
    model = torch.load(os.path.join(args.model_input, 'model.pt'), map_location=map_location)
    output_dir = args.data_output
    os.makedirs(output_dir, exist_ok=True)


def run(files):
    results = []
    nthreads = min(2*cpu_count(), len(files))

    print(f"Ready to process {len(files)} images.")
    with ThreadPool(nthreads) as pool:
        imgs = pool.map(Image.open, files)

    for f, img in zip(files, imgs):
        img = Image.open(f)
        tensor = transform(img).unsqueeze(0)
        if torch.cuda.is_available():
            tensor = tensor.cuda()

        with torch.no_grad():
            output = model(tensor)
            softmax = nn.Softmax(dim=1)
            pred_probs = softmax(output).cpu().numpy()[0]
            index = torch.argmax(output, 1)[0].cpu().item()
            result = {'Filename': Path(f).name, 'Class': MNIST.classes[index]}
            for c, prob in zip(MNIST.classes, pred_probs):
                result[f"Prob of {c}"] = prob
        results.append(result)
    columns = sorted(list(results[0].keys()))
    df = pd.DataFrame(results, columns=columns)
    print("Result:")
    print(df)
    output_file = os.path.join(output_dir, f"{uuid4().hex}.parquet")
    df.to_parquet(output_file, index=False)
    return results


# This is only for local debug, in AzureML this code will never be reached.
if __name__ == '__main__':
    init()
    local_input = 'mnist_sample_data'
    files = [os.path.join(local_input, f) for f in os.listdir(local_input)]
    results = run(files)
    print(results)
