"""
@title

@description

"""
import argparse
import os

import discord

from media_server import env_dir
from media_server.MediaClient import MediaClient

print(f'Loading token from {env_dir}')
MEDIA_SERVER_TOKEN = os.getenv('MEDIA_SERVER_PUBLIC_KEY')

def main(main_args):
    intents = discord.Intents.default()
    intents.message_content = True

    client = MediaClient(intents=intents)
    client.run(MEDIA_SERVER_TOKEN)

    _ = input('Press any key to exit...')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    args = parser.parse_args()
    main(vars(args))
