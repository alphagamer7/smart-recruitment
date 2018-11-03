
class APILengthError(Exception):

    def __init__(self, text, count):
        super().__init__(text)
        self._count = count

    @property
    def sides(self):
        return self._count

    def __str__(self):
        return "'{}' for for analysing Profile {}".format(self.args[0], self._count)

    def __repr__(self):
        return "TriangleError({!r}, {!r}".format(self.args[0], self._count)

    def test_api_error(count):
        if count < 100:
            raise APILengthError("Need minimum of ", count)

try:
    APILengthError.test_api_error(5)
except APILengthError as e:
    print("Raised Exception")

