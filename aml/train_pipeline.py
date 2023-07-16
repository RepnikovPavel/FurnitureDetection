from typing import Dict,List,Any,Tuple
def DictToListOfPairs(dict:Dict[str,Any])->List[Tuple[str,Any]]:
    # input: key-value table 
    # output: array of pairs <key,value>
    out_=  []
    for k,v in dict.items():
        out_.append((k,v))
    return out_

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

