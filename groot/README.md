# Groot (AI)
This folder contains all the informations and source code to train, te4st, and run a daemon beside the website and the redis database.

## Requirements installation
Simply run the following commands:
```
$ python3 -m venv ve
$ source ve/bin/activate
$ pip install -r requirements.txt
```

## training the AI
You'll first need to download the [dataset](https://www.kaggle.com/msheriey/104-flowers-garden-of-eden?select=jpeg-311x311) and extract it to the following path : `data/flowers/`. You'll then be able to train the AI by running the following command

```
$ python3 train.py <train_size>
```

### Training with GPU (NVIDIA)
Alternatively you can run the training on your GPU, using Cuda and CuDNN libraries.
The packages in requirements.txt are the ones compatible with CUDA 10.1 and CuDNN 7.6

Install Cuda10.1 and CuDNN7.5 from AUR:
```
$ yay cudnn7-cuda10.1
```