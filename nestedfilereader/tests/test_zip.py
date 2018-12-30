from nestedfilereader import open
from nestedfilereader.zipreader import ZipReader
import pytest
import zipfile
import io

def setup_module():
    ZipReader.register()

@pytest.fixture(scope="session")
def nested_zip_fn(tmp_path_factory):
    root_fn = tmp_path_factory.mktemp("zip") / "root.zip"

    fn, content = "hello.txt", "Hello World"
    for i in range(3):
        f = io.BytesIO()
        with zipfile.ZipFile(f, "w") as zf:
            zf.writestr(fn, content)

        fn = "{}.zip".format(i)
        content = f.getvalue()

    with zipfile.ZipFile(root_fn, "w") as zf:
        zf.writestr(fn, content)

    return root_fn

def test_nested_file(nested_zip_fn):
    with open(nested_zip_fn / "2.zip/1.zip/0.zip/hello.txt") as f:
        print(f.read())

def test_nested_reader(nested_zip_fn):
    with open(nested_zip_fn / "2.zip/1.zip") as f:
        with f.open("0.zip/hello.txt") as f:
            print(f.read())

def test_imembers(nested_zip_fn):
    with open(nested_zip_fn) as zf:
        for m in zf.imembers():
            print(m)