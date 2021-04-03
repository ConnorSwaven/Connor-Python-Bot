
# See if string is binary
def is_Binary(userText):
  # If Binary, convert to string
    b = {'0', '1'}
    t = set(userText.replace(" ", ""))
    if b == t or t == {'0'} or t == {'1'}:
      return True
    return False

# Convert from binary to text
def binaryConvert(userText):
  binary_values = userText.split()
  ascii_string = ""
  for binary_value in binary_values:
    an_integer = int(binary_value, 2)
    ascii_character = chr(an_integer)
    ascii_string += ascii_character
  return str(ascii_string)