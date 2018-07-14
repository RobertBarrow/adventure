#! python
import json

def ask_question(choices, answer):

    print("\nWhich of the following words is a correct spelling?\n")
    c = 0
    for choice in choices:
        c += 1
        print('\n\t[' + str(c) + "] " + format(choice))
    decision = input("\nEnter the number or Q to quit\t")
    return(decision)

def load_questions():
# with open('data.txt', 'w') as f:
#    json.dump(data, f, ensure_ascii=True)
    with open('data/spelling_questions.json') as f:
        questions = json.load(f)
    return(questions)

SCORE = 0
questions = load_questions()

for choices, answer in questions:
    
    decision = ask_question(choices, answer)
    if decision == 'Q' or decision == 'q': 
        break
    if int(decision) == answer:
        print("CORRECT!")
        SCORE += 1
    else:   
        print("No, sorry.  The answer was " + str(answer) + ".\n")

print("\nYour total score was: " + str(SCORE))
    

