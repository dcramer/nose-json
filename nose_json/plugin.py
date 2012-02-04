"""
nose_json.plugin
~~~~~~~~~~~~~~~~

:copyright: 2012 DISQUS.
:license: BSD
"""
import codecs
import simplejson
import traceback
from time import time
from nose.exc import SkipTest
from nose.plugins import Plugin
from nose.plugins.xunit import id_split, nice_classname, exc_message


class JsonReportPlugin(Plugin):
    name = 'json'
    score = 2000
    encoding = 'UTF-8'

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            taken = time() - self._timer
        else:
            # test died before it ran (probably error in setup())
            # or success/failure added before test started probably
            # due to custom TestResult munging
            taken = 0.0
        return taken

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option(
            '--json-file', action='store',
            dest='json_file', metavar="FILE",
            default=env.get('NOSE_JSON_FILE', 'nosetests.json'),
            help=("Path to json file to store the report in. "
                  "Default is nosetests.json in the working directory "
                  "[NOSE_JSON_FILE]"))

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            self.stats = {'errors': 0,
                          'failures': 0,
                          'passes': 0,
                          'skipped': 0
                          }
            self.results = []
            self.report_file = codecs.open(options.json_file, 'w',
                                           self.encoding, 'replace')

    def report(self, stream):
        self.stats['encoding'] = self.encoding
        self.stats['total'] = (self.stats['errors'] + self.stats['failures']
                               + self.stats['passes'] + self.stats['skipped'])

        self.report_file.write(simplejson.dumps({
            'stats': self.stats,
            'results': self.results,
        }))
        self.report_file.close()

    def startTest(self, test):
        self._timer = time()

    def addError(self, test, err, capt=None):
        taken = self._timeTaken()

        if issubclass(err[0], SkipTest):
            type = 'skipped'
            self.stats['skipped'] += 1
        else:
            type = 'error'
            self.stats['errors'] += 1
        tb = ''.join(traceback.format_exception(*err))
        id = test.id()
        self.results.append({
            'classname': ':'.join(id_split(id)[0].rsplit('.', 1)),
            'name': id_split(id)[-1],
            'time': taken,
            'type': type,
            'errtype': nice_classname(err[0]),
            'message': exc_message(err),
            'tb': tb,
        })

    def addFailure(self, test, err, capt=None, tb_info=None):
        taken = self._timeTaken()
        tb = ''.join(traceback.format_exception(*err))
        self.stats['failures'] += 1
        id = test.id()
        self.results.append({
            'classname': ':'.join(id_split(id)[0].rsplit('.', 1)),
            'name': id_split(id)[-1],
            'time': taken,
            'type': 'failure',
            'errtype': nice_classname(err[0]),
            'message': exc_message(err),
            'tb': tb,
        })

    def addSuccess(self, test, capt=None):
        taken = self._timeTaken()
        self.stats['passes'] += 1
        id = test.id()
        self.results.append({
            'classname': ':'.join(id_split(id)[0].rsplit('.', 1)),
            'name': id_split(id)[-1],
            'time': taken,
            'type': 'success',
        })
