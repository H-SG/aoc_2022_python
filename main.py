def read_to_array(path: str, strip: bool = True) -> list[str]:
    with open(path) as f:
        lines: list[str] = f.readlines()

    # let's always clean up
    if strip:
        return [x.strip() for x in lines]
    else:
        return lines

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
    print(f"The elf carrying the most calories is carrying {calory_list[-1]} calories")
    print(f"The three elves carrying the most calories are carrying {sum(calory_list[-3:])} calories")

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

    print(f"The score when following the assumed strategy guide is {score_1}")
    print(f"The score when following the true strategy guide is {score_2}")

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

    print(f"Sum of priorities in common item types is {sum(common_items_priority)}")
    
    # strings to kinda chars
    rucksacks_items: list[list[str]] = [[y for y in x] for x in rucksacks]

    # sets and intersections
    badges: list[str] = []
    for i in range(0, len(rucksacks_items), 3):
        com1: set[str] = set(rucksacks_items[i]).intersection(rucksacks_items[i + 1])
        badges.append(list(com1.intersection(rucksacks_items[i + 2]))[0])

    # moar ascii schenaningans
    badges_priority: list[int] = [ord(x) - 96 if ord(x) > 91 else ord(x) - 38 for x in badges]

    print(f"Sum of priorities for the badges are {sum(badges_priority)}")

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

    print(f"Number of overlapping rosters are {subsets}")
    print(f"Number of overlapped assignments are {overlapping}")

def day_5_part_1() -> None:
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
    t_stacks: list[list[str]] = []

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
                t_stacks.append([])

            if col != 'None':
                t_stacks[j].append(col[1])

    # need to flip around the stacks to work on the end of the list
    t_stacks: list[list[str]] = [list(reversed(x)) for x in t_stacks]

    # parse through the instructions
    for instruction in instructions:
        sub_instructions: list[str] = instruction.split(" ")

        num_move: int = int(sub_instructions[1])
        origin: int = int(sub_instructions[3]) - 1
        destination: int = int(sub_instructions[5]) - 1

        # for part 2, we just leave out this little reversed here
        to_move = list(reversed(t_stacks[origin][-num_move:]))
        t_stacks[origin] = t_stacks[origin][:-num_move]
        t_stacks[destination] += to_move

    # make our top of crate string
    end_string: str = "".join([x[-1] for x in t_stacks])

    print(f'The top of crates string for part 1 is {end_string}')

def day_5_part_2() -> None:
    # this is virtually a copy paste of part 1, because lazy
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
    t_stacks: list[list[str]] = []

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
                t_stacks.append([])

            if col != 'None':
                t_stacks[j].append(col[1])

    # need to flip around the stacks to work on the end of the list
    t_stacks: list[list[str]] = [list(reversed(x)) for x in t_stacks]

    # parse through the instructions
    for instruction in instructions:
        sub_instructions: list[str] = instruction.split(" ")

        num_move: int = int(sub_instructions[1])
        origin: int = int(sub_instructions[3]) - 1
        destination: int = int(sub_instructions[5]) - 1

        # for part 1, we just add in a little reversed here
        to_move = t_stacks[origin][-num_move:]
        t_stacks[origin] = t_stacks[origin][:-num_move]
        t_stacks[destination] += to_move

    # make our top of crate string
    end_string: str = "".join([x[-1] for x in t_stacks])

    print(f'The top of crates string for part 2 is {end_string}')

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

    print(f"The first start of packet marker is at {part_1_index}")
    print(f"The first start of message marker is at {part_2_index}")

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
    current_path: str = None
    current_dir: Directory = None
    root_dir: Directory = None
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
                if current_path is not None:
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

    print(f"The sum size of all folders smaller than 100000 is {sub_100000_sum}")

    # all magic numbers courtesy of the elves
    free_space: int = 70000000 - root_dir.size
    space_needed: int = 30000000 - free_space

    # i guess this is unneeded, could just store the sizes
    deletion_candidates: dict[str, int] = {k:v for k, v in dir_size_dict.items() if v >= space_needed}
    sorted_delection_candidates: dict[str, int] = dict(sorted(deletion_candidates.items(), key=lambda item: item[1]))
    
    print(f"The smallest directory to be deleted is {list(sorted_delection_candidates.keys())[0]} with size {list(sorted_delection_candidates.values())[0]}")

if __name__ == "__main__":
    day_1()
    day_2()
    day_3()
    day_4()
    day_5_part_1()
    day_5_part_2()
    day_6()
    day_7()