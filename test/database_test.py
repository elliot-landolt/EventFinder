from app.database.models.searches import Search

def test_connection():
    searches = Search.where(user="Guest")
    assert len(searches) > 0