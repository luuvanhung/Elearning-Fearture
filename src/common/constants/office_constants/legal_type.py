from common.constants.base_const import Const

__all__ = ["LegalTypeConst"]


class LegalTypeConst(Const):
    # get these legal types from url: https://en.wikipedia.org/wiki/List_of_legal_entity_types_by_country#Vietnam
    LEGAL_TYPES = (
        "Company with Limited Liability",
        "Limited Liability Company with a Single member",
        "Company with Joint Stock",
        "Company of Partners",
        "Enterprise Partnership",
        "Enterprise of the State",
        "Enterprise Private",
        "Enterprise with Foreign Investment",
        "Co-operation",
        "Branch Company",
        "Group Company",
    )
