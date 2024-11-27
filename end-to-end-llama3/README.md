# Chatbot using AWS SageMaker and Meta-Llama

This is a chatbot project designed for bank-related interactions like withdrawing money, buying stocks, and managing user accounts. We're using **SageMaker** to train and deploy the model, and we're starting with the **Meta-Llama 3-8B-Instruct** model as a base.  
The project also includes a **Docker** setup for running a MariaDB container to store all the bank-related data.

The project is split into a few different stages, each handled in separate folders under the `sagemaker` directory. Here's an overview of how everything fits together.


### Just a Note:
This implementation is **not** the most optimal or best practice for building a production-grade chatbot. The goal here is to demonstrate the various steps involved in creating a working system around the model. It shows the required stages of data processing, model training, model deployment, and integration with a backend database. 


## Project Structure

```plaintext
.
├── sagemaker/
│   ├── processing/
│   ├── training/
│   └── inference/
├── docker/
├── client.py
├── chat.py
├── stocks.py
├── transaction.py
├── user_account.py
└── requirements.txt
```

### 1. Processing

The processing step is about generating example of conversations that one would have with a chatbot from  a bank.  
Once the data is ready, it gets saved to in Amazon S3. Later we push that data to the hub.  

### 2. Training

The training folder is where the magic happens. We're fine-tuning the meta-llama/Meta-Llama-3-8B-Instruct model from Hugging Face using qLoRA .

- Base Model: **meta-llama/Meta-Llama-3-8B-Instruct**
- Fine-Tuning: We use qLoRA to adjust the model to handle banking specific tasks.


### 3. Inference

The inference folder is where we deploy the model for real-time use. After training, we push the model to AWS SageMaker, which allows us to create an endpoint for the chatbot. This is where the chatbot "lives" and where you can interact with it—whether it's for checking balances, buying stocks, or processing transactions.  

### 4. Docker Setup for MariaDB

The docker folder has everything needed to set up a MariaDB container. This database stores important information, like:

- User Accounts: User balances, details, and account info.
- Transactions: A history of all bank transactions (withdrawals, deposits, etc.).
- Stocks: Information on stock purchases and portfolio details.

The table definitions are stored in the init.sql file inside the docker folder, which contains the SQL schema for the tables.

### 5. Chatbot Client

The `client.py` file is the main way users interact with the chatbot.

The chatbot client sends requests to the backend, and the chat.py script processes the requests. It formats everything and sends it to the model for inference (the model responds with the appropriate actions or data).  
Once the model has been deployed and mariadb container has been set up, just do a `python3 client.py --mode prod` to use it