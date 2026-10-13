
import requests
import textwrap


def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.status_code == 200:
        joke_data = response.json()

        setup = textwrap.fill(joke_data['setup'], width=60)
        punchline = textwrap.fill(joke_data['punchline'], width=60)

        print("\n" + "=" * 50)
        print("🐬😂 Here's a Random Joke for You! 😂🐬")
        print("=" * 50 + "\n")

        print(f"🤔 {setup}\n")
        print(f"🤣 {punchline}\n")

        print("🎉" + "-" * 48 + "🎉\n")

        return f"🤔 {setup} 😂 {punchline}"

    else:
        print("😢❌ Failed to retrieve joke. Please try again later! 🔄")
        return None


def main():
    print("🎉 Welcome to the JSoofy Random Joke Generator! 🐬😂\n")
    print("Press [Enter] for a new joke, or type 'q'/'exit' to quit. 🚪\n")

    while True:
        user_input = input("😎 Your choice: ").strip().lower()

        if user_input in ("q", "exit"):
            print("\n😂 Thanks for laughing with us! Goodbye! 👋🐬\n")
            break

        get_random_joke()


if __name__ == "__main__":
    main()