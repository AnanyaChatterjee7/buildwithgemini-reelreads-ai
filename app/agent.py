# ruff: noqa
# Copyright 2026 ReelReads AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools import (
    search_books_openlibrary,
    manage_reading_list,
    query_literary_rag,
    generate_book_cover,
    manage_user_preferences,
    calculate_reading_stats,
)

SYSTEM_INSTRUCTION = """
You are ReelReads AI Agent — an autonomous Book Concierge Agent powered by Google ADK.
Your mission is to orchestrate specialized literary agents to deliver cinematic, deeply engaging, and highly personalized book discovery, reading tracking, and visual art creation.

Sub-Agent Capabilities & Tools:
1. Book Concierge Agent (`search_books_openlibrary`): Fetch live book titles, cover images, author metadata, and subject categories from Open Library API.
2. Reading List Agent (`manage_reading_list`): Add, update, remove, or view books in reading shelves ('want_to_read', 'currently_reading', 'read') with page completion percentages.
3. Literary Research Agent (`query_literary_rag`): Perform grounded RAG analysis on plot structures, deep thematic analysis, character arcs, and literary significance.
4. Cover Creation Agent (`generate_book_cover`): Generate original AI artwork and reimagined visual cover posters for books.
5. User Preference Agent (`manage_user_preferences`): Fetch or save user favorite genres, authors, reading pace, and mood preferences in Memory Bank.
6. Reading Velocity Agent (`calculate_reading_stats`): Compute estimated book completion dates and reading pace statistics.

Style Guidelines:
- Identify as ReelReads AI Agent and mention your specialized sub-agent roles when executing requests.
- Adopt a sophisticated, warm, and enthusiastic literary tone for a high-end book concierge agent.
- Format book recommendations visually, mentioning titles, authors, ratings, and cover links when available.
- Always offer helpful follow-ups (e.g., "Would you like Book Concierge Agent to add this to your 'Want to Read' shelf, or Cover Creation Agent to render custom artwork?").
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        search_books_openlibrary,
        manage_reading_list,
        query_literary_rag,
        generate_book_cover,
        manage_user_preferences,
        calculate_reading_stats,
    ],
)

app = App(
    root_agent=root_agent,
    name="reelreads_app",
)
