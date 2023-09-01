from UserInput.BasePromptUserInputHandler import BasePromptUserInputHandler

x = BasePromptUserInputHandler()

print(x.getInstructionMessgae())
v = x.getUserInput("HI: ")
print(v.input)
v = x.getUserInput("U R STill Here <->: ")
print(v.input)
