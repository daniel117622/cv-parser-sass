# Routing Architecture

This project uses a single domain with a clear separation between frontend and backend routes, managed by an NGINX reverse proxy:

- All requests to `/api/` are routed to the backend (**resume-parser**), with the `/api/` prefix stripped before forwarding. For example, a request to `/api/upload` is proxied to the backend’s `/upload` endpoint.
- All other requests (such as `/`, `/about`, `/docs`, or any static assets) are routed to the frontend (**seller-website**), which serves static HTML templates and assets.

## How it works

### Frontend (Landing Page & Docs)

- Accessed via `/` and all non-API routes.
- Serves static content and documentation using Flask and Jinja2 templates.

### Backend (API Endpoints)

- Accessed via `/api/` routes (e.g., `/api/upload`).
- Handles file uploads, resume parsing, and returns structured JSON data.

## Example Requests

| URL            | Routed To       | Description                            |
|----------------|-----------------|----------------------------------------|
| `/`            | seller-website  | Landing page                           |
| `/about`       | seller-website  | About page or other static content     |
| `/api/upload`  | resume-parser   | Resume parsing API endpoint            |
| `/api/status`  | resume-parser   | API status/health endpoint             |

This architecture keeps your API and frontend cleanly separated, easy to maintain, and simple to consume for both users and developers.
