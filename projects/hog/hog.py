"""CS 61A Presents The Game of Hog."""

from tkinter import W
from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    count, sum = 0, 0
    sow_sad = False
    # roll num_rolls times
    while count < num_rolls:
        dice_num = dice()
        if dice_num == 1:
            sow_sad = True
        count += 1
        sum += dice_num
    # check if happened "sow sad"
    if sow_sad:
        sum = 1
    return sum
    # END PROBLEM 1


def picky_piggy(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    """
    # BEGIN PROBLEM 2
    REPEATING_DIGITS = 6   # 1/7 is 6-digit repeating decimal
    real_digit = score % REPEATING_DIGITS
    # if is 6th digit, pts is same as 0th(score == 0)
    if real_digit == 0:
        real_digit = 6
    dividend, divisor, quotient = 1, 7, 0
    while real_digit > 0:
        dividend *= 10
        quotient = dividend // divisor
        dividend -= quotient * divisor
        real_digit -= 1
    return quotient

    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Picky Piggy.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        pts = picky_piggy(opponent_score)
    else:
        pts = roll_dice(num_rolls, dice)
    return pts
    # END PROBLEM 3


def hog_pile(player_score, opponent_score):
    """Return the points scored by player due to Hog Pile.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 4
    bonus_point = 0
    if player_score == opponent_score:
        bonus_point = player_score
    return bonus_point
    # END PROBLEM 4


def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    def have_winner():
        return score0 >= goal or score1 >= goal

    def calc_pts(score, opponent, rolls):
        score += take_turn(rolls, opponent, dice, goal)
        score += hog_pile(score, opponent)
        return score

    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while not have_winner():
        if who == 0:
            score0 = calc_pts(score0, score1, strategy0(score0, score1))
        else:
            score1 = calc_pts(score1, score0, strategy1(score1, score0))
        who = next_player(who)
        say = say(score0, score1)
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! That's a record gain for Player 1!
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! That's a record gain for Player 1!
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! That's a record gain for Player 1!
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7

    def say_highest(score0, score1):
        score = score0 if who == 0 else score1
        gain = score - last_score
        if gain > running_high:
            print(f'{gain} point(s)! That\'s a record gain for Player {who}!')
        return announce_highest(who, score, max(gain, running_high))

    return say_highest
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TRIALS_COUNT times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    # BEGIN PROBLEM 8
    
    def calc_average(*args):
        """Calculate the average value of ORIGINAL_FUNCTION called TRIALS_COUNT times
        and also pass the arguments in this function into ORIGINAL_FUNCTION
        """
        count, sum = 0, 0
        while count < trials_count:
            count += 1
            sum += original_function(*args)
        return sum / count

    return calc_average
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    BEGIN, END = 1, 10
    count = BEGIN
    best_num, max_score = -1, -1
    average_dice = make_averaged(roll_dice, trials_count)

    while count <= END:
        score = average_dice(count, dice)
        if score > max_score:
            best_num = count
            max_score = score
        count += 1

    return best_num
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    TRIALS_COUNT = 100000
    six_sided_max = max_scoring_num_rolls(six_sided, TRIALS_COUNT)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    for i in range(1, 11):
        print(f'always_roll({i}) win rate:', average_win_rate(always_roll(i)))
        print(f'with its score:', make_averaged(roll_dice)(i))
    print('picky_piggy_strategy win rate:', average_win_rate(picky_piggy_strategy))
    print('hog_pile_strategy win rate:', average_win_rate(hog_pile_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def picky_piggy_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least CUTOFF points, and
    returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if picky_piggy(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


def hog_pile_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Hog Pile taking
    effect. It also returns 0 dice if it gives at least CUTOFF points.
    Otherwise, it returns NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    gain = picky_piggy(opponent_score)
    if hog_pile(score + gain, opponent_score):
        return 0
    elif gain >= cutoff:
        return 0
    else:
        return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Choose the best strategy for each step, based on which strategy has the better score for each step.
    prevent the risks as well.
        *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    NUM_ROLLS = 6
    AVERAGE_GAIN = 8   # average score for the 'always 5/6' strategy with the highest average win rate
    gain = hog_pile_strategy(score, opponent_score, cutoff= AVERAGE_GAIN, num_rolls= NUM_ROLLS)
    return 6
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
