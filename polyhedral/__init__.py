import znc

import prettytable
import diceparse


def _mkhelp():
    headers = "Command Arguments Description".split()
    pt = prettytable.PrettyTable(headers)
    pt.align = 'l'
    pt.add_row(['Add', '<chan>', 'Enable dice in <chan>'])
    pt.add_row(['Del', '<chan>', 'Disable dice in <chan>'])
    pt.add_row(['List', '', ''])
    pt.add_row(['Help', '', 'Generate this output'])
    return pt.get_string(sortby='Command')


HELP_TEXT = _mkhelp().splitlines()
PM_TRIGGER = '!r'


class polyhedral(znc.Module):
    description = 'Polyhedral Dice'

    def cmd_add(self, line):
        '''Add a channel
        usage: Add <channel> <trigger>
        channel - the channel name
        trigger - the prefix that the script will respond to
        '''
        channel, _, trigger = line.partition(' ')
        if not channel or not trigger:
            self.PutModule('Invalid arguments')
            return
        self.nv[channel] = trigger
        self.PutModule('Channel added')

    def cmd_del(self, line):
        '''Remove a channel
        usage: Del <channel>
        channel - the channel name
        '''
        channel, _, _ = line.partition(' ')
        if not channel:
            self.PutModule('Invalid arguments')
            return
        if channel in self.nv:
            del self.nv[channel]
            self.PutModule('Channel removed')
        else:
            self.PutModule('Channel not found')

    def cmd_list(self, line):
        '''List all channels currently in the script
        usage: List
        '''
        channels = list(self.nv.items())
        if channels:
            pt = prettytable.PrettyTable(('Channel', 'Trigger'))
            pt.align = 'l'
            for channel, trigger in channels:
                pt.add_row((channel, trigger))
            for line in pt.get_string(sortby='Channel').splitlines():
                self.PutModule(line)
        else:
            self.PutModule('No channels enabled')

    def cmd_help(self, line):
        command = line.split(' ')[0] if line else None
        help_text = {
            'add': self.cmd_add.__doc__.splitlines(),
            'del': self.cmd_del.__doc__.splitlines(),
            'list': self.cmd_list.__doc__.splitlines(),
            None: HELP_TEXT
        }
        for line in help_text.get(command):
            self.PutModule(line)

    def OnModCommand(self, line):
        command, _, args = line.partition(' ')
        dispatch = {
            'add': self.cmd_add,
            'del': self.cmd_del,
            'list': self.cmd_list,
            'help': self.cmd_help,
        }
        if command.lower() in dispatch:
            dispatch[command.lower()](args)
        else:
            self.PutModule('Unknown command.  Try Help.')

    def OnChanMsg(self, nick, chan, message):
        nick = nick.GetNick()
        first, _, rest = str(message).partition(' ')
        chan = chan.GetName()
        trigger = self.nv.get(chan, None)
        if trigger and first == trigger:
            self._roll(nick, chan, rest)
        return znc.CONTINUE

    def OnPrivMsg(self, nick, message):
        nick = nick.GetNick()
        first, _, rest = str(message).partition(' ')
        if first == PM_TRIGGER:
            self._roll('You', nick, rest)
        return znc.CONTINUE

    def _roll(self, nick, to, dice_line):
        lines = diceparse.roll(dice_line)
        if len(lines):
            for line in lines:
                self.send_message(to, line)

    def send_message(self, to, text):
        self.PutIRC('PRIVMSG {0} :{1}'.format(to, text))
