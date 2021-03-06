#!/usr/bin.env python
#coding=UTF-8

'''
    @author:nemo
    @date:2014-04-03
    @desc:
        elong的航班信息验证
'''

import re
import time
import datetime
import string
from common.logger import logger
from common.class_common import Flight
from util.crawl_func import crawl_single_page
from common.common import get_proxy, invalid_proxy

#elong机场中文名与iatacode对照表
airports_dict = {'香港国际机场':'HKG','青岛流亭':'TAO','雅加达机场':'JKT','重庆江北':'CKG','西安咸阳':'XIY',\
        '登帕萨机场':'DPS','澳门国际机场':'MFM','深圳宝安':'SZX','武汉天河':'WUH','杭州萧山':'HGH',\
        '成都双流':'CTU','广州新白云':'CAN','大连周水子':'DLC','南京禄口':'NKG','北京首都机场':'PEK',\
        '上海虹桥':'SHA','上海浦东':'PVG','三亚凤凰':'SYX','名古屋机场':'NGO','日本东京羽田机场':'HND',\
        '台北松山机场':'TSA','迪拜机场':'DXB','图拉曼里机场':'MEL','巴黎戴高乐机场':'CDG','斯德哥尔摩阿兰达机场':'ARN',\
        '波士顿机场':'BOS','华盛顿罗纳尔德－里根国家机场':'DCA','火奴鲁鲁机场':'NHL','拉斯维加斯机场':'LAS',\
        '迈阿密机场':'MIA','纽约肯尼迪国际机场':'JFK','西雅图机场':'SEA','芝加哥奥黑尔国际机场':'ORD','莫斯科多莫杰多沃机场':'DME',\
        '哥本哈根机场':'CPH','阿克纠宾斯克机场':'AKX','雅典机场':'ATH','约翰内斯堡机场':'JNB','柏林舍讷费尔德机场':'SXF',\
        '法兰克福机场':'FRA','慕尼黑机场':'MUC','马尼拉机场':'MNL','普吉国际机场':'HKT','新加坡机场':'SIN',\
        '多伦多机场':'YYZ','温哥华机场':'YVR','布里斯班机场':'BNE','巴黎奥利机场':'ORY','尼斯机场':'NCE',\
        '奥兰多国际机场':'MCO','丹佛机场':'DEN','华盛顿杜勒斯机场':'IAD','洛杉矶机场':'LAX','旧金山机场':'SFO',\
        '悉尼机场':'SYD','亚特兰大机场':'ATL','汉堡机场':'HAM','台北桃园机场':'TPE','金浦国际机场':'GMP',\
        '仁川国际机场':'ICN','皮埃尔埃利奥特特鲁多国际机场':'YUL','日本东京成田机场':'NRT','大阪关西机场':'KIX',\
        '马德里机场':'MAD','维也纳机场':'VIE','胡志明市机场':'SGN','罗马费米齐诺机场':'FCO','米兰马尔本萨机场':'MXP',\
        '河内机场':'HAN','开罗机场':'CAI','曼谷(素万那普)机场':'BKK','吉隆坡机场':'KUL','金边机场':'PNH',\
        '伦敦希思罗机场':'LHR','柏林泰格尔机场':'TXL','赫尔辛基机场':'HEL','布鲁塞尔机场':'BRU','伊斯坦布尔机场':'IST',\
        '莫斯科谢列梅捷沃机场':'SVO','莫斯科伏努科沃机场':'VKO','阿姆斯特丹机场':'AMS','底特律机场':'DTT','米兰里奈特机场':'LIN','苏黎世机场':'ZRH',\
        '伦敦盖特维克机场':'LGW','纽约纽瓦克机场':'EWR','威尼斯机场':'VCE','佛罗伦萨机场':'FLR','巴塞罗那机场':'BCN',\
        '布拉格机场':'PRG','日内瓦机场':'GVA','科隆/波恩机场':'CGN','爱丁堡国际机场':'EDI','布达佩斯机场':'BUD','纽约拉瓜迪亚机场':'LGA',\
        '英曼彻斯特机场':'MAN','波泰拉机场':'LIS','纽卡斯尔':'NCL','都灵机场':'TRN','来比锡机场':'LEJ','马拉加机场':'AGP',\
        '不莱梅机场':'BRE','波伦亚机场':'BLQ','波尔多国际机场':'BOD','华沙机场':'WAW','马赛国际机场':'MRS','那不勒斯机场':'NAP',\
        '瓦伦西亚机场':'VLC','纽伦堡机场':'NUE','波尔多国际机场':'BOD','波尔图机场':'OPO','格拉斯哥国际机场':'GLA',\
        '杜塞尔多夫机场':'DUS','斯图加特国际机场':'STR','巴塞尔机场':'BSL','奥斯陆机场':'OSL','卑尔根机场':'BGO','伯明翰机场':'BHX',\
        '贝尔法斯特机场':'BHD','维罗纳机场':'VRN','卢森堡机场':'LUX'}

#elong iatacode与城市拼音（英文名）对照表
cities_dict = {'CPH': 'copenhagen', 'LIN': 'milan', 'AGB': 'augsburg', 'BGO': 'bergen', 'HEL': 'helsinki', 'NAP': 'naples', 'LIS': 'lisbon',\
        'BOD': 'bordeaux', 'FNI': 'nimes', 'AGP': 'malaga', 'SXB': 'strasbourg', 'SXF': 'berlin', 'LYS': 'lyon', 'LBA': 'leeds', 'HAJ': 'hannover',\
        'HAM': 'hamburg', 'MRS': 'marseille', 'BFS': 'belfast', 'LPL': 'liverpool', 'LHR': 'london', 'SVQ': 'seville', 'VIE': 'vienna',\
        'BVA': 'paris', 'MAD': 'madrid', 'LEJ': 'leipzig', 'MAN': 'manchester', 'TSF': 'venice', 'FLR': 'florence', 'BER': 'berlin',\
        'RTM': 'rotterdam', 'VLC': 'valencia', 'SZG': 'salzburg', 'OSL': 'oslo', 'AMS': 'amsterdam', 'BUD': 'budapest', 'STO': 'stockholm',\
        'TRN': 'turin', 'BLQ': 'bologna', 'PRG': 'prague', 'GRX': 'granada', 'OXF': 'oxford', 'PSA': 'pisa', 'MXP': 'milan', 'LCY': 'london',\
        'INN': 'innsbruck', 'ANR': 'antwerp', 'OPO': 'porto', 'BCN': 'barcelona', 'LUX': 'luxembourg city', 'GLA': 'glasgow', 'MUC': 'munich',\
        'LUG': 'lugano', 'CGN': 'cologne', 'BSL': 'basel', 'PMF': 'milan', 'SEN': 'london', 'NUE': 'nuremberg', 'VRN': 'verona', 'FCO': 'rome',\
        'FRA': 'frankfurt', 'WAW': 'warsaw', 'DUS': 'dusseldorf', 'LTN': 'london', 'CDG': 'paris', 'MMX': 'malmo', 'ORY': 'paris', 'BRU': 'brussels',\
        'EDI': 'edinburgh', 'BRS': 'bristol', 'BRN': 'bern', 'BRE': 'bremen', 'CIA': 'rome', 'TXL': 'berlin', 'VCE': 'venice', 'STN': 'london',\
        'GVA': 'geneva', 'GOA': 'genova', 'KLV': 'karlovy vary', 'STR': 'stuttgart', 'GOT': 'goteborg', 'ZRH': 'zurich', 'BHD': 'belfast',\
        'LGW': 'london', 'BHX': 'birmingham', 'NCL': 'newcastle', 'NCE': 'nice', 'ARN': 'stockholm','PVG':'shanghai','PEK':'beijing'}

#解析出含有航班信息的字段
flightPattern = re.compile(r'<tbody>(.*?)</tbody>',re.S)#每一个这样的结构都是一个完整的航班信息
typePattern = re.compile(r'<table(.*?)</table>',re.S)#找到table的数量来判断是不是中转航班，分别处理

#解析出一条航班的各类信息
classPattern = re.compile(r'<td class="cols(.*?)</td>',re.S)

URL = 'http://iflight.elong.com/%s/cn_day%d.html'

def elong_request_parser(content):
    
    result = -1

    try:
        infos = content.split('|')
        flight_info = infos[0].strip()
        time_info = infos[1].strip()
        ticketsource = infos[2].strip()

        flight_no = flight_info.split('-')[0]
        dept_id,dest_id = flight_info.split('-')[1],flight_info.split('-')[2]

        #date：20140510，time：09:10
        dept_day,dept_hour = time_info.split('_')[0],time_info.split('_')[1]

        dept_date = dept_day[0:4] + '-' + dept_day[4:6] + '-' + dept_day[6:]#2014-05-10

        dept_time = dept_date + 'T' + dept_hour + ':00'

        dept_id = cities_dict[dept_id]
        dest_id = cities_dict[dest_id]
        location = dept_id +  '-' + dest_id

        origday = datetime.datetime(string.atoi(dept_date[0:4]),string.atoi(dept_date[5:7]),string.atoi(dept_date[8:]))
        urlday = (origday - datetime.datetime.today()).days
        #dept_date = orig_date
        #logger.info('contents: %s %s %s %s '%(location,flight_no,dept_date,str(urlday)))
    except Exception,e:
        logger.error(str(e))
        logger.error('Content Error: Wrong content format with %s'%content)
        return result
    
    url = URL%(location,urlday)

    p = get_proxy(source='elongFlight')

    htmlcontent = crawl_single_page(url,n=1,proxy = p)
    if htmlcontent == '':
        invalid_proxy(p)
        logger.error('Proxy Error: htmlcontent is null with proxy: %s'%p)
        return result
    
    #判断是否返回导航页，返回导航页说明content没有航班信息
    
    #判断是否找到航班信息，没有返回[]
    temp_flight_list = flightPattern.findall(htmlcontent)
    if len(temp_flight_list) == 1:
        logger.error('Parser Error: cannot find flights with %s'%location)
        return result

    flight_list = temp_flight_list[:-1]
    
    #flights = []
    typ = 0
    for item in flight_list:
        typ = len(typePattern.findall(item))
        if typ == 0:
            pass
        elif typ != 1:
            transferFlight = transferFlight_parser(item,dept_date,airports_dict)
            if transferFlight.dept_time == dept_time and transferFlight.flight_no == flight_no:#transferFlight.dest_id == dest_id and transferFlight.dept_id == dept_id and transferFlight.flight_no == flight_no:
                return transferFlight.price
        else:
            directFlight = directFlight_parser(item,dept_date,airports_dict)
            if directFlight.dept_time == dept_time and directFlight.flight_no == flight_no:#directFlight.dest_id == dest_id and directFlight.dept_id == dept_id and directFlight.flight_no == flight_no:
                return directFlight.price             
    return result
def directFlight_parser(flightstring,date,airports_dict):
    flight = Flight()

    #直达航班提取出长度为1的列表
    cols01 = re.compile(r'<td class="cols01">(.*?)</td>',re.S).findall(flightstring)[0]
    cols02 = re.compile(r'<td class="cols02">(.*?)</td>',re.S).findall(flightstring)[0]
    cols03 = re.compile(r'<td class="cols03">(.*?)</td>',re.S).findall(flightstring)[0]
    cols04 = re.compile(r'<td class="cols04">(.*?)</td>',re.S).findall(flightstring)[0]
    cols05 = re.compile(r'<td class="cols05">(.*?)</td>',re.S).findall(flightstring)[0]
    cols06 = re.compile(r'<td class="cols06">(.*?)</td>',re.S).findall(flightstring)[0]

    aircorp = re.compile(r'</span>(.*?)<br />',re.S).findall(cols01)[0].strip()
    flight_no = re.compile(r'<br />(.*?)&nbsp',re.S).findall(cols01)[0].strip()
    plane_type = re.compile(r'method="PlaneType" >(.*?)</a>',re.S).findall(cols01)[0].strip()

    airports = []
    days = 0
    dept_airport = re.compile(r'</span>(.*?)<br />',re.S).findall(cols02)[0].strip()
    dept_time = re.compile(r'<span class=" t14 bold black">(.*?)</span>',re.S).findall(cols02)[0].strip()
    arr_time_airport = re.compile(r'<br />(.*?)$',re.S).findall(cols02)[0].strip()
    if arr_time_airport.find('+1天') == -1:
        arr_time, arr_airport = arr_time_airport.split(' ')[0].strip(),arr_time_airport.split(' ')[-1].strip()
    else:
        days += 1
        arr_time, arr_airport = arr_time_airport.split(' ')[0].strip().split('(')[0].strip(),arr_time_airport.split(' ')[-1].strip()
    airports.append(dept_airport)
    airports.append(arr_airport)

    timeinfo = []
    during_time =  re.compile(r'(.*?)<br />',re.S).findall(cols03)[0].strip()
    timeinfo.append(dept_time)
    timeinfo.append(arr_time)
    timeinfo.append(during_time)
    
    during = 0#timeshifter(timeinfo)
    dept_date = datetime.datetime(string.atoi(date[0:4]),string.atoi(date[5:7]),string.atoi(date[8:]))
    dest_date = dept_date + datetime.timedelta(days)
    dept_daytime = date + 'T' + dept_time + ':00'
    dest_daytime = str(dest_date).split(' ')[0] + 'T' + arr_time + ':00'

    price = re.compile(r'</span>(.*?)</span>',re.S).findall(cols04)[0].strip()
    tax = re.compile(r'参考税 &yen;(.*?)<div class',re.S).findall(cols04)[0].strip()

    flight.flight_no = flight_no
    flight.plane_no = plane_type
    flight.airline = aircorp
    if airports_dict.has_key(airports[0]):
        flight.dept_id = airports_dict[airports[0]]
    else:
        flight.dept_id = airports[0]
    if airports_dict.has_key(airports[-1]):
        flight.dest_id = airports_dict[airports[-1]]
    else:
        flight.dest_id = airports[-1]
    flight.dept_day = date
    flight.dept_time = dept_daytime
    flight.dest_time = dest_daytime
    flight.dur = during
    flight.price = float(price)
    flight.tax = float(tax)
    flight.surcharge = -1.0
    flight.currency = 'CNY'
    flight.seat_type = '经济舱'
    flight.source = 'elong::elong'
    flight.return_rule = 'NULL'
    flight.stop = 0

    #flight_tuple = (flight.flight_no,flight.plane_no,flight.airline,flight.dept_id,flight.dest_id,flight.dept_day,\
            #flight.dept_time,flight.dest_time,flight.dur,flight.price,flight.tax,flight.surcharge,\
            #flight.currency,flight.seat_type,flight.source,flight.return_rule,flight.stop)

    #return flight_tuple
    return flight

def transferFlight_parser(flightstring,date,airports_dict):
    flight = Flight()
    
    #中转航班，cols01-03有多个，cols04-06有一个
    cols01 = re.compile(r'<td class="cols01">(.*?)</td>',re.S).findall(flightstring)
    cols02 = re.compile(r'<td class="cols02">(.*?)</td>',re.S).findall(flightstring)
    cols03 = re.compile(r'<td class="cols03">(.*?)</td>',re.S).findall(flightstring)
    cols04 = re.compile(r'<td class="cols04">(.*?)</td>',re.S).findall(flightstring)[0]
    cols05 = re.compile(r'<td class="cols05">(.*?)</td>',re.S).findall(flightstring)[0]
    cols06 = re.compile(r'<td class="cols06">(.*?)</td>',re.S).findall(flightstring)[0]

    flight.stop = len(cols01) - 1

    if flight.stop > 2:
        return [] #暂定不要两次以上转机的方案

    aircorps = []
    flight_nos = []
    plane_types = []
    dept_times = []
    during_times = []
    airports = []
    days = 0
    timeinfo = []
    i = 0
    for i in range(0,len(cols01)):
        aircorp = re.compile(r'</span>(.*?)<br />',re.S).findall(cols01[i])[0].strip()
        flight_no = re.compile(r'<br />(.*?)&nbsp',re.S).findall(cols01[i])[0].strip()
        plane_type = re.compile(r'method="PlaneType" >(.*?)</a>',re.S).findall(cols01[i])[0].strip()

        dept_airport = re.compile(r'</span>(.*?)<br />',re.S).findall(cols02[i])[0].strip()
        if dept_airport.find('+2天') != -1:
            days += 2
        elif dept_airport.find('+1天') != -1:
            days += 1
        
        arr_time_airport = re.compile(r'<br />(.*?)$',re.S).findall(cols02[i])[0].strip()
        dept_time = re.compile(r'<span class=" t14 bold black">(.*?)</span>',re.S).findall(cols02[i])[0].strip()
        if arr_time_airport.find('+1天') == -1:
            arr_time, arr_airport = arr_time_airport.split(' ')[0].strip(),arr_time_airport.split(' ')[-1].strip()
        else:
            arr_time, arr_airport = arr_time_airport.split(' ')[0].strip().split('(')[0].strip(),arr_time_airport.split(' ')[-1].strip()
            if i == len(cols01) - 1:
                days += 1

        during_time =  re.compile(r'(.*?)<br />',re.S).findall(cols03[i])[0].strip()

        aircorps.append(aircorp)
        flight_nos.append(flight_no)
        plane_types.append(plane_type)
        dept_times.append(dept_time)
        during_times.append(during_time)
        airports.append(dept_airport)
        airports.append(arr_airport)
        timeinfo.append(dept_time)
        timeinfo.append(arr_time)
        timeinfo.append(during_time)

    during = 0#timeshifter(timeinfo)
    dept_date = datetime.datetime(string.atoi(date[0:4]),string.atoi(date[5:7]),string.atoi(date[8:]))
    dest_date = dept_date + datetime.timedelta(days)
    dept_daytime = date + 'T' + timeinfo[0]  + ':00'
    dest_daytime = str(dest_date).split(' ')[0] + 'T' + timeinfo[-2] + ':00'

    price = re.compile(r'</span>(.*?)</span>',re.S).findall(cols04)[0].strip()
    tax = re.compile(r'参考税 &yen;(.*?)<div class',re.S).findall(cols04)[0].strip()
   
    if flight.stop == 1:
        flight_no_str = flight_nos[0]+'_'+flight_nos[1]
        plane_no_str = plane_types[0]+'_'+plane_types[1]
        aircorp_str = aircorps[0]+'_'+aircorps[1] #也可以改为多家航空公司
    elif flight.stop == 2:
        flight_no_str = flight_nos[0]+'_'+flight_nos[1]+'_'+flight_nos[2]
        plane_no_str = plane_types[0]+'_'+plane_types[1]+'_'+flight_nos[2]
        aircorp_str = aircorps[0]+'_'+aircorps[1]+'_'+aircorps[2] #也可以改为多家航空公司
    else:
        return []

    flight.flight_no = flight_no_str
    flight.plane_no = plane_no_str
    flight.airline = aircorp_str
    if airports_dict.has_key(airports[0]):
        flight.dept_id = airports_dict[airports[0]]
    else:
        flight.dept_id = airports[0]
    if airports_dict.has_key(airports[-1]):
        flight.dest_id = airports_dict[airports[-1]]
    else:
        flight.dest_id = airports[-1]
    flight.dept_day = date
    flight.dept_time = dept_daytime
    flight.dest_time = dest_daytime
    flight.dur = during
    flight.price = int(price)
    flight.tax = int(tax)
    flight.surcharge = -1.0
    flight.currency = 'CNY'
    flight.seat_type = '经济舱'
    flight.source = 'elong::elong'             
    flight.return_rule = 'NULL'
    
    #flight_tuple = (flight.flight_no,flight.plane_no,flight.airline,flight.dept_id,flight.dest_id,flight.dept_day,\
             #flight.dept_time,flight.dest_time,flight.dur,flight.price,flight.tax,flight.surcharge,\
             #flight.currency,flight.seat_type,flight.source,flight.return_rule,flight.stop)

    #return flight_tuple
    return flight

#飞行时长计算，输入list，长度为3的倍数，对应转机次数-1，三项分别为起飞时间，到达时间（当地），飞行时长
def timeshifter(timeinfo):
    during = 0
    dept_hour, dept_min = 0,0
    dest_hour, dest_min = 0,0
    transfer_hour, transfer_min = 0,0#计算待机时间

    length = len(timeinfo) / 3

    if length == 0:
        print "no timeinfo, cannot convert"
        return None
    elif length == 1:
        dept_hour,dept_min = int(timeinfo[0].split(':')[0]),int(timeinfo[0].split(':')[1])
        dest_hour,dest_min = int(timeinfo[1].split(':')[0]),int(timeinfo[1].split(':')[1])
        during_hour,min_str = int(timeinfo[2].split('小时')[0]),timeinfo[2].split('小时')[1]
        if min_str == '':
            during_min = 0
        else:
            during_min = int(min_str.split('分')[0])
        during = 3600 * during_hour + 60 * during_min
        return during
    else:
        dept_hour,dept_min = int(timeinfo[0].split(':')[0]),int(timeinfo[0].split(':')[1])
        dest_hour,dest_min = int(timeinfo[1].split(':')[0]),int(timeinfo[1].split(':')[1])
        during_hour,during_min = 0,0
        transfer_hour,transfer_min = 0,0
        for i in range(0,length - 1):
            dept_hour_temp,dept_min_temp = int(timeinfo[(i+1)*3+0].split(':')[0]),int(timeinfo[(i+1)*3+0].split(':')[1])
            during_hour_temp,min_str_temp = int(timeinfo[i*3+2].split('小时')[0]),timeinfo[i*3+2].split('小时')[1]
            if min_str_temp == '':
                during_min_temp = 0
            else:
                during_min_temp = int(min_str_temp.split('分')[0])
            dest_hour_temp,dest_min_temp = int(timeinfo[i*3+1].split(':')[0]),int(timeinfo[i*3+1].split(':')[1])
            transfer_min = dept_min_temp - dest_min_temp
            if transfer_min < 0:
                transfer_min += 60
                transfer_hour -= 1
            transfer_hour = dept_hour_temp - dest_hour_temp
            if transfer_hour < 0:
                transfer_hour += 24
            
            during_hour += (transfer_hour + during_hour_temp)
            during_min += (transfer_min + during_min_temp)
        
        during_hour_temp,min_str_temp = int(timeinfo[-1].split('小时')[0]),timeinfo[-1].split('小时')[1]
        if min_str_temp == '':
            during_min_temp = 0
        else:
            during_min_temp = int(min_str_temp.split('分')[0])
        during_hour += during_hour_temp
        during_min += during_min_temp

        during = 3600 * during_hour + 60 * during_min
        return during


if __name__ == '__main__':

    content = 'LH729_LH296-PVG-TRN|20140416_13:15|elong::elong'

    result = elong_request_parser(content)
    
    print str(result)
