
def countSAT(clause,sln):
    hits = [1 if c in sln else 0 for c in clause]
    return sum(hits)

def isSAT(clause,sln):
    hits = [c in sln for c in clause]
    return True in hits
