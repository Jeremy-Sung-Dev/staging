#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" convert_dec_to_hex.py

Description:
  From Lee to Everyone:  08:02 PM
  https://drive.google.com/drive/u/0/folders/1B3PprciploQlAA8BlSdrFgH3d7IQxDeG

  Problem 1: Write a function that converts an non-negative decimal integer x to its hexadecimal representation.

  For example, if the input is 10, your function shall return “A”; if the input is 15, your function shall return “F”; if the input is 1000, your function shall return “3E8”.  For more example, you could try at https://www.binaryhexconverter.com/decimal-to-hex-converter.

Attributes:
  __version__ = 12/22/2018 8:11 PM, __project__ = staging, __author__ = Jeremy Sung, __email__ = jsungcoding@gmail.com
"""

import pprint as pp

class convert_dec_to_hex:

  def __init__(self):
    ## self.hex = {i: i for i in range(10)}
    ## self.hex = { i : i for i in range(10) }.update( { 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F" } ) ## None
    ## self.hex = dict( {i: i for i in range(10)}, **{10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"} ) ## TypeError: keywords must be strings
    ## self.hex = dict( { i: i for i in range(10) }, **{"10": "A", "11": "B", "12": "C", "13": "D", "14": "E", "15": "F"})  ## worked but not useful
    self.hex = { **{i: i for i in range(10)}, **{10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"} }

  def convert_dec_to_hex(self, num):

    res = []
    print("Number comes in: {}".format(num))
    ## print("Number / 16 comes in: {}".format(num/16))  ## Number / 16 comes in: 1.0625
    ## print("Number / 16 comes in: {}".format(num >> 4))  ## Worked: return 1, i.e. 17 / 16

    ## if (num / 16) < 16:
    if (num >> 4) < 16:
      res.append( self.hex[ num % 16 ] )
      res.append( self.hex[ num >> 4 ] )

    else:

      print("num > 16: {}".format(num >> 4))

    #   res.append(self.hex[num % 16])
    #   num = num / 16
    #   print("num / 16: {}".format(num))
    #
    #   while (num / 16) >= 16:
    #
    #     res.append(self.hex[num % 16])
    #     num = num / 16
    #
    #     if ( num / 16 ) < 16:
    #       res.append(self.hex[num % 16])
    #     else:
    #       num = num / 16
    #       continue
    #
    print("".join[res])
    return res




  def convert_dec_to_hex_nums(self, *nums):
    pass


if __name__ == "__main__":

  inst_convert_dec_to_hex = convert_dec_to_hex()
  ## pp.pprint(inst_convert_dec_to_hex.hex)

  ## num = 10  ## KeyError: 10
  ## num = "10"
  num = 17
  inst_convert_dec_to_hex.convert_dec_to_hex(num)
  # print(inst_convert_dec_to_hex.convert_dec_to_hex(num))
  # nums = [10, 15, 1000]
  # print(inst_convert_dec_to_hex.convert_dec_to_hex_nums(*nums))   ## Expected: A; ["A", "F", "3E8"]
  
  