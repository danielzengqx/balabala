#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CTS schedule process
   by Kobe Gong. 2017-7-16
"""

import re, os, time, datetime, sys
import argparse
import signal
import threading, subprocess
import queue, yaml
import pexpect
from cmd import Cmd


class arg_handle():
    def __init__(self, name=' '):
        self.parser = self.build_option_parser("-" * 50)

    def build_option_parser(self, description):
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(
            '-w', '--way',
            dest='way',
            action='store',
            #action='append',
            #metavar='pattern',
            choices={'shell', 'post'},
            default='shell',
            #default=['case.yaml'],
            #type=int,
            #required=True,
            help='Specify how to add object, ["shell", "post"] are support now',
        )

        return parser

    def get_args(self, attrname):
        return getattr(self.args, attrname)

    def check_args(self):
        pass

    def run(self):
        self.args = self.parser.parse_args()
        P.warning_p("CMD line: " + str(self.args))
        self.check_args()


class Cprint:
	def __init__(self, value=' '):

		STYLE = {
			'fore': {
				'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
				'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
			},

			'back': {
				'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
				'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
			},

			'mode': {
				'default': 0, 'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
			},

			'default': {
				'end': 0,
			}
		}
		self.style = STYLE
		self.name = value

	def common_p(self, string, mode='defult', fore='blue', back=''):
		mode = '%s' % self.style['mode'][mode] if mode in self.style['mode'] else self.style['mode']['default']
		fore = '%s' % self.style['fore'][fore] if fore in self.style['fore'] else ''
		back = '%s' % self.style['back'][back] if back in self.style['back'] else ''
		style = ';'.join([s for s in [mode, fore, back] if s])
		style = '\033[%sm' % style
		end = '\033[%sm' % self.style['default']['end']

		print ("%s%s%s" % (style, string, end))


	def notice_p(self, string, mode='defult', fore='yellow', back=''):
		mode = '%s' % self.style['mode'][mode] if mode in self.style['mode'] else self.style['mode']['default']
		fore = '%s' % self.style['fore'][fore] if fore in self.style['fore'] else ''
		back = '%s' % self.style['back'][back] if back in self.style['back'] else ''
		style = ';'.join([s for s in [mode, fore, back] if s])
		style = '\033[%sm' % style
		end = '\033[%sm' % self.style['default']['end']

		print ("%s%s%s" % (style, string, end))


	def debug_p(self, string, mode='defult', fore='green', back=''):
		mode = '%s' % self.style['mode'][mode] if mode in self.style['mode'] else self.style['mode']['default']
		fore = '%s' % self.style['fore'][fore] if fore in self.style['fore'] else ''
		back = '%s' % self.style['back'][back] if back in self.style['back'] else ''
		style = ';'.join([s for s in [mode, fore, back] if s])
		style = '\033[%sm' % style
		end = '\033[%sm' % self.style['default']['end']

		try:
		    raise Exception
		except:
		    f = sys.exc_info()[2].tb_frame.f_back
		print ("%s%s [%s line:%s] %s%s" % (style, datetime.datetime.now(), repr(os.path.abspath(sys.argv[0])), f.f_lineno, self.name + string, end))


	def error_p(self, string, mode='defult', fore='red', back=''):
		mode = '%s' % self.style['mode'][mode] if mode in self.style['mode'] else self.style['mode']['default']
		fore = '%s' % self.style['fore'][fore] if fore in self.style['fore'] else ''
		back = '%s' % self.style['back'][back] if back in self.style['back'] else ''
		style = ';'.join([s for s in [mode, fore, back] if s])
		style = '\033[%sm' % style
		end = '\033[%sm' % self.style['default']['end']

		try:
		    raise Exception
		except:
		    f = sys.exc_info()[2].tb_frame.f_back
		print ("%s%s [%s line:%s] %s%s" % (style, datetime.datetime.now(), repr(os.path.abspath(sys.argv[0])), f.f_lineno, self.name + string, end))


	def warning_p(self, string, mode='blink', fore='red', back='black'):
		mode = '%s' % self.style['mode'][mode] if mode in self.style['mode'] else self.style['mode']['default']
		fore = '%s' % self.style['fore'][fore] if fore in self.style['fore'] else ''
		back = '%s' % self.style['back'][back] if back in self.style['back'] else ''
		style = ';'.join([s for s in [mode, fore, back] if s])
		style = '\033[%sm' % style
		end = '\033[%sm' % self.style['default']['end']

		print ("%s%s%s" % (style, string, end))


class my_cmd(Cmd):
    def __init__(self, shell):
        Cmd.__init__(self)
        self.prompt = "Let't go>"
        self.shell = shell

    def help_listnodes(self):
        P.common_p("list all the nodes")

    def do_listnodes(self, arg, opts=None):
        self.shell.send('import nodes.views')
        self.shell.send('nodes.views.listnodes()')

    def help_listgateways(self):
        P.common_p("list all the gateways")

    def do_listgateways(self, arg, opts=None):
        self.shell.send('import gateways.views')
        self.shell.send('gateways.views.listgateways()')

    def help_createrawdata(self):
        P.common_p("createrawdata timestart timeend step nodeid gatewayid")
        P.common_p("    createrawdata 2016-12-27 2017-1-8 x[mon|day|hour] 1 LO470CNSZDT001")

    def do_createrawdata(self, arg, opts=None):
        self.shell.send('import nodes.views')
        self.shell.send('nodes.views.create_rawdata(timestart="%s", timeend="%s", timestep="%s", nodeid="%s", gatewayid="%s")' % tuple(arg.split()))

    def default(self, arg, opts=None):
        try:
            subprocess.call(arg, shell=True)
        except:
            pass

    def emptyline(self):
        pass

    def help_exit(self):
        P.common_p("Will exit!")

    def do_exit(self, arg, opts=None):
        P.notice_p("It is time to say goodbye!")
        sys.exit()


class Shell():
    def __init__(self, prompt='>>>'):
        self.prompt = prompt


    def connect(self):
        self.conn = pexpect.spawn('python3 manage.py shell', encoding='utf-8', echo=False)
        self.conn.logfile = sys.stdout

        try:
            result = self.conn.expect([self.prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=5)
            if result == 0:
                P.notice_p("Shell start success!")
                return

            elif result == 1:
                P.error_p("Shell start EOF!")

            elif result == 2:
                P.error_p("Shell start timeout!")

            else:
                P.error_p("I don't know what happen!")

        except:
            P.error_p("Something wrong!!!")
            self.conn.close()
            return


    def send(self, cmd, timeout=5, prompt='>>>'):
        #P.common_p(cmd)
        self.conn.sendline(cmd)

        try:
            result = self.conn.expect([prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=timeout)
            if result == 0:
                #result = (self.conn.before).decode('utf-8')
                result = self.conn.before
                P.notice_p(result)
                return result

            else:
                P.error_p("Shell send EOF or timeout!")
                return 0

        except exception as er:
            P.error_p("Something wrong!!![%s]" % (er))
            self.conn.close()
            return 0


if __name__ == '__main__':
    P = Cprint(' ')

    #arg init
    arg_handle = arg_handle()
    arg_handle.run()


    shell = Shell()
    shell.connect()


    #cmd loop
    signal.signal(signal.SIGINT, lambda signal, frame: print("%s[32;2m%s%s[0m" % (chr(27), '\nExit CLI: CTRL+Q, Exit SYSTEM: quit!!!!', chr(27))))
    my_cmd = my_cmd(shell=shell)
    my_cmd.cmdloop()
