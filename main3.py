
import gradio as gr
import pandas as pd

MENU = {
    "pizza": 950, "pasta": 420, "burger": 880, "fries": 760, "tacos": 310,
    "sushi": 280, "ramen": 260, "biryani": 990, "paneer tikka": 540,
    "butter chicken": 610, "masala dosa": 470, "idli": 350, "samosa": 640,
    "pav bhaji": 380, "momos": 720, "noodles": 590, "fried rice": 500,
    "sandwich": 450, "salad": 230, "pancakes": 210, "waffles": 190,
    "brownie": 330, "cake": 300, "coke": 800, "coffee": 670, "tea": 560,
    "mango lassi": 400, "ice cream": 690, "milkshake": 360, "nachos": 270,
}

KEY_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

KEY_POS = {
    key: (row, col)
    for row, keys in enumerate(KEY_ROWS)
    for col, key in enumerate(keys)
}


# Check whether two letters are neighbouring keyboard keys
def are_neighbours(x, y):
    if x == y or x not in KEY_POS or y not in KEY_POS:
        return False

    (r1, c1), (r2, c2) = KEY_POS[x], KEY_POS[y]

    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1


# Calculate the cost of changing one letter
def change_cost(x, y, use_keyboard):
    if x == y:
        return 0

    if use_keyboard and are_neighbours(x, y):
        return 0.5

    return 1


# Build the edit-distance table
def build_table(a, b, use_keyboard, use_swaps):

    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    # Initialise the first column
    for i in range(len(a) + 1):
        table[i][0] = i

    for j in range(len(b) + 1):
        table[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):

            delete = table[i - 1][j] + 1
            insert = table[i][j - 1] + 1

            change = (
                table[i - 1][j - 1]
                + change_cost(a[i - 1], b[j - 1], use_keyboard)
            )

            table[i][j] = min(delete, insert, change)

            if (
                use_swaps
                and i > 1
                and j > 1
                and a[i - 1] == b[j - 2]
                and a[i - 2] == b[j - 1]
            ):
                table[i][j] = min(
                    table[i][j],
                    table[i - 2][j - 2] + 1
                )

    return table


def edit_distance(a, b, use_keyboard, use_swaps):
    return build_table(a, b, use_keyboard, use_swaps)[-1][-1]


def suggest(query, use_keyboard, use_swaps, k=5):

    query = query.lower().strip()
    ranked = []

    for dish, orders in MENU.items():

        dist = edit_distance(query, dish, use_keyboard, use_swaps)

        ranked.append((dist, -orders, dish))

    ranked.sort()

    return [
        (dish, dist, -neg_orders)
        for dist, neg_orders, dish in ranked[:k]
    ]


def max_typos(query):
    return max(1, len(query) // 4)


def did_you_mean(query, use_keyboard, use_swaps):

    query = query.lower().strip()

    if query in MENU:
        return query, f"Showing results for **{query}**"

    best = suggest(query, use_keyboard, use_swaps, k=1)

    if not best:
        return None, "No results found."

    dish, dist, orders = best[0]

    if dist <= max_typos(query):
        return dish, f"Did you mean: **{dish}**?"

    return None, f"No dishes found for '{query}'."


def search(query, keyboard, swaps):

    query = query.lower().strip()

    if not query:
        return "Type a dish name above.", None, None

    dish, message = did_you_mean(query, keyboard, swaps)

    top_dishes = suggest(query, keyboard, swaps, k=5)

    top_df = pd.DataFrame(
        top_dishes,
        columns=["Dish", "Edit Distance", "Orders"]
    )

    target = dish or top_dishes[0][0]

    matrix = build_table(query, target, keyboard, swaps)

    headers = ["", "."] + list(target)

    rows = [
        ["." if i == 0 else query[i - 1]]
        + [f"{v:g}" for v in row]
        for i, row in enumerate(matrix)
    ]

    grid_df = pd.DataFrame(rows, columns=headers)

    info_text = (
        f"## {message}\n"
        f"_Allowed typos for a {len(query)}-letter search: "
        f"{max_typos(query)}_"
    )

    return info_text, top_df, grid_df


with gr.Blocks(title="Did You Mean?") as demo:

    gr.Markdown('# Food search with "Did you mean?"')

    query_input = gr.Textbox(
        label="Search the menu",
        value="biriyani"
    )

    with gr.Row():

        keyboard_check = gr.Checkbox(
            value=True,
            label="Upgrade 1: neighbouring keys cost 0.5"
        )

        swaps_check = gr.Checkbox(
            value=True,
            label="Upgrade 2: swapped letters cost 1"
        )

    answer_output = gr.Markdown()

    with gr.Row():

        top_output = gr.Dataframe(
            label="Closest dishes"
        )

        grid_output = gr.Dataframe(
            label="Edit-distance table (bottom-right cell = the answer)"
        )

    gr.Examples(
        [
            ["piza"],
            ["cske"],
            ["noodels"],
            ["panner tika"],
            ["lasi"]
        ],
        inputs=query_input
    )

    inputs = [query_input, keyboard_check, swaps_check]

    outputs = [answer_output, top_output, grid_output]

    for trigger in (
        query_input.change,
        keyboard_check.change,
        swaps_check.change
    ):
        trigger(search, inputs, outputs)

    demo.load(search, inputs, outputs)


if __name__ == "__main__":
    demo.launch()
