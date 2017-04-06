import sys
from datetime import datetime
import time

def freq_ip(ip):
    ip_names = {}
    if ip in ip_names:
        ip_names[ip] = ip_names[ip]+1
    else:
        ip_names[ip]=1
    return


def heavy_resources(activity,bytes_used):
    if activity not in resources_bytes:
        
        resources_bytes[parts[6]]= int(bytes_used if bytes_used is not '-' else 0)

    if activity in resources:
        resources[activity] = resources[activity]+1
    else:
        resources[activity]=1

    return

def blocked_requests(ip,date,activity,code,login_fail):
    
    
    time = datetime.strptime(date.replace('[',''), '%d/%b/%Y:%H:%M:%S')

    if ip not in login_fail and code !='401':   #skip if it's not a login failed request
        return

    if ip in login_fail and code !='401' and activity!='/login' and login_fail[ip]['flag']==False:       #continue if not failed request and ip not in blocked state and not a login request
        return
    
    
    
    if code=='200' and activity=='/login' and ip in login_fail:       #if successful login and 3 attempts not made
        if login_fail[ip]['flag']==False:
            
            login_fail.pop(ip)
            return
        if login_fail[ip]['flag']==True and (time-login_fail[ip]['t3']).total_seconds() < 300:      #if successful login but in blocked state
            with open(args[5],'a') as blocked:
                blocked.write(each+'\n')
                blocked.close()
                return
        
    
    if code == '401':
            
        
        if ip not in login_fail:
            login_fail[ip] = {'t1' : time, 't2':None,'t3':None,'flag':False}    #first time failed login
            return
        else:                           
            if login_fail[ip]['flag']==True and (time - login_fail[ip]['t3']).total_seconds()<300: #if already failed and blocked
                with open(args[5],'a') as blocked:
                    blocked.write(each+'\n')
                    blocked.close()
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
            with open(args[5],'a') as blocked:
                blocked.write(each+'\n')
                blocked.close()
                return
        if login_fail[ip]['flag']==True and (time-login_fail[ip]['t1']).total_seconds() > 300:    #if it's past 5 minuetes blocked state
            login_fail.pop(ip)
            return
    print("hello")
    return






login_fail = {}


args = sys.argv
print args

resources= {}
resources_bytes = {}
with open(args[1],'r') as data:
    log = data.read().splitlines()



        
    
    
for each in log:

    
    parts = each.split(' ')
    
    
    #freq_ip(parts[0])
    #heavy_resources(parts[6],parts[len(parts)-1])

    blocked_requests(parts[0],parts[3],parts[6],parts[len(parts)-2],login_fail)


        
"""        

sorted_ips = sorted(ip.items(), key=lambda x: x[1],reverse=True)

print type(sorted_ips)

with open(args[2],'w')as hosts:
    for i in range(0,10) if len(sorted_ips)>10 else range(0,len(sorted_ips)):
        hosts.write(sorted_ips[i][0]+','+str(sorted_ips[i][1])+'\n')


res_value = {}


for key, value in resources.items():
    res_value[key] = value * resources_bytes[key]

sorted_res = sorted(res_value.items(), key=lambda x: x[1],reverse=True)

with open(args[4],'w')as hosts:
    for i in range(0,10) if len(sorted_res)>10 else range(0,len(sorted_res)) :
        hosts.write(sorted_res[i][0]+'\n')

print("done")

    
"""

    



        








