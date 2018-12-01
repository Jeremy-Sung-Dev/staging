#!C:\staging\python\systems\Scripts\python.exd

import pandas as pd


if __name__ == "__main__":

  # text1 = "some text here"
  # text2 = "other text here"
  # df = pd.DataFrame({"a": [1,2,3,4,5], "b": [6,7,8,9,10], "conn": [11,12,13,14,15]})
  #
  # writer = pd.ExcelWriter("test.xlsx")
  # df.to_excel(writer, startrow=4, startcol=0)
  #
  # worksheet = writer.sheets['Sheet1']
  # worksheet.write(0, 0, text1)
  # worksheet.write(1, 0, text2)
  # #another solution
  # #worksheet.write_string(0, 0, text1)
  # #worksheet.write_string(1, 0, text2)
  #
  # writer.save()

  # Create a Pandas dataframe from some data.
  df1 = pd.DataFrame({'Data': [10, 20, 30, 40]})
  df2 = df1.T

  # Create a Pandas Excel writer using XlsxWriter as the engine.
  writer = pd.ExcelWriter('test2.xlsx', engine='xlsxwriter')

  # Write the data in column and transposed (row) directions.
  df1.to_excel(writer, sheet_name='Sheet1',
               startrow=1, startcol=1, header=False, index=False)

  df2.to_excel(writer, sheet_name='Sheet1',
               startrow=1, startcol=3, header=False, index=False)

  # Close the Pandas Excel writer and output the Excel file.
  writer.save()