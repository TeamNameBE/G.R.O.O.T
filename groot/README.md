# Groot (AI)

## Installation
```
python3 -m venv ve
source ve/bin/activate
pip install -r requirements.txt
```

## training the AI
```
python3 train.py <train_size>
```

### Training with GPU
The packages in requirements.txt are the ones compatible with CUDA 10.1 and CuDNN 7.6

For manjaro :
```
yay cudnn7-cuda10.1
```