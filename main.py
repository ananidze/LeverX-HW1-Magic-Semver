import re
from functools import total_ordering


@total_ordering
class Version:
    _semver_regex = re.compile(
        r"^(?P<major>0|[1-9]\d*)\."
        r"(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    def __init__(self, version):
        normalized_version = re.sub(r"(\d)([a-zA-Z])", r"\1-\2", str(version))

        match = self._semver_regex.match(normalized_version)
        if not match:
            raise ValueError(f"Invalid version string: '{version}'")

        self.major = int(match.group("major"))
        self.minor = int(match.group("minor"))
        self.patch = int(match.group("patch"))

        if prerelease := match.group("prerelease"):
            self.prerelease = tuple(
                int(i) if i.isdigit() else i for i in prerelease.split(".")
            )
        else:
            self.prerelease = ()

    def __eq__(self, other):
        if not isinstance(other, Version):
            raise NotImplementedError("Comparison not supported between instances of 'Version' and other types")

        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __lt__(self, other):
        if not isinstance(other, Version):
            raise NotImplementedError("Comparison not supported between instances of 'Version' and other types")

        core_self = (self.major, self.minor, self.patch)
        core_other = (other.major, other.minor, other.patch)
        if core_self != core_other:
            return core_self < core_other

        if self.prerelease and not other.prerelease:
            return True
        if not self.prerelease and other.prerelease:
            return False
        if not self.prerelease and not other.prerelease:
            return False

        for self_id, other_id in zip(self.prerelease, other.prerelease):
            self_is_int = isinstance(self_id, int)
            other_is_int = isinstance(other_id, int)

            if self_is_int and not other_is_int:
                return True
            if not self_is_int and other_is_int:
                return False

            if self_id != other_id:
                return self_id < other_id

        return len(self.prerelease) < len(other.prerelease)


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), "le failed"
        assert Version(right) > Version(left), "ge failed"
        assert Version(right) != Version(left), "neq failed"


if __name__ == "__main__":
    main()
