from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
import torch


model_name = "distilgpt2"
model = GPT2LMHeadModel.from_pretrained(model_name, cache_dir="./cache/")
tokenizer = GPT2Tokenizer.from_pretrained(model_name, cache_dir="./cache/")


train_path = './train/données.txt'
test_path = './train/test.txt'

train_dataset = TextDataset(
  tokenizer=tokenizer,
  file_path=train_path,
  block_size=128)

test_dataset = TextDataset(
  tokenizer=tokenizer,
  file_path=test_path,
  block_size=128)


data_collator = DataCollatorForLanguageModeling(
  tokenizer=tokenizer, mlm=False)



training_args = TrainingArguments(
  output_dir="./gpt2-finetuned",
  overwrite_output_dir=True,
  num_train_epochs=3,
  per_device_train_batch_size=4,
  per_device_eval_batch_size=4,
  eval_steps=400,
  save_steps=800,
  warmup_steps=500,
  prediction_loss_only=True
)


print("traning")
trainer = Trainer(
  model=model,
  args=training_args,
  data_collator=data_collator,
  train_dataset=train_dataset,
  eval_dataset=test_dataset)

trainer.train()
print("finish")

trainer.save_model("./gpt2-finetuned")

model.save_pretrained('./gpt2-finetuned')
tokenizer.save_pretrained('./gpt2-finetuned')


model = GPT2LMHeadModel.from_pretrained("./gpt2-finetuned")
prompt = "Qu'incarne la fidélité dans le septennat annoncé ?"
inputs = tokenizer.encode(prompt, return_tensors="pt")
outputs = model.generate(inputs, max_length=50, num_return_sequences=5)
print("Generated Text: ", tokenizer.decode(outputs[0], skip_special_tokens=True))
