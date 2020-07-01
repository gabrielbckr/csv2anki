import os
import click
import pandas as pd
from pathlib import Path
import genanki as anki
from csv2anki.models import simple_flashcard
from csv2anki.generator.deck_generator import DeckGenerator


@click.command()
@click.option('--source', '-s', prompt='Path to source csv file.')
@click.option('--first', '-f', prompt='Index to first values columns.')
@click.option('--second', '-t', prompt='Index to second values columns.')
@click.option('--name', '-n', default=None, prompt='Name to your new deck.')
@click.option('--header', default=False, prompt='Indicates if csv file has header.')
@click.option('--output', default='.', prompt='Path to output deck.')
def create_deck(source, first: str, second: str, name: str,
                header: bool, output: str):
    """Creates a new anki deck from a csv file."""

    if not os.path.exists(source):
        source = Path('../').resolve().joinpath(source)

    df: pd.DataFrame
    if header is False:
        df = pd.read_csv(source, header=None)
    else:
        df = pd.read_csv(source)

    if first.isnumeric():
        first = int(first)

    if second.isnumeric():
        second = int(second)

    output = Path(output).resolve()

    engine = DeckGenerator(model=simple_flashcard, df=df,
                           word=first, answer=second)
    my_deck = engine.generate_cards().get_deck(name)
    if name is None:
        name = 'output'
    anki.Package(my_deck).write_to_file(f'{output}/{name}.apkg')

    click.echo(f'Done creating new deck {name} at {output}.')
