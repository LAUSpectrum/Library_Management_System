from utils import *
from operations.get_info import *
from operations.member import renew_book, return_book

def unit_test_insert_infos_to_database():

	drop_db()
	init_db()

	# Session = sessionmaker(bind=engine)

	admin_list = [["63", "刘森", "senlau@126.com", "senlau"], ["64", "张伟", "zhangwei@126.com", "zhangwei"]]
	member_list = [
		["1800", "张三", "zhangsan@qq.com", "zhangsan"],
		["2070", "王五", "wangwu@qq.com", "wangwu"],
		["1404", "李四", "lisi@qq.com", "lisi"],
		["2205", "赵六", "zhaoliu@qq.com", "zhaoliu"]
	]

	admin_info = get_admin_info(admin_list)
	member_info = get_member_info(member_list)

	# process the database
	Session = sessionmaker(bind=engine)
	session = Session()
	insert_db_data(session, admin_info, "admin")
	insert_db_data(session, member_info, "member")
	insert_db_data(session, load_douban_data()[:1000], "book")

	# search_book_test(session)

	session.close()


def unit_test_borrow_renew_return_books():

	# process the database
	Session = sessionmaker(bind=engine)
	session = Session()

	# borrow books
	borrow_info = [
		get_borrow_info("1404", '9787540454098'),
		get_borrow_info("1404", '9787104123019'),
		get_borrow_info("1404", '9787532513413'),
		get_borrow_info("2070", '9787805425245'),
		get_borrow_info("2070", '9780262297387'),
		get_borrow_info("1800", '9780385683562'),
		get_borrow_info("2205", '9780500281284'),
		get_borrow_info("2205", '9780783129501')
	]
	insert_db_data(session, borrow_info, "borrow")

	# renew books
	member_id = "1998"
	book_isbn = '9787805425245'  # this member didn't borrow this book
	renew_book(session, member_id, book_isbn)

	member_id = "2205"
	book_isbn = '9787805425245'
	renew_book(session, member_id, book_isbn)  # first time this member renew the book
	renew_book(session, member_id, book_isbn)  # seconde time this member renew the book
	renew_book(session, member_id, book_isbn)  # one last time this member can renew the book
	renew_book(session, member_id, book_isbn)  # he cannot renew the book

	# return books
	return_book(session, "1404", '9787540454098')
	return_book(session, "1404", '9787104123019')
	return_book(session, "2070", '9780262297387')
	return_book(session, "2250", '9780783129501')

	# borrow books
	insert_db_data(session, [get_borrow_info("2020", '9787805425245')], "borrow")

	# lent books
	books_unreturned = session.query(Borrow).filter(Borrow.is_active == True).all()

	session.close()


if __name__ == "__main__":
	unit_test_insert_infos_to_database()
	unit_test_borrow_renew_return_books()