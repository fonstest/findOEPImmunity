#!/usr/bin/env python

__VERSION__ = '1.0'
import immlib
import argparse
import immutils
import getopt
import pelib
import pefile
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

def getEPsection(pe,rva):
  """returns the section that contains the entry point, -1 if none"""
  for i,s in enumerate(pe.sections):
      if s.contains_rva(rva):
          break
  else: return -1
  return i



"""load PE, return pe object, it's entry point, imagebase, VA of the section of the entry point, its physical size"""
def loadPE():
  try:
    name = imm.getDebuggedName()
    module  = imm.getModule(name)
    if not module:
      raise Exception, "Couldn't find %s .." % name
      return False
  except Exception,e:
    imm.log('module %s not found'%(name))
    return False
  
  start = module.getBaseAddress()
  size = module.getSize()
  data = imm.readMemory(start, size)


  pe = pefile.PE(data=data)
  oep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
  ib = pe.OPTIONAL_HEADER.ImageBase
  section = pe.sections[getEPsection(pe,oep)]
  start, size = section.VirtualAddress, section.SizeOfRawData

  return pe, oep, ib, start, size

def displaySections(pe):
  for i,section in enumerate(pe.sections):
    imm.log("%s %s %s %s"%(i, hex(section.VirtualAddress+ib), hex(section.Misc_VirtualSize), hex(section.SizeOfRawData )))

"""
Main
"""

def usage():
  imm.log("!findpacker  -t --techniques Comma separed list of techbiques for find OEP:intersectionJMP,pushadd,WxorX all to use the whole set",focus=1)




def main(args):
  """arguments error handling"""
  imm.log("dsadsa")
  pe,oep,ib,start,size = loadPE()
  for i,section in enumerate(pe.sections):
    imm.log("%s %s %s %s"%(i, hex(section.VirtualAddress+ib), hex(section.Misc_VirtualSize), hex(section.SizeOfRawData )))
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








