import unittest

from app.main.util.data_validation import validate_region_name


class TestCorrectRegionValidation(unittest.TestCase):

    def test_correct_region_validation(self):

        correct_region_simple = "Argentina"
        correct_region_with_spaces = "United%20Kingdom"
        correct_region_with_hiphen = "timor-leste"

        self.assertTupleEqual(
            (True, "Argentina", None),
            validate_region_name(correct_region_simple)
        )

        self.assertTupleEqual(
            (True, "United Kingdom", None),
            validate_region_name(correct_region_with_spaces)
        )

        self.assertTupleEqual(
            (True, "timor-leste", None),
            validate_region_name(correct_region_with_hiphen)
        )


class TestIncorrectRegionValidation(unittest.TestCase):

    def test_incorrect_region_validation(self):

        no_region_informed = None
        empty_region = ""
        region_with_number = "timor-leste123456"

        self.assertTupleEqual(
            (False, None, "'region' parameter must be informed"),
            validate_region_name(no_region_informed)
        )

        self.assertTupleEqual(
            (
                False,
                "",
                " ".join([
                    "'region' must be a non-empty string",
                    "containing a valid country name",
                    "(letters, whitespaces and hiphen only)"
                ])
            ),
            validate_region_name(empty_region)
        )

        self.assertTupleEqual(
            (
                False,
                "timor-leste123456",
                " ".join([
                    "'region' must be a non-empty string",
                    "containing a valid country name",
                    "(letters, whitespaces and hiphen only)"
                ])
            ),
            validate_region_name(region_with_number)
        )


if __name__ == '__main__':
    unittest.main()
