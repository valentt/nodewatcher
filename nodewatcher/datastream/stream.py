import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class DataStream(object):
  def __init__(self):
    """
    Class constructor.
    """
    self.backend = None

    # Load the backend as specified in configuration
    if getattr(settings, "DATA_STREAM_BACKEND", None) is not None:
      try:
        module = importlib.import_module(settings.DATA_STREAM_BACKEND)
        self.backend = getattr(module, "Backend")()
      except (ImportError, AttributeError):
        raise ImproperlyConfigured("Error importing data stream backend %s!" % settings.DATA_STREAM_BACKEND)

  def insert(self, metric_uri, tags, value):
    """
    Inserts a data point into the timestamped data stream.

    :param metric_uri: Unique metric identifier
    :param tags: Metric tags
    :param value: Metric value
    """
    if not self.backend:
      return

    return self.backend.insert(metric_uri, tags, value)

  def get_data(self, metric_uri, granularity, start, end):
    """
    Performs a query against the data stream and returns the
    results.

    :param metric_uri: Unique metric identifier
    :param granularity: Wanted data granularity
    :param start: Start timestamp
    :param end: End timestamp
    :return: A list of resulting datapoints, sorted by time
    """
    if not self.backend:
      return []

    return self.backend.get_data(metric_uri, granularity, start, end)

  def get_metrics(self, tags):
    """
    Returns the metrics that match the specified tags.

    :param tags: A dictionary of tags to match
    :return: A list of metrics
    """
    if not self.backend:
      return []

    return self.backend.get_metrics(tags)

stream = DataStream()
