from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import (
    user_route,
    user_progress_route,
    chat_route,
    feedback_rating_route,
    project_route,
    learning_content_route,
    subject_route,
    topic_route,
    glossary_route,
    doubt_trend_route,
    motivational_trigger_route,
    assessment_route,
    media_asset_route,
    motivational_prompt_route,
    session_route,
    user_activity_route,
    ai_training_log_route,
    language_variant_route,
    ask_route,
    auto_learn_route
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(user_route.router, prefix="/user", tags=["User"])
app.include_router(user_progress_route.router, prefix="/progress", tags=["User Progress"])
app.include_router(chat_route.router, prefix="/chat", tags=["Chat"])
app.include_router(feedback_rating_route.router, prefix="/feedback", tags=["Feedback"])
app.include_router(project_route.router, prefix="/project", tags=["Project"])
app.include_router(learning_content_route.router, prefix="/content", tags=["Learning Content"])
app.include_router(subject_route.router, prefix="/subject", tags=["Subject"])
app.include_router(topic_route.router, prefix="/topic", tags=["Topic"])
app.include_router(glossary_route.router, prefix="/glossary", tags=["Glossary"])
app.include_router(doubt_trend_route.router, prefix="/trend", tags=["Doubt Trends"])
app.include_router(motivational_trigger_route.router, prefix="/trigger", tags=["Motivational Trigger"])
app.include_router(assessment_route.router, prefix="/assessment", tags=["Assessment"])
app.include_router(media_asset_route.router, prefix="/media", tags=["Media Asset"])
app.include_router(motivational_prompt_route.router, prefix="/prompt", tags=["Motivational Prompt"])
app.include_router(session_route.router, prefix="/session", tags=["Session"])
app.include_router(auto_learn_route.router, prefix="/auto-learn", tags=["Auto Learning"])
app.include_router(user_activity_route.router, prefix="/activity", tags=["User Activity"])
app.include_router(ai_training_log_route.router, prefix="/ai-log", tags=["AI Training Log"])
app.include_router(language_variant_route.router, prefix="/variant", tags=["Language Variant"])
app.include_router(ask_route.ask_router, prefix="/ask", tags=["Ask"])

@app.get("/")
def root():
    return {"message": "MVP Backend API is live"}
