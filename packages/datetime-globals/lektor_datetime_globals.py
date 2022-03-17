# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
import datetime


class DatetimeGlobalsPlugin(Plugin):
    name = 'datetime-globals'
    description = u'This plugin adds `datetime`.'

    def on_setup_env(self, **extra):
        self.env.jinja_env.globals['now'] = datetime.datetime.utcnow
        self.env.jinja_env.globals['today'] = datetime.datetime.today
