from errors.main import ExtendableError, INSERT_FAILED

class InsertFailed(ExtendableError):
  def __init__(self, code=..., info="Insert into database failed"):
    super().__init__(INSERT_FAILED, info)