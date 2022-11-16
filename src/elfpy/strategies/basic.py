"""
Base policy class

Policies inherit from Users (thus each policy is assigned to a user)
subclasses of BasicPolicy will implement trade actions
"""


from elfpy.user import User


class BasicPolicy(User):
    """
    most basic policy setup
    """

    def __init__(self, market, rng, budget=1000, verbose=False):
        """call basic policy init then add custom stuff"""
        super().__init__(market=market, rng=rng, budget=budget, verbose=verbose)

    def action(self):
        """specify action"""
        action_list = []
        # implement trade here
        return action_list
