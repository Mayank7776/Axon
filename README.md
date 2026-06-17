# Axon - Full-Stack Fitness & AI Trainer Platform

Axon is a feature-rich, high-performance web application consisting of a modern **Angular frontend** and a scalable **FastAPI (Python) backend**. It integrates custom AI-driven trainers, workout tracking, analytics, media-rich health blogs, and global announcement dispatches.

---

## 📂 Project Directory Structure

```text
Axon/
├── Backend/                 # Python Backend (FastAPI API)
│   ├── src/                 # Application source code
│   │   ├── controllers/     # Route handlers / API controllers (Auth, Blogs, Chat, Muscles, Workouts, Users, Roles)
│   │   ├── core/            # Configs, DB setups, and Environment settings
│   │   ├── models/          # Database models (ORM tables via SQLAlchemy)
│   │   ├── schemas/         # Data validation schemas (Pydantic v2)
│   │   ├── services/        # Business logic & services (Cloudinary, Auth, Workouts, etc.)
│   │   └── utils/           # Utility functions (Rate limiting, DataTables filters)
│   ├── migrations/          # Alembic migrations history and version scripts
│   ├── tests/               # Backend unit test suites
│   ├── requirements.txt     # Backend core dependencies
│   └── requirements-dev.txt # Local test/dev packages
│
└── Frontend/                # Angular Frontend (SPA)
    ├── src/                 # Angular application source code
    │   ├── app/             # Application shell and module structures
    │   │   ├── core/        # Route guards, interceptors, base components
    │   │   ├── features/    # Module-specific UI views
    │   │   ├── models/      # Typed TypeScript interfaces (e.g. DataTableFilter)
    │   │   ├── services/    # Injectable API connector classes (Auth, Blogs, Chat, Workouts, Users, Roles, Notifications)
    │   │   └── shared/      # UI components, pipes, directives
    │   └── environments/    # Environment configurations (Dev, Prod)
    ├── package.json         # Node.js configurations & dependencies
    └── tailwind.config.js   # Tailwind styling utility configuration
```

---

## 🛠️ Tech Stack

### Backend
- **Core Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (PostgreSQL backend dialect support)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Rate Limiting**: [SlowAPI](https://github.com/laurentS/slowapi) (integrated in router controllers)
- **Media Hosting**: [Cloudinary](https://cloudinary.com/) (handles image/video uploads)

### Frontend
- **Framework**: [Angular](https://angular.dev/) (Version 20+)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **HTTP client**: Reactive RxJS-based wrapper over Angular HttpClient

---

## 🚀 Key Features & Modules

### 1. Workout Tracking & Stats Analytics (`/workout`)
- **Plan Configurations**: Custom workout plans consisting of day templates (Days 1–7) and exercise sets.
- **AI Recommendation Engine**: Save plans generated dynamically by an AI Trainer.
- **Active Tracker**: Select the current workout day and log reps, sets, and weights performed.
- **Completion Analytics**:
  - Daily progress: computed dynamically as `(completed_sets / total_sets) * 100`.
  - Overall consistency: computes workout stats over a dates span divided by total days, penalizing missed days.
- **Auto-Deactivation**: Setting a plan to active automatically flags all other plans of that user as inactive.

### 2. Media-Rich Health Blogs (`/blogs`)
- **Categorization**: Seeded categories supported out of the box: *Workout, Nutrition, Weight Loss, Muscle Gain, Recovery, Supplements, and Lifestyle*.
- **Media Upload**: Compulsory thumbnail image and optional video file uploads handled using Cloudinary storage.
- **Unique Slugs**: Auto-generates unique, SEO-friendly slugs from title headers with recursion handling (e.g., `chest-press-1` on conflict).

### 3. Broadcast Notification System (`/notifications`)
- **Broadcast Announcements**: Broadcasts system-wide general notifications or reminders.
- **Read-Tracking Mapping**: Tracks individual user read statuses using a distinct mapping table (`user_notification_reads`) to optimize database size.
- **API Features**: Fetch all unread/read messages, mark individual/all read, or delete globally.

### 4. Interactive Chat Sessions (`/chat`)
- **History Mapping**: Store AI Trainer chat sessions per user.
- **Messaging CRUD**: Fetch historical chat streams and append user/AI replies with defined role contexts.

### 5. Roles & Profiles Admin (`/users`, `/roles`)
- **Granular Security**: Assign default system roles.
- **DataTable Filtering**: Backend DataTable handler enables pagination page limits, regex searching, and column sorting.
- **Avatar Upload**: Custom user profiles with profile picture uploads.

---

## 💻 Getting Started

### Prerequisites
* [Node.js](https://nodejs.org/) (Recommended version: 18+ or 20+ LTS)
* [Python](https://www.python.org/) (Recommended version: 3.10+)

---

### 🐍 Backend Setup

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Environment Variables Config:**
   Create a `.env` file in the `Backend/` directory and configure details matching `.env.example`:
   - Database connections (`DB_CONNECTION`)
   - JWT and secret tokens
   - Mail server credentials
   - Cloudinary keys (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, etc.)
   - Groq API keys

5. **Run Database Migrations:**
   ```bash
   # Upgrades database to the latest schema version and seeds categories
   python -m alembic upgrade head
   ```

6. **Run Local Server:**
   ```bash
   python src/main.py
   ```
   Access backend docs locally at `http://localhost:8000/docs`.

---

### 🅰️ Frontend Setup

1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend
   ```

2. **Install Node Modules:**
   ```bash
   npm install
   ```

3. **Start Local Development:**
   ```bash
   npm start
   ```
   Open your browser and navigate to `http://localhost:4200/`.

4. **Build Compilation Check:**
   ```bash
   npm run build
   ```
