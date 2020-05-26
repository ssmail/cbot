# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import click


@click.group()
def db():
    pass


@click.command()
@click.option("--name", help="用户名")
def add(name):
    click.echo(f'add user {name}')


@click.command()
@click.option("--id", help="用户名")
def delete(id):
    click.echo(f'delete user {id}')


db.add_command(delete)
db.add_command(add)

if __name__ == '__main__':
    db()

# python3 cli.py add --name 23

# python3 cli.py delete --id=fdsa
