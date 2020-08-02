from textblob import TextBlob


def get_score(text):
    text_to_analyse = TextBlob(text)
    return text_to_analyse.sentiment.polarity


def get_final_score(scores):
    summation = 0
    for score in scores:
        summation += score

    average = summation / len(scores)

    return average


def get_text_score(score):
    """Very positive - above 0.75
Positive - (0.25, 0.75)
Neutral - (-0.25, 0.25)
Negative - (-0.75, -0.25)
Very negative - below -0.75"""

    scores = ["Very Positive",
              "Positive",
              "Neutral",
              "Negative",
              "Very Negative"]

    if score > 0.75:
        return scores[0]

    elif 0.25 <= score <= 0.75:
        return scores[1]

    elif -0.25 <= score <= 0.25:
        return scores[2]

    elif -0.75 <= score <= -0.25:
        return scores[3]

    else:
        return scores[4]
