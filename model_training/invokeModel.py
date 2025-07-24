import torch
from transformers import RobertaTokenizer
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

import numpy as np

# Define your model class (must match training)
class RobertaForVAD(torch.nn.Module):
    def __init__(self, model_name):
        super().__init__()
        from transformers import RobertaModel
        self.roberta = RobertaModel.from_pretrained(model_name)
        self.dropout = torch.nn.Dropout(0.1)
        self.regressor = torch.nn.Linear(self.roberta.config.hidden_size, 3)

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs.last_hidden_state[:, 0]
        x = self.dropout(pooled)
        return self.regressor(x)

if __name__ == "__main__":
    # Load model and tokenizer
    model = RobertaForVAD('roberta-base')
    model.load_state_dict(torch.load('model_training/roberta_vad_regression.pt', map_location='cpu'))
    model.eval()
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
   # text = "I am extremely nervous about the upcoming exam."

    # inputs = tokenizer(text, return_tensors='pt', truncation=True, padding='max_length', max_length=128)
    # with torch.no_grad():
    #     outputs = model(inputs['input_ids'], inputs['attention_mask'])
    # vad = outputs[0].tolist()  # [V, A, D]
    # print(f"Valence: {vad[0]:.3f}, Arousal: {vad[1]:.3f}, Dominance: {vad[2]:.3f}")

    df = pd.read_csv('model_training/data/test_vad.csv')
    true_vad = df[['V', 'A', 'D']].values
    pred_vad = []

    for text in df['text']:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding='max_length', max_length=128)
        with torch.no_grad():
            outputs = model(inputs['input_ids'], inputs['attention_mask'])
        pred_vad.append(outputs[0].numpy())

    pred_vad = np.array(pred_vad)
    np.save('model_training/data/pred_vad.npy', pred_vad)  # <-- Add this line here

    output_df = df.copy()
    output_df['pred_V'] = pred_vad[:, 0]
    output_df['pred_A'] = pred_vad[:, 1]
    output_df['pred_D'] = pred_vad[:, 2]
    output_df.to_csv('model_training/data/test_vad_with_predictions.csv', index=False)

    # Calculate metrics for each dimension
    for i, name in enumerate(['Valence', 'Arousal', 'Dominance']):
        mse = mean_squared_error(true_vad[:, i], pred_vad[:, i])
        mae = mean_absolute_error(true_vad[:, i], pred_vad[:, i])
        r2 = r2_score(true_vad[:, i], pred_vad[:, i])
        print(f"{name}: MSE={mse:.4f}, MAE={mae:.4f}, R2={r2:.4f}")
    
    accuracy = accuracy_score(true_vad, pred_vad)
    precision = precision_score(true_vad, pred_vad, average='weighted')
    recall = recall_score(true_vad, pred_vad, average='weighted')
    f1 = f1_score(true_vad, pred_vad, average='weighted')
    cm = confusion_matrix(true_vad, pred_vad)
    print(f"accuracy: {accuracy}, precision: {precision},recall: {recall}, f1: {f1},confusion matrix: {cm}")