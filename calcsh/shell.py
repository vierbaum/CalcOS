import calcsh
while True:
    text = input(">")
    result, error = calcsh.run("sh", text)

    if error:
        print(error.asString())
    else:
        print(result)