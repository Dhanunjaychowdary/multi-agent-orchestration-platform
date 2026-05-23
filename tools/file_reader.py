"""File reading tool for the multi-agent orchestration platform."""

import os
from pathlib import Path
from typing import Optional


# Maximum file size allowed (configurable via env, default 10 MB)
_MAX_FILE_SIZE_BYTES = int(os.environ.get("MAX_FILE_SIZE_MB", "10")) * 1024 * 1024


def read_file(file_path: str, encoding: str = "utf-8", max_chars: Optional[int] = None) -> str:
      """
          Read the contents of a local file and return it as a string.

              Args:
                      file_path: Absolute or relative path to the file.
                              encoding: File encoding (default ``utf-8``).
                                      max_chars: Optional character limit. If set, only the first
                                                  ``max_chars`` characters are returned.

                                                      Returns:
                                                              The file contents as a string.

                                                                  Raises:
                                                                          FileNotFoundError: If the path does not exist.
                                                                                  IsADirectoryError: If the path is a directory.
                                                                                          ValueError: If the file exceeds the maximum allowed size.
                                                                                                  IOError: For other I/O related errors.
                                                                                                      """
      path = Path(file_path).resolve()

    if not path.exists():
              raise FileNotFoundError(f"File not found: {file_path}")

    if path.is_dir():
              raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    file_size = path.stat().st_size
    if file_size > _MAX_FILE_SIZE_BYTES:
              raise ValueError(
                            f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds the "
                            f"maximum allowed size ({_MAX_FILE_SIZE_BYTES // 1024 // 1024} MB)."
              )

    content = path.read_text(encoding=encoding)

    if max_chars is not None and len(content) > max_chars:
              content = content[:max_chars]

    return content


def list_directory(dir_path: str, recursive: bool = False) -> list:
      """
          List files in a directory.

              Args:
                      dir_path: Path to the directory.
                              recursive: If True, list all files recursively.

                                  Returns:
                                          Sorted list of file paths (strings) relative to ``dir_path``.

                                              Raises:
                                                      NotADirectoryError: If the path is not a directory.
                                                              FileNotFoundError: If the path does not exist.
                                                                  """
      path = Path(dir_path).resolve()

    if not path.exists():
              raise FileNotFoundError(f"Directory not found: {dir_path}")

    if not path.is_dir():
              raise NotADirectoryError(f"Path is not a directory: {dir_path}")

    if recursive:
              files = [str(p.relative_to(path)) for p in path.rglob("*") if p.is_file()]
else:
          files = [str(p.relative_to(path)) for p in path.iterdir() if p.is_file()]

    return sorted(files)
