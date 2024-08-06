# Inference

This repository contains code for performing inference with a pretrained model. The code is divided into two main parts: one for local testing and another for deploying the script in production.

## Project Structure

The code is organized into the following folders:

- **`code/`**: The main code directory containing all necessary scripts for both local and production deployment.
  - **`local/`**: Contains the same structure as the parent folder, specifically for testing locally.
  - **`docker/`**: Contains the `Dockerfile` needed to build a Docker image. This image includes a configurable startup timeout. For more information on how to customize the Dockerfile, refer to the [SageMaker PyTorch user-defined  repo](https://github.com/jeromeCondere/sagemaker_pytorch_user_defined).

## How to Run the Inference

Follow these steps to run the inference in a production environment:

###  Build and Push the Docker Image
First, build the Docker image using the `Dockerfile` located in the `docker/` folder. After building the image, push it to Amazon ECR (Elastic Container Registry).

###  Configure the `deploy.py` Script
In the `deploy.py` script, replace the `ecr_image` placeholder with your ECR image URI:  

```
huggingface_model = HuggingFaceModel(
    model_data=s3_model_path,
    source_dir=s3_code_path,
    entry_point='inference.py',
    role=role,
    transformers_version="4.26.0",
    pytorch_version="1.13.1", 
    py_version="py39",
    image_uri=ecr_image,
    sagemaker_session=sagemaker_session,
    env=env
)
```
  
 Also change the `config_inference.json` with the right values

###  Prepare the Model and Code Archives

Run the create_tar.sh script to create the necessary .tar archives for the model and code. Then, execute deploy.py to deploy the model.

###  Test Inference

For testing the inference, use the invoke_endpoint.py script. This script uploads the .tar archives to S3 before deploying the model.   

```
def predict_fn(input_data, model_and_tokenizer, context=None):
	# Perform prediction
	model, tokenizer = model_and_tokenizer
	print('Input data is ', str(input_data))
	print('Converting to tensor ')
	input_ids = tokenizer.apply_chat_template(input_data, truncation=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
	outputs = model.generate(
		input_ids=input_ids,
		max_new_tokens=25,
		temperature=0.5,
		top_k=50,
		top_p=0.95
	)
	prediction = {'response': tokenizer.batch_decode(outputs)[0]}
	return prediction
```
