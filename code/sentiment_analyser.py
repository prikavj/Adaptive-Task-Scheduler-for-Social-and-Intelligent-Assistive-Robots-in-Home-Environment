from transformers import pipeline
import sys
import emot
import sys
import re
import statistics
sys.stdout.reconfigure(encoding='utf-8')

def emotion_score(text):
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base",top_k=None )

    emot_obj = emot.core.emot() 
    emoji_names = emot_obj.emoji(text)
    emo_names = [i.strip(":").replace('_', ' ') for i in emoji_names['mean']]
    emo_values = emoji_names['value']

    for emoji in emo_values:
        text = text.replace(emoji, '')
    text = re.sub(' +', ' ', text.strip())

    if len(text) != 0 and len(emo_names) == 0:
        op_emotion = convert_to_label_based_dict(classifier(text))
    elif len(text) != 0 and len(emo_names) != 0:
        emo_names.append(text)
        op_emotion = convert_to_label_based_dict(classifier(emo_names))
    else:
        op_emotion = "Wrong Text Input"
    
    # Categorize emotions
    happy = op_emotion.get('joy', 0) + op_emotion.get('surprise', 0)
    sad = op_emotion.get('sadness', 0) + op_emotion.get('fear', 0) + op_emotion.get('anger', 0) + op_emotion.get('disgust', 0)
    neutral = op_emotion.get('neutral', 0)

    emotion_normalised_score = {'happy' : happy, 'sad' : sad, 'neutral' : neutral}
    return emotion_normalised_score

def convert_to_label_based_dict(sentiment_list):
    label_based_dict = {}
    mean_op_dict = {}
    for sentiments in sentiment_list:
        for sentiment in sentiments:
            label = sentiment['label']
            score = sentiment['score']
            if label in label_based_dict:
                label_based_dict[label].append(score)  
            else:
                label_based_dict[label] = [score]
    
    for k in label_based_dict.keys():
        mean_op_dict[k] = round(statistics.mean(label_based_dict[k]),4)
    return mean_op_dict

if __name__ == "__main__":
    task = "I am not feeling well 😔. Please bring me my medicine."
    emotion_score = emotion_score(task)
    print(emotion_score)