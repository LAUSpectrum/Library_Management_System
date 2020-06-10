from sqlalchemy import Column, Integer, String, Date, ForeignKey, DATETIME, Boolean
from sqlalchemy.orm import relationship
from DbConfig import Base
import datetime, time


class Borrow(Base):
	__tablename__ = 'borrow'

	is_activate = Column(Boolean, default=True)
	left_opportunity = Column(Integer, default=3)  # one can only renew books a book for three times
	book_isbn = Column(String(32), ForeignKey("books.isbn"))
	# book = relationship("Book",backref="this_book_has_been_borrowed")
	member_id = Column(String(32), ForeignKey("members.id"))
	# member = relationship("Member",backref="this_member_borrow_this_book")

	borrow_date = Column(DATETIME, nullable=False, primary_key=True)
	due_date = Column(DATETIME, nullable=False)
	return_date = Column(DATETIME, nullable=True)

