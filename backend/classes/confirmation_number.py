import random
import string

def confirmation_number():
  return "CON-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
