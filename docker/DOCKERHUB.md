# 📺 SmarTunarr

[![GitHub](https://img.shields.io/github/v/tag/piperlebau/smartunarr?label=version&color=blue)](https://github.com/piperlebau/smartunarr/releases)
[![Docker](https://img.shields.io/badge/docker-ghcr.io-2496ED?logo=docker&logoColor=white)](https://github.com/piperlebau/smartunarr/pkgs/container/smartunarr)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/piperlebau/smartunarr/blob/master/LICENSE)

**Smart TV Channel Programming** — Intelligent scheduling and programming for Tunarr channels using Jellyfin content and AI-powered optimization.

---

## 🚀 Quick Start

```bash
# Pull the image
docker pull ghcr.io/piperlebau/smartunarr:latest

# Run with Docker Compose
curl -o docker-compose.yml https://raw.githubusercontent.com/piperlebau/smartunarr/master/docker/docker-compose.yml
docker compose up -d
```

**Access**: http://localhost:3000

---

## ✨ What You Get

| Component | Port | Description |
|-----------|------|-------------|
| 🖥️ **Web UI** | 3000 | Modern React interface |
| ⚡ **API** | 4273 | FastAPI REST API |
| 🗄️ **Database** | - | SQLite |

**Platforms**: `linux/amd64`, `linux/arm64`

---

## 🎬 Features

✅ **Smart Programming** — AI-powered TV channel schedule generation

✅ **Profile-based Scoring** — Customizable content scoring profiles

✅ **Jellyfin Integration** — Direct connection to your Jellyfin libraries

✅ **Tunarr Integration** — Seamless channel management

✅ **Scheduled Tasks** — Automated programming with cron support

✅ **AI Enhancement** — Optional Ollama integration for content optimization

✅ **Multi-language** — 5 languages (EN, FR, DE, ES, IT)

✅ **History Tracking** — Complete execution history with comparison

---

## ⚙️ Configuration

### Basic Deployment

```yaml
version: '3.8'

services:
  smartunarr:
    image: ghcr.io/piperlebau/smartunarr:latest
    container_name: smartunarr
    ports:
      - "3000:3000"   # Web UI
      - "4273:4273"   # API
    volumes:
      - smartunarr-data:/app/data
    environment:
      - LOG_LEVEL=INFO
      - DATABASE_URL=sqlite+aiosqlite:///data/smartunarr.db
    restart: unless-stopped

volumes:
  smartunarr-data:
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DATABASE_URL` | `sqlite+aiosqlite:///data/smartunarr.db` | Database connection |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

---

## 🏷️ Available Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest stable release |
| `v0.1.0` | Specific version |

```bash
# Pin to specific version
docker pull ghcr.io/piperlebau/smartunarr:v0.1.0
```

---

## 🔄 Update

```bash
docker compose pull
docker compose up -d
docker image prune -f
```

---

## 📚 Documentation

- **🐳 [Docker Guide](https://github.com/piperlebau/smartunarr/blob/master/docker/README.md)** — Complete deployment guide
- **📘 [GitHub](https://github.com/piperlebau/smartunarr)** — Source code and docs

---

## 🛠️ Technology Stack

**Backend**: Python 3.11 • FastAPI • SQLAlchemy • APScheduler

**Frontend**: React 18 • TypeScript • Tailwind CSS • i18next

**DevOps**: Docker • GitLab CI • GitHub Actions

---

## 🙏 Built With

- **[Claude Code](https://claude.ai/claude-code)** — AI-assisted development

---

## 📄 License

MIT License - see [LICENSE](https://github.com/piperlebau/smartunarr/blob/master/LICENSE)

---

<div align="center">

**Built with Claude Code 🤖 for the Tunarr community 📺**

[⭐ Star on GitHub](https://github.com/piperlebau/smartunarr) • [🐛 Report Bug](https://github.com/piperlebau/smartunarr/issues) • [💡 Request Feature](https://github.com/piperlebau/smartunarr/issues)

</div>
