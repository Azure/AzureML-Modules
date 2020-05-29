## A sample pipeline of MNIST Image Classification with MPI training and parallel score

### Overview
This sample include a pipeline that train an image classification model with MNIST data using MPI,
then use the trained model to predict the class of sample images in parallel.

### Data Preparation
First you need to prepare the data for scoring.
Run the following commands to generate sample images in local, then register them as a Dataset.
You could also prepare your own data for scoring.
```
python mnist/sample_image_generator.py --dst YOUR_SAMPLE_IMAGE_FOLDER --count SAMPLE_COUNT
python mnist/create_dataset.py --local-path YOUR_SAMPLE_IMAGE_FOLDER --dataset-name YOUR_DATASET_NAME --workspace-name YOUR_WORKSPACE_NAME --subscription-id YOUR_SUB_ID --resource-group YOUR_RESOURCE_GROUP
```


### Register Modules
Follow [the guide](https://msdata.visualstudio.com/AzureML/_git/ModuleDocs?path=%2Fdocs%2Fcli%2Fa-quick-go-through.md&_a=preview) to install AzureML CLI for module registration.
Register two modules with the commands:

```
az ml module register --spec-file train_mpi.yaml
az ml module register --spec-file score_parallel.yaml
```
* train_mpi.yaml: An mpi module training an image classification model with [horovod](https://github.com/horovod/horovod),
the code is from [this link](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/ml-frameworks/pytorch/training/distributed-pytorch-with-horovod/distributed-pytorch-with-horovod.ipynb);
* score_parallel.yaml: A parallel module predict the classes of sample images,
then store the results as DataFrames in multiple parquet files. 


### Run pipeline in Designer
Create an experiment like this:

 ![An example pipeline](_assets/README/pipeline.JPG)
