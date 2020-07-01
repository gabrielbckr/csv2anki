import click

from csv2deck.commands.create_deck import create_deck


@click.group()
def app():
    pass


app.add_command(create_deck)


if __name__ == '__main__':
    app()
