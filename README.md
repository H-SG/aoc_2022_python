# aoc_2022_python
Back for another year babey!

Last year I did rust, which while a lot of fun was a bit hard when I started running into the limits of my algo knowledge.

As such, this year the learning forcus for me is on  algos, and I will be sticking with the comfortingly familiar Python.

As usual, my IDE de jour will be VS Code on WSL and using lots of typing.

## Day 1
I almost completely forgot about day 1. The whole week I've been harking on about doing this, and almost catastrophy.

I'm not going to write too many functions yet, I'l; start abstracting things out once I've figured out what happens the mostest. For now, please accept this very naive implementation.

## Day 2
Doing this on day 3, because I'M A REBEL. Looks like list, splits, and some pattern matching. Bish bash bosh.

I think this could go quicker with nested matching, but since there are only 9 possible options it didn't take too long to sort out.

## Day 3
String manipulations for dayz, honestly I don't do much string manipulation day to day, but using intersection in sets is something novel for me.

## Day 4
I'm actually kinda on time, but wasted an inordinate ammount of time dickering about with badly formed if loops and resulting bad answers.

Brain not work good early.

One could do it just with sets and length comparisons.

## Day 5
Stacks! Transpotitions! Stacks suddenly lists!

I enjoyed this quite a bit, because going from part 1 to part 2 involved removing a single wrapping function on a single line.

## Day 6
Nice and quick one, but my colleagues are quicker 😡.

## Day 7
Time for some data structures, something which I am not formally familiar with, I think this might be the first tree/graph thing I've made in ages. I escaped the recursion maelstrom by benefit that it is not needed here.

## Day 8
I thought this was going to be easy, and it almost was if only I didn't swap an x and y around on one line!

I feel like there must be a neat trick to solving this most quickly, but it eludes me.

## Day 9
This wasn't too bad, though the part 1 only solution did feel more elegant, but ultimately the number of loops remained unchanged (even if one loop now only ever goes through one iteration).

I forgot to do mypy checks for a few days, so a few errors have been fixed, but there is some annoying mypy behaviour I have to sus out and figure what is the best approach...

## Day 10
Pseudo assembly and racing the beam! This is my JAM. My use of pattern matching so far has been pleasingly high. I'm truly astounded I had no off by one errors for part 2.

## Day 11
Phew! Part 2 came in like a real sucker punch and I should've seen it coming the moment the problem statement said "...find another way to keep your worry levels manageable."

Now, I kinda stumbled on the solution by accident, and it took me a while to figure out why. 

Spoilers, replace the worry level of an item by the modulo result of that worry level and the least common multiple of all the check values from all the monkeys.

If you don't reduce worry level in some way, you're going to run into BIG BigNum issues. My first thought was to divide the worry level by the modulo value if the check passes when the monkey wants to throw. However, this doesn't really happen enough to make a difference, we need to do somemthing else.

Let's consider a trivial example of two monkeys. Their test divisors being 2 and 3 (lcm = 6), and only 1 is ever added to the worry level:

| Original Worry | % 6 (lcm) Remainder | % 2   | % 3   |
|----------------|---------------------|-------|-------|
| 1              | 1                   | False | False |
| 2              | 2                   | True  | False |
| 3              | 3                   | False | True  |
| 4              | 4                   | True  | False |
| 5              | 5                   | False | False |
| 6              | 0                   | True  | True  |
| 7              | 1                   | False | False |
| 8              | 2                   | True  | False |
| 9              | 3                   | False | True  |
| 10             | 4                   | True  | False |
| 11             | 5                   | False | False |
| 12             | 0                   | True  | True  |
| 13             | 1                   | False | False |
| 14             | 2                   | True  | False |

As one can see, the modulo result preserves the behaviour of the common factors modulo on the actual worry, so we can always just replace worry level with the modulo remainder and still get the expected monkey check behaviour.

There may be some nice formal mathermagical explanation for this, but I don't formally know what that might be.

## Day 12
I've always wondered how pathfinding works algorithmically, and now I know for at least Djikstra's method.

For a brief time I was banging my head thinking my puzzle input was not solvable, when I incorrectly assumed I can only ascend or DESCEND by max one height level 🤦.

Today is the first day I feel I could make a neat little visualisation, so I'm going to try that.

## Day 13
That wasn't too hard, but I also wouldn't describe it as that interesting.

I guess the trinary recursion result is kinda neat, but really it was just a bit of pain to do today. I guess using `eval` just felt like too much of cop-out, and I was worried how mypy would handle it.