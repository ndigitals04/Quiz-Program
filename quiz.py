import sys
import random, datetime, threading,time,os

# exit_flag = threading.Event()
base_questions = {
    "Who is Naruto's father?": [
        "Minato Namikaze", "Jiraiya", "Kakashi Hatake", "Hiruzen Sarutobi"
    ],
    "What is the name of Naruto's signature jutsu?": [
        "Rasengan", "Chidori", "Amaterasu", "Shadow Clone Explosion"
    ],
    "Which tailed beast is sealed inside Naruto?": [
        "Kurama (Nine-Tails)", "Shukaku (One-Tail)", "Gyuki (Eight-Tails)", "Matatabi (Two-Tails)"
    ],
    "Who was the first Hokage?": [
        "Hashirama Senju", "Tobirama Senju", "Hiruzen Sarutobi", "Minato Namikaze"
    ],
    "What clan does Sasuke belong to?": [
        "Uchiha", "Hyuga", "Nara", "Akimichi"
    ],
    "Who killed Itachi Uchiha?": [
        "Sasuke Uchiha", "Kakashi Hatake", "Naruto Uzumaki", "Madara Uchiha"
    ],
    "What is Kakashi's Sharingan eye origin?": [
        "Gifted by Obito", "Inherited from his father", "Stolen from an Uchiha", "Awakened naturally"
    ],
    "What is the full name of Naruto’s mother?": [
        "Kushina Uzumaki", "Kurenai Yuhi", "Mei Terumi", "Tsunade Senju"
    ],
    "What is the name of the organization that hunts tailed beasts?": [
        "Akatsuki", "Anbu", "Root", "Orochimaru’s Lab"
    ],
    "What is the name of Sasuke’s older brother?": [
        "Itachi", "Madara", "Obito", "Fugaku"
    ],
    "Who is known as the 'Copy Ninja'?": [
        "Kakashi Hatake", "Might Guy", "Jiraiya", "Shikamaru Nara"
    ],
    "What was Naruto’s dream since childhood?": [
        "To become Hokage", "To defeat Sasuke", "To master Sage Mode", "To join the Akatsuki"
    ],
    "Who trains Naruto in Sage Mode?": [
        "Jiraiya", "Kakashi", "Ma & Pa", "Orochimaru"
    ],
    "What is the final evolution of Sasuke’s Sharingan?": [
        "Rinnegan", "Mangekyō Sharingan", "Byakugan", "Eternal Mangekyō Sharingan"
    ],
    "Which village is Naruto from?": [
        "Konohagakure", "Sunagakure", "Kirigakure", "Iwagakure"
    ],
    "Who is the Eight-Tails jinchuriki?": [
        "Killer Bee", "Gaara", "Naruto", "Yugito Nii"
    ],
    "Which character is best in medical ninjutsu?": [
        "Tsunade", "Ino", "Sakura", "Hinata"
    ],
    "What is the summoning animal of Jiraiya?": [
        "Toad", "Snake", "Slug", "Falcon"
    ],
    "What power does the Byakugan grant?": [
        "360-degree vision", "Fire manipulation", "Mind control", "Super strength"
    ],
    "What is the name of the final war in Naruto Shippuden?": [
        "Fourth Great Ninja War", "Third Shinobi Conflict", "Uchiha Rebellion", "Battle of the Akatsuki"
    ]
}


questions = base_questions
cached_answers =[""]

def instructions():
    print("Welcome to this simple Quiz program. For best use please follow the following instructions:")
    print("Ensure you only send the allowed keywords as responses")
    print("You may type option 'A','B', 'C', or 'D' as a response to a question")
    print("You may type 'submit' to submit your answers for processing")
    print("You may type 'close' to close the application")
    print("Typing start after this instructions will immediately start the quiz.")
    print("Any other input given aside what is stated would be responded to with an error. Good luck!")

def permissionToStartQuiz():
    start_permission = ""
    while start_permission != "close":
        start_permission = input("Type 'start' to begin the Quiz: ")
        if start_permission.lower() == "start":
            return "start"
        elif start_permission == "close":
            print("Great stopping by")
            sys.exit()
        else:
            print("What you typed is not an allowed input")

def prepareQuiz():
    quiz = []
    
    for question,options in questions.items():
        # print(options)
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)
        quiz_options = {"A":shuffled_options[0], "B":shuffled_options[1], "C":shuffled_options[2], "D":shuffled_options[3]}
        quiz_question = [question,quiz_options]
        quiz.append(quiz_question)
    
    random.shuffle(quiz)
    return quiz

def renderSkippedQuestions(skipped_questions,quiz,answers,start_time,duration):
    skipped = []
    for i in range(len(skipped_questions)):
        print(f"{skipped_questions[i][0]}. {skipped_questions[i][1]}")
        for option_letter, option in skipped_questions[i][2].items():
            print(f"{option_letter}. {option}")
        option = ""
        while option != "close":
            time_left = time_checker(start_time,duration)
            minutes,seconds = divmod(time_left, 60)
            print(f"You have {minutes}m, {seconds:.0f}s left")
            option = input("\nType the letter of your chosen Option: ")
            if option.upper() == "A":
                answer = quiz[skipped_questions[i][3]][1]["A"]
                answers[skipped_questions[i][3]] = [quiz[skipped_questions[i][3]][0],answer,"A"]
                break
            elif option.upper() == "B":
                answer = quiz[skipped_questions[i][3]][1]["B"]
                answers[skipped_questions[i][3]] = [quiz[skipped_questions[i][3]][0],answer,"B"]
                break
            elif option.upper() == "C":
                answer = quiz[skipped_questions[i][3]][1]["C"]
                answers[skipped_questions[i][3]] = [quiz[skipped_questions[i][3]][0],answer,"C"]
                break
            elif option.upper() == "D":
                answer = quiz[skipped_questions[i][3]][1]["D"]
                answers[skipped_questions[i][3]] = [quiz[skipped_questions[i][3]][0],answer,"D"]
                break
            elif option.lower() == "skip":
                answers[skipped_questions[i][3]] = [quiz[skipped_questions[i][3]][0],"",""]
                skip_index = skipped_questions[i][3]
                skipped.append([skipped_questions[i][0],skipped_questions[i][1],skipped_questions[i][2],skip_index])
                break
            elif option.lower() == "close" or option.lower() == "submit":
                permission_to_close= ""
                while True:
                    print("Are you sure you want to close and submit this quiz?")
                    permission_to_close = input("Type yes or no: ")
                    if permission_to_close == "yes":
                        return "close"
                    elif permission_to_close == "no":
                        print("Alright continue the Quiz")
                        break
                    else:
                        print("Only Yes or No is allowed")
            else:
                print("Your option is not a valid one. Try again")
        cached_answers[0] = answers
    if skipped != []:
        skipped_questions = skipped
        renderSkippedQuestions(skipped_questions,quiz,answers,start_time,duration)
    return answers


def renderQuiz(quiz, start_time, duration):
    answers = []
    skipped =[]
    for i in range(len(quiz)):
        print(f"{i+1}. {quiz[i][0]}")
        for option_letter, option in quiz[i][1].items():
            print(f"{option_letter}. {option}")
        option = ""
        while option != "close":
            time_left = time_checker(start_time,duration)
            minutes,seconds = divmod(time_left, 60)
            print(f"You have {minutes}m, {seconds:.0f}s left")
            option = input("\nType the letter of your chosen Option: ")
            if option.upper() == "A":
                answer = quiz[i][1]["A"]
                answers.append([quiz[i][0],answer,"A"])
                break
            elif option.upper() == "B":
                answer = quiz[i][1]["B"]
                answers.append([quiz[i][0],answer, "B"])
                break
            elif option.upper() == "C":
                answer = quiz[i][1]["C"]
                answers.append([quiz[i][0],answer, "C"])
                break
            elif option.upper() == "D":
                answer = quiz[i][1]["D"]
                answers.append([quiz[i][0],answer,"D"])
                break
            elif option.lower() == "skip":
                answers.append([quiz[i][0], "", ""])
                skip_index = answers.index([quiz[i][0], "", ""])
                skipped.append([i+1,quiz[i][0],quiz[i][1], skip_index])
                break
            elif option.lower() == "close" or option.lower() == "submit":
                permission_to_close= ""
                while True:
                    print("Are you sure you want to close and submit this quiz?")
                    permission_to_close = input("Type yes or no: ")
                    if permission_to_close == "yes":
                        return ("close",answers)
                    elif permission_to_close == "no":
                        print("Alright continue the Quiz")
                        break
                    else:
                        print("Only Yes or No is allowed")
            else:
                print("Your option is not a valid one. Try again")
        cached_answers[0] = answers
    if skipped != []:
        answers = renderSkippedQuestions(skipped,quiz,answers,start_time,duration)
    return answers

def getKeyByValue(dictionary, target_value):
    for key,value in dictionary.items():
        if value == target_value:
            return key
    return None

def analyzeAnswers(answers,quiz):
    analytics = []
    score = 0
    for i in range(len(answers)):
        # print(answers)
        correct_answer = base_questions[answers[i][0]][0]
        correct_answer_option = getKeyByValue(quiz[i][1],correct_answer)
        if correct_answer == answers[i][1]:
            selected_answer_statement = f"You selected option {answers[i][2]} - {answers[i][1]}"
            correct_answer_statement = f"The Correct answer is {correct_answer_option} - {correct_answer}, You are Correct."
            correction = [i+1,answers[i][0],selected_answer_statement,correct_answer_statement]
            analytics.append(correction)
            score += 1
        elif answers[i][2] == "":
            selected_answer_statement = "You didn't answer the question"
            correct_answer_statement = f"The correct answer is {correct_answer_option} - {correct_answer}"
            correction = [i+1,answers[i][0], selected_answer_statement,correct_answer_statement]
            analytics.append(correction)
        else:
            selected_answer_statement = f"You selected option {answers[i][2]} - {answers[i][1]} "
            correct_answer_statement = f"The Correct answer is {correct_answer_option} - {correct_answer}, You are Wrong."
            correction = [i+1, answers[i][0], selected_answer_statement,correct_answer_statement]
            analytics.append(correction)
    return (analytics,score)


def startQuiz():
    instructions()
    start_permission=permissionToStartQuiz()
    if start_permission == "start":
        quiz = prepareQuiz()
        start_time = time.time()
        duration = 300
        timer = threading.Timer(duration,timeup,args=[quiz])
        timer.daemon = True
        timer.start()
        answers = renderQuiz(quiz, start_time, duration)
        if type(answers) == tuple:
            results = analyzeAnswers(answers[1],quiz)
            analytics = results[0]
            score = results[1] 
            print("Results: ")
            for correction in analytics:
                print(f"{correction[0]}. {correction[1]}")        
                print(correction[2])
                print(correction[3])
            no_of_questions = len(questions)
            print(f"\nYou scored {score}/{no_of_questions}")
            print("Great having you")
            sys.exit()
        else:
            # while not exit_flag.is_set():
            results = analyzeAnswers(answers,quiz)
            analytics = results[0]
            score = results[1] 
            print("Results: ")
            for correction in analytics:
                print(f"{correction[0]}. {correction[1]}")        
                print(correction[2])
                print(correction[3])
            no_of_questions = len(questions)
            print(f"\nYou scored {score}/{no_of_questions}")
        
    
def timeup(quiz):
    # exit_flag.set()
    # print(cached_answers[0])
    results = analyzeAnswers(cached_answers[0],quiz)
    analytics = results[0]
    score = results[1] 
    print("\nResults: ")
    for correction in analytics:
        print(f"{correction[0]}. {correction[1]}")
        print(correction[2])
        print(correction[3])
    no_of_questions = len(questions)
    print(f"\nYou scored {score}/{no_of_questions}")
    print("Thanks for testing the quiz program out")
    os._exit(0)
    
def time_checker(start_time, duration):
    elasped_time = time.time() - start_time
    time_left = duration - elasped_time
    time_left = max(0,time_left)
    return time_left
    


startQuiz()


