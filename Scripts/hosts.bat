@echo off
echo ====================================
echo ===   sitereport.netcraft.com    ===
echo ====================================
notepad "C:\Windows\System32\drivers\etc\hosts"
rem Flush DNS cache
ipconfig /flushdns
