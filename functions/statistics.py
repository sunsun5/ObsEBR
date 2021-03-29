import pandas as pd

def overlap(first_inter,second_inter):
    for f,s in ((first_inter,second_inter), (second_inter,first_inter)):

        for time in (f["hora inici"], f["hora final"]):
            if s["hora inici"] < time < s["hora final"]:
                return True
    else:
        return False