from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Each can only be either a knight or a knave, not both
    Not(And(AKnave, AKnight)),
    Or(AKnight, AKnave),

    # What was said in the puzzle
    Implication(AKnave, Not(And(AKnave, AKnight))),
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Each can only be either a knight or a knave, not both
    Not(And(AKnave, AKnight)),
    Or(AKnight, AKnave),

    Not(And(BKnave, BKnight)),
    Or(BKnight, BKnave),

    # What was said in the puzzle
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Each can only be either a knight or a knave, not both
    Not(And(AKnave, AKnight)),
    Or(AKnight, AKnave),

    Not(And(BKnave, BKnight)),
    Or(BKnight, BKnave),

    # What was said in the puzzle
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, And(AKnave, BKnight)),

    Implication(BKnight, Not(And(BKnight, AKnight))),
    Implication(BKnave, And(BKnave, AKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Each can only be either a knight or a knave, not both
    Not(And(AKnave, AKnight)),
    Or(AKnight, AKnave),

    Not(And(BKnave, BKnight)), 
    Or(BKnight, BKnave),

    Not(And(CKnave, CKnight)),
    Or(CKnight, CKnave),

    # What was said in the puzzle
    # Find out what A said
    Or(
        # I am a knight
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),

        # I am a knave
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),

    # What B said
    Implication(BKnight, Implication(AKnight, Not(AKnight))),
    Implication(BKnight, Implication(AKnave, Not(AKnave))),
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),

    # What C said
    Implication(CKnave, AKnave),
    Implication(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
