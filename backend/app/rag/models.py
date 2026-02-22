from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline
import torch

PHI_3_MINI = "microsoft/Phi-3-mini-4k-instruct"
FLAN_T5_MODEL = "google/flan-t5-large" 
QWEN2 = "Qwen/Qwen2-1.5B-Instruct"

_llm_pipeline = None

def get_llm(model_str: str = QWEN2):
    global _llm_pipeline
    if _llm_pipeline is None:
        tokenizer = AutoTokenizer.from_pretrained(model_str)
        model = AutoModelForCausalLM.from_pretrained(
            model_str,
            dtype=torch.float16,
            device_map="auto"
        )
        _llm_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=300,
            temperature=0.2,
            do_sample=True,
            return_full_text=False
        )
    return _llm_pipeline