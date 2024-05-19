import pandas as pd
from comet import download_model, load_from_checkpoint
import os
from tqdm import tqdm


# 1. Data Preparation
source_file = "valid.en"
translated_file = "valid.vi"
source_lang="en"
target_lang="vi"
threadhold = 0.8

with open(source_file, "r", encoding="utf-8") as f:
    source_sentences = f.readlines()
    source_sentences = [sentence.strip() for sentence in source_sentences]  # remove newlines

with open(translated_file, "r", encoding="utf-8") as f:
    translated_sentences = f.readlines()
    translated_sentences = [sentence.strip() for sentence in translated_sentences]  # remove newlines

data = pd.DataFrame({source_lang: source_sentences, target_lang: translated_sentences})



# 2. COMET Model Setup (Same as before)
model_path = download_model("wmt20-comet-qe-da")  
model = load_from_checkpoint(model_path)


# 3. Scoring and Filtering (Updated for multiple lines)
comet_scores = []
for _, row in tqdm(data.iterrows(), total=len(data)):
    src_text = row[source_lang]
    mt_text = row[target_lang]

    score = model.predict(src_text, mt_text)  
    comet_scores.append(score)

data["comet_score"] = comet_scores

high_score_data = data[data["comet_score"] > threadhold]
low_score_data = data[data["comet_score"] <= threadhold]

# Create Directories to organize results (Same as before)
os.makedirs('high_quality', exist_ok=True)
os.makedirs('low_quality', exist_ok=True)

# Write results to files (Modified to keep original line format)
# High Quality
with open(f"high_quality/{source_file.split('.')[0]}_high_quality.txt", "w", encoding="utf-8") as f:
    f.writelines(high_score_data[source_lang])
with open(f"high_quality/{translated_file.split('.')[0]}_high_quality.txt", "w", encoding="utf-8") as f:
    f.writelines(high_score_data[target_lang])

# Low Quality
with open(f"low_quality/{source_file.split('.')[0]}_low_quality.txt", "w", encoding="utf-8") as f:
    f.writelines(low_score_data[source_lang])
with open(f"low_quality/{translated_file.split('.')[0]}_low_quality.txt", "w", encoding="utf-8") as f:
    f.writelines(low_score_data[target_lang])
