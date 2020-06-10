import pandas as pd
from DbConfig import Base, engine
from sqlalchemy.orm import Session, sessionmaker
from tables.Book import Book
from tables.Admin import Admin
from tables.Member import Member
from tables.Borrow import Borrow
import time, datetime
import warnings
warnings.filterwarnings("ignore")


def init_db():
	Base.metadata.create_all(engine)


def drop_db():
	Base.metadata.drop_all(engine)


def insert_db_data(session: Session, db_data_list: list, mode="book"):  # this method should be privately owned by admin

	switch = {
		"member": Member,
		"admin": Admin,
		"book": Book,
		"borrow": Borrow
	}
	try:
		Constructor = switch[mode.lower()]  # distinguish the constructor
		all_objects = [Constructor(**data) for data in db_data_list]  # use dict to construct a object
		session.add_all(all_objects)
		session.commit()
		# session.close()

	except KeyError:
		print("the parameter mode should be selected from: \"member\", \"book\" and \"admin!\"")
		return None


def load_douban_data():
	file_path = "../data/book_douban.csv"
	df = pd.read_csv(file_path, header=0)

	# df.info()
	# print(df.columns)

	# remove duplicate
	if sum(df.duplicated()): df.drop_duplicates()

	column_names = ["ISBM", "书名", "作者", "出版社", "出版时间"]
	columns = df[column_names].values.tolist()
	isbns = set(df["ISBM"].values.tolist())

	infos = []
	# process
	for info in columns:
		if info[0] != "None" and info[0] in isbns:
			infos.append({
				"isbn": str(info[0]),
				"name": str(info[1]),
				"author": str(info[2]),
				"publisher": str(info[3]),
				"release_date": str(info[4])}
			)
			isbns.remove(info[0])
		else: continue

	return infos


def search_book_test(session: Session):
	# return names and isbns of all books
	info_all_names_and_isbns = session.query(Book.name, Book.isbn).all()
	# return all books written by Lu Xun
	result_luxun_wrote = session.query(Book).filter_by(author='鲁迅').all()
	# return the first HanHan's books in MySQL
	result_hanhan_wrote = session.query(Book).filter_by(author='韩寒').first()
	# return a specific book
	result_a_book = session.query(Book).filter_by(name="演讲的本质").all()
	# return nothing
	result_no_book = session.query(Book).filter_by(name="唐诗六百首").all()

	# get books by Admin
	result_ = session.query(Admin).filter_by(member_id=100)

	return None


def renew_book(session: Session, member_id, book_isbn):

	records = session.query(Borrow).filter(
		Borrow.member_id == member_id,
		Borrow.book_isbn == book_isbn,
		Borrow.is_activate == True,
	).all()

	if records:
		BorrowRecord = records[0]

		if BorrowRecord.left_opportunity > 0:  # he's got opportunity renew this book

			borrow_date = datetime.datetime.now()
			due_date = datetime.datetime.now() + datetime.timedelta(days=30)

			BorrowRecord.borrow_date = borrow_date.strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.left_opportunity -= 1

			print("please return this book before {}, and you can renew this book for {} times.".format(
				due_date.strftime("%Y-%m-%d %H:%M:%S"), BorrowRecord.left_opportunity))

			session.commit()

			time.sleep(1)
		else: print("you have to return this book on time!")
	else:
		print("no record has been found!")


def return_book(session: Session, member_id, book_isbn):
	records = session.query(Borrow).filter(Borrow.member_id == member_id, Borrow.book_isbn == book_isbn).all()

	if records:
		BorrowRecord = records[0]
		if BorrowRecord.is_activate:
			return_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.is_activate = False
			BorrowRecord.return_date = return_date

			print("you return this book till at {}".format(return_date))
			session.commit()
		else:
			print("you've returned this book.")
	else:
		print("no record has been found!")


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


def get_admin_info(admin_list):
	return [{"id": int(i), "name": n, "email": e, "password": p} for i, n, e, p in admin_list]


def get_member_info(member_list):
	return [{"id": int(i), "name": n, "email": e, "password": p} for i, n, e, p in member_list]


def unit_test_insert_infos_to_database():

	drop_db()
	init_db()

	# Session = sessionmaker(bind=engine)

	admin_list = [["63", "LAUSen", "senlau@126.com", "senlau"]]
	member_list = [
		["1998", "Zhang Sen", "zhangsen@qq.com", "zhangsen1998"],
		["2020", "WANG MingZe", "wangmingze@hotmail.com", "wangwangwang"]
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
		get_borrow_info("1998", '9787540454098'),
		get_borrow_info("1998", '9787104123019'),
		get_borrow_info("1998", '9787532513413'),
		get_borrow_info("2020", '9787805425245')
	]
	insert_db_data(session, borrow_info, "borrow")

	# renew books
	member_id = "1998"
	book_isbn = '9787805425245'  # this member didn't borrow this book
	renew_book(session, member_id, book_isbn)

	member_id = "2020"
	book_isbn = '9787805425245'
	renew_book(session, member_id, book_isbn)  # first time this member renew the book
	renew_book(session, member_id, book_isbn)  # seconde time this member renew the book
	renew_book(session, member_id, book_isbn)  # one last time this member can renew the book
	renew_book(session, member_id, book_isbn)  # he cannot renew the book

	# return books
	return_book(session, member_id, book_isbn)
	return_book(session, member_id, book_isbn)

	# borrow books
	insert_db_data(session, [get_borrow_info("2020", '9787805425245')], "borrow")

	# lent books
	books_unreturned = session.query(Borrow).filter(Borrow.is_activate == True).all()

	session.close()


if __name__ == "__main__":
	unit_test_insert_infos_to_database()
	unit_test_borrow_renew_return_books()