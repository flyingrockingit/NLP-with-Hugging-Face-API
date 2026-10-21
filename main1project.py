# PART 1: TOKENISING
def clean_message(message):
    punctuation = ".,!?:;\"'()-"
    cleaned_text = message.lower()

    for char in punctuation:
        cleaned_text = cleaned_text.replace(char, " ")

    tokens = cleaned_text.split()
    return tokens

# PART 2: WEIGHTS AND THE SCORE
WORD_WEIGHTS = {
    "broken": 3,
    "ruined": 3,
    "missing": 3,
    "refund": 3,
    "damaged": 3,
    "late": 2,
    "wrong": 2,
    "delay": 2,
    "asap": 2,
    "angry": 2,
    "upset": 2,
    "help": 1,
    "today": 1,
}


def calculate_urgency_score(tokens):
    total_score = 0
    for token in tokens:
        if token in WORD_WEIGHTS:
            total_score += WORD_WEIGHTS[token]
    return total_score

# PART 3: THE THRESHOLD
URGENCY_THRESHOLD = 2

def classify_message(message):
    tokens = clean_message(message)
    score = calculate_urgency_score(tokens)

    if score >= URGENCY_THRESHOLD:
        label = "URGENT"
    else:
        label = "NORMAL"

    return label, score, tokens

# PART 4: FALSE POSITIVES AND FALSE NEGATIVES
def run_bakery_sorter():
    test_messages = [
        ("My cake arrived broken and completely ruined!", "URGENT"),
        ("Hello, what time do you open on Saturdays?", "NORMAL"),
        ("Where is my order? It is late for the party today!", "URGENT"),
        ("Thanks for your help! The wedding cake was amazing.", "NORMAL"),
        ("The order arrived but the cupcakes are missing.", "URGENT"),
        ("Can I change my delivery address for tomorrow?", "NORMAL"),
    ]

    print("--- MAYA'S BAKERY MESSAGE SORTER ---\n")

    correct = 0
    false_positives = 0
    false_negatives = 0

    for i, (msg, expected) in enumerate(test_messages, start=1):
        predicted, score, tokens = classify_message(msg)

        if predicted == expected:
            result = "CORRECT"
            correct += 1
        elif predicted == "URGENT" and expected == "NORMAL":
            result = "FALSE POSITIVE"
            false_positives += 1
        else:
            result = "FALSE NEGATIVE"
            false_negatives += 1

        print(f'Test #{i}: "{msg}"')
        print(f"  Tokens: {tokens}")
        print(f"  Score: {score} | Threshold: {URGENCY_THRESHOLD}")
        print(f"  Predicted: {predicted} | Expected: {expected}")
        print(f"  Result: {result}")
        print("-" * 50)

    total = len(test_messages)
    print("\n--- RESULTS SUMMARY ---")
    print(f"Accuracy: {correct}/{total} ({int((correct/total)*100)}%)")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")

def interactive_mode():
    print("\n===========================")
    print("INTERACTIVE HELP DESK TESTING MODE")
    print("(Type 'quit' or 'exit' to end program)")
    print("=============================")

    while True:
        user_input = input("\nEnter a message: ")

        if user_input.lower().strip() in ["quit", "exit"]:
            print("Exiting Help Desk Sorter. Goodbye!")
            break

        if not user_input.strip():
            continue

        label, score, tokens = classify_message(user_input)

        print(f"  Tokens : {tokens}")
        print(f"  Score  : {score}")
        print(f"  Status : [{label}]")


if __name__ == "__main__":
    run_bakery_sorter()

    interactive_mode()