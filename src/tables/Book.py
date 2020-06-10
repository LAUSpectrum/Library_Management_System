from DbConfig import Base
from sqlalchemy import Column, String


class Book(Base):
	__tablename__ = 'books'

	isbn = Column(String(32), unique=True, nullable=False, primary_key=True)
	name = Column(String(256))
	author = Column(String(256))
	publisher = Column(String(256))
	release_date = Column(String(64))

	def set_name(self, name):
		self.name = name

	def set_author(self ,author):
		self.author = author

	def set_publisher(self, publisher):
		self.publisher = publisher

	def set_release_date(self, date):
		self.release_date = date