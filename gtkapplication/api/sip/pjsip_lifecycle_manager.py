import logging
import pkg_resources
import pjsua2
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.sip.pjsip_container
import gtkapplication.api.sip.logger
import gtkapplication.api.sip.account
import gtkapplication.api.sip.buddy
import gi
gi.require_version('Gtk','3.0')
from gi.repository import GObject,GLib
class PjSipLifeCycleManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._source_tag=None
		self._total_event_count=0
	@property
	def total_event_count(self):
		return self._total_event_count
	def startup(self):
		self._logger.debug("entered startup()")
		ep_cfg=pjsua2.EpConfig()
		ep_cfg.uaConfig.mainThreadOnly=True
		ep_cfg.uaConfig.threadCnt=0
		version=pkg_resources.require("gtkapplication")[0].version
		ep_cfg.uaConfig.userAgent="pyphone-{0}".format(version)
		self._logger.debug('ep_cfg.uaConfig.userAgent = %s',ep_cfg.uaConfig.userAgent)
		ep_cfg.logConfig.msgLogging=1
		ep_cfg.logConfig.level=5
		ep_cfg.logConfig.consoleLevel=5
		decor=pjsua2.PJ_LOG_HAS_YEAR|pjsua2.PJ_LOG_HAS_MONTH|pjsua2.PJ_LOG_HAS_DAY_OF_MON|pjsua2.PJ_LOG_HAS_TIME|pjsua2.PJ_LOG_HAS_MICRO_SEC|pjsua2.PJ_LOG_HAS_SENDER|pjsua2.PJ_LOG_HAS_NEWLINE|pjsua2.PJ_LOG_HAS_SPACE|pjsua2.PJ_LOG_HAS_THREAD_SWC|pjsua2.PJ_LOG_HAS_INDENT
		self._logger.debug('decor = %s',decor)
		ep_cfg.logConfig.decor=decor
		ep_cfg.logConfig.filename="logs/pjsip.log"
		ep_cfg.logConfig.fileFlags=pjsua2.PJ_O_APPEND
		pjsip_log_writer=gtkapplication.api.sip.logger.PjLogger()
		ep_cfg.logConfig.writer=pjsip_log_writer
		sip_container=gtkapplication.api.sip.pjsip_container.sip_container
		sip_container.pjsip_log_writer=pjsip_log_writer
		sip_container.ep=pjsua2.Endpoint()
		ep=sip_container.ep
		ep.libCreate()
		ep.libInit(ep_cfg)
		pjsip_version=ep.libVersion().full
		self._logger.debug('pjsip_version = %s',pjsip_version)
		sip_udp_tranport_config=pjsua2.TransportConfig()
		sip_udp_tranport_config.port=5060
		sip_udp_tranport_config.enabled=1
		ep.transportCreate(pjsua2.PJSIP_TRANSPORT_UDP,sip_udp_tranport_config)
		self._logger.debug("transport created")
		acfg=pjsua2.AccountConfig()
		acfg.idUri=gtkapplication.data.config_data.PROFILE_DATA['sip_uri']
		acfg.regConfig.registrarUri=gtkapplication.data.config_data.PROFILE_DATA['sip_registrar_uri']
		acfg.regConfig.registerOnAdd=True
		acfg.regConfig.timeoutSec=60
		acfg.regConfig.retryIntervalSec=60
		aci=pjsua2.AuthCredInfo()
		aci.scheme="digest"
		aci.realm="*"
		aci.username=gtkapplication.data.config_data.PROFILE_DATA['sip_username']
		aci.dataType=0
		aci.data=gtkapplication.data.config_data.PROFILE_DATA['sip_password']
		aciv=pjsua2.AuthCredInfoVector()
		aciv.append(aci)
		acfg.sipConfig.authCreds=aciv
		sip_container.sip_account_list.append(gtkapplication.api.sip.account.Account(acfg))
		sip_account=sip_container.sip_account_list[0]
		sip_account.cfg=acfg
		sip_account.create(acfg,True)
		presence_status=pjsua2.PresenceStatus()
		presence_status.status=pjsua2.PJSUA_BUDDY_STATUS_ONLINE
		sip_account.setOnlineStatus(presence_status)
		self._logger.debug("sip account created: %r",sip_account)
		bcfg=pjsua2.BuddyConfig()
		bcfg.uri=gtkapplication.data.config_data.PROFILE_DATA['sip_buddy_uri']
		bcfg.subscribe=True
		buddy=gtkapplication.api.sip.buddy.Buddy(sip_account)
		buddy.create(sip_account,bcfg)
		sip_account.server_buddy=buddy
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		contact_manager.create_free_buddy_contacts(sip_account)
		acfg=pjsua2.AccountConfig()
		acfg.idUri=gtkapplication.data.config_data.PROFILE_DATA['twilio_sip_uri']
		acfg.regConfig.registrarUri=gtkapplication.data.config_data.PROFILE_DATA['twilio_sip_registrar_uri']
		self._logger.debug("twilio sip_uri = '%s', registrar = %s",acfg.idUri,acfg.regConfig.registrarUri)
		acfg.regConfig.registerOnAdd=True
		acfg.regConfig.timeoutSec=60
		acfg.regConfig.retryIntervalSec=60
		aci=pjsua2.AuthCredInfo()
		aci.scheme="digest"
		aci.realm="*"
		aci.username=gtkapplication.data.config_data.PROFILE_DATA['twilio_sip_username']
		aci.dataType=0
		aci.data=gtkapplication.data.config_data.PROFILE_DATA['twilio_sip_password']
		aciv=pjsua2.AuthCredInfoVector()
		aciv.append(aci)
		acfg.sipConfig.authCreds=aciv
		sip_container.sip_account_list.append(gtkapplication.api.sip.account.Account(acfg))
		twilio_sip_account=sip_container.sip_account_list[1]
		twilio_sip_account.cfg=acfg
		twilio_sip_account.create(acfg,True)
		presence_status=pjsua2.PresenceStatus()
		presence_status.status=pjsua2.PJSUA_BUDDY_STATUS_ONLINE
		twilio_sip_account.setOnlineStatus(presence_status)
		ep.libStart()
		self._logger.debug("after libStart()")
		tone_generator=pjsua2.ToneGenerator()
		tone_generator.createToneGenerator(16000,1)
		sip_container.tone_generator=tone_generator
		self._logger.debug("tone generator created")
		self._source_tag=GObject.timeout_add(50,self.poll_pjsip_events_timer,False)
		self._logger.debug("timer started source_tag is %s",self._source_tag)
		self._logger.info("timer started")
	def poll_pjsip_events_timer(self,quitting):
		if quitting:
			self._logger.debug("quitting detected, terminating polling, source tag is %s",self._source_tag)
			assert self._source_tag is not None
			GLib.source_remove(self._source_tag)
			self._logger.debug("removed source tag")
			self._source_tag=None
			return False
		else:
			pjsip_endpoint=gtkapplication.api.sip.pjsip_container.sip_container.ep
			event_count=pjsip_endpoint.libHandleEvents(10)
			self._total_event_count+=event_count
			if event_count<0:
				self._logger.error("libHandleEvents returned %s",event_count)
			elif event_count>3:
				self._logger.debug('event_count current = %d, total = %d',event_count,self._total_event_count)
			if self._total_event_count%5==0:
				self._logger.debug("%d total events processed",self._total_event_count)
				self._total_event_count+=1
			return True
	def shutdown(self):
		self._logger.debug('entered shutdown')
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		contact_manager.destroy_free_buddy_contacts()
		self._logger.debug("free buddies destroyed")
		sip_container=gtkapplication.api.sip.pjsip_container.sip_container
		while sip_container.sip_account_list:
			account=sip_container.sip_account_list.pop()
			if account.server_buddy is not None:
				self._logger.debug("deleting buddy %r",account.server_buddy)
				account.server_buddy=None
			self._logger.debug("deleting acc %r",account)
			account=None
		self._logger.debug("accounts deleted")
		sip_container.sip_account_list=None
		self._logger.debug('removed accounts')
		sip_container.tone_generator.stop()
		sip_container.tone_generator=None
		sip_container.ep.libDestroy()
		self._logger.debug('pjsip endpoint destroyed')
		self.poll_pjsip_events_timer(True)
		self._logger.debug("timer stopped")
		self._logger.debug("total events processed = %d",self._total_event_count)
		sip_container.ep=None
		sip_container.pjsip_log_writer=None
		sip_container=None
		self._logger.debug('exiting shutdown')