[Restrição por domino e-mail](https://docs.fortinet.com/document/fortigate/6.2.0/new-features/480209/restricted-saas-access-0365-g-suite-dropbox)</br>
[Restrição por domino e-mail 2](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/8049/restricted-saas-access)</br>

### Restrição
 > Exemplo 4379 UAD
```
config firewall address
    edit "login.live.com"
        set type fqdn
        set fqdn "login.live.com"
    next
end
```
```
config web-proxy profile
   edit "SaaS-Tenant-Restriction"
        set header-client-ip pass
        set header-via-request pass
        set header-via-response pass
        set header-x-forwarded-for pass
        set header-front-end-https pass
        set header-x-authenticated-user pass
        set header-x-authenticated-groups pass
        set strip-encoding disable
        set log-header-change disable
        config headers
            edit 1
                set name "Restrict-Access-To-Tenants"
                set dstaddr "login.microsoftonline.com"
                set action add-to-request
                set base64-encoding disable
                set add-option new
                set protocol https http
                **set content "sicoob.com.br"** >>> dominio de e-mail
            next
            edit 2
                set name "Restrict-Access-Context" 
                set dstaddr "login.microsoftonline.com" 
                set action add-to-request
                set base64-encoding disable
                set add-option new
                set protocol https http
                **set content "b417b620-2ae9-4a83-ab6c-7fbd828bda1d"** >>> RESTRICT_ID Tenante
            next
            edit 3
                set name "sec-Restrict-Tenant-Access-Policy"
                set dstaddr "login.live.com"
                set action add-to-request
                set base64-encoding disable
                set add-option new
                set protocol https http
                set content "restrict-msa"
            next
        end	
	next		
end			
```
```

config firewall policy
     edit 1
		set name "WF"
		set uuid 09928b08-ce46-51e7-bd95-422d8fe4f200
		set srcintf "port10" "wifi"
		set dstintf "port9"
		set srcaddr "all"
		set dstaddr "all"
		set action accept
		set schedule "always"
		set service "ALL"
		**set webproxy-profile "SaaS-Tenant-Restriction"**  >>> Adicionar na regra via CLI
		set utm-status enable
		set utm-inspection-mode proxy
		set logtraffic all
		set webfilter-profile "blocktest2" 
                set application-list "g-default"
		set profile-protocol-options "protocol"
		set ssl-ssh-profile "protocols"
		set nat enable
	next
end
```
