from helper.interface import Interface

i = Interface('foo', 'bar')  # Do not know how to simulate logging in yet.
while True:
    command = input('>>> ')
    try:
        i.execute(command)
    except:
        pass

# Example:
# >>> cookie ${your cookies (get them from your browser's developer mode)}  # "Login".
# >>> gt  # Get the term list.
# >>> gc ${term id}  # Get the course list.
# >>> gl ${course id}  # Get the lesson list.
