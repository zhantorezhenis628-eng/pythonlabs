def snaketocamel(text):
    words = text.split('_')
    return words[0]+ ''.join(word.capitalize() for word in words[1:])
text = "hello_world_python_"
print(snaketocamel(text))