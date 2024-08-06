FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-training:1.13.1-transformers4.26.0-gpu-py39-cu117-ubuntu20.04

RUN pip install --upgrade torch==2.4.1
RUN pip install --upgrade torchvision==0.19

RUN pip install --upgrade transformers==4.45.2

RUN pip install --upgrade datasets==3.0.1
RUN pip install --upgrade trl==0.19
RUN pip install --upgrade bitsandbytes==0.43.3


RUN pip uninstall -y apex


