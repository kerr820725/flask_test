from autoTest.ApiTestPC import ApiTestYFT
from page_objects.BasePages import *
from page_objects.BetPages import *

# page = LoginPage("dev02")
# page.login("twen103", "123qwe")
# page = BetPage_Btcffc(page)
# page.go_to()
# page.add_all_random()
# page.submit_trace()

yft = ApiTestYFT('yulin.qa', 'testxyft1800')
yft.test_bet_bjpk10_new(stop_on_win=True)
#
# yft = ApiTestYFT('m.yulin.qa', 'testxyft1800')
# yft.test_bet_fhxyft(stop_on_win=True)

# import json
# data = '{"lotteryType":"fhxyft","currIssueNo":"","stopOnWon":"","totalAmount":"","issueList":[],"schemeList":[],"timeZone":"GMT+8","isWap":false,"online":true}'
# data = json.loads(data)
# data['schemeList'] = '[{"playType":"pt330","betType":"bt02","betItem":"123457#123457#123457#123457#123457#1234#1234#1234#1234#1234#1234","betTimes":1,"potType":"Y","doRebate":"yes"}]'
# data['currIssueNo'] = '123456'
# data['stopOnWon'] = 'yes'
# data['totalAmount'] = '654321'
# data['issueList'] = '[1]'
# print(data)