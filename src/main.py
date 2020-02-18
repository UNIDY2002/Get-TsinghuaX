from helper.interface import instruct

print('Get-TsinghuaX MOOC字幕抓取助手')
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
# >>> get  # Get all the subtitles.
