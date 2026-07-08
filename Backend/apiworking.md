# Axon Backend API Reference Guide

This document details all available API endpoints in the Axon Backend, including their HTTP methods, route paths, query parameters, request bodies (JSON and Multipart Form-Data), rate limits, and functionality.

The server runs by default at `http://localhost:8000`. Standard Swagger interactive documentation can be accessed at `http://localhost:8000/docs`.

---

## Table of Contents
1. [Authentication (`/auth`)](#1-authentication-auth)
2. [Roles (`/roles`)](#2-roles-roles)
3. [Users (`/users`)](#3-users-users)
4. [Chat Sessions & Messages (`/chat`)](#4-chat-sessions--messages-chat)
5. [Muscle Groups & Exercises (`/musclegroup`)](#5-muscle-groups--exercises-musclegroup)
6. [Workout Plans & Statistics (`/workout`)](#6-workout-plans--statistics-workout)
7. [Blogs & Categories (`/blogs`)](#7-blogs--categories-blogs)
8. [Notifications (`/notifications`)](#8-notifications-notifications)

---

## 1. Authentication (`/auth`)

These endpoints handle registration, login (password-based and OTP-based), token refreshing, and password reset.

### `POST /auth/register`
* **Description:** Register a new user.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepassword123"
  }
  ```

### `POST /auth/login`
* **Description:** Authenticate a user and receive JWT tokens.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "username_or_email": "johndoe@example.com",
    "password": "securepassword123"
  }
  ```
* **Response Data:** Returns access and refresh tokens.

### `POST /auth/forgot-password`
* **Description:** Request a password reset link sent to the user's email.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "email": "johndoe@example.com"
  }
  ```

### `POST /auth/reset-password`
* **Description:** Reset password using a token received via email link.
* **Rate Limit:** `5 / minute`
* **Query Parameters:**
  * `token` (string, required) - Reset token.
* **Request Body (JSON):**
  ```json
  {
    "new_password": "newsecurepassword123"
  }
  ```

### `GET /auth/is-authenticated`
* **Description:** Check if the current JWT token is valid.
* **Headers Required:** `Authorization: Bearer <access_token>`
* **Response Data:** Returns the authenticated user profile info.

### `POST /auth/otp-login`
* **Description:** Step 1 of OTP Flow: Request a login One-Time Password sent to the user's email.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "email": "johndoe@example.com"
  }
  ```

### `POST /auth/otp-verification`
* **Description:** Step 2 of OTP Flow: Verify OTP code and receive authentication tokens.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "email": "johndoe@example.com",
    "otp": "123456"
  }
  ```
* **Response Data:** Returns access and refresh tokens.

### `POST /auth/otp-resend`
* **Description:** Resend OTP to the user's email.
* **Rate Limit:** `3 / minute`
* **Request Body (JSON):**
  ```json
  {
    "email": "johndoe@example.com"
  }
  ```

### `POST /auth/refresh-token`
* **Description:** Exchange a refresh token for a new access token and refresh token pair.
* **Rate Limit:** `1 / minute`
* **Request Body (JSON):**
  ```json
  {
    "refreshToken": "refresh_token_string_here"
  }
  ```

---

## 2. Roles (`/roles`)

Manage user authorization levels (e.g., admin, trainer, user).

### `GET /roles/`
* **Description:** Retrieve all system roles.
* **Rate Limit:** `5 / minute`

### `POST /roles/`
* **Description:** Create a new user role.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "name": "Trainer",
    "description": "Fitness trainer with access to create workouts",
    "is_active": true
  }
  ```

### `PUT /roles/{id}`
* **Description:** Update role properties.
* **Rate Limit:** `5 / minute`
* **Path Parameters:**
  * `id` (string, required) - Role UUID.
* **Request Body (JSON):**
  ```json
  {
    "name": "Lead Trainer",
    "description": "Updated description",
    "is_active": true
  }
  ```

### `DELETE /roles/{id}`
* **Description:** Delete a role. Returns error if any users are assigned to this role.
* **Rate Limit:** `5 / minute`
* **Path Parameters:**
  * `id` (string, required) - Role UUID.

---

## 3. Users (`/users`)

Endpoints for administrative user CRUD operations. Note that user creation and updates support avatar image uploads via `multipart/form-data`.

### `GET /users/`
* **Description:** Retrieve users with pagination, sorting, and search.
* **Rate Limit:** `5 / minute`
* **Query Parameters (DataTable Filters):**
  * `page` (integer, default: 1) - Page number.
  * `limit` (integer, default: 10, max: 100) - Records per page.
  * `search` (string, optional) - Filter by username or email.
  * `sort_by` (string, default: "created_at") - Sorting column.
  * `sort_order` (string, default: "desc") - Sorting direction (`asc` or `desc`).

### `GET /users/{id}`
* **Description:** Get profile details for a specific user.
* **Rate Limit:** `5 / minute`
* **Path Parameters:**
  * `id` (string, required) - User UUID.

### `POST /users/`
* **Description:** Create a new user account (with optional avatar upload).
* **Rate Limit:** `5 / minute`
* **Request Format:** `multipart/form-data`
* **Parameters (Form Fields):**
  * `username` (string, required)
  * `email` (string, required)
  * `password` (string, required, min length 8)
  * `role_id` (string, required)
  * `image` (file, optional) - Profile picture file.

### `PUT /users/{id}`
* **Description:** Update user properties and/or upload a new avatar.
* **Rate Limit:** `5 / minute`
* **Path Parameters:**
  * `id` (string, required) - User UUID.
* **Request Format:** `multipart/form-data`
* **Parameters (Form Fields):**
  * `username` (string, optional)
  * `email` (string, optional)
  * `password` (string, optional)
  * `role_id` (string, optional)
  * `image` (file, optional) - New profile picture file.

### `DELETE /users/{id}`
* **Description:** Delete a user account.
* **Rate Limit:** `5 / minute`
* **Path Parameters:**
  * `id` (string, required) - User UUID.

---

## 4. Chat Sessions & Messages (`/chat`)

Endpoints to handle real-time interactions with AI agents (Trainer, Nutritionist, Designer).

### `GET /chat/sessions`
* **Description:** Get all chat sessions belonging to a specific user.
* **Rate Limit:** `20 / minute`
* **Query Parameters:**
  * `user_id` (string, required) - User UUID.

### `GET /chat/sessions/{session_id}`
* **Description:** Get detailed metadata of a specific chat session.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `session_id` (string, required) - Chat Session UUID.

### `POST /chat/sessions`
* **Description:** Initialize a new AI chat session.
* **Rate Limit:** `10 / minute`
* **Request Body (JSON):**
  ```json
  {
    "user_id": "user_uuid_here",
    "agent_type": "trainer", 
    "title": "My Fitness Plan Consultation"
  }
  ```
  * *Valid `agent_type` values:* `"trainer"`, `"nutrition"`, `"designer"`

### `PATCH /chat/sessions/{session_id}`
* **Description:** Rename or update a chat session's title.
* **Rate Limit:** `10 / minute`
* **Path Parameters:**
  * `session_id` (string, required) - Chat Session UUID.
* **Request Body (JSON):**
  ```json
  {
    "title": "New Session Title"
  }
  ```

### `DELETE /chat/sessions/{session_id}`
* **Description:** Delete a chat session and all its associated messages.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `session_id` (string, required) - Chat Session UUID.

### `GET /chat/sessions/{session_id}/messages`
* **Description:** Retrieve the message history for a specific chat session.
* **Rate Limit:** `30 / minute`
* **Path Parameters:**
  * `session_id` (string, required) - Chat Session UUID.

### `POST /chat/messages`
* **Description:** Send a message to an AI agent in a session and receive a response.
* **Rate Limit:** `5 / minute`
* **Request Body (JSON):**
  ```json
  {
    "session_id": "session_uuid_here",
    "message": "Can you design a 3-day split workout plan for a beginner?"
  }
  ```

---

## 5. Muscle Groups & Exercises (`/musclegroup`)

Endpoints to manage exercise categories (muscle groups) and the exercises themselves.

### `GET /musclegroup/get-musclegroup`
* **Description:** Retrieve all muscle groups.
* **Rate Limit:** `50 / minute`

### `GET /musclegroup/get-musclegroup/{id}`
* **Description:** Get details of a single muscle group.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `id` (string, required) - Muscle Group UUID.

### `POST /musclegroup/upsert-musclegroup`
* **Description:** Create or update a muscle group (with image upload).
* **Rate Limit:** `5 / minute`
* **Request Format:** `multipart/form-data`
* **Parameters (Form Fields):**
  * `id` (string, optional) - Provide ID to update, leave blank to create.
  * `name` (string, optional) - Name of the muscle group (e.g. Chest).
  * `image` (file, optional) - Banner/Illustration image.

### `POST /musclegroup/delete-musclegroup/{id}`
* **Description:** Delete a muscle group.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Muscle Group UUID.

### `GET /musclegroup/get-all-excercise`
* **Description:** Retrieve all exercises belonging to a specific muscle group.
* **Rate Limit:** `50 / minute`
* **Query Parameters:**
  * `id` (string, required) - Muscle Group UUID.

### `GET /musclegroup/get-excercise/{id}`
* **Description:** Get details of a specific exercise.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `id` (string, required) - Exercise UUID.

### `POST /musclegroup/upsert-excercise`
* **Description:** Create or update an exercise (with support for image and video uploads).
* **Rate Limit:** `5 / minute`
* **Request Format:** `multipart/form-data`
* **Parameters (Form Fields):**
  * `id` (string, optional) - Provide ID to update, leave blank to create.
  * `muscle_group_id` (string, required) - Target Muscle Group UUID.
  * `created_by` (string, optional) - User UUID of the creator.
  * `name` (string, required) - Exercise Name (e.g. Bench Press).
  * `description` (string, optional) - Step-by-step description.
  * `category` (string, required) - Category label (e.g. Strength, Cardio).
  * `image` (file, optional) - Informational/Static image file.
  * `video` (file, optional) - Video demonstration file.

### `POST /musclegroup/delete-excercise/{id}`
* **Description:** Delete an exercise.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Exercise UUID.

---

## 6. Workout Plans & Statistics (`/workout`)

Endpoints to manage custom and AI-generated workout plans, workout days, sets/reps configurations, and logged execution statistics.

### `GET /workout/all-plan`
* **Description:** Retrieve all workout plans configured for a user.
* **Rate Limit:** `20 / minute`
* **Query Parameters:**
  * `user_id` (string, required) - User UUID.

### `GET /workout/plan/{id}`
* **Description:** Retrieve the full structured hierarchy of a workout plan, including days, exercises, and sets.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Workout Plan UUID.

### `POST /workout/upsert-plan`
* **Description:** Create or update plan metadata (Title, Description, is_active).
* **Rate Limit:** `20 / minute`
* **Request Body (JSON):**
  ```json
  {
    "id": "plan_uuid_here_or_null",
    "user_id": "user_uuid_here",
    "name": "Advanced Push-Pull-Legs Split",
    "description": "Hypertrophy-focused 3 day split",
    "is_active": true
  }
  ```

### `DELETE /workout/delete-plan/{id}`
* **Description:** Delete a workout plan.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Workout Plan UUID.

### `GET /workout/all-day`
* **Description:** Retrieve all workout days associated with a specific workout plan.
* **Rate Limit:** `20 / minute`
* **Query Parameters:**
  * `plan_id` (string, required) - Workout Plan UUID.

### `GET /workout/day/{id}`
* **Description:** Get details of a single workout day (includes exercises and sets configurations).
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Workout Day UUID.

### `POST /workout/upsert-day`
* **Description:** Add or update a workout day configuration within a plan, complete with exercise lists and target sets/reps.
* **Rate Limit:** `20 / minute`
* **Request Body (JSON):**
  ```json
  {
    "id": "day_uuid_here_or_null",
    "plan_id": "plan_uuid_here",
    "day_number": 1,
    "exercises": [
      {
        "exercise_id": "exercise_uuid_here",
        "sort_order": 0,
        "sets": [
          {
            "set_number": 1,
            "target_reps": 12,
            "weight_kg": 60.0,
            "rest_seconds": 90
          },
          {
            "set_number": 2,
            "target_reps": 10,
            "weight_kg": 65.0,
            "rest_seconds": 90
          }
        ]
      }
    ]
  }
  ```

### `DELETE /workout/delete-day/{id}`
* **Description:** Delete a workout day.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `id` (string, required) - Workout Day UUID.

### `POST /workout/save-ai-plan`
* **Description:** Parse and save a structured workout plan generated by the AI agent.
* **Rate Limit:** `20 / minute`
* **Request Body (JSON):**
  ```json
  {
    "user_id": "user_uuid_here",
    "name": "AI Generated Beginner Plan",
    "description": "Generated by fitness trainer AI",
    "days": [
      {
        "day_number": 1,
        "exercises": [
          {
            "exercise_name": "Pushups",
            "sort_order": 0,
            "sets": [
              {
                "set_number": 1,
                "target_reps": 15,
                "rest_seconds": 60
              }
            ]
          }
        ]
      }
    ]
  }
  ```

### `GET /workout/active-day`
* **Description:** Fetch the user's active workout plan's exercises scheduled for a specific date.
* **Rate Limit:** `20 / minute`
* **Query Parameters:**
  * `user_id` (string, required) - User UUID.
  * `date` (string, optional) - Format: `YYYY-MM-DD`. If omitted, defaults to today.

### `POST /workout/save-workout-stats`
* **Description:** Log execution statistics (completed sets, actual weight lifted, repetitions performed) for a workout session.
* **Rate Limit:** `20 / minute`
* **Request Body (JSON):**
  ```json
  {
    "user_id": "user_uuid_here",
    "workout_plan_id": "plan_uuid_here",
    "day_number": 1,
    "day_label": "Chest Day",
    "workout_date": "2026-07-08",
    "exercises_data": [
      {
        "exercise_id": "exercise_uuid_here",
        "exercise_name": "Bench Press",
        "sort_order": 0,
        "sets": [
          {
            "set_number": 1,
            "target_reps": 12,
            "reps_performed": 12,
            "weight_kg": 60.0,
            "rest_seconds": 90,
            "is_completed": true
          }
        ]
      }
    ]
  }
  ```

### `GET /workout/workout-stats/{user_id}`
* **Description:** Retrieve historical statistics of logged workouts for a specific user.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `user_id` (string, required) - User UUID.

---

## 7. Blogs & Categories (`/blogs`)

Manage public informational blogs. Supports uploading media (images and videos) dynamically.

### `GET /blogs/categories`
* **Description:** Get all available blog categories.
* **Rate Limit:** `50 / minute`

### `POST /blogs/upsert`
* **Description:** Create a new blog post or edit an existing one (with media uploads).
* **Rate Limit:** `5 / minute`
* **Request Format:** `multipart/form-data`
* **Parameters (Form Fields):**
  * `id` (string, optional) - Provide ID to update, leave blank to create.
  * `created_by` (string, required) - User UUID of the author.
  * `title` (string, required) - Blog Title.
  * `content` (string, required) - Detailed Markdown/HTML content.
  * `category_id` (string, required) - Category UUID.
  * `excerpt` (string, optional) - Short summary/teaser.
  * `is_published` (boolean, default: false) - Publish state.
  * `image` (file, optional) - Featured image.
  * `video` (file, optional) - Inline demonstration/intro video.

### `DELETE /blogs/{id}`
* **Description:** Delete a blog post.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Blog Post UUID.

### `GET /blogs/list/{category}`
* **Description:** Retrieve all blogs belonging to a specific category.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `category` (string, required) - Category slug (e.g. `nutrition`, `workout-tips`).

---

## 8. Notifications (`/notifications`)

Manage system notifications and their user-specific read/unread states.

### `GET /notifications/`
* **Description:** Retrieve all notifications relevant to a user (indicates if read or unread).
* **Rate Limit:** `50 / minute`
* **Query Parameters:**
  * `user_id` (string, required) - User UUID.

### `POST /notifications/`
* **Description:** Create a new broadcast notification.
* **Rate Limit:** `10 / minute`
* **Request Body (JSON):**
  ```json
  {
    "title": "New Feature Available!",
    "message": "You can now chat with our AI Trainer.",
    "type": "info",
    "redirect_url": "/chat"
  }
  ```

### `PATCH /notifications/read-all`
* **Description:** Mark all notifications as read for a user.
* **Rate Limit:** `20 / minute`
* **Request Body (JSON):**
  ```json
  {
    "user_id": "user_uuid_here"
  }
  ```

### `PATCH /notifications/{id}/read`
* **Description:** Mark a specific notification as read.
* **Rate Limit:** `50 / minute`
* **Path Parameters:**
  * `id` (string, required) - Notification UUID.
* **Request Body (JSON):**
  ```json
  {
    "user_id": "user_uuid_here"
  }
  ```

### `DELETE /notifications/{id}`
* **Description:** Delete a notification.
* **Rate Limit:** `20 / minute`
* **Path Parameters:**
  * `id` (string, required) - Notification UUID.
