# Axon

Axon is a full-stack web application consisting of a modern **Angular frontend** and a **Python backend**.

---

## 📂 Project Structure

```text
Axon/
├── Backend/                 # Python Backend (API)
│   ├── src/                 # Application source code
│   │   ├── controllers/     # Route handlers / API controllers
│   │   ├── core/            # Configuration and settings
│   │   ├── models/          # Database models (ORM)
│   │   ├── schemas/         # Data validation schemas (Pydantic)
│   │   ├── services/        # Business logic
│   │   └── utils/           # Shared utility functions
│   ├── tests/               # Backend tests
│   ├── .env.example         # Template for environment configurations
│   ├── requirements.txt     # Production dependencies
│   └── requirements-dev.txt # Development dependencies
│
└── Frontend/                # Angular Frontend
    ├── src/                 # Angular application source code
    │   ├── app/             # Core components and routing
    │   └── environments/    # Environment configurations (Dev, QA, Staging, Prod)
    ├── public/              # Static assets (Favicon, images, etc.)
    ├── angular.json         # Angular workspace configuration
    ├── package.json         # Node dependencies & scripts
    └── tailwind.config.js   # Tailwind CSS configuration
```

---

## 🛠️ Getting Started

### Prerequisites
* [Node.js](https://nodejs.org/) (Recommended version: 18+ or 20+ LTS)
* [Python](https://www.python.org/) (Recommended version: 3.10+)

---

### 🐍 Backend Setup

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   * **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   * Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   * Open `.env` and fill in your local configurations (e.g. database credentials).

6. **Run the server:**
   ```bash
   python src/main.py
   ```

---

### 🅰️ Frontend Setup

1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend
   ```

2. **Install Node modules:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The application will run locally at `http://localhost:4200/`.

---

## 🚀 Running Builds

### Frontend Production Build
To compile the frontend assets for deployment:
```bash
npm run build
```
This generates the optimized build artifacts in the `Frontend/dist/` directory.
