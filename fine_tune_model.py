import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
import numpy as np
import joblib  # Import joblib for saving encoders

# Define Dataset Class
class ChatbotDataset(Dataset):
    def _init_(self, data, tokenizer, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def _len_(self):
        return len(self.data)

    def _getitem_(self, item):
        text = self.data.iloc[item]['User_Input']
        label = self.data.iloc[item]['Emotion']  # Emotion column as label
        
        # Handling NaN labels: Replace NaN with a default value (e.g., 0) if found
        if pd.isna(label):
            print(f"Warning: NaN label found at index {item}, replacing with default value (0)")
            label = 0  # or any other default value you want to assign
        
        # Ensure label is an integer (this is necessary for classification tasks)
        label = int(label)  # Convert to integer (if not already)

        # Encoding the input text
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)  # Ensure it's a tensor of type long (int64)
        }

# Load the dataset
data = pd.read_csv('./Datasets/mental_health_chatbot_dataset.csv')  # Update path as needed
data = data[['User_Input', 'Emotion']]  # Use 'User_Input' and 'Emotion' for training

# Convert Emotion to numerical values if not already done
emotion_mapping = {'happy': 0, 'sad': 1, 'angry': 2, 'fearful': 3, 'surprised': 4}  # Update this as per your dataset
data['Emotion'] = data['Emotion'].map(emotion_mapping)

# Split data into train and test sets
train_data, val_data = train_test_split(data, test_size=0.1)

# Initialize the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(emotion_mapping))

# Create Dataset objects
train_dataset = ChatbotDataset(train_data, tokenizer, max_len=128)
val_dataset = ChatbotDataset(val_data, tokenizer, max_len=128)

# Create DataLoader objects
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# Define a function to compute the evaluation metrics (accuracy in this case)
def compute_metrics(p):
    predictions, labels = p
    preds = np.argmax(predictions, axis=1)
    accuracy = accuracy_score(labels, preds)
    return {"accuracy": accuracy}

# Training Arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy"  # Use 'accuracy' as the metric for the best model
)

# Trainer Class
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics  # Pass the custom metric function
)

# Train the model
trainer.train()

# Save the model after training
trainer.save_model('chatbot_model')

# Save the enco…