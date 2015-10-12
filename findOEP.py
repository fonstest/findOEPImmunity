#!/usr/bin/env python

__VERSION__ = '1.0'
import immlib
import argparse
import immutils
import getopt
from immutils import *

imm = immlib.Debugger()

"""
Funcitons
"""

def CheckIntersectionJMP(inst):
  imm.log("trying to locate intersection jmp")
  return "Done"

def CheckPushAdd(inst):
  imm.log("checking push Add")

def CheckWxorX(inst):
  imm.log("checking WxorX")

"""
Main
"""

def usage():
  imm.log("!findpacker  -t --techniques Comma separed list of techbiques for find OEP:intersectionJMP,pushadd,WxorX all to use the whole set",focus=1)


def main(args):
  """arguments error handling"""
  if not args:
    usage()
    return "No args"
  try:
    opts, argo = getopt.getopt(args,"t:")
  except getopt.GetoptError:
    usage()
    return "Bad argument %s" % args[0]

  techniques = {
      "intersectionJMP" : CheckIntersectionJMP, 
      "pushadd" : CheckPushAdd,
      "WxorX" : CheckWxorX
      }
  """Parse the chosen techniques"""  
  for option,ar in opts:
    if option == "-t":
      chosenTech = ar.split(",")
  
  """Set the function that has to been executed for each instruction"""
  toExecuteTech = []
  for tec in chosenTech:
    if(techniques.get(tec) is not None):
      imm.log("Activating technique "+tec)
      toExecuteTech.append(techniques.get(tec))
    else:
      imm.log("Technique "+tec+" not found")

  for execTech in toExecuteTech:
    execTech("test")

  return "Done"








