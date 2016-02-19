import readlineio as rio
#import patreon

@rio.main
def example_input():
    rio.output('Patreon Nuke Tool. Use with Caution!')
    rio.input('What is the email address to nuke?').then(nuke_email)

def nuke_email(email):
    patreon.nuke_by_email(email)
    rio.output("Done!")

if __name__ == '__main__':
    rio.run()