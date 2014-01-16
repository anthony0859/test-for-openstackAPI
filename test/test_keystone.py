import os
import sys

reldir = os.path.join(os.path.dirname(__file__), '..')
absdir = os.path.abspath(reldir)
sys.path.append(absdir)

from keystone import keystone

