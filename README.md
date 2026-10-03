# socialmedia-publish

An MCP server that picks up the posts you create in a folder and publishes them to
your Instagram account through the official Instagram API. Use it from Claude Desktop,
Claude Code, or any other MCP client: *"what posts are queued?"*, *"publish the beach
post"*, *"post everything that's due"*.

## Before you start: your Instagram account type

Meta's API **cannot publish to Personal Instagram accounts**. Only *professional*
accounts (Creator or Business) can. Switching is free, takes a minute, and you can
switch back at any time: **Instagram app → Settings → Account type and tools → Switch
to professional account → Creator**. Your profile, followers and posts stay the same.
You can keep the account private-looking; the change mainly adds insights.

Tools that log in with your password (for example `instagrapi`) break Instagram's
terms and often get accounts locked, so this project doesn't use them.

## 1. Get an access token (one-time setup)

1. Go to <https://developers.facebook.com/apps>, click **Create app**, and choose the
   **Instagram** use case ("Manage messaging & content on Instagram").
2. Open **Instagram → API setup with Instagram login**.
3. Under **Generate access tokens**, click **Add account** and log in with your
   Instagram account. Since this app is only for you, you don't need App Review: as
   the app's owner you can already use it in development mode.
4. Click **Generate token**, and make sure it has the `instagram_business_basic` and
   `instagram_business_content_publish` permissions. That token is a long-lived token,
   valid for 60 days. The `refresh_access_token` tool extends it.

## 2. Install

```bash
git clone https://github.com/pbhatt48/socialmedia-publish.git
cd socialmedia-publish
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env    # then paste your token into .env
```

## 3. Connect it to Claude

**Claude Code:**

```bash
claude mcp add instagram -- /full/path/to/socialmedia-publish/.venv/bin/instagram-mcp
```

**Claude Desktop:** add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "instagram": {
      "command": "/full/path/to/socialmedia-publish/.venv/bin/instagram-mcp",
      "env": {
        "ENV_FILE": "/full/path/to/socialmedia-publish/.env",
        "POSTS_DIR": "/full/path/to/socialmedia-publish/posts"
      }
    }
  }
}
```

Then ask Claude to *"check my Instagram account status"* to confirm the token works.

## 4. Create posts

Each post is a folder in `posts/pending/`:

```
posts/pending/beach-day/
├── caption.txt     # the caption (hashtags included)
├── 1.jpg           # one image → photo post
└── 2.jpg           # several files → carousel (up to 10), in file-name order
```

You can use a `post.json` file instead of, or as well as, `caption.txt`. It lets you
list media URLs and schedule the post:

```json
{
  "caption": "Sunday coffee ☕ #weekend",
  "media": ["https://example.com/photos/coffee.jpg"],
  "publish_at": "2026-10-05T09:00:00-04:00"
}
```

| What you put in the folder         | What gets posted |
|------------------------------------|------------------|
| 1 JPEG image                       | Photo post       |
| 1 MP4/MOV video                    | Reel             |
| 2-10 images and/or videos          | Carousel         |

After a post is published, its folder moves to `posts/published/<date>_<name>/` with a
`result.json` containing the Instagram media ID and link.

### Media must be reachable online

Instagram doesn't accept uploads directly: it downloads each image or video from a
public `https://` URL. You have two options:

- **Use URLs** in `post.json` `media` (for example, from Google Photos shared links,
  Dropbox raw links, S3 or Cloudinary).
- **Use local files** and host the `posts/` folder somewhere public, then set
  `PUBLIC_MEDIA_BASE_URL`. `posts/pending/beach-day/1.jpg` is fetched from
  `$PUBLIC_MEDIA_BASE_URL/pending/beach-day/1.jpg`. For example, sync `posts/` to an
  S3 bucket or Cloudflare R2, or push it to a public GitHub repo and use
  `https://raw.githubusercontent.com/<you>/<repo>/main/posts`.

Images must be JPEG (Instagram's API doesn't accept PNG or HEIC).

## Tools

| Tool                    | What it does |
|-------------------------|--------------|
| `list_pending_posts`    | Lists queued posts and anything wrong with them |
| `preview_post`          | Shows exactly what will be sent, without posting |
| `publish_post`          | Publishes one queued post and moves it to `published/` |
| `publish_due_posts`     | Publishes every post whose `publish_at` time has passed |
| `publish_now`           | Posts directly from URLs, skipping the queue |
| `account_status`        | Checks the token and shows the 24-hour posting limit (100 posts) |
| `refresh_access_token`  | Extends the token by 60 days. Save the new token in `.env` |

## Automatic scheduled posting

MCP servers run only while a client is connected. To publish scheduled posts
without opening Claude, run the same code from cron:

```cron
*/15 * * * * cd /full/path/to/socialmedia-publish && .venv/bin/instagram-mcp --publish-due >> publish.log 2>&1
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
