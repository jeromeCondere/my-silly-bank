
import subprocess
subprocess.run(["pip", "uninstall", "-y",  "apex"])


import os
import torch
from datasets import load_dataset, Dataset, DatasetDict
import json
import transformers
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoTokenizer,
    TrainingArguments,
    pipeline,
)
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from trl import SFTTrainer
from huggingface_hub import HfApi, HfFolder
# import wandb
import argparse
import peft
import datasets
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per_device_train_batch_size" , type=int, default=10, help='size of train batch')
    parser.add_argument("--per_device_eval_batch_size", type=int, default=10, help='size of eval batch')
    parser.add_argument("--gradient_accumulation_steps", type=int, default=10, help='gradient accumulation step')
    parser.add_argument("--save_steps", type=int, default=50, help='save steps')
    parser.add_argument("--eval_steps", type=int, default=175, help='eval steps')
    parser.add_argument("--max_steps", type=int, default=10, help='max steps (override epochs)')
    parser.add_argument("--epochs", type=int, default=5, help='epoch')
    parser.add_argument("--wandb_token", type=str)
    parser.add_argument("--hf_token", type=str)
    parser.add_argument("--output_dir", type=str, default=os.environ.get("SM_MODEL_DIR"), help="Directory to save the model")
    return parser.parse_args()



def main():
    # Parse command-line arguments
    args = parse_args()
    base_model = 'meta-llama/Meta-Llama-3-8B-Instruct'
    new_model = "Meta-Llama-3-8B-for-bank"
    print('Running training job')
    print('transformers version: ', transformers.__version__)
    print('peft version: ', peft.__version__)
    print('torch version: ', torch.__version__)
    print('datasets version: ', datasets.__version__)

    os.environ['BNB_CUDA_VERSION'] = '120'
    new_path = '/opt/conda/lib'
    
    # Get the current LD_LIBRARY_PATH
    current_path = os.environ.get('LD_LIBRARY_PATH', '')
    
    # Update LD_LIBRARY_PATH
    os.environ['LD_LIBRARY_PATH'] = f"{new_path}:{current_path}"

    os.environ["WANDB_NOTEBOOK_NAME"] = 'bank'

    token = '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'

    # wandb_token = ''
    # wandb.login(
    #     key = wandb_token
    # )
    # set api for login and save token
    api = HfApi(
        endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
        token=token, # Token is not persisted on the machine.
    )
    
    # os.environ["WANDB_API_KEY"] = wandb_token
    # os.environ["WANDB_NOTEBOOK_NAME"] = 'bank'
    os.environ["SM_MODEL_DIR"] = 'yokata'
    output_dir = os.environ.get("SM_MODEL_DIR")

    # tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=True, token=token)
    # tokenizer.pad_token = tokenizer.eos_token
    # shuffled_dataset = load_dataset('jeromecondere/bank-chat')
    # Quantization configuration for Lora
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    # For lora we take r=8, that gives us around 1.34M trainable parameters
    # LoRA configuration
    peft_config = LoraConfig(
        r=16,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=['up_proj', 'down_proj', 'gate_proj', 'k_proj', 'q_proj', 'v_proj', 'o_proj']
    )
    # model_8bit = AutoModelForCausalLM.from_pretrained(
    #    "facebook/opt-350m", 
    #    quantization_config=bnb_config,
    #    device_map={"": 0}
    # )

    print('yokata')
    time.sleep(7200)

    print('yokata')
    # print(model_8bit)
    # # Load base moodel
    # model = AutoModelForCausalLM.from_pretrained(
    #     base_model,
    #     quantization_config=bnb_config,
    #     device_map={"": 0},
    #     token=token
    # )
    # print(model)
    # # Cast the layernorm in fp32, make output embedding layer require grads, add the upcasting of the lmhead to fp32
    # model = prepare_model_for_kbit_training(model)
    # print('\n\nmodel after casting the layer norm to fp32')
    # print(model)


    # # Set training arguments
    # training_arguments = TrainingArguments(
    #         output_dir=output_dir,
    #         num_train_epochs=args.epochs,
    #         per_device_train_batch_size=args.per_device_train_batch_size,
    #         per_device_eval_batch_size = args.per_device_eval_batch_size,
    #         gradient_accumulation_steps=args.gradient_accumulation_steps,
    #         evaluation_strategy="steps",
    #         eval_steps=args.eval_steps,
    #         save_steps = args.save_steps,
    #         logging_steps=1,
    #         optim="paged_adamw_8bit",
    #         learning_rate=2e-4,
    #         lr_scheduler_type="linear",
    #         # warmup_steps=10,
    #         max_steps = args.max_steps,
    #         # report_to="wandb"
    # )
    
    # # Set supervised fine-tuning parameters
    # trainer = SFTTrainer(
    #     model=model,
    #     train_dataset=shuffled_dataset['train'],
    #     eval_dataset=shuffled_dataset['test'],
    #     peft_config=peft_config,
    #     dataset_text_field="messages",
    #     max_seq_length=512,
    #     tokenizer=tokenizer,
    #     args=training_arguments,
    # )
    # # Train the model
    # trainer.train()

    # # Save the model
    # trainer.save_model(output_dir)

if __name__ == "__main__":
    main()
