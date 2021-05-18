import os.path
import logging
import pjsua2
import gtkapplication.api.contacts.vcf_parser
import gtkapplication.api.contacts.contact_state
import gtkapplication.api.sip.sipuri
import gtkapplication.api.contacts.contact
import gtkapplication.data
class ContactManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
	def startup(self,vcf_file_path=None):
		if gtkapplication.api.contacts.contact_state.g_contacts is None:
			data_folder_location=gtkapplication.data.get_data_folder_location()
			if vcf_file_path is None:
				vcf_file_path=os.path.join(data_folder_location,"contacts.vcf")
			full_path=os.path.abspath(vcf_file_path)
			self._logger.debug("contacts.vcf file path = %s",full_path)
			assert os.path.exists(full_path)
			parser=gtkapplication.api.contacts.vcf_parser.Parser()
			gtkapplication.api.contacts.contact_state.g_contacts=parser.parse_vcf_file_into_contacts(vcf_file_path)
			self._logger.info('Loaded %d contacts OK',len(gtkapplication.api.contacts.contact_state.g_contacts))
			parser=None
		else:
			raise ValueError("Attempt to reinitialize contacts in contact manager")
	def shutDown(self):
		self._logger.debug('entered shutDown')
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		gtkapplication.api.contacts.contact_state.g_contacts=None
		self._logger.debug("exit shutdown")
	def find_contact_by_phone_number(self,phone_number,create_temp_contact_if_not_found=False):
		self._logger.debug('entered find_contact_by_phone_number')
		self._logger.debug('phone_number = %s',phone_number)
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type in ["tel","x-signal"]:
					if contact_point.uri_string==phone_number:
						self._logger.debug('found contact %s matching phone number %s',contact,phone_number)
						contact.selected_contact_point=contact_point
						active_contact_point_index=contact.contact_points.index(contact_point)
						self._logger.debug('found contact %s matching phone number %s with contact point index %s',contact,phone_number,active_contact_point_index)
						return (contact,active_contact_point_index)
		self._logger.debug("no contact matching phone number '%s' found",phone_number)
		if create_temp_contact_if_not_found:
			self._logger.debug("creating temporary contact")
			contact=self._create_temporary_contact("Unknown","tel","",phone_number)
			return (contact,0)
		else:
			return (None,None)
	def _create_temporary_contact(self,contact_name,point_type,point_description,point_uri):
		self._logger.debug("entered _create_temporary_contact")
		self._logger.debug("contact_name = %s",contact_name)
		self._logger.debug("point_type = %s",point_type)
		self._logger.debug("point_description = %s",point_description)
		self._logger.debug("point_uri = %s",point_uri)
		contact=gtkapplication.api.contacts.contact.Contact("Unknown")
		contact_point=gtkapplication.api.contacts.contact_point.ContactPoint(point_type,point_description,point_uri,uri_string_national=point_uri)
		contact.selected_contact_point=contact_point
		contact.contact_points.append(contact_point)
		return contact
	def find_cell_number_for_contact(self,phone_number,create_temp_contact_if_not_found=False):
		self._logger.debug('entered find_cell_number_for_contact')
		self._logger.debug('phone_number = %s',phone_number)
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type=="tel"and contact_point.description=="cell":
					if contact_point.uri_string==phone_number:
						self._logger.debug('found contact %s matching phone number %s',contact,phone_number)
						contact.selected_contact_point=contact_point
						active_contact_point_index=contact.contact_points.index(contact_point)
						return (contact,active_contact_point_index)
		self._logger.debug("no contact matching phone number '%s' found",phone_number)
		if create_temp_contact_if_not_found:
			self._logger.debug("Contact not found, creating temporary")
			contact=self._create_temporary_contact(phone_number,"tel","cell",phone_number)
			active_contact_point_index=0
			return (contact,active_contact_point_index)
		else:
			self._logger.debug("No contact found and temporary contact not requested, returning None")
			return (None,None)
	def find_contacts_with_cell_numbers(self):
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		contact_list_with_cell_numbers=[]
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type=="tel"and contact_point.description=="cell":
					contact.selected_contact_point=contact_point
					active_contact_point_index=contact.contact_points.index(contact_point)
					contact_list_with_cell_numbers.append((contact,active_contact_point_index))
		return contact_list_with_cell_numbers
	def find_contact_by_sip_uri(self,sip_uri_string,create_temp_contact_if_not_found=False):
		self._logger.debug('entered find_contact_by_sip_uri')
		self._logger.debug("from_uri = '%s'",sip_uri_string)
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		sip_uri_parser=gtkapplication.api.sip.sipuri.SipUriParser()
		sip_uri=sip_uri_parser.parseSipUri(sip_uri_string)
		self._logger.debug("parsed sip_uri_string %s",sip_uri_string)
		if sip_uri.host=="sip.twilio.com":
			self._logger.debug("sip_uri.host is sip.twilio.com")
			pstn_phone_number=sip_uri.user
			return self.find_contact_by_phone_number(pstn_phone_number,True)
		else:
			self._logger.debug("sip_uri.host NOT sip.twilio.com")
			for contact in contacts:
				for contact_point in contact.contact_points:
					if contact_point.point_type=="x-sip":
						contact_point_uri=sip_uri_parser.parseSipUri(contact_point.uri_string)
						if contact_point_uri==sip_uri:
							self._logger.info('found contact %s matching uri %s',contact,str(contact_point_uri))
							contact.selected_contact_point=contact_point
							active_contact_point_index=contact.contact_points.index(contact_point)
							self._logger.debug("contact %s has active_contact_point_index = %s",contact,active_contact_point_index)
							return (contact,active_contact_point_index)
						else:
							self._logger.debug('no match on uri_string = %s for contact %s',contact_point.uri_string,contact)
		self._logger.info("no contact matching uri '%s' found",str(sip_uri))
		if create_temp_contact_if_not_found:
			self._logger.debug("Contact not found, creating temporary")
			contact=self._create_temporary_contact("Unknown","x-sip","unknown",sip_uri_string)
			active_contact_point_index=0
			return (contact,active_contact_point_index)
		else:
			self._logger.debug("No contact found and temporary contact not requested, returning None")
			return (None,None)
	def get_contacts(self):
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		return gtkapplication.api.contacts.contact_state.g_contacts
	def get_free_buddy_contacts(self):
		self._logger.debug("entered get_free_buddy_contacts")
		contacts_list=[]
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type=="x-sip":
					self._logger.debug("found free buddy for contact %s (%r)",contact,contact_point)
					contacts_list.append([contact,contact_point.uri_string])
		return contacts_list
	def create_free_buddy_contacts(self,sip_account):
		self._logger.debug('entered find_free_buddy_contacts')
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type=="x-sip":
					self._logger.debug("contact %s has free buddy with uri '%s'",contact,contact_point.uri_string)
					bcfg=pjsua2.BuddyConfig()
					bcfg.uri=contact_point.uri_string
					bcfg.subscribe=True
					buddy=gtkapplication.api.sip.buddy.Buddy(sip_account)
					buddy.create(sip_account,bcfg)
					contact.buddy=buddy
	def destroy_free_buddy_contacts(self):
		self._logger.debug('entered destroy_free_buddy_contacts')
		assert gtkapplication.api.contacts.contact_state.g_contacts is not None
		contacts=gtkapplication.api.contacts.contact_state.g_contacts
		for contact in contacts:
			for contact_point in contact.contact_points:
				if contact_point.point_type=="x-sip":
					contact.destroy_buddy()
					self._logger.debug("destroyed buddy for contact %s",contact)