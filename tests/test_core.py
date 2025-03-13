import pytest

from ezname.core import EzName, concatenate, generate, generate_batch


def test_concatenate():
    assert concatenate("happy", "cat") == "happy-cat"
    assert concatenate("happy", "cat", prefix="test") == "test-happy-cat"
    assert concatenate("happy", "cat", suffix="v1") == "happy-cat-v1"
    assert concatenate("happy", "cat", delimiter="_") == "happy_cat"
    assert (
        concatenate("happy", "cat", prefix="test", suffix="v1", delimiter="_")
        == "test_happy_cat_v1"
    )


def test_generate():
    # Basic generation
    name = generate()
    assert isinstance(name, str)
    assert "-" in name

    # With prefix and suffix
    name = generate(prefix="test", suffix="v1")
    assert name.startswith("test-")
    assert name.endswith("-v1")

    # With custom delimiter
    name = generate(delimiter="_")
    assert "_" in name
    assert "-" not in name

    # As tuple
    name = generate(as_tuple=True)
    assert isinstance(name, tuple)
    assert len(name) == 2
    assert all(isinstance(x, str) for x in name)

    # With seed
    name1 = generate(seed=42)
    name2 = generate(seed=42)
    assert name1 == name2


def test_generate_batch():
    # Basic batch generation
    names = generate_batch(3)
    assert len(names) == 3
    assert all(isinstance(name, str) for name in names)
    assert all("-" in name for name in names)

    # With prefix and suffix
    names = generate_batch(3, prefix="test", suffix="v1")
    assert all(name.startswith("test-") for name in names)
    assert all(name.endswith("-v1") for name in names)

    # With custom delimiter
    names = generate_batch(3, delimiter="_")
    assert all("_" in name for name in names)
    assert all("-" not in name for name in names)

    # As tuple
    names = generate_batch(3, as_tuple=True)
    assert all(isinstance(name, tuple) for name in names)
    assert all(len(name) == 2 for name in names)
    assert all(all(isinstance(x, str) for x in name) for name in names)

    # With seed
    names1 = generate_batch(3, seed=42)
    names2 = generate_batch(3, seed=42)
    assert names1 == names2


class TestEzName:
    def test_init(self):
        # Empty initialization
        namer = EzName()
        assert len(namer) == 0

        # Initialize with string names
        namer = EzName(["happy-cat", "sad-dog"])
        assert len(namer) == 2
        assert all(isinstance(name, str) for name in namer.names)

        # Initialize with tuple names
        namer = EzName([("happy", "cat"), ("sad", "dog")])
        assert len(namer) == 2

        # Test duplicate names
        with pytest.raises(AssertionError):
            EzName(["happy-cat", "happy-cat"])

        # Test mixed types
        with pytest.raises(ValueError):
            EzName(["happy-cat", ("sad", "dog")])

    def test_iteration(self):
        names = ["happy-cat", "sad-dog"]
        namer = EzName(names)

        # Test iteration
        assert list(namer) == names

        # Test multiple iterations
        assert list(namer) == names
        assert list(namer) == names

    def test_indexing(self):
        names = ["happy-cat", "sad-dog"]
        namer = EzName(names)

        assert namer[0] == "happy-cat"
        assert namer[1] == "sad-dog"
        with pytest.raises(IndexError):
            _ = namer[2]

    def test_generate(self):
        namer = EzName(["happy-cat"])

        # Basic generation
        name = namer.generate()
        assert isinstance(name, str)
        assert name != "happy-cat"

        # With prefix and suffix
        name = namer.generate(prefix="test", suffix="v1")
        assert name.startswith("test-")
        assert name.endswith("-v1")
        assert name != "test-happy-cat-v1"

        # As tuple
        name = namer.generate(as_tuple=True)
        assert isinstance(name, tuple)
        assert len(name) == 2
        assert name != ("happy", "cat")

        # With seed
        name1 = namer.generate(seed=42)
        name2 = namer.generate(seed=42)
        assert name1 == name2

    def test_to_tuple(self):
        # Basic conversion
        assert EzName.to_tuple("happy-cat") == ("happy", "cat")

        # With different delimiter
        assert EzName.to_tuple("happy_cat", delimiter="_") == ("happy", "cat")

        # With less than 2 parts
        assert EzName.to_tuple("cat") == ("", "cat")
        assert EzName.to_tuple("") == ("", "")

        # With more than 2 parts
        assert EzName.to_tuple("very-happy-cat") == ("very", "happy-cat")

        # With None
        assert EzName.to_tuple(None) == ("", "")

        # With tuple
        assert EzName.to_tuple(("happy", "cat")) == ("happy", "cat")

    def test_to_string(self):
        # Basic conversion
        assert EzName.to_string(("happy", "cat")) == "happy-cat"

        # With different delimiter
        assert EzName.to_string(("happy", "cat"), delimiter="_") == "happy_cat"

        # With string input
        assert EzName.to_string("happy-cat") == "happy-cat"

        # With None
        assert EzName.to_string(None) == ""

    def test_to_tuple_batch(self):
        # Basic conversion
        assert EzName.to_tuple_batch(["happy-cat", "sad-dog"]) == [
            ("happy", "cat"),
            ("sad", "dog"),
        ]

        # With different delimiter
        assert EzName.to_tuple_batch(["happy_cat"], delimiter="_") == [("happy", "cat")]

        # With None
        assert EzName.to_tuple_batch(None) == []

        # With tuple input
        assert EzName.to_tuple_batch([("happy", "cat")]) == [("happy", "cat")]

    def test_to_string_batch(self):
        # Basic conversion
        assert EzName.to_string_batch([("happy", "cat"), ("sad", "dog")]) == [
            "happy-cat",
            "sad-dog",
        ]

        # With different delimiter
        assert EzName.to_string_batch([("happy", "cat")], delimiter="_") == [
            "happy_cat"
        ]

        # With None
        assert EzName.to_string_batch(None) == []

        # With string input
        assert EzName.to_string_batch(["happy-cat"]) == ["happy-cat"]
