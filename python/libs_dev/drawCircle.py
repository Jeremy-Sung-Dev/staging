#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" drawCircle.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/5/2018 4:26 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import turtle

class drawCircle:

  ## http://interactivepython.org/runestone/static/CS152f17/Labs/lab04_01a.html
  def drawPolygon(self, t, sideLength, numSides):
    turnAngle = 360 / numSides
    for i in range(numSides):
      t.forward(sideLength)
      t.right(turnAngle)


  def drawCircle(self, anyTurtle, radius):
    circumference = 2 * 3.1415 * radius
    sideLength = circumference / 360
    self.drawPolygon(anyTurtle, sideLength, 360)



  def drawCircle_By_Hand(self):
    """ Does not reply on Turtle """
    width, height = 11, 11
    a, b = 5, 5
    r = 5
    EPSILON = 2.2

    map_ = [['.' for x in range(width)] for y in range(height)]

    ## draw the circle
    for y in range(height):
      for x in range(width):
        # see if we're close to (x-a)**2 + (y-b)**2 == r**2
        if abs((x - a) ** 2 + (y - b) ** 2 - r ** 2) < EPSILON ** 2:
          map_[y][x] = '#'

    # print the map
    for line in map_:
      print(' '.join(line))


if __name__ == "__main__":

  drawCircle = drawCircle()

  ## http://interactivepython.org/runestone/static/CS152f17/Labs/lab04_01a.html
  wn = turtle.Screen()
  wheel = turtle.Turtle()
  drawCircle.drawCircle(wheel, 20)


  ## Draw By Hand:
  ## drawCircle.drawCircle()


  # ## Testing:
  # width = 5
  # height = 10
  #
  # ## 2D
  # # for i in [['.' for x in range(width)] for y in range(height)]:
  # #   print(i)
  #
  # ## 1D
  # # for i in ['.' for x in range(width) for y in range(height)]:
  # #   print(i)


