from transformers import pipeline


def predict_sentiment(text):
    classifier = pipeline("sentiment-analysis", model="./my_fineTuned_model")
    output = classifier(text)
    return output


