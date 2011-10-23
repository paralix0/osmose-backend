#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from plugins.Plugin import Plugin
import datetime
import dateutil

class Construction(Plugin):

    err_4070    = 4070
    err_4070_fr = u"Construction terminée"
    err_4070_en = u"Finished construction"

    def init(self, logger):
        self.tag_date = ["opening_date", "check_date", "open_date", "construction:date", "temporary:date_on", "date_on"]
        self.default_date = datetime.datetime(9999, 12, 31)
        self.today = datetime.datetime.today()
        self.date_limit = datetime.datetime(self.today.year-2, self.today.month, self.today.day)

    def getTagDate(self, tags):
        for i in self.tag_date:
            if i in tags:
                return tags[i]

    def convert2date(self, string):
        date = parser.parse(string, default=self.default)
        if date.year != 9999:
            return date

    def node(self, data, tags):
        if not "construction" in tags:
            return

        date = None
        tagDate = self.getTagDate(tags)
        if tagDate:
            date = self.convert2date(tagDate)

        if date:
            if date < self.today:
                return [(4070, 0, {})]
        else:
            if datetime.datetime.strptime(data["timestamp"][0:10], "%Y-%m-%d") < self.date_limit:
                return [(4070, 1, {})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
