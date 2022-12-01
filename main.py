def day_1() -> None:
    # i'm certain there is a more efficient way of doing this, but
    # this is what came up this morning in my meatbrain
    calory_list: list[int] = []
    new_elf: bool = False
    with open('data/day1.txt') as f:
        for line in f:
            if len(calory_list) == 0:
                calory_list.append(int(line))
            else:
                if new_elf == True:
                    calory_list.append(int(line))
                    new_elf = False
                else:
                    if line == "\n":
                        new_elf = True
                    else:
                        calory_list[-1] += int(line)

    calory_list.sort()
    print(f"The elf carrying the most calories is carrying {calory_list[-1]} calories")
    print(f"The three elves carrying the most calories are carrying {sum(calory_list[-3:])} calories")


if __name__ == "__main__":
    day_1()