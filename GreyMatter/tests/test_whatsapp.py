from yowsup.registration import WACodeRequest

method = "sms"

config = {
    'cc': '91',
    'mcc': '404',
    'sim_mcc': '000',
    'phone': '7406888020',
    'sim_mnc': '000',
    'mnc': '86'
}

codeReq = WACodeRequest(config['cc'], config['phone'], config['mcc'], config['mnc'], config['sim_mcc'], config['sim_mnc'])

result = codeReq.send()
print(result)