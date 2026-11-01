import gradio as gr
from article import ARTICLES


def search_article(query):
    if not query or not query.strip():
        return "Enter a keyword or phrase to search"

    query = query.strip().lower()
    results = []

    for title, text in ARTICLES:
        if query in title.lower() or query in text.lower():
            results.append((title, text))

    if not results:
        return f"No articles found for '{query}'."

    output = f"### Found {len(results)} matching article(s)\n\n"

    for title, text in results:
        output += f"### {title}\n\n"
        output += f"{text}\n\n---\n\n"

    return output


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Mini Search Engine"
) as demo:

    gr.Markdown("# Mini Search Engine")

    gr.Markdown(
        "Search a small encyclopedia of articles "
        "by entering a keyword or phrase."
    )

    with gr.Row():

        search_input = gr.Textbox(
            label="Search",
            placeholder="Try: Moon, volcanoes, internet ...",
            scale=4
        )

        search_button = gr.Button(
            "Search",
            variant="primary",
            scale=1
        )

    search_output = gr.Markdown()

    search_button.click(
        fn=search_article,
        inputs=search_input,
        outputs=search_output
    )
    
if __name__ == "__main__":
    demo.launch()