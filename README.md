# wordle-bot
This repository is a Wordle bot that automates the desktop browser to solve the Wordle game in under 6 attempts (from New York Times website). 
This can be used for Safari, Firefox, or Chrome if you already have Selenium driver installed for the browser.

## Installation
1. Install/configure [Selenium browser drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) if you haven't.
2. Download this repository and extract the .zip file.
3. Install needed pip packages: `pip install -r requirements.txt`
4. Run the program: `python main.py`

## To-do
- [x] Chrome support
- [x] Firefox support
- [ ] Fix update word prediction list when no. of present letter > 1 in one row