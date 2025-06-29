from transformers import pipeline

# Load only once globally
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_insurance_document(text: str) -> bool:
    candidate_labels = ["insurance claim form", "bank form", "job application", "unrelated form"]
    result = classifier(text[:1000], candidate_labels=candidate_labels)
    top_label = result['labels'][0]
    score = result['scores'][0]

    return top_label == "insurance claim form" and score > 0.6  # Threshold to be strict
