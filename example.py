import readlineio as r
import time

@r.main('User nuke tool')
def nuke_tool():
    r.output('Patreon Nuke Tool. Use with Caution!')
    r.input('What is the email address to nuke?').then(nuke_email_confirm)

def nuke_email_confirm(email):
    #r.session.set('email', email)
    r.output('Nuking user [' + email + ']')
    r.choice('Continue?').then(nuke_email)

def nuke_email(choice):
    #email = r.session.get('email')
    if choice == 'Yes':
        #r.output('Continuing with nuke on user: ' + email)
        r.output('Erasing user messages...')
        time.sleep(1)
        r.output('Dereferencing payment history...')
        time.sleep(1)
        r.output('Erasing user info...')
        time.sleep(1)
        r.output('Done!')
    else:
        r.output('Aborting process')

if __name__ == '__main__':
    r.run(nuke_tool)