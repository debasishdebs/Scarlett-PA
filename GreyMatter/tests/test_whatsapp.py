from yowsup.registration import WACodeRequest
import config as cfg


method = "sms"

config = cfg.WHATSAPP_ALT_NUM_DETAILS

codeReq = WACodeRequest(config['cc'], config['phone'], config['mcc'],
                        config['mnc'], config['sim_mcc'], config['sim_mnc'])

result = codeReq.send()
print(result)
