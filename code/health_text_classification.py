from transformers import pipeline
import sys
import sys
sys.stdout.reconfigure(encoding='utf-8')

def health_text_classifier(text):
    classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
    candidate_labels = ["life critical medical emergency", "casual medical need", "general activity"]
    op_text_class = classifier(text,candidate_labels)
    class_score = {}
    for i in range(len(op_text_class['labels'])):
        class_score[op_text_class['labels'][i]] = round(op_text_class['scores'][i],4)
    return class_score

if __name__ == "__main__":
    task = "Go and save Amit, he has fallen down the stairs."
    classification_score = health_text_classifier(task)
    print(classification_score)