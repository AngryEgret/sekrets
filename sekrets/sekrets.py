#!/usr/bin/env python

import sys
import gnupg
import requests
import json
import click

@click.group()
def cli():
    """Simple program to leverage keybase.io and gpg to encrypt files
    for multiple public keys"""
    pass

@cli.command()
@click.option('--recipients', prompt=True, help='Path to recipients file')
@click.option('--input', prompt=True, help='Path to cleartext file')
@click.option('--output', prompt=True, help='Path to encrypted file')
@click.option('--gpghome', default='~/.gnupg/')
def encrypt(recipients, input, output, gpghome):
    """This command will encrypt the provided input file against the
    public keys of the users provided in the recipients file."""
    click.echo('Encrypting...')

    gpg = gnupg.GPG(gnupghome = gpghome)

    with open(recipients) as stream:
        recipient_dict = json.load(stream)

    cleartext = open(input, "rb")

    encrypted_ascii_data = gpg.encrypt_file(
            cleartext,
            recipient_dict.values(),
            always_trust = True,
            output = output)

    click.echo('... Encryption Complete')

@cli.command()
@click.option('--input', prompt=True, help='Path to cleartext file')
@click.option('--output', prompt=True, help='Path to encrypted file')
@click.option('--gpghome', default='~/.gnupg/')
def decrypt(input, output, gpghome):
    """This command will decrypt the provided input file and output the
    cleartext file to the output path provided.
    """
    click.echo('Decrypting...')

    gpg = gnupg.GPG(gnupghome = gpghome)

    ciphertext = open(input, "rb")

    encrypted_ascii_data = gpg.decrypt_file(
            ciphertext,
            always_trust = True,
            output = output)

    click.echo('... Decryption Complete')

@cli.command()
@click.option('--recipients', prompt=True, help='Path to recipients file')
@click.option('--gpghome', default='~/.gnupg/')
def key_import(recipients, gpghome):
    """This command will import the public keys for the recipients in the
    provided recipients file.

    The recipients file should be a json file in the format of:
    \b
        {
            "<keybase identity>":"gpg fingerprint",
            "<keybase identity>":"gpg fingerprint",
            "<keybase identity>":"gpg fingerprint"
        }
    """
    click.echo('Importing...')

    gpg = gnupg.GPG(gnupghome = gpghome)

    with open(recipients) as stream:
        recipient_dict = json.load(stream)

    for recipient in recipient_dict.keys():
        r = requests.get('https://keybase.io/{}/key.asc'.format(recipient))
        if r.ok:
            try:
                result = gpg.import_keys(r.text)
            except Exception as e:
                click.echo('Error importing key for recipient {}'.format(recipient))
                click.echo(e)
                sys.exit(1)
        else:
            try:
                click.echo('Error downloading key for {}'.format(recipient))
            except Exception as e:
                click.echo('Error downloading keys')
                click.echo(e)
                sys.exit(1)
    click.echo('... Importing Complete')

if __name__ == '__main__':
    cli(obj={})
