# -*- coding: utf-8 -*-
import re
from lektor.pluginsystem import Plugin

class BootstrapTableMixin(object):
    name = 'Markdown Bootstrap Tables'
    description = u'Format table with bootstrap classes.'

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
            '<table class="table">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)



_prefix_re = re.compile(r'^\s*!!! (info|tip|note|success|warning|danger)\s+')

CLASSES = {
    "info": "info",
    "tip": "info",
    "success": "success",
    "warning": "warning",
    "danger": "danger",
}

class AdmonitionMixin(object):
    name = 'Markdown Admonition'
    description = u'Adds basic admonition tag support to Markdown.'

    def paragraph(self, text):
        match = _prefix_re.match(text)
        if match is None:
            return super(AdmonitionMixin, self).paragraph(text)
        adtype = match.group(1)
        return '<div class="alert alert-%s" role="alert">%s</div>' % (
            CLASSES[adtype],
            text[match.end():]
        )


class MarkdownExtrasPlugin(Plugin):
    name = 'markdown-extras'
    description = u'Adds markdown extras.'

    def on_markdown_config(self, config, **extra):
        config.renderer_mixins.append(BootstrapTableMixin)
        config.renderer_mixins.append(AdmonitionMixin)
