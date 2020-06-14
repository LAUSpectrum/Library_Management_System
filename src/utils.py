import pandas as pd
from DbConfig import Base, engine, sessionmaker
from sqlalchemy.orm import Session
from tables.Book import Book
from tables.Admin import Admin
from tables.Member import Member
from tables.Borrow import Borrow
import warnings
import prettytable as pt
from colorama import Fore

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


def show_borrow_record(session, query_results):
	record_not_return, record_returned = [], []
	for row in query_results:
		if row.is_active:
			record_not_return.append([
				row.member_id, session.query(Member).filter(Member.id == row.member_id).first().name,
				row.borrow_date, row.due_date, row.left_opportunity])
		else:
			record_returned.append([
				row.member_id, session.query(Member).filter(Member.id == row.member_id).first().name,
				row.borrow_date, row.return_date])

	if record_not_return:
		print(Fore.GREEN + "未还书信息: ")
		tb_not_return = pt.PrettyTable()
		tb_not_return.field_names = ["借书人ID", "借书人姓名", "借书日期", "应还日期", "可续借次数"]
		for record in record_not_return:
			tb_not_return.add_row(record)
		tb_not_return.set_style(pt.MSWORD_FRIENDLY)
		print(tb_not_return)

	if record_returned:
		print(Fore.GREEN + "已还信息: ")
		tb_returned = pt.PrettyTable()
		tb_returned.field_names = ["借书人ID", "借书人姓名", "借书日期", "还书日期"]
		for record in record_returned:
			tb_returned.add_row(record)
		tb_returned.set_style(pt.MSWORD_FRIENDLY)
		print(tb_returned)


def find_people(session, Table: Base, id, password):

	if session.query(Table).filter(Table.id == id, Table.password == password).all():
		return True
	else: return False
