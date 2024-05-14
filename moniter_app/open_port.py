from psutil import process_iter, NoSuchProcess, AccessDenied
import subprocess


def find_process_by_port(port):
    """
    Finds a process using a specific port (if any).
    Args:
        port: The port number to search for.
    Returns:
        A psutil.Process object or None if no process is found.
    """
    for process in process_iter():
        try:
            for conn in process.connections():
                # print('process', conn)
                if conn.laddr.port == port:
                    result = close_port(conn.laddr.port)
                    return result
        except (NoSuchProcess, AccessDenied):

            pass  # Ignore errors

# port connection not working.


def close_port(port):
    '''
    reference of this code
    https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
    '''
    cmd = ['kill', '-9', f"($(lsof -t -i:{port}))"]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    o, e = proc.communicate()
    port_out = o.decode('ascii')
    port_error = e.decode('ascii')
    port_code = proc.returncode
    return (port_code, port_error, port_out)
