CREATE TABLE IF NOT EXISTS statements (
    id UUID PRIMARY KEY,
    actor_mbox TEXT,
    actor_name TEXT,
    verb_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_name TEXT,
    result_score DOUBLE PRECISION,
    result_success BOOLEAN,
    result_duration_seconds DOUBLE PRECISION,
    context_course TEXT,
    statement JSONB NOT NULL,
    stored_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_statements_actor ON statements(actor_mbox);
CREATE INDEX IF NOT EXISTS idx_statements_verb ON statements(verb_id);
CREATE INDEX IF NOT EXISTS idx_statements_course ON statements(context_course);
CREATE INDEX IF NOT EXISTS idx_statements_stored ON statements(stored_at);

CREATE TABLE IF NOT EXISTS learner_analytics (
    actor_mbox TEXT PRIMARY KEY,
    actor_name TEXT,
    total_statements INTEGER NOT NULL DEFAULT 0,
    quiz_attempts INTEGER NOT NULL DEFAULT 0,
    quiz_avg_score DOUBLE PRECISION,
    video_views INTEGER NOT NULL DEFAULT 0,
    forum_posts INTEGER NOT NULL DEFAULT 0,
    active_days INTEGER NOT NULL DEFAULT 0,
    last_activity TIMESTAMPTZ,
    engagement_score DOUBLE PRECISION,
    risk_score DOUBLE PRECISION,
    risk_level TEXT,
    remediation TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS course_kpis (
    course_id TEXT PRIMARY KEY,
    learners INTEGER NOT NULL DEFAULT 0,
    statements INTEGER NOT NULL DEFAULT 0,
    avg_quiz_score DOUBLE PRECISION,
    at_risk_learners INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
