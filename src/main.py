from helper.interface import instruct

i = instruct()

while True:
    command = input('>>> ')
    try:
        i.exec(command)
    except Exception as e:
        print('Error:', e)

# Example:
# >>> gt  # Get the term list.
# >>> gc ${term id}  # Get the course list.
# >>> gl ${course id}  # Get the lesson list.
# >>> get .  # Get all the subtitles.
# >>> search  # Enter search mode.
# >>> 思想道德  # Search for 思想道德.
# >>> search  # Exit search mode.
