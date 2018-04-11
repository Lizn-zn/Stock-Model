from WindPy import *
import os
w.start()
# get stock code in SH and SZ
AllAstock = w.wset("SectorConstituent")
stock_code = AllAstock.Data[1]
fields =  "ev,mkt_cap_ard,ev3,pe_ttm,val_pe_deducted_ttm,pe_lyr,pb_lf,pb_mrq,pb_lyr,ps_ttm,ps_lyr,pcf_ocf_ttm,pcf_ocflyr,pcf_ncf_ttm,pcf_nflyr"
date = ['0131','0228','0331','0430','0531','0630','0731','0831','0930','1031','1130','1231']
year = 2010
for t in range(8):
    year += t
    for i in range(len(date)):
        guzhi_data = w.wss(stock_code,fields,"unit=1;tradeDate=" + str(year)+date[i]+";currencyType=")
        if not (os.path.exists('guzhi')):
            print("create dict")
            os.mkdir('guzhi')
        file = open('guzhi/'+str(year)+date[i]+'.csv','w')
        file.write(str(guzhi_data.Data[0]))
        file.close()
file = open('guzhi/readme.txt')
file.write('this is guzhi data,the data is ev,mkt_cap_ard,ev3,pe_ttm,val_pe_deducted_ttm,pe_lyr,pb_lf,pb_mrq,pb_lyr,ps_ttm,ps_lyr,pcf_ocf_ttm,pcf_ocflyr,pcf_ncf_ttm,pcf_nflyr')
file.close()

print(guzhi_data)