"""Requests for the anlyzer server.
"""

def set_roots(id_, included=[], excluded=[]):
    return {"id": id_,
        "method": "analysis.setAnalysisRoots",
        "params": {
            "included": included,
            "excluded": excluded
            }
        }
