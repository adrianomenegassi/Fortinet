<p class="callout inform">Esse documento tem como objetivo registrar os apontamentos de segurança realizados nas redes da Central, através da ferramenta Nessus, solicitação feita pela auditoria anual realiada pelo CCS.</p>

##### Redes alvo:
` 10.209.63.0/24 - Gerencia Rack03 de Acesso`<br/>
` 10.209.64.0/24 - Gerencia Rack04 de Acesso`<br/>
` 10.209.65.0/24 - Gerencia Rack05 de Acesso`<br/>
` 10.209.66.0/24 - Gerencia Rack06 de Acesso`<br/>
` 10.209.67.0/24 - Gerencia Rack07 de Acesso`<br/>
` 10.209.68.0/24 - Gerencia Rack08 de Acesso`<br/>
` 10.209.1.0/24 - Gerencia Site A`<br/>
` 10.199.1.0/24 - Gerencia Site B`<br/>


> ##### [Diretório do SharedPoint com todos relatórios e relação de equipamentos](https://sicoob.sharepoint.com/sites/SicoobUnicoob-SegurancaPrivacidade/Documentos%20Compartilhados/Forms/AllItems.aspx?csf=1&web=1&e=V5BRQO&ovuser=b417b620%2D2ae9%2D4a83%2Dab6c%2D7fbd828bda1d%2Cadriano%2Emesquita%40sicoob%2Ecom%2Ebr&OR=Teams%2DHL&CT=1712142936292&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDAyMjkyNDUxNyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&RootFolder=%2Fsites%2FSicoobUnicoob%2DSegurancaPrivacidade%2FDocumentos%20Compartilhados%2FGeneral%2FCiberseguran%C3%A7a%2FPROJETOS%2FVulnerabilidades%2FAuditoria%20CCS%202024%2FVLANs%2DGerenciamento&FolderCTID=0x01200060496EB528D546479EE8400EA62E1AED)


#### Vulnerabilidades - Switchs Cisco e HPe
<p class="callout danger">SSL Version 2 and 3 Protocol Detection</p>

```
Cisco#no ip http server
Cisco#no ip http secure-server
```
```
[hpe]no ip http enable
[hpe]no ip https enable
```
<p class="callout danger">SSL Medium Strength Cipher Suites Supported (SWEET32) <br/> SSL/TLS EXPORT_RSA <= 512-bit Cipher Suites Supported (FREAK)</p>

```
Cisco#ip ssh server algorithm encryption aes256-ctr aes128-ctr
Cisco#ip ssh server algorithm mac hmac-sha1
Cisco#no ip ssh server algorithm mac hmac-sha1-96
Cisco#no ip ssh server algorithm kex diffie-hellman-group-exchange-sha1
```
```
[hpe]ssh2 algorithm key-exchange ecdh-sha2-nistp256 ecdh-sha2-nistp384 dh-group14-sha1
[hpe]ssh2 algorithm cipher aes128-ctr aes192-ctr aes256-ctr
[hpe]ssh2 algorithm mac sha2-256 sha2-512 sha1
```
<p class="callout warning">Network Time Protocol (NTP) Mode 6 Scanner</p>

```
Cisco#access-list 90 deny   any
Cisco#access-list 91 permit 10.209.4.10
Cisco#access-list 91 permit 10.209.4.9
Cisco#ntp access-group peer 91
Cisco#ntp access-group serve 90
Cisco#ntp server 10.209.4.10 prefer
Cisco#ntp server 10.209.4.9
```
```
[hpe1920]acl number 2500
[hpe1920]rule permit source 10.209.4.10 0
[hpe1920]ntp-service access peer 2500
[hpe1920]ntp-service unicast-server 10.209.4.10 priority
```
```
[hpe5130]acl basic 2500
[hpe5130]rule 10 permit source 10.209.4.10 0
[hpe5130]ntp-service peer acl 2500
[hpe5130]ntp-service unicast-server 10.209.4.10 priority
``` 
<p class="callout warning">Unencrypted Telnet Server</p>

```
Cisco#line vty 0 4
Cisco#logging synchronous
Cisco#login local
Cisco#length 0
Cisco#transport input ssh
Cisco#line vty 5 15
Cisco#login local
Cisco#transport input ssh
```
```
[hpe]user-interface vty 0 4
[hpe]authentication-mode scheme   
[hpe]protocol inbound ssh
```
<p class="callout alert">SSL Weak Cipher Suites Supported</p>


> Essa é a unica vulnerabilidade (severidade BAIXA) que ficou pedente nos switchs cisco MGMT01 SiteA e Sw01 Rack 8.<br/> Entretanto a chave "KEX" nem possui nesses modelos, sendo um falso positico do scaner no Nessus. Entretanto até <br/> dia 08/06/2024 vamos tentar atualizar o firmware para deixa-los na ultima versão.

<br/><br/><br/><br/><br/>
