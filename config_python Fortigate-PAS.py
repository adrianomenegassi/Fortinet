# Função para substituir variáveis no texto
def substituir_variaveis(texto, variaveis):
    for chave, valor in variaveis.items():
        texto = texto.replace(f"${chave}", valor)
    return texto

# Dicionário de variáveis com descrições
variaveis = {
    "PA": "Número da PA",
    "UAD": "Número da UAD (43xx)",
    "LAN_INTERFACE": "Interface à qual a VLAN será vinculada (lan1?)",
    "IP_SRV_UAD": "IP do servidor AD e DNS da UAD",
    "HOSTNAME_SRV": "Hostname do servidor da UAD",
    "IP_UAD": "Número do segundo octeto utilizado para o bloco de IPs das PAs",
    "VTI_2009": "Final do IP do VTI utilizado pela PA na central",
    "SUBNET_UAD": "Subnet inteira da UAD (ex: 10.241.240.0 255.255.240.0)",
    "HOSTNAME": "Hostname do firewall da PA (FG_43xx_xx)",
    "IF_WLAN": "Qual interface da Wlan (lan2?)",
    "WAN01": "IP e subnet utilizado para o link primário",
    "GW_WAN01": "Gateway da operadora da WAN01",
    "ISP_WAN01": "Descricao da operadora utilizada na WAN01",
    "WAN02": "IP e subnet utilizado para o link secundário",
    "GW_WAN02": "Gateway da operadora da WAN02",
    "ISP_WAN02": "Descricao da operadora utilizada na WAN02",
    "WAN03": "IP e subnet utilizado para o link Multisicoob",
    "GW_WAN03": "Gateway da operadora Multisicoob",
    "ISP_WAN03": "Descricao da operadora Multisicoob",
}

# Perguntar ao usuário se deseja configurar
configurara = input("Deseja gerar uma nova configuração do Fortigate (S/N)? ").strip().lower()

if configurara == 's':
    # Solicitar ao usuário quais blocos deseja configurar
    configurar_wan1 = input("Configurar Internet WAN1 (S/N): ").strip().lower()
    configurar_wan2 = input("Configurar Internet WAN2 (S/N): ").strip().lower()
    configurar_multisicoob = input("Configurar link Multisicoob (S/N): ").strip().lower()
    configurar_fortilink = input("Configurar Fortilink para fortiswitch (S/N): ").strip().lower()
    #configurar_lan = input("Configurar bloco LAN (S/N): ").strip().lower() 
    configurar_vlans = input("Configurar VLANS padrão (S/N): ").strip().lower()
    configurar_wlan = input("Configurar WLAN padrão Wifi(S/N): ").strip().lower()
    configurar_geral = input("Configurar demais config Gerais (S/N): ").strip().lower()
    
   

    # Solicitar ao usuário os valores das variáveis relacionadas aos blocos selecionados
    for chave, descricao in variaveis.items():
        if (
            (configurar_wan1 == 's' and chave in ["WAN01", "GW_WAN01", "ISP_WAN01", "PA", "UAD"]) or
            (configurar_wan2 == 's' and chave in ["WAN02", "GW_WAN02", "ISP_WAN02", "PA", "UAD"]) or
            (configurar_multisicoob == 's' and chave in ["WAN03", "GW_WAN03", "ISP_WAN03", "PA", "UAD"]) or
            (configurar_fortilink == 's' and chave in ["PA", "IP_UAD", "LAN_INTERFACE"]) or
            #(configurar_lan == 's' and chave in ["PA", "IP_UAD", "LAN_INTERFACE"]) or
            (configurar_fortilink == 's' and chave in ["PA", "IP_UAD", "LAN_INTERFACE"]) or
            (configurar_vlans == 's' and chave in ["PA", "IP_UAD", "LAN_INTERFACE"]) or
            (configurar_wlan == 's' and chave in ["IF_WLAN"]) or
            (configurar_geral == 's' and chave in [ "HOSTNAME_SRV", "PA", "UAD", "LAN_INTERFACE", "SUBNET_UAD", "VTI_2009", "IP_UAD", "IP_SRV_UAD", "HOSTNAME"])
         ):
            valor = input(f"Digite o {descricao}: ")
            variaveis[chave] = valor

    # Modelo de configuração
    configuracao = """
    # Prepara interfaces
    config system interface
     edit fortilink
      unset member a
      set status down
      end
    config firewall policy
    delete 1
    end
    config system dhcp server
    delete 1
    end
    config firewall address
    delete lan
    end
    config system virtual-switch
        edit "lan"
            set physical-switch "sw0"
            config port
    delete lan1
    delete lan2
    delete lan3 
    end
    config system virtual-switch
    delete lan
    end
   """
    # Condições para configurar os blocos selecionados
    if configurar_wan1 == 's':
        configuracao += """
        config system interface
            edit "wan"
                set vdom "root"
                set mode static        
                set ip $WAN01
                set allowaccess ping
                set type physical
                set description "$ISP_WAN01"
                set alias "WAN01"
                set lldp-reception enable
                set role wan
            next
        end """
    if configurar_wan2 == 's':
        configuracao += """
        config system interface
            edit "a"
                set vdom "root"
                set mode static
                set ip $WAN02
                set allowaccess ping
                set type physical
                set description "$ISP_WAN02"
                set alias "WAN02"
                set lldp-reception enable
                set role wan
            next
        end """
    if configurar_multisicoob == 's':    
        configuracao += """
        config system interface
            edit "lan3"
                set vdom "root"
                set mode static
                set ip $WAN03
                set allowaccess ping
                set type physical
                set description "$ISP_WAN03"
                set alias "MPLS"
                set lldp-reception enable
                set role wan
            next    
        end """
   #### CASO SEJA FORTSWITCH UTILIZAR O FORTILINK #####     
    if configurar_fortilink == 's':
         configuracao += """
        config system interface
         edit "fortilink"
        set vdom "root"
        set fortilink enable
        set ip 10.255.1.1 255.255.255.0
        set allowaccess ping fabric
        set type aggregate
        set member "a"
        set lldp-reception enable
        set lldp-transmission enable
        set switch-controller-nac "fortilink"
        set switch-controller-dynamic "fortilink"
        set swc-first-create 255
               next
        end """
        
    if configurar_vlans == 's':
         configuracao += """
           config system interface
          edit "IF_LAN"
           set vdom "root"
           set ip 10.$IP_UAD.$PA.1 255.255.255.128
          set allowaccess ping https ssh snmp http fgfm
          set device-identification enable
        set role lan
        set interface "$LAN_INTERFACE"
        set vlanid 240
    next
    edit "IF_ATM"
        set vdom "root"
        set ip 10.$IP_UAD.$PA.161 255.255.255.224
        set allowaccess ping
        set device-identification enable
        set role lan
        set interface "$LAN_INTERFACE"
        set vlanid 241
    next
    edit "IF_DEVICES"
        set vdom "root"
        set ip 10.$IP_UAD.$PA.129 255.255.255.224
        set allowaccess ping
        set device-identification enable
        set role lan
        set interface "$LAN_INTERFACE"
        set vlanid 242
    next
    edit "IF_SEG"
        set vdom "root"
        set ip 10.$IP_UAD.$PA.193 255.255.255.224
        set allowaccess ping
        set device-identification enable
        set role lan
        set interface "$LAN_INTERFACE"
        set vlanid 243
    next
    edit "IF_VOIP"
        set vdom "root"
        set ip 10.$IP_UAD.$PA.225 255.255.255.224
        set allowaccess ping
        set device-identification enable
        set role lan
        set interface "$LAN_INTERFACE"
        set vlanid 244
    next
     end
    config system zone
    edit "ZN_LAN"
        set interface "IF_ATM" "IF_DEVICES" "IF_LAN" "IF_SEG" "IF_VOIP"
    next
    end     """
    if configurar_wlan == 's':
         configuracao += """
     config system interface
      edit "$IF_WLAN"
        set vdom "root"
        set ip 10.253.253.1 255.255.255.0
        set allowaccess ping
        set type physical
        set alias "IF_WLAN_MGMT"
        set device-identification enable
            next
            edit "IF_WLAN_CORP"
        set vdom "root"
        set ip 10.250.250.1 255.255.255.0
        set allowaccess ping
        set device-identification enable
        set interface "$IF_WLAN"
        set vlanid 250
        next
        edit "IF_WLAN_COLAB"
        set vdom "root"
        set ip 10.251.251.1 255.255.255.0
        set allowaccess ping
        set device-identification enable
        set interface "$IF_WLAN"
        set vlanid 251
        next
        edit "IF_WLAN_GUEST"
        set vdom "root"
        set ip 10.252.252.1 255.255.255.0
        set allowaccess ping
        set role lan
        set interface "$IF_WLAN"
        set vlanid 252
        next
        end 
        config system zone
       edit "ZN_LAN"
        set interface "IF_ATM" "IF_WLAN_CORP" "IF_DEVICES" "IF_LAN" "IF_SEG" "IF_VOIP"
       next
       edit "ZN_GUEST"
        set interface "IF_WLAN_COLAB" "IF_WLAN_GUEST"
        next
       end"""    
    if configurar_geral == 's':  
        configuracao += """

#######DHCP SERVERS#######
config system dhcp server
    edit 0
        set lease-time 0
        set ntp-service default
        set default-gateway 10.253.253.1
        set netmask 255.255.255.0
        set interface "$IF_WLAN"
        config ip-range
            edit 1
                set start-ip 10.253.253.254
                set end-ip 10.253.253.254
            next
        end
        set timezone-option default
        set dns-server1 8.8.8.8
        set dns-server2 1.1.1.1
    next
    edit 0
        set lease-time 0
        set ntp-service default
        set default-gateway 10.250.250.1
        set netmask 255.255.255.0
        set interface "IF_WLAN_CORP"
        config ip-range
            edit 1
                set start-ip 10.250.250.200
                set end-ip 10.250.250.240
            next
        end
        set timezone-option default
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set lease-time 0
        set ntp-service default
        set default-gateway 10.251.251.1
        set netmask 255.255.255.0
        set interface "IF_WLAN_COLAB"
        config ip-range
            edit 1
                set start-ip 10.251.251.100
                set end-ip 10.251.251.200
            next
        end
        set timezone-option default
        set dns-server1 8.8.8.8
        set dns-server2 1.1.1.1
    next
    edit 0
        set lease-time 28800
        set default-gateway 10.$IP_UAD.$PA.1
        set netmask 255.255.255.128
        set interface "IF_LAN"
        config ip-range
            edit 1
                set start-ip 10.$IP_UAD.$PA.2
                set end-ip 10.$IP_UAD.$PA.126
            next
        end
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set default-gateway 10.$IP_UAD.$PA.161
        set netmask 255.255.255.224
        set interface "IF_ATM"
        config ip-range
            edit 1
                set start-ip 10.$IP_UAD.$PA.190
                set end-ip 10.$IP_UAD.$PA.190
            next
        end
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set default-gateway 10.$IP_UAD.$PA.129
        set netmask 255.255.255.224
        set interface "IF_DEVICES"
        config ip-range
            edit 1
                set start-ip 10.$IP_UAD.$PA.150
                set end-ip 10.$IP_UAD.$PA.158
            next
        end
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set default-gateway 10.$IP_UAD.$PA.193
        set netmask 255.255.255.224
        set interface "IF_SEG"
        config ip-range
            edit 1
                set start-ip 10.$IP_UAD.$PA.194
                set end-ip 10.$IP_UAD.$PA.222
            next
        end
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set default-gateway 10.$IP_UAD.$PA.225
        set netmask 255.255.255.224
        set interface "IF_VOIP"
        config ip-range
            edit 1
                set start-ip 10.$IP_UAD.$PA.226
                set end-ip 10.$IP_UAD.$PA.254
            next
        end
        set dns-server1 $IP_SRV_UAD
        set dns-server2 10.209.4.10
    next
    edit 0
        set lease-time 0
        set ntp-service default
        set default-gateway 10.252.252.1
        set netmask 255.255.255.0
        set interface "IF_WLAN_GUEST"
        config ip-range
            edit 1
                set start-ip 10.252.252.10
                set end-ip 10.252.252.254
            next
        end
        set timezone-option default
        set dns-server1 8.8.8.8
        set dns-server2 1.1.1.1
    next
end

#######SD-WAN ZONE######
config system sdwan
    set status enable
    config zone
        edit "virtual-wan-link"
        next
        edit "SD-WAN_2009"
        next
        edit "SD-WAN_$UAD_UAD"
        next
    end
end """
###### VPNs ########
    if configurar_wan1 == 's':
        configuracao += """
    ###PHASE 1##### 
    config vpn ipsec phase1-interface
    edit "VPN01_ST01_2009"
        set type ddns
        set interface "wan"
        set ike-version 2
        set peertype any
        set net-device disable
        set proposal aes256-sha512
        set localid "VPN01_$UAD_$PA"
        set dhgrp 14
        set remotegw-ddns "vpn01.sicoobunicoob.com.br"
        set psksecret ENC ATIbVSAFRf90pRrl97RPPXuXs5uLFuxWkrfjjf0TV2XLm0tIyfbPF9pBMl9grj9wk3cAF86fLgfFRt3MEmn9lo9KPOzkxnITqjL/GoE8vldVSuc/azRwSxSXrdyJkpi8C6IM3RhDcaNNX56R0Fwyb+ARQfBHwEby/V13LIFWlWfxIi8lCmS4FktGXhkzRqiw2zSXsQ==
    next 
    edit "VPN01_$UAD_UAD"
        set type ddns
        set interface "wan"
        set ike-version 2
        set peertype any
        set net-device disable
        set proposal aes256-sha512
        set localid "VPN01_$UAD_$PA"
        set dhgrp 14
        set remotegw-ddns "vpn01-$UAD.sicoobunicoob.com.br"
        set psksecret ENC 7/Z8D9z1jTiEtveyuxot6l0lpsxXzhiVil9iMOwwwvdUBCUkoTnzx9Oit6YRjv524BBVwocpVTlrZaAx3UYKDQ1qjYsFA8r7vRcQSOe4njh2Z5uXtfeCQUofqgGx/fV0dNuKaAuirvsvIkf48oNn3UeTvg0DIpz8YrTbeS0wXo+7jBeq2vQ9iIRIDvwfI4U2ZUJB6w==
    next
    end
    ###PHASE 2#####
    config vpn ipsec phase2-interface
    edit "VPN01_ST01_2009"
        set phase1name "VPN01_ST01_2009"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 10.$IP_UAD.$PA.0 255.255.255.0
    next
    edit "VTI_VPN01_2009"
        set phase1name "VPN01_ST01_2009"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 169.254.70.$VTI_2009 255.255.255.255
    next
    edit "VPN01_$UAD_UAD"
        set phase1name "VPN01_$UAD_UAD"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 10.$IP_UAD.$PA.0 255.255.255.0
    next
    edit "VTI_VPN01_$UAD_$PA"
        set phase1name "VPN01_$UAD_UAD"
        set proposal aes256-sha512
        set auto-negotiate enable
        set src-subnet 169.254.200.$PA 255.255.255.255
    next
    end
     config system sdwan
     config members
      edit 52
            set interface "VPN01_ST01_2009"
            set zone "SD-WAN_2009"    
        next
        edit 55
            set interface "VPN01_$UAD_UAD"
            set zone "SD-WAN_$UAD_UAD"
        next
        end 
        end """
    if configurar_wan2 == 's':
        configuracao += """
    ###PHASE 1##### 
    config vpn ipsec phase1-interface    
    edit "VPN02_ST01_2009"
        set type ddns
        set interface "a"
        set ike-version 2
        set peertype any
        set net-device disable
        set proposal aes256-sha512
        set localid "VPN02_$UAD_$PA"
        set dhgrp 14
        set remotegw-ddns "vpn02.sicoobunicoob.com.br"
        set psksecret ENC VKqNcbVyhnCLaKnDqHf3KNbozdIJbS3kzpOSz87+H6jiy9hXKGAV1kLaRWOBjEovMU1i8weGnXSXqyrV7PRIRBqP6PcAo82B5mQpC8A/SM6SXxm6qHREzDU6Zp4Z5H+33GJWQkjO6jATuUJ55tlY0dH7GmgoAih/1ND5HmAkyRiShsmhZfPq7GB1J49rhy6WidHc/A==
    next 
    edit "VPN02_$UAD_UAD"
        set type ddns
        set interface "a"
        set ike-version 2
        set peertype any
        set net-device disable
        set proposal aes256-sha512
        set localid "VPN02_$UAD_$PA"
        set dhgrp 14
        set remotegw-ddns "vpn02-$UAD.sicoobunicoob.com.br"
        set psksecret ENC 3/+edsvc+B1axzeZiNwViZr5Spu/fc15A3g+Ld5gIog1vMcrBXdGcXP/MXb2MjpzJBVXoeZsLDje22BNT65DxUUvkuujsmQerqr8wsQ0bkJE1rjb5klx78ilym1t6+4BO1tET64gU2M7HQxDiDrXhwsyakZIYMXS17+MCZpGDKRbPG8lFiXYBp2FsJFCbfIpa2caGg==
    next
    end
    ###PHASE 2#####
    config vpn ipsec phase2-interface
    edit "VPN02_ST01_2009"
        set phase1name "VPN02_ST01_2009"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 10.$IP_UAD.$PA.0 255.255.255.0
    next
    edit "VTI_VPN02_2009"
        set phase1name "VPN02_ST01_2009"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 169.254.90.$VTI_2009 255.255.255.255
    next
    edit "VPN02_$UAD_UAD"
        set phase1name "VPN02_$UAD_UAD"
        set proposal aes128-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 10.$IP_UAD.$PA.0 255.255.255.0
    next
    edit "VTI_VPN02_$UAD"
        set phase1name "VPN02_$UAD_UAD"
        set proposal aes256-sha512
        set dhgrp 14
        set auto-negotiate enable
        set src-subnet 169.254.210.$PA 255.255.255.255
    next
    end 
    config system sdwan
     config members
      edit 53
            set interface "VPN02_ST01_2009"
            set zone "SD-WAN_2009"    
        next
       edit 56
            set interface "VPN02_$UAD_UAD"
            set zone "SD-WAN_$UAD_UAD"
        next 
        end 
        end """
   
    configuracao += """    
######SD-WAN MEMBERS#####
config system sdwan
   config members
        edit 50
            set interface "wan"
            set gateway $GW_WAN01
        next
        edit 51
            set interface "a"
            set gateway $GW_WAN02
        next
        end
end
######## HEALTH CHECKS ########
config system sdwan
   config health-check
        edit "PROBE_INTERNET"
            set server "8.8.8.8" "1.1.1.1"
            set members 50 51
            config sla
                edit 1
                    set latency-threshold 60
                    set jitter-threshold 40
                    set packetloss-threshold 5
                next
            end
        next
        edit "PROBE_VPN02_2009"
            set server "169.254.90.1"
            set members 53
            config sla
                edit 1
                    set link-cost-factor latency packet-loss
                    set latency-threshold 60
                    set packetloss-threshold 3
                next
            end
        next
        edit "PROBE_VPN01_2009"
            set server "169.254.70.1"
            set members 52
            config sla
                edit 1
                    set link-cost-factor latency packet-loss
                    set latency-threshold 60
                    set packetloss-threshold 3
                next
            end
        next
        edit "PROBE_VPN01_$UAD_UAD"
            set server "169.254.200.1"
            set members 54
            config sla
                edit 1
                    set latency-threshold 90
                    set jitter-threshold 40
                    set packetloss-threshold 5
                next
            end
        next
        edit "PROBE_VPN02_$UAD_UAD"
            set server "169.254.210.1"
            set members 55
            config sla
                edit 1
                    set latency-threshold 90
                    set jitter-threshold 40
                    set packetloss-threshold 5
                next
            end
        next
    end
end
######SD-WAN RULES########
config system sdwan
config service
        edit 0
            set name "REDE_BANCOOB"
            set mode sla
            set dst "REDE_BANCOOB"
            set src "IF_ATM address" "IF_LAN address" "IF_WLAN_CORP address"
            config sla
                edit "PROBE_VPN01_$UAD_UAD"
                    set id 1
                next
                edit "PROBE_VPN02_$UAD_UAD"
                    set id 1
                next
            end
            set priority-members 55 56
        next
        edit 0
            set name "REDE_UAD"
            set mode sla
            set dst "REDE_$UAD_UAD"
            set src "IF_ATM address" "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address" "IF_WLAN_CORP address"
            config sla
                edit "PROBE_VPN01_$UAD_UAD"
                    set id 1
                next
                edit "PROBE_VPN02_$UAD_UAD"
                    set id 1
                next
            end
            set priority-members 55 56
        next
        edit 0
            set name "REDE_2009"
            set mode sla
            set dst "REDE_2009" "REDE_BANCOOB"
            set src "IF_ATM address" "IF_LAN address" "IF_VOIP address" "IF_WLAN_CORP address" "IF_DEVICES address" "IF_SEG address"
            config sla
                edit "PROBE_VPN02_2009"
                    set id 1
                next
                edit "PROBE_VPN01_2009"
                    set id 1
                next
            end
            set priority-members 52 53
        next
        edit 0
            set name "Internet_Services"
            set mode sla
            set src "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address" "IF_WLAN_COLAB address" "IF_WLAN_CORP address" "IF_WLAN_GUEST address"
            set internet-service enable
            set internet-service-name "Microsoft-Skype_Teams" "Zoom.us-Zoom.Meeting" "Cisco-Webex"
            config sla
                edit "PROBE_INTERNET"
                    set id 1
                next
            end
            set priority-members 50 51
        next
        edit 0
            set name "Internet_Balance"
            set mode load-balance
            set dst "all"
            set src "IF_DEVICES address" "IF_SEG address" "IF_LAN address" "IF_VOIP address" "IF_WLAN_GUEST address" "IF_WLAN_COLAB address" "IF_WLAN_CORP address"
            config sla
                edit "PROBE_INTERNET"
                    set id 1
                next
            end
            set priority-members 50 51
        next
    end
end 
##### ROTAS ######
config router static
    edit 0
        set distance 1
        set sdwan-zone "virtual-wan-link"
    next
    edit 0
        set dst 10.209.0.0 255.255.0.0
        set distance 1
        set sdwan-zone "SD-WAN_2009"
    next
    edit 0
        set dst 172.16.0.0 255.255.0.0
        set distance 1
        set sdwan-zone "SD-WAN_2009"
    next
    edit 0
        set dst $SUBNET_UAD
        set distance 1
        set sdwan-zone "SD-WAN_$UAD_UAD"
    next
    edit 5
        set dst 172.16.0.0 255.255.0.0
        set distance 1
        set sdwan-zone "SD-WAN_$UAD_UAD"
    next
end
###### LDAP SERVERS ######
config user ldap
    edit "LDAP_2009"
        set server "10.209.4.10"
        set source-ip "10.$IP_UAD.$PA.1"
        set cnid "SAMAccountName"
        set dn "dc=unicoob,dc=local"
        set type regular
        set username "firewall$UAD@unicoob.local"
        set password ENC cGxfbMWJS9Fjr3HwmMTO3cpdm2YojxUcapK4mQs4Xn6DB4v0nc9d2Z5HuMgfTNZopWrrUOtssh1jZSOd2z6dD4xuTtsUk87fwJzCQXGFMOmFRmXwYSs0Q+0pojWGVunbhz3LAd7MXLI8+88U/wnxMtCcTamrSy8bFw6RNdjiIkmHnATAsw4r8G7SQi7HSCUQHtVXIw==
    next
    edit "LDAP_$UAD_UAD"
        set server "$IP_SRV_UAD"
        set source-ip "10.$IP_UAD.$PA.1"
        set cnid "SAMAccountName"
        set dn "dc=unicoob,dc=local"
        set type regular
        set username "firewall$UAD@unicoob.local"
        set password ENC cGxfbBTIAjt4kFx1xU9KM+JZli+fT+QwcX7Usbp8kTbDXBPYDBkHk8J2Smc4ULk4d0eaJH4LaDLvwf/etXgApQzpqKzup1SSdvDuflftBosq3vDRXJV5nst4wNdYk9+eMbssFcYUoojIM/OhLH6UI4Oymie2P/a05OF4wSuz5fJ8tjkvOwALAuGCRbWm8PmNPIjGZw==
    next
end
##### USER GROUPS#####
config user group
    edit "ADMIN_FIREWALL"
        set member "LDAP_2009" "LDAP_$UAD_UAD"
        config match
            edit 1
                set server-name "LDAP_2009"
                set group-name "CN=GP 2009 00 Acesso Fortigate Admin,OU=Fortigate,OU=SAML,OU=Grupos Especiais,DC=unicoob,DC=local"
            next
            edit 2
                set server-name "LDAP_$UAD_UAD"
                set group-name "CN=GP 2009 00 Acesso Fortigate Admin,OU=Fortigate,OU=SAML,OU=Grupos Especiais,DC=unicoob,DC=local"
            next
        end
    next
end
###### SYSTEM########
####ADMINISTRATORS######
config system admin
    edit "ADM_FIREWALL"
        set remote-auth enable
        set trusthost1 10.209.4.0 255.255.255.0
        set trusthost2 10.209.34.0 255.255.255.0
        set trusthost3 $IP_SRV_UAD 255.255.255.255
        set trusthost4 10.209.28.0 255.255.255.0
        set trusthost5 10.209.38.0 255.255.255.255
        set accprofile "super_admin"
        set vdom "root"
        set wildcard enable
        set remote-group "ADMIN_FIREWALL"
    next
    edit "admin"
        set trusthost1 10.209.4.0 255.255.255.0
        set trusthost2 10.209.34.0 255.255.255.0
        set trusthost3 $IP_SRV_UAD 255.255.255.255
        set trusthost4 10.209.28.0 255.255.255.0
        set trusthost5 10.209.38.0 255.255.255.0
        set trusthost6 192.168.0.0 255.255.0.0
        set accprofile "super_admin"
        set vdom "root"
    next
end
####SETTINGS#####
config system global
    set alias "$HOSTNAME"
    set hostname "$HOSTNAME"
    set switch-controller enable
    set timezone 18
end
config system password-policy
    set status enable
    set minimum-length 15
    set min-lower-case-letter 1
    set min-upper-case-letter 1
    set min-non-alphanumeric 1
    set min-number 1
    set expire-status enable
    set expire-day 45
end
##### SNMP #####
config system snmp sysinfo
    set status enable
    set description "$HOSTNAME"
end
config system snmp community
    edit 1
        set name "S0n!cW@!!_SD-WAN"
        config hosts
            edit 1
                set ip 10.209.4.142 255.255.255.255
            next
            edit 2
                set ip 10.209.4.32 255.255.255.255
            next
        end
    next
end
####FSSO#####
config user fsso
    edit "FSSO_$HOSTNAME_SRV"
        set server "$IP_SRV_UAD"
        set password ENC as4poiWTPjrBiJ5KBecwClgW84OL37J0335fmkkFfcS1KI0+uaLook1GiV2Vw28Mv6/AAj+JKQmSJafbFX7GueCFWE9Cu0juPd8AnIp6OQwEKvAEv06RUINP4GUV8LIGWMeRGB7sWKsNl18QQPiy4UPb0OFrKcckoHL1eiA3fRZ+r2S+R9hfUo/VMjNr1NPaRdqMBw==
        set ldap-server "LDAP_$UAD_UAD"
        set source-ip 10.$IP_UAD.$PA.1
    next
end
####OBJECTS######
config firewall address
    edit "IF_LAN address"
        set type interface-subnet
        set subnet 10.$IP_UAD.$PA.0 255.255.255.128
        set interface "IF_LAN"
    next
    edit "IF_DEVICES address"
        set type interface-subnet
        set subnet 10.$IP_UAD.$PA.128 255.255.255.224
        set interface "IF_DEVICES"
    next
    edit "IF_ATM address"
        set type interface-subnet
        set subnet 10.$IP_UAD.$PA.160 255.255.255.224
        set interface "IF_ATM"
    next
    edit "IF_SEG address"
        set type interface-subnet
        set subnet 10.$IP_UAD.$PA.192 255.255.255.224
        set interface "IF_SEG"
    next
    edit "IF_VOIP address"
        set type interface-subnet
        set subnet 10.$IP_UAD.$PA.224 255.255.255.224
        set interface "IF_VOIP"
    next
    edit "REDE_2009"
        set subnet 10.209.0.0 255.255.0.0
    next
    edit "REDE_BANCOOB"
        set subnet 172.16.0.0 255.255.0.0
    next
    edit "Argentina"
        set type geography
        set country "AR"
    next
    edit "Brasil"
        set type geography
        set country "BR"
    next
    edit "Canada"
        set type geography
        set country "CA"
    next
    edit "GEO-IP_AkaMs"
        set type fqdn
        set fqdn "aka.ms"
    next
    edit "GEO-IP_Allianz"
        set type fqdn
        set fqdn "www.allianz.com.br"
    next
    edit "GEO-IP_Allianznet"
        set type fqdn
        set fqdn "allianznet.com.br"
    next
    edit "GEO-IP_Booking.com"
        set type fqdn
        set fqdn "booking.com"
    next
    edit "GEO-IP_CarGov"
        set type fqdn
        set fqdn "car.gov.br"
    next
    edit "GEO-IP_CarGov-WWW"
        set type fqdn
        set fqdn "www.car.gov.br"
    next
    edit "GEO-IP_CreditoPepa"
        set type fqdn
        set fqdn "creditorural.apepa.com.br"
    next
    edit "GEO-IP_Decolar.com"
        set type fqdn
        set fqdn "decolar.com"
    next
    edit "GEO-IP_Emfocofrisia"
        set type fqdn
        set fqdn "emfoco.frisia.coop.br"
    next
    edit "GEO-IP_Oicontasb2b"
        set type fqdn
        set fqdn "oicontasb2b.com.br"
    next
    edit "GEO-IP_Opepa"
        set type fqdn
        set fqdn "apepa.com.br"
    next
    edit "GEO-IP_PHBSolar"
        set type fqdn
        set fqdn "phbsolar.com.br"
    next
    edit "GEO-IP_SancorSeguros"
        set type fqdn
        set fqdn "mkt.sancorsegurosbrasil.com.br"
    next
    edit "GEO-IP_SolarManpv"
        set type fqdn
        set fqdn "solarmanpv.com"
    next
    edit "GEO-IP_TeamViewer"
        set type fqdn
        set fqdn "*.teamviewer.com"
    next
    edit "GEO-IP_Templatetrack"
        set type fqdn
        set fqdn "templatetrack-sicoob.azurewebsites.net"
    next
    edit "GEO-IP_biolinky.co"
        set type fqdn
        set fqdn "biolinky.co"
    next
    edit "GEO-IP_googleapis"
        set type fqdn
        set fqdn "googleapis.com"
    next
    edit "GEO-IP_jsdelivr"
        set type fqdn
        set fqdn "cdn.jsdelivr.net"
    next 
    edit "GEO-IP_officeapp"
        set type fqdn
        set fqdn "c2rsetup.officeapps.live.com"
    next
    edit "HOST_SRV_MGFSRF001"
        set subnet 10.209.4.10 255.255.255.255
    next
    edit "HOST_SRV_MGFSRV001"
        set subnet 10.209.4.6 255.255.255.255
    next
    edit "HOST_SRV_MGFSRV002"
        set subnet 10.209.4.9 255.255.255.255
    next
    edit "HOST_SRV_MGFSRV003"
        set subnet 10.209.4.5 255.255.255.255
    next
    edit "HOST_SRV_SIGA"
        set subnet 10.209.255.109 255.255.255.255
    next
    edit "IF_WLAN_COLAB address"
        set type interface-subnet
        set subnet 10.251.251.0 255.255.255.0
        set interface "IF_WLAN_COLAB"
    next
    edit "IF_WLAN_CORP address"
        set type interface-subnet
        set subnet 10.250.250.0 255.255.255.0
        set interface "IF_WLAN_CORP"
    next
    edit "IF_WLAN_GUEST address"
        set type interface-subnet
        set subnet 10.252.252.0 255.255.255.0
        set interface "IF_WLAN_GUEST"
    next
    edit "REDE_$UAD_UAD"
        set subnet 10.$IP_UAD.240.0 255.255.240.0
    next
    edit "USA"
        set type geography
        set country "US"
    next
    edit "lan2 address"
        set type interface-subnet
        set subnet 10.253.253.0 255.255.255.0
        set interface "lan2"
    next
    edit "FCTEMS_ALL_FORTICLOUD_SERVERS"
        set type dynamic
        set sub-type ems-tag
    next
    edit "$HOSTNAME_SRV"
        set subnet $IP_SRV_UAD 255.255.255.255
    next
end
config firewall addrgrp
    edit "GRP_SRV_ADs"
        set member "HOST_SRV_MGFSRF001" "HOST_SRV_MGFSRV001" "HOST_SRV_MGFSRV002" "HOST_SRV_MGFSRV003"
    next
    edit "GRP_GEOIP_Countries"
        set member "Argentina" "Brasil" "Canada" "USA"
    next
    edit "GRP_GEOIP_Address"
        set member "GEO-IP_AkaMs" "GEO-IP_Allianz" "GEO-IP_Allianznet" "GEO-IP_biolinky.co" "GEO-IP_Booking.com" "GEO-IP_CarGov" "GEO-IP_CarGov-WWW" "GEO-IP_CreditoPepa" "GEO-IP_Decolar.com" "GEO-IP_Emfocofrisia" "GEO-IP_googleapis" "GEO-IP_jsdelivr" "GEO-IP_officeapp" "GEO-IP_Oicontasb2b" "GEO-IP_Opepa" "GEO-IP_PHBSolar" "GEO-IP_SancorSeguros" "GEO-IP_SolarManpv" "GEO-IP_TeamViewer" "GEO-IP_Templatetrack" "GRP_GEOIP_Countries"
    next
end
config firewall internet-service-group
    edit "GRP_SERVICES_APP_BOTH"
        set member "Google-Google.Cloud" "Google-Gmail" "Apple-APNs" "Microsoft-Skype_Teams" "Microsoft-Azure" "Microsoft-Outlook" "Microsoft-Dynamics" "Microsoft-WNS" "Microsoft-Office365.Published" "Microsoft-Office365.Published.Optimize" "Microsoft-Office365.Published.Allow" "Microsoft-Office365.Published.USGOV" "Amazon-AWS" "Amazon-AWS.GovCloud.US" "Amazon-Amazon.SES" "Adobe-Adobe.Sign" "Oracle-Oracle.Cloud" "Cisco-Meraki.Cloud" "Cisco-Secure.Endpoint" "GitHub-GitHub" "Cloudflare-CDN" "Akamai-CDN"
    next
    edit "GRP_SERVICES_APP_DST"
        set direction destination
        set member "Google-Other" "Google-Web" "Google-ICMP" "Google-DNS" "Google-Outbound_Email" "Google-SSH" "Google-FTP" "Google-NTP" "Google-Inbound_Email" "Google-LDAP" "Google-NetBIOS.Session.Service" "Google-RTMP" "Google-NetBIOS.Name.Service" "Meta-Other" "Meta-Web" "Meta-ICMP" "Meta-DNS" "Meta-Outbound_Email" "Meta-SSH" "Meta-FTP" "Meta-NTP" "Meta-Inbound_Email" "Meta-LDAP" "Meta-NetBIOS.Session.Service" "Meta-RTMP" "Meta-NetBIOS.Name.Service" "Meta-Whatsapp" "Meta-Instagram" "Apple-Other" "Apple-Web" "Apple-ICMP" "Apple-DNS" "Apple-Outbound_Email" "Apple-SSH" "Apple-FTP" "Apple-NTP" "Apple-Inbound_Email" "Apple-LDAP" "Apple-NetBIOS.Session.Service" "Apple-RTMP" "Apple-NetBIOS.Name.Service" "Apple-App.Store" "Amazon-AWS.WorkSpaces.Gateway" "Microsoft-Other" "Microsoft-Web" "Microsoft-ICMP" "Microsoft-DNS" "Microsoft-Outbound_Email" "Microsoft-SSH" "Microsoft-FTP" "Microsoft-NTP" "Microsoft-Inbound_Email" "Microsoft-LDAP" "Microsoft-NetBIOS.Session.Service" "Microsoft-RTMP" "Microsoft-NetBIOS.Name.Service" "Microsoft-Office365" "Microsoft-Microsoft.Update" "Microsoft-Intune" "TeamViewer-Other" "TeamViewer-Web" "TeamViewer-ICMP" "TeamViewer-DNS" "TeamViewer-Outbound_Email" "TeamViewer-SSH" "TeamViewer-FTP" "TeamViewer-NTP" "TeamViewer-Inbound_Email" "TeamViewer-LDAP" "TeamViewer-NetBIOS.Session.Service" "TeamViewer-RTMP" "TeamViewer-NetBIOS.Name.Service" "TeamViewer-TeamViewer" "Telegram-Telegram" "Bitdefender-Other" "Bitdefender-Web" "Bitdefender-ICMP" "Bitdefender-DNS" "Bitdefender-Outbound_Email" "Bitdefender-SSH" "Bitdefender-FTP" "Bitdefender-NTP" "Bitdefender-Inbound_Email" "Bitdefender-LDAP" "Bitdefender-NetBIOS.Session.Service" "Bitdefender-RTMP" "Bitdefender-NetBIOS.Name.Service" "Cloudflare-Web" "Cloudflare-ICMP" "Cloudflare-DNS" "Cloudflare-NetBIOS.Session.Service" "Cloudflare-NetBIOS.Name.Service" "Cisco-Other" "Cisco-Web" "Cisco-ICMP" "Cisco-DNS" "Cisco-Outbound_Email" "Cisco-SSH" "Cisco-FTP" "Cisco-NTP" "Cisco-Inbound_Email" "Cisco-LDAP" "Cisco-NetBIOS.Session.Service" "Cisco-RTMP" "Cisco-NetBIOS.Name.Service" "Cisco-Webex" "Cisco-Duo.Security" "Cisco-AppDynamic" "Cisco-Webex.FedRAMP" "Fortinet-Other" "Fortinet-Web" "Fortinet-ICMP" "Fortinet-DNS" "Fortinet-Outbound_Email" "Fortinet-SSH" "Fortinet-FTP" "Fortinet-NTP" "Fortinet-Inbound_Email" "Fortinet-LDAP" "Fortinet-NetBIOS.Session.Service" "Fortinet-RTMP" "Fortinet-NetBIOS.Name.Service" "Fortinet-FortiGuard" "Fortinet-FortiMail.Cloud" "Fortinet-FortiCloud" "Fortinet-FortiVoice.Cloud" "Fortinet-FortiGuard.Secure.DNS" "Fortinet-FortiEDR" "Fortinet-FortiClient.EMS"
    next
    end
    ##### IP POOL ####
    config firewall ippool
    edit "NAT_MERAKI_CORP"
        set startip 10.$IP_UAD.$PA.2
        set endip 10.$IP_UAD.$PA.2
    next
    end
    ###### POLICY ######
        config firewall policy
    edit 0
        set name "ZN_LAN_ATM to SD-WAN_$UAD_UAD"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_$UAD_UAD"
        set action accept
        set srcaddr "IF_ATM address"
        set dstaddr "REDE_BANCOOB"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "ZN_LAN to SD-WAN_$UAD_UAD"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_$UAD_UAD"
        set action accept
        set srcaddr "IF_LAN address" "IF_VOIP address"
        set dstaddr "REDE_$UAD_UAD" "REDE_BANCOOB"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "IF_WLAN_CORP to SD-WAN_$UAD_UAD"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_$UAD_UAD"
        set action accept
        set srcaddr "IF_WLAN_CORP address"
        set dstaddr "REDE_BANCOOB" "REDE_$UAD_UAD"
        set schedule "always"
        set service "ALL"
        set nat enable
        set ippool enable
        set poolname "NAT_MERAKI_CORP"
    next
    edit 0
        set name "SD-WAN_$UAD_UAD to ZN_LAN"
        set srcintf "SD-WAN_$UAD_UAD"
        set dstintf "ZN_LAN"
        set action accept
        set srcaddr "REDE_$UAD_UAD"
        set dstaddr "IF_ATM address" "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "IF_WLAN_MGMT to SD-WAN_$UAD_UAD"
        set srcintf "lan2"
        set dstintf "SD-WAN_$UAD_UAD"
        set action accept
        set srcaddr "lan2 address"
        set dstaddr "$HOSTNAME_SRV"
        set schedule "always"
        set service "RADIUS"
        set nat enable
        set ippool enable
        set poolname "NAT_MERAKI_CORP"
    next 
    edit 0
        set name "ZN_LAN to SD-WAN_$UAD_UAD_DENY"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_$UAD_UAD"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ZN_LAN to SD-WAN_2009_DNS"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_2009"
        set action accept
        set srcaddr "IF_ATM address" "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address"
        set dstaddr "GRP_SRV_ADs"
        set schedule "always"
        set service "DNS" "PING"
    next
    edit 0
        set name "ZN_LAN_ATM to SD-WAN_2009"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_2009"
        set action accept
        set srcaddr "IF_ATM address"
        set dstaddr "REDE_BANCOOB"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "ZN_LAN to SD-WAN_2009"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_2009"
        set action accept
        set srcaddr "IF_LAN address" "IF_VOIP address"
        set dstaddr "REDE_2009" "REDE_BANCOOB"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "SD-WAN_2009 to ZN_LAN"
        set srcintf "SD-WAN_2009"
        set dstintf "ZN_LAN"
        set action accept
        set srcaddr "REDE_2009"
        set dstaddr "IF_ATM address" "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address"
        set schedule "always"
        set service "ALL"
    next
    edit 0
        set name "IF_WLAN_CORP to SD-WAN_2009"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_2009"
        set action accept
        set srcaddr "IF_WLAN_CORP address"
        set dstaddr "REDE_2009" "REDE_BANCOOB"
        set schedule "always"
        set service "ALL"
        set nat enable
        set ippool enable
        set poolname "NAT_MERAKI_CORP"
    next
    edit 0
        set name "ZN_LAN to SD-WAN_2009_DENY"
        set srcintf "ZN_LAN"
        set dstintf "SD-WAN_2009"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "IF_WLAN_MGMT to WAN"
        set srcintf "lan2"
        set dstintf "virtual-wan-link"
        set action accept
        set srcaddr "lan2 address"
        set internet-service enable
        set internet-service-name "Cisco-Meraki.Cloud" "Cloudflare-DNS" "Cloudflare-Other" "Cloudflare-Web" "Google-DNS" "Google-ICMP" "Cisco-Web"
        set schedule "always"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set webfilter-profile "default"
        set dnsfilter-profile "default"
        set nat enable
    next
    edit 0
        set name "ZN_GUEST to WAN_SERVICES"
        set srcintf "ZN_GUEST"
        set dstintf "virtual-wan-link"
        set action accept
        set srcaddr "IF_WLAN_COLAB address" "IF_WLAN_GUEST address"
        set internet-service enable
        set internet-service-group "GRP_SERVICES_APP_BOTH" "GRP_SERVICES_APP_DST"
        set schedule "always"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set webfilter-profile "default"
        set dnsfilter-profile "default"
        set application-list "default"
        set logtraffic all
        set nat enable
    next
    edit 0
        set name "ZN_GUEST to WAN"
        set srcintf "ZN_GUEST"
        set dstintf "virtual-wan-link"
        set action accept
        set srcaddr "IF_WLAN_COLAB address" "IF_WLAN_GUEST address"
        set dstaddr "GRP_GEOIP_Address" "GRP_GEOIP_Countries"
        set schedule "always"
        set service "ALL"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set av-profile "default"
        set webfilter-profile "default"
        set dnsfilter-profile "default"
        set ips-sensor "default"
        set application-list "default"
        set logtraffic all
        set nat enable
    next
    edit 0
        set name "ZN_GUEST to WAN_DENY"
        set srcintf "ZN_GUEST"
        set dstintf "virtual-wan-link"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ZN_LAN to WAN_SERVICES"
        set srcintf "ZN_LAN"
        set dstintf "virtual-wan-link"
        set action accept
        set srcaddr "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address" "IF_WLAN_CORP address"
        set internet-service enable
        set internet-service-group "GRP_SERVICES_APP_BOTH" "GRP_SERVICES_APP_DST"
        set schedule "always"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set webfilter-profile "default"
        set dnsfilter-profile "default"
        set logtraffic all
        set nat enable
    next
    edit 0
        set name "ZN_LAN to WAN"
        set srcintf "ZN_LAN"
        set dstintf "virtual-wan-link"
        set action accept
        set srcaddr "IF_DEVICES address" "IF_LAN address" "IF_SEG address" "IF_VOIP address" "IF_WLAN_CORP address"
        set dstaddr "GRP_GEOIP_Address" "GRP_GEOIP_Countries"
        set schedule "always"
        set service "ALL"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set av-profile "default"
        set webfilter-profile "default"
        set dnsfilter-profile "default"
        set ips-sensor "default"
        set application-list "default"
        set logtraffic all
        set nat enable
    next
    edit 0
        set name "ZN_LAN to WAN_DENY"
        set srcintf "ZN_LAN"
        set dstintf "virtual-wan-link"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ZN_LAN to ZN_LAN_DENY"
        set srcintf "ZN_LAN"
        set dstintf "ZN_LAN"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    end """     
    
    # Substituir variáveis no modelo de configuração
    configuracao_final = substituir_variaveis(configuracao, variaveis)

    # Salvar o arquivo de configuração
    nome_arquivo = input("Digite o nome do arquivo de configuração: ")
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write(configuracao_final)

    print(f"Arquivo de configuração {nome_arquivo} gerado com sucesso.")
else:
    print("Nenhum bloco configurado. Encerrando o programa.")
