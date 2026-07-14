import traceback


try:
    with open("diary.txt", "a", encoding="utf-8") as diary_file:
        prompt = "What happened today? "

        while True:
            entry = input(prompt)

            if entry == "done for now":
                break

            diary_file.write(entry + "\n")
            prompt = "What else? "

except Exception as error:
    exception_name = type(error).__name__

    print(f"{exception_name}: {error}")

    traceback_details = traceback.extract_tb(error.__traceback__)

    for detail in traceback_details:
        print(
            f'File "{detail.filename}", '
            f"line {detail.lineno}, "
            f"in {detail.name}"
        )