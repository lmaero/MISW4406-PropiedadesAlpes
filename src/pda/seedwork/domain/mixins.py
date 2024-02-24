from .exceptions import BusinessRuleException
from .rules import BusinessRule


class ValidateMixinRules:
    def validate_rule(self, rule: BusinessRule):
        if not rule.is_valid():
            raise BusinessRuleException(rule)
