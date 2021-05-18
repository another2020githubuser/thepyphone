import re
import logging
import operator
import vobject
import phonenumbers
import gtkapplication.api.contacts.contact
import gtkapplication.api.contacts.contact_point
class Parser:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
	def parse_vcf_file_into_contacts(self,vcf_file_path):
		contacts=[]
		re_pattern=r"[^\+\d+]"
		with open(vcf_file_path,'r')as file_reader:
			file_contents=file_reader.read()
			file_reader.close()
			vcards=vobject.readComponents(file_contents)
			for vcard in vcards:
				contact_name=vcard.contents['fn'][0].value
				contact=gtkapplication.api.contacts.contact.Contact(contact_name)
				found_number_count=0
				try:
					contact_point_type='tel'
					phone_numbers=vcard.contents[contact_point_type]
					found_number_count=len(phone_numbers)
					self._logger.debug('found %d phone_numbers for %s',found_number_count,contact_name)
					for phone_number in phone_numbers:
						contact_point_description=', '.join(phone_number.params['TYPE']).lower()
						pstn_phone_number=re.sub(re_pattern,'',phone_number.value)
						assert len(gtkapplication.data.config_data.PROFILE_DATA)>0,"Profile not initialized"
						phone_number_region=gtkapplication.data.config_data.PROFILE_DATA['phone_number_region']
						self._logger.debug("phone_number_region = %s",phone_number_region)
						parsed_number=phonenumbers.parse(pstn_phone_number,phone_number_region)
						contact_point_uri=phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)
						contact_point_uri_national=phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.NATIONAL)
						contact_point=gtkapplication.api.contacts.contact_point.ContactPoint(contact_point_type,contact_point_description,contact_point_uri,uri_string_national=contact_point_uri_national)
						self._logger.debug('%s',contact_point)
						contact.contact_points.append(contact_point)
				except KeyError as key_error:
					self._logger.debug("No Phone Number for contact '%s'. key_error is %s",contact.name,key_error)
				try:
					contact_point_type='x-sip'
					sip_uris=vcard.contents[contact_point_type]
					assert len(sip_uris)==1
					found_number_count+=len(sip_uris)
					self._logger.debug('found %d sip uris for %s',len(sip_uris),contact_name)
					for sip_uri in sip_uris:
						contact_point_description=', '.join(sip_uri.params['TYPE'])
						contact_point_uri=sip_uri.value
						contact_point=gtkapplication.api.contacts.contact_point.ContactPoint(contact_point_type,contact_point_description,contact_point_uri,"Free")
						self._logger.debug('found %s for %s',contact_point,contact_name)
						contact.contact_points.append(contact_point)
				except KeyError as key_error:
					self._logger.debug("No SIP uri for contact '%s'. key_error is %s",contact.name,key_error)
				if found_number_count==0:
					self._logger.debug('no contact points for contact %s, skipping import',contact.name)
				elif found_number_count>10:
					self._logger.warning("contact %s has too many contact points: limit 10, found %d",contact.name,found_number_count)
				else:
					contacts.append(contact)
		self._logger.debug("contacts dictionary has %d items",len(contacts))
		sorted_contacts=sorted(contacts,key=operator.attrgetter('name'))
		vcards=None
		return sorted_contacts