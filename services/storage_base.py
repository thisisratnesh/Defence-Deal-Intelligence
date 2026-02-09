# This base class defines common interface for all storage backends


class StorageWriter:
    """
    Base storage interface.
    All storage implementations must follow this contract.
    """

    def save_structured_deals(self, structured_deals: list):
        """
        Save structured deals to storage.

        :param structured_deals: List of structured deal dictionaries
        """
        raise NotImplementedError("Subclasses must implement save_structured_deals()")
