import random
import string
import json

# Consider adding string.punctuation
possible_characters = string.ascii_letters + string.digits


def generate_password(length=256):
    rng = random.SystemRandom()
    return "".join([rng.choice(possible_characters) for i in range(length)])


if __name__ == "__main__":
    secret = generate_password(256)
    print(secret)
    with open('./config.json', 'w') as file:
        json.dump({"secret": secret}, file)