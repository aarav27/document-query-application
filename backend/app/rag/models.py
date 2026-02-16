from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline
import torch

PHI_3_MINI = "microsoft/Phi-3-mini-4k-instruct"
FLAN_T5_MODEL = "google/flan-t5-small" 

def get_flan_llm():
    model_name: str = FLAN_T5_MODEL
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        
        dtype=torch.float32,
        device_map="auto"
    )
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,
        temperature=0.2
    )
    return pipe