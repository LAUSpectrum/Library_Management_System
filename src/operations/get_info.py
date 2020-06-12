import datetime
import time


def get_borrow_info(member_id, book_isbn):
	# one can borrow a book for 30 days at most
	borrow_date = datetime.datetime.now()
	due_date = datetime.datetime.now() + datetime.timedelta(days=30)

	time.sleep(1.1)  # in case "Duplicate entry '2020-06-10 21:10:49' for key 'PRIMARY'"
	return {
		"borrow_date": borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
		"due_date": due_date.strftime("%Y-%m-%d %H:%M:%S"),
		"book_isbn": book_isbn,
		"member_id": member_id
	}


def get_book_info(book_list):
	return [{"isbn": i, "name": n, "author": a, "publisher": p, "release_date": r} for i, n, a, p, r in book_list]


def get_admin_info(admin_list):
	return [{"id": i, "name": n, "email": e, "password": p} for i, n, e, p in admin_list]


def get_member_info(member_list):
	return [{"id": i, "name": n, "email": e, "password": p} for i, n, e, p in member_list]
