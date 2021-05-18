import logging
import json
import gtkapplication.api.db.db_access
class BusinessLayer:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def insert_sms_message(self,from_phone_number,message_body,sms_direction):
		self._logger.debug("entered insert_sms_message")
		values=(from_phone_number,message_body,sms_direction)
		sql_stmt="insert into sms_message (from_phone_number, message_body, direction) values (?, ?, ?);"
		db_access=gtkapplication.api.db.db_access.DBAccess()
		sms_message_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("sms_message_row_id = %d",sms_message_row_id)
		assert sms_message_row_id>0
		return sms_message_row_id
	def insert_mms_link(self,sms_message_row_id,mms_link,content_type):
		self._logger.debug("entered insert_mms_link")
		values=(sms_message_row_id,mms_link,content_type)
		sql_stmt="insert into mms_link (fk_sms_message_id, url, content_type) values (?, ?, ?);"
		db_access=gtkapplication.api.db.db_access.DBAccess()
		mms_link_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("mms_link_row_id = %d",mms_link_row_id)
		assert mms_link_row_id>0
		return mms_link_row_id
	def insert_missed_call_message(self,from_phone_number):
		self._logger.debug("entered insert_missed_call_message")
		values=(from_phone_number,)
		sql_stmt="insert into missed_call (from_phone_number) values (?);"
		db_access=gtkapplication.api.db.db_access.DBAccess()
		missed_call_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("missed_call_row_id = %d",missed_call_row_id)
		assert missed_call_row_id>0
		return missed_call_row_id
	def insert_blocked_call_message(self,from_phone_number):
		self._logger.debug("entered insert_blocked_call_message")
		values=(from_phone_number,)
		sql_stmt="insert into blocked_call (from_phone_number) values (?);"
		db_access=gtkapplication.api.db.db_access.DBAccess()
		blocked_call_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("blocked_call_row_id = %d",blocked_call_row_id)
		assert blocked_call_row_id>0
		return blocked_call_row_id
	def insert_blocked_sms_message(self,from_phone_number):
		self._logger.debug("entered insert_blocked_sms_message")
		values=(from_phone_number,)
		sql_stmt="insert into blocked_sms (from_phone_number) values (?);"
		db_access=gtkapplication.api.db.db_access.DBAccess()
		blocked_sms_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("blocked_sms_row_id = %d",blocked_sms_row_id)
		assert blocked_sms_row_id>0
		return blocked_sms_row_id
	def insert_sip_registration_failure_message(self,account_id,account_uri,status,reason,code):
		self._logger.debug("entered insert_sip_registration_failure_message")
		values=(account_id,account_uri,status,reason,code)
		sql_stmt='''insert into sip_registration_failure (account_id, account_uri, status, reason, code)
                      values (?, ?, ?, ?, ?);
                    '''
		db_access=gtkapplication.api.db.db_access.DBAccess()
		sip_registration_failure_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("sip_registration_failure_row_id = %d",sip_registration_failure_row_id)
		assert sip_registration_failure_row_id>0
		return sip_registration_failure_row_id
	def insert_free_buddy_text_delivery_failure_message(self,to_uri,message_body,reason,code):
		self._logger.debug("entered insert_im_delivery_failure_message")
		values=(to_uri,message_body,reason,code)
		sql_stmt='''insert into free_buddy_text_delivery_failure (to_uri, message_body, reason, code)
                      values (?, ?, ?, ?);
                    '''
		db_access=gtkapplication.api.db.db_access.DBAccess()
		sms_delivery_failure_row_id=db_access.execute_and_return_rowid(sql_stmt,values)
		self._logger.debug("sms_delivery_failure_row_id = %d",sms_delivery_failure_row_id)
		assert sms_delivery_failure_row_id>0
		return sms_delivery_failure_row_id
	def insert_or_replace_twilio_message_instance(self,message):
		self._logger.debug("entered insert_twilio_message_instance")
		assert message is not None
		db_access=gtkapplication.api.db.db_access.DBAccess()
		sql_stmt="select count(*) from twilio_message_instance where sid = ?;"
		params=(message.sid,)
		row_count=db_access.execute_and_return_scalar(sql_stmt,params)
		record_exists=(row_count==1)
		self._logger.debug("record_exists = %s",record_exists)
		if record_exists:
			sql_stmt="UPDATE twilio_message_instance SET account_sid = ?,\
                        api_version = ?,\
                        body = ?,\
                        date_created = ?,\
                        date_updated = ?,\
                        date_sent = ?,\
                        direction = ?,\
                        error_code = ?,\
                        error_message = ?,\
                        from_ = ?,\
                        messaging_service_sid = ?,\
                        num_media = ?,\
                        num_segments = ?,\
                        price = ?,\
                        price_unit = ?,\
                        status = ?,\
                        subresource_uris = ?,\
                        to_ = ?,\
                        uri = ? where sid = ? ;"
			params=('{0}'.format(message.account_sid),'{0}'.format(message.api_version),'{0}'.format(message.body).replace("'","''"),'{0}'.format(message.date_created),'{0}'.format(message.date_updated),'{0}'.format(message.date_sent),'{0}'.format(message.direction),'{0}'.format(message.error_code),'{0}'.format(message.error_message),'{0}'.format(message.from_),'{0}'.format(message.messaging_service_sid),'{0}'.format(message.num_media),'{0}'.format(message.num_segments),'{0}'.format(message.price),'{0}'.format(message.price_unit),'{0}'.format(message.status),'{0}'.format(json.dumps(message.subresource_uris)),'{0}'.format(message.to),'{0}'.format(message.uri),'{0}'.format(message.sid))
			db_access=gtkapplication.api.db.db_access.DBAccess()
			rows_affected=db_access.execute_and_return_rowcount(sql_stmt,params)
			assert rows_affected==1
		else:
			sql_stmt="INSERT INTO twilio_message_instance ( account_sid,\
                        api_version,\
                        body,\
                        date_created,\
                        date_updated,\
                        date_sent,\
                        direction,\
                        error_code,\
                        error_message,\
                        from_,\
                        messaging_service_sid,\
                        num_media,\
                        num_segments,\
                        price,\
                        price_unit,\
                        sid,\
                        status,\
                        subresource_uris,\
                        to_,\
                        uri) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
			params=('{0}'.format(message.account_sid),'{0}'.format(message.api_version),'{0}'.format(message.body).replace("'","''"),'{0}'.format(message.date_created),'{0}'.format(message.date_updated),'{0}'.format(message.date_sent),'{0}'.format(message.direction),'{0}'.format(message.error_code),'{0}'.format(message.error_message),'{0}'.format(message.from_),'{0}'.format(message.messaging_service_sid),'{0}'.format(message.num_media),'{0}'.format(message.num_segments),'{0}'.format(message.price),'{0}'.format(message.price_unit),'{0}'.format(message.sid),'{0}'.format(message.status),'{0}'.format(json.dumps(message.subresource_uris)),'{0}'.format(message.to),'{0}'.format(message.uri))
			db_access=gtkapplication.api.db.db_access.DBAccess()
			row_id=db_access.execute_and_return_rowid(sql_stmt,params)
			assert row_id>0