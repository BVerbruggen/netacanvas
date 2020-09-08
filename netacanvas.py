#use pandas module for data manipulation using dataframes
import pandas as pd

# read netacad and canvas gradebook export csv files into dataframes, keep useful columns and rename headers, drop NaN rows (students with no score registered)
netacad = (pd.read_csv("netacad.csv", usecols = [0,3,24], skiprows = [1], header=0, names = ["Netacad Name","StudentID", "Netacad Score"])).dropna()
canvas = (pd.read_csv("canvas.csv", usecols = [0,3,16], skiprows = [1], header=0, names = ["Canvas Name","StudentID", "Canvas Score"])).dropna()


#outer merge of both tables on StudentID
netacad_canvas_merge = netacad.merge(canvas, how = 'outer', on = "StudentID")
#store only the students who have a null (NaN) score in either netacad or canvas
output = netacad_canvas_merge[netacad_canvas_merge.isnull().any(1)]
print(output)
#write to output.csv file
output.to_csv('output.csv',index=False)
print("Written result to output.csv.")


