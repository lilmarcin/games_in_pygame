# Pygame Projects

This repository contains projects created using the Pygame library. 

## Installation

To install the project dependencies, run:

```bash
pip install -r requirements.txt
```

## List of projects
### Adding/Removing Balls

The program involves generating a single ball that bounces off the screen edges. Upon collision, the ball has a 25% chance of generating a new ball and a 25% chance of removing itself. Explore whether there's a higher chance (theoretically) of filling the entire screen with balls or clearing all the balls from the screen.

- Example Video
![Adding/Removing Balls](/images/adding_removing_balls.gif)

### Ball Race

In this project, balls race on a map with obstacles (more maps to be added in the future). The winner is the ball that reaches the finish line first (green area).

- Example Video
![Ball Race](/images/ball_race_1.gif)

### Galton Board 
This project simulates a Galton Board, which is a board with nails arranged in a triangular pattern. Balls falling from the top bounce off the nails in different directions, with a 50% chance of bouncing left or right. As a result, the final position of the balls is entirely random.

Balls entering individual compartments under the board create a histogram resembling a binomial distribution, nearly equal to a normal distribution (exact for an infinite number of infinitely small balls and infinitely many compartments). The Galton Board illustrates the natural formation of a normal distribution due to small random deviations.
- file `galton_board.py` uses Pymunk to create space
- file `galton_board_edit.py` uses own gravity and collisions to create space

- Example Video
![Galton_board](/images/galton_board_pymunk.gif)

## Usage
Run each project via command
```bash
python -u path_to_file.py
```
e.g.
```bash
python -u galton_board.py
```

## License

This project is licensed under the MIT License.

