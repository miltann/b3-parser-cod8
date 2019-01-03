# -*- coding: utf-8 -*-

# ################################################################### #
#                                                                     #
#  BigBrotherBot(B3) (www.bigbrotherbot.net)                          #
#  Copyright (C) 2005 Michael "ThorN" Thornton                        #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
# CHANGELOG
#
# 08/01/2012 - v0.1 - NTAuthority (http://fourdeltaone.net/)
# unknown - v0.4 - NTAuthority (http://fourdeltaone.net/)
# 04.10.2018 - v0.5 - WatchMiltan 
# - added cod8 rcon commands
# 30.12.2018 - v0.6 - WatchMiltan
# - working unban command
#

__author__ = 'NTAuthority, WatchMiltan'
__version__ = '0.6'

import b3.parsers.cod6
import re

class Cod8Parser(b3.parsers.cod6.Cod6Parser):

    gameName = 'cod8'
        
    _guidLength = 16
    _commands = {
        'message': 'tell %(cid)s %(message)s',
        'say': 'say %(message)s',
        'set': 'set %(name)s "%(value)s"',
        'kick': 'dropclient %(cid)s "%(reason)s"',
        'ban': 'banclient %(cid)s "%(reason)s"',
        'unban': 'unban %(guid)s',
        'tempban': 'tempbanclient %(cid)s "%(reason)s"'
    }

    _regPlayer = re.compile(r'(?P<slot>[0-9]+)\s+'
                            r'(?P<score>[0-9-]+)\s+'
                            r'(?P<ping>[0-9]+)\s+'
                            r'(?P<guid>[a-z0-9]+)\s+'
                            r'(?P<name>.*?)\s+'
                            r'(?P<last>[0-9]+)\s+'
                            r'(?P<ip>[0-9.]+):'
                            r'(?P<port>[0-9-]+)', re.IGNORECASE)

    ####################################################################################################################
    #                                                                                                                  #
    #   PARSER INITIALIZATION                                                                                          #
    #                                                                                                                  #
    ####################################################################################################################

    def startup(self):
        """
        Called after the parser is created before run().
        """
        b3.parsers.cod6.Cod6Parser.startup(self)
        
    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        if not client or not client.guid:
            return

        self.write(self.getCommand('unban', guid=client.guid, reason=reason))
        if admin:
            admin.message('Removed ban for %s from banlist.' % client.exactName)
