# zulip-cli

CLI interface to Zulip. It assumes that your zuliprc is in `~/zuliprc`

## Examples
- Sending a message to a stream `./zulip-cli.py msg send -s "test here" -S woah`
- Editing a message `./zulip-cli.py msg edit 1122133`
- Emoji-reacting to a message `./zulip-cli.py msg add-emoji 1122133 octopus`
- Mark all messages as read (warn: also applies to muted streams) `./zulip-cli.py msg mark-all-as-read`
- View subscribed streams `./zulip-cli.py stream list-subscriptions`
