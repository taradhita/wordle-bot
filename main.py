from numpy import append
from wordle import WordleSolver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time

def play_wordle(driver, shadow_root, wordle, sorted_top_words):
    current_guess = ''
    for guess in range(5):
        if guess != 0:
            answer = current_guess
        else:
            # select randomly from top 10 sorted words with most possibilities
            first_guess = (list(zip(*sorted_top_words[:10]))[0])
            answer = random.choice(first_guess)
        
        time.sleep(1)

        game_row = shadow_root.find_element(By.CSS_SELECTOR, "game-row:nth-child(" +str(guess+1)+")")
        game_row.send_keys(answer)
        game_row.send_keys(Keys.ENTER)

        row = execute_shadow_root(driver, game_row)
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")

        evaluation = evaluate_answer(tiles)

        if evaluation != [2,2,2,2,2]:
            wordle.retrieve_answer(answer, evaluation)
   
            newlist = wordle.update_predict_list(wordlist_in_char)
            print(newlist)
            current_guess = newlist[0]
        
        time.sleep(5)

def execute_shadow_root(driver, element):
    return driver.execute_script("return arguments[0].shadowRoot", element)

def retrieve_first_guess(wordle, char, list):
    scores = wordle.count_word_score(char)
    sorted_top_words = wordle.sort_top_word_opening(list, scores)

    return sorted_top_words

def evaluate_answer(tiles):
    evaluation = []
    eval_to_int = {
        "correct": 2,
        "present": 1,
        "absent": 0
    }

    for tile in tiles:
        evaluation.append(eval_to_int[tile.get_attribute("evaluation")])

    return evaluation

def open_wordle(driver):
    driver.get("https://www.nytimes.com/games/wordle/index.html")

    # i don't know why, but this is the only way the modal can be closed (on safari)
    driver.find_element(By.XPATH, "//html").click()
    driver.find_element(By.XPATH, "//html").click()

if __name__ == '__main__':
    driver = webdriver.Safari()
    open_wordle(driver)

    game_app = driver.find_element(By.TAG_NAME, 'game-app')
    shadow_root = execute_shadow_root(driver, game_app)

    wordle = WordleSolver()
    wordlist = wordle.load_wordlist()
    wordlist_in_char = wordle.split_into_chars(wordlist)
    scores = wordle.count_word_score(wordlist_in_char)
    sorted_top_words = wordle.sort_top_word_opening(wordlist, scores)

    play_wordle(driver, shadow_root, wordle, sorted_top_words)

    driver.quit()