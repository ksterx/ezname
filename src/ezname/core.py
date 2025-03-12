import random
from typing import Final, TypeAlias

from ezname.fixtures import ADJECTIVES, NOUNS

DEFAULT_DELIMITER: Final[str] = "-"

Prefix: TypeAlias = str | None
Suffix: TypeAlias = str | None
Delimiter: TypeAlias = str


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

    ret = f"{adjective}{delimiter}{noun}"
    if prefix:
        ret = f"{prefix}{delimiter}{ret}"
    if suffix:
        ret = f"{ret}{delimiter}{suffix}"
    return ret


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
