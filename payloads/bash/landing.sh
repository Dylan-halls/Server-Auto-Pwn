function bash_sockets {
  exec 3<>/dev/tcp/192.168.1.65/4443; echo -e "bash landing..." >&3;
  return=\`cat <&3\`
  if [ $return == "succesful" ]; then
    bashSockets=true
  else
    bashSockets=false
  fi
}

function wget_check {
  rm landing...
  wget http://192.168.1.65:4443/landing...
  return=`cat landing...`
  if [ $return == 'succesful' ]; then
    wget_run=true
  else
    wget_run=false
  fi
}

#wget_check
bash_sockets
echo $bashSockets
#echo $wget_run
