import pytest
from app.tools import (
    search_books_openlibrary,
    manage_reading_list,
    query_literary_rag,
    generate_book_cover,
    calculate_reading_stats,
)

def test_openlibrary_search():
    res = search_books_openlibrary("dune")
    assert res["status"] in ["success", "partial_fallback"]
    assert len(res["books"]) > 0

def test_manage_reading_list():
    res = manage_reading_list(
        action="add",
        title="Foundation",
        author="Isaac Asimov",
        status="want_to_read",
        total_pages=255
    )
    assert res["status"] == "success"
    
    get_res = manage_reading_list(action="get_list")
    assert get_res["status"] == "success"
    assert get_res["total_books"] >= 3

def test_query_literary_rag():
    res = query_literary_rag("Dune themes")
    assert res["status"] == "grounded_rag_match"
    assert res["title"] == "Dune"
    assert len(res["themes"]) > 0

def test_generate_book_cover():
    res = generate_book_cover("Cyberpunk city neon lights", title="Neuromancer")
    assert res["status"] == "success"
    assert "Neuromancer" in res["title"]

def test_calculate_reading_stats():
    res = calculate_reading_stats(pages_per_day=30.0)
    assert res["status"] == "success"
    assert res["reading_streak_days"] == 14
