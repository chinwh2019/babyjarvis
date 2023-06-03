# %%
import torch 
import transformers 
from transformers import AutoTokenizer, AutoModelForCausalLM

# %%
print("torch version: ", torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))    
# %%
tokenizer = AutoTokenizer.from_pretrained("mosaicml/mpt-7b-chat")

model = AutoModelForCausalLM.from_pretrained(
    "mosaicml/mpt-7b-chat",
    torch_dtype=torch.float16,
    trust_remote_code=True
    ).to("cuda:0")
# %%
tokenizer = AutoTokenizer.from_pretrained("mosaicml/mpt-7b-instruct")

model = AutoModelForCausalLM.from_pretrained(
    "mosaicml/mpt-7b-instruct",
    torch_dtype=torch.float16,
    trust_remote_code=True
    ).to("cuda:0")
# %%
prompt = "<human>: Who is Alan Turing?\n<bot>:"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
input_length = inputs.input_ids.shape[1]

outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    do_sample=True,
    temperature=0.7,
    top_p=0.7, 
    top_k=50,
    return_dict_in_generate=True
    )

token = outputs.sequences[0, input_length:]
output_str = tokenizer.decode(token)

print("output: ", output_str)
# %%
prompt = "<human>: Describe 10 main points about Malaysia?\n<bot>:"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
input_length = inputs.input_ids.shape[1]

outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    do_sample=True,
    temperature=0.7,
    top_p=0.7, 
    top_k=50,
    return_dict_in_generate=True
    )

token = outputs.sequences[0, input_length:]
output_str = tokenizer.decode(token)

print("output: ", output_str)
# %%
