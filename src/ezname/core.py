import random
from typing import Final, TypeAlias

from ezname.fixtures import ADJECTIVES, NOUNS

DEFAULT_DELIMITER: Final[str] = "-"

Prefix: TypeAlias = str | None
Suffix: TypeAlias = str | None
Delimiter: TypeAlias = str


def concatenate(
    adjective: str,
    noun: str,
    prefix: Prefix = None,
    suffix: Suffix = None,
    delimiter: Delimiter = DEFAULT_DELIMITER,
) -> str:
    ret = f"{adjective}{delimiter}{noun}"
    if prefix:
        ret = f"{prefix}{delimiter}{ret}"
    if suffix:
        ret = f"{ret}{delimiter}{suffix}"
    return ret


def generate(
    prefix: Prefix = None,
    suffix: Suffix = None,
    delimiter: Delimiter = DEFAULT_DELIMITER,
    as_tuple: bool = False,
    seed: int | None = None,
) -> str | tuple[str, str]:
    """
    Generate a random name in the format adjective-noun.

    Args:
        prefix: Optional prefix to add before the adjective-noun.
        suffix: Optional suffix to add after the adjective-noun.
        delimiter: String used to separate components of the name.
        as_tuple: If True, returns (adjective, noun) as a tuple instead of a string.
        seed: Optional random seed for reproducible generation.

    Returns:
        A string in the format "prefix-adjective-noun-suffix"
        (if prefix/suffix provided) or a tuple (adjective, noun) if as_tuple is True.
    """
    # Set random seed if provided
    if seed is not None:
        random_state = random.Random(seed)
        noun = random_state.choice(NOUNS)
        adjective = random_state.choice(ADJECTIVES)
    else:
        noun = random.choice(NOUNS)
        adjective = random.choice(ADJECTIVES)

    if as_tuple:
        if prefix or suffix or delimiter != DEFAULT_DELIMITER:
            raise ValueError(
                "as_tuple is True, so prefix, suffix, "
                "and delimiter must not be provided"
            )
        return adjective, noun

    return concatenate(adjective, noun, prefix, suffix, delimiter)


def generate_batch(
    n: int,
    prefix: Prefix = None,
    suffix: Suffix = None,
    delimiter: Delimiter = DEFAULT_DELIMITER,
    as_tuple: bool = False,
    seed: int | None = None,
) -> list[str] | list[tuple[str, str]]:
    """
    Generate a list of random names.

    Args:
        n: Number of names to generate.
        prefix: Optional prefix to add before each adjective-noun.
        suffix: Optional suffix to add after each adjective-noun.
        delimiter: String used to separate components of each name.
        as_tuple: If True, returns list of (adjective, noun) tuples instead of strings.
        seed: Optional random seed for reproducible generation.

    Returns:
        A list of strings or tuples based on the as_tuple parameter.
    """
    if seed is not None:
        # Initialize a random state with the seed
        random_state = random.Random(seed)
        return [
            generate(
                prefix, suffix, delimiter, as_tuple, random_state.randint(0, 2**32 - 1)
            )
            for _ in range(n)
        ]
    else:
        return [generate(prefix, suffix, delimiter, as_tuple) for _ in range(n)]


class EzName:
    def __init__(
        self,
        names: list[str] | list[tuple[str, str]] | None = None,
        seed: int | None = None,
    ):
        if names is None:
            names = []
        assert len(set(names)) == len(names), "names must be unique"
        if all(isinstance(name, str) for name in names):
            self.as_tuple = False
        elif all(isinstance(name, tuple) for name in names):
            self.as_tuple = True
        else:
            raise ValueError("names must be a list of strings or tuples")

        self.names = self.to_string_batch(names)
        self.seed = seed
        self._iterator = None

    def __iter__(self):
        self._iterator = iter(self.names)
        return self

    def __next__(self) -> str | tuple[str, str]:
        if self._iterator is None:
            self._iterator = iter(self.names)
        return next(self._iterator)

    def __len__(self):
        return len(self.names)

    def __getitem__(self, index: int) -> str | tuple[str, str]:
        return self.names[index]

    def generate(
        self,
        prefix: Prefix = None,
        suffix: Suffix = None,
        delimiter: Delimiter = DEFAULT_DELIMITER,
        as_tuple: bool = False,
        seed: int | None = None,
    ) -> str | tuple[str, str]:
        if seed is None:
            seed = self.seed

        random_state = random.Random(seed)
        for adj in random_state.sample(ADJECTIVES, len(ADJECTIVES)):
            for noun in random_state.sample(NOUNS, len(NOUNS)):
                if as_tuple:
                    name = (adj, noun)
                else:
                    name = concatenate(adj, noun, prefix, suffix, delimiter)
                if self.to_string(name) not in self.names:
                    self.names.append(name)
                    return name
        raise ValueError("All names have been exhausted")

    @staticmethod
    def to_tuple(
        name: str | tuple[str, str] | None = None,
        delimiter: Delimiter = DEFAULT_DELIMITER,
    ) -> tuple[str, str]:
        if name is None:
            return ("", "")
        elif isinstance(name, str):
            parts = name.split(delimiter)
            if len(parts) < 2:
                return ("", parts[0] if parts else "")
            elif len(parts) > 2:
                return (parts[0], delimiter.join(parts[1:]))
            return tuple(parts)
        else:
            return name

    @staticmethod
    def to_string(
        name: str | tuple[str, str] | None = None,
        delimiter: Delimiter = DEFAULT_DELIMITER,
    ) -> str:
        if name is None:
            return ""
        elif isinstance(name, str):
            return name
        else:
            return delimiter.join(name)

    @staticmethod
    def to_tuple_batch(
        names: list[str] | None = None,
        delimiter: Delimiter = DEFAULT_DELIMITER,
    ) -> list[tuple[str, str]]:
        if names is None:
            return []
        elif all(isinstance(name, str) for name in names):
            return [tuple(name.split(delimiter)) for name in names]
        else:
            return names

    @staticmethod
    def to_string_batch(
        names: list[str] | list[tuple[str, str]] | None = None,
        delimiter: Delimiter = DEFAULT_DELIMITER,
    ) -> list[str]:
        if names is None:
            return []
        elif all(isinstance(name, str) for name in names):
            return names
        else:
            return [delimiter.join(name) for name in names]
