i=1
for (file in list.files('/Users/julian/Code/RPS/NREL Data')) 
{
  s[i] <-data.frame(read.csv('/Users/julian/Code/RPS/NREL Data/'+file,skip = 55,sep='\t'))
}