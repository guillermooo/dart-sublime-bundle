"""Requests for the anlyzer server.
"""

class TaskPriority:
    '''Levels of priority for requests.
    '''
    HIGHEST = 0
    HIGH = 100
    DEFAULT = 200
    LOW = 300
    LOWEST = 400


def set_roots(id_, included=[], excluded=[]):
    return {"id": id_,
        "method": "analysis.setAnalysisRoots",
        "params": {
            "included": included,
            "excluded": excluded
            }
        }


def find_top_level_decls(id_, pattern):
    return {
      "id": id_,
      "method": "search.findTopLevelDeclarations",
      "params": {
        "pattern": pattern
      }
    }


def update_content(id_, files={}):
  return {
    "id": id_,
    "method": "analysis.updateContent",
    "params": {
      "files": files
    }
  }


def set_priority_files(id_, files=[]):
  return {
    "id": id_,
    "method": "analysis.setPriorityFiles",
    "params": {
      "files": files
    }
  }


def find_element_refs(id_, fname, offset, potential=False):
  return {
    "id": id_,
    "method": "search.findElementReferences",
    "params": {
      "file": fname,
      "offset": offset,
      "includePotential": potential
    }
  }
