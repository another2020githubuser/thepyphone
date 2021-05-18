import logging
import os
import sqlite3
from contextlib import closing
import gtkapplication.data
class DBAccess:
	def __init__(self,db_name=None):
		self._logger=logging.getLogger(__name__)
		if db_name is None:
			self._db_name=os.path.abspath(os.path.join(gtkapplication.data.get_data_folder_location(),"pyphone.db"))
		else:
			self._db_name=db_name
		self._logger.debug("db name ='%s'",self._db_name)
		if os.path.exists(self._db_name):
			self._logger.debug("db file found")
		else:
			self._logger.error("db file not found at %s",self._db_name)
	def execute_and_return_scalar(self,sql_stmt,values=None):
		self._logger.debug("entered execute_and_return_scalar")
		self._logger.debug('sql_stmt = %s',sql_stmt)
		with sqlite3.connect(self._db_name)as conn:
			with closing(conn.cursor())as cursor:
				if values is None:
					cursor.execute(sql_stmt)
				else:
					cursor.execute(sql_stmt,values)
				rows=cursor.fetchall()
				self._logger.debug('len(rows) = %s',len(rows))
				assert len(rows)==1
				row=rows[0]
				assert len(row)==1
				scalar_value=row[0]
				self._logger.debug('scalar_value = %s',scalar_value)
				return scalar_value
	def execute_and_return_dictionary(self,sql_stmt,values=None):
		self._logger.debug("entered execute_and_return_dictionary")
		with sqlite3.connect(self._db_name)as conn:
			conn.row_factory=sqlite3.Row
			with closing(conn.cursor())as cursor:
				if values is None:
					cursor.execute(sql_stmt)
				else:
					cursor.execute(sql_stmt,values)
				rows=cursor.fetchall()
				self._logger.debug('len(rows) = %s',len(rows))
				if len(rows)!=1:
					self._logger.warning("Expected 1 row, got %d",len(rows))
					return dict()
				row=rows[0]
				row_as_dict=dict(row)
				return row_as_dict
	def select_and_return_rows(self,sql_stmt):
		self._logger.debug("entered select_and_return_rows")
		self._logger.debug("sql_stmt = %s",sql_stmt)
		with sqlite3.connect(self._db_name,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)as conn:
			conn.row_factory=sqlite3.Row
			with closing(conn.cursor())as cursor:
				cursor.execute(sql_stmt)
				rows=cursor.fetchall()
				self._logger.debug("%d rows",len(rows))
				assert len(rows)>=0
				return rows
	def execute_and_return_rows(self,sql_stmt):
		conn=sqlite3.connect(self._db_name,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		cursor.execute(sql_stmt)
		rows=cursor.fetchall()
		self._logger.debug("%d rows",len(rows))
		assert len(rows)>0
		conn.close()
		return rows
	def execute_and_return_rowcount(self,sql_stmt,values=None):
		self._logger.debug("sql_stmt = %s",sql_stmt)
		self._logger.debug('values = %s',values)
		with sqlite3.connect(self._db_name)as conn:
			with closing(conn.cursor())as cursor:
				if values is None:
					cursor.execute(sql_stmt)
				else:
					cursor.execute(sql_stmt,values)
				return cursor.rowcount
	def execute_and_return_rowid(self,sql_stmt,params):
		assert isinstance(params,tuple)
		self._logger.debug("sql_stmt = %s",sql_stmt)
		self._logger.debug("parms = %s",params)
		with sqlite3.connect(self._db_name)as conn:
			with closing(conn.cursor())as cursor:
				cursor.execute(sql_stmt,params)
				return cursor.lastrowid