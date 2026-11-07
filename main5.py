import gradio as gr
from langdetect import detect, detect_langs, LangDetectException

languages = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "sw": "Swahili",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ar": "Arabic",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "ja": "Japanese",
    "ko": "Korean",
    "hi": "Hindi",
    "ru": "Russian",
    "nl": "Dutch",
    "tr": "Turkish",
    "pl": "Polish",
    "el": "Greek",
    "he": "Hebrew",
    "th": "Thai",
    "vi": "Vietnamese"
}

def detect_language(sentence):
    if not sentence.strip():
        return "Please enter a sentence."

    try:
        language_code = detect(sentence)
        probabilities = detect_langs(sentence)

        language_name = languages.get(language_code, language_code)
        confidence = probabilities[0].prob * 100

        return (
            f"Detected Language: {language_name}\n"
            f"Language code: {language_code}\n"
            f"Confidence: {confidence:.2f}%"
        )

    except LangDetectException:
        return "Unable to detect language. Try a longer sentence."

demo = gr.Interface(
    fn=detect_language,
    inputs=gr.Textbox(
        lines=4,
        placeholder="Enter a sentence here ... ",
        label="Your sentence"
    ),
    outputs=gr.Textbox(label="Language Detection Result"),
    title="Language Detection System",
    description="Enter a sentence to identify the language used.",
    submit_btn="Detect Language",
    clear_btn="Clear"
)

if __name__ == "__main__":
    demo.launch()