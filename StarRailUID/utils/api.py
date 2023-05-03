from gsuid_core.utils.database.api import DBSqla


class SRDBSqla(DBSqla):
    def __init__(self) -> None:
        super().__init__(is_sr=True)


srdbsqla = SRDBSqla()
get_sqla = srdbsqla.get_sqla
