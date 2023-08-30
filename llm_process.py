import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed
import torch

#llama2を実行
def llama2(question):
    print(f'質問文：{question}')
    model = r"C:\Users\m_mori\Desktop\llm_chat\Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model)
    generator = pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float32,
        tokenizer=tokenizer
    )
    
    text = generator(
        question,
        max_length=200,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        top_k=10,
        num_return_sequences=1,
        
    )
    for t in text:
        answer = t['generated_text']
    return answer


#line_large_lmを実行
def line_llm(question):
    print(f'質問文：{question}')
    model = AutoModelForCausalLM.from_pretrained("line-corporation/japanese-large-lm-3.6b")
    tokenizer = AutoTokenizer.from_pretrained("line-corporation/japanese-large-lm-3.6b", use_fast=False)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    set_seed(101)
    
    text = generator(
        question,
        max_length=200,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        num_return_sequences=1,
    )
    for t in text:
        answer = t['generated_text']
    return answer


#toudai_llmを実行
def toudai_llm(question):
    print(f'質問文：{question}')
    tokenizer = AutoTokenizer.from_pretrained("matsuo-lab/weblab-10b-instruction-sft")
    model = AutoModelForCausalLM.from_pretrained("matsuo-lab/weblab-10b-instruction-sft", torch_dtype=torch.float16)

    if torch.cuda.is_available():
        model = model.to("cuda")
        
    text = f'{question} 応答：'
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
    
    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.95
        )

    answer = tokenizer.decode(output_ids.tolist()[0]) 
    return answer



