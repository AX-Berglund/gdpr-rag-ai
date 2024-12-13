import os
import json

def preprocess_gdpr_text(input_dir, output_file, chunk_size=500):
    articles = []
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r") as f:
                article_text = f.read()
                article_id = os.path.splitext(filename)[0]
                chunks = [
                    {"id": f"{article_id}_{i}", "text": article_text[i:i+chunk_size].strip()}
                    for i in range(0, len(article_text), chunk_size)
                ]
                articles.extend(chunks)
    
    with open(output_file, "w") as outfile:
        json.dump(articles, outfile, indent=4)
    print(f"Preprocessed data saved to {output_file}")

if __name__ == "__main__":
    input_directory = "./data/articles"
    output_path = "./data/preprocessed_chunks.json"
    preprocess_gdpr_text(input_directory, output_path)
