FROM tensorflow/tensorflow:latest

RUN pip install numpy

ENV TF_CPP_MIN_LOG_LEVEL=2
ENV CUDA_VISIBLE_DEVICES=

COPY evaluate /evaluate
COPY judger.py /evaluate/judger.py

WORKDIR /evaluate

CMD ["python", "judger.py"]