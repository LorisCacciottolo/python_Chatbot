from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_path = "./gpt2-finetuned"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

prompt = "The French president's name is"

input_ids = tokenizer.encode(prompt, return_tensors='pt')

output = model.generate(input_ids, max_length=100, num_return_sequences=1)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Text: ", generated_text)
