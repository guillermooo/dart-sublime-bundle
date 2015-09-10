from threading import Lock


class AutocompleteContext(object):
    '''
    An autocomplete context.

    Singleton.
    '''

    def __init__(self):
        self.lock = Lock()
        self._is_open = False
        self._id = None
        self._request_id = None
        self._results = []
        self._formatted_results = []
        self.coords = None

    def __enter__(self):
        self.lock.acquire()
        self._is_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        self._is_open = False

    @property
    def id(self):
        assert self._is_open, 'must open context first -- use as a context manager'
        return self._id

    @id.setter
    def id(self, value):
        assert self._is_open, 'must open context first -- use as a context manager'
        self._id = value

    @property
    def request_id(self):
        assert self._is_open, 'must open context first -- use as a context manager'
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        assert self._is_open, 'must open context first -- use as a context manager'
        self._request_id = value

    @property
    def results(self):
        assert self._is_open, 'must open context first -- use as a context manager'
        return self._results

    @results.setter
    def results(self, value):
        assert self._is_open, 'must open context first -- use as a context manager'
        self._results = value

    def set_results(self, view, value):
        self.results = value
        self.coords = view.sel()[0]

    @property
    def formatted_results(self):
        return self._formatted_results

    @formatted_results.setter
    def formatted_results(self, value):
        self._formatted_results = value

    def invalidate(self):
        assert self._is_open, 'must open context first -- use as a context manager'
        self.invalidate_results()
        self._request_id = None
        self._id = None

    def invalidate_results(self):
        assert self._is_open, 'must open context first -- use as a context manager'
        self._results = []
        self._formatted_results = []

    def should_hide_auto_complete_list(self, view):
        s0 = view.sel()[0]
        return s0 < self.coords


