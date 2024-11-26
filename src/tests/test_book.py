from src.schemas.book_schemas import BookCreateModel

books_prefix = 'api/v1/books'

def test_get_all_books(fake_book_service, fake_session, test_client):
    response = test_client.get(
        url=f"{books_prefix}"
    )
    
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)
    
def test_create_book(fake_book_service, fake_session, test_client):
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher":"The New York Public Library",
        "published_date": "1925-04-10",
        "language": "English", 
        "page_count": 384,
    }

    response = test_client.post(
        url=f"{books_prefix}",
        json=book_data
    )
    
    book_create_data = BookCreateModel(**book_data)
    
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(book_create_data, fake_session)
    
def test_get_book_by_id(fake_book_service, fake_session, test_book, test_client):
    response = test_client.get(f"{books_prefix}/{test_book.uid}")
    
    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid, fake_session)
    
def test_update_book(fake_book_service, fake_session, test_book, test_client):
    response = test_client.put(f"{books_prefix}/{test_book.uid}")
    
    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid, fake_session)