import psutil
import subprocess


def find_process_by_port(port):
    """
    Finds a process using a specific port (if any).
    Args:
        port: The port number to search for.
    Returns:
        A psutil.Process object or None if no process is found.
    """
    for process in psutil.process_iter():
        try:
            for conn in process.connections():
                if conn.laddr.port == port:
                    return process
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass  # Ignore errors

# port connection not working.


def close_port(port):
    '''
    reference of this code
    https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
    '''
    cmd = ['kill', '-9', str(port)]
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


# close_port()
# p = find_process_by_port(8005)
# print(p.as_dict())

#     '_send_signal', 'as_dict', 'children', 'cmdline', 'connections', 'cpu_affinity', 'cpu_num', 'cpu_percent', 'cpu_times', 'create_time', 'cwd', 'environ', 'exe', 'gids', 'io_counters', 'ionice', 'is_running', 'kill', 'memory_full_info', 'memory_info', 'memory_info_ex', 'memory_maps', 'memory_percent', 'name', 'nice', 'num_ctx_switches', 'num_fds', 'num_threads', 'oneshot', 'open_files', 'parent', 'parents', 'pid', 'ppid', 'resume', 'rlimit', 'send_signal', 'status', 'suspend', 'terminal', 'terminate', 'threads', 'uids', 'username', 'wait']
