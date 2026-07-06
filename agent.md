# Axon Workspace Agent Directory

This directory maps all Cursor rules and specialized code generation skills configured for the Axon repository. 

Whenever you are tasked with creating, editing, or refactoring code, read this file to locate the exact rule files and skill templates to load into your context.

---

## 🐍 Backend Workspace Configurations (`Backend/`)

### Rules (`Backend/.cursor/rules/`)
*   [architecture.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/architecture.mdc): Controls the `Controller → Service → Model` layers boundary rules.
*   [api.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/api.mdc): Standardizes REST interfaces, HTTP statuses, and SlowAPI rate limiting.
*   [database.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/database.mdc): Standardizes SQLAlchemy models, relationships, and eager loading.
*   [security.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/security.mdc): Regulates JWT auth, dependency validations, and data ownership checkers.
*   [testing.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/testing.mdc): Guidelines for writing pytest test cases and client mocks.
*   [coding-standards.mdc](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/rules/coding-standards.mdc): Coding standards, modern Union types, and camelCase request models rules.

### Skills (`Backend/.cursor/skills/`)
Each skill is contained in a separate directory with a `Skill.md` file detailing requirements and full templates:
*   **CRUD Scaffolding**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-crud-module/Skill.md) (Scaffolds Model, Schema, Service, Controller, and Migration)
*   **FastAPI Routers**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-controller/Skill.md) (Router setup with rate limiters and DI)
*   **Business Logic Services**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-service/Skill.md) (Service queries, searches, sorting, and offset pagination)
*   **Pydantic Validation**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-schema/Skill.md) (camelCase and PascalCase schema structures)
*   **SQLAlchemy Models**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-model/Skill.md) (Models with UUID primary keys and back_populates)
*   **Database Migrations**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-migration/Skill.md) (Generating and running Alembic migrations)
*   **Cloudinary Uploads**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Backend/.cursor/skills/create-cloudinary-upload/Skill.md) (Image/video uploads and deletions)

---

## 🅰️ Frontend Workspace Configurations (`Frontend/`)

### Rules (`Frontend/.cursor/rules/`)
*   [architecture.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/architecture.mdc): Core feature-first modular architecture rules.
*   [angular.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/angular.mdc): Standalone elements syntax and custom `basename.ts` file structures.
*   [ui.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/ui.mdc): Design standards, premium colors, spacing, grid layouts, and TailwindCSS rules.
*   [api-integration.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/api-integration.mdc): Regulates shared `ApiService` calls and response mapping.
*   [rxjs.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/rxjs.mdc): Rules on observable pipelines, subscription cleanups, and avoiding nested subscribes.
*   [coding-standards.mdc](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/rules/coding-standards.mdc): TypeScript styles, injection patterns, and Angular signals standards.

### Skills (`Frontend/.cursor/skills/`)
Each skill is contained in a separate directory with a `Skill.md` file detailing requirements and full templates:
*   **Feature Modules**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-feature/Skill.md) (Creates feature layout folders and registers lazy routes)
*   **Standalone Components**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-component/Skill.md) (Scaffolds component declarations, selector, and templates)
*   **API Services Wrapper**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-service/Skill.md) (REST wrapper services injecting `ApiService`)
*   **Reactive Forms**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-form/Skill.md) (Constructs typed forms and validation alerts)
*   **Data Grid Tables**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-datatable/Skill.md) (Server paginated list tables with sorting and debounced search)
*   **Endpoint Wireups**: [Skill.md](file:///c:/Users/Evince/Desktop/Axon/Frontend/.cursor/skills/create-api-integration/Skill.md) (Handling API request states and loading indicators)
