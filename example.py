import readlineio as rio
import time

@rio.main('A fun example program')
def main():
    rio.output("I'm running this from my laptop.")
    time.sleep(2)
    rio.output("I also added some delay so this looks more fancy.")
    time.sleep(2)
    rio.choice("Do you like it?").then(respond)

def respond(choice):
    if choice == 'Yes':
        rio.output('Yay!')
    else:
        rio.output('Oh...')

if __name__ == '__main__':
    rio.run(main)