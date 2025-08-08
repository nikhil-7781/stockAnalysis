from transformers import pipeline

# Load summarization model once
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_texts(texts, max_length=60):
    summaries = []
    for text in texts:
        try:
            summary = summarizer_pipeline(text, max_length=max_length, min_length=20, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            summaries.append(text)  # fallback to original if summarizer fails
    return summaries
