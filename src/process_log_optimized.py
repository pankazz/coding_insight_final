import sys
import datetime
import time


login_fail = {}
d={}
time_dict = {}
ip_names={}
resources= {}
resources_bytes = {}
date_objects = {}
args=sys.argv
requests = []

def freq_ip(ip):
    
    if ip in ip_names:
        ip_names[ip] = ip_names[ip]+1
    else:
        ip_names[ip]=1


def heavy_resources(activity,bytes_used):

    if bytes_used =='-':
        bytes_used = 0
        
    if activity in resources:
        resources[activity] = resources[activity]+ int(bytes_used)
    else:
        resources[activity] = int(bytes_used)


def aggreg(datend_timeime):
    dtime = date_objects[datend_timeime]
    if dtime in time_dict:
        time_dict[dtime] = time_dict[dtime] +1
    else:
        time_dict[dtime] = 1


def blocked_requests(ip,date,activity,code):
    if date not in date_objects:
        date_objects[date] = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')

    time = date_objects[date]
    #time = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')
    if ip not in login_fail and code !='401':   #skip if it's not a login failed request
        return
    if ip in login_fail and code !='401' and activity!='/login' and login_fail[ip]['flag']==False:       #continue if not failed request and ip not in blocked state and not a login request
        return
    if code=='200' and activity=='/login' and ip in login_fail:       #if successful login and 3 attempts not made
        if login_fail[ip]['flag']==False:
            login_fail.pop(ip)
            return
        if login_fail[ip]['flag']==True and (time-login_fail[ip]['t3']).total_seconds() < 300:      #if successful login but in blocked state
            """with open(args[5],'a') as blocked:
                blocked.write(each+'\n')
                blocked.close()"""
            requests.append(each)
            return
    if code == '401':
        if ip not in login_fail:
            login_fail[ip] = {'t1' : time, 't2':None,'t3':None,'flag':False}    #first time failed login
            return
        else:                           
            if login_fail[ip]['flag']==True and (time - login_fail[ip]['t3']).total_seconds()<300: #if already failed and blocked
                """with open(args[5],'a') as blocked:
                    blocked.write(each+'\n')
                    blocked.close()"""
                requests.append(each)
                return
            if login_fail[ip]['flag']==True and (time - login_fail[ip]['t3']).total_seconds()>300: #if failed attempt and blocked state is over
                    login_fail[ip]['t1'] = time
                    login_fail[ip]['t2'] = None
                    login_fail[ip]['t3'] = None
                    login_fail[ip]['flag'] = False
                    return
            if login_fail[ip]['t2'] is None:                    
                if (time-login_fail[ip]['t1']).total_seconds() < 20:        #if 2nd failed attempt and within time range
                    login_fail[ip]['t2'] = time
                    return
                else:
                    login_fail[ip]['t1'] = time
                    return #if 2nd failed attempt and difference > 20 seconds, it becomes first failed attempt
            else:
                if login_fail[ip]['t3'] is None:                            #if 3rd failed attempt
                    if (time-login_fail[ip]['t2']).total_seconds() < 20 and (time-login_fail[ip]['t1']).total_seconds() < 20: #if 3rd failed attempt and in less than 20 secs from previous
                        login_fail[ip]['t3'] = time
                        login_fail[ip]['flag'] = True
                        return
                    if (time-login_fail[ip]['t2']).total_seconds() > 20:        #if 3rd failed attempt but after 20 seconds of 2nd, it becomes first 
                        login_fail[ip]['t1'] = time
                        login_fail[ip]['t2'] = None 
                        return
                    if (time-login_fail[ip]['t2']).total_seconds() < 20 and (time-login_fail[ip]['t1']).total_seconds() > 20:  #if 3rd failed attempt and after 20 seconds from first, second becomes first and this becomes 2nd
                        login_fail[ip]['t1'] = login_fail[ip]['t2']
                        login_fail[ip]['t2'] = time
                        return
    else:

        if ip not in login_fail:        #if not failed attempt and not in map
            return
        if ip in login_fail and login_fail[ip]['flag']==False:  #if not failed attempt and not blocked too
            return
        if ip in login_fail and login_fail[ip]['flag']==True and (time - login_fail[ip]['t3']).total_seconds()<300:   #if a blocked request
            requests.append(each)
            return
            """with open(args[5],'a') as blocked:
                blocked.write(each+'\n')
                blocked.close()
                return"""
        if login_fail[ip]['flag']==True and (time-login_fail[ip]['t1']).total_seconds() > 300:    #if it's past 5 minuetes blocked state
            login_fail.pop(ip)
            return
    return


with open(args[1],'r') as data:
    log = data.read().splitlines()

size = len(log)-1

for each in log:
    parts = each.split(' ')
    date  = parts[3].replace('[','')

    freq_ip(parts[0])

    heavy_resources(parts[6],parts[len(parts)-1])

    blocked_requests(parts[0],date,parts[6],parts[len(parts)-2])

    aggreg(date)

#lis.append((end,count))   #to take care of the last case

# sort ip by their values
sorted_ips = sorted(ip_names.items(), key=lambda x: x[1],reverse=True)
with open(args[2],'w')as hosts:
    for i in range(0,10) if len(sorted_ips)>10 else range(0,len(sorted_ips)):
        hosts.write(sorted_ips[i][0]+','+str(sorted_ips[i][1])+'\n')


#sort resources by their value
sorted_res = sorted(resources.items(), key=lambda x: x[1],reverse=True)

with open(args[4],'w')as hosts:
    for i in range(0,10) if len(sorted_res)>10 else range(0,len(sorted_res)) :
        hosts.write(sorted_res[i][0]+'\n')




start = log[0].split(' ')[3].replace('[','')
end  = log[size].split(' ')[3].replace('[','')

time_zone = log[0].split(' ')[4].replace(']','')

start_time = date_objects[start]
end_time = date_objects[end]

time_max = start_time + datetime.timedelta(seconds=3600)

start_value = time_dict[start_time]

#count = 0
summ = start_value
j =  start_time + datetime.timedelta(seconds=1)
while start_time <= end_time:
    while j <= time_max:
        #next_time =  datetime.datetime.strftime(j,'%d/%b/%Y:%H:%M:%S')
        if j in time_dict:
            summ = summ + time_dict[j]
            j =  j+ datetime.timedelta(seconds=1)
        else:
            j =  j+ datetime.timedelta(seconds=1)

    d[start_time] = summ

    if start_time in time_dict:
        summ = summ - time_dict[start_time]
    start_time = start_time+datetime.timedelta(seconds=1)
    time_max = time_max + datetime.timedelta(seconds=1)


sorted_wind = sorted(d.items(), key=lambda x: x[1],reverse=True)
if len(sorted_wind) > 10:
    sorted_wind = sorted_wind[0:10]
sorted_wind.sort(key=lambda x: x[0])
sorted_wind.sort(key=lambda x: x[1], reverse=True)


#the test case had no new line in hours.txt but it had in hosts and resources. So formatting accordingly

with open(args[3],'w')as hosts:
    if len(sorted_wind)>10:
        length  = 10
    else:
        length = len(sorted_wind)

    for i in range(0,length):

        if i < length -1:
            hosts.write(datetime.datetime.strftime(sorted_wind[i][0],'%d/%b/%Y:%H:%M:%S')+' '+ time_zone+','+str(sorted_wind[i][1])+'\n')
        else:
            hosts.write(datetime.datetime.strftime(sorted_wind[i][0],'%d/%b/%Y:%H:%M:%S')+' '+ time_zone+','+str(sorted_wind[i][1]))


with open(args[5],'w') as blocked:
    for k in range(0,len(requests)):
        blocked.write(requests[k]+'\n')
    blocked.close()