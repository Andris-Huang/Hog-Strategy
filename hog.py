"""CS 61A Presents The Game of Hog.""" 

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
    k = 1
    total = 0
    stop = False
    while k <= num_rolls:
        a = dice()
        if a == 1:
            stop = True
        else:
            total += a 
        k += 1
    if stop:
        return 1
    else:
        return total
    

    # END PROBLEM 1


def piggy_points(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    """
    # BEGIN PROBLEM 2
    score_squared = score ** 2
    last_digit_1 = score_squared % 10
    minimum = last_digit_1
    while score_squared >= 10:
        last_digit = score_squared //10 % 10
        if last_digit < minimum:
            minimum = last_digit
        score_squared = score_squared // 10
    return minimum + 3
        
        

    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Piggy Points.
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
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return piggy_points(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def more_boar(player_score, opponent_score):
    """Return whether the player gets an extra turn.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> more_boar(21, 43)
    True
    >>> more_boar(22, 43)
    True
    >>> more_boar(43, 21)
    False
    >>> more_boar(12, 12)
    False
    >>> more_boar(7, 8)
    False
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    def comparison(a):
        while a > 99:
            a = a // 10
        return a
    b = comparison(player_score) 
    c = comparison(opponent_score) 
    return (b // 10) < (c // 10) and (b % 10) < (c % 10)
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
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    #roll_dice(num_rolls, dice=six_sided)
    b = True
    while b:
        flip_role = False
        c = True
        while c:
            if who == 1:
                flip_role = True
                score0, score1 = score1, score0
                strategy0, strategy1 = strategy1, strategy0
            score0 += take_turn(strategy0(score0, score1), score1, dice, goal)
            c = more_boar(score0, score1)
            if flip_role:
                score0, score1 = score1, score0
                strategy0, strategy1 = strategy1, strategy0
            say = say(score0, score1)
            if score0 >= goal or score1 >= goal: 
                b = False
                break
        who = next_player(who)

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

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

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

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    Player 1 has reached a new maximum point gain. 9 point(s)!
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    Player 1 has reached a new maximum point gain. 21 point(s)!
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    Player 1 has reached a new maximum point gain. 30 point(s)!
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def say(score0, score1):
        last = last_score
        high = running_high
        if who:
            gain = score1 - last
            last = score1
        else:
            gain = score0 - last_score
            last = score0
        if gain > high:
            print("Player " + str(who) + " has reached a new maximum point gain. " + str(gain) + " point(s)!")
            high = gain
        return announce_highest(who, last, high)
    return say
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
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def func(*args):
        total = 0
        i = 0
        while i < trials_count:
            total += original_function(*args)
            i += 1
        return total / trials_count

    return func
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
    "*** YOUR CODE HERE ***"
    sum1 = 0
    k = 0
    while k < trials_count:
        sum1 += roll_dice(1, dice)
        k += 1
    score = sum1 / trials_count
    highest = 1

    i = 2
    while i <= 10:
        total = 0
        j = 0
        while j < trials_count:
            total += roll_dice(i, dice)
            j += 1
        total /= trials_count
        if score < total:
            score = total
            highest = i
        i += 1
    
    return highest
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
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))

    #print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
    #print('piggypoints_strategy win rate:', average_win_rate(piggypoints_strategy))
    #print('more_boar_strategy win rate:', average_win_rate(more_boar_strategy))
    #print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def piggypoints_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if piggy_points(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 10


def more_boar_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    new_score = score + piggy_points(opponent_score)
    if piggypoints_strategy(score, opponent_score, cutoff, num_rolls) == 0 or more_boar(new_score, opponent_score):
        return 0
    else:
        return num_rolls # Replace this statement
    # END PROBLEM 11



from dice import six_sided, four_sided, make_test_dice, make_fair_dice
from ucb import main, trace, interact
import numpy as np
from collections import defaultdict

eight_sided = make_fair_dice(8)

def time_trot(n, k):
    if k> 0 and n % k == 8:
        return True
    return False

class HogMove(object):
    def __init__(self, num_rolls, who):
        self.num_rolls = num_rolls
        self.who = who


class HogState(object):
    def __init__(self, state, num_rolls, turn, next_to_move=1, extra_turn=0):
        self.self_score = state[0]
        self.opp_score = state[1]
        self.num_rolls = num_rolls
        self.turn = turn
        self.next_to_move = next_to_move
        self.extra_turn = extra_turn

    @property
    def game_result(self):
        # check if game is over

        if self.self_score >= 100:
            return 1.
        elif self.opp_score >= 100:
            return -1.
        else:
            # if not over - no result
            return None

    def is_game_over(self):
        return self.game_result != None

    def is_move_legal(self, move):
        return True

    def move(self, move):
        def roll(num, extra):
            if extra < 1:
                return roll_dice(num, six_sided)
            else:
                return roll_dice(num, eight_sided)
        
        extra = self.extra_turn

        if move.num_rolls == 0:
            if move.who == 1:
                new_score = [self.self_score + piggy_points(self.opp_score), self.opp_score]
            else:
                new_score = [self.self_score, self.opp_score + piggy_points(self.self_score)]
        else:
            if move.who == 1:
                new_score = [self.self_score + roll(move.num_rolls, extra), self.opp_score]
            else:
                new_score = [self.self_score, self.opp_score + roll(move.num_rolls, extra)]
        
        if extra < 1 and time_trot(self.turn, move.num_rolls):
            self.next_to_move = self.next_to_move
            extra += 1
        
        elif more_boar(self.self_score, self.opp_score):
            self.next_to_move = self.next_to_move
            extra += 1

        else:
            self.next_to_move = -1 * self.next_to_move
            extra = 0    
        
        new_turn = self.turn + 1

        return HogState(new_score, move.num_rolls, new_turn, self.next_to_move, extra)

    def get_legal_actions(self):
        return [HogMove(i, self.next_to_move) for i in range(11)]

class MonteCarloTreeSearchNode(object):
    def __init__(self, state: HogState, parent=None):
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            c.q
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

class MonteCarloTreeSearch(object):
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param=1.4)

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

def final_strategy(score, opponent_score):
    """
    This strategy adapts the method of Monte Carlo Tree Search (MCTS). The MCTS algorithm follows four steps: Selection,
    Expansion, Simulation, and Backpropagation. In my understanding, it simulates all the possible children of the 
    root and picks the best best child based on statistics modeled by the following equation:
    
        UCT(vi, v) = Q(vi)/N(vi) + c * sqrt(log(Nv)/N(vi)),
    
    where the c parameter used in this code is sqrt(2) = 1.4.

    Acknowledgement:
        Although I do not have any other collaborator, the theory behind MCTS is definitely beyond my current scope.
    The introduction to the algorithm and some instructions for implementation were found from int8.io, and I was
    also inspired by the MCTS on Tic Tac Toe, implemented by int8.
    """
    global turn
    turn = 1
    if score == 0 and opponent_score == 0:
        turn += 1
        return 6
    initial_state = HogState(state=[score, opponent_score], num_rolls=6, turn=turn)
    root = MonteCarloTreeSearchNode(state=initial_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(10)
    c_state = best_node.state
    num = c_state.num_rolls
    turn += c_state.turn

    return num

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
