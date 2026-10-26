# Autonomous Media Lab updater

[Run an update or inspect recent runs](https://github.com/drawsomerex/autonomous-media-lab-updater/actions/workflows/refresh.yml).

GitHub Actions requests updates to https://autonomousmedialab.com about every 15 minutes and supports **Run workflow** for an immediate refresh. The website imports public YouTube videos, podcast episodes and Suno albums on RackNerd; the Mac can be off. GitHub may queue scheduled jobs, so the interval is not an exact delivery deadline.

The runner authenticates with a dedicated `AML_UPDATE_SECRET` stored in Actions secrets and the website's private configuration. A timestamped HMAC binds the method, path and request body. The key can only request a source refresh. Successful runs report source counts and the latest imported video; source failures make the workflow fail while the website retains its last good content. Website editor accounts and hosting credentials are managed separately.

YouTube RSS is preferred. When it is unavailable, the website reads this creator's public channel listing and public video metadata, preserving titles, descriptions, thumbnails and publication timestamps. The website does not download video or audio from YouTube or Suno.

This public repository uses standard GitHub-hosted Ubuntu runners. The import job has read-only repository permissions. The separate monthly maintenance workflow runs the signing tests and commits its health-check date, keeping the repository active so GitHub's inactivity rule does not disable scheduled workflows. That job has write access only to this repository and does not receive the import key.

Local tests: `python3 -m unittest discover -s tests -v`.

The full website source and maintenance guide are kept in the owner's Websites folder and Second Brain. This repository contains the scheduler client and maintenance code.
