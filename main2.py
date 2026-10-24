import gradio as gr

LEXICON = {
    "good": 2, "great": 3, "amazing": 3, "love": 3, "fast": 1, 
    "worth": 2, "awesome": 3, "excellent": 3, "nice": 2, "perfect": 3, 
    "bad": -2, "terrible": -3, "slow": -1, "broke": -2, "disappointed": -2, 
    "awful": -3, "hate": -3, "poor": -2, "useless": -3
}

NEGATION = {"not", "no", "never", "isn't", "none", "nothing", "neither", "nor"}
PUNCTUATION = ".,!?:;\"'()"

def clean_word(word):
    return word.lower().strip(PUNCTUATION)

def is_negation(word):
    return word in NEGATION or word.endswith("n't")

def analyse(review):
    pairs = []
    is_negated = False

    for original in review.split():
        word = clean_word(original)
        point = 0

        if is_negation(word):
            is_negated = True
            pairs.append((original, 0))
            continue

        if word in LEXICON:
            point = LEXICON[word]
            if is_negated:
                point = -point
                is_negated = False

        pairs.append((original, point))

    return pairs

def mood_score(review):
    return sum(points for _, points in analyse(review))

def classify(review):
    score = mood_score(review)
    if score >= 1:
        return "POSITIVE"
    elif score <= -1:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

COLORS = {"positive": "lightgreen", "negative": "salmon"}

def process_review(review):
    pieces = []
    for word, points in analyse(review):
        if points > 0:
            label = "positive"
        elif points < 0:
            label = "negative"
        else:
            label = None
        
        pieces.append((word + " ", label))

    return classify(review), mood_score(review), pieces

demo = gr.Interface(
    fn=process_review,
    inputs=gr.Textbox(lines=3, label="Paste a review"),
    outputs=[
        gr.Textbox(label="Mood Classification"),
        gr.Number(label="Mood Score"),
        gr.HighlightedText(label="Word Sentiment Breakdown", color_map=COLORS),
    ],
    title="Moodly: Here for Mood Detector",
    description="Green words add positive points; red words subtract points. Total score >= 1 is POSITIVE, <= -1 is NEGATIVE.",
    examples=[
        ["This product is great and fast, totally worth it!"],
        ["The service was terrible and slow. I hate it."],
        ["It was not good, actually quite bad."],
        ["The package arrived. It is okay, nothing special."]
    ]
)

if __name__ == "__main__":
    demo.launch(share=False)