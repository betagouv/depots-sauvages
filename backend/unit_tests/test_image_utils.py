from backend.doc_maker.image_utils import save_base64_to_temp_file


def test_save_base64_to_temp_file_with_data_uri():
    png_data_uri = (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
        "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    file_path = save_base64_to_temp_file(png_data_uri)
    assert file_path is not None
    assert file_path.endswith(".png")


def test_save_base64_to_temp_file_raw_base64():
    raw_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    file_path = save_base64_to_temp_file(raw_png_base64)
    assert file_path is not None
    assert file_path.endswith(".png")


def test_save_base64_to_temp_file_invalid_image():
    # Base64 string that is not a valid image
    invalid_base64 = "SGVsbG8gV29ybGQ="  # "Hello World"
    assert save_base64_to_temp_file(invalid_base64) is None


def test_save_base64_to_temp_file_empty():
    assert save_base64_to_temp_file("") is None
    assert save_base64_to_temp_file(None) is None


def test_save_base64_to_temp_file_unsupported_extension(mocker):
    png_data_uri = (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
        "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    mock_kind = mocker.MagicMock()
    mock_kind.mime = "image/png"
    mock_kind.extension = "exe"  # Extension suspecte/non autorisée

    mocker.patch("filetype.guess", return_value=mock_kind)
    assert save_base64_to_temp_file(png_data_uri) is None


