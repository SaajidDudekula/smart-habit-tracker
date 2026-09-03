# Habit / OS — Living Spec

## Product
Habit / OS is a dark tactical habit-tracking command center. Authenticated users create and manage habits, complete each habit once per server-anchored day, review completion history, inspect seven-day progress, and compare consistency on a leaderboard.

## Persistence and data model
- Supabase PostgreSQL is the only active database. FastAPI uses SQLAlchemy 2 async sessions through the Supabase transaction pooler on port 6543.
- Schema changes are versioned with Alembic; the initial migration is `001_supabase`.
- `users`: string `id`, unique lowercase `email`, display `name`, bcrypt `password_hash`
- `habits`: string `id`, `user_id`, `name`, `description`, hex `color`, UTC `created_at`
- `completions`: string `id`, `user_id`, `habit_id`, SQL date; unique constraint across user, habit, date

## API and auth
- All routes are under `/api` through the FastAPI `api_router`.
- `/api/auth/register`, `/api/auth/login`, `/api/auth/me`, `/api/auth/logout`
- JWTs are stored in an httpOnly `habit_access_token` cookie; protected routes use the current user dependency.
- Production cookies are `Secure`; the JWT signing key is a rotated environment secret ignored by Git.
- CORS is restricted to the public app URL. A request guard also blocks cross-site browser requests while accepting the platform's app-specific ingress alias.
- `/api/habits` supports list/create, `/api/habits/{id}` supports update/delete, `/api/habits/{id}/complete` toggles today's completion.
- `/api/habits/history` returns date-stamped completion records.
- `/api/habits/dashboard` returns today totals, active streak, consistency percentage, and seven daily progress points.
- `/api/leaderboard` ranks registered users by unique completion dates and total completions.

## Key flows
1. Anonymous users land on `/auth`, register or sign in, then enter the dashboard with a personalized welcome toast; registration uses a first-time journey message while login uses “Welcome back.”
2. Dashboard users add, edit, delete, and toggle today's habits; mutations invalidate dashboard, habits, and history queries.
3. History shows grouped completion records; the live social-circle leaderboard contains only registered users and shows active habits, friendly podium titles, ordinal positions, streaks, and consistency points.
4. Sign out clears the httpOnly cookie and frontend query cache.

## Runtime note
The app uses FastAPI with Supabase PostgreSQL for persistence. The previous MongoDB data was intentionally not migrated, so Supabase starts with a clean schema. Supabase Auth is not used; the existing JWT/httpOnly-cookie flow remains active.
