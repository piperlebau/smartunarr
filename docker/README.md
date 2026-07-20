# 🐳 SmarTunarr Docker Deployment

**Smart TV Channel Programming - Complete deployment guide**

This guide covers Docker deployment of SmarTunarr. For Docker Hub overview, see [DOCKERHUB.md](DOCKERHUB.md).

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Download docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/piperlebau/smartunarr/master/docker/docker-compose.yml

# Start SmarTunarr
docker compose up -d

# View logs
docker compose logs -f smartunarr
```

**Access**: http://localhost:3000

### Option 2: Docker Run

```bash
docker run -d \
  --name smartunarr \
  -p 3000:3000 \
  -p 4273:4273 \
  -v smartunarr-data:/app/data \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  ghcr.io/piperlebau/smartunarr:latest
```

---

## 📦 What's in the Image

The unified SmarTunarr image includes:

| Component | Description | Port |
|-----------|-------------|------|
| 🖥️ **Web UI** | React frontend (nginx) | 3000 |
| ⚡ **API** | FastAPI backend | 4273 |
| 🗄️ **Database** | SQLite | - |

**Platforms**: `linux/amd64`, `linux/arm64`

---

## 🔧 Configuration

### Docker Compose Example

```yaml
version: '3.8'

services:
  smartunarr:
    image: ghcr.io/piperlebau/smartunarr:latest
    container_name: smartunarr
    hostname: smartunarr
    ports:
      - "3000:3000"   # Web UI
      - "4273:4273"   # API
    volumes:
      - smartunarr-data:/app/data
    environment:
      # Logging
      - LOG_LEVEL=INFO

      # Database (SQLite default)
      - DATABASE_URL=sqlite+aiosqlite:///data/smartunarr.db

      # CORS (optional)
      - CORS_ORIGINS=*

    restart: unless-stopped

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4273/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  smartunarr-data:
    driver: local
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `DATABASE_URL` | `sqlite+aiosqlite:///data/smartunarr.db` | Database connection string |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |

---

## 💾 Backup & Restore

### Via Volume

```bash
# Backup
docker run --rm \
  -v smartunarr-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/smartunarr-$(date +%Y%m%d).tar.gz -C /data .

# Restore
docker run --rm \
  -v smartunarr-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/smartunarr-YYYYMMDD.tar.gz"
```

---

## 🔄 Updates

```bash
# Pull latest image
docker compose pull

# Recreate container
docker compose up -d

# Clean old images
docker image prune -f
```

### Version Pinning

```yaml
services:
  smartunarr:
    image: ghcr.io/piperlebau/smartunarr:v0.1.0  # Pin to specific version
```

---

## 🐛 Troubleshooting

### Container Won't Start

Check logs: `docker compose logs smartunarr`

Common issues:
- Port conflict: Change ports in compose file
- Permission: `chmod -R 755 ./data`
- Database locked: Stop all instances

### Services Can't Connect

**Mac/Windows**: Use `host.docker.internal` instead of `localhost`

**Linux**: Use your machine's IP (not `localhost`)

Test: `docker compose exec smartunarr curl -I http://YOUR_SERVICE`

---

## 📚 Resources

- **🐳 Docker Hub**: https://github.com/piperlebau/smartunarr/pkgs/container/smartunarr
- **📘 GitHub**: https://github.com/piperlebau/smartunarr

---

**Built with Docker 🐳 for the Tunarr community 📺**
