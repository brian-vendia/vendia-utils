from enum import Enum


class Action(Enum):
    """The action enum contains all possible actions generated for customers."""

    ADD = "add"
    CREATE = "create"
    DELETE = "delete"
    GET = "get"
    LIST = "list"
    ON_ADD = "onAdd"
    ON_CREATE = "onCreate"
    ON_DELETE = "onDelete"
    ON_REMOVE = "onRemove"
    ON_UPDATE = "onUpdate"
    PUT = "put"
    REMOVE = "remove"
    UPDATE = "update"

    def __str__(self) -> str:
        # wrap value with `str()` to appease pylint
        return str(self.value)

    def is_update(self) -> bool:
        """Returns true if the action is updating an object in the ledger"""
        return self in {Action.UPDATE, Action.PUT}

    def is_object_mutation(self) -> bool:
        """Returns true if the action mutates an existing object in the ledger.

        This function tracks all of the actions that can be applied to an existing object
        in the world state.
        """
        return self in {Action.DELETE, Action.UPDATE, Action.PUT, Action.REMOVE}

    def is_graphql_mutation(self) -> bool:
        """Returns true if the action applies to a mutation graphql query."""
        return self in {Action.ADD, Action.CREATE, Action.DELETE, Action.UPDATE, Action.PUT, Action.REMOVE}

    def is_subscription(self) -> bool:
        """Returns true if the action is a subscription operation."""
        return self in {Action.ON_ADD, Action.ON_CREATE, Action.ON_DELETE, Action.ON_REMOVE, Action.ON_UPDATE}

    def is_delete(self) -> bool:
        """Returns true if the action deletes objects from world state"""
        return self in {Action.DELETE, Action.REMOVE}
