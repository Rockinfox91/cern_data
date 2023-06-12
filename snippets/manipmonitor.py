import socket
import sys
import time
from datetime import datetime

PROG = "ManMon"
MAX_AXES = 4  # Umbilical + 3 axes

buff = bytearray(4096)
sbuff = bytearray(4096)
tbuff = bytearray(64)

command = None
log_file = None
poly_object = None
m_term = None

Axes = [None] * (MAX_AXES + 1)  # Make sure we can NULL terminate list
Modes = [bytearray(16) for _ in range(MAX_AXES)]

verbose = 0x0
interval = 500
ibin = 0
Np = 10000
expert = 0x0

dt = 100
rl = [0.0] * MAX_AXES
ts = [0.0] * MAX_AXES
err = [0.0] * MAX_AXES
vel = [0.0] * MAX_AXES
steps = [0.0] * MAX_AXES
stretch = [0.0] * MAX_AXES
z, f, sum, serr = 0.0, 0.0, 0.0, 0.0
ts_frac = 0.0
total = -99999999

t, t1, t_x = 0, 0, 0
usec = 10000
server_addr = None

s_buff = None

fp = None

l_opt = [
    {"name": "-log_file", "type": str, "value": log_file},
    {"name": "-poly_object", "type": str, "value": poly_object},
    {"name": "-interval", "type": int, "value": interval},
    {"name": "-command", "type": str, "value": command},
    {"name": "-time", "type": float, "value": dt},
    {"name": "-points", "type": int, "value": Np},
    {"name": "-verbose", "type": bool, "value": verbose},
    {"name": "-total", "type": float, "value": total},
    {"name": "-expert", "type": bool, "value": expert},
    {"name": "-terminate", "type": str, "value": m_term},
]


def parseOptions(argv, l_opt):
    global log_file, poly_object, interval, command, dt, Np, verbose, total, expert, m_term

    for i in range(1, len(argv)):
        if argv[i] == "-log_file":
            log_file = argv[i + 1]
        elif argv[i] == "-poly_object":
            poly_object = argv[i + 1]
        elif argv[i] == "-interval":
            interval = int(argv[i + 1])
        elif argv[i] == "-command":
            command = argv[i + 1]
        elif argv[i] == "-time":
            dt = float(argv[i + 1])
        elif argv[i] == "-points":
            Np = int(argv[i + 1])
        elif argv[i] == "-verbose":
            verbose = bool(argv[i + 1])
        elif argv[i] == "-total":
            total = float(argv[i + 1])
        elif argv[i] == "-expert":
            expert = bool(argv[i + 1])
        elif argv[i] == "-terminate":
            m_term = argv[i + 1]


parseOptions(sys.argv, l_opt)

if not poly_object:
    print(f"{PROG} : No POLY object to monitor")
    sys.exit(1)

# Ouverture du fichier journal
if log_file:
    fp = open(log_file, "a")
    if not fp:
        print(f"{PROG} : Unable to open log file {log_file}")
        sys.exit(1)

# Connexion au serveur
try:
    server_addr = socket.gethostbyname(poly_object)
except socket.error:
    print(f"{PROG} : Unknown host: {poly_object}")
    sys.exit(1)

# Configuration du socket
s_buff = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_buff.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_buff.settimeout(5)

# Connexion au serveur
try:
    s_buff.connect((server_addr, 2000))
except socket.error:
    print(f"{PROG} : Unable to connect to server {poly_object}")
    sys.exit(1)

# Boucle principale
while True:
    t1 = datetime.now()

    # Envoi de la commande au serveur
    if command:
        s_buff.sendall(command.encode())

    # Réception des données du serveur
    try:
        rbuff = s_buff.recv(4096)
    except socket.error:
        print(f"{PROG} : Lost connection to server {poly_object}")
        break

    # Traitement des données reçues
    for i in range(MAX_AXES):
        ax = Axes[i]
        mode = Modes[i]
        rbuff_ptr = 0

        # Lecture des données
        if expert:
            ax_err, ax_vel, ax_steps, ax_stretch, ax_ts, ax_rl, ax_mode = (
                struct.unpack("dddddB", rbuff[rbuff_ptr:rbuff_ptr + 37])
            )
            rbuff_ptr += 37
        else:
            ax_err, ax_vel, ax_steps, ax_stretch, ax_ts, ax_rl = (
                struct.unpack("ddddd", rbuff[rbuff_ptr:rbuff_ptr + 40])
            )
            rbuff_ptr += 40

        # Mise à jour des variables
        err[i] = ax_err
        vel[i] = ax_vel
        steps[i] = ax_steps
        stretch[i] = ax_stretch
        ts[i] = ax_ts
        rl[i] = ax_rl

        if expert:
            mode = ax_mode
        else:
            mode = 0

        Modes[i] = mode

    t_x += 1

    # Calcul de la somme des erreurs
    sum = 0.0
    for i in range(MAX_AXES):
        sum += err[i]

    # Calcul de la vitesse
    if t_x > 1:
        z = ts[0] - ts[1]
        if z != 0:
            f = (err[0] - err[1]) / z
        else:
            f = 0

    # Affichage des données
        if verbose:
            print(f"sum = {sum}, f = {f}")

        # Écriture des données dans le fichier journal
        if log_file and fp:
            log_entry = f"{t},{dt},{Np},{total},"
            for i in range(MAX_AXES):
                log_entry += f"{err[i]},{vel[i]},{steps[i]},{stretch[i]},{ts[i]},{rl[i]},{Modes[i]},"
            log_entry += f"{sum},{f}\n"
            fp.write(log_entry)

        # Vérification de la condition de sortie
        if t >= T:
            break

        # Pause pour atteindre le prochain intervalle de temps
        elapsed_time = (datetime.now() - t1).total_seconds()
        time_to_sleep = dt - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    # Fermeture du socket
    s_buff.close()

    # Fermeture du fichier journal
    if fp:
        fp.close()