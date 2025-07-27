HELPSTRING='''- !Help: Displays command list.
- !Hello: Returns "Hello!".
- !Roll: Used to roll dice in 1d10 format. Use "+" to add dice total togheter and "," to count them separately. To make multiple rolls of the same type easier use "(1d20)x10" for example to make 10 seperate d20 rolls
'''

COMMANDS_LIST={
    "!Help": {
        "type": "message",
        "reply": f"{HELPSTRING}"
    },
    "!Hello": {
        "type": "message",
        "reply": "Hello!"
        },
    "!Roll": {
        "type": "DiceRoll"
    }
}