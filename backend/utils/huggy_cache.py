from transformers import AutoTokenizer, AutoModelForCausalLM

print("Downloading and caching GPT-2… this might take a minute.")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
print("✅ GPT-2 model and tokenizer cached successfully!")
