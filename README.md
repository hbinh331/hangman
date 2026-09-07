# Hangman game

> Simple hangman game using Pygame

## Overview
This project simulates the famous hangman game using Python

## Project structure
```text
├── animals.txt         # Wordlist
├── logic.py            # Game logic 
├── main.py             # GUI             
└── .gitignore
```
## Features
- A random word is selected from the wordlist  
- After each guess, display: word status, guessed letters, remaining guesses
- Handle empty input, non-alphabet input, guessed letters
- Case-insensitive
- Game ends: notification upon winning/losing, display answer, prompt users to Play again/Quit

## Usage
```
python main.py
```
## Limitations
- A score and ranking system can be implemented for better playing experience
- Lacks a function that allows users to select wordlists from a wide range of topics   
*These new functions can be easily implemented with the use of Pygame
