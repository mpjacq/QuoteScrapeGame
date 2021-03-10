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
    Plays a guessing game, which scrapes website for a quote and has player
    type in their guess. Answer must match first and last name as typed
    on the website (including punctuation), but guesses may be case
    insensitive.
    :return: None
    """

    guessed = False
    tries = 1

    # Scrape quotes and author from webpage
    all_quotes = get_quotes()
    choice = random.choice(all_quotes)
    quote = choice[0]
    author = choice[1]

    # Set up the intro message and first turn.
    print("\n##################################"
          "\n########## Who Said It? ##########"
          "\n##################################\n")

    # Display the quote
    print(quote + "\n")

    # Explain the rules and get player guess
    guess = input("Who said it? You'll get 3 tries. Please type your guess (first and last name): ")

    while not guessed and tries <= 3:

        # Correct guess
        if guess.lower() == author.lower():
            print(f"That's correct! It took you {tries} guess(es). Good job!")
            guessed = True
            return

        # Incorrect guess
        else:

            if tries < 3:
                print(f"Sorry, {guess} is incorrect. You have {3 - tries} tries remaining.")
                guess = input("Try again: ")

            # If player has used all 3 tries
            else:
                print(f"Sorry, you used up all of your tries. The correct answer was: {author}")

            tries += 1


if __name__ == "__main__":

    playing = True

    play_count = 0

    while playing:

        # Only ask if they want to play again after the first time.
        if play_count > 0:
            play_again = input("Would you like to play again? Y/N ")

        # Increment play count after first play-through so that
        # we get the prompt asking if you want to play again
        else:
            play_again = "Y"
            play_count += 1

        # Call game method if they want to play again
        if play_again.upper() == "Y":
            guessing_game()

        # Exit while loop if not playing again
        elif play_again.upper() == "N":
            playing = False

        # Keep looping if invalid input
        else:
            print(f"{play_again} isn't a valid input.")

    # Exit message
    print("Goodbye!")


