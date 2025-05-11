import sys;

def add(a, b, c):
  return a * b*c*4
 
if __name__ == "__main__":
  a = int(sys.argv[1])
  b = int(sys.argv[2])
  c = int(sys.argv[3])
  result = int(sys.argv[4])
  print(add(a, b,c) == result)

