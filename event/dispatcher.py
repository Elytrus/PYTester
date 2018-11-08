from collections import defaultdict


class Dispatcher:
    def __init__(self):
        """
        Constructor for event.dispatcher.Dispatcher
        """

        self.handlers = defaultdict(list)

    def register(self, event_type, handler):
        """
        Registers a handler to event type `event_type`

        :param event_type: Event type to bind to
        :type event_type: class
        :param handler: Handler to register
        :type handler: function
        :return: Nothing
        :rtype: NoneType
        """

        self.handlers[event_type].append(handler)

    def dispatch(self, event):
        """
        Dispatches the event `event`

        :param event: The event that is being dispatched
        :type event: object
        :return: Nothing
        :rtype: NoneType
        """

        for handler in self.handlers[type(event)]:
            handler(event)
