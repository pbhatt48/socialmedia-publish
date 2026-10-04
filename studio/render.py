"""Render a 1080x1350 quote card.

    python studio/render.py post.json studio/art/oak.py out.jpg

post.json holds eyebrow, quote, name, role, source and optionally quoteSize.
The art module must define build() returning SVG inner markup for a 900x520
viewBox. The output format follows the extension (.jpg for Instagram, .png).
"""
import glob
import importlib.util
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent.resolve()


def load_art(path: str) -> str:
    spec = importlib.util.spec_from_file_location("art", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build()


def find_installed_chromium() -> str | None:
    """A Chromium that is already on disk, for when the pip-installed Playwright
    expects a newer build than the environment provides (and can't download it)."""
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), "/opt/pw-browsers",
             os.path.expanduser("~/.cache/ms-playwright")]
    for root in filter(None, roots):
        for pattern in ("chromium_headless_shell-*/*/headless_shell",
                        "chromium_headless_shell-*/*/chrome-headless-shell",
                        "chromium-*/chrome-linux*/chrome"):
            found = sorted(glob.glob(os.path.join(root, pattern)), reverse=True)
            if found:
                return found[0]
    return None


def launch(p):
    args = ["--allow-file-access-from-files"]
    try:
        return p.chromium.launch(args=args)
    except Exception:
        path = find_installed_chromium()
        if not path:
            raise
        return p.chromium.launch(args=args, executable_path=path)


def render(post: dict, out: str) -> None:
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.add_init_script("window.POST = " + json.dumps(post) + ";")
        page.goto((HERE / "template.html").as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(400)
        if out.lower().endswith((".jpg", ".jpeg")):
            page.screenshot(path=out, type="jpeg", quality=92)
        else:
            page.screenshot(path=out)
        browser.close()


if __name__ == "__main__":
    post_json, art_py, out = sys.argv[1:4]
    post = json.loads(pathlib.Path(post_json).read_text())
    post["art"] = load_art(art_py)
    render(post, out)
