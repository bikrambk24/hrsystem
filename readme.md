# HR Portal (Django REST API + PostgreSQL)

A Human Resource Management REST API built with **Django** and **Django REST Framework**, using **PostgreSQL** for data storage.  
Includes authentication with roles, forced password change on first login, attendance clock-in/out, HR operations, workflow features, and reporting endpoints.

---

## Live Demo (Render)
- **Render URL:** <https://hrportal-xgzw.onrender.com>  

### Demo Admin Account (Superuser)
- **Email/Username:** <admin@hr.com>
- **Password:** <Hrportal26@>

---

## Tech Stack
- Python / Django
- Django REST Framework (DRF)
- PostgreSQL
- GitHub (branches, PRs, reviews, merges)
- Render (deployment)

---

## Main Features
- **Accounts & Security**
  - Role-based access (HR / Team Lead / Employee)
  - Login / Logout
  - Forced password change on first login
- **Attendance**
  - Clock-in / Clock-out rules (once per day)
  - Attendance history
- **HR Operations**
  - Employee creation and management
  - Departments
- **Workflow**
  - Leave request + approval
  - HR checks (mocked)
- **Reports**
  - Summary reporting endpoints (API)

---

## Render Deployment Notes
### 1) Profile Picture Issue (Render Free Plan)
Profile picture uploads may **not display or persist reliably** on the **Render Free plan** because uploaded media files require **persistent storage** (or an external media service like Cloudinary/S3). Render free web services use an **ephemeral filesystem**, so uploaded files can be lost after redeploy/restart.

---

## Local Setup

### 1) Clone & install dependencies
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <PROJECT_FOLDER>
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt