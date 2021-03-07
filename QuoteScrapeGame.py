from bs4 import BeautifulSoup
import requests
import random

def get_quotes():
    """
    Returns a dictionary of quotes and their authors. Data is from
    quotes.toscrape.com. Requires no input. Will collect quotes from
    all pages till contents run out.
    :return: Dictionary with keys 0-# of quotes from webpage source,
    values of [quote text, author]
    """

    # Set up variables to page through the website,
    # which will be updated in the while loop to advance

    url = "https://quotes.toscrape.com/page/"
    num = 1
    req = requests.get(str(url) + str(num))
    page_ok = req.text.find("No quotes found!")
    html = req.text
    quote_text_list = []
    auth_text_list = []
    qa_dict = {}

    # page_ok returns -1 when not "no quotes found!" on the page
    while page_ok == -1:

        soup = BeautifulSoup(html, "html.parser")
        quote = soup.find_all(class_="text")
        author = soup.find_all(class_="author")

        # Extract the quotes from the page
        for q in range(0, len(quote)):
            quote_text_list.append(quote[q].get_text())

        # Extract the authors from the page
        for a in range(0, len(author)):
            auth_text_list.append(author[a].get_text())

        # Add quote: author pairing to the dictionary of results
        # dict format: { 0: [quote, auth], 1: [quote, auth]...}
        for q in range(0, len(quote_text_list)):
            qa_dict[q] = [quote_text_list[q], auth_text_list[q]]

        # Advance page
        num += 1
        req = requests.get(str(url) + str(num))
        page_ok = req.text.find("No quotes found!")
        html = req.text

    return qa_dict

def guessing_game():
    """

    :return:
    """

    playing = True
    guessed = False
    tries = 1

    # Scrape quotes and author from webpage
    all_quotes = get_quotes()
    choice = random.choice(all_quotes)
    quote = choice[0]
    author = choice[1]

    # Set up the intro message and first turn.
    print("##################################\n########## Who Said It? ##########\n##################################\n")
    print(quote + "\n")
    guess = input("Who said it? Please type your guess. You'll get 3 tries.\n"
                  "Please include the whole name (first and last): \n")

    while not guessed and tries < 3:

        if guess.lower() == author.lower():
            print(f"That's correct! It took you {tries} guess(es). Good job!")
            try_again = input("Would you like to play again? Y/N ")

            if try_again.upper() == "Y":
                guessed = True

            else:
                guessed = True

        else:
            print(f"Sorry, {guess} is incorrect. You have {3 - tries} tries remaining.")
            tries += 1
            guess = input("Try again:\n")

    counter = 0

    while tries >= 3 and not guessed:

        if counter == 0:
            print(f"Sorry, you used up all of your tries. The correct answer was: {author}")
            try_again = input("Would you like to play again? Y/N ")

        if try_again.upper() == "Y":
            print("\n")
            guessing_game()

        elif try_again.upper() == "N":
            print("Goodbye!")
            return

        else:
            counter += 1
            try_again = input("That's not a valid choice. Want to try that again? Y/N: ")


if __name__ == "__main__":

    guessing_game()

