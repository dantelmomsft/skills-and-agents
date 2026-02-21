"""
download_folder.py

Downloads a specific folder from a public GitHub repository
using the GitHub API (zipball endpoint), without cloning the full repo.

Usage:
    python scripts/download_folder.py <owner/repo> <folder_path> [--branch BRANCH] [--output OUTPUT_DIR]

Examples:
    python scripts/download_folder.py octocat/Hello-World src/utils
    python scripts/download_folder.py octocat/Hello-World src/utils --branch develop
    python scripts/download_folder.py octocat/Hello-World src/utils --output ./downloaded
"""

import argparse
import io
import os
import sys
import zipfile

import urllib.request
import urllib.error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a specific folder from a public GitHub repo via the GitHub API."
    )
    parser.add_argument(
        "repo",
        help="GitHub repository in 'owner/repo' format (e.g. octocat/Hello-World)",
    )
    parser.add_argument(
        "folder",
        help="Path of the folder inside the repo to download (e.g. src/utils)",
    )
    parser.add_argument(
        "--branch",
        default="HEAD",
        help="Branch, tag, or commit SHA to download from (default: HEAD)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Local directory to place the downloaded folder (default: ./<folder_name>)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub personal access token (or set GITHUB_TOKEN env var). Optional for public repos.",
    )
    return parser.parse_args()


def build_zipball_url(repo: str, branch: str) -> str:
    return f"https://api.github.com/repos/{repo}/zipball/{branch}"


def download_zip(url: str, token: str | None) -> bytes:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    print(f"Downloading archive from: {url}")
    try:
        with urllib.request.urlopen(request) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        if exc.code == 404:
            print("  -> Repository or branch not found.", file=sys.stderr)
        elif exc.code == 401:
            print("  -> Unauthorized. Provide a valid --token or set GITHUB_TOKEN.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)

    return data


def extract_folder(zip_bytes: bytes, target_folder: str, output_dir: str) -> int:
    """
    Extracts files from `target_folder` inside the zip archive to `output_dir`.
    GitHub zipballs contain a top-level directory like `owner-repo-<sha>/`, so the
    actual path inside the zip is `<root>/<target_folder>/`.

    Returns the number of files extracted.
    """
    target_folder = target_folder.strip("/")
    extracted = 0

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        all_names = zf.namelist()
        if not all_names:
            print("Archive is empty.", file=sys.stderr)
            sys.exit(1)

        # The first entry is always the root prefix directory, e.g. "owner-repo-abc1234/"
        root_prefix = all_names[0].split("/")[0] + "/"
        folder_prefix = root_prefix + target_folder + "/"

        matching = [n for n in all_names if n.startswith(folder_prefix) and n != folder_prefix]
        if not matching:
            print(
                f"Folder '{target_folder}' not found in the repository archive.\n"
                f"  (looked for prefix: {folder_prefix!r})",
                file=sys.stderr,
            )
            sys.exit(1)

        for name in matching:
            relative_path = name[len(folder_prefix):]
            if not relative_path:
                continue  # Skip the folder entry itself

            dest_path = os.path.join(output_dir, relative_path)

            if name.endswith("/"):
                os.makedirs(dest_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with zf.open(name) as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())
                extracted += 1

    return extracted


def main() -> None:
    args = parse_args()

    folder_name = os.path.basename(args.folder.rstrip("/"))
    output_dir = args.output if args.output else os.path.join(".", folder_name)
    output_dir = os.path.abspath(output_dir)

    zip_bytes = download_zip(
        url=build_zipball_url(args.repo, args.branch),
        token=args.token,
    )

    print(f"Extracting '{args.folder}' to: {output_dir}")
    count = extract_folder(zip_bytes, args.folder, output_dir)
    print(f"Done. {count} file(s) extracted to '{output_dir}'.")


if __name__ == "__main__":
    main()
