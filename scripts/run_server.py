"""
@title

@description

"""
import argparse
import os

import discord

from media_server import env_dir
from media_server.MediaClient import MediaClient



def main(main_args):
    """
    If you want to generate this URL dynamically at run-time inside your bot and using the
    discord.Permissions interface, you can use [discord.utils.oauth_url().

    https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions
    https://discordpy.readthedocs.io/en/stable/api.html#discord.utils.oauth_url
    https://discord.com/developers/docs/topics/oauth2#bots

    :param main_args:
    :return:
    """
    print(f'Loading token from {env_dir}')
    media_server_token = os.getenv('MEDIA_SERVER_TOKEN')

    intents = discord.Intents.all()
    client = MediaClient(intents=intents)

    client.run(media_server_token)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    args = parser.parse_args()
    main(vars(args))
