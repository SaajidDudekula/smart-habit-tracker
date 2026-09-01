# Habit / OS — Living Spec

## Product
Habit / OS is a dark tactical habit-tracking command center. Authenticated users create and manage habits, complete each habit once per server-anchored day, review completion history, inspect seven-day progress, and compare consistency on a leaderboard.

## Data model
- `users`: string `id`, unique lowercase `email`, display `name`, bcrypt `password_hash`
- `habits`: string `id`, `user_id`, `name`, `description`, hex `color`, UTC `created_at`
- `completions`: string `id`, `user_id`, `habit_id`, ISO date string; unique index across user, habit, date

## API and auth
- All routes are under `/api` through the FastAPI `api_router`.
- `/api/auth/register`, `/api/auth/login`, `/api/auth/me`, `/api/auth/logout`
- JWTs are stored in an httpOnly `habit_access_token` cookie; protected routes use the current user dependency.
- `/api/habits` supports list/create, `/api/habits/{id}` supports update/delete, `/api/habits/{id}/complete` toggles today's completion.
- `/api/habits/history` returns date-stamped completion records.
- `/api/habits/dashboard` returns today totals, active streak, consistency percentage, and seven daily progress points.
- `/api/leaderboard` ranks registered users by unique completion dates and total completions.

## Key flows
1. Anonymous users land on `/auth`, register or sign in, then enter the dashboard.
2. Dashboard users add, edit, delete, and toggle today's habits; mutations invalidate dashboard, habits, and history queries.
3. History shows grouped completion records; Leaderboard shows podium and full rankings.
4. Sign out clears the httpOnly cookie and frontend query cache.

## Runtime note
The app is implemented on the pre-built FastAPI + MongoDB runtime so it runs in the provided pod; the requested REST/JWT/product behavior is preserved. No third-party integrations are enabled.