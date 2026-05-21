def evaluate_mcq(user_answers, questions):
    score = 0

    for i, q in enumerate(questions):
        correct = q["answer"]

        # ✅ If answer is A/B/C/D → convert to option
        if correct in ["A", "B", "C", "D"]:
            index = ord(correct) - 65
            correct = q["options"][index]

        if user_answers[i] == correct:
            score += 1

    return score