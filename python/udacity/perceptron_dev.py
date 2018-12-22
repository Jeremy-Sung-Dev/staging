#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" perceptron_dev.py

Description:
  Challenges:
  Solutions:

Attributes:
  __version__ = 12/21/2018 1:25 PM, __project__ = staging, __author__ = Jeremy Sung, __email__ = jsungcoding@gmail.com
"""

import pandas as pd


class perceptron_dev:

  def __init__(self, **perceptron_AND_parameters):
    self.weight1 = perceptron_AND_parameters["weight1"]
    self.weight2 = perceptron_AND_parameters["weight2"]
    self.bias = perceptron_AND_parameters["bias"]

  def perceptron_dev(self, test_inputs, correct_outputs):

    # ## Inputs and outputs
    # test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    # correct_outputs = [False, False, False, True]
    outputs = []

    # Generate and check output
    for test_input, correct_output in zip(test_inputs, correct_outputs):
      linear_combination = self.weight1 * test_input[0] + self.weight2 * test_input[1] + self.bias
      ## linear_combination = round(self.weight1 * test_input[0], 3) + round(self.weight2 * test_input[1], 3) + self.bias

      ## output = int(linear_combination >= 0.0)
      output = True if linear_combination >= 0.0 else False
      is_correct_string = 'Yes' if output == correct_output else 'No'

      outputs.append([test_input[0], test_input[1], linear_combination, output, is_correct_string])

    # Print output
    self.num_wrong = len([output[4] for output in outputs if output[4] == 'No'])
    output_frame = pd.DataFrame(outputs, columns=['Input 1', '  Input 2', '  Linear Combination', '  Activation Output',
                                                  '  Is Correct'])

    if not self.num_wrong:
      print('Nice!  You got it all correct.')
      ## print('Nice!  You got it all correct.\n')
    else:
      print('Keep trying!')
      ## print('You got {} wrong.  Keep trying!\n'.format(self.num_wrong))

    print(output_frame.to_string(index=False))


  def perceptron_dy_dev(self, test_inputs, correct_outputs, learning_rate=-0.1):

    self.perceptron_dev(test_inputs, correct_outputs)
    count = 1.0

    while self.num_wrong and count <= 100:
      count += 1.0

      self.weight1 += test_inputs[0][0] * learning_rate
      self.weight2 += test_inputs[0][1] * learning_rate
      self.bias += learning_rate

      print("\nNext Round: {}: weight1:{}, weight2:{}, bias:{}".format(int(count), round(self.weight1, 3), round(self.weight2, 3), round(self.bias, 3)))

      self.perceptron_dev(test_inputs, correct_outputs)

    print("Times: {}".format(count))


if __name__ == "__main__":

  ### --- Dynamically come closer to the line  -----------------###

  perceptron_Dy_parameters = { "weight1" : 3.0, "weight2" : 4.0, "bias" : -10.0 }
  perceptron_Dy = perceptron_dev(**perceptron_Dy_parameters)

  ## test_inputs = [(4, 5)]
  test_inputs = [(1, 1)]
  correct_outputs = [True]
  ## correct_outputs = [False]  ## I want to move the line, i.e. the point, to the other side of the line.
  ## learning_rate = -0.1
  learning_rate = 0.1

  perceptron_Dy.perceptron_dy_dev(test_inputs, correct_outputs, learning_rate)

  # ### -------------------------------------------------------###
  #
  # perceptron_OR_parameters = { "weight1" : 1.0, "weight2" : 1.0, "bias" : -0.5 }
  # perceptron_OR = perceptron_dev(**perceptron_OR_parameters)
  #
  # test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
  # correct_outputs = [False, True, True, True]
  # learning_rate = 1
  #
  # perceptron_OR.perceptron_dev(test_inputs, correct_outputs)
  #
  # ### -------------------------------------------------------###
  # perceptron_AND_parameters = { "weight1" : 1.0, "weight2" : 1.0, "bias" : -1.5 }
  # perceptron_AND = perceptron_dev(**perceptron_AND_parameters)
  #
  # test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
  # correct_outputs = [False, False, False, True]
  # learning_rate = 1
  #
  # perceptron_AND.perceptron_dev(test_inputs, correct_outputs)
  #
  # ### -------------------------------------------------------###
  #
  # ### -------------------------------------------------------###


  