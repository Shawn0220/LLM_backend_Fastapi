FROM 

ADD . /root/llm-chat-backend

WORKDIR /root/llm-chat-backend

RUN pip install cryptography==39.0.2 && \
    pip install -r requirements.txt && \
    pip install sentence_transformers pymilvus

RUN unzip -o peft-0.5.0.zip && \
    cd peft && python setup.py install --user && cd ..

SHELL ["/bin/bash", "-c"]

VOLUME ["/root/llm-chat-backend/apps/chat"]

EXPOSE 8002

CMD python main.py
