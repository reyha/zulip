from __future__ import absolute_import
from __future__ import print_function

from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from zerver.models import get_realm_by_string_id
from zerver.lib.actions import set_default_streams

from optparse import make_option
import sys

class Command(BaseCommand):
    help = """Set default streams for a realm

Users created under this realm will start out with these streams. This
command is not additive: if you re-run it on a domain with a different
set of default streams, those will be the new complete set of default
streams.

For example:

python manage.py set_default_streams --realm=foo --streams=foo,bar,baz
python manage.py set_default_streams --realm=foo --streams="foo,bar,baz with space"
python manage.py set_default_streams --realm=foo --streams=
"""

    def add_arguments(self, parser):
        # type: (CommandParser) -> None
        parser.add_argument('-r', '--realm',
                            dest='string_id',
                            type=str,
                            help='The subdomain or string_id of the existing realm to which to '
                                 'attach default streams.')

        parser.add_argument('-s', '--streams',
                            dest='streams',
                            type=str,
                            help='A comma-separated list of stream names.')

    def handle(self, **options):
        # type: (*Any, **str) -> None
        if options["string_id"] is None or options["streams"] is None:
            print("Please provide both a subdomain name or string_id and a default \
set of streams (which can be empty, with `--streams=`).", file=sys.stderr)
            exit(1)

        stream_names = [stream.strip() for stream in options["streams"].split(",")]
        realm = get_realm_by_string_id(options["string_id"])
        set_default_streams(realm, stream_names)
