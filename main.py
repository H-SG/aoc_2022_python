import copy
import math
from statistics import mean
from typing import Optional
from itertools import pairwise, combinations
from dataclasses import dataclass

# a constant to keep mypy happy for day 12
BIG_DISTANCE: int = 10_000

# constant for day 15
MAX_DISTANCE: int = 4_000_000

def read_to_array(path: str, strip: bool = True) -> list[str]:
    with open(path) as f:
        lines: list[str] = f.readlines()

    # let's always clean up
    if strip:
        return [x.strip() for x in lines]
    else:
        return lines

def read_to_2d_array(path: str) -> list[list[str]]:
    raw_array: list[str] = read_to_array(path)

    return [[y for y in x] for x in raw_array]

def day_1() -> None:
    # i'm certain there is a more efficient way of doing this, but
    # this is what came up this morning in my meatbrain
    # edit: i made it better
    calory_list: list[int] = [0]
    with open('data/day1.txt') as f:
        for line in f:
            if line == "\n":
                calory_list.append(0)
            else:
                calory_list[-1] += int(line)

    calory_list.sort()
    print(f"Day 1.1: The elf carrying the most calories is carrying {calory_list[-1]} calories")
    print(f"Day 1.2: The three elves carrying the most calories are carrying {sum(calory_list[-3:])} calories")

def day_2() -> None:
    # open sesame
    with open('data/day2.txt') as f:
        lines: list[str] = f.readlines()

    # p a t t e r n s
    def rps_score_1(round: str) -> int:
        match round.split(" "):
            case ["A", "Y"]:
                return 8
            case ["B", "Z"]:
                return 9
            case ["C", "X"]:
                return 7
            case ["A", "X"]:
                return 4
            case ["B", "Y"]:
                return 5
            case ["C", "Z"]:
                return 6
            case [_, "X"]:
                return 1
            case [_, "Y"]:
                return 2
            case [_, "Z"]:
                return 3
        return 0

    def rps_score_2(round: str) -> int:
        match round.split(" "):
            case ["A", "X"]:
                return 3
            case ["A", "Y"]:
                return 4
            case ["A", "Z"]:
                return 8
            case ["B", "X"]:
                return 1
            case ["B", "Y"]:
                return  5
            case ["B", "Z"]:
                return 9
            case ["C", "X"]:
                return 2
            case ["C", "Y"]:
                return 6
            case ["C", "Z"]:
                return 7
        return 0

    # scoring loop, could use apply here with numpy, or pandas?
    score_1 = 0
    score_2 = 0
    for line in lines:
        score_1 += rps_score_1(line.strip("\n"))
        score_2 += rps_score_2(line.strip("\n"))

    print(f"Day 2.1: The score when following the assumed strategy guide is {score_1}")
    print(f"Day 2.2: The score when following the true strategy guide is {score_2}")

def day_3() -> None:
    # three days, three challenges, all needing things in an array
    # so let's make a function
    rucksacks: list[str] = read_to_array("data/day3.txt")
    rucksacks = [x.strip("\n") for x in rucksacks]

    # split the string into compartments
    rucksacks_compartments = [[x[:len(x)//2], x[len(x)//2:]] for x in rucksacks]

    # check if any item in the first compartment is in the second
    common_items: list[int] = []
    for rucksack_compartments in rucksacks_compartments:
        comp1: str = rucksack_compartments[0]
        comp2: str = rucksack_compartments[1]
        for letter in comp1:
            if letter in comp2:
                # turns out there is more than one item sometimes, so we need to break here
                common_items.append(ord(letter))
                break

    # some tricks with ascii
    common_items_priority: list[int] = [x - 96 if x > 91 else x - 38 for x in common_items]

    print(f"Day 3.1: Sum of priorities in common item types is {sum(common_items_priority)}")
    
    # strings to kinda chars
    rucksacks_items: list[list[str]] = [[y for y in x] for x in rucksacks]

    # sets and intersections
    badges: list[str] = []
    for i in range(0, len(rucksacks_items), 3):
        com1: set[str] = set(rucksacks_items[i]).intersection(rucksacks_items[i + 1])
        badges.append(list(com1.intersection(rucksacks_items[i + 2]))[0])

    # moar ascii schenaningans
    badges_priority: list[int] = [ord(x) - 96 if ord(x) > 91 else ord(x) - 38 for x in badges]

    print(f"Day 3.2: Sum of priorities for the badges are {sum(badges_priority)}")

def day_4() -> None:
    # get the assignments
    assignments: list[str] = read_to_array('data/day4.txt')

    # split into elves
    first_elf: list[list[str]] = [x.split(',')[0].split("-") for x in assignments]
    second_elf: list[list[str]] = [x.split(',')[1].split("-") for x in assignments]

    # our counters
    subsets: int = 0
    overlapping: int = 0

    # loop time
    for fe, se in zip(first_elf, second_elf):
        # make ints, mypy doesn't like if i reuse fe and se, i guess this is better
        # practice
        fe_i: list[int] = [int(x) for x in fe]
        se_i: list[int] = [int(x) for x in se]

        # sanity check while i failed to get the right answer
        assert fe_i[1] - fe_i[0] >= 0
        assert se_i[1] - se_i[0] >= 0

        # did this with nested ifs first, nasty, brutish
        if (fe_i[0] >= se_i[0]) and (fe_i[1] <= se_i[1]):
            subsets += 1
        elif (se_i[0] >= fe_i[0]) and (se_i[1] <= fe_i[1]):
            subsets += 1

        # using sets a lot, get those intersections
        fe_areas: set[int] = set(range(fe_i[0], fe_i[1] + 1))
        se_areas: set[int] = set(range(se_i[0], se_i[1] + 1))

        if len(fe_areas.intersection(se_areas)) > 0:
            overlapping += 1

    print(f"Day 4.1: Number of overlapping rosters are {subsets}")
    print(f"Day 4.2: Number of overlapped assignments are {overlapping}")

def day_5() -> None:
    # get our inputs
    raw_inputs: list[str] = read_to_array('data/day5.txt', False)

    # get index of where instructions and data split
    for i, raw_input in enumerate(raw_inputs):
        if len(raw_input) == 1:
            split_index = i
            break
    else:
        raise ValueError

    # our stacks and instructions
    stacks: list[str] = raw_inputs[:split_index - 1]
    instructions: list[str] = [x.strip() for x in raw_inputs[split_index + 1:]]

    # want to transpose the stacks
    t_stacks_9000: list[list[str]] = []

    # this does the actual transposition
    for i, row in enumerate(stacks):
        # honestly this is ugly as heck
        crow: str = row.strip('\n').replace("    ", "None ").replace("]N", "] N").replace("  ", " ")
        cols: list[str] = [x.strip() for x in crow.split(" ")]
        for j, col in  enumerate(cols):
            # 9 is a magic number, sorry
            if j == 9:
                continue
            if i == 0:
                t_stacks_9000.append([])

            if col != 'None':
                t_stacks_9000[j].append(col[1])

    # need to flip around the stacks to work on the end of the list
    t_stacks_9000 = [list(reversed(x)) for x in t_stacks_9000]
    t_stacks_9001 = copy.deepcopy(t_stacks_9000)

    # parse through the instructions
    for instruction in instructions:
        sub_instructions: list[str] = instruction.split(" ")

        num_move: int = int(sub_instructions[1])
        origin: int = int(sub_instructions[3]) - 1
        destination: int = int(sub_instructions[5]) - 1

        # part 1
        to_move = list(reversed(t_stacks_9000[origin][-num_move:]))
        t_stacks_9000[origin] = t_stacks_9000[origin][:-num_move]
        t_stacks_9000[destination] += to_move

        # part 2
        to_move = t_stacks_9001[origin][-num_move:]
        t_stacks_9001[origin] = t_stacks_9001[origin][:-num_move]
        t_stacks_9001[destination] += to_move

    # make our top of crate string
    end_string_9000: str = "".join([x[-1] for x in t_stacks_9000])
    end_string_9001: str = "".join([x[-1] for x in t_stacks_9001])

    print(f'Day 5.1: The top of crates string is {end_string_9000}')
    print(f'Day 5.2: The top of crates string is {end_string_9001}')

def day_6() -> None:
    # our input is one long string
    stream: str = read_to_array('data/day6.txt')[0]

    # a nice little function  which does the things
    def first_unique_substring(stream: str, substring_len: int) -> int:
        for i in range(0, len(stream)):
            substring: str = stream[i:i+substring_len]

            substring_chars: list[str] = [x for x in substring]

            # sets babey
            if len(set(substring_chars)) == substring_len:
                return i + substring_len
        else:
            raise ValueError

    part_1_index: int = first_unique_substring(stream, 4)
    part_2_index: int = first_unique_substring(stream, 14)

    print(f"Day 6.1: The first start of packet marker is at {part_1_index}")
    print(f"Day 6.2: The first start of message marker is at {part_2_index}")

# this class is for day 7
class Directory:
    # some of these properties are likely redundant, but just in case...
    def __init__(self, path):
        self.path = path
        self.files = []
        self.dirs = []
        self.file_sizes = {}
        self.parent = None
        self.children = {}
        self.parsed = False
        self.size = 0
        self.files_only_size = 0

def day_7() -> None:
    # get all the terminal history
    commands: list[str] = read_to_array('data/day7.txt')

    # the start of our solution outputs
    sub_100000_sum: int = 0
    dir_size_dict: dict[str, int] = {}

    # since the commands causally linked, we can just step through them and build a directory tree
    current_path: str = ""
    current_dir: Directory
    root_dir: Directory
    for command in commands:
        match command.split(" "):
            # if we move up, we are 100% done with the folder
            case ["$", "cd", ".."]:
                dir_size_dict[current_path] = current_dir.size
                current_path = f'{"/".join(current_path.split("/")[:-2])}/'
                current_dir.parsed = True
                current_dir.parent.size += current_dir.size
                if current_dir.size <= 100000:
                    sub_100000_sum += current_dir.size
                current_dir = current_dir.parent
            # if we go into a new folder, we have to create it in the tree/graph
            case ["$", "cd", folder]:
                # special case for creating root tree
                if current_path != "":
                    current_path += f"{folder}/"
                    current_dir.children[current_path] = Directory(current_path)
                    current_dir.children[current_path].parent = current_dir
                    current_dir = current_dir.children[current_path]
                else:
                    current_path = folder
                    root_dir = Directory(current_path)
                    current_dir = root_dir
            # we do nothing when files are listed
            case ["$", "ls"]:
                pass
            # add it to the list, we'll get to it
            case ["dir", folder]:
                current_dir.dirs.append(folder)
            # get all the sizes!
            case [size, file]:
                current_dir.files.append(file)
                current_dir.file_sizes[file] = int(size)
                current_dir.size += int(size)
                current_dir.files_only_size += int(size)

    # the commands don't traverse back to root, so the last folder path won't have sizes
    # summed back to root, this is a copy of the case ["$", "cd", ".."], best practice
    # would've been to refactor this out to a function in case of errors, but lazy
    while (current_path != '/'):
        dir_size_dict[current_path] = current_dir.size
        current_path = f'{"/".join(current_path.split("/")[:-2])}/'
        current_dir.parsed = True
        current_dir.parent.size += current_dir.size
        if current_dir.size <= 100000:
                    sub_100000_sum += current_dir.size
        current_dir = current_dir.parent

    print(f"Day 7.1: The sum size of all folders smaller than 100000 is {sub_100000_sum}")

    # all magic numbers courtesy of the elves
    free_space: int = 70000000 - root_dir.size
    space_needed: int = 30000000 - free_space

    # i guess this is unneeded, could just store the sizes
    deletion_candidates: dict[str, int] = {k:v for k, v in dir_size_dict.items() if v >= space_needed}
    sorted_delection_candidates: dict[str, int] = dict(sorted(deletion_candidates.items(), key=lambda item: item[1]))
    
    print(f"Day 7.2: The smallest directory to be deleted is {list(sorted_delection_candidates.keys())[0]} with size {list(sorted_delection_candidates.values())[0]}")

def day_8() -> None:
    # our trees
    tree_map: list[str] = read_to_array('data/day8.txt')

    # the scope of our map
    cols: int = len(tree_map[0])
    rows: int = len(tree_map)
    best_tree_score: int = 0

    # make a map of trees that are visible
    visible_tree_map: list[list[bool]] = [[False for _ in range(cols)] for _ in range(rows)]

    # not sure if I could handle this in the next loop, but let's just make the edges visble
    for i in range(cols):
        if (i == 0) or (i == cols - 1):
            visible_tree_map[i] = [True for _ in range(rows)]

        visible_tree_map[i][0] = True
        visible_tree_map[i][-1] = True

    # check each tree for visibility
    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            current_tree_value: int = int(tree_map[y][x])

            # some of these reversed lists are a key tool which will help us later ;)
            left_to_right: list[int] = list(reversed([int(c) for c in tree_map[y][:x + 1]]))
            right_to_left: list[int] = [int(c) for c in tree_map[y][x:]]
            top_to_bottom: list[int] = list(reversed([int(r[x]) for r in tree_map[:y + 1]]))
            bottom_to_top: list[int] = [int(r[x]) for r in tree_map[y:]]

            # check if the tree is visible and calculate it's view score
            viewing_sub_score = 1
            for check_direction in [left_to_right, right_to_left, top_to_bottom, bottom_to_top]:
                if all([current_tree_value > c for c in check_direction[1:]]):
                    visible_tree_map[y][x] = True

                
                for i, tree in enumerate(check_direction[1:]):
                    if tree >= current_tree_value:
                        viewing_sub_score *= i + 1
                        break
                else:
                    viewing_sub_score *= len(check_direction[1:])

            # check if we have a new winrar
            best_tree_score = max(best_tree_score, viewing_sub_score)

    # count the number of visible trees
    visible_trees = sum([sum(x) for x in visible_tree_map])

    print(f'Day 8.1: The number of visible trees are {visible_trees}')
    print(f'Day 8.2: The tree with the best score has a score of {best_tree_score}')

# class for day 9
class Pos:
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    # need this for set
    def __hash__(self) -> int:
        return hash(f"{self.x=}, {self.y=}")

    # need this for set
    def __eq__(self, other) -> bool:
        return isinstance(other, Pos) and self.x == other.x and self.y == other.y
    
    # little helper function for getting the offset of a different point compared to this one
    def pos_delta(self, other) -> tuple[int, int]:
        return other.x - self.x, other.y - self.y

def day_9(knot_num: int, day_indicator: str) -> None:
    # get our steps, for the first time we have a parameter, the number of knots
    # in our rope (including head and tail)
    head_steps = read_to_array('data/day9.txt')

    # make our starting position of knots, and put the tail position in thar
    knots: list[Pos] = [Pos(0, 0) for _ in range(knot_num)]
    tail_posses: list[Pos] = [Pos(0, 0)]

    # function which makes the tail move according to the head
    # technically the while loop is not needed in the current implementation
    # but for the case of just two knots, it was a useful simplification...
    # y'know, this could've been a function in the class itself
    def tail_follow(tail: Pos, head: Pos, log_tail: bool = False) -> None:
        dx, dy = tail.pos_delta(head)
        while ((abs(dx) > 1) or (abs(dy) > 1)):
            if (abs(dx) > 0) and (abs(dy) > 0):
                if (dx == 1) and (dy == 1):
                    break
                tail.y += dy//abs(dy)
                tail.x += dx//abs(dx)
            elif abs(dx) > 1:
                tail.x += dx//abs(dx)
            elif abs(dy) > 1:
                tail.y += dy//abs(dy)
            if log_tail:
                tail_posses.append(copy.deepcopy(tail))
            dx, dy = tail.pos_delta(head)

    # helper function for iteration through all knots in a list and updating them
    # to the knot ahead of it
    def iter_knots(knots: list[Pos]) -> None:
        for j, knot in enumerate(knots[1:]):
                    tail_follow(knot, knots[j])

        tail_posses.append(copy.deepcopy(knots[-1]))

    # step through our steps
    for step in head_steps:
        dy: int = 0
        dx: int = 0
        match step.split(" "):
            # in what direction is the head going
            case ['U', mag]:
                dy = int(mag)
            case ['D', mag]:
                dy = -int(mag)
            case ['L', mag]:
                dx = -int(mag)
            case ['R', mag]:
                dx = int(mag)

        # update the head iteratively for the multi-knot scenario and all trailing knots
        if dy != 0:
            for _ in range(abs(dy)):
                knots[0].y += dy//abs(dy)
                iter_knots(knots)
        if dx != 0:
            for _ in range(abs(dx)):
                knots[0].x += dx//abs(dx)
                iter_knots(knots)

    # get our results
    print(f"{day_indicator} The tail covers {len(set(tail_posses))} unique positions with {knot_num} knots")

def day_10() -> None:
    # get our instructions
    instructions = read_to_array('data/day10.txt')

    # cpu state
    cycle: int = 1
    X: int = 1

    # part 1 vars
    sum_strengths: int = 0
    check_signal: list[int] = [20, 60, 100, 140, 180, 220]

    # part 2 crt
    crt_screen: list[list[str]] = [['⬛' for _ in range(40)] for _ in range(6)]

    # pixel drawing helper
    def draw_pixel(cycle: int, x_val: int, crt: list[list[str]]) -> None:
        # get our current drawing pos
        ref_cycle: int = cycle - 1
        cur_row: int = int(math.floor(ref_cycle / 40))
        cur_row = cur_row % 6
        cur_col: int = ref_cycle % 40

        # get our valid sprite positions
        sprite_pos = [x_val - 1, x_val, x_val + 1]

        # if beam is on valid sprite pos, draw
        if cur_col in sprite_pos:
            crt[cur_row][cur_col] = '🟦'

    # signal checking helper
    def check_signal_val(cycle: int) -> int:
        if cycle in check_signal:
            return cycle * X
        return 0            

    # while we have instructions, work through them
    while (len(instructions) > 0):
        # pattern matching
        match instructions[0].split(" "):
            # order within the cases is quite important
            case ['noop']:
                draw_pixel(cycle, X, crt_screen)
                cycle += 1
                sum_strengths += check_signal_val(cycle)
            case ['addx', val]:
                draw_pixel(cycle, X, crt_screen)
                cycle += 1
                sum_strengths += check_signal_val(cycle)
                draw_pixel(cycle, X, crt_screen)
                cycle += 1
                X += int(val)
                sum_strengths += check_signal_val(cycle)

        # discard previous instruction
        instructions = instructions[1:]

    # draw results
    print(f"Day 10.1: The sum of the six signal strengths is {sum_strengths}")
    print(f"Day 10.2:")
    for row in crt_screen:
        print("".join(row))

# our monkey class
class Monkeys:
    def __init__(self) -> None:
        self.items: list[int]
        self.operation: str
        self.test_modulo: int
        self.true_recip: int
        self.false_recip: int
        self.items_inspected = 0
        self.worry = 3
    
    # little helper to inspect an item
    def inspect_item(self, item: int) -> int:
        new_val: int = self.do_operation(item)
        if self.worry == 3:
            item = math.floor(new_val / self.worry)
        else:
            # look at readme for why this works
            item = new_val % self.worry
        self.items_inspected += 1
        return item

    # littler helper to do operation on the item in question
    def do_operation(self, item: int) -> int:
        match self.operation.split(" "):
            case ['+', val]:
                return item + int(val)
            case ['*', val]:
                if val == 'old':
                    return item * item
                else:
                    return item * int(val)
        raise ValueError

    # little helper to test our item and tell us where to put it
    def test_item(self, item: int) -> tuple[int, int]:
        self.items.remove(item)
        if item % self.test_modulo == 0:
            return self.true_recip, item
        else:
            return self.false_recip, item

def day_11(rounds: int, day_indicator: str, worry: bool = True) -> None:
    # get our monkeys
    monkeys_raw = read_to_array('data/day11.txt')

    # make a list of monkeys
    monkeys_list: list[Monkeys] = []

    # parse the monkey data
    for monkeys_raw_line in monkeys_raw:
        match monkeys_raw_line.split(" "):
            case ['Monkey', *_]:
                monkeys_list.append(Monkeys())
            case ['Starting', 'items:', *val]:
                monkeys_list[-1].items = [int(x.strip(",")) for x in val]
            case ['Operation:', *val]:
                ops = val[-2:]
                monkeys_list[-1].operation = " ".join(ops)
            case ['Test:', *val]:
                monkeys_list[-1].test_modulo = int(val[-1])
            case ['If', 'true:', *val]:
                monkeys_list[-1].true_recip = int(val[-1])
            case ['If', 'false:', *val]:
                monkeys_list[-1].false_recip = int(val[-1])

    # handling for part 1 and 2
    if not worry:
        # this is an interesting trick, check readme for more info
        mod_lcm = math.lcm(*[monkey.test_modulo for monkey in monkeys_list])
        for monkey in monkeys_list:
            monkey.worry = mod_lcm

    # go through the rounds!
    for _ in range(rounds):
        for i in range(len(monkeys_list)):
            for _ in range(len(monkeys_list[i].items)):
                new_worry: int = monkeys_list[i].inspect_item(monkeys_list[i].items[0])
                monkeys_list[i].items[0] = new_worry
                new_monkey, new_item = monkeys_list[i].test_item(new_worry)
                monkeys_list[new_monkey].items.append(new_item)
        
    # get our monkey beezknees
    monkey_business: list[int] = [monkey.items_inspected for monkey in monkeys_list]
    monkey_business.sort()
    print(f'{day_indicator} The level of monkey business is {monkey_business[-2] * monkey_business[-1]} after {rounds} rounds')

# class for a map position, a lot of these vars are optional for V I S U A L I S A T I O N
class MapPoint:
    def __init__(self, height_code: str, x: int, y: int) -> None:
        match height_code:
            case 'S':
                height_char = 'a'
            case 'E':
                height_char = 'z'
            case val:
                height_char = val

        self.height_code: int = ord(height_char) - ord('a') + 1
        self.distance_score: int = BIG_DISTANCE
        self.visited: bool = False
        self.char: str = height_code
        self.x: int = x
        self.y: int = y
        self.path_to_here: list[MapPoint] = []
        self.visit_order: int = BIG_DISTANCE

def day_12() -> None:
    # get our inputs, a new function is added to make 2d array of strings
    height_map: list[list[str]] = read_to_2d_array('data/day12.txt')
    
    # our tasty vars
    map_points: list[list[MapPoint]] = [[] for _ in height_map]
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]

    # parse our raw input into MapPoint
    for y, row in enumerate(height_map):
        for x, pos in enumerate(row):
            map_points[y].append(MapPoint(pos, x, y))
            match pos:
                case 'S':
                    start_pos = (x, y)
                case 'E':
                    end_pos = (x, y)

    # function used for debugging when I was derping
    def print_map(map_points: list[list[MapPoint]]) -> None:
        print('map')
        for row in map_points:
            print("".join([f"\033[94m{x.char}\033[0m" if x.visited else f"{x.char}" for x in row]))

    def map_visualisation(map_points: list[list[MapPoint]], last_only: bool = True) -> None:
        # vars
        map_visited: list[list[bool]] = [[False for _ in y] for y in map_points]
        ordered_map_dict: dict[MapPoint, int] = {}

        # make a dict which we can use to get the map points in order that they were parsed
        for map_row in map_points:
            for pos in map_row:
                ordered_map_dict[pos] = pos.visit_order

        
        # sort that into visit order
        ordered_map_dict = {k: v for k, v in sorted(ordered_map_dict.items(), key=lambda item: item[1]) if k.visit_order < BIG_DISTANCE}

        positions: list[MapPoint]
        if last_only:
            positions = [list(ordered_map_dict.keys())[-1]]
        else:
            positions = list(ordered_map_dict.keys())

        for map_pos in positions:
            path_list: list[MapPoint] = map_pos.path_to_here
            map_string: str = ""
            for y, row in enumerate(map_points):
                row_string: str = ""
                for x, pos in enumerate(row):
                    if last_only:
                        map_visited[y][x] = pos.visited
                    if map_visited[y][x] and pos not in path_list:
                        row_string += f"\033[91m{pos.char}\033[0m"
                    elif pos in path_list:
                        row_string += f"\033[92m{pos.char}\033[0m"
                        map_visited[y][x] = True
                    elif pos == map_pos:
                        row_string += f"\033[92m{pos.char}\033[0m"
                        map_visited[y][x] = True
                    else:
                        row_string += f"\033[90m{pos.char}\033[0m"
                map_string += f"{row_string}\n"

        print(map_string[:-1])

    # this could be done recursively, but sunk cost
    # this is the closest i could do to what wikipedia says in djikstra's algo
    # i've always wondered about path finding, and now i know
    def find_path_length(map_points: list[list[MapPoint]], start_pos: tuple[int, int], end_pos: tuple[int, int], shortest_path: bool = False) -> int:
        # this will come in handy for visualisation later
        visit_num: int = 0
        
        # set out starting position
        map_points[start_pos[1]][start_pos[0]].distance_score = 0
        unvisited_points: dict[MapPoint, int] = {map_points[start_pos[1]][start_pos[0]]: map_points[start_pos[1]][start_pos[0]].distance_score}

        # while our end point is not visited, keep searching
        while (map_points[end_pos[1]][end_pos[0]].visited == False):
            # if we run out of unvisited points, we can't reach the end point, so escape early
            if len(unvisited_points) == 0:
                return BIG_DISTANCE

            # set our current point and update it's parameters
            current_pos: MapPoint = list(unvisited_points.keys())[0]
            current_pos.visited = True
            current_pos.visit_order = visit_num
            cur_x: int = current_pos.x
            cur_y: int = current_pos.y
            visit_num += 1

            # remove our current point from the unvisited list, because we are here right now
            del unvisited_points[current_pos]
            
            # special handling for descending to lowest point, here we have no set end_point
            # merely the first position where we are at height a is valid and break out early
            if shortest_path:
                if current_pos.char == 'a':
                    return current_pos.distance_score            

            # if we are at our end point, we can return early            
            if (cur_x == end_pos[0]) and (cur_y == end_pos[1]):
                return(current_pos.distance_score)

            # get our list of neighbours, with bounds validation
            next_points: list[tuple[int, int]] = [(max(cur_x - 1, 0), cur_y),
                                                (min(cur_x + 1, len(map_points[0]) - 1), cur_y),
                                                (cur_x, max(cur_y - 1, 0)),
                                                (cur_x, min(cur_y + 1, len(map_points) - 1))]

            # iterate through our neighbours
            for point in next_points:
                # current neighbour
                next_pos = map_points[point[1]][point[0]]

                # if our neighbour has already been visited, we can ignore it
                if next_pos.visited == True:
                    continue
                
                # special handling for ascending or descending search rules
                if shortest_path:
                    # while descending, only consider the neighbour if one lower or higher
                    if not next_pos.height_code - current_pos.height_code >= -1:
                        continue
                else:
                    # while ascending, only consider the neighbour if less than one higher
                    if not next_pos.height_code - current_pos.height_code <= 1:
                        continue
                
                # add the distance score and set the unvisited points
                next_pos.distance_score = min(next_pos.distance_score, current_pos.distance_score + 1)
                unvisited_points[next_pos] = next_pos.distance_score
                next_pos.path_to_here = current_pos.path_to_here + [current_pos]
                
            # we always want to visit unvisited points in order of shortest path
            unvisited_points = {k: v for k, v in sorted(unvisited_points.items(), key=lambda item: item[1])}
        
        # last hail mary return which we should never face
        return BIG_DISTANCE

    # get our deepcopy maps, cause where we're going shallow copies are king
    # i do miss explicit pointers/rust syntax here
    part_1_map = copy.deepcopy(map_points)
    part_2_map = copy.deepcopy(map_points)

    # our results
    part_1_path = find_path_length(part_1_map, start_pos, end_pos)
    part_2_path = find_path_length(part_2_map, end_pos, start_pos, True)

    print(f"Day 12.1: The shortest path to the signal point is {part_1_path}")
    map_visualisation(part_1_map)
    print(f"Day 12.2: The shortest scenic path to the signal point is {part_2_path}")
    map_visualisation(part_2_map)

def day_13() -> None:
    # get our raw input
    raw_signals: list[str] = read_to_array('data/day13.txt')

    # list for parsing signal pairs
    signal_pairs: list[list[list]] = [[]]
    packets: list[list] = [] # for part 2

    # parse through our raw signals, the use of eval feels... dirty?
    # i'm so sorry
    for raw_signal in raw_signals:
        match raw_signal:
            case "":
                signal_pairs.append([])
            case _:
                signal_pairs[-1].append(eval(raw_signal))
                packets.append(eval(raw_signal))
    
    # our good packets
    good_order_indices: list[int] = []

    # function to compare a packet pair RECURSIVELY, it took me a while to grok this out
    # and to figure out how to handle the none return case nicely, because deep in the 
    # recursion tree we might not be able to make a definitive decision
    def compare_pair(left, right) -> Optional[bool]:
        for l, r in  zip(left, right):
            if isinstance(l, int) and isinstance(r, int):
                if l == r:
                    continue
                return r > l
            
            new_left: list
            new_right: list
            if isinstance(l, list) and isinstance(r, list):
                new_left = l
                new_right = r
            else:
                if isinstance(l, int):
                    new_left = [l]
                    new_right = r
                else:
                    new_left = l
                    new_right = [r]

            result = compare_pair(new_left, new_right)
            if result is not None:
                return result
            else:
                continue

        if len(left) == len(right):
            # we will only ultimately return none of both packets are identical
            return None
        return len(left) < len(right)    

    # work through the signal pairs
    for i, signal_pair in enumerate(signal_pairs):
        left_value: list = signal_pair[0]
        right_value: list = signal_pair[1]

        if compare_pair(left_value, right_value):
            good_order_indices.append(i + 1)

    print(f"Day 13.1: The sum of the pair indices are {sum(good_order_indices)}")

    start_packet = [[2]]
    end_packet = [[6]]

    start_index: int = 1
    end_index: int = 2 # not one since start packet will be inserted before it

    # we don't need to sort the packets, just figure out how many come before 
    # the respective divider packets
    for packet in packets:
        if compare_pair(packet, start_packet):
            start_index += 1

        if compare_pair(packet, end_packet):
            end_index += 1

    print(f'Day 13.2: The decoder key is {start_index * end_index}')

# class for day 14
class CavePoint:
    def __init__(self, x: int, y: int, type: str = '#'):
        self.x = x
        self.y = y
        self.type = type # keeping this here in case I want to make a visualisation

    # need this for set
    def __hash__(self) -> int:
        # thanks to David Fourie for this obvious improvement
        return hash((self.x, self.y))

    # need this for set
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    # function which moves sand until it can move no more
    def sand_motion(self, cave_points: set, deepest_y: int, abyss_floor: bool = False) -> bool:
        # return true if sand stops
        # return false if sand drops into abyss or has not valid path

        # check if there are three points directly below, left, and right of the current item
        # and then move based on that result
        while (self.y < deepest_y):
            # if an existing point is at the sand origin, we're finished
            if self in cave_points:
                return False

            # making these points is time expensive, so only do when absolutely needed
            direct_bottom_point: CavePoint = CavePoint(self.x, self.y + 1)
            if direct_bottom_point in cave_points:
                bottom_left_point: CavePoint = CavePoint(self.x - 1, self.y + 1)
                if bottom_left_point in cave_points:
                    bottom_right_point: CavePoint = CavePoint(self.x + 1, self.y + 1)
                    if bottom_right_point in cave_points:
                        return True
                    else:
                        # move right down and test again
                        self.y += 1
                        self.x += 1
                else:
                    # move left down and test again
                    self.y += 1
                    self.x -= 1
            else:
                # move down and test again
                self.y += 1

        # do the special return for abyss floor, essentially adds a virtual floor
        if abyss_floor:
            self.y -= 1
            return True
        else:
            return False

def day_14() -> None:
    # get our rock paths
    raw_rock_paths: list[str] = read_to_array('data/day14.txt')

    # make our set
    cave_points: set[CavePoint] = set()

    # vars for later
    deepest_y: int = 0
    sand_units: int = 0

    # parse the rock paths to make sets
    for raw_rock_path in raw_rock_paths:
        path_route: list[str] = raw_rock_path.split('->')
        
        for p0, p1 in pairwise(path_route):
            x0: int
            x1: int
            y0: int
            y1: int
            x0, y0 = [int(x) for x in p0.split(',')]
            x1, y1 = [int(x) for x in p1.split(',')]

            deepest_y = max(deepest_y, y0, y1)

            dy: int = y1 - y0
            dx: int = x1 - x0

            if x0 == x1:
                for y in range(y0, y1 + (dy//abs(dy)), dy//abs(dy)):
                    cave_points.add(CavePoint(x0, y))
            else:
                for x in range(x0, x1 + (dx//abs(dx)), dx//abs(dx)):
                    cave_points.add(CavePoint(x, y0))

    current_sand: CavePoint

    # add a grains of sand, move them, until no more grains can be added
    while (True):
        current_sand = CavePoint(500, 0, 'o')

        if current_sand.sand_motion(cave_points, deepest_y):
            cave_points.add(copy.deepcopy(current_sand))
            sand_units += 1
        else:
            break

    print(f"Day 14.1: {sand_units} units of sand come to rest before falling into the abyss")
    
    # we can use our previous cave_points as a starting point for the next part
    deepest_y += 2

    while (True):
        current_sand = CavePoint(500, 0, 'o')

        if current_sand.sand_motion(cave_points, deepest_y, True):
            cave_points.add(copy.deepcopy(current_sand))
            sand_units += 1
        else:
            break

    print(f"Day 14.2: {sand_units} units of sand come to rest")

# created a dataclass for the fast solution to day 15
@dataclass
class SensorPairs:
    sx: int
    sy: int
    bx: int
    by: int

    # post init is a handy thing for dataclasses
    def __post_init__(self):
        self.d = abs(self.sx - self.bx) + abs(self.sy - self.by)

    # checks if an arbitrary point is within the scan area of this sensor pair
    def in_range(self, other: tuple[int, int]) -> bool:
        other_distance: int = abs(self.sx - other[0]) + abs(self.sy - other[1])
        return other_distance <= self.d

    # checks if an arbitrary point is outside the scan area of this sensor pair
    def out_range(self, other: tuple[int, int]) -> bool:
        other_distance: int = abs(self.sx - other[0]) + abs(self.sy - other[1])
        return self.d < other_distance

def day_15() -> None:
    # i may be presumptious in calling this one fast
    raw_sensor_readings: list[str] = read_to_array('data/day15.txt')

    # vars vars vars
    key_row: int = 2_000_000
    sensor_pairs: list[SensorPairs] = []

    # keeping mypy happy
    sensor_x: int
    sensor_y: int
    beacon_x: int
    beacon_y: int
    beacon_set: set[int] = set()
    dy: int
    dx: int

    # how much of x in the key_row have we already covered
    x_ranges: list[list[int]] = []
    final_x_ranges: list[list[int]] = []

    # parse our raw readings into the two lists
    for sensor_reading in raw_sensor_readings:
        split_reading = sensor_reading.split(" ")
        sensor_x = int(split_reading[2].split("=")[1].strip(','))
        sensor_y = int(split_reading[3].split("=")[1].strip(":"))
        beacon_x = int(split_reading[-2].split("=")[1].strip(','))
        beacon_y = int(split_reading[-1].split("=")[1])

        sensor_pairs.append(SensorPairs(sensor_x, sensor_y, beacon_x, beacon_y))
        
        # a tool to help us later
        if beacon_y == key_row:
            beacon_set.add(beacon_x)

        # part 1 we can do right here by logging the ranges of x in the key row covered
        if key_row in range(sensor_y - sensor_pairs[-1].d, sensor_y + sensor_pairs[-1].d + 1):
            dy = abs(key_row - sensor_y)
            dx = sensor_pairs[-1].d - dy
            x0: int = sensor_x - dx
            x1: int = sensor_x + dx
            x_ranges.append([x0, x1])

    # now to collapse all the ranges into a single one as per overlaps and borders
    final_x_ranges.append(list(x_ranges.pop(0)))
    while(len(x_ranges) > 0):
        x_range: list[int] = x_ranges.pop(0)

        for final_x_range in final_x_ranges:
            if x_range[0] in range(final_x_range[0], final_x_range[1] + 2):
                final_x_range[1] = max(x_range[1], final_x_range[1])
                break

            if x_range[1] in range(final_x_range[0] - 1, final_x_range[1] + 1):
                final_x_range[0] = min(x_range[0], final_x_range[0])
                break
        else:
            final_x_ranges.append(list(x_range))

        # i'm taking a risk and assuming all the ranges eventually overlap
        if len(x_ranges) == 0:
            if len(final_x_ranges) == 1:
                break
            x_ranges = copy.deepcopy(final_x_ranges)
            final_x_ranges = [x_ranges.pop(0)]

    key_row_positions: int = (final_x_ranges[0][1] - final_x_ranges[0][0]) + 1

    for bx in beacon_set:
        if bx in range(final_x_ranges[0][0], final_x_ranges[0][1]):
            key_row_positions -= 1

    print(f"Day 15.1: {key_row_positions} positions cannot contain a beacon")

    # part 2 i hope we can do with itertools and some clever thinking
    # basically, we're looking for a combination of four diamonds
    # between them there should be 4 instances of overlapping or touching and 
    # 2 instances of gaps exactly 1 in size
    for four_pairs in combinations(sensor_pairs, 4):
        overlaps: int = 0
        one_gaps: int = 0
        for two_pairs in combinations(four_pairs, 2):
            bsd0 = two_pairs[0]
            bsd1 = two_pairs[1]

            max_distance: int = bsd0.d + bsd1.d + 1
            actual_distance: int = abs(bsd0.sx - bsd1.sx) + abs(bsd0.sy - bsd1.sy)

            if actual_distance <= max_distance:
                overlaps += 1

            if actual_distance == max_distance + 1:
                one_gaps += 1
        
        if overlaps == 4 and one_gaps == 2:
            # we have our pair of four diamonds, now we want to get the smallest one and it's relative
            # position to the rest
            x_list: list[int] = [x.sx for x in four_pairs]
            y_list: list[int] = [x.sy for x in four_pairs]
            distance_list: list[int] = [x.d for x in four_pairs]
            x_list.sort()
            y_list.sort()
            distance_list.sort()

            # we want the smallest, since that will be the fewest potential search iterations
            smallest_diamond: SensorPairs = [x for x in four_pairs if x.d == distance_list[0]][0]

            x_max: int = x_list[2]
            y_max: int = y_list[2]

            # we only need to check the border of one side of the smallest diamond, that which
            # is facing the potential beacon
            check_top: bool = True
            check_left: bool = True

            if smallest_diamond.sy <= y_max:
                check_top = False             
                
            if smallest_diamond.sx <= x_max:
                check_left = False

            # set our y search range + 1 to get the outer border of the diamond
            # any new beacon must lie just beyond the border of existing diamonds
            y_range: list[int] = [smallest_diamond.sy - (smallest_diamond.d + 2), smallest_diamond.sy + (smallest_diamond.d + 2)]

            if check_top == False:
                y_range[0] = smallest_diamond.sy
            else:
                y_range[1] = smallest_diamond.sy

            for y in range(*y_range):
                dy = abs(y - smallest_diamond.sy)
                dx = (smallest_diamond.d + 1) - dy

                # check the one valid edge for a point which is not in any of the other three diamonds
                if check_left:
                    if all(p.out_range((smallest_diamond.sx - dx, y)) for p in four_pairs):
                        print(f"Day 15.2: The tuning frequency is {(smallest_diamond.sx - dx) * 4_000_000 + y}")
                        break
                else:
                    if all(p.out_range((smallest_diamond.sx + dx, y)) for p in four_pairs):
                        print(f"Day 15.2: The tuning frequency is {(smallest_diamond.sx + dx) * 4_000_000 + y}")
                        break                    
            else:
                continue
            break

if __name__ == "__main__":
    # day_1()
    # day_2()
    # day_3()
    # day_4()
    # day_5()
    # day_6()
    # day_7()
    # day_8()
    # day_9(2, "Day 9.1:")
    # day_9(10, "Day 9.2:")
    # day_10()
    # day_11(20, "Day 11.1:")
    # day_11(10_000, "Day 11.2", False)
    # day_12()
    # day_13()
    # day_14()
    day_15()