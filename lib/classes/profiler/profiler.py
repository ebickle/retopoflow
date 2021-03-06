'''
Copyright (C) 2015 CG Cookie
http://cgcookie.com
hello@cgcookie.com

Created by Jonathan Denning, Jonathan Williamson, and Patrick Moore

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import inspect
import time
from ...common_utilities import dprint, dcallstack

class Profiler(object):
    class ProfilerHelper(object):
        def __init__(self, pr, text):
            full_text = (pr.stack[-1].text+'^' if pr.stack else '') + text
            assert full_text not in pr.d_start, '"%s" found in profiler already?'%text
            self.pr = pr
            self.text = full_text
            self._is_done = False
            self.pr.d_start[self.text] = time.time()
            self.pr.stack += [self]
        def __del__(self):
            if not self._is_done:
                dprint('WARNING: calling ProfilerHelper.done!')
                self.done()
        def done(self):
            assert self.pr.stack[-1] == self
            assert not self._is_done
            self.pr.stack.pop()
            self._is_done = True
            st = self.pr.d_start[self.text]
            en = time.time()
            self.pr.d_times[self.text] = self.pr.d_times.get(self.text,0) + (en-st)
            self.pr.d_count[self.text] = self.pr.d_count.get(self.text,0) + 1
            del self.pr.d_start[self.text]
    
    def __init__(self):
        self.d_start = {}
        self.d_times = {}
        self.d_count = {}
        self.stack = []
    
    def start(self, text=None):
        if not text:
            frame = inspect.currentframe().f_back
            filename = os.path.basename( frame.f_code.co_filename )
            linenum = frame.f_lineno
            fnname = frame.f_code.co_name
            text = '%s (%s:%d)' % (fnname, filename, linenum)
        return self.ProfilerHelper(self, text)
    
    def __del__(self):
        #self.printout()
        pass
    
    def printout(self):
        dprint('Profiler:')
        for text in sorted(self.d_times):
            tottime = self.d_times[text]
            totcount = self.d_count[text]
            calls = text.split('^')
            if len(calls) == 1:
                t = text
            else:
                t = '    '*(len(calls)-2) + ' \\- ' + calls[-1]
            dprint('  %6.2f / %3d = %6.2f - %s' % (tottime, totcount, tottime/totcount, t))
        dprint('')

profiler = Profiler()