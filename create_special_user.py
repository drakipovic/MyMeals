import getpass

from my_meals.models import User

while 1:
    print 'What role do you want to create? Available options are user_manager or admin.'
    role = raw_input()
    if role != 'user_manager' and role != 'admin':
        print 'Please choose from user_manager or admin.'
    else:
        break

print 'Desired username:'
username = raw_input()

while 1:
    password = getpass.getpass()
    password_again = getpass.getpass(prompt='Password again:')

    if password != password_again:
        print 'Password do not match, try again!'
    else:
        user = User(username, password, role)
        user.save()
        print '{} {} successfully created'.format(role, username)
        break
