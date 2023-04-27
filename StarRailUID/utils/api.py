from gsuid_core.utils.database.api import DBSqla


class SRDBSqla(DBSqla):
    def __init__(self) -> None:
        super().__init__(is_sr=True)


get_sqla = SRDBSqla().get_sqla
