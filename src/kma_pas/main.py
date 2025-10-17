import os
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

pandas2ri.activate()

def load_rdata(path):
    # path can be relative or absolute
    loaded = ro.r['load'](path)            # returns an R character vector of names
    names = list(loaded)                   # convert to Python list of names
    objects = {}
    for name in names:
        robj = ro.globalenv[name]          # get object from R global env
        try:
            pobj = pandas2ri.rpy2py(robj) # try to convert to pandas if possible
        except Exception:
            pobj = robj                   # fallback to rpy2 object
        objects[name] = pobj
    return objects

def main():
    path = "Policie.Rdata"                 # change to the correct path if needed
    if not os.path.exists(path):
        print("File not found:", path)
        return
    objs = load_rdata(path)
    print("Loaded names:", list(objs.keys()))
    # Example: access 'Policie' if present
    if 'Policie' in objs:
        policie = objs['Policie']
        print(type(policie))
        # if it's a pandas DataFrame:
        if hasattr(policie, "head"):
            print(policie.head())
        else:
            print(policie)
    else:
        print(objs)

if __name__ == "__main__":
    main()
