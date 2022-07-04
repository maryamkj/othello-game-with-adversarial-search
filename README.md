<h1 align="center" , class = "#top">
  <br>
    Othello Game
  <br>
  <br>
</h1>

<h4 align="center">This is an artificial intelligence agent that you can play with in 3 easy, medium, and hard levels.<br><br></h4>

<p align="center">
  <a href="#what-is-othello">What is othello?</a> •
  <a href="#getting-started">Getting started</a> •
  <a href="#algorithm">Algorithm</a> •
  <a href="#heuristic-function">Heuristic function</a> •
  <a href="#acknowledgments">Acknowledgments</a> •
  <a href="#author-info">Author Info</a>
</p>

![how to play](https://github.com/maryamkj/othello-game-with-adversarial-search/blob/main/app/readme_gif/how%20to%20play.gif)
<br></br>
> ## What is othello?
<br></br>
Othello is a two player boardgame, played on an 8×8 uncheckered board.
<br>
Players take turns placing disks on the board with their assigned color facing up. During a play, any disks of the opponent's color that are in a straight line and bounded by the disk just placed and another disk of the current player's color are turned over to the current player's color. The objective of the game is to have the majority of disks turned to display one's color when the last playable empty square is filled.
<br> 
for more information on what is otello and how to play it click on [this link](https://board-games-galore.fandom.com/wiki/Othello) 
<br></br>
> ## Getting started
<br></br>
<p>Here we discuss how you can run the program and start playing with it in two ways.</p>
1. Clone the repository 

&emsp;
<tab>You can simply clone the repository and run main.py in your compiler.
<br>
2.  Run the program on google Colaboratory
<br>
&emsp;
<tab>The second way to play othello with this intelligent agent is to run the source code on google Colaboratory.
For doing that click on [google-golab-main-file.ipynb](https://github.com/maryamkj/othello-game-with-adversarial-search/blob/main/google-golab-main-file.ipynb) in the above list, and then click on Open in Colab badge.
<br></br>
> ## Algorithm
<br></br>
The [adversarial search algorithm](https://cs.lmu.edu/~ray/notes/asearch/) is used to select the move in each step, the heuristic function is used to determine the game strategy which is described in detail [here](#algorithm).<br>
Also, in order to avoid useless processes, pruning algorithm has been used, which you can read more about in [this link](https://www.javatpoint.com/ai-alpha-beta-pruning).
<br></br>
> ## Heuristic function
<br></br>
The heuristic function is a way to inform the search about the direction to a goal. It provides an informed way to guess which neighbor of a node will lead to a goal. 
<p>To calculate the value of the h function in this game, we need three constant coefficients.</p>
1. The first quantity indicates the number of pieces belonging to the player. We know that at the end of the game, the number of pieces of each player who is more is the winner of the game, so in the strategy of the game, the number of pieces should be taken into account to choose each action, the weight of each piece is considered 0.1 .
<p></p>
2. The next quantity indicates the number of moves that the player can make in one state, the bigger this number is, the more open our hand is to make a better move, the weight of each action is 1.
<p></p>
3. The last quantity indicates the important positions on the boeard game that in this game the four corners of the field have been selected, because the first time these cells belong to a player, their color will not return. The weight of each important position is considered 5.
<p></p>
<br>

![heuristic evaluation](https://github.com/maryamkj/othello-game-with-adversarial-search/blob/main/app/readme%20heuristic%20function/heuristic_evaluation.png)

From the sum of the 3 quantities explained in their coefficients, we can get an estimate of the effectiveness of each action so that we can make an intelligent choice.

<br></br>
> ## Acknowledgments
<br></br>
The credit for the design and implementation of this project belongs entirely to [Nika Shahabi](https://github.com/nikashahabi), I am honored that I was given the opportunity to optimize and improve this project.
<br></br>
> ## Author info
- Email - kashanijoumaryam@gmail.com
- LinkedIn - [Maryam Kashani jou](https://www.linkedin.com/in/maryam-kashani-jou/)
- Telegram id - [@marii_kj](https://t.me/Marii_kj)

