
[Referencia ZTNA EMS Saas](https://fortinetweb.s3.amazonaws.com/docs.fortinet.com/v2/attachments/f2e44070-1152-11ee-8e6d-fa163e15d75b/Zero_Trust_Network_Access-7.2.5-ZTNA_CASB_Protection_for_SaaS_Apps.pdf)

### FORTIEMS 
> Configurações necessárias no FortiEMS</br></br>

Endpint Profiles > ZTNA Destinations</br></br></br></br>

![image](https://github.com/user-attachments/assets/315a3980-255f-4919-84ac-67e1ac4149f3)</br></br></br></br>


### FORTIGATE 
> Configurações necessárias di Fortigate 7.2
```
config firewall vip
    edit "teste_ZTNA"
        set uuid 00af4d36-9622-51ef-0803-3a226f0950c7
        set type access-proxy
        set extip 141.18.147.241
        set extintf "port1"
        set server-type https
        set extport 8843
        set ssl-certificate "Fortinet_SSL"
    next
end
```
```
config firewall access-proxy
    edit "teste_ZTNA"
        set vip "teste_ZTNA"
        config api-gateway
            edit 1
                set url-map "/saas"
                set service saas
                set application "dropbox"
            next
            edit 2
                config realservers
                    edit 1
                        set addr-type fqdn
                        set address "drop"
                    next
                end
```
```
config firewall proxy-policy
    edit 1
        set uuid 7b09e834-9622-51ef-7044-99b8ba9f3d82
        set name "teste_ZTNA"
        set proxy access-proxy
        set access-proxy "teste_ZTNA"
        set srcintf "virtual-wan-link"
        set srcaddr "all"
        set dstaddr "all"
        set ztna-ems-tag "EMS1_ZTNA_TAG_Colaboradores"
        set action accept
        set schedule "always"
        set logtraffic all
    next
end
```





