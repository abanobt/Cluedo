# Cluedo Game

## Introduction
This is a digital implementation of the classic murder mystery board game Cluedo (Clue).
There are many versions of this game, so I decided to to use the 1949 version to inform my
implementation. I referenced the wiki (https://cluedo.fandom.com/wiki/Cluedo_1949) for
to get information on that version.

## Modifications
Some important modifications to the game have been made to the board layout/movement.
In the original, the board is a set of tiles and rooms, in this implementation, the
board is just the rooms. Furthermore, in the original, the characters started outside
the rooms, in this implementation the players start in a randomly selected room. 
See game_board_comparison.png to see a comparison.

## Source code
The entire source code is in the folder AbanobTanous_Project2_SourceCode/cluedo/

## Requirements
Python 3.13
pygame 2.6

## How to run
pip install pygame
cd cluedo
python main.py