from common.constants.base_const import Const

__all__ = ["ApplicationChoice"]


class ApplicationChoice(Const):

    CLIENT_CONFIDENTIAL = "confidential"
    CLIENT_PUBLIC = "public"
    CLIENT_TYPES = (CLIENT_CONFIDENTIAL, CLIENT_PUBLIC)

    GRANT_AUTHORIZATION_CODE = "authorization-code"
    GRANT_IMPLICIT = "implicit"
    GRANT_PASSWORD = "password"
    GRANT_CLIENT_CREDENTIALS = "client-credentials"
    GRANT_OPENID_HYBRID = "openid-hybrid"
    GRANT_TYPES = (
        GRANT_AUTHORIZATION_CODE,
        GRANT_IMPLICIT,
        GRANT_PASSWORD,
        GRANT_CLIENT_CREDENTIALS,
        GRANT_OPENID_HYBRID,
    )

    NO_ALGORITHM = ""
    RS256_ALGORITHM = "RS256"
    HS256_ALGORITHM = "HS256"
    ALGORITHM_TYPES = (NO_ALGORITHM, RS256_ALGORITHM, HS256_ALGORITHM)
