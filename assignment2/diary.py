import traceback

try:
    with open("diary.txt", "a") as file:
        prompt = "What happened today? "

        while True:
            entry = input(prompt)
            file.write(entry + "\n")

            if entry == "done for now":
                break

            prompt = "What else? "

except Exception as e:
    print("An exception occurred.")
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception message: {e}")
    traceback.print_exc()