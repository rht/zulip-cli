#!/usr/bin/env python3
import logging
import sys

from typing import Any, Dict

import zulip
import click

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger('zulip-cli')

DataT = Dict[str, Any]

client = zulip.Client(config_file="~/zuliprc")

@click.group()
def cli():
    pass

@cli.group()
def msg():
    pass

@cli.group()
def stream():
    pass

@msg.command(name='send')
@click.argument("recipients", type=str, nargs=-1)
@click.option('--stream', '-s', default='',
              help='Allows the user to specify a stream for the message.')
@click.option('--subject', '-S', default='',
              help='Allows the user to specify a subject for the message.')
@click.option('--message', '-m', required=True)
def do_send_message(recipients, stream, subject, message) -> bool:
    '''Sends a message and optionally prints status about the same.'''

    # Sanity check user data
    has_stream = stream != ''
    has_subject = subject != ''
    if len(recipients) != 0 and has_stream:
        click.echo('You cannot specify both a username and a stream/subject.')
        raise SystemExit(1)
    if len(recipients) == 0 and (has_stream != has_subject):
        click.echo('Stream messages must have a subject')
        raise SystemExit(1)
    if len(recipients) == 0 and not has_stream:
        click.echo('You must specify a stream/subject or at least one recipient.')
        raise SystemExit(1)

    if has_stream:
        message_data = {
            'type': 'stream',
            'content': message,
            'subject': subject,
            'to': stream,
        }
    else:
        message_data = {
            'type': 'private',
            'content': message,
            'to': recipients,
        }

    if message_data['type'] == 'stream':
        log.info('Sending message to stream "%s", subject "%s"... ' %
                 (message_data['to'], message_data['subject']))
    else:
        log.info('Sending message to %s... ' % message_data['to'])
    response = client.send_message(message_data)
    if response['result'] == 'success':
        log.info('Message sent.')
        return True
    else:
        log.error(response['msg'])
        return False

@msg.command()
def upload():
    '''Upload a single file and get the corresponding URI.
    '''
    # TODO

@msg.command()
@click.argument("message_id", type=int)
@click.option('--message', '-m', required=True)
def edit(message_id, message):
    '''Edit/update the content or topic of a message.
    '''
    request = {
        "message_id": message_id,
        "content": message,
    }
    result = client.update_message(request)
    log.info(result)

@msg.command()
@click.argument("message_id", type=int)
def delete(message_id):
    '''Permanently delete a message.
    '''
    result = client.delete_message(message_id)
    log.info(result)

# TODO
# https://zulip.com/api/get-messages
# https://zulip.com/api/construct-narrow

@msg.command()
@click.argument("message_id", type=int)
@click.argument("emoji_name")
def add_emoji(message_id, emoji_name):
    '''Add an emoji reaction to a message.
    '''
    request = {
        'message_id': message_id,
        'emoji_name': emoji_name,
    }

    result = client.add_reaction(request)
    log.info(result)

@msg.command()
@click.argument("message_id", type=int)
@click.argument("emoji_name")
def remove_emoji(message_id, emoji_name):
    '''Remove an emoji reaction from a message.
    '''
    request = {
        'message_id': message_id,
        'emoji_name': emoji_name,
    }

    result = client.remove_reaction(request)
    log.info(result)

# TODO
# https://zulip.com/api/render-message
# https://zulip.com/api/get-raw-message
# https://zulip.com/api/check-narrow-matches

@msg.command()
@click.argument("message_id", type=int)
def get_edit_history(message_id):
    '''Fetch the message edit history of a previously edited message.
    Note that edit history may be disabled in some organizations; see https://zulip.com/help/view-a-messages-edit-history.
    '''
    result = client.get_message_history(message_id)
    log.info(result)

# TODO
# https://zulip.com/api/update-message-flags

@msg.command()
def mark_all_as_read():
    '''Marks all of the current user's unread messages as read.
    '''
    result = client.mark_all_as_read()
    log.info(result)

@stream.command()
def list_subscriptions():
    '''Get all streams that the user is subscribed to.
    '''
    result = client.list_subscriptions()
    log.info(result)

if __name__ == '__main__':
    cli()
