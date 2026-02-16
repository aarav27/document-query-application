from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

PHI_3_MINI = "microsoft/Phi-3-mini-4k-instruct"

def get_phi_llm(model_name: str = PHI_3_MINI):

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="auto"
    )

    pipl = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,
        temperature=0.2
    )

    return pipl