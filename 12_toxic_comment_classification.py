# toxic comment classification
import os
import re
import string
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (confusion_matrix, classification_report, ConfusionMatrixDisplay)
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
pd.set_option('display.max_colwidth', 100)
np.random.seed(42)
tf.random.set_seed(42)

#task 1
df = pd.read_csv('toxic_comments_dataset.csv')
print("=== TASK 1: DATASET EXPLORATION ===")
print("\nFirst 10 records:")
print(df.head(10))
print("\nLast 8 records:")
print(df.tail(8))
print("\nDataset shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nData types of each column:")
print(df.dtypes)
print("\nStatistical summary:")
print(df.describe())

#task 2
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    text = re.sub(r'@\w+|#\w+', ' ', text)
    text = re.sub(r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E0-\U0001F1FF]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
print("\n=== TASK 2: CLEANING & PREPROCESSING ===")
df.dropna(subset=['Comment_Text', 'Toxicity_Label'], inplace=True)
df['Clean_Comment'] = df['Comment_Text'].apply(clean_text)
before_dedup = df.shape[0]
df.drop_duplicates(inplace=True)
after_dedup = df.shape[0]
print(f"Rows before deduplication: {before_dedup}")
print(f"Rows after deduplication:  {after_dedup}")
df.reset_index(drop=True, inplace=True)
print("\nMissing values in each column:")
print(df.isnull().sum())
print("\nToxicity label distribution:")
print(df['Toxicity_Label'].value_counts())
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Toxicity_Label', order=df['Toxicity_Label'].value_counts().index)
plt.title('Distribution of Toxicity Labels')
plt.xlabel('Toxicity Label')
plt.ylabel('Count')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
X = df['Clean_Comment']
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['Toxicity_Label'])
num_classes = len(label_encoder.classes_)
print("\nTarget Classes:", list(label_encoder.classes_))
print("Number of Classes:", num_classes)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}")

#task 3
print("\n=== TASK 3: NLP TOKENIZATION & PADDING ===")
VOCAB_SIZE = 8000
OOV_TOKEN = '<OOV>'
tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOKEN)
tokenizer.fit_on_texts(X_train)
vocab_len = len(tokenizer.word_index) + 1
print(f"Effective Vocabulary size: {vocab_len}")
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)
seq_lengths = [len(seq) for seq in X_train_seq]
print("Max sequence length in training data:", max(seq_lengths))
MAX_LEN = 20
X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_LEN, padding='post', truncating='post')
X_test_pad = pad_sequences(X_test_seq, maxlen=MAX_LEN, padding='post', truncating='post')
print("Padded training shape:", X_train_pad.shape)
print("Padded testing shape: ", X_test_pad.shape)

#task 4
print("\n=== TASK 4: MODEL BUILDING & TRAINING ===")
EMBEDDING_DIM = 64
model = Sequential([
    Embedding(input_dim=vocab_len, output_dim=EMBEDDING_DIM),
    LSTM(64, return_sequences=False),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()
history = model.fit(
    X_train_pad, 
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

#task 5
print("\n=== TASK 5: EVALUATION & VISUALIZATION ===")
y_pred_probs = model.predict(X_test_pad)
y_pred = np.argmax(y_pred_probs, axis=1)
fig_cm, ax_cm = plt.subplots(figsize=(7, 6))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
disp.plot(cmap='Blues', xticks_rotation=45, values_format='d', ax=ax_cm)
ax_cm.set_title('Confusion Matrix - Toxic Comment Classification')
plt.tight_layout()
plt.show()
test_loss, test_accuracy = model.evaluate(X_test_pad, y_test, verbose=0)
print(f"Test Loss:     {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}\n")
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print("Classification Report:\n", report)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(history.history['accuracy'], label='Train Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[1].plot(history.history['loss'], label='Train Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
plt.tight_layout()
plt.show()
new_comments = [
    "Thank you for sharing this perspective with the community.",
    "This comment is rude and disrespectful.",
    "The comment is extremely hostile and violates community standards.",
    "This reply contains a threat-like statement and is unsafe.",
    "The message targets a group unfairly and violates community rules."
]
clean_new = [clean_text(c) for c in new_comments]
seq_new = tokenizer.texts_to_sequences(clean_new)
pad_new = pad_sequences(seq_new, maxlen=MAX_LEN, padding='post', truncating='post')
pred_probs_new = model.predict(pad_new)
pred_labels_new = label_encoder.inverse_transform(np.argmax(pred_probs_new, axis=1))
print("\n--- Model Predictions on New Comments ---")
for comment, label in zip(new_comments, pred_labels_new):
    print(f"Comment: {comment}\nPredicted Label: {label}\n")