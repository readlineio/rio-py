import readlineio as rio
import time

@rio.main
def example_input():
    rio.output('Patreon Nuke Tool. Use with Caution!')
    rio.input('What is the email address to nuke?').then(nuke_email)

def nuke_email(email):
    rio.output('Nuking user <' + email + '>')
    rio.choice('Continue?').then(actually_nuke_email)

def actually_nuke_email(choice):
    if choice == 'Yes':
        rio.output('Erasing user messages...')
        time.sleep(1)
        rio.output('Dereferencing payment history...')
        time.sleep(1)
        rio.output('Erasing user info...')
        time.sleep(1)
        rio.output('Done!')
    else:
        rio.output('Aborting process')

if __name__ == '__main__':
    rio.run()