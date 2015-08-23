from collections import defaultdict
from threading import Lock


class RequestIdManager(object):
    """
    Manages request ids for the Dart Analysis Server.
    """

    _lock = Lock()

    def __init__(self):
        self.MAX_ID = 1 << 10
        self._id = -1
        # Maps view.id's to request id's, and these to response types.
        self.request_ids = defaultdict(dict)

    def new_id(self, view, response_type):
        """
        Returns a new id for a request.

        @view
          The view from which the new request is going to be made.

        @response_type
          The type of the DAS response (result) for the new request.
        """

        with self._lock:
            if self._id >= self.MAX_ID:
                self._id = -1
            self._id += 1
            self.request_ids[view.id()][str(self._id)] = response_type
            return str(self._id)

    def validate(self, view, data):
        """
        Returns `True` if the @data originates from a known request.

        @view
          The view in which the response data was received.

        @data
          JSON raw response data from DAS.
        """

        with self._lock:
            return view and (data.get('id') in self.request_ids[view.id()])

    def get_response_type(self, view, request_id):
        """
        Returns the response (result) type for the @request_id.

        If @view+@request_id are not present, raises an error.

        @view
          View in which the response data was received.

        @request_id
          The original request id.
        """

        with self._lock:
            view_id = view.id()
            v = self.request_ids[view_id][request_id]
            del self.request_ids[view_id][request_id]
            return v
