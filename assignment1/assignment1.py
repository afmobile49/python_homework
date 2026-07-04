# Write your code here.

def hello():
    return "Hello!"

def greet(name):
    return "Hello, "+name+"!"


def calc(num1, num2, operation="multiply"):
    if operation == "multiply" and (isinstance(num1, str) or isinstance(num2, str)):
        return "You can't multiply those values!"
    
    if operation == "add":
        return num1 + num2
    
    elif operation == "subtract":
        res = num1 - num2
        return round(res, 1) if isinstance(res, float) else res
    
    elif operation == "multiply":
        return num1 * num2
    
    elif operation == "divide":
        if num2 == 0:
            return "You can't divide by 0!"
        return num1 / num2
    
    elif operation == "modulo":
        return num1 % num2



def data_type_conversion(value, target_type):
    try:
        if target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "str":
            return str(value)
    except (ValueError, TypeError):

        return f"You can't convert {value} into a {target_type}."
    


def grade(score1, score2, score3):
    try:
        average = (score1 + score2 + score3) / 3
        
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
            
    except TypeError:
        return "Invalid data was provided."


def repeat(text, count):
    pr1=text * count
    print(pr1) 
    return text * count


def student_scores(action, **kwargs):
    scores = kwargs.values()
    
    if action == "mean":
       return sum(scores) / len(scores)
        
    elif action == "best":
        return max(kwargs, key=kwargs.get)


def titleize(text):
    lowercase_words = {"and", "or", "of", "a", "an", "the", "in", "at", "to", "but", "by", "for"}
    
    words = text.split()
    retrunf = []
    
    for index, word in enumerate(words):
        if index == 0 or word.lower() not in lowercase_words:
            retrunf.append(word.capitalize())
        else:
            retrunf.append(word.lower())
            
    return " ".join(retrunf)



def hangman(secret_word, guessed_letters):
    result = []
    for letter in secret_word:
        if letter in guessed_letters:
            result.append(letter)
        else:
            result.append("_")
            
    return "".join(result)


def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    processed_words = []
    
    for word in words:
        if word[0].lower() in vowels:
            processed_words.append(word + "ay")
        else:
            vowel_index = 0
            for i, char in enumerate(word):
                if char.lower() in vowels:
                    vowel_index = i
                    break
            
            if vowel_index > 0 and word[vowel_index].lower() == 'u' and word[vowel_index-1].lower() == 'q':
                vowel_index += 1
                
            consonant_cluster = word[:vowel_index]
            rest_of_word = word[vowel_index:]
            processed_words.append(rest_of_word + consonant_cluster + "ay")
            
    return " ".join(processed_words)
