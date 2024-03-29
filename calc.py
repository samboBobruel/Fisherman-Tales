while True:
    try:
        print("Solution:", eval(input("Insert a math problem:").replace("^", "**")))
    except:
        print("Invalid math problem")